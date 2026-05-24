from model.ranking_strategy import RankingFactory


class PresenterRanking:
    """Presenter de la pestaña Ranking."""

    def __init__(self, view, model):
        self.vista = view
        self.modelo = model
        self.pais_seleccionado = None

        self.vista.btnBuscarPais.add_listener(self.f_buscar_pais)
        self.vista.btnSelectPais.add_listener(self.f_seleccionar_pais)
        self.vista.btnGenerarRanking.add_listener(self.f_generar_ranking)

    def f_buscar_pais(self):
        try:
            texto = self.vista.entrada()

            if not texto:
                self.vista.mensaje("Error", "Introduce un país para buscar.")
                return

            lista_paises = self.modelo.buscar_nombre_pais(texto)

            self.pais_seleccionado = None
            self.vista.actualizar_label_pais("ninguno")
            self.vista.limpiar_ranking()
            self.vista.salida_paises(lista_paises)

        except Exception as e:
            self.vista.mensaje("Error", str(e))

    def f_seleccionar_pais(self, nombre_pais):
        self.pais_seleccionado = nombre_pais

    def f_generar_ranking(self):
        try:
            if self.pais_seleccionado is None:
                self.vista.mensaje("Error", "Primero selecciona un país de la lista.")
                return

            tipo_ranking = self.vista.obtener_tipo_ranking()
            cantidad = self.vista.obtener_cantidad_ciudades()

            if cantidad <= 0:
                self.vista.mensaje("Error", "La cantidad de ciudades debe ser mayor que 0.")
                return

            pais = self.modelo.consultar_clima_actual_pais(
                self.pais_seleccionado,
                cantidad
            )

            estrategia = RankingFactory.crear(tipo_ranking)
            ciudades_ordenadas = estrategia.ordenar(pais.localidades)

            filas_ranking = self.crear_filas_ranking(ciudades_ordenadas)
            self.vista.mostrar_ranking(filas_ranking)

        except Exception as e:
            self.vista.mensaje("Error", str(e))

    def crear_filas_ranking(self, ciudades):
        filas = []

        for n, ciudad in enumerate(ciudades, start=1):
            fila = {
                "posicion": n,
                "ciudad": ciudad.nombre,
                "temperatura": f"{ciudad.parametros.temperatura:.2f}",
                "humedad": f"{ciudad.parametros.humedad:.2f}",
                "viento": f"{ciudad.parametros.viento:.2f}"
            }
            filas.append(fila)

        return filas
