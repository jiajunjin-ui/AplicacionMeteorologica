import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry
from .localidad import Localidad
from .parametro import Parametro

class SolicitudOpenMeteo:
    """Clase que da información sobre variables clímaticas de localidades(ciudades y puntos en mapa),
    devolviendo los resultados en instancias de Parametro
    - Usa una instancia de Localidad() ---> devuelve una instancia de Parametro()

    Parameter
    ----------
    - localidad : class
        Clase que guarda los datos de geocoding: nombre, lat, lon; y datos climáticos: Parametro()
    """
  # Guardado de resultados en cache para agilizar la busqueda, si se repite la misma busqueda en menos de 1h 
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    def __init__(self, localidad):
        self.url_openmeteo = "https://api.open-meteo.com/v1/forecast"
        if isinstance(localidad, Localidad):
            self.localidad = localidad

    def obtener_pronostico_horario(self):
        """Método que da el pronóstico climático de los próximos 3 días 
        de la localidad escogida."""
        params = {
            "latitude": self.localidad.lat,
	        "longitude": self.localidad.lon,
	        "hourly": [
                "temperature_2m", 
                "relative_humidity_2m", 
                "precipitation_probability", 
                "wind_speed_10m", 
                "weather_code"
                ],
            "past_days": 0,
            "forecast_days": 3
            }
        
        respuestas = self.openmeteo.weather_api(self.url_openmeteo, params=params)
        respuesta = respuestas[0]

        porhora = respuesta.Hourly()

        temp_2m_h = porhora.Variables(0).ValuesAsNumpy()
        hum_rel_h = porhora.Variables(1).ValuesAsNumpy()
        prob_precip_h = porhora.Variables(2).ValuesAsNumpy()
        wind_speed_10m_h = porhora.Variables(3).ValuesAsNumpy()
        weather_code_h = porhora.Variables(4).ValuesAsNumpy()

        date_h = pd.date_range(
            start = pd.to_datetime(porhora.Time(), unit="s", utc=True),
            end = pd.to_datetime(porhora.TimeEnd(), unit="s", utc=True),
            freq = pd.Timedelta(seconds=porhora.Interval()),
            inclusive = 'left'
            )
        date_h = date_h.to_pydatetime()
            
        return Parametro(
            temperatura=temp_2m_h,
            humedad=hum_rel_h,
            viento=wind_speed_10m_h,
            prob_precip=prob_precip_h,
            weather_code=weather_code_h,
            date=date_h
            )

    def obtener_clima_actual(self):
        """"Método que da el clima actual de la localidad escogida."""
        params = {
            "latitude": self.localidad.lat,
	        "longitude": self.localidad.lon,
	        "current": [
                "temperature_2m",
                "relative_humidity_2m", 
                "precipitation_probability", 
                "wind_speed_10m", 
                "wind_direction_10m",
                "wind_gusts_10m",
                "weather_code",
                "is_day"
                ],
            "timezone": "auto",
            "format": "flatbuffers"
            }
    
        responses = self.openmeteo.weather_api(self.url_openmeteo, params=params)

        temp_2m_actual_list = []
        hum_rel_actual_list = []
        prob_precip_actual_list = []
        wind_speed_10m_actual_list = []
        wind_direction_10m_actual_list = []
        wind_gusts_10m_actual_list = []
        weather_code_actual_list = []
        is_day_actual_list = []
        
        es_lista = False
        
        if isinstance(self.localidad.lon, list) and isinstance(self.localidad.lat, list):
            es_lista = True 

        for response in responses:
            actual=response.Current()

            temp_2m_actual_list.append(actual.Variables(0).Value())
            hum_rel_actual_list.append(actual.Variables(1).Value())
            prob_precip_actual_list.append(actual.Variables(2).Value())
            wind_speed_10m_actual_list.append(actual.Variables(3).Value())
            wind_direction_10m_actual_list.append(actual.Variables(4).Value())
            wind_gusts_10m_actual_list.append(actual.Variables(5).Value())
            weather_code_actual_list.append(actual.Variables(6).Value())
            is_day_actual_list.append(actual.Variables(7).Value())
            date_actual = pd.to_datetime(actual.Time(), unit="s", utc=True)
        
        if es_lista:
            return Parametro(
                temperatura=temp_2m_actual_list,
                humedad=hum_rel_actual_list,
                viento=wind_speed_10m_actual_list,
                direccion_viento=wind_direction_10m_actual_list,
                rafaga_viento=wind_gusts_10m_actual_list,
                prob_precip=prob_precip_actual_list,
                weather_code=weather_code_actual_list,
                date=date_actual,
                is_day=is_day_actual_list
                )
        
        else:
            return Parametro(
                temperatura=temp_2m_actual_list[0],
                humedad=hum_rel_actual_list[0],
                viento=wind_speed_10m_actual_list[0],
                direccion_viento=wind_direction_10m_actual_list[0],
                rafaga_viento=wind_gusts_10m_actual_list[0],
                prob_precip=prob_precip_actual_list[0],
                weather_code=weather_code_actual_list[0],
                date=date_actual,
                is_day=is_day_actual_list[0]
                )
    
    

if __name__ == '__main__':
    localidad = Localidad(nombre="Barcelona", lat=41.3888, lon=2.159 )
    solicitud = SolicitudOpenMeteo(localidad)
    pronostico_hora = solicitud.obtener_pronostico_horario()
    print(pronostico_hora.date)
    print(pronostico_hora.humedad)

    clima_actual = solicitud.obtener_clima_actual()
    print(clima_actual.date)
    print(clima_actual.humedad)
    



