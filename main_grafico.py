import tkinter as tk

from Mapa import Mapa
from presenter_ventana2 import PresenterVentana2
from view_ventana2 import ViewVentana2


ventana = tk.Tk()
modelo = Mapa()
vista = ViewVentana2(ventana)
PresenterVentana2(vista, modelo)
ventana.mainloop()
