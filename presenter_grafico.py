import pandas as pd

class PresenterGrafico:
    def __init__(self, view, model, mediador_presenter=None):
        self.vista = view
        self.modelo = model
        self.mediador = mediador_presenter

        # Suscripción a las señales de la vista
        self.vista.btnBuscar.add_listener(self.f_actualizar_lista)
        self.vista.btnSelect.add_listener(self.f_actualizar_grafico)
        self.vista.btnCambiarPantallaInicio.add_listener(self.f_cambiar_a_pantalla_inicio)


    def f_actualizar_lista(self):
        try:
            text_in = self.vista.entrada()
            lista_ciudades = self.modelo.buscar_nombre_ciudad(text_in)
            self.vista.salida(lista_ciudades)
        except Exception as e:
            self.vista.mensaje('Error', str(e))
    
    def f_actualizar_grafico(self, nombre_ciudad):
        try:
            ciudad_select = nombre_ciudad
            ciudad_con_param = self.modelo.consultar_pronostico_localidad(ciudad_select)
            datos_porhora = ciudad_con_param.parametros

            date = datos_porhora.date
            temp = datos_porhora.temperatura
            hum_rel = datos_porhora.humedad
            viento = datos_porhora.viento
            prob_precip = datos_porhora.prob_precip
            estado_cielo = datos_porhora.weather_code

            self.vista.crear_grafico(date, temp, hum_rel, viento, prob_precip, estado_cielo)
        except Exception as e:
            self.vista.mensaje('Error', str(e))

    def f_cambiar_a_pantalla_inicio(self):
        """Cambia a la pantalla del Inicio"""
        try:
            self.mediador.cambiar_presenter('PresenterInicio')
            self.mediador.obtener_presenter_actual()
        except Exception as e:
            self.vista.mensaje('Error', str(e))
