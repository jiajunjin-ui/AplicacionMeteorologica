import tkinter as tk
import tkinter.messagebox
from tkinter import ttk

from model import Event


class ViewRanking:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Ranking")
        self.ventana.geometry("960x560")

        self.lista_btn_paises = []

        self.btnBuscarPais = Event()
        self.btnSelectPais = Event()
        self.btnGenerarRanking = Event()

        self.setup_ui()

    def setup_ui(self):
        """VENTANA PRINCIPAL TIENE DOS COLUMNAS: IZQUIERDA (CONTROLES) - DERECHA (RANKING)"""
        self.ventana.grid_columnconfigure(0, weight=1)
        self.ventana.grid_columnconfigure(1, weight=3)
        self.ventana.grid_rowconfigure(0, weight=1)

        # COLUMNA IZQUIERDA
        self.columna_izq = tk.Frame(self.ventana, padx=10, pady=10)
        self.columna_izq.grid(row=0, column=0, sticky="nsew")

        tk.Label(self.columna_izq, text="Introduce un país:").grid(row=0, column=0, sticky="w")

        self.entrada_pais = tk.Entry(self.columna_izq, width=25)
        self.entrada_pais.grid(row=1, column=0, sticky="ew")

        self.btn_buscar_pais = tk.Button(
            self.columna_izq,
            text="Buscar país",
            command=self.actualizar_lista_paises
        )
        self.btn_buscar_pais.grid(row=2, column=0, pady=5, sticky="ew")

        self.label_pais_seleccionado = tk.Label(
            self.columna_izq,
            text="País seleccionado: ninguno"
        )
        self.label_pais_seleccionado.grid(row=3, column=0, sticky="w", pady=(10, 0))

        tk.Label(self.columna_izq, text="Cantidad de ciudades:").grid(row=4, column=0, sticky="w", pady=(10, 0))

        self.entry_cantidad = tk.Entry(self.columna_izq, width=25)
        self.entry_cantidad.insert(0, "10")
        self.entry_cantidad.grid(row=5, column=0, sticky="ew", pady=5)

        tk.Label(self.columna_izq, text="Tipo de ranking:").grid(row=6, column=0, sticky="w", pady=(10, 0))

        self.combo_tipo = ttk.Combobox(
            self.columna_izq,
            values=[
                "Más calurosas",
                "Más frías",
                "Más viento",
                "Más humedad"
            ],
            state="readonly"
        )
        self.combo_tipo.current(0)
        self.combo_tipo.grid(row=7, column=0, sticky="ew", pady=5)

        self.btn_generar = tk.Button(
            self.columna_izq,
            text="Generar ranking",
            command=self.generar_ranking
        )
        self.btn_generar.grid(row=8, column=0, pady=5, sticky="ew")

        self.columna_izq.grid_columnconfigure(0, weight=1)

        # COLUMNA DERECHA
        self.columna_der = tk.Frame(self.ventana, padx=10, pady=10)
        self.columna_der.grid(row=0, column=1, sticky="nsew")
        self.columna_der.grid_rowconfigure(1, weight=1)
        self.columna_der.grid_columnconfigure(0, weight=1)

        self.label_titulo_ranking = tk.Label(
            self.columna_der,
            text="Ranking de ciudades más pobladas del país",
            font=("Arial", 12, "bold")
        )
        self.label_titulo_ranking.grid(row=0, column=0, sticky="w", pady=(0, 10))

        columnas = ("posicion", "ciudad", "temperatura", "humedad", "viento")
        self.tabla = ttk.Treeview(
            self.columna_der,
            columns=columnas,
            show="headings"
        )

        self.tabla.heading("posicion", text="#")
        self.tabla.heading("ciudad", text="Ciudad")
        self.tabla.heading("temperatura", text="Temp. °C")
        self.tabla.heading("humedad", text="Humedad %")
        self.tabla.heading("viento", text="Viento km/h")

        self.tabla.column("posicion", width=50, anchor="center")
        self.tabla.column("ciudad", width=220)
        self.tabla.column("temperatura", width=110, anchor="center")
        self.tabla.column("humedad", width=110, anchor="center")
        self.tabla.column("viento", width=120, anchor="center")

        self.tabla.grid(row=1, column=0, sticky="nsew")

        self.scroll_tabla = ttk.Scrollbar(
            self.columna_der,
            orient="vertical",
            command=self.tabla.yview
        )
        self.tabla.configure(yscrollcommand=self.scroll_tabla.set)
        self.scroll_tabla.grid(row=1, column=1, sticky="ns")

    def entrada(self):
        return self.entrada_pais.get().strip()

    def obtener_tipo_ranking(self):
        return self.combo_tipo.get()

    def obtener_cantidad_ciudades(self):
        return int(self.entry_cantidad.get())

    def actualizar_lista_paises(self):
        self.btnBuscarPais.emit()

    def salida_paises(self, lista_paises):
        self.limpiar_lista_paises()

        for n, nombre_pais in enumerate(lista_paises):
            boton = tk.Button(
                self.columna_izq,
                text=nombre_pais,
                command=lambda pais=nombre_pais: self.seleccionar_pais(pais)
            )
            boton.grid(row=n + 9, column=0, pady=5, sticky="ew")
            self.lista_btn_paises.append(boton)

    def seleccionar_pais(self, nombre_pais):
        self.actualizar_label_pais(nombre_pais)
        self.btnSelectPais.emit(nombre_pais)
        self.limpiar_lista_paises()

    def actualizar_label_pais(self, nombre_pais):
        self.label_pais_seleccionado.config(
            text=f"País seleccionado: {nombre_pais}"
        )

    def limpiar_lista_paises(self):
        for boton in self.lista_btn_paises:
            boton.destroy()
        self.lista_btn_paises.clear()

    def generar_ranking(self):
        self.btnGenerarRanking.emit()

    def limpiar_ranking(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

    def mostrar_ranking(self, filas_ranking):
        self.limpiar_ranking()

        for fila in filas_ranking:
            self.tabla.insert(
                "",
                "end",
                values=(
                    fila["posicion"],
                    fila["ciudad"],
                    fila["temperatura"],
                    fila["humedad"],
                    fila["viento"]
                )
            )

    def mensaje(self, prompt, txt):
        tk.messagebox.showerror(prompt, txt)


if __name__ == "__main__":
    ventana = tk.Tk()
    vista = ViewRanking(ventana)
    ventana.mainloop()
