import numpy as np
import config as cfg

def get_nominal_positions():
    """
    Computes the 3D nominal positions of the sensors. The array is centered with respect to the Nadir (0,0)
    """
    indices = np.arange(cfg.N_SENSORS) - (cfg.N_SENSORS - 1) / 2.0
    
    # The physical array is tilted in the across-track/along-track plane.
    x_nom = indices * cfg.D_ACT
    y_nom = indices * cfg.D_AT
    z_nom = np.full(cfg.N_SENSORS, cfg.H_ALTITUDE)
    
    return x_nom, y_nom, z_nom