"""
Advanced Diagnosis Workflow for CRI Dispersion Relation.
Fully optimized using Xarray and Dask for lazy multi-dimensional parameter sweeps.
"""

import os
import sys
import argparse
import itertools
import multiprocessing
import numpy as np
import xarray as xr
import dask
import json
from pathlib import Path
from matplotlib import pyplot as plt

sys.path.append("/home/b11209013/KW_CRI/src")
from parameter import WaveParameters
from calc_dispersion import compute_dispersion

def calc_dispersion_grid(k_cal, k_dis, param_overrides, coeff_mask, param_grids):
    """
    Construct an N-dimensional parameter grid and compute dispersion lazily using Dask.
    """
    if coeff_mask[0]:
        mode_size = 3
    elif coeff_mask[1]:
        mode_size = 2
    elif coeff_mask[2]:
        mode_size = 1
    else:
        mode_size = 0
        
    # Chunk parameters to size 1 to parallelize over parameter combinations
    das = {k: xr.DataArray(v, dims=[k], coords={k: v}).chunk({k: 1}) for k, v in param_grids.items()}
    
    # k_cal MUST be a single chunk because track_roots requires the full k-spectrum to track modes continuously
    k_da = xr.DataArray(k_cal, dims=['k'], coords={'k': k_dis}).chunk({'k': -1})
    
    p_keys = list(param_grids.keys())
    args = [k_da] + [das[k] for k in p_keys]
    
    def _core_dispersion_wrapper_closure(k_arr, *p_vals):
        try:
            p_dict = {k: float(v) for k, v in zip(p_keys, p_vals)}
            params = WaveParameters(**p_dict)
            
            for k_override, v_override in param_overrides.items():
                setattr(params, k_override, v_override)
                
            disp_rel = compute_dispersion(params, k_arr, coeff_mask)
            return disp_rel
        except Exception as e:
            # Return NaNs if the parameter combination leads to unstable/invalid roots
            return np.full((len(k_arr), mode_size), np.nan + 1j*np.nan, dtype=np.complex128)

    out = xr.apply_ufunc(
        _core_dispersion_wrapper_closure,
        *args,
        input_core_dims=[['k']] + [[] for _ in p_keys],
        output_core_dims=[['k', 'mode']],
        vectorize=True,
        dask='parallelized',
        output_dtypes=[np.complex128],
        dask_gufunc_kwargs={'output_sizes': {'mode': mode_size}}
    )
    
    return out

def plot_single_configuration(ds_slice, title, output_path):
    """
    Generates a professional Matplotlib plot for a single parameter configuration.
    Handles NaN values implicitly through Xarray plot methods.
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
    
    fig, ax = plt.subplots(1, 2, figsize=(18, 4), dpi=150)
    
    ls_list = ["-", "--", ":"]
    mode_labels = ["Slow Mode", "Intermediate Mode", "Fast Mode"]
    
    # Plot Growth Rate
    for m in range(ds_slice.sizes['mode']):
        ls = ls_list[m] if m < len(ls_list) else "-"
        label = mode_labels[m] if m < len(mode_labels) else f"Mode {m}"
        
        # Xarray implicitly handles NaNs and aligns dimensions
        ds_slice['instab'].isel(mode=m).plot.line(
            ax=ax[0], x='k', color="k", linestyle=ls, linewidth=2.5, label=label
        )

    ax[0].axhline(0, color="k", linestyle="-", linewidth=1, alpha=0.5) 
    ax[0].set_xlim(0, 30)
    ax[0].set_ylabel(r"Growth Rate ($\mathrm{day^{-1}}$)", fontweight="bold")
    ax[0].set_xlabel(r"Non-dimensional Wavenumber $k$")
    ax[0].set_title("Linear Instability", fontweight="bold")
    ax[0].grid(True, linestyle=":", alpha=0.7)
    ax[0].legend(loc="upper right", frameon=True)
    
    # Plot Phase Speed
    for m in range(ds_slice.sizes['mode']):
        ls = ls_list[m] if m < len(ls_list) else "-"
        ds_slice['pspeed'].isel(mode=m).plot.line(
            ax=ax[1], x='k', color="k", linestyle=ls, linewidth=2.5
        )

    ax[1].set_ylabel(r"Phase Speed ($\mathrm{m~s^{-1}}$)", fontweight="bold")
    ax[1].set_xlabel(r"Non-dimensional Wavenumber $k$")
    ax[1].set_title("Phase Speed", fontweight="bold")
    ax[1].set_xlim(0, 30)
    ax[1].grid(True, linestyle=":", alpha=0.7)
    
    plt.suptitle(title, fontsize=16, fontweight="bold", y=1.05)
    
    # Save figure securely
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

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
    parser.add_argument("--scheme", type=str, default="full", help="Name of scheme in schemes.json")
    parser.add_argument("--scheme_file", type=str, default="/home/b11209013/KW_CRI/Code/schemes.json", help="Path to scheme config")
    parser.add_argument("--override_params", type=str, nargs="+", default=[], help="Key=Value pairs to override params inline")
    parser.add_argument("--coeff_mask", type=int, nargs=4, help="4 binary values to mask [G3, G2, G1, G0]")
    
    args = parser.parse_args()
    
    with open(args.scheme_file, 'r') as f:
        schemes = json.load(f)
    base_config = schemes.get(args.scheme, schemes.get("full", {}))

    param_overrides = base_config.get("param_overrides", {}).copy()
    for override in args.override_params:
        if "=" in override:
            key, val = override.split("=")
            param_overrides[key] = float(val)

    if args.coeff_mask is not None:
        coeff_mask = [bool(m) for m in args.coeff_mask]
    else:
        coeff_mask = base_config.get("coeff_mask", [True, True, True, True])
    
    # 1. Parse Parameters
    param_grids = {}
    default_params = WaveParameters()
    for param in ["c1", "c2", "scaling_factor", "F", "f", "b1", "m1", "m2", "gamma_q"]:
        val = getattr(args, param)
        if val is not None:
            param_grids[param] = val
        else:
            # Fallback to default if not provided to ensure predictable Dask shape
            param_grids[param] = [getattr(default_params, param)]
            
    # Print experimental setup
    total_experiments = np.prod([len(v) for v in param_grids.values()])
    print(f"Total experimental configurations to run: {total_experiments}")
    
    # 2. Configure Wavenumber domain
    k_dis = np.linspace(0, 1e2, 10001)[1:]
    k_cal = 2 * np.pi * 4320 / 40000 * k_dis
    
    # 3. Construct Dask-backed Xarray Dataset
    omega = calc_dispersion_grid(k_cal, k_dis, param_overrides, coeff_mask, param_grids)
    
    ds = xr.Dataset({'omega': omega})
    
    # Add proper non-dimensional coordinate attributes
    ds['k'].attrs = {'long_name': 'Non-dimensional Wavenumber'}
    
    # Compute dimensional wavenumber explicitly for scaling relations
    ds.coords['k_cal'] = ('k', k_cal)
    ds['k_cal'].attrs = {'long_name': 'Dimensional Wavenumber', 'units': 'rad m^{-1}'}
    
    # Define Mode coordinate
    if coeff_mask[0]:
        mode_size = 3
    elif coeff_mask[1]:
        mode_size = 2
    elif coeff_mask[2]:
        mode_size = 1
    else:
        mode_size = 0
    ds.coords['mode'] = np.arange(mode_size)
    
    # 4. Perform Advanced Diagnostics
    # Removed post-hoc `np.argsort` by phase speed here! 
    # `calc_dispersion.track_roots` ALREADY tracks modes continuously based on proximity.
    # Sorting at every independent `k` creates false jumps during mode crossings.
    
    ds['instab'] = -1 * ds['omega'].imag
    ds['instab'].attrs = {'long_name': 'Growth Rate', 'units': 'day^{-1}'}
    
    ds['pspeed'] = (ds['omega'].real / ds['k_cal']) * 50 
    ds['pspeed'].attrs = {'long_name': 'Phase Speed', 'units': 'm s^{-1}'}
    
    # 5. Output Management
    provided_keys = [k for k in param_grids if getattr(args, k) is not None]
    param_names = "_".join(provided_keys) if provided_keys else "default"
    
    base_dir = Path("/home/b11209013/KW_CRI")
    fig_dir = base_dir / f"Figure/{args.scheme}/{param_names}"
    data_dir = base_dir / f"File/{args.scheme}/{param_names}"
    
    fig_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)
    
    print("Computing dispersion relations natively with Dask...")
    nc_path = data_dir / "dispersion_data.nc"
    
    # Clean previous if exists to prevent dimension clash
    if nc_path.exists():
        nc_path.unlink()
        
    # Drop complex 'omega' variable since NetCDF4 engine doesn't support complex data natively
    ds = ds.drop_vars('omega')
    
    # Evaluate the lazy dask array into memory using multiprocessing scheduler
    with dask.config.set(scheduler='processes', num_workers=8):
        ds.load()
        
    # Save the computed data to NetCDF synchronously
    ds.to_netcdf(nc_path)
        
    print(f"Data saved to {nc_path}")
    
    # Re-load from disk to free memory and plot 
    ds_disk = xr.open_dataset(nc_path)
    
    # 6. Visualization 
    print("Generating diagnostic plots...")
    
    # Iterate through the grid of combinations
    keys = list(param_grids.keys())
    values_product = list(itertools.product(*[param_grids[k] for k in keys]))
    
    single_fig_dir = fig_dir / "single"
    single_fig_dir.mkdir(parents=True, exist_ok=True)
    
    for vals in values_product:
        sel_dict = dict(zip(keys, vals))
        
        # Only include modified parameters in the title/filename
        mod_dict = {k: v for k, v in sel_dict.items() if k in provided_keys}
        
        modification = "_".join([f"{k}={v}" for k, v in mod_dict.items()]) if mod_dict else "default"
        title = rf"Sensitivity ({', '.join([f'{k}={v}' for k, v in mod_dict.items()])})" if mod_dict else "Default Parameters"
        
        # Select the specific 1D slice
        ds_slice = ds_disk.sel(**sel_dict)
        
        output_fig = single_fig_dir / f"{modification}.png"
        plot_single_configuration(ds_slice, title, output_fig)
        
    print("All sensitivity experiments completed and plots generated.")

if __name__ == "__main__":
    main()
