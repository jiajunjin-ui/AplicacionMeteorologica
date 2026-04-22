import pandas as pd
from ciudad import Ciudad
from solicitudopenmeteo import SolicitudOpenMeteo
import time

class Parametro:
    def __init__(self, ciudad, ciudad_select):
        if isinstance(ciudad, Ciudad):
            self.ciudad = ciudad 
        self.ciudad_select = ciudad_select
        self.param = None
        self.solicitud = SolicitudOpenMeteo(self.ciudad)

    def actualizar_param(self):
        try:
            self.param = self.solicitud.obtener_var(self.ciudad_select)
            return self.param
        except Exception:
            raise Exception('Error al actualizar parámetros')
    
if __name__ == "__main__" :
    ciudad1 = Ciudad("Barce")
    ciudad1.buscar_ciudades()
    param1 = Parametro(ciudad1,"Barcelona")
    print(param1.actualizar_param())




    
    
    
