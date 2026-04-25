"""
Paquete lógico:
Paquete que agrupa toda la lógica de los Model's 
que se quiere que se muestre fuera de la carpeta 
model.

- ModelFacade
Métodos de Ciudad ---agrupar---> ModelFacade
Métodos de OpenMeteo ---agruopar---> ModelFacade

- Event

"""
from .facademodel import ModelFacade
from .event import Event

__all__ = ['ModelFacade', 'Event']