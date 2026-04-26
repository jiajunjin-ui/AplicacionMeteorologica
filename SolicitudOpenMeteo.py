import requests
import pandas as pd

from Ciudad import Ciudad
from Parametro import Parametro


class SolicitudOpenMeteo:
    """Servicio para geocoding, clima actual, previsión horaria y geocoding inverso."""

    def __init__(self):
        self.url_geocoding = "https://geocoding-api.open-meteo.com/v1/search"
        self.url_tiempo = "https://api.open-meteo.com/v1/forecast"
        self.url_geocoding_inverso = "https://nominatim.openstreetmap.org/reverse"
        self.ciudad_buscador = None

    # FUNCIONES PARA EL MAPA

    def buscar_ciudad(self, nombre_ciudad):
        try:
            params = {
                "name": nombre_ciudad,
                "count": 1,
                "language": "es",
                "format": "json",
            }

            respuesta = requests.get(self.url_geocoding, params=params).json()

            resultados = respuesta.get("results", [])
            if not resultados:
                raise ValueError(f"La ciudad '{nombre_ciudad}' no se encuentra en Open-Meteo.")

            ciudad_encontrada = resultados[0]

            return Ciudad(
                nombre=ciudad_encontrada["name"],
                latitud=ciudad_encontrada["latitude"],
                longitud=ciudad_encontrada["longitude"],
            )

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

            respuesta = requests.get(self.url_tiempo, params=params).json()

            actuales = respuesta["current"]

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

    def obtener_punto_con_clima(self, latitud, longitud):
        nombre_lugar = self.obtener_nombre_desde_coordenadas(latitud, longitud)

        ciudad = Ciudad(
            nombre=nombre_lugar,
            latitud=latitud,
            longitud=longitud,
        )

        parametros = self.obtener_parametros(latitud, longitud)

        if parametros is not None:
            ciudad.parametros = parametros

        return ciudad

    def obtener_nombre_desde_coordenadas(self, latitud, longitud):
        try:
            params = {
                "lat": latitud,
                "lon": longitud,
                "format": "jsonv2",
                "addressdetails": 1,
                "accept-language": "es",
            }

            headers = {"User-Agent": "AplicacionMeteorologica/1.0"}

            respuesta = requests.get(self.url_geocoding_inverso, params=params, headers=headers).json()

            direccion = respuesta.get("address", {})
            nombre = (
                direccion.get("city")
                or direccion.get("town")
                or direccion.get("village")
                or direccion.get("municipality")
                or direccion.get("hamlet")
                or direccion.get("county")
                or direccion.get("state")
                or direccion.get("display_name")
            )

            return nombre or f"Punto ({latitud:.2f}, {longitud:.2f})"

        except Exception as e:
            print("Error al obtener el nombre del lugar:", e)
            return f"Punto ({latitud:.2f}, {longitud:.2f})"

    # FUNCIONES PARA EL GRÁFICO

    def buscar_ciudades(self, texto):
        """Devuelve una lista de ciudades para que la vista cree botones."""
        self.ciudad_buscador = Ciudad(texto)
        return self.ciudad_buscador.buscar_ciudades()

    def obtener_prevision_horaria(self, ciudad_select):
        """Devuelve un DataFrame horario de 3 días para la ciudad seleccionada."""
        if self.ciudad_buscador is None:
            raise ValueError("Primero hay que buscar una ciudad.")

        latitud, longitud = self.ciudad_buscador.obtener_coordenadas(ciudad_select)

        params = {
            "latitude": latitud,
            "longitude": longitud,
            "hourly": ",".join(
                [
                    "temperature_2m",
                    "relative_humidity_2m",
                    "precipitation_probability",
                    "wind_speed_10m",
                    "weather_code",
                ]
            ),
            "forecast_days": 3,
            "timezone": "auto",
        }

        respuesta = requests.get(self.url_tiempo, params=params).json()

        hourly = respuesta.get("hourly")

        dataframe = pd.DataFrame(
            {
                "date": pd.to_datetime(hourly["time"]),
                "temp_2m": hourly["temperature_2m"],
                "hum_rel": hourly["relative_humidity_2m"],
                "prob_precip": hourly["precipitation_probability"],
                "wind_speed_10m": hourly["wind_speed_10m"],
                "weather_code": hourly["weather_code"],
            }
        )

        return dataframe
