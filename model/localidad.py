class Localidad:
    """Clase que da información sobre la localidad seleccionada por el usuario. 
         
    Las localidades pueden ser ciudades, puntos del mapa o países.

    Parameter
    ----------
    Atributos de clase

    - nombre : str
        Caneda de texto que corresponde al nombre de la localidad
    - lat : float or list
        Valor numérico o lista de valores num. que corresponde a la latitud/es de una localidad
    - lon : float or list 
        Valor numérico o lista de valores num. que corresponde a la longitud/es de una localidad
    - forzar_set : bool
        Variable que al estar en True fuerza el set sin validación 
    Atributo de instancia 

    - parame : class
        Parametros climático gurdados en la clase Parametro
    """
    _caracteres_invalidos = '{#%/"&<>[]():;|+=*@#~$€£}0123456789'

    def __init__(self, nombre=None, lat=None, lon=None, forzar_set=False):
        self._nombre = None
        if nombre is not None:
            if forzar_set == True:
                self._nombre = nombre  # Saltar validación
            else:
                self.nombre = nombre 
        
        self.lat = lat
        self.lon = lon
        self.parametros = None
    
    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, new_nombre):   
        if not isinstance(new_nombre, str):
            raise TypeError(f"El nombre debe ser una cadena de texto, no {type(new_nombre).__name__}")
        if any(caracter in self._caracteres_invalidos for caracter in new_nombre):
            raise ValueError(f"{new_nombre} contiene caracteres inválidos.")

        self._nombre = new_nombre

if __name__ == '__main__':
    localidad1 = Localidad(nombre="Barcelona", lat=41.3888, lon=2.159)
    print(localidad1.nombre, localidad1.lat, localidad1.lon)
    localidad2 = Localidad(nombre="Barc#lona", lat=41.3888, lon=2.159, forzar_set=True)
    print(localidad2.nombre, localidad2.lat, localidad2.lon)
