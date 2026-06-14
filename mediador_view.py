import tkinter as tk
from view_grafico import ViewGrafico
from view_mapa import ViewMapa
from view_inicio import ViewInicio
from view_ranking import ViewRanking


class MediadorView:
    def __init__(self, ventana):

        # Stacked de pantallas ############################
        self.ventana = ventana
        self.contenedor = tk.Frame(self.ventana)
        self.contenedor.pack(expand=True, fill="both")

        self._dic_views = {}
        self._view_actual = None

        # Registro de pantallas ###########################
        self._registrar_view(ViewGrafico)
        self._registrar_view(ViewMapa)
        self._registrar_view(ViewRanking)
        self._registrar_view(ViewInicio)

    def _registrar_view(self, view):
        nombre_view = view.__name__
        frame_view = view(parent=self.contenedor, mediador_view=self)
        frame_view.grid(row=0, column=0, sticky="nsew")
        self._dic_views[nombre_view] = frame_view

    def cambiar_frame_view(self, nombre_pantalla):
        frame_pantalla = self._dic_views.get(nombre_pantalla)
        if frame_pantalla:
            self._view_actual = frame_pantalla
            self.ventana.title(frame_pantalla.titulo)
            self.ventana.geometry(frame_pantalla.size)
            frame_pantalla.tkraise()
        else:
            raise KeyError(f'La pantalla {nombre_pantalla} no existe')

    def obtener_frame_view_actual(self):
        return self._view_actual