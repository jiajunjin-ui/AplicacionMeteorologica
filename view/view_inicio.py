import tkinter as tk
from tkinter import ttk
import tkinter.messagebox

from view.view_base import ViewBase
from model import Event

class ViewInicio(ViewBase):
    def __init__(self, parent, mediador_view):
        super().__init__(
            parent, 
            mediador_view, 
            titulo = "Aplicación Meteorológica",
            size = '400x300')
        
        # Eventos: patrón Observer ###########################
        self.btnCambiarPantallaGrafico = Event()
        self.btnCambiarPantallaMapaDis = Event()
        self.btnCambiarPantallaMapaCont = Event()

        self.setup_ui()

    def setup_ui(self):
        # Frame Centrado #####################################
        self.frame_central = tk.Frame(self, width=400, height=300)
        self.frame_central.grid(row=0, column=0, sticky="nsew")
        self.frame_central.grid_propagate(False)
        self.frame_central.columnconfigure(0, weight=3)
        self.frame_central.rowconfigure(0, weight=1)
        self.frame_central.rowconfigure(5, weight=1)

        # Elementos ##########################################
        btn_ir_a_grafico = tk.Button(self.frame_central,
                                           text='Ciudades',
                                           width=20,
                                           font=("Arial", 11),
                                           command=lambda: self.cambiar_a_pantalla_grafico()
                                           )
        btn_ir_a_mapa_dis = tk.Button(self.frame_central,
                                        text='Mapas elementos discretos',
                                        width=20,
                                        font=("Arial", 11),
                                        command=lambda: self.cambiar_a_pantalla_mapa_dis()
                                        )

        btn_ir_a_mapa_cont = tk.Button(self.frame_central,
                                        text='Mapas elementos continuos',
                                        width=20,
                                        font=("Arial", 11),
                                        command=lambda: self.cambiar_a_pantalla_mapa_cont()
                                        )


        # Organización #######################################
        btn_ir_a_grafico.grid(row=1, column=0, columnspan=4, padx= 10, pady=5)
        btn_ir_a_mapa_dis.grid(row=2, column=0, columnspan=4, padx=10, pady=5)
        btn_ir_a_mapa_cont.grid(row=3, column=0, columnspan=4, padx=10, pady=5)

    def cambiar_a_pantalla_grafico(self):
        self.btnCambiarPantallaGrafico.emit()
    
    def cambiar_a_pantalla_mapa_dis(self):
        self.btnCambiarPantallaMapaDis.emit()

    def cambiar_a_pantalla_mapa_cont(self):
        self.btnCambiarPantallaMapaCont.emit()

    def mensaje(self, prompt, txt):
        """Muestra error con messagebox"""
        tk.messagebox.showerror(prompt, txt)
    
if __name__ == "__main__":
    from mediador_view import MediadorView
    ventana = tk.Tk()
    mediador_view = MediadorView(ventana)
    mediador_view.cambiar_frame_view('ViewInicio')
    mediador_view.obtener_frame_view_actual()
    ventana.mainloop()

