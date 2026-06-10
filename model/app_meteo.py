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
        """Método que devuelve una lista con los nombres de las ciudades 
        que presentan cierta similitud con el texto introducido"""
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
    
    def generar_malla_clima_actual_pais(self, nombre_pais, malla=None): 
        """Método para generar una malla nxn con datos clímaticos que se guarda en una instancia de Localidad"""
        pais_con_fronteras = self.cargar_fronteras_a_pais(nombre_pais)
        nombre = pais_con_fronteras.nombre
        lon_min, lat_min, lon_max, lat_max = pais_con_fronteras.fronteras
        lat_exten = lat_max - lat_min
        lon_exten = lon_max - lon_min
        margen_lat = (lat_exten) * 0.04
        margen_lon = (lon_exten) * 0.04
        
        if lat_exten < 2.0 and lon_exten < 2.0:
            malla = 5
        else:
            malla = 7

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

        malla_hum = np.array(parametros.humedad)
        parametros.humedad = malla_hum

        malla_dir_viento = np.array(parametros.direccion_viento)
        parametros.direccion_viento = malla_dir_viento

        malla_raf_viento = np.array(parametros.rafaga_viento)
        parametros.rafaga_viento = malla_raf_viento


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
        temperaturas = pais_localidad.parametros.temperatura
        humedades = pais_localidad.parametros.humedad

        raf_vientos = pais_localidad.parametros.rafaga_viento
        rad = np.deg2rad(pais_localidad.parametros.direccion_viento)
        u = -3 * np.sin(rad)
        v = -3 * np.cos(rad)

        # Límites ###################################################
        lon_min, lat_min, lon_max, lat_max = fronteras

        # Cálculo la extensión del mapa #############################
        lon_exten = lon_max - lon_min
        lat_exten = lat_max - lat_min

        # Añadir margenes ###########################################
        margen_lon = lon_exten * 0.04
        margen_lat = lat_exten * 0.04

        lon_min = lon_min - margen_lon
        lon_max = lon_max + margen_lon
        lat_min = lat_min - margen_lat
        lat_max = lat_max + margen_lat

        # Malla Interpoladora #######################################
        grid_x, grid_y = np.mgrid[lon_min:lon_max:800j,
                                  lat_min:lat_max:800j]
        grid_z_temp = griddata(coords, temperaturas, (grid_x, grid_y), method='cubic')
        grid_z_hum = griddata(coords, humedades, (grid_x, grid_y), method='cubic')
        grid_z_raf_viento = griddata(coords, raf_vientos, (grid_x, grid_y), method='cubic')


        return(lons_array, lats_array,
               lon_min, lon_max,
               lat_min, lat_max,
               grid_x, grid_y, 
               grid_z_temp, grid_z_hum, 
               grid_z_raf_viento, u, v, 
               nombre, geometria)

