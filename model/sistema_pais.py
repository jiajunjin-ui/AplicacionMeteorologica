import requests
import geonamescache
import os
import unicodedata

from .pais import Pais
from .localidad import Localidad


class SistemaPais:
    """Clase encargada de buscar paises y sus ciudades principales."""

    def __init__(self):
        self.url_buscar_pais = "https://nominatim.openstreetmap.org/search"
        self.geo_cache = geonamescache.GeonamesCache()
        self._paises_encontrados = {}
        self._catalogo_paises = self._crear_catalogo_paises()

    def normalizar_texto(self, texto):
        texto = texto.strip().lower()
        texto = unicodedata.normalize("NFD", texto)
        texto = "".join(
            caracter for caracter in texto
            if unicodedata.category(caracter) != "Mn"
        )
        return texto

    def _crear_catalogo_paises(self):
        catalogo = {}
        ruta_paises = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "datos",
            "paises_es.txt"
        )

        with open(ruta_paises, encoding="utf-8") as fichero:
            for linea in fichero:
                linea = linea.strip()

                if not linea:
                    continue

                codigo_iso, nombre = linea.split("|", maxsplit=1)
                catalogo[nombre] = Pais(nombre=nombre, codigo_iso=codigo_iso)

        return catalogo

    def buscador_nombre_pais(self, texto):
        """Busca paises que coincidan con el texto introducido."""

        texto = texto.strip()

        if len(texto) < 3:
            raise ValueError("Se deben introducir al menos 3 letras del pais.")

        texto_normalizado = self.normalizar_texto(texto)

        self._paises_encontrados = {}

        for nombre, pais in self._catalogo_paises.items():
            nombre_normalizado = self.normalizar_texto(nombre)

            if nombre_normalizado.startswith(texto_normalizado):
                self._paises_encontrados[nombre] = Pais(
                    nombre=pais.nombre,
                    codigo_iso=pais.codigo_iso
                )

        if not self._paises_encontrados:
            for nombre, pais in self._catalogo_paises.items():
                nombre_normalizado = self.normalizar_texto(nombre)

                if texto_normalizado in nombre_normalizado:
                    self._paises_encontrados[nombre] = Pais(
                        nombre=pais.nombre,
                        codigo_iso=pais.codigo_iso
                    )

        if not self._paises_encontrados:
            raise ValueError("No se encontro ningun pais.")

        return sorted(self._paises_encontrados.keys())

    def seleccionar_pais(self, nombre_pais):
        """Devuelve el pais seleccionado de la lista generada."""

        if nombre_pais not in self._paises_encontrados:
            raise KeyError("Seleccione un pais de la lista generada.")

        return self._paises_encontrados[nombre_pais]

    def buscar_pais(self, nombre_pais):
        nombre_pais = nombre_pais.strip()

        if not nombre_pais:
            raise ValueError("Introduce un pais.")

        if nombre_pais in self._paises_encontrados:
            return self._paises_encontrados[nombre_pais]

        if nombre_pais in self._catalogo_paises:
            return self._catalogo_paises[nombre_pais]

        nombre_normalizado = self.normalizar_texto(nombre_pais)

        for nombre, pais in self._catalogo_paises.items():
            if self.normalizar_texto(nombre) == nombre_normalizado:
                return Pais(nombre=pais.nombre, codigo_iso=pais.codigo_iso)

        params = {
            "q": nombre_pais,
            "format": "jsonv2",
            "addressdetails": 1,
            "featureType": "country",
            "limit": 5,
            "accept-language": "es"
        }

        headers = {
            "User-Agent": "AplicacionMeteorologica/1.0"
        }

        respuesta = requests.get(
            self.url_buscar_pais,
            params=params,
            headers=headers
        ).json()

        if not respuesta:
            raise ValueError("No se encontro el pais introducido.")

        primer_pais = None

        for resultado in respuesta:
            if resultado.get("addresstype") != "country":
                continue

            direccion = resultado.get("address", {})
            nombre = direccion.get("country")
            codigo_iso = direccion.get("country_code")

            if nombre is None or codigo_iso is None:
                continue

            pais = Pais(
                nombre=nombre,
                codigo_iso=codigo_iso.upper()
            )

            if primer_pais is None:
                primer_pais = pais

            if self.normalizar_texto(nombre) == nombre_normalizado:
                return pais

        if primer_pais is not None:
            return primer_pais

        raise ValueError("Introduce un pais valido.")

    def buscar_ciudades_principales(self, nombre_pais, cantidad=3):
        pais = self.buscar_pais(nombre_pais)
        pais.localidades = []

        ciudades = self.geo_cache.get_cities()
        ciudades_del_pais = []

        for ciudad in ciudades.values():
            if ciudad["countrycode"] == pais.codigo_iso:
                ciudades_del_pais.append(ciudad)

        if not ciudades_del_pais:
            raise ValueError("No se encontraron ciudades principales para ese pais.")

        ciudades_del_pais.sort(
            key=lambda ciudad: ciudad.get("population", 0),
            reverse=True
        )

        for ciudad in ciudades_del_pais[:cantidad]:
            localidad = Localidad(
                nombre=ciudad["name"],
                lat=float(ciudad["latitude"]),
                lon=float(ciudad["longitude"]),
                forzar_set=True
            )

            pais.agregar_localidad(localidad)

        return pais
