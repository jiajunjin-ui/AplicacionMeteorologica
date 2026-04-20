import requests

class Ciudad:
    """Clase que da información sobre la ciudad seleccionada por el usuario.

    Parameter
    ----------
    - nombre : str
        Caneda de texto que corresponde a una ciudad; puede ser el nombre entero o una parte de esta. 
        Nota: debe de contener al menos 3 leras.
    """
    _caractres_invalidos = '#%/<>"()&:;|+=*@#~$€£0123456789'

    def __init__(self, nombre=None):
        self._nombre = None
        self._datos_ciudades = {}
        if nombre is not None:
            self.nombre = nombre

    @property
    def nombre(self):
        """Getter: Toma el nombre"""
        return self._nombre
    
    @nombre.setter
    def nombre(self, nuevo_nombre):
        """Setter: Asignar nombre después de validación"""

      # Validación ##########################
        if not isinstance(nuevo_nombre, str):
           raise TypeError(f'El nombre debe ser una cadena de texto, no {type(nuevo_nombre).__name__}')
        if nuevo_nombre != None and not nuevo_nombre.strip():
           raise ValueError('Nombre en blanco!')
        if any(i in self._caractres_invalidos for i in nuevo_nombre):
           raise TypeError(f'{nuevo_nombre} contiene caracteres inválidos')
       
      # Set #################################
        self._nombre = nuevo_nombre
        
    @property
    def datos_ciudad(self):
        return self._datos_ciudades
           
    def buscar_ciudades(self):
        """Función que se conecta a OpenMeteo para buscar nombres de ciudades que presenten cierta coincidencia con el str introducido."""
        
        geo_url = "https://geocoding-api.open-meteo.com/v1/search?"
        params = {
            "name": self.nombre, 
            "count": 10,
            "language": "es",
            "format": "json"
        }
        responses = requests.get(geo_url, params=params).json()

        if "results" in responses:
            self._datos_ciudades = {}
            for result in responses["results"]:
                self._datos_ciudades[result["name"]] = (result["latitude"], result["longitude"])
            return list(self._datos_ciudades.keys())
        elif len(self.nombre) < 3:
            raise ValueError('Se debe introducir más de 3 letras')
        else:
            raise ValueError(f'La ciudad {self.nombre} no se encuentra en la base de OpenMeteo')
    
    def obtener_coordenadas(self, ciudad_select):
        """Función que devuelve las coordenadas de la ciudad seleccionada por el usuario."""
        if ciudad_select not in self._datos_ciudades:
            raise KeyError('Seleccione una ciudad')
        coord = self._datos_ciudades[ciudad_select]
        return coord[0], coord[1]