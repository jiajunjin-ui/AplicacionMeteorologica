import tkinter as tk
from tkinter import ttk
import tkinter.messagebox

from view_base import ViewBase
from model import Event


class ViewInicio(ViewBase):
    def __init__(self, parent, mediador_view):
        super().__init__(
            parent,
            mediador_view,
            titulo="Prueba",
            size='400x300')

        # Eventos: patrón Observer ###########################
        self.btnCambiarPantallaGrafico = Event()
        self.btnCambiarPantallaMapa = Event()
        self.btnCambiarPantallaRanking = Event()

    def setup_ui(self):
        # Frame Centrado #####################################
        self.frame_central = ttk.Frame(self)
        self.frame_central.grid(row=0, column=0, padx=110, pady=80)

        # Elementos ##########################################
        self.btn_ir_a_grafico = tk.Button(self.frame_central,
                                          text='Previsión por ciudad',
                                          width=20,
                                          font=("Arial", 11),
                                          command=lambda: self.cambiar_a_pantalla_grafico()
                                          )
        self.btn_ir_a_mapa = tk.Button(self.frame_central,
                                       text='Mapas',
                                       width=20,
                                       font=("Arial", 11),
                                       command=lambda: self.cambiar_a_pantalla_mapa()
                                       )
        self.btn_ir_a_ranking = tk.Button(self.frame_central,
                                       text='Ranking',
                                       width=20,
                                       font=("Arial", 11),
                                       command=lambda: self.cambiar_a_pantalla_ranking()
                                       )

        # Organización #######################################
        self.btn_ir_a_grafico.grid(row=0, column=0)
        self.btn_ir_a_mapa.grid(row=1, column=0)
        self.btn_ir_a_ranking.grid(row=2, column=0)

    def cambiar_a_pantalla_grafico(self):
        self.btnCambiarPantallaGrafico.emit()

    def cambiar_a_pantalla_mapa(self):
        self.btnCambiarPantallaMapa.emit()

    def cambiar_a_pantalla_ranking(self):
        self.btnCambiarPantallaRanking.emit()

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