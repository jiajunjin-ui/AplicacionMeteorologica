from SolicitudOpenMeteo import SolicitudOpenMeteo


class Mapa:
    """Modelo encargado de pedir datos meteorológicos para mapa y gráfico."""

    def __init__(self, servicio=None):
        self.servicio = servicio if servicio is not None else SolicitudOpenMeteo()

    # Funcion usados por Presenter.py y Ventana.py
    def buscar_ciudad_con_clima(self, nombre_ciudad):
        return self.servicio.obtener_ciudad_con_clima(nombre_ciudad)

    def buscar_punto_con_clima(self, latitud, longitud):
        return self.servicio.obtener_punto_con_clima(latitud, longitud)

    def facade_buscar_ciudades(self, texto):
        return self.servicio.buscar_ciudades(texto)

    def facade_actualizar_param(self, ciudad_select):
        return self.servicio.obtener_prevision_horaria(ciudad_select)