import requests
from Ciudad import Ciudad
from Parametro import Parametro


class SolicitudOpenMeteo:
    def __init__(self):
        self.url_geocoding = "https://geocoding-api.open-meteo.com/v1/search"
        self.url_tiempo = "https://api.open-meteo.com/v1/forecast"

    def buscar_ciudad(self, nombre_ciudad):
        try:
            params = {
                "name": nombre_ciudad,
                "count": 1,
                "language": "es",
                "format": "json"
            }

            respuesta = requests.get(self.url_geocoding, params=params)
            datos = respuesta.json()

            if "results" not in datos or len(datos["results"]) == 0:
                return None

            ciudad_encontrada = datos["results"][0]

            ciudad = Ciudad(
                nombre=ciudad_encontrada["name"],
                latitud=ciudad_encontrada["latitude"],
                longitud=ciudad_encontrada["longitude"]
            )

            return ciudad

        except Exception as e:
            print("Error al buscar la ciudad:", e)
            return None

    def obtener_parametros(self, latitud, longitud):
        try:
            params = {
                "latitude": latitud,
                "longitude": longitud,
                "current": "temperature_2m,relative_humidity_2m,wind_speed_10m"
            }

            respuesta = requests.get(self.url_tiempo, params=params)
            datos = respuesta.json()

            actuales = datos["current"]

            parametro = Parametro(
                temperatura=actuales["temperature_2m"],
                humedad=actuales["relative_humidity_2m"],
                viento=actuales["wind_speed_10m"]
            )

            return parametro

        except Exception as e:
            print("Error al obtener el clima:", e)
            return None

    def obtener_ciudad_con_clima(self, nombre_ciudad):
        ciudad = self.buscar_ciudad(nombre_ciudad)

        if ciudad is None:
            return None

        parametros = self.obtener_parametros(ciudad.latitud, ciudad.longitud)

        if parametros is not None:
            ciudad.parametros = parametros

        return ciudad