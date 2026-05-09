class PresenterMapa:
    """Actua como puente entre la logica y la pantalla."""

    def __init__(self, view, model):
        self.vista = view
        self.modelo = model

        self.vista.btn_buscar.add_listener(self.f_buscar_nombre)
        self.vista.btn_select.add_listener(self.f_buscar_por_nombre)
        self.vista.click_mapa.add_listener(self.f_buscar_por_click)
        

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

            self.vista.mostrar_ciudad_en_mapa(
                nombre,
                lat,
                lon,
                temperatura,
                humedad,
                viento
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

            self.vista.mostrar_ciudad_en_mapa(
                nombre,
                lat,
                lon,
                temperatura,
                humedad,
                viento
            )

        except Exception as e:
            self.vista.mostrar_error(str(e))