import tkinter as tk
import tkinter.messagebox

from tkinter import ttk

from model.event import Event

class Ventana2:
    def __init__(self, ventana2):

      # Configuración visual de la ventana ##############
        self.ventana = ventana2
        self.ventana.title("Previsión por ciudad")
        self.ventana.geometry("500x400")
        
      # Eventos: patrón Observer ########################
        self.actLista = Event()
        self.btnBuscar = Event()
        self.btnConsultar = Event()

        self.setup_ui()
    
    def setup_ui(self):
        """ Configuración de Widgets """

      # Variables de estado ##############################
        self.var = tk.StringVar() 

      # Elementos #########################################
        self.label_busca = ttk.Label(self.ventana, text="Ciudad:")
        self.entry_busca = ttk.Entry(self.ventana, width=40)
        self._lista_desp = ttk.Combobox(self.ventana, textvariable=self.var, state="readonly", width=40)
        self.btn_busca = ttk.Button(self.ventana, text="Buscar", command=lambda: self.actualizar_lista())
        self.btn_consulta = ttk.Button(self.ventana, text="Consultar", command=lambda: self.consultar_var())

      # Organización #####################################
        self.ventana.columnconfigure(0, weight=1)
        self.ventana.columnconfigure(1, weight=1)
        self.ventana.columnconfigure(2, weight=1)

        self.label_busca.grid(row=0, column=0, sticky="e")
        self.entry_busca.grid(row=0, column=1, sticky="w")
        self._lista_desp.grid(row=1, column=1, sticky="w")
        self.btn_busca.grid(row=0, column=2)
        self.btn_consulta.grid(row=1, column=2)
        

    def entrada(self):
        """Toma el texto de Entry"""
        return self.entry_busca.get()
    
    def salida(self, lista):
        """Devuelve una lista de ciudades en el Combobox"""
        self.var.set("")
        self._lista_desp.set('')
        self._lista_desp.config(values=[])
        self._lista_desp.update_idletasks()

        if lista:
            self._lista_desp.config(values=lista)
        self._lista_desp.focus_set()
        self._lista_desp.event_generate('<Down>')

    def mensaje(self, prompt, txt):
        """Muestra error con messagebox"""
        tk.messagebox.showerror(prompt, txt)

    def actualizar_lista(self):
        #texto = self.entrada()
        #if len(texto) > 3:
        self.actLista.emit()

    def select_ciudad(self):
        pass
    
    def consultar_var(self):
        pass


