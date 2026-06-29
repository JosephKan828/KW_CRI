"""
Advanced Diagnosis Workflow for CRI Dispersion Relation Sensitivity Heatmaps.
Optimized using Xarray and Dask for lazy multi-dimensional operations.
"""

import argparse
import numpy as np
import seaborn as sns
import xarray as xr
from pathlib import Path
from matplotlib import pyplot as plt

def plot_combined_heatmaps(ds_sel, param_name, title, output_path):
    """
    Generate and save a (2, 3) heatmap for instability and phase speed.
    ds_sel must be a 2D Dataset with dimensions ('k', param_name) and mode coordinate.
    """
    plt.rcParams.update({
        "font.family": "serif",
        "mathtext.fontset": "cm"
    })
    fig, ax = plt.subplots(2, 3, figsize=(16, 7), dpi=150)
    
    mode_titles = ["Moisture Mode", "Convectively Coupled Wave", "Fast Gravity Wave"]
    
    x_ticks = ds_sel['k'].values
    y_ticks = ds_sel[param_name].values
    
    instab_data = ds_sel['instab'].transpose(param_name, 'k', 'mode').values
    pspeed_data = ds_sel['pspeed'].transpose(param_name, 'k', 'mode').values
    
    for i in range(3):
        # --- Top Row: Instability ---
        sns.heatmap(
            instab_data[..., i],
            ax=ax[0, i],
            annot=True,
            fmt=".2f", 
            cmap="coolwarm",
            vmin=-2.0, vmax=2.0,
            cbar=(i == 2),
            xticklabels=False,
            yticklabels=np.round(y_ticks, 2) if i == 0 else False
        )
        ax[0, i].invert_yaxis()
        ax[0, i].set_title(mode_titles[i] if i < len(mode_titles) else f"Mode {i}", fontsize=14, fontweight="bold")
        
        if i == 0:
            ax[0, i].set_ylabel(param_name, fontsize=14, fontweight="bold")
            
        if i == 2:
            cbar = ax[0, i].collections[0].colorbar
            cbar.set_label(r"Growth Rate ($\mathrm{day^{-1}}$)", fontsize=12)

        # --- Bottom Row: Phase Speed ---
        sns.heatmap(
            pspeed_data[..., i],
            ax=ax[1, i],
            annot=True,
            fmt=".2f", 
            cmap="coolwarm",
            vmin=-15.0, vmax=45.0, center=0.0,
            cbar=(i == 2),
            xticklabels=np.round(x_ticks, 1),
            yticklabels=np.round(y_ticks, 2) if i == 0 else False
        )
        ax[1, i].invert_yaxis()
        ax[1, i].set_xlabel(r"Non-dimensional Wavenumber $k$", fontsize=14)
        
        if i == 0:
            ax[1, i].set_ylabel(param_name, fontsize=14, fontweight="bold")
            
        if i == 2:
            cbar = ax[1, i].collections[0].colorbar
            cbar.set_label(r"Phase Speed ($\mathrm{m~s^{-1}}$)", fontsize=12)

    fig.suptitle(title, x=0.5, y=1.02, fontsize=16, fontweight="bold")
    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

def main():
    parser = argparse.ArgumentParser(description="Visualize dispersion relation sensitivities (Heatmap).")
    parser.add_argument("--c1", type=float, nargs="+", help="Phase speed of mode 1")
    parser.add_argument("--c2", type=float, nargs="+", help="Phase speed of mode 2")
    parser.add_argument("--scaling_factor", type=float, nargs="+", help="Scaling factor")
    parser.add_argument("--F", type=float, nargs="+", help="Bulk heating parameter")
    parser.add_argument("--f", type=float, nargs="+", help="Fraction of heating applied to first mode")
    parser.add_argument("--b1", type=float, nargs="+", help="Thermodynamic constant")
    parser.add_argument("--m1", type=float, nargs="+", help="Moisture coupling parameter for mode 1")
    parser.add_argument("--m2", type=float, nargs="+", help="Moisture coupling parameter for mode 2")
    parser.add_argument("--gamma_q", type=float, nargs="+", help="Moisture relaxation rate")
    parser.add_argument("--mode", type=str, choices=["full", "simplified"], default="full", help="Experiment mode")
    
    args = parser.parse_args()
    
    provided_params = {}
    for param in ["c1", "c2", "scaling_factor", "F", "f", "b1", "m1", "m2", "gamma_q"]:
        val = getattr(args, param)
        if val is not None:
            provided_params[param] = val
            
    keys = list(provided_params.keys())
    param_names = "_".join(keys) if keys else "default"
    
    data_dir = Path(f"/home/b11209013/KW_CRI/File/{param_names}_sensitivity_{args.mode}")
    fig_dir = Path(f"/home/b11209013/KW_CRI/Figure/{param_names}_sensitivity_{args.mode}")
    nc_path = data_dir / "dispersion_data.nc"
    
    if not nc_path.exists():
        print(f"NetCDF file {nc_path} not found. Did you run CRI_dispersion.py first? Exiting.")
        return
        
    print(f"Loading data from {nc_path}...")
    ds = xr.open_dataset(nc_path)
    
    varied_params = [k for k in keys if len(provided_params[k]) > 1]
    
    if len(varied_params) == 0:
        print("Need at least 2 parameter values for a heatmap. Exiting.")
        return
    elif len(varied_params) > 1:
        print(f"Warning: Multiple varied parameters found {varied_params}. Will use the first one {varied_params[0]} for heatmap y-axis.")
    
    target_param = varied_params[0]
    
    previous_values = {
        "F": [3.0, 4.0, 5.0],
        "f": [0.0, 0.25, 0.5, 0.75, 1.0],
        "m1": [-1.0, -0.5, 0.0, 0.5, 1.0],
        "c1": [0.8, 1.0, 1.2],
        "c2": [0.4, 0.5, 0.6],
        "scaling_factor": [0.0, 0.1, 0.5, 1.0, 2.0],
        "b1": [0.0, 1.0, 2.0, 3.0, 4.0],
        "m2": [-2.0, -1.0, 0.0, 1.0, 2.0],
        "gamma_q": [0.0, 0.25, 0.5, 0.7, 1.0]
    }
    
    if target_param in previous_values:
        # Find which of previous_values are actually in the dataset
        valid_vals = [v for v in previous_values[target_param] if np.any(np.isclose(ds[target_param].values, v))]
        if valid_vals:
            ds = ds.sel({target_param: valid_vals}, method='nearest')

    # Identify the target indices for the visualization grids
    target_k_vals = [1, 5, 10, 15, 20, 25, 30]
    ds_sel = ds.sel(k=target_k_vals, method='nearest')
    
    # If other varied parameters exist, slice them to a single value
    sel_dict = {}
    for p in varied_params[1:]:
        sel_dict[p] = provided_params[p][0]
    
    if sel_dict:
        ds_sel = ds_sel.sel(**sel_dict)
        
    ds_sel = ds_sel.squeeze()
    
    title = f"Dispersion Relation Sensitivity: {target_param}"
    if sel_dict:
        title += f" ({', '.join(f'{k}={v}' for k,v in sel_dict.items())})"
    
    output_path = fig_dir / f"sensitivity_heatmap.png"
    print(f"Generating Combined Heatmap for {target_param}...")
    
    plot_combined_heatmaps(ds_sel.compute(), target_param, title, output_path)
    print(f"Done! Figure saved to {output_path}")

if __name__ == "__main__":
    main()
