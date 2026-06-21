import tkinter as tk 

class ViewBase(tk.Frame):
    """Clase Padre de las distintas Views"""
    def __init__(self, parent, mediador_view, titulo, size='400x300'):
        super().__init__(parent)
        self.mediador = mediador_view
        self.titulo = titulo 
        self.size = size 
        
        self.setup_ui()
    
    def setup_ui(self):
        pass