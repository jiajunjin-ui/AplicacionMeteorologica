from .ciudad import Ciudad
from .openmeteo import OpenMeteo

class ModelFacade:
    """ 
    Patrón de diseño Facade (Fachada) para Model: 
    Agrupar todos los metodos de las clases lógicas en una sola clase.
    """
    def __init__(self, nombre_init=None):
        self.ciudad = Ciudad(nombre_init)
        self.var_meteo = OpenMeteo(self.ciudad)
    
    # Métodos de la clase Ciudad ########################
    def buscar_ciudades(self, text):
        self.ciudad.nombre = text
        return self.ciudad.buscar_ciudades()
    
    def obtener_coordenadas(self, ciudad_select):
        return self.ciudad.obtener_coordenadas(ciudad_select)
    
    # Métodos de la clase OpenMeteo #####################
    def obtener_var(self, ciudad_select):
        return self.var_meteo.obtener_var(ciudad_select)
