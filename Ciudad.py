class Ciudad:
    def __init__(self, nombre, latitud=None, longitud=None):
        self.nombre = nombre
        self.latitud = latitud
        self.longitud = longitud
        self.parametros = None

    def mostrar_info(self):
        print("Ciudad:", self.nombre)
        print("Latitud:", self.latitud)
        print("Longitud:", self.longitud)

        if self.parametros is not None:
            self.parametros.mostrar_parametros()
        else:
            print("No hay datos meteorológicos")