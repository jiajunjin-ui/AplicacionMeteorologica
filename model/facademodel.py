from .ciudad import Ciudad
from .solicitudopenmeteo import SolicitudOpenMeteo
from .parametro import Parametro

class ModelFacade:
    """ Patrón de diseño Facade (Fachada) para Model: 
    Agrupar todos los metodos de las clases lógicas en una sola clase.
    """
    def __init__(self, nombre=None):
        self.ciudad = Ciudad(nombre)
        self.solicitud = SolicitudOpenMeteo(self.ciudad)
        self.parametros = Parametro(self.ciudad, nombre_ciudad=None)
    
    # Métodos de la clase Ciudad ########################
    def facade_buscar_ciudades(self, text):
        self.ciudad.nombre = text
        return self.ciudad.buscar_ciudades()
    
    def facade_obtener_coordenadas(self, ciudad_select):
        return self.ciudad.obtener_coordenadas(ciudad_select)
    
    
    # Métodos de la clase OpenMeteo #####################
    def facade_obtener_var(self, ciudad_select):
        return self.solicitud.obtener_var(ciudad_select)
    
    
    # Métodos y atributos de la clase Parametro #####################
    def facade_actualizar_param_prediccion(self, ciudad_select):
        self.parametros.nombre_ciudad = ciudad_select
        return self.parametros.actualizar_param_prediccion()
    
    def facade_actualizar_param_ahora(self, ciudad_select):
        self.parametros.nombre_ciudad = ciudad_select
        return self.parametros.actualizar_param_ahora()

