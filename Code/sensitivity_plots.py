"""
Advanced Diagnosis Workflow for CRI Dispersion Relation Sensitivity Plots.
Optimized using Xarray and Dask for lazy multi-dimensional operations.
Generates both Contour and Heatmap visualizations.
"""

import argparse
from matplotlib.colors import TwoSlopeNorm
import numpy as np
import seaborn as sns
import xarray as xr
from pathlib import Path
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker

def plot_combined_contours(ds_sel, param_name, title, output_path):
    """
    Generate and save a (2, 3) contour plot for instability and phase speed.
    ds_sel must be a 2D Dataset with dimensions ('k', param_name) and mode coordinate.
    Automatically handles NaNs and aligns dimensions via Xarray native plotting.
    """
    plt.rcParams.update({
        "font.family": "serif", 
        "mathtext.fontset": "cm",
        "axes.labelsize": 14,
        "axes.titlesize": 15,
        "legend.fontsize": 12,
        "xtick.labelsize": 12,
        "ytick.labelsize": 12,
        "xtick.direction": "in",
        "ytick.direction": "in",
        "xtick.top": True,
        "ytick.right": True,
        "axes.linewidth": 1.2
    })
    
    num_modes = ds_sel.sizes['mode']
    fig, ax = plt.subplots(2, num_modes, figsize=(6 * num_modes, 7.5), dpi=150, squeeze=False)
    mode_titles = ["Slow Mode", "Intermediate Mode", "Fast Mode"]
    
    for i in range(num_modes):
        # Extract robust dimension-aligned DataArrays for the specific mode
        da_instab = ds_sel['instab'].isel(mode=i)
        da_pspeed = ds_sel['pspeed'].isel(mode=i)
        
        # --- Top Row: Instability ---
        cf_instab = da_instab.plot.contourf(
            ax=ax[0, i],
            x='k', y=param_name,
            levels=np.linspace(-2, 2, 21),
            cmap="RdBu_r",
            norm=TwoSlopeNorm(vmin=-2, vcenter=0, vmax=2),
            extend="both",
            add_colorbar=False
        )
        
        c_instab_lines = da_instab.plot.contour(
            ax=ax[0, i],
            x='k', y=param_name,
            levels=np.arange(-2.0, 2.1, 0.25),
            colors="k",
            linewidths=1.2,
            alpha=0.6,
            add_colorbar=False
        )
        ax[0, i].clabel(c_instab_lines, inline=True, fontsize=10, fmt="%.2f")
        ax[0, i].set_title(mode_titles[i] if i < len(mode_titles) else f"Mode {i}", fontsize=15, fontweight="bold")
        
        ax[0, i].minorticks_on()
        ax[0, i].set_xlabel("")
        
        if i == 0:
            ax[0, i].set_ylabel("Instability", fontsize=14, fontweight="bold")
        else:
            ax[0, i].set_ylabel("")
            ax[0, i].set_yticklabels([])
            
        if i == num_modes - 1:
            cbar = fig.colorbar(cf_instab, ax=ax[0, i], orientation="vertical", shrink=0.85, aspect=30, pad=0.04)
            cbar.set_ticks([-2, -1, 0, 1, 2])
            cbar.set_label(r"Growth Rate ($\mathrm{day^{-1}}$)", fontsize=13)
            cbar.ax.tick_params(direction="in")

        # --- Bottom Row: Phase Speed ---
        cf_pspeed = da_pspeed.plot.contourf(
            ax=ax[1, i],
            x='k', y=param_name,
            levels=np.linspace(-10, 50, 21),
            cmap="BrBG",
            norm=TwoSlopeNorm(vmin=-10, vcenter=0, vmax=50),
            extend="both",
            add_colorbar=False
        )
        
        c_pspeed_lines = da_pspeed.plot.contour(
            ax=ax[1, i],
            x='k', y=param_name,
            levels=np.arange(-10, 51, 5),
            colors="k",
            linewidths=1.2,
            alpha=0.6,
            add_colorbar=False
        )
        ax[1, i].clabel(c_pspeed_lines, inline=True, fontsize=10, fmt="%d")
        
        ax[1, i].minorticks_on()
        ax[1, i].set_xlabel(r"Non-dimensional Wavenumber $k$", fontsize=14)
        ax[1, i].set_title("")

        if i == 0:
            ax[1, i].set_ylabel("Phase Speed", fontsize=14, fontweight="bold")
        else:
            ax[1, i].set_ylabel("")
            ax[1, i].set_yticklabels([])

        if i == num_modes - 1:
            cbar = fig.colorbar(cf_pspeed, ax=ax[1, i], orientation="vertical", shrink=0.85, aspect=30, pad=0.04)
            cbar.set_ticks([-10, 0, 10, 20, 30, 40, 50])
            cbar.set_label(r"Phase Speed ($\mathrm{m~s^{-1}}$)", fontsize=13)
            cbar.ax.tick_params(direction="in")

    fig.suptitle(title, x=0.5, y=1.02, fontsize=17, fontweight="bold")
    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

def plot_combined_heatmaps(ds_sel, param_name, title, output_path):
    """
    Generate and save a (2, 3) heatmap for instability and phase speed.
    ds_sel must be a 2D Dataset with dimensions ('k', param_name) and mode coordinate.
    Automatically handles dimensional alignment via transposing and NaN masking natively.
    """
    plt.rcParams.update({
        "font.family": "serif",
        "mathtext.fontset": "cm",
        "axes.labelsize": 14,
        "axes.titlesize": 15,
        "xtick.labelsize": 12,
        "ytick.labelsize": 12,
        "axes.linewidth": 1.2
    })
    num_modes = ds_sel.sizes['mode']
    fig, ax = plt.subplots(2, num_modes, figsize=(6 * num_modes, 7.5), dpi=150, squeeze=False)
    
    mode_titles = ["Slow Mode", "Intermediate Mode", "Fast Mode"]
    
    for i in range(num_modes):
        # Extract robust dimension-aligned DataFrames for the specific mode
        # Transpose guarantees k is row (x-axis after .T) and param_name is col (y-axis after .T)
        da_instab = ds_sel['instab'].isel(mode=i).transpose('k', param_name)
        da_pspeed = ds_sel['pspeed'].isel(mode=i).transpose('k', param_name)
        
        df_instab = da_instab.to_pandas().T
        df_pspeed = da_pspeed.to_pandas().T
        
        # --- Top Row: Instability ---
        sns.heatmap(
            df_instab,
            ax=ax[0, i],
            annot=True,
            fmt=".2f", 
            cmap="RdBu_r",
            vmin=-2.0, vmax=2.0, center=0,
            cbar=(i == num_modes - 1),
            xticklabels=False,
            yticklabels=True if i == 0 else False,
            linewidths=0.5,
            linecolor='lightgray',
            cbar_kws={'label': r"Growth Rate ($\mathrm{day^{-1}}$)"} if i == num_modes - 1 else None
        )
        ax[0, i].invert_yaxis()
        ax[0, i].set_title(mode_titles[i] if i < len(mode_titles) else f"Mode {i}", fontsize=15, fontweight="bold")
        
        for _, spine in ax[0, i].spines.items():
            spine.set_visible(True)
            spine.set_linewidth(1.2)
            
        ax[0, i].tick_params(direction="in", top=True, right=True, left=True, bottom=True)
        ax[0, i].set_xlabel("")
        
        if i == 0:
            ax[0, i].set_ylabel("Instability", fontsize=14, fontweight="bold")
            ax[0, i].set_yticklabels([f"{float(t.get_text()):.2f}" for t in ax[0, i].get_yticklabels()])
        else:
            ax[0, i].set_ylabel("")

        if i == num_modes - 1:
            cbar = ax[0, i].collections[0].colorbar
            cbar.ax.tick_params(direction="in")
            cbar.set_label(r"Growth Rate ($\mathrm{day^{-1}}$)", fontsize=13)

        # --- Bottom Row: Phase Speed ---
        sns.heatmap(
            df_pspeed,
            ax=ax[1, i],
            annot=True,
            fmt=".2f", 
            cmap="BrBG",
            vmin=-15.0, vmax=45.0, center=0.0,
            cbar=(i == num_modes - 1),
            xticklabels=True,
            yticklabels=True if i == 0 else False,
            linewidths=0.5,
            linecolor='lightgray',
            cbar_kws={'label': r"Phase Speed ($\mathrm{m~s^{-1}}$)"} if i == num_modes - 1 else None
        )
        ax[1, i].invert_yaxis()
        
        for _, spine in ax[1, i].spines.items():
            spine.set_visible(True)
            spine.set_linewidth(1.2)
            
        ax[1, i].tick_params(direction="in", top=True, right=True, left=True, bottom=True)
        ax[1, i].set_xlabel(r"Non-dimensional Wavenumber $k$", fontsize=14)
        ax[1, i].set_xticklabels([f"{float(t.get_text()):.1f}" for t in ax[1, i].get_xticklabels()])
        
        if i == 0:
            ax[1, i].set_ylabel("Phase Speed", fontsize=14, fontweight="bold")
            ax[1, i].set_yticklabels([f"{float(t.get_text()):.2f}" for t in ax[1, i].get_yticklabels()])
        else:
            ax[1, i].set_ylabel("")

        if i == num_modes - 1:
            cbar = ax[1, i].collections[0].colorbar
            cbar.ax.tick_params(direction="in")
            cbar.set_label(r"Phase Speed ($\mathrm{m~s^{-1}}$)", fontsize=13)

    fig.suptitle(title, x=0.5, y=1.02, fontsize=17, fontweight="bold")
    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

def main():
    parser = argparse.ArgumentParser(description="Visualize dispersion relation sensitivities (Contour and Heatmap).")
    parser.add_argument("--c1", type=float, nargs="+", help="Phase speed of mode 1")
    parser.add_argument("--c2", type=float, nargs="+", help="Phase speed of mode 2")
    parser.add_argument("--scaling_factor", type=float, nargs="+", help="Scaling factor")
    parser.add_argument("--F", type=float, nargs="+", help="Bulk heating parameter")
    parser.add_argument("--f", type=float, nargs="+", help="Fraction of heating applied to first mode")
    parser.add_argument("--b1", type=float, nargs="+", help="Thermodynamic constant")
    parser.add_argument("--m1", type=float, nargs="+", help="Moisture coupling parameter for mode 1")
    parser.add_argument("--m2", type=float, nargs="+", help="Moisture coupling parameter for mode 2")
    parser.add_argument("--gamma_q", type=float, nargs="+", help="Moisture relaxation rate")
    parser.add_argument("--scheme", type=str, default="full", help="Experiment scheme")
    
    args = parser.parse_args()
    
    provided_params = {}
    for param in ["c1", "c2", "scaling_factor", "F", "f", "b1", "m1", "m2", "gamma_q"]:
        val = getattr(args, param)
        if val is not None:
            provided_params[param] = val
            
    keys = list(provided_params.keys())
    param_names = "_".join(keys) if keys else "default"
    
    data_dir = Path(f"/home/b11209013/KW_CRI/File/{args.scheme}/{param_names}")
    fig_dir = Path(f"/home/b11209013/KW_CRI/Figure/{args.scheme}/{param_names}")
    nc_path = data_dir / "dispersion_data.nc"
    
    if not nc_path.exists():
        print(f"NetCDF file {nc_path} not found. Did you run CRI_dispersion.py first? Exiting.")
        return
        
    print(f"Loading data from {nc_path}...")
    ds = xr.open_dataset(nc_path)
    
    varied_params = [k for k in keys if len(provided_params[k]) > 1]
    
    if len(varied_params) == 0:
        print("Need at least 2 parameter values for plotting. Exiting.")
        return
    elif len(varied_params) > 1:
        print(f"Warning: Multiple varied parameters found {varied_params}. Will use the first one {varied_params[0]} for y-axis.")
    
    target_param = varied_params[0]
    
    # --- CONTOUR PREPARATION ---
    target_k_max = 30
    ds_sel_contour = ds.sel(k=slice(None, target_k_max))
    
    sel_dict = {}
    for p in varied_params[1:]:
        sel_dict[p] = provided_params[p][0]
    
    if sel_dict:
        ds_sel_contour = ds_sel_contour.sel(**sel_dict)
        
    ds_sel_contour = ds_sel_contour.squeeze().compute()
    
    title = f"Dispersion Relation Sensitivity: {target_param}"
    if sel_dict:
        title += f" ({', '.join(f'{k}={v}' for k,v in sel_dict.items())})"
    
    output_path_contour = fig_dir / f"sensitivity_contour.png"
    print(f"Generating Combined Contour Plot for {target_param}...")
    plot_combined_contours(ds_sel_contour, target_param, title, output_path_contour)
    print(f"Saved: {output_path_contour}")
    
    # --- HEATMAP PREPARATION ---
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
    
    ds_heatmap = ds
    if target_param in previous_values:
        valid_vals = [v for v in previous_values[target_param] if np.any(np.isclose(ds_heatmap[target_param].values, v))]
        if valid_vals:
            ds_heatmap = ds_heatmap.sel({target_param: valid_vals}, method='nearest')

    target_k_vals = [1, 5, 10, 15, 20, 25, 30]
    ds_sel_heatmap = ds_heatmap.sel(k=target_k_vals, method='nearest')
    
    if sel_dict:
        ds_sel_heatmap = ds_sel_heatmap.sel(**sel_dict)
        
    ds_sel_heatmap = ds_sel_heatmap.squeeze().compute()
    
    output_path_heatmap = fig_dir / f"sensitivity_heatmap.png"
    print(f"Generating Combined Heatmap for {target_param}...")
    plot_combined_heatmaps(ds_sel_heatmap, target_param, title, output_path_heatmap)
    print(f"Saved: {output_path_heatmap}")
    
    print("Done! Both Contour and Heatmap figures generated successfully.")

if __name__ == "__main__":
    main()
