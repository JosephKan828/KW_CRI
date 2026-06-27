import os
import sys
import argparse
import itertools
import multiprocessing
import numpy as np

from pathlib import Path
from matplotlib import pyplot as plt

sys.path.append("/home/b11209013/KW_CRI/src")
from parameter import WaveParameters
from calc_dispersion import compute_dispersion

def run_experiment(param_dict, output_fig_dir, output_data_dir):
    """
    Run dispersion calculation and generate plots for a given set of parameters.
    """
    # Create a string representation for the filename and title based on varying parameters
    # Format as key1=val1_key2=val2
    modification = "_".join([f"{k}={v}" for k, v in param_dict.items()])
    if not modification:
        modification = "default"
    
    title = rf"Sensitivity ({', '.join([f'{k}={v}' for k, v in param_dict.items()])})"
    
    # 1. Computation
    k_dis = np.linspace(0, 1e2, 10001)[1:]
    k_cal = 2 * np.pi * 4320 / 40000 * k_dis
    
    # Initialize parameters dynamically with the varying dictionary
    params = WaveParameters(**param_dict)
    
    # solve dispersion relation
    disp_rel = compute_dispersion(params, k_cal, [True, True, True, True])
    
    # Save Data
    os.makedirs(output_data_dir, exist_ok=True)
    np.save(os.path.join(output_data_dir, f"{modification}.npy"), disp_rel)
    
    # Calculate instability and phase speed
    instab: np.ndarray = -1*disp_rel.imag

    pspeed: np.ndarray = (disp_rel.real / k_cal[:, None]) * 50 
    
    sort_idx: np.ndarray = np.argsort(pspeed, axis=1)

    # 2. Visualization
    ls_list = ["-", "--", ":"]
    mode_labels = ["Moisture Mode", "Convectively Coupled Wave", "Fast Gravity Wave"]
    
    plt.rcParams.update({"font.family": "serif"})
    fig, ax = plt.subplots(1, 2, figsize=(18, 4), dpi=150)
    
    # --- Subplot 1: Growth Rate ---
    for i in range(disp_rel.shape[1]):
        if i < len(ls_list):
            ax[0].plot(k_dis, instab[:, i][sort_idx[:, i]], color="k", linestyle=ls_list[i], 
                       linewidth=2.5, label=mode_labels[i] if i < len(mode_labels) else f"Mode {i}")
            
    ax[0].axhline(0, color="k", linestyle="-", linewidth=1, alpha=0.5) 
    ax[0].set_xlim(0, 30)
    ax[0].set_ylabel("Growth Rate (day$^{-1}$)", fontsize=13)
    ax[0].set_title("Linear Instability", fontsize=14, fontweight="bold")
    ax[0].grid(True, linestyle=":", alpha=0.7)
    ax[0].legend(loc="upper right", frameon=True, fontsize=11)
    ax[0].tick_params(axis='both', labelsize=11)
    
    # --- Subplot 2: Phase Speed ---
    for i in range(disp_rel.shape[1]):
        if i < len(ls_list):
            ax[1].plot(k_dis, pspeed[:, i][sort_idx[:, i]], color="k", linestyle=ls_list[i], linewidth=2.5)

    ax[1].set_ylabel("Phase Speed (m/s)", fontsize=13)
    ax[1].set_title("Phase Speed", fontsize=14, fontweight="bold")
    ax[1].set_xlabel("Non-dimensional Wavenumber $k$", fontsize=13)
    ax[1].grid(True, linestyle=":", alpha=0.7)
    ax[1].tick_params(axis='both', labelsize=11)
    ax[1].set_xlim(0, 30)
    
    plt.suptitle(title, fontsize=16, fontweight="bold")
    
    os.makedirs(os.path.join(output_fig_dir, f"single/"), exist_ok=True)
    plt.savefig(os.path.join(output_fig_dir, f"single/{modification}.png"), dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Finished processing for {modification}")

def run_single_experiment_wrapper(args):
    exp_dict, fig_dir, data_dir = args
    try:
        run_experiment(exp_dict, fig_dir, data_dir)
    except Exception as e:
        print(f"Experiment {exp_dict} failed with exception: {e}")

def main():
    parser = argparse.ArgumentParser(description="Systematically test sensitivity of dispersion relation over multiple parameters.")
    
    # Add parameter arguments taking multiple values to support grid search
    parser.add_argument("--c1", type=float, nargs="+", help="Phase speed of mode 1")
    parser.add_argument("--c2", type=float, nargs="+", help="Phase speed of mode 2")
    parser.add_argument("--scaling_factor", type=float, nargs="+", help="Scaling factor")
    parser.add_argument("--F", type=float, nargs="+", help="Bulk heating parameter")
    parser.add_argument("--f", type=float, nargs="+", help="Fraction of heating applied to first mode")
    parser.add_argument("--b1", type=float, nargs="+", help="Thermodynamic constant")
    parser.add_argument("--m1", type=float, nargs="+", help="Moisture coupling parameter for mode 1")
    parser.add_argument("--m2", type=float, nargs="+", help="Moisture coupling parameter for mode 2")
    parser.add_argument("--gamma_q", type=float, nargs="+", help="Moisture relaxation rate")
    
    
    args = parser.parse_args()
    
    # Extract only parameters that were provided by user
    # WaveParameters defaults will be used for any parameter not provided
    param_grids = {}
    for param in ["c1", "c2", "scaling_factor", "F", "f", "b1", "m1", "m2", "gamma_q"]:
        val = getattr(args, param)
        if val is not None:
            param_grids[param] = val
            
    # If no parameters are provided, itertools.product will naturally generate 
    # a single empty dictionary, which triggers the default WaveParameters()

    # Generate Cartesian product of all provided parameter grids
    keys = list(param_grids.keys())
    values_product = list(itertools.product(*[param_grids[k] for k in keys]))
    
    # Convert back to list of dictionaries for each experiment
    experiments = [dict(zip(keys, values)) for values in values_product]
    
    print(f"Total experiments to run: {len(experiments)} sequentially.")
    
    # form figure directory and data directory
    param_names = "_".join(keys) if keys else "default"
    fig_dir : Path = Path(f"/home/b11209013/KW_CRI/Figure/{param_names}_sensitivity")
    data_dir: Path = Path(f"/home/b11209013/KW_CRI/File/{param_names}_sensitivity")

    os.makedirs(fig_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)
    

    # Execute in parallel
    print(f"Starting parallel execution using {multiprocessing.cpu_count()} cores...")
    args_list = [(exp, fig_dir, data_dir) for exp in experiments]
    with multiprocessing.Pool(8) as pool:
        pool.map(run_single_experiment_wrapper, args_list)
            
    print("All sensitivity experiments completed.")

if __name__ == "__main__":
    main()
