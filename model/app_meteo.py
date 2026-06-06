from .sistema_localizacion import SistemaLocalizacion
from .sistema_pais import SistemaPais
from .solicitud_openmeteo import SolicitudOpenMeteo
from .localidad import Localidad
import numpy as np 
from scipy.interpolate import griddata

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
        elif isinstance(loc, tuple):
            localidad = self.buscador.buscador_nombre_coordenads(loc)
        
        self.servicio_clima = SolicitudOpenMeteo(localidad)
        parametros = self.servicio_clima.obtener_clima_actual()
        localidad.parametros = parametros
        return localidad

    def buscar_nombre_pais(self, texto):
        return self.buscador_paises.buscador_nombre_pais(texto)

    def consultar_clima_actual_pais(self, nombre_pais, cantidad):
        pais = self.buscador_paises.buscar_ciudades_principales(nombre_pais, cantidad)

        for localidad in pais.localidades:
            self.servicio_clima = SolicitudOpenMeteo(localidad)
            parametros = self.servicio_clima.obtener_clima_actual()
            localidad.parametros = parametros
        return pais
    
    # Métodos exclusivos de MapaVariables ------------------------------------------
    def cargar_fronteras_a_pais(self, nombre_pais):
        """Método empleado para asignar los límites y la geometría del país a una instancia de la clase Pais"""
        pais_con_fronteras = self.buscador_paises.cargar_fronteras_pais(nombre_pais)
        return pais_con_fronteras
    
    def generar_malla_clima_actual_pais(self, nombre_pais, malla=5): 
        """Método para generar una malla nxn con datos clímaticos que se guarda en una instancia de Localidad"""
        pais_con_fronteras = self.cargar_fronteras_a_pais(nombre_pais)
        nombre = pais_con_fronteras.nombre
        lon_min, lat_min, lon_max, lat_max = pais_con_fronteras.fronteras
        margen_lat = (lat_max - lat_min) * 0.06
        margen_lon = (lon_max - lon_min) * 0.06

        lats_lines = np.linspace(lat_min - margen_lat , lat_max + margen_lat, malla)
        lons_lines = np.linspace(lon_min - margen_lon, lon_max + margen_lon, malla)

        lista_lats = np.repeat(lats_lines, len(lons_lines)).tolist()
        lista_lons = np.tile(lons_lines, len(lats_lines)).tolist()

        malla_pais_loc = Localidad(
            nombre=nombre,
            lat=lista_lats,
            lon=lista_lons,
            forzar_set=True
        )

        self.servicio_clima = SolicitudOpenMeteo(malla_pais_loc)
        parametros = self.servicio_clima.obtener_clima_actual()

        malla_temp = np.array(parametros.temperatura)
        parametros.temperatura = malla_temp
        malla_pais_loc.parametros = parametros
     
        return malla_pais_loc
    
    def generar_datos_mapa_var(self, nombre_pais):
        """Método que proporciona los datos necesarios para graficar mapas de elementos continuos"""

        pais_con_fronteras = self.cargar_fronteras_a_pais(nombre_pais)
        nombre = pais_con_fronteras.nombre 
        fronteras = pais_con_fronteras.fronteras
        geometria = pais_con_fronteras.geometria
        
        pais_localidad = self.generar_malla_clima_actual_pais(nombre_pais)
        lons = pais_localidad.lon
        lats = pais_localidad.lat
        lons_array = np.array(lons)
        lats_array = np.array(lats)
        coords = np.column_stack((lons_array, lats_array))

        # Variables Clímaticas ######################################
        temps = pais_localidad.parametros.temperatura

        # Límites ###################################################
        lon_min, lat_min, lon_max, lat_max = fronteras

        # Cálculo del centro y extensión del mapa ###################
        lon_exten = lon_max - lon_min
        lat_exten = lat_max - lat_min

        # Añadir margenes ###########################################
        margen_lon = lon_exten * 0.06
        margen_lat = lat_exten * 0.06

        lon_min = lon_min - margen_lon
        lon_max = lon_max + margen_lon
        lat_min = lat_min - margen_lat
        lat_max = lat_max + margen_lat

        # Malla Interpoladora #######################################
        grid_x, grid_y = np.mgrid[lon_min:lon_max:800j,
                                  lat_min:lat_max:800j]
        grid_z = griddata(coords, temps, (grid_x, grid_y), method='cubic')

        if np.any(np.isnan(grid_z)):
            grid_z_nearest = griddata(coords, temps, (grid_x, grid_y), method='nearest')
            grid_z = np.where(np.isnan(grid_z), grid_z_nearest, grid_z)
        
        return(lons_array, lats_array,
               lon_min, lon_max,
               lat_min, lat_max,
               grid_x, grid_y, grid_z,
               nombre, geometria)

