class Event:
    """Clase para gestionar la comunicación entre Vista y Presenter."""
    def __init__(self):
        # Lista donde guardaremos las funciones que quieren 'escuchar'
        self.suscriptores = []

    def add_listener(self, funcion_a_conectar):
        """Añade una función a la lista de suscriptores."""
        self.suscriptores.append(funcion_a_conectar)

    def emit(self):
        """Llama a todas las funciones suscritas, una por una."""
        for funcion in self.suscriptores:
            funcion()
