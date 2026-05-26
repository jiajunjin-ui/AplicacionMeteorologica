from .sistema_localizacion import SistemaLocalizacion
from .sistema_pais import SistemaPais
from .solicitud_openmeteo import SolicitudOpenMeteo
from .localidad import Localidad
import numpy as np 

class AppMeteo:
    def __init__(self):
        self.buscador = SistemaLocalizacion()
        self.buscador_paises = SistemaPais()
        self.servicio_clima = None
    
    def buscar_nombre_ciudad(self, text):
        return self.buscador.buscador_nombre_ciudad(text)

    def consultar_pronostico_localidad(self, loc):
        if isinstance(loc, str):
            localidad = self.buscador.seleccionar_ciudad(loc)
        elif isinstance(loc, tuple):
            localidad = self.buscador.buscador_nombre_coordenads(loc)
        
        self.servicio_clima = SolicitudOpenMeteo(localidad)
        parametros = self.servicio_clima.obtener_pronostico_horario()
        localidad.parametros = parametros
        return localidad
    
    def consultar_clima_actual_localidad(self, loc):
        if isinstance(loc, str):
            localidad = self.buscador.seleccionar_ciudad(loc)
        if isinstance(loc, tuple):
            localidad = self.buscador.buscador_nombre_coordenads(loc)
        
        self.servicio_clima = SolicitudOpenMeteo(localidad)
        parametros = self.servicio_clima.obtener_clima_actual()
        localidad.parametros = parametros
        return localidad

    def buscar_nombre_pais(self, texto):
        return self.buscador_paises.buscador_nombre_pais(texto)

    def consultar_clima_actual_pais(self, nombre_pais, cantidad=3):
        pais = self.buscador_paises.buscar_ciudades_principales(nombre_pais, cantidad)

        for localidad in pais.localidades:
            self.servicio_clima = SolicitudOpenMeteo(localidad)
            parametros = self.servicio_clima.obtener_clima_actual()
            localidad.parametros = parametros

        return pais
    
    def malla_clima_actual_pais(self, nombre_pais, radio=7, malla=5):
        pais_localidad = self.buscador_paises.buscar_ciudades_principales(nombre_pais, 1)
        ciudad_central = pais_localidad.localidades[0]
        lat_centro = ciudad_central.lat
        lon_centro = ciudad_central.lon

        lats_lines = np.linspace(lat_centro - radio, lat_centro + radio, malla)
        lons_lines = np.linspace(lon_centro - radio, lon_centro + radio, malla)
    
        lista_lats = np.repeat(lats_lines, len(lons_lines)).tolist()
        lista_lons = np.tile(lons_lines, len(lats_lines)).tolist()

        malla_pais_loc = Localidad(
            nombre=f'Malla_{nombre_pais}',
            lat=lista_lats,
            lon=lista_lons,
            forzar_set=True
        )

        self.servicio_clima = SolicitudOpenMeteo(malla_pais_loc)
        parametros = self.servicio_clima.obtener_clima_actual()

        malla_temp = np.array(parametros.temperatura)
        parametros.temperatura = malla_temp
        malla_pais_loc.parametros = parametros

        malla_pais_loc.lat = lista_lats
        malla_pais_loc.lon = lista_lons
     
        return malla_pais_loc
