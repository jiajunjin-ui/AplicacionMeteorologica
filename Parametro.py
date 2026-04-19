class Parametro:
    def __init__(self, temperatura, humedad, viento):
        self.temperatura = temperatura
        self.humedad = humedad
        self.viento = viento

    def mostrar_parametros(self):
        print("Temperatura:", self.temperatura, "°C")
        print("Humedad:", self.humedad, "%")
        print("Viento:", self.viento, "km/h")