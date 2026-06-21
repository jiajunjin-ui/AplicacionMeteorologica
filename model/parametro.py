class Parametro:
    """Clase que almacena información sobre las variables climáticas de 
    la localidad (Localidad, Pais) seleccionada por el usuario.

    Parameter
    ----------
    Atributos de clase

    - temperatura : float / list(float)
        Atributo que almacena info. sobre la temperatura en ºC
    - humedad : float / list(float)
        Atributo que almacena info. sobre la humedad relativa en %
    - viento : float / list(float)
        Atributo que almacena info. sobre la valocidad del viento en km/h
    - direccion_viento : float / list(float)
        Atributo que almacena info. sobre la dirección del viento en º
    - rafaga_viento : float / list(float)
        Atributo que almacena info. sobre la racha del viento 
        (aumento de vel. en un corto periodo de tiempo) en km/h
    - prob_precip : float / list(float)
        Atributo que almacena info. sobre la prob. de precipitación en %
    - weather_code : int / list(int)
        Atributo que almacena info. sobre el estado del cielo en un int de la siguiente lista:

        [0, 1, 2, 3, 45, 48, 51, 53, 55, 56, 57 ,61 , 63, 65, 66, 67, 71, 73, 75, 77, 80, 81, 82, 85, 86, 95, 96, 99]
    - date : str / list(str)
        Atributo que almacena info. sobre fechas 
    - is_day : bool / list(bool)
        Atributo que almacena info. sobre si es de dia o de noche 
    """
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