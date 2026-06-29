"""
Advanced Diagnosis Workflow for CRI Dispersion Relation Sensitivity Contours.
Optimized using Xarray and Dask for lazy multi-dimensional operations.
"""

import argparse
from matplotlib.colors import TwoSlopeNorm
import numpy as np
import xarray as xr
from pathlib import Path
from matplotlib import pyplot as plt

def plot_combined_contours(ds_sel, param_name, title, output_path):
    """
    Generate and save a (2, 3) contour plot for instability and phase speed.
    ds_sel must be a 2D Dataset with dimensions ('k', param_name) and mode coordinate.
    """
    plt.rcParams.update({
        "font.family": "serif", 
        "mathtext.fontset": "cm",
        "axes.labelsize": 13,
        "axes.titlesize": 14,
        "legend.fontsize": 11,
        "xtick.labelsize": 11,
        "ytick.labelsize": 11
    })
    
    fig, ax = plt.subplots(2, 3, figsize=(18, 7), dpi=150)
    mode_titles = ["Moisture Mode", "Convectively Coupled Wave", "Fast Gravity Wave"]
    
    k_plot = ds_sel['k'].values
    y_plot = ds_sel[param_name].values
    X, Y = np.meshgrid(k_plot, y_plot)
    
    # Extract data as numpy arrays for contouring, transpose to match meshgrid (param, k)
    instab_data = ds_sel['instab'].transpose(param_name, 'k', 'mode').values
    pspeed_data = ds_sel['pspeed'].transpose(param_name, 'k', 'mode').values
    
    for i in range(3):
        # --- Top Row: Instability ---
        cf_instab = ax[0, i].contourf(
            X, Y, instab_data[..., i],
            levels=np.linspace(-2, 2, 21),
            cmap="RdBu_r",
            norm=TwoSlopeNorm(vcenter=0),
            extend="both"
        )
        
        c_instab_lines = ax[0, i].contour(
            X, Y, instab_data[..., i],
            levels=np.arange(-2.0, 2.1, 0.25),
            colors="k",
            linewidths=2,
            alpha=0.6
        )
        ax[0, i].clabel(c_instab_lines, inline=True, fontsize=10)
        ax[0, i].set_title(mode_titles[i] if i < len(mode_titles) else f"Mode {i}", fontsize=14, fontweight="bold")
        
        if i == 0:
            ax[0, i].set_ylabel(param_name, fontsize=14, fontweight="bold")
        else:
            ax[0, i].set_yticks([])
            
        if i == 2:
            cbar = fig.colorbar(cf_instab, ax=ax[0, i], orientation="vertical", shrink=0.8, aspect=40)
            cbar.set_ticks([-2, -1, 0, 1, 2])
            cbar.set_label(r"Growth Rate ($\mathrm{day^{-1}}$)", fontsize=12)

        # --- Bottom Row: Phase Speed ---
        cf_pspeed = ax[1, i].contourf(
            X, Y, pspeed_data[..., i],
            levels=np.linspace(-10, 50, 21),
            cmap="RdBu_r",
            norm=TwoSlopeNorm(vcenter=0),
            extend="both"
        )
        
        c_pspeed_lines = ax[1, i].contour(
            X, Y, pspeed_data[..., i],
            levels=np.arange(-10, 51, 5),
            colors="k",
            linewidths=2,
            alpha=0.6
        )
        ax[1, i].clabel(c_pspeed_lines, inline=True, fontsize=10)
        ax[1, i].set_xlabel(r"Non-dimensional Wavenumber $k$", fontsize=14)

        if i == 0:
            ax[1, i].set_ylabel(param_name, fontsize=14, fontweight="bold")
        else:
            ax[1, i].set_yticks([])

        if i == 2:
            cbar = fig.colorbar(cf_pspeed, ax=ax[1, i], orientation="vertical", shrink=0.8, aspect=40)
            cbar.set_ticks([-10, 0, 10, 20, 30, 40, 50])
            cbar.set_label(r"Phase Speed ($\mathrm{m~s^{-1}}$)", fontsize=12)

    fig.suptitle(title, x=0.5, y=1.02, fontsize=16, fontweight="bold")
    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

def main():
    parser = argparse.ArgumentParser(description="Visualize dispersion relation sensitivities (Contour).")
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
        print("Need at least 2 parameter values for a contour plot. Exiting.")
        return
    elif len(varied_params) > 1:
        print(f"Warning: Multiple varied parameters found {varied_params}. Will use the first one {varied_params[0]} for contour y-axis.")
    
    target_param = varied_params[0]
    
    # Filter wavenumbers for the visualization (up to k=30)
    target_k_max = 30
    ds_sel = ds.sel(k=slice(None, target_k_max))
    
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
    
    output_path = fig_dir / f"sensitivity_contour_{target_param}.png"
    print(f"Generating Combined Contour Plot for {target_param}...")
    
    # Evaluate lazily loaded data and plot
    plot_combined_contours(ds_sel.compute(), target_param, title, output_path)
    print(f"Done! Figure saved to {output_path}")

if __name__ == "__main__":
    main()
