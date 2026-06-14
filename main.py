import tkinter as tk
from model import AppMeteo
from mediador_view import MediadorView
from mediador_presenter import MediadorPresenter

class main():
    ventana = tk.Tk()
    ventana.resizable(False, False)

    modelo = AppMeteo()

    mediador_view = MediadorView(ventana)
    mediador_presenter = MediadorPresenter(mediador_view, modelo)

    mediador_presenter.cambiar_presenter('PresenterInicio')
    mediador_presenter.obtener_presenter_actual()
    ventana.mainloop()
 
if __name__ == "__main__":
    main()