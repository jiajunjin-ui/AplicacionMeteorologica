class Pais:
    """Clase que almacena información sobre la localidad seleccionada por el usuario.

    Parameter
    ----------
    Atributos de clase

    - nombre : str
        Caneda de texto correspondiente al nombre del país o región
    - codigo_iso : str
        Codigo de 2 carácteres que sireve como identificador del país o región
    - loncalidades : list 
        Lista de instancia de Localidad correspondientes a ciudades del país o región
    - fronteras : tupla
        Tupla de 4 elementos que acotan los límites del país o región  
    - geometria : gemoetry
        Atributo que almacena la gemetria del país o región 
    """
    def __init__(self, nombre=None, codigo_iso=None, fronteras=None, geometria=None):
        self.nombre = nombre
        self.codigo_iso = codigo_iso
        self.localidades = []
        self.fronteras = fronteras
        self.geometria = geometria

    def agregar_localidad(self, localidad):
        self.localidades.append(localidad)
    