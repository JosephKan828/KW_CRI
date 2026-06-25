# KW_CRI: Coupled Thermodynamic Dispersion Relation

This repository contains the mathematical derivations, numerical solvers, and automated sensitivity testing framework for analyzing the dispersion relation of a coupled thermodynamic system. 

The primary objective is to investigate the linear instability and phase speed of the system's normal modes (Slow Mode, Intermediate Mode, and Fast Wave) under various physical parameter configurations.

## 🎯 Scientific Objective

The system consists of three prognostic equations for temperature ($T_1, T_2$) and moisture ($q$), along with diagnostic forcing terms. By projecting these variables onto normal mode plane wave solutions $(e^{i(\omega t - kx)})$, we formulate the system into a homogeneous matrix equation. 

The requirement that the determinant of this matrix equals zero yields a cubic dispersion relation in terms of the angular frequency $\omega$:

$$ \Gamma_{3}\omega^{3} + \Gamma_{2}\omega^{2} + \Gamma_{1}\omega + \Gamma_{0} = 0 $$

Solving this cubic equation for a given wavenumber $k$ yields three distinct wave modes:
1. **Slow Mode** (Moisture Mode)
2. **Intermediate Mode** (Convectively Coupled Waves)
3. **Fast Wave** (Fast Gravity Wave)

A complete step-by-step mathematical derivation of the $\Gamma$ coefficients and matrices is available in [`docs/CRI_dispersion_Relation.md`](docs/CRI_dispersion_Relation.md).

## 🚀 Repository Structure

* **`Code/`**: Contains the core Python physics scripts and the Bash automation pipeline.
  * **`CRI_dispersion.sh`**: The master execution script. This is the main entry point for running sensitivity experiments.
  * **`CRI_dispersion.py`**: The numerical solver that dynamically computes the roots of the dispersion relation for swept parameter grids.
  * **`visualize_sensitivity.py`**: A visualization suite that automatically generates 2x3 combined heatmaps (Instability & Phase Speed).
* **`docs/`**: Mathematical derivations and automated experiment logging (`logging.md`).
* **`File/`**: Dynamically generated `.npy` array files containing the raw roots computed during sensitivity sweeps.
* **`Figure/`**: Auto-generated heatmaps visualizing the sensitivity of phase speed and instability across different wavenumbers.

## 🛠️ Automated Sensitivity Workflow

This project features a fully automated, end-to-end parameter sweep pipeline. 

To run an experiment, simply modify the parameter lists at the top of `Code/CRI_dispersion.sh` (e.g., `gamma_q_LIST`, `f_LIST`, `m1_LIST`). 

Then execute the script:
```bash
cd Code/
./CRI_dispersion.sh "Testing moisture relaxation sensitivity"
```

**The Master Script will automatically:**
1. **Log the Experiment:** Append the timestamp, description, git commit hash, and swept parameters to `docs/logging.md`.
2. **Compute Physics:** Execute `CRI_dispersion.py` to calculate the dispersion relation across the parameter grid and save the `.npy` files to dynamically named folders in `File/`.
3. **Visualize:** Trigger `visualize_sensitivity.py` to ingest the newly generated arrays and output a unified `(2,3)` grid heatmap into the `Figure/` directory.
4. **Deploy:** Perform a silent, AI-assisted `git commit` (with a dynamically generated semantic commit message) and push the code, logs, arrays, and images to GitHub.

## 📊 Visualizations

The output of the pipeline is a consolidated `combined_sensitivity.png` heatmap consisting of:
- **Top Row:** Linear Instability of the Slow, Intermediate, and Fast modes.
- **Bottom Row:** Phase Speed of the Slow, Intermediate, and Fast modes.
- **Y-Axis:** The parameter values being swept.
- **X-Axis:** Sampled wavenumbers ($k$).