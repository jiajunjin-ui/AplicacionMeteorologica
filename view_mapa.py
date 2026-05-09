import tkinter as tk
import tkinter.messagebox
from tkintermapview import TkinterMapView
from model import Event
import os
from PIL import Image, ImageTk

class ViewMapa:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Mapa meteorologico")
        self.ventana.geometry("960x560")

        self.marcador_actual = None
        self.nombre_actual = None
        self.lat_actual = None
        self.lon_actual = None
        self.temperatura_actual = None
        self.humedad_actual = None
        self.viento_actual = None
        self.tipo_icono_actual = None

        self.icono_sol = self.cargar_icono("sol.png")
        self.icono_nube = self.cargar_icono("nube.png")
        self.icono_lluvia = self.cargar_icono("lluvia.png")
        self.icono_tormenta = self.cargar_icono("tormenta.png")
        self.icono_nieve = self.cargar_icono("nieve.png")
        self.icono_niebla = self.cargar_icono("niebla.png")

        self.btn_buscar = Event()
        self.btn_select = Event()
        self.click_mapa = Event()

        self.lista_btn = []

        self.setup_ui()

    def setup_ui(self):
        """VENTANA PRINCIPAL TIENE DOS COLUMNAS: DERECHA (MAPA) - IZQUIERDA (CONTROLES)"""
        self.ventana.grid_columnconfigure(0, weight=1)
        self.ventana.grid_columnconfigure(1, weight=3)
        self.ventana.grid_rowconfigure(0, weight=1)

        # COLUMNA IZQUIERDA
        self.columna_izq = tk.Frame(self.ventana, padx=10, pady=10)
        self.columna_izq.grid(row=0, column=0, sticky="nsew")

        tk.Label(self.columna_izq, text="Introduce una ciudad/pais:").grid(row=0, column=0, sticky="w")

        self.entrada_ciudad = tk.Entry(self.columna_izq, width=25)
        self.entrada_ciudad.grid(row=1, column=0, sticky="ew")

        btn_buscar = tk.Button(self.columna_izq, text="Ubicar en el mapa", command=lambda: self.opera("1"))
        btn_buscar.grid(row=2, column=0, pady=5, sticky="ew")

        self.mostrar_temperatura = tk.BooleanVar(value=True)
        self.mostrar_humedad = tk.BooleanVar(value=True)
        self.mostrar_viento = tk.BooleanVar(value=True)

        chk_temp = tk.Checkbutton(self.columna_izq, text="Temperatura", variable=self.mostrar_temperatura, command=self.actualizar_marcador_actual)
        chk_temp.grid(row=3, column=0, pady=5, sticky="w")
        chk_humedad = tk.Checkbutton(self.columna_izq, text="Humedad", variable=self.mostrar_humedad, command=self.actualizar_marcador_actual)
        chk_humedad.grid(row=4, column=0, pady=5, sticky="w")
        chk_viento = tk.Checkbutton(self.columna_izq, text="Viento", variable=self.mostrar_viento, command=self.actualizar_marcador_actual)
        chk_viento.grid(row=5, column=0, pady=5, sticky="w")

        self.columna_izq.grid_columnconfigure(0, weight=1)

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

    def mostrar_ciudad_en_mapa(self, nombre, lat, lon, temperatura, humedad, viento, tipo_icono):
        self.nombre_actual = nombre
        self.lat_actual = lat
        self.lon_actual = lon
        self.temperatura_actual = temperatura
        self.humedad_actual = humedad
        self.viento_actual = viento
        self.tipo_icono_actual = tipo_icono

        if self.marcador_actual is not None:
            self.marcador_actual.delete()

        self.mapa.set_position(lat, lon)
        self.mapa.set_zoom(7)

        texto = self.construir_texto_marcador()
        icono = self.elegir_icono(tipo_icono)

        self.marcador_actual = self.mapa.set_marker(
            lat,
            lon,
            text=texto,
            icon=icono,
            icon_anchor="center"
        )

    def cargar_icono(self, nombre_archivo):
        carpeta_actual = os.path.dirname(__file__)
        ruta_icono = os.path.join(carpeta_actual, "iconos", nombre_archivo)

        imagen = Image.open(ruta_icono)
        imagen = imagen.resize((70, 70))

        return ImageTk.PhotoImage(imagen)

    def elegir_icono(self, tipo_icono):
        if tipo_icono == "sol":
            return self.icono_sol
        if tipo_icono == "nube":
            return self.icono_nube
        if tipo_icono == "lluvia":
            return self.icono_lluvia
        if tipo_icono == "tormenta":
            return self.icono_tormenta
        if tipo_icono == "nieve":
            return self.icono_nieve
        if tipo_icono == "niebla":
            return self.icono_niebla

    def construir_texto_marcador(self):
        if self.nombre_actual is None:
            return ""

        detalles = []

        if self.mostrar_temperatura.get() and self.temperatura_actual is not None:
            detalles.append(f"{self.temperatura_actual:.2f} °C")

        if self.mostrar_humedad.get() and self.humedad_actual is not None:
            detalles.append(f"{self.humedad_actual}%")

        if self.mostrar_viento.get() and self.viento_actual is not None:
            detalles.append(f"{self.viento_actual:.2f} km/h")

        if not detalles:
            return self.nombre_actual

        return self.nombre_actual + "\n" + " | ".join(detalles)

    def actualizar_marcador_actual(self):
        if self.nombre_actual is not None:
            self.mostrar_ciudad_en_mapa(
                self.nombre_actual,
                self.lat_actual,
                self.lon_actual,
                self.temperatura_actual,
                self.humedad_actual,
                self.viento_actual,
                self.tipo_icono_actual
            )

    def opera(self, op):
        if op == "1":
            self.btn_buscar.emit()

    def mostrar_lista_ciudades(self, lista):
        self.limpiar_lista_btn()
        for n, nombre_ciudad in enumerate(lista):
            boton = tk.Button(
                        self.columna_izq, 
                        text=nombre_ciudad, 
                        command=lambda ciudad=nombre_ciudad: self.seleccionar_ciudad(ciudad), 
                        width=30
            )
            boton.grid(row=n+6, column=0, pady=5, sticky="w")
            self.lista_btn.append(boton)
    
    def limpiar_lista_btn(self):
        """Funcion que borra la lista de botones."""
        for boton in self.lista_btn:
            boton.destroy()
        self.lista_btn.clear()
    
    def seleccionar_ciudad(self, nombre_ciudad):
        """Funcion que toma la referencia (str) de la ciudad elegida por
           el usuario, para operar con ella."""
        self.btn_select.emit(nombre_ciudad)
        self.limpiar_lista_btn()

if __name__ == "__main__":
    ventana = tk.Tk()
    vista = ViewMapa(ventana)
    ventana.mainloop()
