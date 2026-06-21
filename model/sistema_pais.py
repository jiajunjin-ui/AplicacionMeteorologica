import requests
import geonamescache
import unicodedata
from shapely import simplify
from shapely.geometry import MultiPolygon
import cartopy.io.shapereader as shpreader
import cartopy.crs as ccrs

from .pais import Pais
from .localidad import Localidad


class SistemaPais:
    """Clase encargada de buscar países a partir de un str y 
    puede devolver una lista de sus ciudades principales, información sobre su geometria y sus límites en coordenadas."""

    def __init__(self):
        self.url_buscar_pais = "https://nominatim.openstreetmap.org/search"
        self.geo_cache = geonamescache.GeonamesCache()
        self._paises_encontrados = {}
        self.cache_geometria_fronteras = {}
        self.base_datos_10m = self._cargar_db_paises("10m")
        self.base_datos_110m = self._cargar_db_paises("110m")
        self.paises_pequenos = self._generar_list_paises_pequeños()

    # Métodos principales --------------------------------------
    def normalizar_texto(self, texto):
        texto = texto.strip().lower()
        texto = unicodedata.normalize("NFD", texto)
        texto = "".join(
            caracter for caracter in texto
            if unicodedata.category(caracter) != "Mn"
        )
        return texto

    def _cargar_db_paises(self, resolucion):
        """Carga la base de datos de Natural Earth y la transforma en una lista, para poder reiterar el uso de esta"""
        shp_archivo = shpreader.natural_earth(resolution=resolucion,
                                              category='cultural',
                                              name='admin_0_map_units')
        lector = shpreader.Reader(shp_archivo)

        return list(lector.records())

    def buscador_nombre_pais(self, texto):
        """Busca paises cuyo nombre empieza por el texto introducido."""

        texto = texto.strip()

        if len(texto) < 3:
            raise ValueError("Se deben introducir al menos 3 letras del pais.")

        texto_normalizado = self.normalizar_texto(texto)
        self._paises_encontrados = {}

        for ne_pais in self.base_datos_10m:
            nombre = ne_pais.attributes.get('NAME_ES')
            nombre_normalizado = self.normalizar_texto(nombre)
            if texto_normalizado in nombre_normalizado:
                codigo_iso = ne_pais.attributes.get('ISO_A2_EH')
                self._paises_encontrados[nombre] = Pais(
                    nombre=nombre,
                    codigo_iso=codigo_iso
                )

        if not self._paises_encontrados:
            raise ValueError("No se encontro ningun pais.")

        return sorted(self._paises_encontrados.keys())

    def seleccionar_pais(self, nombre_pais):
        """Devuelve el pais seleccionado de la lista generada."""
        if nombre_pais not in self._paises_encontrados:
            raise KeyError("Seleccione un pais de la lista generada.")
        return self._paises_encontrados[nombre_pais]

    def _generar_list_paises_pequeños(self):
        """Genera una lista de codigos_iso de los países/regiónes 
        que no son visbles en mapas de baja resolución 110m """
        list_cod_vis_baja_resolucion = []
        list_cod_vis_alta_resolucion = []
        for ne_region in self.base_datos_10m:
            codigo_iso = ne_region.attributes.get('ISO_A2_EH')
            if codigo_iso and codigo_iso not in ['-99', ' ']:
                min_zoom = ne_region.attributes.get('min_zoom', 0.0)
                scalerank = ne_region.attributes.get('scalerank', 0)
                if min_zoom < 6.0 and scalerank < 6:
                    list_cod_vis_baja_resolucion.append(codigo_iso)
                else:
                    list_cod_vis_alta_resolucion.append(codigo_iso)
        return sorted(list(set(list_cod_vis_baja_resolucion) - set(list_cod_vis_alta_resolucion)))
    

    # Métodos especializados -----------------------------------
    # Mapa de elementos discretos
    def buscar_ciudades_principales(self, nombre_pais, cantidad):
        pais = self.seleccionar_pais(nombre_pais)
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

    # Mapa de elementos continuos
    def cargar_fronteras_pais(self, nombre_pais):
        """Método que asigna los límites y la geometría del país a una instancia de la clase Pais"""
        pais = self.seleccionar_pais(nombre_pais)
        codigo_pais = pais.codigo_iso

        if codigo_pais in self.cache_geometria_fronteras:
            geometria, bordes = self.cache_geometria_fronteras[codigo_pais]
            pais.geometria = geometria
            pais.fronteras = bordes
            return pais

        if codigo_pais in self.paises_pequenos:
            db = self.base_datos_10m
        else:
            db = self.base_datos_110m

        geometria_pais = None
        for ne_pais in db:
            if ne_pais.attributes.get('ISO_A2_EH') == codigo_pais:
                geometria_completa = ne_pais.geometry
                if isinstance(geometria_completa, MultiPolygon):
                    geometria_pais = max(geometria_completa.geoms, key=lambda p: p.area)
                else:
                    geometria_pais = geometria_completa
                break

        if geometria_pais is not None:
            crs_original = ccrs.PlateCarree()
            crs_tranform = ccrs.epsg(3857)
            geom_pais_transform = crs_tranform.project_geometry(geometria_pais, crs_original)

            tolerancia = geom_pais_transform.length * 0.001
            geometria_suavizada = simplify(geom_pais_transform, tolerance=tolerancia, preserve_topology=True)


            self.cache_geometria_fronteras[codigo_pais] = (geometria_suavizada, geometria_pais.bounds)
            pais.geometria = geometria_suavizada
            pais.fronteras = geometria_pais.bounds
        else:
            raise ValueError("Error al generar la geometria del país")

        return pais

if __name__ == '__main__':
    sistema_pais = SistemaPais()
    print(sistema_pais.normalizar_texto('6Uuuu9OI/'))
    lista_paises = sistema_pais.buscador_nombre_pais('Ale')
    print(lista_paises)
    print(sistema_pais.buscar_ciudades_principales(lista_paises[0], 5).localidades)
    print(sistema_pais.cargar_fronteras_pais(lista_paises[0]).fronteras)

