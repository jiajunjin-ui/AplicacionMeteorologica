from .sistema_localizacion import SistemaLocalizacion
from .sistema_pais import SistemaPais
from .solicitud_openmeteo import SolicitudOpenMeteo


class AppMeteo:
    def __init__(self):
        self.buscador = SistemaLocalizacion()
        self.buscador_paises = SistemaPais()
        self.servicio_clima = None

    def buscar_nombre_ciudad(self, text):
        return self.buscador.buscador_nombre_ciudad(text)

    def consultar_pronostico_localidad(self, loc):
        if isinstance(loc, str):
            localidad = self.buscador.seleccionar_ciudad(loc)
        elif isinstance(loc, tuple):
            localidad = self.buscador.buscador_nombre_coordenadas(loc)
        else:
            raise TypeError("El formato de localidad no es valido.")

        self.servicio_clima = SolicitudOpenMeteo(localidad)
        parametros = self.servicio_clima.obtener_pronostico_horario()
        localidad.parametros = parametros
        return localidad

    def consultar_clima_actual_localidad(self, loc):
        if isinstance(loc, str):
            localidad = self.buscador.seleccionar_ciudad(loc)
        elif isinstance(loc, tuple):
            localidad = self.buscador.buscador_nombre_coordenadas(loc)
        else:
            raise TypeError("El formato de localidad no es valido.")

        self.servicio_clima = SolicitudOpenMeteo(localidad)
        parametros = self.servicio_clima.obtener_clima_actual()
        localidad.parametros = parametros
        return localidad

    def buscar_nombre_pais(self, texto):
        return self.buscador_paises.buscador_nombre_pais(texto)

    def consultar_clima_actual_pais(self, nombre_pais, cantidad):
        pais = self.buscador_paises.buscar_ciudades_principales(nombre_pais, cantidad)

        for localidad in pais.localidades:
            self.servicio_clima = SolicitudOpenMeteo(localidad)
            parametros = self.servicio_clima.obtener_clima_actual()
            localidad.parametros = parametros

        return pais

    def consultar_ranking_pais(self, nombre_pais, cantidad, tipo_ranking):
        """
        Obtiene el pais, cantidad y tipo de ranking seleccionado por el usuario y busca las principales ciudades del pais y
        sus parametros para despues ordenarlo en funcion del tipo_ranking.
        """
        pais = self.consultar_clima_actual_pais(nombre_pais, cantidad)
        ciudades = pais.localidades

        if tipo_ranking == "mas_calurosas":
            return sorted(
                ciudades,
                key=lambda ciudad: ciudad.parametros.temperatura,
                reverse=True
            )
        if tipo_ranking == "mas_frias":
            return sorted(
                ciudades,
                key=lambda ciudad: ciudad.parametros.temperatura
            )
        if tipo_ranking == "mas_viento":
            return sorted(
                ciudades,
                key=lambda ciudad: ciudad.parametros.viento,
                reverse=True
            )
        if tipo_ranking == "mas_humedad":
            return sorted(
                ciudades,
                key=lambda ciudad: ciudad.parametros.humedad,
                reverse=True
            )

        raise ValueError("Tipo de ranking no valido.")
