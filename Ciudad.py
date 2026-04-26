import requests
from Parametro import Parametro

class Ciudad:
    _caracteres_invalidos = '#%/<>"(){[&:;|+=*@#~$€£0123456789}]'
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    def __init__(self, nombre=None, latitud=None, longitud=None):
        self._nombre = nombre
        self.latitud = latitud
        self.longitud = longitud
        self.parametros = Parametro()
        self._datos_ciudades = {}

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, new_nombre):   # Esta funcion no se esta usando!
        if not isinstance(new_nombre, str):
            raise TypeError(f"El nombre debe ser una cadena de texto, no {type(new_nombre).__name__}")
        if not new_nombre.strip():
            raise ValueError("Nombre en blanco!")
        if any(caracter in self._caracteres_invalidos for caracter in new_nombre):
            raise ValueError(f"{new_nombre} contiene caracteres inválidos.")

        self._nombre = new_nombre

    def buscar_ciudades(self):
        """Funcion se conecta al servicio de geocoding de OpenMeteo para buscar nombres de ciudades
        que presenten cierta coincidencia con el str introducido.
        """
        if len(self.nombre) < 3:
            raise ValueError("Se deben introducir al menos 3 letras.")

        params = {
            "name": self.nombre,
            "count": 10,
            "language": "es",
            "format": "json",
        }

        respuesta = requests.get(self.geo_url, params=params).json()
        resultados = respuesta.get("results", [])

        if not resultados:
            raise ValueError(f"La ciudad '{self.nombre}' no se encuentra en Open-Meteo.")

        self._datos_ciudades.clear()

        for resultado in resultados:
            self._datos_ciudades[resultado["name"]] = (resultado["latitude"], resultado["longitude"])

        return list(self._datos_ciudades.keys())

    def obtener_coordenadas(self, ciudad_select):
        """Función que devuelve las coordenadas de la ciudad seleccionada por el usuario."""
        if ciudad_select not in self._datos_ciudades:
            raise KeyError("Seleccione una ciudad de la lista generada.")
        self.latitud, self.longitud = self._datos_ciudades[ciudad_select]
        self.nombre = ciudad_select
        return self.latitud, self.longitud