class PresenterGrafico:
    def __init__(self, view, model, mediador_presenter=None):
        self.vista = view
        self.modelo = model
        self.mediador = mediador_presenter

        # Limpiar listeners suscritos previamente 
        self.vista.btnBuscar.clear_listeners()
        self.vista.btnSelect.clear_listeners()
        self.vista.check_selec.clear_listeners()
        self.vista.btnCambiarPantallaInicio.clear_listeners()
        self.vista.btnCambiarPantallaRanking.clear_listeners()

        # Suscripción a las señales de la vista
        self.vista.btnBuscar.add_listener(self.f_actualizar_lista_ciudades)
        self.vista.btnSelect.add_listener(self.f_alamacenar_datos)
        self.vista.check_selec.add_listener(self.f_cambiar_seleccion_de_vars)
        self.vista.btnCambiarPantallaInicio.add_listener(self.f_cambiar_a_pantalla_inicio)
        self.vista.btnCambiarPantallaRanking.add_listener(self.f_cambiar_a_pantalla_ranking)

    def f_actualizar_lista_ciudades(self):
        try:
            text_in = self.vista.entrada()
            lista_ciudades = self.modelo.buscar_nombre_ciudad(text_in)
            self.vista.mostrar_lista_ciudades(lista_ciudades)
        except Exception as e:
            self.vista.mensaje('Error', str(e))
    
    def f_alamacenar_datos(self, nombre_ciudad):
        """Almacena los valores de las variables climáticas de la ciudad"""
        try:
            ciudad_select = nombre_ciudad
            ciudad_con_param = self.modelo.consultar_pronostico_localidad(ciudad_select)
            datos_porhora = ciudad_con_param.parametros

            self.date = datos_porhora.date
            self.datos_variables = {
                "Temperatura": datos_porhora.temperatura,
                "Humedad Rel.": datos_porhora.humedad,
                "Viento": datos_porhora.viento,
                "Prob. Precipitación": datos_porhora.prob_precip
            }

            self.vista.mostrar_elementos_graficos()

            self.f_cambiar_seleccion_de_vars()
        except Exception as e:
            self.vista.mensaje('Error', str(e))
    
    def f_cambiar_seleccion_de_vars(self):
        """Decide que variables graficar según los checkbuttons del view"""
        var_activas = self.vista.obtner_var_selec()
        datos_filtardos = {}
        for var in var_activas:
            if var in self.datos_variables:
                datos_filtardos[var] = self.datos_variables[var]
        
        self.vista.actualizar_grafico(self.date, datos_filtardos)

    def f_cambiar_a_pantalla_inicio(self):
        """Cambia a la pantalla de Inicio"""
        try:
            self.vista.limpiar_grafico_cambio_pantalla()
            self.mediador.cambiar_presenter('PresenterInicio')
            self.mediador.obtener_presenter_actual()
        except Exception as e:
            self.vista.mensaje('Error', str(e))
    
    def f_cambiar_a_pantalla_ranking(self):
        """Cambia a la pantalla de Ranking"""
        try:
            self.vista.limpiar_grafico_cambio_pantalla()
            self.mediador.cambiar_presenter('PresenterRanking')
            self.mediador.obtener_presenter_actual()
        except Exception as e:
            self.vista.mensaje('Error', str(e))
