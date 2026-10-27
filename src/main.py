import numpy as np
import matplotlib.pyplot as plt
import config as cfg
from array_geometry import get_nominal_positions
from radiation_model import calc_intensity_nominal, calc_intensity_analytical
from simulator import run_montecarlo
from performance_metrics import calc_ppl, calc_pbr, get_nadir_coords

def plot_heatmap(X, Y, U, title):
    plt.figure(figsize=(6, 4.5))
    U_db = 10 * np.log10(U / np.max(U))
    plt.pcolormesh(X / 1000, Y / 1000, U_db, shading='auto', cmap='jet', vmin=-30, vmax=0)
    plt.colorbar(label='Normalized power [dB]')
    plt.title(title)
    plt.xlabel("X [km] (across-track)")
    plt.ylabel("Y [km] (along-track)")
    plt.tight_layout()

def plot_1d_cut(x_vec, U_nom, U_mc, U_ana):
    """ 1D chart to evalueate ideal vs. Monte Carlo """
    iy, _ = get_nadir_coords() # cut on Y = 0
    
    plt.figure(figsize=(8, 5))
    
    # dB plot normalized at the nominal peak
    max_nom = np.max(U_nom[iy, :])
    
    plt.plot(x_vec / 1000, 10 * np.log10(U_nom[iy, :] / max_nom), 'k--', label='Nominal (Ideal)', linewidth=1.5)
    plt.plot(x_vec / 1000, 10 * np.log10(U_ana[iy, :] / max_nom), 'r-', label='Analytical (Eq. 41)', linewidth=2)
    plt.plot(x_vec / 1000, 10 * np.log10(U_mc[iy, :] / max_nom), 'b:', label='Monte Carlo (+ faults)', linewidth=2)
    
    plt.grid(True, which='both', linestyle='--', alpha=0.5)
    plt.title("Comparison of Radiation Patterns along the X-axis (Y=0)")
    plt.xlabel("Ground position X [km]")
    plt.ylabel("Measured power [dB]")
    plt.ylim([-35, 2])
    plt.legend()
    plt.tight_layout()

def main():
    print("--- Starting Simulation ---")
    x_nom, y_nom, z_nom = get_nominal_positions()

    print("Chosen configuration: {} ({} sensors)".format(cfg.SELECTED_CONFIG, cfg.N_SENSORS))
    
    print("Nominal Pattern Calculation...")
    U_nom = calc_intensity_nominal(x_nom, y_nom, z_nom)
    
    print("Analytical Average Approximation (Eq. 37)...")
    U_ana = calc_intensity_analytical(U_nom)
    
    print(f"Monte Carlo Simulation ({cfg.N_MONTECARLO} runs, {cfg.K_FAULTS} faults)...")
    U_mc = run_montecarlo(x_nom, y_nom, z_nom)
    
    # Metriche
    ppl_mc = calc_ppl(U_mc, U_nom)
    pbr_mc = calc_pbr(U_mc)
    
    print("\n--- Performance Metrics ---")
    print(f"Monte Carlo -> PPL (Peak Loss): {ppl_mc:.2f} dB")
    print(f"Monte Carlo -> PBR (Signal/Clutter): {pbr_mc:.2f} dB")
    
    # Plots
    plot_heatmap(cfg.X_GRID, cfg.Y_GRID, U_nom, "Nominal 2D pattern (Eq. 29)")
    plot_heatmap(cfg.X_GRID, cfg.Y_GRID, U_mc, "Monte Carlo 2D average")
    plot_1d_cut(cfg.x_vec, U_nom, U_mc, U_ana)
    
    plt.show()

if __name__ == "__main__":
    main()