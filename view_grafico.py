import tkinter as tk
import tkinter.messagebox

from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from model import Event

class ViewGrafico:
    """View de la representación gráfica de la evolución de las variables climáticas, predicciones a 3 días."""
    def __init__(self, ventana2):

      # Configuración visual de la ventana #################
        self.ventana2 = ventana2
        self.ventana2.title("Previsión por ciudad")
        self.ventana2.geometry('800x500')
        
      # Eventos: patrón Observer ###########################
        self.btnBuscar = Event()
        self.btnSelect = Event()

      # Lista de botones con las ciudades ##################
        self.lista_btn = []
      # Lista de CheckButtons de variables climáticas ######
        self.lista_checkbtn = []

        self.setup_ui()
    
    def setup_ui(self):
        """ Configuración de Widgets """
      # Farme para agrupar el frame de la interfaz de búsqueda[arriba] y la lista de botones[abajo]
        self.frame1 = ttk.Frame(self.ventana2)
        self.frame1.grid(row=0, column=0, padx=150, pady=10)

      # Frame que contiene la interfaz de búsqueda [Horizontal]
        self.frame2 = ttk.Frame(self.frame1, width=800, height=50)
        self.frame2.grid(row=0, column=0, pady=10, padx=10)
        self.frame2.grid_propagate(False)

      # Frame que contiene los CheckBtn[izq.] y el garfico[der.]
        self.frame3 = ttk.Frame(self.ventana2)
        self.frame3.grid(row=1, column=0, padx= 20, sticky="w")


      # Elementos ##########################################
        self.label_busca = ttk.Label(self.frame2, text="Ciudad:")
        self.entry_busca = ttk.Entry(self.frame2, width=50)
        self.btn_busca = ttk.Button(self.frame2, text="Buscar", command=lambda: self.actualizar_lista_btn())

      # Organización #######################################
        self.label_busca.grid(row=0, column=0, pady=5)
        self.entry_busca.grid(row=0, column=1, pady=5)
        self.btn_busca.grid(row=0, column=2, pady=5)

    
############################## Parte lògica ##############################

    def entrada(self):
        """Método que toma el texto de Entry."""
        return self.entry_busca.get()
    
    def salida(self, lista):
        """Método que da la orden de borrado de elementos gráficos y genera 
        una nueva lista de botones con las ciudades que podrían coincidir."""
        self.limpiar_lista_btn()
        self.limpiar_grafico()
        for n, nombre_ciudad in enumerate(lista):
            boton = ttk.Button(
                        self.frame1, 
                        text=nombre_ciudad, 
                        command=lambda ciudad=nombre_ciudad: self.seleccionar_ciudad(ciudad), 
                        width=30
            )
            boton.grid(row=n+1, column=0, padx=100, sticky="w")
            self.lista_btn.append(boton)

    def actualizar_lista_btn(self):
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
    
    def crear_grafico(self, date, temp, hum_rel, viento, prob_precip, estado_cielo, nombre_vars):
        """Método que crear los widgets (CheckButtons) y el canvas del 
        gráfico"""
      # Guardar datos  
        self.date = date
        self.datos_variables = {
            "Temperatura": temp,
            "Humedad Rel.": hum_rel,
            "Viento": viento,
            "Prob. Precipitación": prob_precip,
            "Estado cielo": estado_cielo
            }

      # Contenedor para los CheckBtn #######################
        self.conten_checkbtn = ttk.Frame(self.frame3)
        self.conten_checkbtn.grid(row=0, column=0)

      # Creación de fix y axis para incorporar en canvas ###
        self.fig, self.ax = plt.subplots(figsize=(6,3.5))

        self.fig.tight_layout()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame3)
        self.canvas.get_tk_widget().grid(row=0, column=1, columnspan=2)  
       
      # Diccionario: key=nombre_var, value=BooleanVar ######
        self.var_y_estado = {}   

        for n, var in enumerate(nombre_vars):
            estado = tk.BooleanVar(value=True)
            self.var_y_estado[var] = estado
            btnCheck = tk.Checkbutton(
                    self.conten_checkbtn, 
                    text=var, 
                    variable=estado,
                    command=self.actualizar_grafico
            )
            btnCheck.grid(row=n, column=0, sticky="w")
            self.lista_checkbtn.append(btnCheck)

        self.actualizar_grafico()

    def actualizar_grafico(self):
        """Método que representa los resultados en el canvas del gráfico"""
        self.ax.clear()
        
        vars_select = []
        for var, estado in self.var_y_estado.items():
            if estado.get():  #  -----> estado = tk.BooleanVar(value=True);  estado.get
                vars_select.append(var)

        if vars_select:
            
            self.ax.xaxis_date()
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y\n%H:%M'))
            self.ax.xaxis.set_major_locator(mdates.HourLocator(byhour=[0, 12]))
      
            for var in vars_select:
                self.ax.plot(self.date, self.datos_variables[var], label=var)

            # Quitar margenes y juste de limites de X & Y ##
            self.ax.set_xlim(left=min(self.date), right=max(self.date))
            self.ax.set_ylim(bottom=0)
            self.ax.margins(x=0)
            
            # Leyenda ######################################
            self.ax.legend(loc='upper right', fontsize='small')
            
            # Formato de etiquetas de X ####################
            plt.setp(self.ax.get_xticklabels(), rotation=30, ha='center', fontsize=8) 
            self.fig.subplots_adjust(bottom=0.25)
    
        self.canvas.draw()
    
    def limpiar_grafico(self):
        """Método que borra canvas y lista de CheckButtons."""
        if self.lista_checkbtn:
            self.canvas.get_tk_widget().destroy()
            for checkbtn in self.lista_checkbtn:
                checkbtn.destroy()
        self.lista_checkbtn.clear()
          
    #--------------------------------------------------------------------

    def mensaje(self, prompt, txt):
        """Muestra error con messagebox"""
        tk.messagebox.showerror(prompt, txt)

if __name__ == "__main__":
    ventana = tk.Tk()
    vista = ViewGrafico(ventana)
    ventana.mainloop()