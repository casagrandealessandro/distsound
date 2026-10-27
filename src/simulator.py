import numpy as np
import config as cfg
from radiation_model import calc_distances

def run_montecarlo(x_nom, y_nom, z_nom):
    """
    Eq 34, 35 e 36: Execution of Monte Carlo simulations for the perturbed field intensity.
    Note that faulty sensors are included in the simulation.
    """
    M = cfg.N_MONTECARLO
    # used to accumulate the intensity values from each Monte Carlo run
    U_sum = np.zeros_like(cfg.X_GRID, dtype=float)
    
    for i in range(M):
        # perturbation of sensor positions (Gaussian noise)
        x_pert = x_nom + np.random.normal(0, cfg.SIGMA_X, cfg.N_SENSORS)
        y_pert = y_nom + np.random.normal(0, cfg.SIGMA_Y, cfg.N_SENSORS)
        z_pert = z_nom + np.random.normal(0, cfg.SIGMA_Z, cfg.N_SENSORS)
        
        # faulty sensors: randomly select K_FAULTS sensors to be inactive
        active_mask = np.ones(cfg.N_SENSORS)
        if cfg.K_FAULTS > 0:
            faulty_idx = np.random.choice(cfg.N_SENSORS, cfg.K_FAULTS, replace=False)
            active_mask[faulty_idx] = 0
            
        # Eq 34 & 35 for each single run
        dist = calc_distances(x_pert, y_pert, z_pert)
        phases = np.exp(-1j * cfg.K_WAVE * dist)
        
        Psi_i = np.sum(phases * active_mask, axis=-1)
        U_i = np.abs(Psi_i)**2
        
        U_sum += U_i
        
    # Eq 36: enseble average over M runs
    U_mean_mc = U_sum / M
    return U_mean_mc