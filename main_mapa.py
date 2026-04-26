import tkinter as tk

from FacadeModel import FacadeModel
from Presenter import Presenter
from Ventana import TkView


ventana = tk.Tk()
modelo = FacadeModel()
vista = TkView(ventana)
Presenter(vista, modelo)
ventana.mainloop()#