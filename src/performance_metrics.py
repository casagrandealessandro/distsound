import numpy as np
import config as cfg

def get_nadir_coords():
    """ Find the index of the matrix closest to the center (0,0) """
    idx_x = np.argmin(np.abs(cfg.x_vec - 0))
    idx_y = np.argmin(np.abs(cfg.y_vec - 0))
    return idx_y, idx_x

def calc_ppl(U_perturbed, U_nom):
    """ Eq 42: Peak Power Loss metric in dB """
    iy, ix = get_nadir_coords()
    ppl = U_perturbed[iy, ix] / U_nom[iy, ix]
    return 10 * np.log10(ppl)

def calc_pbr(U_perturbed):
    """Approximate Eq. 43 at half the first grating-lobe angle, in dB."""
    iy, ix = get_nadir_coords()

    # Evaluate the background around the paper's reference angle theta_g / 2.
    distance_from_center = np.sqrt(cfg.X_GRID**2 + cfg.Y_GRID**2)
    theta_g = np.arcsin(cfg.LAMBDA / cfg.D_ACT)
    background_radius = cfg.H_ALTITUDE * np.tan(theta_g / 2.0)
    grid_spacing = max(np.diff(cfg.x_vec).mean(), np.diff(cfg.y_vec).mean())
    background_mask = np.abs(distance_from_center - background_radius) <= grid_spacing
    
    pbr = U_perturbed[iy, ix] / np.mean(U_perturbed[background_mask])
    return 10 * np.log10(pbr)