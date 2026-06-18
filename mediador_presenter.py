from presenter_grafico import PresenterGrafico
from presenter_mapa import PresenterMapa
from presenter_inicio import PresenterInicio
from presenter_mapa_variables import PresenterMapaVariables

class MediadorPresenter:
    def __init__(self, mediador_view, model):
        self.mediador_vista = mediador_view
        self.modelo = model 

        self._dic_registros = {}
        self.presenter_actual = None

        # Registro de presenters ##########################
        self._registrar_presenter(PresenterGrafico, 'ViewGrafico')
        self._registrar_presenter(PresenterMapa, 'ViewMapa')
        self._registrar_presenter(PresenterInicio, 'ViewInicio')
        self._registrar_presenter(PresenterMapaVariables, 'ViewMapaVariables')
    
    def _registrar_presenter(self, clase_presenter, nombre_view):
        """Método que registra la clase del presenter y el nobre(str) del view associado"""
        nombre_presenter = clase_presenter.__name__
        self._dic_registros[nombre_presenter] = {
            'clase': clase_presenter,
            'vista': nombre_view
            }
    
    def cambiar_presenter(self, nombre_presenter):
        """Método empleado para cambiar e instanciar el presenter"""
        registro = self._dic_registros.get(nombre_presenter)
        if registro:
            nombre_view = registro['vista']
            self.mediador_vista.cambiar_frame_view(nombre_view)
            view_actual = self.mediador_vista.obtener_frame_view_actual()
            clase_presenter = registro['clase']
            instancia_presenter = clase_presenter(view_actual, self.modelo, self)
            self.presenter_actual = instancia_presenter
        else:
            raise KeyError(f'El presenter {nombre_presenter} no existe')
    
    def obtener_presenter_actual(self):
        """Método que devuelve la instancia del presenter actual"""
        return self.presenter_actual