import tkinter as tk
import tkinter.messagebox

from tkinter import ttk

from model.event import Event

class ViewVentana2:
    def __init__(self, ventana2):

      # Configuración visual de la ventana ###############
        self.ventana2 = ventana2
        self.ventana2.title("Previsión por ciudad")
        self.ventana2.geometry("500x400")
        
      # Eventos: patrón Observer #########################
        self.btnBuscar = Event()
        self.btnSelect = Event()

      # Lista de botones con las ciudades ################
        self.lista_btn = []

        self.setup_ui()
    
    def setup_ui(self):
        """ Configuración de Widgets """

      # Elementos #########################################
        self.label_busca = ttk.Label(self.ventana2, text="Ciudad:")
        self.entry_busca = ttk.Entry(self.ventana2, width=40)
        self.btn_busca = ttk.Button(self.ventana2, text="Buscar", command=lambda: self.actualizar_lista_btn())
        self.label_resultado = ttk.Label(self.ventana2)

      # Organización #####################################
        self.ventana2.columnconfigure(0, weight=1)
        self.ventana2.columnconfigure(1, weight=1)
        self.ventana2.columnconfigure(2, weight=1)

        self.label_busca.grid(row=0, column=0, sticky="e")
        self.entry_busca.grid(row=0, column=1, sticky="w")
        self.btn_busca.grid(row=0, column=2)
        self.label_resultado.grid(row=1, column=0)
    

    def entrada(self):
        """Toma el texto de Entry"""
        return self.entry_busca.get()
    
    def salida(self, lista):
        """Devuelve una lista de ciudades en forma de botones"""
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

    def limpiar_lista_btn(self):
        for boton in self.lista_btn:
            boton.destroy()
        self.lista_btn.clear()

    def actualizar_lista_btn(self):
        self.limpiar_result()
        self.btnBuscar.emit()

    def seleccionar_ciudad(self, nombre_ciudad):
        self.btnSelect.emit(nombre_ciudad)
        self.limpiar_lista_btn()

    def limpiar_result(self):
        self.label_resultado.config(text="")

    def resultados(self, resultado):
        self.label_resultado.config(text=resultado)

    def mensaje(self, prompt, txt):
        """Muestra error con messagebox"""
        tk.messagebox.showerror(prompt, txt)


