import tkinter as tk
from model import ModelFacade
from ventana2 import Ventana2
from presenter import Presenter

class main():
    # 1. Crear la ventana raíz de Tkinter
    ventana2 = tk.Tk()
    
    # 2. Instanciar los Modelos
    modelo = ModelFacade(None)

    # 3. Instanciar Vista de Tkinter
    vista = Ventana2(ventana2)

    # 4. Instanciar el Presenter 
    presenter = Presenter(vista, modelo)

    # 5. Iniciar bucle de eventos 
    ventana2.mainloop()
    
if __name__ == "__main__":
    main()