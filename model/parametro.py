import pandas as pd
from .ciudad import Ciudad
from .solicitudopenmeteo import SolicitudOpenMeteo

class Parametro:
    def __init__(self, ciudad, nombre_ciudad):
        if isinstance(ciudad, Ciudad):
            self.ciudad = ciudad 
        self.nombre_ciudad = nombre_ciudad
        self.param = None
        self.solicitud = SolicitudOpenMeteo(self.ciudad)

    def actualizar_param(self):
        try:
            self.param = self.solicitud.obtener_var(self.nombre_ciudad)
            return self.param
        except Exception:
            raise Exception('Error al actualizar parámetros')
    
# if __name__ == "__main__" :
#     ciudad1 = Ciudad("Barce")
#     ciudad1.buscar_ciudades()
#     param1 = Parametro(ciudad1,"Barcelona")
#     print(param1.actualizar_param())




    
    
    
