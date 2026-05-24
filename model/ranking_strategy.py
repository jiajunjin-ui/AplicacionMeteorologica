from abc import ABC, abstractmethod


class EstrategiaRanking(ABC):
    """Clase base para todos los rankings."""

    @abstractmethod
    def ordenar(self, ciudades):
        pass

    @abstractmethod
    def obtener_valor(self, ciudad):
        pass


class RankingMasCalor(EstrategiaRanking):
    def ordenar(self, ciudades):
        return sorted(
            ciudades,
            key=lambda ciudad: ciudad.parametros.temperatura,
            reverse=True
        )

    def obtener_valor(self, ciudad):
        return f"{ciudad.parametros.temperatura:.2f} °C"


class RankingMasFrio(EstrategiaRanking):
    def ordenar(self, ciudades):
        return sorted(
            ciudades,
            key=lambda ciudad: ciudad.parametros.temperatura
        )

    def obtener_valor(self, ciudad):
        return f"{ciudad.parametros.temperatura:.2f} °C"


class RankingMasViento(EstrategiaRanking):
    def ordenar(self, ciudades):
        return sorted(
            ciudades,
            key=lambda ciudad: ciudad.parametros.viento,
            reverse=True
        )

    def obtener_valor(self, ciudad):
        return f"{ciudad.parametros.viento:.2f} km/h"


class RankingMasHumedad(EstrategiaRanking):
    def ordenar(self, ciudades):
        return sorted(
            ciudades,
            key=lambda ciudad: ciudad.parametros.humedad,
            reverse=True
        )

    def obtener_valor(self, ciudad):
        return f"{ciudad.parametros.humedad:.2f} %"


class RankingFactory:
    """Crea la estrategia de ranking según la opción elegida."""

    @staticmethod
    def crear(tipo_ranking):
        if tipo_ranking == "Más calurosas":
            return RankingMasCalor()

        if tipo_ranking == "Más frías":
            return RankingMasFrio()

        if tipo_ranking == "Más viento":
            return RankingMasViento()

        if tipo_ranking == "Más humedad":
            return RankingMasHumedad()

        raise ValueError("Tipo de ranking no válido.")