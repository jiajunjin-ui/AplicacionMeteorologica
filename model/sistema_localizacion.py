import requests
from .localidad import Localidad

class SistemaLocalizacion:
    """Clase que da información geocoding de las localidades(ciudades o puntos en mapa),
    devolviendo los resultados en instancias de Localidad.
    - Usa un str del nombre completo o incompleto de la ciudad -----> devuelve una instancia de Localidad() 
    - Usa una tupla de coordenadas ----> devuelve una instancia de Localidad()
      
      La instancia de Localidad() que devuelve solo contiene los datos de nombre, lat y lon; el atributo parametros se asignan más adelante.
    """
    def __init__(self):
        self.url_geo = "https://geocoding-api.open-meteo.com/v1/search"
        self._ciudades_encontradas = {}
        self.url_geo_inverso = "https://nominatim.openstreetmap.org/reverse"

    # Gráfico y Mapa ##########################################################
    def buscador_nombre_ciudad(self, text):
        """Funcion se conecta al servicio de geocoding de OpenMeteo para buscar nombres de ciudades
        que presenten cierta coincidencia con el str introducido.
        """
        if len(text) < 3:
            raise ValueError("Se deben introducir al menos 3 letras.")
        if not text.strip():
            raise ValueError("Nombre en blanco!")
        
        params = {
            "name": text, 
            "count": 10,
            "language": "es",
            "format": "json"
        }

        respuesta = requests.get(self.url_geo, params=params).json()

        if "results" in respuesta:
            self._ciudades_encontradas = {}
            for res in respuesta["results"]:
                pais = res.get("country", "País desconocido")
                nombre_completo = f'{res["name"]}, {pais}'
                self._ciudades_encontradas[nombre_completo] = Localidad(
                    nombre=res["name"],
                    lat=res["latitude"],
                    lon=res["longitude"]
                )
            return list(self._ciudades_encontradas.keys())
        else:
            raise ValueError(f'La ciudad {text} no se encuentra en la base de OpenMeteo')

    def seleccionar_ciudad(self, ciudad_select):
        """Función que devuelve las coordenadas de la ciudad seleccionada por el usuario."""
        if ciudad_select not in self._ciudades_encontradas:
            raise KeyError("Seleccione una ciudad de la lista generada.") 
        return self._ciudades_encontradas[ciudad_select]
    

    # Mapa ####################################################################
    def buscador_nombre_coordenadas(self, coord):
        try:
            lat, lon = coord
            params = {
                "lat":lat,
                "lon": lon,
                "format": "jsonv2",
                "addressdetails": 1,
                "accept-language": "es",
            }

            headers = {"User-Agent": "AplicacionMeteorologica/1.0"}

            respuesta = requests.get(self.url_geo_inverso, params=params, headers=headers).json()

            direccion = respuesta.get("address", {})
            nombre = (
                direccion.get("city")
                or direccion.get("town")
                or direccion.get("village")
                or direccion.get("municipality")
                or direccion.get("hamlet")
                or direccion.get("county")
                or direccion.get("state")
                or direccion.get("display_name")
            )
            if not nombre:
                nombre = f"Punto ({lat:.2f}, {lon:.2f})"
        
            return Localidad(nombre=nombre, lat=lat, lon=lon, forzar_set=True) 
        
        except Exception as e:
            print("Error al obtener el nombre del lugar:", e)
            nombre = f"Punto ({lat:.2f}, {lon:.2f})"
            return Localidad(nombre=nombre, lat=lat, lon=lon, forzar_set=True)

if __name__ == '__main__':
    sistema_localitzacio = SistemaLocalizacion()
    lista_nombres = sistema_localitzacio.buscador_nombre_ciudad('Barce')
    localidad1 = sistema_localitzacio.seleccionar_ciudad(lista_nombres[0])
    print("Localidad 1:", localidad1.nombre, localidad1.lat, localidad1.lon)

    localidad2 = sistema_localitzacio.buscador_nombre_coordenadas((41.4307, 2.2186))
    print("Localidad 2:", localidad2.nombre, localidad2.lat, localidad2.lon)



