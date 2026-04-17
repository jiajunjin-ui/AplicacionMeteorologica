import tkinter as tk
from tkinter import ttk

from Event import Event

class Ventana2:
    def __init__(self, ventana2):

    ### Configuración visual de la ventana ############### 
        self.ventana = ventana2
        self.ventana.title("Previsión por ciudad")
        self.ventana.geometry("500x400")
        
    ### Eventos: patrón Observer #########################
        self.actLista = Event()
        self.btnBuscar = Event()

        self.setup_ui()
    
    def setup_ui(self):
        """ Configuración de Widgets """

    ### Variables de estado ###############################
        self.var = tk.StringVar() 

    ### Elementos #########################################
        self.label_busca = ttk.Label(self.ventana, text="Ciudad:")
        self.entry_busca = ttk.Entry(self.ventana, width=40)
        self.btn_busca = ttk.Button(self.ventana, text="Buscar", command=lambda: self.actualizar())
        self._lista_desp = ttk.Combobox(self.ventana, textvariable=self.var, width=40)

    ### Organización ######################################
        self.ventana.columnconfigure(0, weight=1)
        self.ventana.columnconfigure(1, weight=1)
        self.ventana.columnconfigure(2, weight=1)
        self.label_busca.grid(row=0, column=0, sticky="e")
        self.entry_busca.grid(row=0, column=1, sticky="w")
        self.btn_busca.grid(row=0, column=2)
        self._lista_desp.grid(row=1, column=1, sticky="w")

    def entrada(self):
        """Toma el texto de Entry"""
        return self.entry_busca.get()
    
    def salida(self, lista):
        """Devuelve una lista de ciudades Combobox"""
        self.var.set("")
        self._lista_desp.set('')
        self._lista_desp.config(values=[])
        self._lista_desp.update_idletasks()
        if lista:
            self._lista_desp.config(values=lista)

    def mensaje(self, prompt, txt):
        """Muestra error con messagebox"""
        tk.messagebox.showerror(prompt, txt)

    def actualizar(self):
        texto = self.entrada()
        if len(texto) > 3:
            self.actLista.emit()

    def select_ciudad(self):
        pass

    
if __name__ == "__main__":
    from Presenter import Presenter
    from Ciudad import Ciudad as Model

    # 1. Crear la ventana raíz de Tkinter
    ventana2 = tk.Tk()
    # 2. Instanciar el Modelo
    modelo = Model("")

    # 3. Instanciar Vista de Tkinter
    vista = Ventana2(ventana2)

    # 4. Instanciar el Presenter 
    presenter = Presenter(vista,modelo)

    # 5. Iniciar bucle de eventos 
    ventana2.mainloop()

