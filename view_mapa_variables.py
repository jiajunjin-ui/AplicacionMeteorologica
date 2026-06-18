import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.feature import ShapelyFeature

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
        self.btnSelect_pais = Event()
        self.btnSelect_var = Event()
        self.btnCambiarPantallaInicio = Event()

        self.lista_btn = []
        
        # Referencias de elementos del mapa ###################
        self.colorbar = None
        self.cbar_ax = None
        self.fig = None 
        self.ax = None
        self.canvas = None

        self.cp = None
        self.lineas = None
        self.flechas = None

        self.setup_ui()

    def setup_ui(self):
        """VENTANA PRINCIPAL TIENE DOS COLUMNAS: DERECHA (MAPA) - IZQUIERDA (CONTROLES)"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)


        # COLUMNA IZQUIERDA ####################################
        self.columna_izq = tk.Frame(self, width=250, padx=10, pady=10) 
        self.columna_izq.grid(row=0, column=0, sticky="nsew")
        self.columna_izq.grid_propagate(False)
        self.columna_izq.grid_columnconfigure(0, weight=1)
        # Contenedor btn países 
        self.frame_paises = tk.Frame(self.columna_izq)
        self.frame_paises.grid(row=4, column=0, sticky="ew")
        self.frame_paises.grid_columnconfigure(0, weight=1)
        # Contenedor var clímaticas 
        self.frame_var = tk.Frame(self.columna_izq, padx=5, pady=5)

        # Elementos 
        self.label_instruccion = tk.Label(self.columna_izq, text="Introduzca País")
        self.entry_pais = tk.Entry(self.columna_izq, width=25)
        btn_buscar_pais = ttk.Button(self.columna_izq, text="Mostrar país", command=lambda: self.actualizar_lista_paises())
        btn_ir_a_inicio = ttk.Button(self.columna_izq, width=10 , text="Inicio", command=lambda: self.cambiar_a_pantalla_inicio())

        # Organización
        self.label_instruccion.grid(row=1, column=0, sticky="w")
        self.entry_pais.grid(row=2, column=0, sticky="ew")
        btn_buscar_pais.grid(row=3, column=0, pady=5, sticky="ew")
        btn_ir_a_inicio.grid(row=0, column=0, sticky="w")

        # Elementos y Organización
        self.lista_variables= ['Temperatura', 'Humedad Relativa', 'Vientos']
        self.seleccion = tk.IntVar()
        for n, var in enumerate(self.lista_variables):
            op = tk.Radiobutton(self.frame_var, 
                                text=var,
                                variable=self.seleccion, 
                                value=n, 
                                command=lambda var=var: self.seleccionar_var(var))
            op.grid(row=n, column=0, pady=2, sticky="w")


        # COLUMNA DERECHA ######################################
        self.columna_der= tk.Frame(self)
        self.columna_der.grid(row=0, column=1, sticky="nsew")
        self.columna_der.grid_columnconfigure(1, weight=3)

        # Elementos y organización 
        self._inicializar_mapa()

    def _inicializar_mapa(self):
        """Método que crea la figura (fig), los ejes (ax) con preoyección y el canvas"""
        self.proyeccion = ccrs.epsg(3857)
        self.fig = Figure(figsize=(5.5, 5.5), dpi=100)
        self.ax = self.fig.add_subplot(111, projection=self.proyeccion)
        self.fig.subplots_adjust(bottom=0.18, top=0.94, left=0.10, right=0.95)
        self.ax.grid(True)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.columna_der)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.canvas.draw_idle()

    def entrada(self):
        """Método que toma el texto de Entry."""
        return self.entry_pais.get()
    
    def actualizar_lista_paises(self):
        self.btnBuscar.emit()
    
    def mostrar_lista_paises(self, lista):
        self.limpiar_lista_paises()
        self.ocultar_selector_var()
        for n, nombre_pais in enumerate(lista):
            boton = ttk.Button(
                self.frame_paises,
                width=20,
                text=nombre_pais,
                command=lambda nombre_pais=nombre_pais: self.seleccionar_pais(nombre_pais)
            )
            boton.grid(row=n, column=0, pady=3)
            self.lista_btn.append(boton)

    def limpiar_lista_paises(self):
        """Método que borra la lista de botones."""
        for boton in self.lista_btn:
            boton.destroy()
        self.lista_btn.clear()

    def seleccionar_pais(self, nombre_pais):
        self.btnSelect_pais.emit(nombre_pais)
        self.limpiar_lista_paises()
    
    def mostrar_selector_var(self):
        self.frame_var.grid(row=5, column=0, pady=15, sticky="ew")

    def ocultar_selector_var(self):
        self.frame_var.grid_forget()

    # MÉTODOS DE GENERACIÓN DE MAPA -----------------------------------------------------
    def generar_mapa(self, lons_array, lats_array, 
                        lon_min, lon_max, 
                        lat_min, lat_max,
                        nombre_pais, geometria_pais, 
                        resolucion):  
        
        self.limpiar_mapa()
        
        # Fijar los límites establecidos #################################
        self.ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=self.proyeccion)
        
        # Características geográficas: líneas de cosa, tierra, bordes #########
        self.ax.add_feature(cfeature.COASTLINE.with_scale(resolucion), edgecolor='black', linewidth=1.5, zorder=2)
        self.ax.add_feature(cfeature.BORDERS.with_scale(resolucion), linestyle=':', edgecolor='black', zorder=2)
        self.ax.add_feature(cfeature.LAND.with_scale(resolucion), facecolor='#f5f5f5', zorder=0)
        self.ax.add_feature(cfeature.OCEAN.with_scale(resolucion), facecolor="#115ab3", alpha=0.7, zorder=0)
        
        # Puntos de control ##############################################
        self.ax.scatter(
            lons_array, lats_array, 
            c='black', 
            s=6, 
            alpha=0.6, 
            transform=self.proyeccion,
            zorder=3)
        
        # Contorno País ##################################################
        if geometria_pais is not None:
            self.ax.add_feature(ShapelyFeature(
                geometria_pais, 
                crs=self.proyeccion,
                 facecolor='none',
                 edgecolor='red',
                 linewidth=1,
                 zorder=4
                 ))

        # Cuadricula de cooordenadas #####################################
        cuadricula = self.ax.gridlines(draw_labels=True, linestyle='--', alpha=0.5)
        cuadricula.top_labels = False
        cuadricula.right_labels = False

        cuadricula.xlabel_style = {'size': 9}
        cuadricula.ylabel_style = {'size': 9}

        # Título y formato de ejes #######################################
        self.ax.set_title(nombre_pais)
        self.ax.set_aspect('equal', adjustable='box')

        # Opciónes de mapa ###############################################
        self.seleccion.set(0)
        self.mostrar_selector_var()
        self.btnSelect_var.emit('Temperatura')


    def seleccionar_var(self, variable):
        self.btnSelect_var.emit(variable)
    

    def rellenar_mapa (self, grid_x_c, grid_y_c, grid_z, 
                       colores, unidades, text_label,
                       cp_levels,
                       hay_lineas, line_levels,
                       grid_z_velx_viento, grid_z_vely_viento,
                       grid_x_d, grid_y_d):
        
        self.limpiar_relleno()
        # Elementos continuos ############################################
        self.cp = self.ax.contourf(
            grid_x_c, grid_y_c, grid_z, 
            levels=cp_levels, 
            cmap=colores,
            alpha=0.7, 
            transform=self.proyeccion,
            zorder=1
            )
        self.ax.set_rasterization_zorder(1.5)

        if hay_lineas:
            self.lineas = self.ax.contour(
                grid_x_c, grid_y_c, grid_z, 
                levels=line_levels, 
                colors='black',
                linewidths=0.5, 
                alpha=0.7,
                transform=self.proyeccion,
                zorder=1
                )
            self.ax.clabel(self.lineas, levels=self.lineas.levels[::2], inline=True, fontsize=8.5, fmt=unidades)

        # Elementos discretos ############################################
        if grid_z_velx_viento is not None and grid_z_vely_viento is not None:
            self.flechas = self.ax.quiver(grid_x_d, grid_y_d, 
                                          grid_z_velx_viento, grid_z_vely_viento,
                                          color='white',
                                          scale=90,
                                          width=0.003,
                                          transform=self.proyeccion,
                                          zorder=5)

        # Colorbar #######################################################
        self.cbar_ax = self.fig.add_axes([0.25, 0.10, 0.5, 0.03])
        self.colorbar = self.fig.colorbar(self.cp, format='%.1f', cax=self.cbar_ax, 
                                          orientation='horizontal',
                                          pad=0.04, shrink=0.7)
        self.colorbar.set_label(text_label, fontsize=9.5)

        self.canvas.draw_idle()

    # MÉTODOS DE LIMPIEZA DE MAPA ------------------------------------------------------
    def limpiar_mapa(self):
        """Limpia el mapa"""
        self.fig.clear()

        self.ax = self.fig.add_subplot(111, projection=self.proyeccion)
        self.fig.subplots_adjust(bottom=0.18, top=0.94, left=0.10, right=0.95)
        self.ax.grid(True, linestyle='--', alpha=0.5)

        self.colorbar = None
        self.cbar_ax = None
        self.cp = None
        self.lineas = None
        self.flechas = None

        self.canvas.draw_idle()

    def limpiar_relleno(self):
        """Limpiar el mapa eliminando colorbar y colores de relleno"""
        if self.cp is not None:
            try:
                self.cp.remove()
            except:
                pass
            self.cp = None
        
        if self.lineas is not None:
            try:
                self.lineas.remove()
            except:
                pass
            self.lineas = None 
        
        if self.flechas is not None:
            try:
                self.flechas.remove()
            except:
                pass 
            self.flechas = None

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

    def limpiar_mapa_cambio_pantalla(self):
        "Limpieza total del mapa y del texto introducido"
        self.limpiar_relleno()
        self.limpiar_mapa()
        self.ocultar_selector_var()
        self.limpiar_lista_paises()
        self.entry_pais.delete(0, tk.END)
        self.canvas.draw()


    def cambiar_a_pantalla_inicio(self):
        self.btnCambiarPantallaInicio.emit()

    def mensaje(self, prompt, txt):
        """Muestra error con messagebox"""
        tk.messagebox.showerror(prompt, txt)
    
    def mensaje_info(self, prompt, txt):
        """Informa de procedimientos prescindibles 
        que no se han podios ejecutar"""
        tk.messagebox.showinfo(prompt, txt)

if __name__ == "__main__":
    from mediador_view import MediadorView
    ventana = tk.Tk()
    mediador_view = MediadorView(ventana)
    mediador_view.cambiar_frame_view('ViewMapaVariables')
    mediador_view.obtener_frame_view_actual()
    ventana.mainloop()
