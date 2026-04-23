import tkinter as tk
import tkinter.messagebox

from tkinter import ttk

from model.event import Event

class ViewVentana2:
    def __init__(self, ventana2):

      # Configuración visual de la ventana ###############
        self.ventana2 = ventana2
        self.ventana2.title("Previsión por ciudad")
        self.ventana2.geometry("700x600")
        
      # Eventos: patrón Observer #########################
        self.btnBuscar = Event()
        self.btnSelect = Event()

      # Lista de botones con las ciudades ################
        self.lista_btn = []
        
        self.label_resultado = None

        self.setup_ui()
    
    def setup_ui(self):
        """ Configuración de Widgets """

      # Elementos #########################################
        self.label_busca = ttk.Label(self.ventana2, text="Ciudad:")
        self.entry_busca = ttk.Entry(self.ventana2, width=40)
        self.btn_busca = ttk.Button(self.ventana2, text="Buscar", command=lambda: self.actualizar_lista_btn())

      # Organización #####################################
        self.ventana2.columnconfigure(0, weight=1)
        self.ventana2.columnconfigure(1, weight=1)
        self.ventana2.columnconfigure(2, weight=1)

        self.label_busca.grid(row=0, column=0, sticky="e")
        self.entry_busca.grid(row=0, column=1, sticky="w")
        self.btn_busca.grid(row=0, column=2)

    
########################## Parte lògica ##########################

    def entrada(self):
        """Método que toma el texto de Entry."""
        return self.entry_busca.get()
    
    def salida(self, lista):
        """Método que devuelve una lista de ciudades en forma de botones"""
        self.limpiar_lista_btn()
        for n, nombre_ciudad in enumerate(lista):
            boton = ttk.Button(
                        self.ventana2, 
                        text=lista[n], 
                        command=lambda: self.seleccionar_ciudad(nombre_ciudad), 
                        width=30
            )
            boton.grid(row=n+1, column=1)
            self.lista_btn.append(boton)

    def actualizar_lista_btn(self):
        """Borra la lista de botones de ciudades de la anterior búsqueda 
           y los sustituye por los de la nueva búsqueda. """
        if self.label_resultado != None:
            self.limpiar_result()
        self.btnBuscar.emit()

    def limpiar_lista_btn(self):
        """Método que borra la lista de botones."""
        for boton in self.lista_btn:
            boton.destroy()
        self.lista_btn.clear()

    def seleccionar_ciudad(self, nombre_ciudad):
        """Método que toma la referencia (str) de la ciudad elegida por 
           el usuario, para operar con ella."""
        self.btnSelect.emit(nombre_ciudad)
        self.limpiar_lista_btn()

    def limpiar_result(self):
        self.label_resultado.destroy()
        self.label_resultado = None

    def resultados(self, resultado):
        self.label_resultado = ttk.Label(self.ventana2, text=resultado)
        self.label_resultado.grid(row=1, column=1)


    def mensaje(self, prompt, txt):
        """Muestra error con messagebox"""
        tk.messagebox.showerror(prompt, txt)


