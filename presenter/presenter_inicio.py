class PresenterInicio:
    def __init__(self, view, model, mediador_presenter=None):
        self.vista = view
        self.modelo = model
        self.mediador = mediador_presenter

        # Limpiar listeners suscritos previamente
        self.vista.btnCambiarPantallaGrafico.clear_listeners()
        self.vista.btnCambiarPantallaMapaDis.clear_listeners()
        self.vista.btnCambiarPantallaMapaCont.clear_listeners()

        # Suscripción a las señales de la vista
        self.vista.btnCambiarPantallaGrafico.add_listener(self.f_cambiar_a_pantalla_grafico)
        self.vista.btnCambiarPantallaMapaDis.add_listener(self.f_cambiar_a_pantalla_mapa_dis)
        self.vista.btnCambiarPantallaMapaCont.add_listener(self.f_cambiar_a_pantalla_mapa_cont)

    def f_cambiar_a_pantalla_grafico(self):
        """Cambia a la pantalla del gráfico"""
        try:
            self.mediador.cambiar_presenter('PresenterGrafico')
            self.mediador.obtener_presenter_actual()
        except Exception as e:
            self.vista.mensaje('Error', str(e))

    def f_cambiar_a_pantalla_mapa_dis(self):
        """Cambia a la pantalla del mapa de elementos discretos"""
        try:
            self.mediador.cambiar_presenter('PresenterMapa')
            self.mediador.obtener_presenter_actual()
        except Exception as e:
            self.vista.mensaje('Error', str(e))

    def f_cambiar_a_pantalla_mapa_cont(self):
        """Cambia a la pantalla del mapa de elementos continuos"""
        try:
            self.mediador.cambiar_presenter('PresenterMapaVariables')
            self.mediador.obtener_presenter_actual()
        except Exception as e:
            self.vista.mensaje('Error', str(e))