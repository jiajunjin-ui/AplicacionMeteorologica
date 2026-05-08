"""
Paquete lógico:
Paquete que agrupa toda la lógica de los Model's 
que se quiere que se muestre fuera de la carpeta 
model.

Model's:
- AppMeteo
Métodos de Localidad ---agrupar en ---> AppMeteo
Métodos de SolicitudOpenMeteo ---agrupar en---> AppMeteo

- Event

"""
from .app_meteo import AppMeteo
from .event import Event

__all__ = ['AppMeteo', 'Event']