class PresenterVentana2:
    def __init__(self, view, model):
        # Agregación: recibe instancias externas
        self.vista = view
        self.modelo = model

        # Suscripción a las señales de la vista
        self.vista.btnBuscar.add_listener(self.f_actualizar_lista)
        self.vista.btnSelect.add_listener(self.f_actualizar_grafico)


    def f_actualizar_lista(self):
        try:
            text_in = self.vista.entrada()
            lista_ciudades = self.modelo.facade_buscar_ciudades(text_in)
            self.vista.salida(lista_ciudades)
        except Exception as e:
            self.vista.mensaje('Error', str(e))
    
    def f_actualizar_grafico(self, nombre_ciudad):
        try:
            ciudad_select = nombre_ciudad
            dataframe = self.modelo.facade_actualizar_param(ciudad_select)
            self.vista.crear_grafico(dataframe)
        except Exception as e:
            self.vista.mensaje('Error', str(e))


