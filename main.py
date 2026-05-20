import tkinter as tk
from model import AppMeteo
<<<<<<< HEAD
from view_grafico import ViewGrafico
from presenter_grafico import PresenterGrafico
from view_mapa import ViewMapa
from presenter_mapa import PresenterMapa
=======
from mediador_view import MediadorView
from mediador_presenter import MediadorPresenter

>>>>>>> feature/Siatema_pantallas

class main():
    ventana = tk.Tk()
    ventana.resizable(False, False)
    modelo = AppMeteo()
<<<<<<< HEAD
    #vista = ViewGrafico(ventana)
    #presenter = PresenterGrafico(vista, modelo)
    vista = ViewMapa(ventana)
    presenter = PresenterMapa(vista, modelo)
=======
    mediador_view = MediadorView(ventana)
    mediador_presenter = MediadorPresenter(mediador_view, modelo)

    mediador_presenter.cambiar_presenter('PresenterInicio')
    mediador_presenter.obtener_presenter_actual()

>>>>>>> feature/Siatema_pantallas
    ventana.mainloop()
if __name__ == "__main__":
    main()