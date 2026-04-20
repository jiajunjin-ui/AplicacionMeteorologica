import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry
from model.ciudad import Ciudad


class OpenMeteo:
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
        lat, lon = self.ciudad.obtener_coordenadas(ciudad_select)
        params = {
            "latitude": lat,
	        "longitude": lon,
	        "hourly": ["precipitation_probability", "temperature_2m"],
            "past_days": 0,
            "forecast_days": 5
        }
        responses = self.openmeteo.weather_api(self.url_base, params=params)
        response = responses[0]

        porhora = response.Hourly()
        prob_precipitacion_h = porhora.Variables(0).ValuesAsNumpy()
        temp_2m_h = porhora.Variables(1).ValuesAsNumpy()

        porhora_data = {"date": pd.date_range(
            start = pd.to_datetime(porhora.Time(), unit="s", utc=True),
            end = pd.to_datetime(porhora.TimeEnd(), unit="s", utc=True),
            freq = pd.Timedelta(seconds=porhora.Interval()),
            inclusive = "left"
        )}

        porhora_data["prob_precipitación"] = prob_precipitacion_h
        porhora_data["temp_2m"] = temp_2m_h

        porhora_dataframe = pd.DataFrame(data = porhora_data)
        return porhora_dataframe



   
