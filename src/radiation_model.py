import numpy as np
import config as cfg

def calc_distances(x_sens, y_sens, z_sens):
    """ Provides the euclidian distances from each sensor to each point on the grid """
    dist = np.sqrt(
        (cfg.X_GRID[..., np.newaxis] - x_sens)**2 +
        (cfg.Y_GRID[..., np.newaxis] - y_sens)**2 +
        (0 - z_sens)**2
    )
    return dist

def calc_intensity_nominal(x_sens, y_sens, z_sens):
    """ Eq 28 & 29: ideal intensity pattern of the field on the ground """
    dist = calc_distances(x_sens, y_sens, z_sens)
    
    # Eq 28: Sum of the complex contributions of the sensors
    # we neglect the term A_nm / d_nm(x,y) and consider only the phase contribution because for a given point
    # on the surface, the amplitude is identical for all sensors (distances are negligible), while the phase
    # gives a contribution that can be constructive or destructive
    Psi_nom = np.sum(np.exp(-1j * cfg.K_WAVE * dist), axis=-1)
    
    # Eq 29: Intensity (Power) = Square of the modulus
    U_nom = np.abs(Psi_nom)**2
    return U_nom

def calc_intensity_analytical(U_nom):
    """Approximate Eq. 37 average intensity for the current physical array model."""
    
    # Phase variance due to positional error.
    # f(sigma) = (k^2 / 4) * (sigma_x^2 + sigma_y^2 + 4*sigma_z^2)
    var_phi = (cfg.K_WAVE**2 / 4.0) * (cfg.SIGMA_X**2 + cfg.SIGMA_Y**2 + 4.0 * cfg.SIGMA_Z**2)
    
    # cos^2(theta) for each point on the 2D grid
    # theta is the off-nadir angle, cos(theta) = h/R
    dist_sq = cfg.X_GRID**2 + cfg.Y_GRID**2 + cfg.H_ALTITUDE**2
    cos_sq_theta = (cfg.H_ALTITUDE**2) / dist_sq
    
    # P_incoh(theta): incoherent component (Eq. 38) (omitting A^2 / h^2)
    P_incoh = cfg.N_SENSORS * cos_sq_theta
    
    # Perturbed-averaged pattern (Eq. 37 approximation).
    # U(theta) = P_incoh + exp(-f) * (U_nom - P_incoh)
    U_ana = P_incoh + np.exp(-var_phi) * (U_nom - P_incoh)
    
    return U_ana