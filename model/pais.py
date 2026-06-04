class Pais:
    def __init__(self, nombre=None, codigo_iso=None, fronteras=None, geometria=None):
        self.nombre = nombre
        self.codigo_iso = codigo_iso
        self.localidades = []
        self.fronteras = fronteras
        self.geometria = geometria

    def agregar_localidad(self, localidad):
        self.localidades.append(localidad)
    