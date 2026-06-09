class PresenterMapaVariables:
    def __init__(self, view, model, mediador_presenter=None):
        self.vista = view
        self.modelo = model
        self.mediador = mediador_presenter

        # Suscripción a las señales de la vista
        self.vista.btnBuscar.add_listener(self.f_actualizar_lista_paises)
        self.vista.btnSelect_pais.add_listener(self.f_generar_mapa)
        self.vista.btnSelect_var.add_listener(self.f_rellenar_mapa)

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
             grid_x, grid_y, 
             grid_z_temp, grid_z_hum,
             nombre_pais, geometria_pais) = datos
            self.dic_datos = {
                'lons_array': lons_array,
                'lats_array': lats_array,
                'lon_min': lon_min, 'lon_max': lon_max,
                'lat_min': lat_min, 'lat_max': lat_max,
                'grid_x': grid_x, 'grid_y': grid_y, 
                'grid_z_temp': grid_z_temp, 'grid_z_hum': grid_z_hum,
                'nombre_pais': nombre_pais, 'geometria_pais': geometria_pais
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

            lista_variables = ['Temperatura', 'Humedad Relativa']

            if geometria_pais is None:
                self.vista.mensaje_info('Error al cargar fronteras',
                                        f'Las fronteras de {nombre_pais} no se encuentran en la base de datos de Natural Earth')
                return 
            self.vista.generar_mapa(lons_array, lats_array,
                                    lon_min, lon_max,
                                    lat_min, lat_max,
                                    nombre_pais, geometria_pais,
                                    lista_variables
                                    )
        except Exception as e:
            self.vista.mensaje('Error', str(e))
    
    def f_rellenar_mapa(self, var_select):
        try:
            grid_x = self.dic_datos['grid_x']
            grid_y = self.dic_datos['grid_y']

            grid_z_temp = self.dic_datos['grid_z_temp']
            grid_z_hum = self.dic_datos['grid_z_hum']
            if var_select == 'Temperatura':
                grid_z = grid_z_temp
                colores = 'RdYlBu_r'
                unidades = '%.1f°C'
                line_level = 10
                text_label = 'Temperatura(ºC)'
            elif var_select == 'Humedad Relativa':
                grid_z = grid_z_hum
                colores = 'YlGnBu_r'
                unidades = '%.1f%%'
                line_level = 15
                text_label = 'Humedad Relativa(%)'

            self.vista.rellenar_mapa(grid_x, grid_y, grid_z, 
                                     colores, unidades, text_label, 
                                     line_level)
            
        except Exception as e:
            self.vista.mensaje('Error', str(e))
    
        

    
    
