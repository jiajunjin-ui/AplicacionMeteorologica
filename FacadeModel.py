from SolicitudOpenMeteo import SolicitudOpenMeteo

class FacadeModel:
    """ Patrón de diseño Facade (Fachada) para Model:
        Agrupar todos los metodos de las clases lógicas en una sola clase.
    """
    def __init__(self):
        self.servicio = SolicitudOpenMeteo()

    def buscar_ciudad_con_clima(self, nombre_ciudad):
        ciudad = self.servicio.obtener_ciudad_con_clima(nombre_ciudad)
        return ciudad

    def buscar_punto_con_clima(self, latitud, longitud):
        ciudad = self.servicio.obtener_punto_con_clima(latitud, longitud)
        return ciudad

    def facade_buscar_ciudades(self, texto_ciudad):
        lista_ciudades = self.servicio.buscar_ciudades(texto_ciudad)
        return lista_ciudades

    def facade_actualizar_param(self, nombre_ciudad):
        dataframe = self.servicio.obtener_prevision_horaria(nombre_ciudad)
        return dataframe #
