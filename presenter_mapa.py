class PresenterMapa:
    """Actua como puente entre la logica y la pantalla."""

    def __init__(self, view, model, mediador_presenter=None):
        self.vista = view
        self.modelo = model
        self.mediador = mediador_presenter

        self.vista.btn_buscar.add_listener(self.f_buscar_nombre)
        self.vista.btn_select.add_listener(self.f_buscar_por_nombre)
        self.vista.click_mapa.add_listener(self.f_buscar_por_click)
        self.vista.btn_buscar_pais.add_listener(self.f_buscar_pais)

    def f_buscar_nombre(self):
        nombre_ciudad = self.vista.obtener_ciudad_buscada()

        if not nombre_ciudad:
            self.vista.mostrar_error("Introduce una ciudad para buscar.")
            return
        list_ciudades = self.modelo.buscar_nombre_ciudad(nombre_ciudad)

        if list_ciudades is None:
            self.vista.mostrar_error("No se encontro la ciudad o no se pudieron obtener datos.")
            return
        self.vista.mostrar_lista_ciudades(list_ciudades)

    def f_buscar_por_nombre(self, nombre_select):
        try:
            ciudad = self.modelo.consultar_clima_actual_localidad(nombre_select)

            nombre = ciudad.nombre
            lat = ciudad.lat
            lon = ciudad.lon

            temperatura = ciudad.parametros.temperatura
            humedad = ciudad.parametros.humedad
            viento = ciudad.parametros.viento
            weather_code = ciudad.parametros.weather_code
            is_day = ciudad.parametros.is_day

            tipo_icono = self.obtener_tipo_icono(weather_code, is_day)

            self.vista.mostrar_ciudad_en_mapa(
                nombre,
                lat,
                lon,
                temperatura,
                humedad,
                viento,
                tipo_icono
            )

        except Exception as e:
            self.vista.mostrar_error(str(e))

    def f_buscar_por_click(self, coordenadas):
        try:
            ciudad = self.modelo.consultar_clima_actual_localidad(coordenadas)

            if ciudad is None:
                self.vista.mostrar_error("No se pudieron obtener datos para ese punto.")
                return

            nombre = ciudad.nombre
            lat = ciudad.lat
            lon = ciudad.lon

            temperatura = ciudad.parametros.temperatura
            humedad = ciudad.parametros.humedad
            viento = ciudad.parametros.viento
            weather_code = ciudad.parametros.weather_code
            is_day = ciudad.parametros.is_day

            tipo_icono = self.obtener_tipo_icono(weather_code, is_day)

            self.vista.mostrar_ciudad_en_mapa(
                nombre,
                lat,
                lon,
                temperatura,
                humedad,
                viento,
                tipo_icono
            )

        except Exception as e:
            self.vista.mostrar_error(str(e))

    def obtener_tipo_icono(self, weather_code, is_day):
        if weather_code == 0:
            if is_day == 1:
                return "sol"
            else:
                return "luna"
        if weather_code in [1, 2, 3]:
            return "nube"
        if weather_code in [45, 48]:
            return "niebla"
        if weather_code in [51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82]:
            return "lluvia"
        if weather_code in [71, 73, 75, 77, 85, 86]:
            return "nieve"
        if weather_code in [95, 96, 99]:
            return "tormenta"

    def f_buscar_pais(self):
        try:
            nombre_pais = self.vista.obtener_ciudad_buscada()

            if not nombre_pais:
                self.vista.mostrar_error("Introduce un país.")
                return

            cantidad_ciudades = 3

            pais = self.modelo.consultar_clima_actual_pais(
                nombre_pais,
                cantidad_ciudades
            )

            datos_ciudades = []

            for ciudad in pais.localidades:
                nombre = ciudad.nombre
                lat = ciudad.lat
                lon = ciudad.lon

                temperatura = ciudad.parametros.temperatura
                humedad = ciudad.parametros.humedad
                viento = ciudad.parametros.viento
                weather_code = ciudad.parametros.weather_code
                is_day = ciudad.parametros.is_day

                tipo_icono = self.obtener_tipo_icono(weather_code, is_day)

                datos_ciudad = {
                    "nombre": nombre,
                    "lat": lat,
                    "lon": lon,
                    "temperatura": temperatura,
                    "humedad": humedad,
                    "viento": viento,
                    "tipo_icono": tipo_icono
                }

                datos_ciudades.append(datos_ciudad)

            self.vista.mostrar_varias_ciudades_en_mapa(datos_ciudades)

        except Exception as e:
            self.vista.mostrar_error(str(e))