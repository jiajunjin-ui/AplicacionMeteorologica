"""
Paquete lógico:
Paquete que agrupa toda la lógica los Model's

- ModelFacade
Métodos de Ciudad ---agrupar---> ModelFacade
Métodos de OpenMeteo ---agruopar---> ModelFacade

- Event

"""
from .facademodel import ModelFacade
from .event import Event

__all__ = ['ModelFacade', 'Event']