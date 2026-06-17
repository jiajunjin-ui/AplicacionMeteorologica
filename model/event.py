class Event:
    """Clase para gestionar la comunicación entre Vista y Presenter."""
    def __init__(self):
        """Inicializa una lista vacía de suscriptores."""
        self.suscriptores = []

    def add_listener(self, funcion):
        """Añade una función a la lista de suscriptores."""
        self.suscriptores.append(funcion)

    def emit(self, *args):
        """Llama a todas las funciones suscritas, una por una."""
        for funcion in self.suscriptores:
            funcion(*args)
    
    def clear_listeners(self):
        """Elimina todos las funciones de la lista de suscriptores"""
        self.suscriptores.clear()
