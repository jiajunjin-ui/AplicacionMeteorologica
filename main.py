import tkinter as tk
from model import AppMeteo
from view_grafico import ViewGrafico
from presenter_grafico import PresenterGrafico
from view_mapa import ViewMapa
from presenter_mapa import PresenterMapa
from view_ranking import ViewRanking
from presenter_ranking import PresenterRanking

class main():
    ventana = tk.Tk()
    modelo = AppMeteo()
    #vista = ViewGrafico(ventana)
    #presenter = PresenterGrafico(vista, modelo)
    #vista = ViewMapa(ventana)
    #presenter = PresenterMapa(vista, modelo)
    vista = ViewRanking(ventana)
    presenter = PresenterRanking(vista, modelo)
    ventana.mainloop()
 
if __name__ == "__main__":
    main()