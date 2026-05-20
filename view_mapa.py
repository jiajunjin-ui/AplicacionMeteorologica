import tkinter as tk
import tkinter.messagebox
from tkintermapview import TkinterMapView
from model import Event
from view_base import ViewBase
import os
from PIL import Image, ImageTk

class ViewMapa(ViewBase):
    def __init__(self, parent, mediador_view):
        super().__init__(
            parent, 
            mediador_view, 
            titulo = "Mapa meteorologico", 
            size = '960x560')

        self.marcador_actual = None
        self.marcadores_actuales = []
        self.datos_marcadores_actuales = []

        self.icono_sol = self.cargar_icono("sol.png")
        self.icono_nube = self.cargar_icono("nube.png")
        self.icono_lluvia = self.cargar_icono("lluvia.png")
        self.icono_tormenta = self.cargar_icono("tormenta.png")
        self.icono_nieve = self.cargar_icono("nieve.png")
        self.icono_niebla = self.cargar_icono("niebla.png")
        self.icono_luna = self.cargar_icono("luna.png")

        self.btn_buscar = Event()
        self.btn_select = Event()
        self.click_mapa = Event()
        self.btn_buscar_pais = Event()

        self.lista_btn = []

        self.setup_ui()

    def setup_ui(self):
        """VENTANA PRINCIPAL TIENE DOS COLUMNAS: DERECHA (MAPA) - IZQUIERDA (CONTROLES)"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        # COLUMNA IZQUIERDA
        self.columna_izq = tk.Frame(self, width=200, padx=10, pady=10)
        self.columna_izq.grid(row=0, column=0, sticky="nsew")
        self.columna_izq.grid_propagate(False)

        tk.Label(self.columna_izq, text="Introduce una localidad/país:").grid(row=0, column=0, sticky="w")

        self.entrada_ciudad = tk.Entry(self.columna_izq, width=25)
        self.entrada_ciudad.grid(row=1, column=0, sticky="ew")

        btn_buscar = tk.Button(self.columna_izq, text="Mostrar localidad", command=lambda: self.opera("1"))
        btn_buscar.grid(row=2, column=0, pady=5, sticky="ew")

        btn_buscar_pais = tk.Button(self.columna_izq, text="Mostrar país", command=lambda: self.opera("2"))
        btn_buscar_pais.grid(row=3, column=0, pady=5, sticky="ew")

        self.mostrar_temperatura = tk.BooleanVar(value=True)
        self.mostrar_humedad = tk.BooleanVar(value=True)
        self.mostrar_viento = tk.BooleanVar(value=True)

        chk_temp = tk.Checkbutton(self.columna_izq, text="Temperatura", variable=self.mostrar_temperatura, command=self.actualizar_marcador_actual)
        chk_temp.grid(row=4, column=0, pady=5, sticky="w")
        chk_humedad = tk.Checkbutton(self.columna_izq, text="Humedad", variable=self.mostrar_humedad, command=self.actualizar_marcador_actual)
        chk_humedad.grid(row=5, column=0, pady=5, sticky="w")
        chk_viento = tk.Checkbutton(self.columna_izq, text="Viento", variable=self.mostrar_viento, command=self.actualizar_marcador_actual)
        chk_viento.grid(row=6, column=0, pady=5, sticky="w")

        self.columna_izq.grid_columnconfigure(0, weight=1)

        # COLUMNA DERECHA
        mapa = tk.Frame(self)
        mapa.grid(row=0, column=1, sticky="nsew")
        self.mapa = TkinterMapView(mapa, width=600, height=560, corner_radius=0)
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
        datos_ciudad = {
            "nombre": nombre,
            "lat": lat,
            "lon": lon,
            "temperatura": temperatura,
            "humedad": humedad,
            "viento": viento,
            "tipo_icono": tipo_icono
        }

        self.mostrar_varias_ciudades_en_mapa([datos_ciudad])

        self.mapa.set_position(lat, lon)
        self.mapa.set_zoom(7)

    def cargar_icono(self, nombre_archivo):
        carpeta_actual = os.path.dirname(__file__)
        ruta_icono = os.path.join(carpeta_actual, "iconos", nombre_archivo)

        imagen = Image.open(ruta_icono)
        imagen = imagen.resize((70, 70))

        return ImageTk.PhotoImage(imagen)

    def elegir_icono(self, tipo_icono):
        if tipo_icono == "sol":
            return self.icono_sol
        if tipo_icono == "luna":
            return self.icono_luna
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

    def construir_texto_marcador(self, datos):
        nombre = datos["nombre"]
        temperatura = datos["temperatura"]
        humedad = datos["humedad"]
        viento = datos["viento"]

        detalles = []

        if self.mostrar_temperatura.get() and temperatura is not None:
            detalles.append(f"{temperatura:.2f} °C")

        if self.mostrar_humedad.get() and humedad is not None:
            detalles.append(f"{humedad:.2f}%")

        if self.mostrar_viento.get() and viento is not None:
            detalles.append(f"{viento:.2f} km/h")

        if not detalles:
            return nombre

        return nombre + "\n" + " | ".join(detalles)

    def actualizar_marcador_actual(self):
        if self.datos_marcadores_actuales:
            self.mostrar_varias_ciudades_en_mapa(
                self.datos_marcadores_actuales,
                actualizar_vista=False
            )

    def opera(self, op):
        if op == "1":
            self.btn_buscar.emit()
        if op == "2":
            self.btn_buscar_pais.emit()

    def mostrar_lista_ciudades(self, lista):
        self.limpiar_lista_btn()
        for n, nombre_ciudad in enumerate(lista):
            boton = tk.Button(
                        self.columna_izq, 
                        text=nombre_ciudad, 
                        command=lambda ciudad=nombre_ciudad: self.seleccionar_ciudad(ciudad), 
                        width=30
            )
            boton.grid(row=n+7, column=0, pady=2)
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

    def limpiar_marcadores(self):
        for marcador in self.marcadores_actuales:
            marcador.delete()

        self.marcadores_actuales.clear()

    def mostrar_varias_ciudades_en_mapa(self, datos_ciudades, actualizar_vista=True):
        self.datos_marcadores_actuales = datos_ciudades

        self.limpiar_marcadores()

        if not datos_ciudades:
            return

        suma_lat = 0
        suma_lon = 0

        for datos in datos_ciudades:
            lat = datos["lat"]
            lon = datos["lon"]

            suma_lat = suma_lat + lat
            suma_lon = suma_lon + lon

            texto = self.construir_texto_marcador(datos)
            icono = self.elegir_icono(datos["tipo_icono"])

            marcador = self.mapa.set_marker(
                lat,
                lon,
                text=texto,
                icon=icono,
                icon_anchor="s"
            )

            self.marcadores_actuales.append(marcador)

        if not actualizar_vista:
            return

        lat_media = suma_lat / len(datos_ciudades)
        lon_media = suma_lon / len(datos_ciudades)

        self.mapa.set_position(lat_media, lon_media)
        self.mapa.set_zoom(5)

if __name__ == "__main__":
    from mediador_view import MediadorView
    ventana = tk.Tk()
    mediador_view = MediadorView(ventana)
    mediador_view.cambiar_frame_view('ViewMapa')
    mediador_view.obtener_frame_view_actual()
    ventana.mainloop()