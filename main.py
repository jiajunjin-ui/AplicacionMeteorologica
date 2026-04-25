import tkinter as tk
from model import ModelFacade
from view_ventana2 import ViewVentana2
from presenter_ventana2 import PresenterVentana2

class main():
    # 1. Crear la ventana raíz de Tkinter
    ventana = tk.Tk()
    
    # 2. Instanciar los Modelos
    modelo = ModelFacade(None)

    # 3. Instanciar Vista de Tkinter
    vista = ViewVentana2(ventana)

    # 4. Instanciar el Presenter 
    presenter = PresenterVentana2(vista, modelo)

    # 5. Iniciar bucle de eventos 
    ventana.mainloop()
    
if __name__ == "__main__":
    main()