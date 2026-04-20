class Presenter:
    def __init__(self, view, model):
        # Agregación: recibe instancias externas
        self.vista = view
        self.modelo = model

        # Suscripción a las señales de la vista
        self.vista.actLista.add_listener(self.f_act_lista)


    def f_act_lista(self):
        try:
            text_in = self.vista.entrada()
            lista_ciudades = self.modelo.buscar_ciudades(text_in)
            self.vista.salida(lista_ciudades)
        except Exception as e:
            self.vista.mensaje('Error', str(e))
    
