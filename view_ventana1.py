import tkinter as tk
from tkintermapview import TkinterMapView
from model import Event

class TkView:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Mapa meteorológico")
        self.ventana.geometry("960x540")
        self.marcador_actual = None

        self.btn_buscar = Event()
        self.btn_temp = Event()
        self.btn_cielo = Event()
        self.btn_ranking = Event()

        self.setup_ui()

    def setup_ui(self):
        '''VENTANA PRINCIPAL TIENE DOS COLUMNAS: DERECHA (MAPA) - IZQUIERDA (CONTROLES)'''
        self.ventana.grid_columnconfigure(0, weight=1)  # Grosor columna izquierda
        self.ventana.grid_columnconfigure(1, weight=3)  # Grosor columna derecha
        self.ventana.grid_rowconfigure(0, weight=1)     # Grosor filas

        # COLUMNA IZQUIERDA
        columna_izq = tk.Frame(self.ventana, padx=10, pady=10)
        columna_izq.grid(row=0, column=0, sticky="nsew")

        tk.Label(columna_izq, text="Introduce una región:").grid(row=0, column=0, sticky="w")

        self.entrada_ciudad = tk.Entry(columna_izq, width=25)
        self.entrada_ciudad.grid(row=1, column=0, sticky="ew")
        btn_buscar = tk.Button(columna_izq, text="Buscar en mapa", command=lambda: self.opera("1"))
        btn_buscar.grid(row=2, column=0, pady=5, sticky="ew")
        btn_temp = tk.Button(columna_izq, text="Mapa de temperaturas", command=lambda: self.opera("2"))
        btn_temp.grid(row=3, column=0, pady=5, sticky="ew")
        btn_cielo = tk.Button(columna_izq, text="Estado del cielo", command=lambda: self.opera("3"))
        btn_cielo.grid(row=4, column=0, pady=5, sticky="ew")
        btn_ranking = tk.Button(columna_izq, text="Ranking", command=lambda: self.opera("4"))
        btn_ranking.grid(row=5, column=0, pady=5, sticky="ew")

        columna_izq.grid_columnconfigure(0, weight=1)

        # COLUMNA DERECHA
        mapa = tk.Frame(self.ventana)
        mapa.grid(row=0, column=1, sticky="nsew")
        self.mapa = TkinterMapView(mapa, width=600, height=500, corner_radius=0)
        self.mapa.pack(fill="both", expand=True)
        self.mapa.set_position(40.4168, -3.7038)
        self.mapa.set_zoom(6)

    def obtener_ciudad_buscada(self):
        return self.entrada_ciudad.get().strip()

    def mostrar_error(self, mensaje):
        print("Aun falta por implementar")

    def mostrar_ciudad_en_mapa(self, ciudad):
        if self.marcador_actual is not None:
            self.marcador_actual.delete()

        self.mapa.set_position(ciudad.latitud, ciudad.longitud)
        self.mapa.set_zoom(7)

        texto_marcador = ciudad.nombre
        if ciudad.parametros is not None:
            texto_marcador = f"{ciudad.nombre}\n{ciudad.parametros.temperatura} ºC"

        self.marcador_actual = self.mapa.set_marker(
            ciudad.latitud,
            ciudad.longitud,
            text=texto_marcador,
        )

    def opera(self, op):
        if op == "1":
            self.btn_buscar.emit()
        if op == "2":
            self.btn_temp.emit()
        if op == "3":
            self.btn_cielo.emit()
        if op == "4":
            self.btn_ranking.emit()

if __name__ == '__main__':
    from presenter_ventana1 import Presenter
    from model.Mapa import Mapa as Model

    ventana = tk.Tk()
    modelo = Model()
    vista = TkView(ventana)
    Presenter(vista, modelo)
    ventana.mainloop()
