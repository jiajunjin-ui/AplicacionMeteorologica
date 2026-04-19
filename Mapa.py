from SolicitudOpenMeteo import SolicitudOpenMeteo


class Mapa:
    """Modelo encargado de pedir datos meteorologicos."""

    def __init__(self, servicio=None):
        self.servicio =  SolicitudOpenMeteo()

    def buscar_ciudad_con_clima(self, nombre_ciudad):
        return self.servicio.obtener_ciudad_con_clima(nombre_ciudad)
