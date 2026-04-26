class Presenter:
    """Actua como puente entre la logica y la pantalla."""

    def __init__(self, view, model):
        self.vista = view
        self.modelo = model

        self.vista.btn_buscar.add_listener(self.fbuscar)
        self.vista.click_mapa.add_listener(self.fbuscar_por_click)

    def fbuscar(self):
        nombre_ciudad = self.vista.obtener_ciudad_buscada()

        if not nombre_ciudad:
            self.vista.mostrar_error("Introduce una ciudad para buscar.")
            return

        ciudad = self.modelo.buscar_ciudad_con_clima(nombre_ciudad)

        if ciudad is None:
            self.vista.mostrar_error("No se encontro la ciudad o no se pudieron obtener datos.")
            return

        self.vista.mostrar_ciudad_en_mapa(ciudad)

    def fbuscar_por_click(self, coordenadas):
        latitud, longitud = coordenadas

        ciudad = self.modelo.buscar_punto_con_clima(latitud, longitud)

        if ciudad is None:
            self.vista.mostrar_error("No se pudieron obtener datos para ese punto.")
            return

        self.vista.mostrar_ciudad_en_mapa(ciudad) #