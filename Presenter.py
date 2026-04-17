class Presenter:
    def __init__(self, view, model):
        # Agregación: recibe instancias externas
        self.vista = view
        self.modelo = model

        # Suscripción a las señales de la vista
        self.vista.actLista.add_listener(self.fact_lista)

    def fact_lista(self):
        try:
            text_in = self.vista.entrada()
            self.modelo.nombre = text_in
            lista_out = self.modelo.buscar_ciudades()
            self.vista.salida(lista_out)
        except Exception as e:
            self.vista.mensaje('Error', str(e))
            
