import tkinter as tk
from model import AppMeteo
from view_grafico import ViewGrafico
from presenter_grafico import PresenterGrafico


class main():
    ventana = tk.Tk()
    modelo = AppMeteo()
    vista = ViewGrafico(ventana)
    presenter = PresenterGrafico(vista, modelo)
    ventana.mainloop()
 
if __name__ == "__main__":
    main()