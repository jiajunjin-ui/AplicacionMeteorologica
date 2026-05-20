class PresenterInicio:
    def __init__(self, view, model, mediador_presenter=None):
        # Agregación: recibe instancias externas
        self.vista = view
        self.modelo = model
        self.mediador = mediador_presenter

        self.vista.btnCambiarPantallaGrafico.add_listener(self.f_cambiar_a_pantalla_grafico)
        self.vista.btnCambiarPantallaMapa.add_listener(self.f_cambiar_a_pantalla_mapa)

    def f_cambiar_a_pantalla_grafico(self):
        """Cambia a la pantalla del gráfico"""
        try:
            self.mediador.cambiar_presenter('PresenterGrafico')
            self.mediador.obtener_presenter_actual()
        except Exception as e:
            self.vista.mensaje('Error', str(e))
    
    def f_cambiar_a_pantalla_mapa(self):
        """Cambia a la pantalla del mapa"""
        try:
            self.mediador.cambiar_presenter('PresenterMapa')
            self.mediador.obtener_presenter_actual()
        except Exception as e:
            self.vista.mensaje('Error', str(e))