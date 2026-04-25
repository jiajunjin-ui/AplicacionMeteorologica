class Presenter:
    """Actua como puente entre la logica y la pantalla."""

    def __init__(self, view, model):
        self.vista = view
        self.modelo = model

        self.vista.btn_buscar.add_listener(self.fbuscar)
        self.vista.btn_temp.add_listener(self.ftemp)
        self.vista.btn_cielo.add_listener(self.fcielo)
        self.vista.btn_ranking.add_listener(self.franking)

    def fbuscar(self):
        nombre_ciudad = self.vista.obtener_ciudad_buscada()

        if not nombre_ciudad:
            self.vista.mostrar_error("Introduce una ciudad para buscar.")
            return

        ciudad = self.modelo.buscar_ciudad_con_clima(nombre_ciudad)

        if ciudad is None:
            self.vista.mostrar_error(
                "No se encontro la ciudad o no se pudieron obtener datos."
            )
            return

        self.vista.mostrar_ciudad_en_mapa(ciudad)

    def ftemp(self):
        self.vista.mostrar_error("Funcion aun no implementada.")

    def fcielo(self):
        self.vista.mostrar_error("Funcion aun no implementada.")

    def franking(self):
        self.vista.mostrar_error("Funcion aun no implementada.")
