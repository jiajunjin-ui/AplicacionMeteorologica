import tkinter as tk
import tkinter.messagebox
from tkinter import ttk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates

from model import Event
from view.view_base import ViewBase

class ViewGrafico(ViewBase):
    """View de la representación gráfica de la evolución de las variables climáticas, predicciones a 3 días."""
    def __init__(self, parent, mediador_view):
        super().__init__(
            parent,
            mediador_view,
            titulo = "Previsión por ciudad",
            size = '800x500')

        # Eventos: patrón Observer ############################
        self.btnBuscar = Event()
        self.btnSelect = Event()
        self.check_selec = Event()
        self.btnCambiarPantallaInicio = Event()

        # Lista de botones con las ciudades ###################
        self.lista_btn = []

        self.setup_ui()
    
    def setup_ui(self):
        """ Configuración de Widgets """
      # Frame para agrupar el frame de la interfaz de búsqueda[arriba] y la lista de botones[abajo]
        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(2, weight=1)

      # Frame que contiene la interfaz de búsqueda [Horizontal]
        self.frame_interfaz_busqueda = tk.Frame(self.frame, width=780, height=60)
        self.frame_interfaz_busqueda.grid(row=0, column=0, columnspan=5, pady=10, padx=10)
        self.frame_interfaz_busqueda.grid_propagate(False)
        self.frame_interfaz_busqueda.columnconfigure(1, weight=1)
        self.frame_interfaz_busqueda.columnconfigure(5, weight=2)

      # Frame que contiene los CheckBtn[izq.] y el garfico[der.]
        self.frame_grafico = tk.Frame(self)
        self.frame_grafico.grid(row=1, column=0, padx= 20, sticky="w")

      # Contenedor para los CheckBtn 
        self.conten_checkbtn = tk.Frame(self.frame_grafico)

      # Elementos ###########################################
        self.label_busca = tk.Label(self.frame_interfaz_busqueda, text="Introduzca una Ciudad: ", font=("Arial", 9))
        self.entry_busca = tk.Entry(self.frame_interfaz_busqueda, width=50, font=("Arial", 9))
        self.entry_busca.focus_set()
        self.btn_busca = ttk.Button(self.frame_interfaz_busqueda, text="Buscar", command=lambda: self.actualizar_lista_ciudades())
        self.btn_cambiar_a_inicio = ttk.Button(self.frame_interfaz_busqueda, text="Inicio", command=lambda: self.cambiar_a_pantalla_inicio())

        self.fig = Figure(figsize=(6, 3.5))
        self.ax = self.fig.add_subplot(111)
        self.fig.tight_layout()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_grafico)

      # Organización ########################################
        self.label_busca.grid(row=1, column=2, pady=5)
        self.entry_busca.grid(row=1, column=3, pady=5)
        self.btn_busca.grid(row=1, column=4, pady=5)
        self.btn_cambiar_a_inicio.grid(row=0, column=0, pady=2)

      # Elementos y Oraganización ###########################
        nombre_vars = ["Temperatura", "Humedad Rel.", "Viento", "Prob. Precipitación"]
        self.var_y_estado = {}   

        for n, var in enumerate(nombre_vars):
            estado = tk.BooleanVar(value=True)
            self.var_y_estado[var] = estado
            btnCheck = tk.Checkbutton(
                    self.conten_checkbtn, 
                    text=var, 
                    variable=estado,
                    command=lambda: self.seleccionar_var()
            )
            btnCheck.grid(row=n, column=0, sticky="w")


    # Sistema de Busqueda Ciudad ----------------------------------------
    def entrada(self):
        """Método que toma el texto de Entry."""
        return self.entry_busca.get()
    
    def mostrar_lista_ciudades(self, lista):
        """Método que da la orden de borrado de elementos gráficos y genera 
        una nueva lista de botones con las ciudades que podrían coincidir."""
        self.limpiar_lista_btn()
        self.limpiar_grafico()

        for n, nombre_ciudad in enumerate(lista):
            boton = ttk.Button(
                        self.frame, 
                        text=nombre_ciudad, 
                        command=lambda ciudad=nombre_ciudad: self.seleccionar_ciudad(ciudad), 
                        width=40
            )
            boton.grid(row=n+1, column=1, sticky="w", padx=5)
            self.lista_btn.append(boton)

    def actualizar_lista_ciudades(self):
        """Ejecuta la orden para crear una lista de botones, borrar los 
        elementos gráficos antiguos"""
        self.btnBuscar.emit()

    def limpiar_lista_btn(self):
        """Método que borra la lista de botones."""
        for boton in self.lista_btn:
            boton.destroy()
        self.lista_btn.clear()

    # Graficar Variables Climáticas--------------------------------------
    def seleccionar_ciudad(self, nombre_ciudad):
        """Toma la referencia (str) de la ciudad elegida por 
           el usuario y ejecuta la orden para creación del gráfico."""
        self.btnSelect.emit(nombre_ciudad)
        self.limpiar_lista_btn()
    
    def seleccionar_var(self):
        self.check_selec.emit()
                        
    def mostrar_elementos_graficos(self):
        """Método que posiciona los elementos graficos, canvas y checkbuttons"""
        self.conten_checkbtn.grid(row=0, column=0, padx=5)
        self.canvas.get_tk_widget().grid(row=0, column=1, columnspan=2)
        for estado in self.var_y_estado.values():
            estado.set(True)

    def obtner_var_selec(self):
        """Método que devuelve una lista de variables climáticas activas"""
        vars_activ = []
        for var, estado in self.var_y_estado.items():
            if estado.get():  #  -----> estado = tk.BooleanVar(value=True);  estado.get
                vars_activ.append(var)
        return vars_activ

    def actualizar_grafico(self, date, datos_filtrados):
        """Método que representa los resultados en el canvas del gráfico"""
        self.ax.clear()

        if datos_filtrados and date is not None:
            self.ax.xaxis_date()
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y\n%H:%M'))
            self.ax.xaxis.set_major_locator(mdates.HourLocator(byhour=[0, 12]))

            for var, valores in datos_filtrados.items():
                self.ax.plot(date, valores, label=var)

            # Quitar margenes y juste de limites de X & Y ###
            self.ax.set_xlim(left=min(date), right=max(date))
            self.ax.set_ylim(bottom=0)
            self.ax.margins(x=0)
            
            # Leyenda #######################################
            self.ax.legend(loc='upper right', fontsize='small')
            
            # Formato de etiquetas de X #####################
            for label in self.ax.get_xticklabels():
                label.set_rotation(30)
                label.set_horizontalalignment('center')
                label.set_fontsize(8)

            self.fig.subplots_adjust(bottom=0.25)
    
        self.canvas.draw()
    
    def limpiar_grafico(self):
        """Método que borra canvas y lista de CheckButtons."""
        self.conten_checkbtn.grid_forget()
        self.canvas.get_tk_widget().grid_forget()

        self.ax.clear()
        self.canvas.draw()

    #--------------------------------------------------------------------
    def limpiar_grafico_cambio_pantalla(self):
        self.limpiar_lista_btn()
        self.limpiar_grafico()
        self.entry_busca.delete(0, tk.END)

    def cambiar_a_pantalla_inicio(self):
        self.btnCambiarPantallaInicio.emit()

    def mensaje(self, prompt, txt):
        """Muestra error con messagebox"""
        tk.messagebox.showerror(prompt, txt)

if __name__ == "__main__":
    from mediador_view import MediadorView

    ventana = tk.Tk()
    mediador_view = MediadorView(ventana)
    mediador_view.cambiar_frame_view('ViewGrafico')
    mediador_view.obtener_frame_view_actual()
    ventana.mainloop()