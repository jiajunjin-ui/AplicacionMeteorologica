import matplotlib.pyplot as plt 
import matplotlib.colors as mcolors
import numpy as np

class PresenterMapaVariables:
    def __init__(self, view, model, mediador_presenter=None):
        self.vista = view
        self.modelo = model
        self.mediador = mediador_presenter

        # Limpiar listeners suscritos previamente 
        self.vista.btnBuscar.clear_listeners()
        self.vista.btnSelect_pais.clear_listeners()
        self.vista.btnSelect_var.clear_listeners()
        self.vista.btnCambiarPantallaInicio.clear_listeners()

        # Suscripción a las señales de la vista
        self.vista.btnBuscar.add_listener(self.f_actualizar_lista_paises)
        self.vista.btnSelect_pais.add_listener(self.f_generar_mapa)
        self.vista.btnSelect_var.add_listener(self.f_rellenar_mapa)
        self.vista.btnCambiarPantallaInicio.add_listener(self.f_cambiar_a_pantalla_inicio)

        self.dic_datos = {}

    def f_actualizar_lista_paises(self):
        try:
            text_in = self.vista.entrada()
            list_posibles_paises = self.modelo.buscar_nombre_pais(text_in)
            self.vista.mostrar_lista_paises(list_posibles_paises)
        except Exception as e:
            self.vista.mensaje('Error', str(e))
    
    def obtener_datos(self, nombre_pais_select):
        try:
            datos = self.modelo.generar_datos_mapa_var(nombre_pais_select)
            (lons_array, lats_array,
             lon_min, lon_max,
             lat_min, lat_max,
             grid_x_c, grid_y_c, 
             grid_x_d, grid_y_d,
             grid_z_temp, grid_z_hum, 
             grid_z_raf_viento,
             grid_z_velx_viento, grid_z_vely_viento,
             nombre_pais, geometria_pais, 
             resolucion) = datos
            self.dic_datos = {
                'lons_array': lons_array,
                'lats_array': lats_array,
                'lon_min': lon_min, 'lon_max': lon_max,
                'lat_min': lat_min, 'lat_max': lat_max,
                'grid_x_c': grid_x_c, 'grid_y_c': grid_y_c,
                'grid_x_d': grid_x_d, 'grid_y_d': grid_y_d, 
                'grid_z_temp': grid_z_temp, 'grid_z_hum': grid_z_hum, 
                'grid_z_raf_viento': grid_z_raf_viento, 
                'grid_z_velx_viento': grid_z_velx_viento, 'grid_z_vely_viento': grid_z_vely_viento,
                'nombre_pais': nombre_pais, 'geometria_pais': geometria_pais, 
                'resolucion': resolucion
            }
        except Exception as e:
            self.vista.mensaje('Error', str(e))
        
        
    def f_generar_mapa(self, nombre_pais_select):
        try:
            self.obtener_datos(nombre_pais_select)

            lons_array = self.dic_datos['lons_array']
            lats_array = self.dic_datos['lats_array']
            
            lon_min = self.dic_datos['lon_min']
            lon_max = self.dic_datos['lon_max']

            lat_min = self.dic_datos['lat_min']
            lat_max = self.dic_datos['lat_max']
            
            geometria_pais = self.dic_datos['geometria_pais']
            nombre_pais = self.dic_datos['nombre_pais']

            resolucion = self.dic_datos['resolucion']

            if geometria_pais is None:
                self.vista.mensaje_info('Error al cargar fronteras',
                                        f'Las fronteras de {nombre_pais} no se encuentran en la base de datos de Natural Earth')
                return 

            self.vista.generar_mapa(lons_array, lats_array,
                                    lon_min, lon_max,
                                    lat_min, lat_max,
                                    nombre_pais, geometria_pais,
                                    resolucion
                                    )
        except Exception as e:
            self.vista.mensaje('Error', str(e))
    
    def f_rellenar_mapa(self, var_select):
        try:
            grid_x_c = self.dic_datos['grid_x_c']
            grid_y_c = self.dic_datos['grid_y_c']

            grid_x_d = self.dic_datos['grid_x_d']
            grid_y_d = self.dic_datos['grid_y_d']

            grid_z_temp = self.dic_datos['grid_z_temp']
            grid_z_hum = self.dic_datos['grid_z_hum']
            grid_z_viento = self.dic_datos['grid_z_raf_viento']
            grid_z_velx_viento, grid_z_vely_viento = None, None 
 
            if var_select == 'Temperatura':
                grid_z = grid_z_temp
                colores = 'RdYlBu_r'
                unidades = '%.1f°C'
                min_z = np.min(grid_z)
                max_z = np.max(grid_z)
                cp_levels = np.linspace(min_z, max_z, 15)
                hay_lineas = True
                line_levels = np.linspace(min_z, max_z, 10)
                text_label = 'Temperatura(ºC)'

            elif var_select == 'Humedad Relativa':
                grid_z = grid_z_hum
                colores = 'YlGnBu'
                unidades = '%.1f%%'
                min_z = np.min(grid_z)
                max_z = np.max(grid_z)
                if np.isclose(min_z, max_z):
                    min_z -= 0.1
                    max_z += 0.1
                    div_cp = 2
                    div_lineas = 2
                else:
                    div_cp = 16  
                    div_lineas = 16 
                cp_levels = np.linspace(min_z, max_z, div_cp)
                hay_lineas = True      
                line_levels = np.linspace(min_z, max_z, div_lineas)
                text_label = 'Humedad Relativa(%)'

            elif var_select == 'Vientos':
                colores_rgb = plt.colormaps['turbo'](np.linspace(0, 1, 256))
                colores_hsv = mcolors.rgb_to_hsv(colores_rgb[:, :3])
                colores_hsv[:, 2] = colores_hsv[:, 2] * 0.7
                color_viento = mcolors.ListedColormap(mcolors.hsv_to_rgb(colores_hsv))

                grid_z = grid_z_viento
                colores = color_viento
                unidades = '%.1fkm/h'
                min_z = np.min(grid_z)
                max_z = np.max(grid_z)
                if np.isclose(min_z, max_z):
                    min_z -= 0.1
                    max_z += 0.1  
                    div_cp = 2 
                else:
                    div_cp = 16    
                cp_levels = np.linspace(min_z, max_z, div_cp)
                hay_lineas = False
                line_levels = 1
                text_label = 'Rachas Viento(km/h)' 
                grid_z_velx_viento = self.dic_datos['grid_z_velx_viento']
                grid_z_vely_viento = self.dic_datos['grid_z_vely_viento']

            self.vista.rellenar_mapa(grid_x_c, grid_y_c, grid_z, 
                                     colores, unidades, text_label,
                                     cp_levels, 
                                     hay_lineas, line_levels,
                                     grid_z_velx_viento, grid_z_vely_viento, 
                                     grid_x_d, grid_y_d)
            
        except Exception as e:
            self.vista.mensaje('Error', str(e))
    
    def f_cambiar_a_pantalla_inicio(self):
        """Cambia a la pantalla de inicio"""
        try:
            self.vista.limpiar_mapa_cambio_pantalla()
            self.vista.limpiar_lista_var()
            self.mediador.cambiar_presenter('PresenterInicio')
            self.mediador.obtener_presenter_actual()
        except Exception as e:
            self.vista.mensaje('Error', str(e))
        

    
    
