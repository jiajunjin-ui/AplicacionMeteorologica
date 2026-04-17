import requests

class Ciudad:
    def __init__(self, nombre):
        caractres_no_validos = '#%/<>"()&:;|+=*@#~$€£'
        if isinstance(nombre, str) and not any(i in caractres_no_validos for i in nombre):
            self.nombre = nombre
        else:
            raise TypeError(f'{nombre} no es un nombre de ciudad válida')
        
        self._datos_ciudades = {}
        
    def buscar_ciudades(self):
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
        else:
            raise ValueError(f'La ciudad {self.nombre} no se encuentra en la base de OpenMeteo')
    
    def obtener_coordenadas(self, ciudad_selec):
        if ciudad_selec in self.datos_ciudades:
            return self._datos_ciudades[ciudad_selec]
        return False
    
#ciudad1 = Ciudad("SAn ADri")
#lista_ciudades = ciudad1.buscar_ciudades()
#print(lista_ciudades)
#print(ciudad1.obtener_coordenadas(lista_ciudades[int(input())]))

#ciudad2 = Ciudad("Brusss")
#print(ciudad2.buscar_ciudades())
