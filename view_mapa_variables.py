import tkinter as tk
import tkinter.messagebox
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
from scipy.interpolate import griddata

from model import Event
from view_base import ViewBase

class ViewMapaVariables(ViewBase):
    def __init__(self, parent, mediador_view):
        super().__init__(
            parent, 
            mediador_view, 
            titulo = "Mapa meteorologico", 
            size = '960x560')
        
        # Eventos: patrón Observer ############################
        self.btnBuscar = Event()
        self.btnSelect = Event()

        self.lista_btn = []
        
        # Referencias de elementos del mapa ###################
        self.colorbar = None
        self.cbar_ax = None
        self.fig = None 
        self.ax = None
        self.canvas = None 

        self.setup_ui()

    def setup_ui(self):
        """VENTANA PRINCIPAL TIENE DOS COLUMNAS: DERECHA (MAPA) - IZQUIERDA (CONTROLES)"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        # COLUMNA IZQUIERDA ################################
        self.columna_izq = tk.Frame(self, width=250, padx=10, pady=10) 
        self.columna_izq.grid(row=0, column=0, sticky="nsew")
        self.columna_izq.grid_propagate(False)
        self.columna_izq.grid_columnconfigure(0, weight=1)
        # Elementos 
        self.label_instruccion = tk.Label(self.columna_izq, text="Introduzca País")
        self.entry_pais = tk.Entry(self.columna_izq, width=25)
        btn_buscar_pais = tk.Button(self.columna_izq, text="Mostrar país", command=lambda: self.actualizar_lista_paises())
        # Organización
        self.label_instruccion.grid(row=0, column=0, sticky="w")
        self.entry_pais.grid(row=1, column=0, sticky="ew")
        btn_buscar_pais.grid(row=2, column=0, pady=5, sticky="ew")


        # COLUMNA DERECHA ##################################
        self.columna_der= tk.Frame(self)
        self.columna_der.grid(row=0, column=1, sticky="nsew")
        # Elementos y organización 
        self._inicializar_mapa()

    def _inicializar_mapa(self):
        """Método que crea la figura (fig), los ejes (ax) con preoyección y el canvas"""
        self.proyeccion = ccrs.PlateCarree()
        self.fig, self.ax = plt.subplots(figsize=(5.5, 5.5), dpi=100, subplot_kw={'projection': self.proyeccion})
        self.fig.subplots_adjust(bottom=0.18, top=0.94, left=0.10, right=0.95)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.columna_der)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def entrada(self):
        """Método que toma el texto de Entry."""
        return self.entry_pais.get()
    
    def actualizar_lista_paises(self):
        self.btnBuscar.emit()
    
    def mostrar_lista_paises(self, lista):
        self.limpiar_lista_paises()
        for n, nombre_pais in enumerate(lista):
            boton = tk.Button(
                self.columna_izq,
                text=nombre_pais,
                command=lambda nombre_pais=nombre_pais: self.seleccionar_pais(nombre_pais)
            )
            boton.grid(row=n+3, column=0, pady=2)
            self.lista_btn.append(boton)
    
    def seleccionar_pais(self, nombre_pais):
        self.btnSelect.emit(nombre_pais)
        self.limpiar_lista_paises()

    def limpiar_lista_paises(self):
        """Método que borra la lista de botones."""
        for boton in self.lista_btn:
            boton.destroy()
        self.lista_btn.clear()

    def actualizar_mapa(self, lons_array, lats_array, 
                        lon_min, lon_max, 
                        lat_min, lat_max,
                        grid_x, grid_y, grid_z,
                        nombre_pais, geometria_pais):  
        
        if self.fig is None or self.ax is None:
            self._inicializar_mapa()
        
        self.limpiar_mapa()

        # Fijar los límites establecidos ###########################################
        self.ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=self.proyeccion)
        
        # Características geográficas: líneas de cosa, tierra, bordes ##############
        self.ax.add_feature(cfeature.COASTLINE.with_scale('10m'), edgecolor='black', linewidth=1.5)
        self.ax.add_feature(cfeature.BORDERS.with_scale('10m'), linestyle=':', edgecolor='black')
        self.ax.add_feature(cfeature.LAND.with_scale('10m'), facecolor='#f5f5f5')
        self.ax.add_feature(cfeature.OCEAN.with_scale('10m'), facecolor="#3980d6", alpha=0.7)
    
        # Mapa de calor isotermas ##################################################
        cp = self.ax.contourf(
            grid_x, grid_y, grid_z, 
            levels=15, 
            cmap='RdYlBu_r',
            alpha=0.6, 
            transform=self.proyeccion
            )
        lineas = self.ax.contour(
            grid_x, grid_y, grid_z, 
            levels=10, 
            colors='black',
            linewidths=0.5, 
            alpha=0.5,
            transform=self.proyeccion
            )
    
        self.ax.clabel(lineas, inline=True, fontsize=8.5, fmt='%.1f°C')
        
        # Puntos de control ########################################################
        self.ax.scatter(
            lons_array, lats_array, 
            c='black', 
            s=8, 
            alpha=0.7, 
            transform=self.proyeccion,
            zorder=5)
        
        # Contorno País ############################################################
        if geometria_pais is not None:
            self.ax.add_geometries(
                [geometria_pais], self.proyeccion,
                facecolor='none',
                edgecolor='red',
                linewidth=1
                )

        # Cuadricula de cooordenadas ###############################################
        cuadricula = self.ax.gridlines(draw_labels=True, linestyle='--', alpha=0.5)
        cuadricula.top_labels = False
        cuadricula.right_labels = False
        
        # Colorbar #################################################################
        if self.colorbar is not None:
            try:
                self.colorbar.remove()
            except:
                pass

        self.cbar_ax = self.fig.add_axes([0.25, 0.09, 0.5, 0.03])
        self.colorbar = self.fig.colorbar(cp, cax=self.cbar_ax, 
                                          orientation='horizontal',
                                          pad=0.04, shrink=0.7)
        self.colorbar.set_label('Temperatura(ºC)', fontsize=9)

        self.ax.set_title(nombre_pais)
        self.ax.set_aspect('equal', adjustable='box')

        self.canvas.draw()
        self.canvas.flush_events()

    def limpiar_mapa(self):
        """Limpia el mapa eliminando colorbar y ejes"""
        if self.colorbar is not None:
            try:
                self.colorbar.remove()
            except:
                pass
            self.colorbar = None
        
        if self.cbar_ax is not None:
            try:
                self.fig.delaxes(self.cbar_ax)
            except:
                pass
            self.cbar_ax = None

        if self.ax is not None:
            self.ax.clear()
    
    def mensaje(self, prompt, txt):
        """Muestra error con messagebox"""
        tk.messagebox.showerror(prompt, txt)
    
    def mensaje_info(self, prompt, txt):
        """Informa procedimientos precindibles que no se han podios ejecutar"""
        tk.messagebox.showinfo(prompt, txt)


if __name__ == "__main__":
    from mediador_view import MediadorView
    ventana = tk.Tk()
    mediador_view = MediadorView(ventana)
    mediador_view.cambiar_frame_view('ViewMapaVariables')
    mediador_view.obtener_frame_view_actual()
    ventana.mainloop()
