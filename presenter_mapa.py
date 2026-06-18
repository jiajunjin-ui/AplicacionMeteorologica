class PresenterMapa:
    """Actua como puente entre la logica y la pantalla."""

    def __init__(self, view, model, mediador_presenter=None):
        self.vista = view
        self.modelo = model
        self.mediador = mediador_presenter

        self.vista.btn_buscar.add_listener(self.f_buscar_nombre) # Cuando se ha pulsado buscar localidad va a la funcion f_buscar_nombre
        self.vista.btn_select.add_listener(self.f_buscar_por_nombre) # Cuando se ha selecciona una de las localidades va a la funcion f_buscar_por_nombre
        self.vista.click_mapa.add_listener(self.f_buscar_por_click) # Cuando se ha clicado en el mapa va a la funcion f_buscar_por_click
        self.vista.btn_buscar_pais.add_listener(self.f_buscar_pais) # Cuando se ha pulsado a buscar pais va a la funcion f_buscar_pais
        self.vista.btn_select_pais.add_listener(self.f_buscar_por_pais) # Cuando se ha seleccionado uno de los paises va a la funcion f_buscar_por_pais

    def f_buscar_nombre(self):
        """
        Funcion que obtiene la localidad introducida por el usuario y que comprueba si es
        valida y busca una lista de localidades con el nombre parecido
        """
        try:
            nombre_ciudad = self.vista.obtener_ciudad_buscada()

            if not nombre_ciudad:
                self.vista.mostrar_error("Introduce una ciudad para buscar.")
                return

            list_ciudades = self.modelo.buscar_nombre_ciudad(nombre_ciudad)

            if list_ciudades is None:
                self.vista.mostrar_error("No se encontro la ciudad o no se pudieron obtener datos.")
                return

            self.vista.mostrar_lista_ciudades(list_ciudades)

        except Exception as e:
            self.vista.mostrar_error(str(e))

    def f_buscar_por_nombre(self, nombre_select):
        """
        Funcion que, una vez el usuario haya seleccionado una localidad de la lista
        proporcionada, busca los parametros de la ciudad genera el marcador y lo muestra
        en el mapa
        """
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
        """
        Funcion que, una vez el usuario haya clicado algun punto del mapa, busca
        la ciudad, los parametros de la ciudad y coloca el marcador en el mapa
        """
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

            # GENERA MARCADOR
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
        """
        Funcion que determina el icono que debe tener la ciudad para mostrar si esta
        despejado, nublado, niebla, lluvia, nieve o tormenta
        """
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
        """
        Funcion que obtiene el pais introducido por el usuario y que comprueba si es
        valido y busca una lista de paises con el nombre parecido
        """
        try:
            nombre_pais = self.vista.obtener_ciudad_buscada()

            if not nombre_pais:
                self.vista.mostrar_error("Introduce un pais.")
                return

            lista_paises = self.modelo.buscar_nombre_pais(nombre_pais)
            self.vista.mostrar_lista_paises(lista_paises)

        except Exception as e:
            self.vista.mostrar_error(str(e))

    def f_buscar_por_pais(self, nombre_pais):
        """
        Funcion que obtiene el pais introducido por el usuario y que busca las
        principales ciudades por poblacion del pais y sus parametros y
        genera los marcadores
        """
        try:
            cantidad_ciudades = 10

            pais = self.modelo.consultar_clima_actual_pais(nombre_pais, cantidad_ciudades)

            # GENERAR MARCADORES
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