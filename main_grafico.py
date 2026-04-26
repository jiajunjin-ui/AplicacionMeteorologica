import tkinter as tk
from view_ventana2 import ViewVentana2
from presenter_ventana2 import PresenterVentana2
from FacadeModel import FacadeModel


ventana2 = tk.Tk()
modelo = FacadeModel()
vista = ViewVentana2(ventana2)
PresenterVentana2(vista, modelo)
ventana2.mainloop()
