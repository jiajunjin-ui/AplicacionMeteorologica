import tkinter as tk
import tkinter.messagebox

from tkinter import ttk
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from model.event import Event

class ViewVentana2:
    def __init__(self, ventana2):

      # Configuración visual de la ventana ################
        self.ventana2 = ventana2
        self.ventana2.title("Previsión por ciudad")
        self.ventana2.geometry('800x500')
        
      # Eventos: patrón Observer ##########################
        self.btnBuscar = Event()
        self.btnSelect = Event()

      # Lista de botones con las ciudades #################
        self.lista_btn = []
      # Lista de CheckButtons de variables climáticas #####
        self.lista_checkbtn = []

        self.setup_ui()
    
    def setup_ui(self):
        """ Configuración de Widgets """
      # Farme para agrupar la interfaz de búsqueda y la lista de botones
        self.frame1 = ttk.Frame(self.ventana2)
        self.frame1.grid(row=0, column=0, padx=20, pady=10)

      # Frame de la interfaz de búsqueda
        self.frame2 = ttk.Frame(self.frame1, width=800, height=50)
        self.frame2.grid(row=0, column=0, pady=10, padx=10)
        self.frame2.grid_propagate(False)

      # Frame para agrupar el garfico y los CheckBtn
        self.frame3 = ttk.Frame(self.ventana2)
        self.frame3.grid(row=1, column=0, padx= 20, sticky="w")


      # Elementos #########################################
        self.label_busca = ttk.Label(self.frame2, text="Ciudad:")
        self.entry_busca = ttk.Entry(self.frame2, width=50)
        self.btn_busca = ttk.Button(self.frame2, text="Buscar", command=lambda: self.actualizar_lista_btn())

      # Organización ######################################
        self.label_busca.grid(row=0, column=0, pady=5)
        self.entry_busca.grid(row=0, column=1, pady=5)
        self.btn_busca.grid(row=0, column=2, pady=5)

    
############################## Parte lògica ##############################

    def entrada(self):
        """Método que toma el texto de Entry."""
        return self.entry_busca.get()
    
    def salida(self, lista):
        """Método que devuelve una lista de ciudades en forma de botones"""
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
        """Borra la lista de botones de ciudades de la anterior búsqueda 
           y los sustituye por los de la nueva búsqueda."""
        self.btnBuscar.emit()

    def limpiar_lista_btn(self):
        """Método que borra la lista de botones."""
        for boton in self.lista_btn:
            boton.destroy()
        self.lista_btn.clear()

    # Graficar Variables Climáticas-------------------------------------

    def seleccionar_ciudad(self, nombre_ciudad):
        """Método que toma la referencia (str) de la ciudad elegida por 
           el usuario, para operar con ella."""
        self.btnSelect.emit(nombre_ciudad)
        self.limpiar_lista_btn()
    
    def crear_grafico(self, resultados):

      # DataFrame con los datos de OpenMeteo #############
        self.df = resultados

      # Contenedor para los CheckBtn #####################
        self.conten_checkbtn = ttk.Frame(self.frame3)
        self.conten_checkbtn.grid(row=0, column=0)

      # Creación de fig y canvas #########################
        self.fig, self.ax = plt.subplots(figsize=(5,3))
        self.fig.tight_layout()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame3)
        self.canvas.get_tk_widget().grid(row=0, column=1, columnspan=2)  
  
        self.list_var = list(self.df.columns[1:])
        self.var_estado = {}

        for n, var in enumerate(self.list_var):
            estado = tk.BooleanVar(value=True)
            self.var_estado[var] = estado
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
        self.ax.clear()

        var_select = []
        for var, estado in self.var_estado.items():
            if estado.get():  #  -----> estado = tk.BooleanVar(value=True);  estado.get
                var_select.append(var)

        if var_select:
            self.df.plot(x=self.df.columns[0], y=var_select, ax=self.ax)
            self.ax.legend(loc='upper right', fontsize='small')
        
        self.canvas.draw()
    
    def limpiar_grafico(self):
        """Método que borra canvas y lista de CheckButtons."""
        if self.lista_checkbtn != []:
            self.canvas.get_tk_widget().destroy()
            for checkbtn in self.lista_checkbtn:
                checkbtn.destroy()
        self.lista_checkbtn.clear()
          
    #--------------------------------------------------------------------

    def mensaje(self, prompt, txt):
        """Muestra error con messagebox"""
        tk.messagebox.showerror(prompt, txt)


