class Pais:
    def __init__(self, nombre=None, codigo_iso=None):
        self.nombre = nombre
        self.codigo_iso = codigo_iso
        self.localidades = []

    def agregar_localidad(self, localidad):
        self.localidades.append(localidad)