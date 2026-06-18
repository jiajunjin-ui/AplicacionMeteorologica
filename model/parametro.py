class Parametro:
    def __init__(self, temperatura=None, humedad=None, 
                 viento=None, direccion_viento=None, rafaga_viento=None,
                 prob_precip=None, weather_code=None, date=None, is_day=None):
        self.temperatura = temperatura
        self.humedad = humedad
        self.viento = viento
        self.direccion_viento = direccion_viento
        self.rafaga_viento = rafaga_viento
        self.prob_precip = prob_precip
        self.weather_code = weather_code
        self.date = date
        self.is_day = is_day