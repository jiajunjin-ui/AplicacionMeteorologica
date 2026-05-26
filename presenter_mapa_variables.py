import numpy as np
from scipy.interpolate import griddata

class PresenterMapaVariables:
    def __init__(self, view, model, mediador_presenter=None):
        self.vista = view
        self.modelo = model
        self.mediador = mediador_presenter

        # Suscripción a las señales de la vista
        self.vista.btnBuscar.add_listener(self.f_actualizar_mapa)
    
    def f_actualizar_mapa(self):
        try:
            text_in = self.vista.entrada()
            pais_localidad = self.modelo.malla_clima_actual_pais(text_in)
            
            temps = pais_localidad.parametros.temperatura
            lats = pais_localidad.lat
            lons = pais_localidad.lon
            lons_array = np.array(lons)
            lats_array = np.array(lats)
            coords = []
            for i in range(len(lons)):
                coords.append([lons[i], lats[i]])
            
             # Establecer límites #######################################################
            lon_min, lon_max = lons_array.min(), lons_array.max()
            lat_min, lat_max = lats_array.min(), lats_array.max()
        
             # Malla Interpoladora ######################################################
            grid_x, grid_y = np.mgrid[lon_min:lon_max:180j,
                                      lat_min:lat_max:180j]
            grid_z = griddata(coords, temps, (grid_x, grid_y), method='cubic')
            
            self.vista.actualizar_mapa(lons_array, lats_array,
                                       lon_min, lon_max,
                                       lat_min, lat_max,  
                                       grid_x, grid_y, grid_z)
        except Exception as e:
            self.vista.mensaje('Error', str(e))