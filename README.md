# Distributed Radar Sounder Simulation

A simple Python simulator for studying how sensor-position errors and sensor failures affect a distributed radar sounder in formation flight.

The model is based on the distributed radar sounder concept described in the paper Carrer et al., IEEE TGRS 2019. It computes:

- the nominal radiation pattern;
- an analytical approximation of the perturbed average pattern;
- a Monte Carlo average with positional perturbations;
- Peak Power Loss (PPL) and Peak-to-Background Ratio (PBR).

The program prints the selected configuration and the PPL/PBR metrics, then displays the generated radiation-pattern plots.

## Configuration

Simulation parameters can be changed in `src/config.py`, including:

- sensor configuration (`trade_off` or `high_resolution`);
- position-error standard deviations;
- number of faulty sensors;
- number of Monte Carlo runs.