import requests
import geonamescache

from .pais import Pais
from .localidad import Localidad


class SistemaPais:
    """Clase encargada de buscar países y sus ciudades principales."""

    def __init__(self):
        self.url_buscar_pais = "https://nominatim.openstreetmap.org/search"
        self.geo_cache = geonamescache.GeonamesCache()

    def buscar_pais(self, nombre_pais):
        if not nombre_pais.strip():
            raise ValueError("Introduce un país.")

        params = {
            "q": nombre_pais,
            "format": "jsonv2",
            "addressdetails": 1,
            "limit": 5,
            "accept-language": "es",
            "featuretype": "country"
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
            raise ValueError("No se encontró el país introducido.")

        for resultado in respuesta:
            tipo_lugar = resultado.get("addresstype")

            if tipo_lugar == "country":
                direccion = resultado.get("address", {})

                nombre = direccion.get("country")
                codigo_iso = direccion.get("country_code")

                if nombre is not None and codigo_iso is not None:
                    pais = Pais(
                        nombre=nombre,
                        codigo_iso=codigo_iso.upper()
                    )

                    return pais

        raise ValueError("Introduce un país válido.")

    def buscar_ciudades_principales(self, nombre_pais, cantidad=3):
        pais = self.buscar_pais(nombre_pais)

        ciudades = self.geo_cache.get_cities()
        ciudades_del_pais = []

        for ciudad in ciudades.values():
            if ciudad["countrycode"] == pais.codigo_iso:
                ciudades_del_pais.append(ciudad)

        if not ciudades_del_pais:
            raise ValueError("No se encontraron ciudades principales para ese país.")

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