from .sistema_localizacion import SistemaLocalizacion
from .solicitud_openmeteo import SolicitudOpenMeteo

class AppMeteo:
    def __init__(self):
        self.buscador = SistemaLocalizacion()
        self.servicio_clima = None
    
    def buscar_nombre_ciudad(self, text):
        return self.buscador.buscador_nombre_ciudad(text)

    def consultar_pronostico_localidad(self, loc):
        if isinstance(loc, str):
            localidad = self.buscador.seleccionar_ciudad(loc)
        elif isinstance(loc, tuple):
            localidad = self.buscador.buscador_nombre_coordenads(loc)
        
        self.servicio_clima = SolicitudOpenMeteo(localidad)
        parametros = self.servicio_clima.obtener_pronostico_horario()
        localidad.parametros = parametros
        return localidad
    
    def consultar_clima_actual_localidad(self, loc):
        if isinstance(loc, str):
            localidad = self.buscador.seleccionar_ciudad(loc)
        if isinstance(loc, tuple):
            localidad = self.buscador.buscador_nombre_coordenads(loc)
        
        self.servicio_clima = SolicitudOpenMeteo(localidad)
        parametros = self.servicio_clima.obtener_clima_actual()
        localidad.parametros = parametros
        return localidad
    