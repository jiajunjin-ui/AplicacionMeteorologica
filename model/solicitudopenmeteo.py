import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry
from .ciudad import Ciudad


class SolicitudOpenMeteo:
    """Clase que devuelve información de variables meteorológicas de la ciudad seleccionada por el usuario.

    Parameter
    ----------
    - ciudad : class
        Instancia de clase Ciudad usada para extraer las coordenadas de esta.
    """
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)
    
    def __init__(self, ciudad):
        if isinstance(ciudad, Ciudad):
            self.ciudad = ciudad
            
        self.url_base = "https://api.open-meteo.com/v1/forecast"
    
    def obtener_var(self, ciudad_select):
        """Método que devuelve un DataFrame de las variables meteorológica
        Parameter
        ----------
        - ciudad_select : str
            Nombre completo de la ciudad, escrito correctamente
        """
        lat, lon = self.ciudad.obtener_coordenadas(ciudad_select)
        params = {
            "latitude": lat,
	        "longitude": lon,
	        "hourly": [
                "temperature_2m", 
                "relative_humidity_2m", 
                "precipitation_probability", 
                "wind_speed_10m", 
                "weather_code"
                ],
            "past_days": 0,
            "forecast_days": 5
        }
        responses = self.openmeteo.weather_api(self.url_base, params=params)
        response = responses[0]

        porhora = response.Hourly()

        temp_2m_h = porhora.Variables(0).ValuesAsNumpy()
        hum_rel_h = porhora.Variables(1).ValuesAsNumpy()
        prob_precip_h = porhora.Variables(2).ValuesAsNumpy()
        wind_speed_10m_h = porhora.Variables(3).ValuesAsNumpy()
        weather_code_h = porhora.Variables(4).ValuesAsNumpy()


        porhora_data = {"date": pd.date_range(
            start = pd.to_datetime(porhora.Time(), unit="s", utc=True),
            end = pd.to_datetime(porhora.TimeEnd(), unit="s", utc=True),
            freq = pd.Timedelta(seconds=porhora.Interval()),
            inclusive = "left"
        )}
        porhora_data["temp_2m"] = temp_2m_h
        porhora_data["hum_rel"] = hum_rel_h
        porhora_data["prob_precip"] = prob_precip_h
        porhora_data["wind_speed_10m"] = wind_speed_10m_h
        porhora_data["weather_code"] = weather_code_h
        
        porhora_dataframe = pd.DataFrame(data = porhora_data)
        return porhora_dataframe

# if __name__ == "__main__" :
#     ciudad1 = Ciudad("Barce")
#     ciudad1.buscar_ciudades()
#     solicitud = SolicitudOpenMeteo(ciudad1)
#     print(solicitud.obtener_var("Barcelona"))  
