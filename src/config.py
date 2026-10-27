import numpy as np

C = 3e8                        # speed of light in vacuum [m/s]

# Configuration table (trade-off vs high-resolution)
# values taken from Table II in the paper
CONFIGURATIONS = {
    "trade_off": {
        "N_SENSORS": 21,
        "D_AT": 28.87,         # along-track spacing [m]
        "D_ACT": 28.67,        # across-track spacing [m]
    },
    "high_resolution": {
        "N_SENSORS": 65,
        "D_AT": 28.37,
        "D_ACT": 28.67,
    }
}


# --- Configuration parameters ---

SELECTED_CONFIG = "trade_off"

cfg_active = CONFIGURATIONS[SELECTED_CONFIG]
N_SENSORS = cfg_active["N_SENSORS"]
D_AT = cfg_active["D_AT"]
D_ACT = cfg_active["D_ACT"]

H_ALTITUDE = 500e3           # orbit altitude [m]
FREQ = 45e6                  # frequency [Hz]
LAMBDA = C / FREQ            # wavelength [m] ~ 6.66 m
K_WAVE = 2 * np.pi / LAMBDA  # wave number [rad/m]


# --- Orbit perturbation parameters for the Monte Carlo simulation ---

SIGMA_X = 0.0                # standard deviations of the positional errors
SIGMA_Y = 0.0
SIGMA_Z = LAMBDA / 10.0
K_FAULTS = 0                 # amount of faulty sensors
N_MONTECARLO = 500           # number of Monte Carlo runs


# --- Simulation surface grid ---

GRID_POINTS = 201
# Region containing the first grating lobe for the selected formation
X_MIN, X_MAX = -120000, 120000
Y_MIN, Y_MAX = -120000, 120000

x_vec = np.linspace(X_MIN, X_MAX, GRID_POINTS)
y_vec = np.linspace(Y_MIN, Y_MAX, GRID_POINTS)
X_GRID, Y_GRID = np.meshgrid(x_vec, y_vec)