import geonamescache
import unicodedata
from shapely import simplify
from shapely.geometry import MultiPolygon
import cartopy.io.shapereader as shpreader

from .pais import Pais
from .localidad import Localidad


class SistemaPais:
    """Clase encargada de buscar países y sus ciudades principales."""

    def __init__(self):
        self.geo_cache = geonamescache.GeonamesCache()
        self._paises_encontrados = {}
        self.cache_geometria_fronteras = {}
        self.base_datos_10m = self._cargar_db_paises("10m")
        self.base_datos_110m = self._cargar_db_paises("110m")
        
    
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
        shp_archivo = shpreader.natural_earth(resolution=resolucion,
                                              category='cultural',
                                              name='admin_0_countries')
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
        self.paises_pequenos = ["AD", "BB", "BH", "VA", "GD", "LI", "MV", 
                                "MT", "MC", "NR", "PW", "KN", "SM", "SC", 
                                "SG", "TV"]
        
        pais = self.seleccionar_pais(nombre_pais)
        codigo_pais = pais.codigo_iso

        if codigo_pais in self.cache_geometria_fronteras:
            geometria = self.cache_geometria_fronteras[codigo_pais]
            pais.geometria = geometria
            pais.fronteras = geometria.bounds
            return pais
            
        if codigo_pais in self.paises_pequenos:
            db = self.base_datos_10m
        else:
            db = self.base_datos_110m
        
        geometria_frontera = None
        for ne_pais in db:
            if ne_pais.attributes.get('ISO_A2_EH') == codigo_pais:
                geometria_completa = ne_pais.geometry
                if isinstance(geometria_completa, MultiPolygon):
                    geometria_frontera = max(geometria_completa.geoms, key=lambda p: p.area)
                else: 
                    geometria_frontera = geometria_completa
                break

        if geometria_frontera is not None:
            if codigo_pais in self.paises_pequenos:
                geometria_suavizada = simplify(geometria_frontera, tolerance=0.00004, preserve_topology=True)
            else:
                geometria_suavizada = simplify(geometria_frontera, tolerance=0.0001, preserve_topology=True)
            
            self.cache_geometria_fronteras[codigo_pais] = geometria_suavizada
            pais.geometria = geometria_suavizada
            pais.fronteras = geometria_suavizada.bounds
        else:
            raise ValueError("Error al generar la geometria del país")

        return pais 
            