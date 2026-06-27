import argparse
import decimal
from matplotlib.colors import TwoSlopeNorm
import numpy as np
import seaborn as sns
from typing import Dict
from pathlib import Path
from matplotlib import pyplot as plt

def load_data(data_dir: Path) -> Dict[str, np.ndarray]:
    """Dynamically load all numpy arrays from the specified directory."""
    disp_roots = {}
    
    # Sort files so they appear in order (e.g. f=0.2, f=0.5, f=0.8)
    for file_path in sorted(data_dir.glob("*.npy")):
        # The arrays are sliced from 99 to match the k_dis definition
        disp_roots[file_path.stem] = np.load(file_path)[99:]
        
    return disp_roots

def plot_combined_contours(instab_grid: np.ndarray, pspeed_grid: np.ndarray, 
                           labels: np.ndarray, k_dis: np.ndarray, title: str, 
                           ylabel: str, output_path: Path):
    """Generate and save a (2, 3) contour plot for instability and phase speed."""
    plt.rcParams.update({"font.family": "serif"})
    fig, ax = plt.subplots(2, 3, figsize=(18, 7))
    
    mode_titles = ["Slow Mode", "Intermediate Mode", "Fast Wave"]
    
    X, Y = np.meshgrid(k_dis, labels)
    
    for i in range(3):
        # --- Top Row: Instability ---

        cf_instab = ax[0, i].contourf(
            X, Y, instab_grid[..., i],
            levels=np.linspace(-2, 2, 21),
            cmap="RdBu_r",
            norm=TwoSlopeNorm(vcenter=0),
            extend="both"
        )
        
        ax[0, i].contour(
            X, Y, instab_grid[..., i],
            levels=np.arange(-2.0, 2.1, 0.25),
            colors="k",
            linewidths=0.5,
            alpha=0.6
        )
        
        ax[0, i].set_title(mode_titles[i], fontsize=14, fontweight="bold")
        
        if i == 0:
            ax[0, i].set_ylabel(f"Instability", fontsize=14, fontweight="bold")
        else:
            ax[0, i].set_yticks([])
        
        if i == 2:
            cbar = fig.colorbar(cf_instab, ax=ax[0, i], orientation="vertical", shrink=0.8, aspect=40)
            cbar.set_ticks([-2, -1, 0, 1, 2])


        # --- Bottom Row: Phase Speed ---
        cf_pspeed = ax[1, i].contourf(
            X, Y, pspeed_grid[..., i],
            levels=np.linspace(-10, 50, 21),
            cmap="RdBu_r",
            norm=TwoSlopeNorm(vcenter=0),
            extend="both"
        )
        
        ax[1, i].contour(
            X, Y, pspeed_grid[..., i],
            levels=np.arange(-10, 51, 5),
            colors="k",
            linewidths=0.5,
            alpha=0.6
        )
        
        ax[1, i].set_xlabel("Wavenumber ($k$)", fontsize=14)

        if i == 0:
            ax[1, i].set_ylabel(f"Phase Speed", fontsize=14, fontweight="bold")
        else:
            ax[1, i].set_yticks([])

        if i == 2:
            cbar = fig.colorbar(cf_pspeed, ax=ax[1, i], orientation="vertical", shrink=0.8, aspect=40)
            cbar.set_ticks([-10, 0, 10, 20, 30, 40, 50])

    fig.suptitle(title, x=0.5, y=1.02, fontsize=16, fontweight="bold")
    
    # Adjust layout to prevent overlap
    plt.tight_layout()
    
    # Ensure the output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description="Visualize dispersion relation sensitivities.")
    
    # Accept the same parameters as CRI_dispersion.py to deduce directory names automatically
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
    
    # Extract parameters to determine directory names
    param_grids = {}
    for param in ["c1", "c2", "scaling_factor", "F", "f", "b1", "m1", "m2", "gamma_q"]:
        val = getattr(args, param)
        if val is not None:
            param_grids[param] = val
            
    keys = list(param_grids.keys())
    param_names = "_".join(keys) if keys else "default"
    
    data_dir = Path(f"/home/b11209013/KW_CRI/File/{param_names}_sensitivity")
    fig_dir = Path(f"/home/b11209013/KW_CRI/Figure/{param_names}_sensitivity")
    
    print(f"Loading data from {data_dir}...")
    disp_roots = load_data(data_dir)
    
    if not disp_roots:
        print(f"No .npy files found in {data_dir}. Did you run CRI_dispersion.py first? Exiting.")
        return
        
    print(f"Loaded {len(disp_roots)} parameter cases: {list(disp_roots.keys())}")
    
    # Setup wavenumbers
    k_dis = np.linspace(0, 1e2, 10001)[100:]
    k_cal = 2 * np.pi * 4320 / 40000 * k_dis
    
    if len(disp_roots) < 2:
        print(f"Need at least 2 parameter values for a contour plot, but only found {len(disp_roots)}. Exiting.")
        return

    # Filter wavenumbers for the visualization (up to k=30)
    target_k_max = 30
    k_mask = k_dis <= target_k_max
    k_plot = k_dis[k_mask]
    
    # Calculate Instability
    instab_array = np.array([-1 * value.imag for value in disp_roots.values()])
    
    # Calculate Phase Speed
    pspeed_array = np.array([(value.real / k_cal[:, None]) * 50 for value in disp_roots.values()])
    
    labels = np.array([float(key.split("=")[-1]) for key in disp_roots.keys()])
    labels_argsort = np.argsort(labels)
    
    # Slice the arrays to only include the target grid points
    instab_grid = instab_array[:, k_mask, :]
    pspeed_grid = pspeed_array[:, k_mask, :]

    # Sort the modes based on phase speed at each (file, k) point
    sort_idx = np.argsort(pspeed_grid, axis=2)
    instab_grid = np.take_along_axis(instab_grid, sort_idx, axis=2)
    pspeed_grid = np.take_along_axis(pspeed_grid, sort_idx, axis=2)
    
    print("Generating Combined Contour Plot...")
    plot_combined_contours(
        instab_grid=instab_grid[labels_argsort],
        pspeed_grid=pspeed_grid[labels_argsort],
        labels=labels[labels_argsort],
        k_dis=k_plot,
        title=f"{param_names} Sensitivity",
        ylabel="Parameters",
        output_path=fig_dir / "sensitivity_contour.png"
    )
    
    print(f"Done! Figure saved to {fig_dir}/sensitivity.png")

if __name__ == "__main__":
    main()
