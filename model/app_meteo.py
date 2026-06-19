from .sistema_localizacion import SistemaLocalizacion
from .sistema_pais import SistemaPais
from .solicitud_openmeteo import SolicitudOpenMeteo
from .localidad import Localidad

import numpy as np
from scipy.interpolate import RegularGridInterpolator
from pyproj import Transformer

class AppMeteo:
    def __init__(self):
        self.buscador = SistemaLocalizacion()
        self.buscador_paises = SistemaPais()
        self.servicio_clima = None
        self.transformador = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)

    def buscar_nombre_ciudad(self, text):
        """Método que devuelve una lista con los nombres de las ciudades
        que presentan cierta similitud con el texto introducido"""
        return self.buscador.buscador_nombre_ciudad(text)

    def consultar_pronostico_localidad(self, loc):
        if isinstance(loc, str):
            localidad = self.buscador.seleccionar_ciudad(loc)
        elif isinstance(loc, tuple):
            localidad = self.buscador.buscador_nombre_coordenadas(loc)
        
        self.servicio_clima = SolicitudOpenMeteo(localidad)
        parametros = self.servicio_clima.obtener_pronostico_horario()
        localidad.parametros = parametros
        return localidad
    
    def consultar_clima_actual_localidad(self, loc):
        if isinstance(loc, str):
            localidad = self.buscador.seleccionar_ciudad(loc)
        if isinstance(loc, tuple):
            localidad = self.buscador.buscador_nombre_coordenadas(loc)
        
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

    def consultar_ranking_pais(self, nombre_pais, cantidad, tipo_ranking):
        """
        Obtiene el pais, cantidad y tipo de ranking seleccionado por el usuario y busca las principales ciudades del pais y
        sus parametros para despues ordenarlo en funcion del tipo_ranking.
        """
        pais = self.consultar_clima_actual_pais(nombre_pais, cantidad)
        ciudades = pais.localidades

        if tipo_ranking == "mas_calurosas":
            return sorted(
                ciudades,
                key=lambda ciudad: ciudad.parametros.temperatura,
                reverse=True
            )
        if tipo_ranking == "mas_frias":
            return sorted(
                ciudades,
                key=lambda ciudad: ciudad.parametros.temperatura
            )
        if tipo_ranking == "mas_viento":
            return sorted(
                ciudades,
                key=lambda ciudad: ciudad.parametros.viento,
                reverse=True
            )
        if tipo_ranking == "mas_humedad":
            return sorted(
                ciudades,
                key=lambda ciudad: ciudad.parametros.humedad,
                reverse=True
            )

        raise ValueError("Tipo de ranking no valido.")


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
        lon_exten = abs(lon_max - lon_min)
        lat_exten = abs(lat_max - lat_min)
        margen_lon = (lon_exten) * 0.04
        margen_lat = (lat_exten) * 0.04

        if lat_min - margen_lat < -90.0 or lat_max + margen_lat > 90.0:
            margen_lat = 0.0
        elif lon_min - margen_lon < -180.0 or lon_max + margen_lon > 180.0:
            margen_lon = 0.0

        if lat_exten < 2.0 and lon_exten < 2.0:
            malla = 5
        else:
            malla = 6

        lats_lines = np.linspace(lat_min - margen_lat , lat_max + margen_lat, malla)
        lons_lines = np.linspace(lon_min - margen_lon, lon_max + margen_lon, malla)

        lista_lons = np.tile(lons_lines, malla)
        lista_lats = np.repeat(lats_lines, malla)

        lista_lons_round = np.round(lista_lons, 6).tolist()
        lista_lats_round = np.round(lista_lats, 6).tolist()


        malla_pais_loc = Localidad(
            nombre=nombre,
            lat=lista_lats_round,
            lon=lista_lons_round,
            forzar_set=True
        )

        self.servicio_clima = SolicitudOpenMeteo(malla_pais_loc)
        parametros = self.servicio_clima.obtener_clima_actual()

        malla_temp = np.array(parametros.temperatura)
        parametros.temperatura = malla_temp.reshape(malla, malla)

        malla_hum = np.array(parametros.humedad)
        parametros.humedad = malla_hum.reshape(malla, malla)

        malla_raf_viento = np.array(parametros.rafaga_viento)
        parametros.rafaga_viento = malla_raf_viento.reshape(malla, malla)

        malla_dir_viento = np.array(parametros.direccion_viento)
        parametros.direccion_viento = malla_dir_viento.reshape(malla, malla)


        malla_pais_loc.parametros = parametros
        return malla_pais_loc


    def generar_datos_mapa_var(self, nombre_pais):
        """Método que proporciona los datos necesarios para graficar mapas de elementos continuos"""
        paises_pequenos = self.buscador_paises.paises_pequenos

        pais_con_fronteras = self.cargar_fronteras_a_pais(nombre_pais)
        nombre = pais_con_fronteras.nombre
        codigo_iso = pais_con_fronteras.codigo_iso
        fronteras = pais_con_fronteras.fronteras
        geometria = pais_con_fronteras.geometria

        pais_localidad = self.generar_malla_clima_actual_pais(nombre_pais)
        lons = pais_localidad.lon
        lats = pais_localidad.lat
        lons_array = np.array(lons)
        lats_array = np.array(lats)

        # Variables Clímaticas ######################################
        temperaturas = pais_localidad.parametros.temperatura
        humedades = pais_localidad.parametros.humedad
        raf_vientos = pais_localidad.parametros.rafaga_viento
        dir_vientos = np.deg2rad(pais_localidad.parametros.direccion_viento)

        # Límites ###################################################
        lon_min, lat_min, lon_max, lat_max = fronteras

        # Cálculo la extensión del mapa #############################
        lon_exten = abs(lon_max - lon_min)
        lat_exten = abs(lat_max - lat_min)

        # Añadir margenes ###########################################
        margen_lon = lon_exten * 0.04
        margen_lat = lat_exten * 0.04

        if lat_min - margen_lat < -90.0 or lat_max + margen_lat > 90.0:
            margen_lat = 0.0
        elif lon_min - margen_lon < -180.0 or lon_max + margen_lon > 180.0:
            margen_lon = 0.0

        lon_min = lon_min - margen_lon
        lon_max = lon_max + margen_lon
        lat_min = lat_min - margen_lat
        lat_max = lat_max + margen_lat

        # Malla Interpoladora #######################################
        lons_array_unico = np.unique(lons_array)
        lats_array_unico = np.unique(lats_array)


        # Elementos continuos
        interp_temp = RegularGridInterpolator((lats_array_unico, lons_array_unico), temperaturas,
                                              bounds_error=False, fill_value=None, method='cubic')
        interp_hum = RegularGridInterpolator((lats_array_unico, lons_array_unico), humedades,
                                              bounds_error=False, fill_value=None, method='cubic')
        interp_raf_viento = RegularGridInterpolator((lats_array_unico, lons_array_unico), raf_vientos,
                                                     bounds_error=False, fill_value=None, method='cubic')

        grid_y_c, grid_x_c = np.mgrid[lat_min:lat_max:600j,
                                      lon_min:lon_max:600j]
        puntos_interp_c = np.dstack((grid_y_c, grid_x_c))

        grid_z_temp = interp_temp(puntos_interp_c)
        grid_z_hum = interp_hum(puntos_interp_c)
        grid_z_raf_viento = interp_raf_viento(puntos_interp_c)
        grid_z_raf_viento = np.clip(grid_z_raf_viento, a_min=0.0, a_max=None)

        # Elementos discretos
        interp_dir_viento = RegularGridInterpolator((lats_array_unico, lons_array_unico), dir_vientos,
                                                     bounds_error=False, fill_value=None, method='cubic')

        grid_y_d, grid_x_d = np.mgrid[lat_min:lat_max:8j,
                                      lon_min:lon_max:8j]
        puntos_interp_d = np.dstack((grid_y_d, grid_x_d))

        grid_z_dir_viento = interp_dir_viento(puntos_interp_d)
        grid_z_velx_viento = 3 * np.sin(grid_z_dir_viento)
        grid_z_vely_viento = 3 * np.cos(grid_z_dir_viento)

        # Transformación de PlaneCarree a Mercator ##################
        lons_array, lats_array = self.transformar_coordenadas(lons_array, lats_array)
        lon_min, lat_min = self.transformar_coordenadas(lon_min, lat_min)
        lon_max, lat_max = self.transformar_coordenadas(lon_max, lat_max)

        grid_x_c, grid_y_c = self.transformar_coordenadas(grid_x_c, grid_y_c)
        grid_x_d, grid_y_d = self.transformar_coordenadas(grid_x_d, grid_y_d)

        # Resolución del mapa #######################################
        if codigo_iso in paises_pequenos:
            resolucion = '10m'
        else:
            resolucion = '110m'

        return(lons_array, lats_array,
               lon_min, lon_max,
               lat_min, lat_max,
               grid_x_c, grid_y_c,
               grid_x_d, grid_y_d,
               grid_z_temp, grid_z_hum,
               grid_z_raf_viento,
               grid_z_velx_viento, grid_z_vely_viento,
               nombre, geometria,
               resolucion)

    def transformar_coordenadas(self, lon, lat):
        lon_transform, lat_transform = self.transformador.transform(lon, lat)
        return lon_transform, lat_transform
