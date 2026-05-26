import tkinter as tk
import tkinter.messagebox
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
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
        self.entrada_pais = tk.Entry(self.columna_izq, width=25)
        btn_buscar_pais = tk.Button(self.columna_izq, text="Mostrar país", command=lambda: self.buscar_pais())
        # Organización
        self.label_instruccion.grid(row=0, column=0, sticky="w")
        self.entrada_pais.grid(row=1, column=0, sticky="ew")
        btn_buscar_pais.grid(row=2, column=0, pady=5, sticky="ew")


        # COLUMNA DERECHA ##################################
        self.columna_der= tk.Frame(self)
        self.columna_der.grid(row=0, column=1, sticky="nsew")
        # Elementos y organización 
        self.projeccion = ccrs.PlateCarree()
        self.fig, self.ax = plt.subplots(figsize=(7, 5), dpi=100, subplot_kw={'projection': self.projeccion})
        self.ax.set_aspect('auto',adjustable='box')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.columna_der)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    
    def entrada(self):
        """Método que toma el texto de Entry."""
        return self.entrada_pais.get()
    
    def buscar_pais(self):
        self.btnBuscar.emit()

    def actualizar_mapa(self, lons_array, lats_array, 
                        lon_min, lon_max, 
                        lat_min, lat_max, 
                        grid_x, grid_y, grid_z):
        self.ax.clear()
     
        # Fijar los límites establecidos ###########################################
        self.ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=self.projeccion)
        
        # Características geográficas: líneas de cosa, tierra, bordes ##############
        self.ax.add_feature(cfeature.COASTLINE.with_scale('10m'), edgecolor='black', linewidth=1.5)
        self.ax.add_feature(cfeature.BORDERS.with_scale('10m'), linestyle=':', edgecolor='black')
        self.ax.add_feature(cfeature.LAND.with_scale('10m'), facecolor='#f5f5f5')
        self.ax.add_feature(cfeature.OCEAN.with_scale('10m'), facecolor="#111ece")
        
        # Mapa de calor isotermas ##################################################
        cp = self.ax.contourf(
            grid_x, grid_y, grid_z, 
            levels=15, 
            cmap='RdYlBu_r',
            alpha=0.6, 
            transform=self.projeccion
            )
        lineas = self.ax.contour(
            grid_x, grid_y, grid_z, 
            levels=10, 
            colors='black',
            linewidths=0.5, 
            alpha=0.5,
            transform=self.projeccion)
        self.ax.clabel(lineas, inline=True, fontsize=8.5, fmt='%.1f°C')
        
        # Puntos de comtrol ########################################################
        self.ax.scatter(
            lons_array, lats_array, 
            c='black', 
            s=8, 
            alpha=0.7, 
            transform=self.projeccion)
        
        # Cuadricula de cooordenadas ###############################################
        cuadricula = self.ax.gridlines(draw_labels=True, linestyle='--', alpha=0.5)
        cuadricula.top_labels = False
        cuadricula.right_labels = False
        
        self.fig.colorbar(cp, label='Temperatura(ºC)', orientation='horizontal', pad=0.08, shrink=0.7)

        self.canvas.draw()

    def mensaje(self, prompt, txt):
        """Muestra error con messagebox"""
        tk.messagebox.showerror(prompt, txt)


if __name__ == "__main__":
    from mediador_view import MediadorView
    ventana = tk.Tk()
    mediador_view = MediadorView(ventana)
    mediador_view.cambiar_frame_view('ViewMapaCalor')
    mediador_view.obtener_frame_view_actual()
    ventana.mainloop()
