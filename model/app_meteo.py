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

        self.paises_especiales = {
            "AD": {"nombre": "Principado de Andorra", "radio": 0.15}, 
            "BB": {"nombre": "Barbados", "radio": 0.25}, 
            "BH": {"nombre": "Bahréin", "radio": 0.25}, 
            "VA": {"nombre": "Ciudad del Vaticano", "radio": 0.05}, 
            "GD": {"nombre": "Grenada", "radio": 0.25}, 
            "LI": {"nombre": "Liechtenstein", "radio": 0.25}, 
            "MV": {"nombre": "Maldivas", "radio": 0.25}, 
            "MT": {"nombre": "Malta", "radio": 0.25},
            "MC": {"nombre": "Mónaco", "radio": 0.25}, 
            "NR": {"nombre": "Nauru", "radio": 0.25}, 
            "PW": {"nombre": "Palaos", "radio": 0.25}, 
            "KN": {"nombre": "San Cristóbal y Nieves", "radio": 0.25}, 
            "SM": {"nombre": "San Marino", "radio": 0.25}, 
            "SC": {"nombre": "Seychelles", "radio": 0.25},
            "SG": {"nombre": "Singapur", "radio": 0.25}, 
            "TV": {"nombre": "Tuvalu", "radio": 0.25},

            "CV": {"nombre": "Cabo Verde", "radio": 1.0}, 
            "WS": {"nombre": "Samoa", "radio": 1.0}, 
            "ST": {"nombre": "Santo Tomé y Príncipe", "radio": 1.0},

            "KR": {"nombre": "Corea del Sur", "radio": 2.5}, 
            "CR": {"nombre": "Costa Rica", "radio": 2.5}, 
            "EC": {"nombre": "Ecuador", "radio": 2.5}, 
            "SV": {"nombre": "El Salvador", "radio": 2.5}, 
            "GR": {"nombre": "Grecia", "radio": 2.5}, 
            "NZ": {"nombre": "Nueva Zelanda", "radio": 2.5}, 
            "PA": {"nombre": "Panamà", "radio": 2.5}, 
            "PT": {"nombre": "Portugal", "radio": 2.5}, 
            "UY": {"nombre": "Uruguay", "radio": 2.5}
            }
        
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
    
    def cargar_fronteras_a_pais(self, nombre_pais):
        pais_con_fronteras = self.buscador_paises.cargar_fronteras_pais(nombre_pais)
        return pais_con_fronteras
    
    def generar_malla_clima_actual_pais(self, nombre_pais, radio=8.0, malla=5): 
        pais_con_fronteras = self.cargar_fronteras_a_pais(nombre_pais)
        str_nombre_pais = pais_con_fronteras.nombre
        lon_min, lat_min, lon_max, lat_max = pais_con_fronteras.fronteras
        lon_centro = (lon_min + lon_max)/2 
        lat_centro = (lat_min + lat_max)/2 

        lats_lines = np.linspace(lat_centro - radio, lat_centro + radio, malla)
        lons_lines = np.linspace(lon_centro - radio, lon_centro + radio, malla)
    
        lista_lats = np.repeat(lats_lines, len(lons_lines)).tolist()
        lista_lons = np.tile(lons_lines, len(lats_lines)).tolist()

        malla_pais_loc = Localidad(
            nombre=str_nombre_pais,
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
        pais_con_fronteras = self.cargar_fronteras_a_pais(nombre_pais)
        nombre = pais_con_fronteras.nombre
        codigo = pais_con_fronteras.codigo_iso 
        fronteras = pais_con_fronteras.fronteras
        geometria = pais_con_fronteras.geometria

        if codigo in self.paises_especiales.keys():
            pais_localidad = self.generar_malla_clima_actual_pais(nombre_pais, radio=self.paises_especiales[codigo]["radio"], malla=5)
        else:
            pais_localidad = self.generar_malla_clima_actual_pais(nombre_pais)
        
        lons = pais_localidad.lon
        lats = pais_localidad.lat
        lons_array = np.array(lons)
        lats_array = np.array(lats)
        coords = np.column_stack((lons_array, lats_array))

        # Variables Clímaticas ######################################
        temps = pais_localidad.parametros.temperatura

        # Límites ###################################################
        if fronteras is not None:
            lon_min, lat_min, lon_max, lat_max = fronteras
        else:
            lon_min, lon_max = lons_array.min(), lons_array.max()
            lat_min, lat_max = lats_array.min(), lats_array.max()

        # Añadir margenes ###########################################
        margen_lon = 0
        margen_lat = 0

        lon_min = lon_min - margen_lon
        lon_max = lon_max + margen_lon
        lat_min = lat_min - margen_lat
        lat_max = lat_max + margen_lat
        
        # Cálculo del centro y extensión del mapa ###################
        lon_centro = (lon_min + lon_max) / 2
        lat_centro = (lat_min + lat_max) / 2
        lon_exten = lon_max - lon_min
        lat_exten = lat_max - lat_min

        # Malla Interpoladora #######################################
        grid_x, grid_y = np.mgrid[lon_min:lon_max:600j,
                                  lat_min:lat_max:600j]
        grid_z = griddata(coords, temps, (grid_x, grid_y), method='cubic')

        if np.any(np.isnan(grid_z)):
            grid_z_nearest = griddata(coords, temps, (grid_x, grid_y), method='nearest')
            grid_z = np.where(np.isnan(grid_z), grid_z_nearest, grid_z)
        
        return(lons_array, lats_array,
               lon_min, lon_max,
               lat_min, lat_max,
               lon_centro, lat_centro,
               lon_exten, lat_exten,
               grid_x, grid_y, grid_z,
               nombre, geometria)

