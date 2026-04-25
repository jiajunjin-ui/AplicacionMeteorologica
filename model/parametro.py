import pandas as pd
from .ciudad import Ciudad
from .solicitudopenmeteo import SolicitudOpenMeteo

class Parametro:
    """Clase que almacena los resultado, datos meteorológicos,
    en el atributo param.

    Parameter
    ----------
    - ciudad : class
        Instancia de clase Ciudad usada para extraer las coordenadas de esta.
    - nombre_ciudad : str
        String del nombre completo de la ciudad seleccionada por el usuario.
    """
    def __init__(self, ciudad, nombre_ciudad):
        if isinstance(ciudad, Ciudad):
            self.ciudad = ciudad 
        self.nombre_ciudad = nombre_ciudad
        self.param = None
        self.solicitud = SolicitudOpenMeteo(self.ciudad)

    def actualizar_param(self):
        """Método que almacena los resultados de las variables meteorológica
        en el atributo param.
        """
        try:
            self.param = self.solicitud.obtener_var(self.nombre_ciudad)
            return self.param
        except Exception:
            raise Exception('Error al actualizar parámetros')