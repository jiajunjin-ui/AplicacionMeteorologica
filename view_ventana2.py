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

        self.setup_ui()
    
    def setup_ui(self):
        """ Configuración de Widgets """

      # Elementos #########################################
        self.label_busca = ttk.Label(self.ventana2, text="Ciudad:")
        self.entry_busca = ttk.Entry(self.ventana2, width=50)
        self.btn_busca = ttk.Button(self.ventana2, text="Buscar", command=lambda: self.actualizar_lista_btn())

      # Organización ######################################
        self.ventana2.columnconfigure(0, weight=1)
        self.ventana2.columnconfigure(1, weight=1)
        self.ventana2.columnconfigure(2, weight=1)

        self.label_busca.grid(row=0, column=0, sticky='e')
        self.entry_busca.grid(row=0, column=1, sticky='w')
        self.btn_busca.grid(row=0, column=1, columnspan=2)

    
############################## Parte lògica ##############################

    def entrada(self):
        """Método que toma el texto de Entry."""
        return self.entry_busca.get()
    
    def salida(self, lista):
        """Método que devuelve una lista de ciudades en forma de botones"""
        self.limpiar_lista_btn()
        for n, nombre_ciudad in enumerate(lista):
            boton = ttk.Button(
                        self.ventana2, 
                        text=nombre_ciudad, 
                        command=lambda ciudad=nombre_ciudad: self.seleccionar_ciudad(ciudad), 
                        width=30
            )
            boton.grid(row=n+1, column=1)
            self.lista_btn.append(boton)

    def actualizar_lista_btn(self):
        """Borra la lista de botones de ciudades de la anterior búsqueda 
           y los sustituye por los de la nueva búsqueda. """
        self.btnBuscar.emit()

    def limpiar_lista_btn(self):
        """Método que borra la lista de botones."""
        for boton in self.lista_btn:
            boton.destroy()
        self.lista_btn.clear()

    #--------------------------------------------------------------------

    def seleccionar_ciudad(self, nombre_ciudad):
        """Método que toma la referencia (str) de la ciudad elegida por 
           el usuario, para operar con ella."""
        self.btnSelect.emit(nombre_ciudad)
        self.limpiar_lista_btn()
    
    def crear_grafico(self, resultados):
      # DataFrame con los datos de OpenMeteo #############
        self.df = resultados

      # Contenedor para los CheckBtn #####################
        controlador_var = ttk.Frame(self.ventana2)
        controlador_var.grid(row=1, column=0)

      # Creación de fig y canvas #########################
        self.fig, self.ax = plt.subplots(figsize=(5,3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.ventana2)
        self.canvas.get_tk_widget().grid(row=1, column=1, columnspan=2)  
  
        self.list_var = list(self.df.columns[1:])
        self.var_estado = {}

        for var in self.list_var:
            estado = tk.BooleanVar(value=True)
            self.var_estado[var] = estado
            btnCheck = tk.Checkbutton(
                    controlador_var, 
                    text=var, 
                    variable=estado,
                    command=self.actualizar_grafico
            )
            btnCheck.pack(anchor='w')

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


    #--------------------------------------------------------------------

    def mensaje(self, prompt, txt):
        """Muestra error con messagebox"""
        tk.messagebox.showerror(prompt, txt)


