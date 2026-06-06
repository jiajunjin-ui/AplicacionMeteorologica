class PresenterMapaVariables:
    def __init__(self, view, model, mediador_presenter=None):
        self.vista = view
        self.modelo = model
        self.mediador = mediador_presenter

        # Suscripción a las señales de la vista
        self.vista.btnBuscar.add_listener(self.f_actualizar_lista_paises)
        self.vista.btnSelect.add_listener(self.f_actualizar_mapa)

    def f_actualizar_lista_paises(self):
        try:
            text_in = self.vista.entrada()
            list_posibles_paises = self.modelo.buscar_nombre_pais(text_in)
            self.vista.mostrar_lista_paises(list_posibles_paises)
        except Exception as e:
            self.vista.mensaje('Error', str(e))


    def f_actualizar_mapa(self, nombre_pais_select):
        try:
            datos = self.modelo.generar_datos_mapa_var(nombre_pais_select)
            (lons_array, lats_array,
             lon_min, lon_max,
             lat_min, lat_max,
             grid_x, grid_y, grid_z,
             nombre_pais, geometria_pais) = datos
            
            if geometria_pais is None:
                self.vista.mensaje_info('Error al cargar fronteras',
                                        f'Las fronteras de {nombre_pais} no se encuentran en la base de datos de Natural Earth')
                return 
            self.vista.actualizar_mapa(lons_array, lats_array,
                                       lon_min, lon_max,
                                       lat_min, lat_max, 
                                       grid_x, grid_y, grid_z,
                                       nombre_pais, geometria_pais
                                       )  
        except Exception as e:
            self.vista.mensaje('Error', str(e))
    
