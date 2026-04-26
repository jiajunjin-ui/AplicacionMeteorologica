import tkinter as tk
from tkintermapview import TkinterMapView
from Event import Event


class TkView:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Mapa meteorologico")
        self.ventana.geometry("960x540")

        self.marcador_actual = None
        self.ciudad_actual = None

        self.btn_buscar = Event()
        self.click_mapa = Event()

        self.setup_ui()

    def setup_ui(self):
        """VENTANA PRINCIPAL TIENE DOS COLUMNAS: DERECHA (MAPA) - IZQUIERDA (CONTROLES)"""
        self.ventana.grid_columnconfigure(0, weight=1)
        self.ventana.grid_columnconfigure(1, weight=3)
        self.ventana.grid_rowconfigure(0, weight=1)

        # COLUMNA IZQUIERDA
        columna_izq = tk.Frame(self.ventana, padx=10, pady=10)
        columna_izq.grid(row=0, column=0, sticky="nsew")

        tk.Label(columna_izq, text="Introduce una ciudad/pais:").grid(row=0, column=0, sticky="w")

        self.entrada_ciudad = tk.Entry(columna_izq, width=25)
        self.entrada_ciudad.grid(row=1, column=0, sticky="ew")

        btn_buscar = tk.Button(columna_izq, text="Ubicar en el mapa", command=lambda: self.opera("1"))
        btn_buscar.grid(row=2, column=0, pady=5, sticky="ew")

        self.mostrar_temperatura = tk.BooleanVar(value=True)
        self.mostrar_humedad = tk.BooleanVar(value=True)
        self.mostrar_viento = tk.BooleanVar(value=True)

        chk_temp = tk.Checkbutton(columna_izq, text="Temperatura", variable=self.mostrar_temperatura, command=self.actualizar_marcador_actual)
        chk_temp.grid(row=3, column=0, pady=5, sticky="w")
        chk_humedad = tk.Checkbutton(columna_izq, text="Humedad", variable=self.mostrar_humedad, command=self.actualizar_marcador_actual)
        chk_humedad.grid(row=4, column=0, pady=5, sticky="w")
        chk_viento = tk.Checkbutton(columna_izq, text="Viento", variable=self.mostrar_viento, command=self.actualizar_marcador_actual)
        chk_viento.grid(row=5, column=0, pady=5, sticky="w")

        columna_izq.grid_columnconfigure(0, weight=1)

        # COLUMNA DERECHA
        mapa = tk.Frame(self.ventana)
        mapa.grid(row=0, column=1, sticky="nsew")
        self.mapa = TkinterMapView(mapa, width=600, height=500, corner_radius=0)
        self.mapa.pack(fill="both", expand=True)
        self.mapa.set_position(40.4168, -3.7038)
        self.mapa.set_zoom(6)

        self.mapa.add_left_click_map_command(self.al_hacer_click_mapa)

    def obtener_ciudad_buscada(self):
        return self.entrada_ciudad.get().strip()

    def mostrar_error(self, mensaje):
        print(mensaje)

    def al_hacer_click_mapa(self, coordenadas):
        """
        Esta funcion se ejecuta cuando el usuario hace clic en el mapa.

        coordenadas es una tupla:
        (latitud, longitud)
        """
        self.click_mapa.emit(coordenadas)

    def mostrar_ciudad_en_mapa(self, ciudad):
        self.ciudad_actual = ciudad

        if self.marcador_actual is not None:
            self.marcador_actual.delete()

        self.mapa.set_position(ciudad.latitud, ciudad.longitud)
        self.mapa.set_zoom(7)

        self.marcador_actual = self.mapa.set_marker(
            ciudad.latitud,
            ciudad.longitud,
            text=self.construir_texto_marcador(ciudad),
        )

    def construir_texto_marcador(self, ciudad):
        if ciudad.parametros is None:
            return ciudad.nombre

        detalles = []

        if self.mostrar_temperatura.get() and ciudad.parametros.temperatura is not None:
            detalles.append(f"{ciudad.parametros.temperatura} °C")
        if self.mostrar_humedad.get() and ciudad.parametros.humedad is not None:
            detalles.append(f"{ciudad.parametros.humedad}%")
        if self.mostrar_viento.get() and ciudad.parametros.viento is not None:
            detalles.append(f"{ciudad.parametros.viento} km/h")

        if not detalles:
            return ciudad.nombre

        return f"{ciudad.nombre}\n" + " | ".join(detalles)

    def actualizar_marcador_actual(self):
        if self.ciudad_actual is not None:
            self.mostrar_ciudad_en_mapa(self.ciudad_actual)

    def opera(self, op):
        if op == "1":
            self.btn_buscar.emit()


if __name__ == '__main__':
    from Presenter import Presenter
    from FacadeModel import FacadeModel

    ventana = tk.Tk()
    modelo = FacadeModel()
    vista = TkView(ventana)
    Presenter(vista, modelo)
    ventana.mainloop() #
