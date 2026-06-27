import argparse
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

def plot_combined_heatmaps(instab_grid: np.ndarray, pspeed_grid: np.ndarray, 
                           labels: list, x_ticks: np.ndarray, title: str, 
                           ylabel: str, output_path: Path):
    """Generate and save a (2, 3) heatmap for instability and phase speed."""
    plt.rcParams.update({"font.family": "serif"})
    fig, ax = plt.subplots(2, 3, figsize=(16, 7))
    
    mode_titles = ["Slow Mode", "Intermediate Mode", "Fast Wave"]
    
    for i in range(3):
        # --- Top Row: Instability ---
        sns.heatmap(
            instab_grid[..., i],
            ax=ax[0, i],
            annot=True,
            fmt=".2f", 
            cmap="coolwarm",
            vmin=-2.0, vmax=2.0,
            cbar=(i == 2), # Colorbar only on the most right panel
            xticklabels=False, # X-ticks only on the lower row
            yticklabels=labels if i == 0 else False
        )
        
        # Title of slow, intermediate, and fast only on the top row
        ax[0, i].set_title(mode_titles[i], fontsize=14, fontweight="bold")
        
        if i == 0:
            ax[0, i].set_ylabel(f"Instability", fontsize=14, fontweight="bold")
            
        # Optional colorbar label
        if i == 2:
            cbar = ax[0, i].collections[0].colorbar
            # cbar.set_label("Instability", fontsize=12)

        # --- Bottom Row: Phase Speed ---
        sns.heatmap(
            pspeed_grid[..., i],
            ax=ax[1, i],
            annot=True,
            fmt=".2f", 
            cmap="coolwarm",
            vmin=-15.0, vmax=45.0, center=0.0,
            cbar=(i == 2), # Colorbar only on the most right panel
            xticklabels=np.round(x_ticks, 1).astype(int), # X-ticks on lower row
            yticklabels=labels if i == 0 else False
        )
        
        if i == 0:
            ax[1, i].set_ylabel(f"Phase Speed", fontsize=14, fontweight="bold")
            
        if i == 2:
            cbar = ax[1, i].collections[0].colorbar
            # cbar.set_label("Phase Speed", fontsize=12)

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

    # Filter to previous assigned values for the sparse grid setup
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
    
    if len(keys) == 1:
        param_name = keys[0]
        if param_name in previous_values:
            valid_vals = set(previous_values[param_name])
            filtered_disp_roots = {}
            for k, v in disp_roots.items():
                try:
                    val_float = float(k.split("=")[-1])
                    if any(np.isclose(val_float, expected_val, atol=1e-5) for expected_val in valid_vals):
                        filtered_disp_roots[k] = v
                except ValueError:
                    pass
            if filtered_disp_roots:
                disp_roots = filtered_disp_roots
        
    print(f"Loaded {len(disp_roots)} parameter cases for heatmap: {list(disp_roots.keys())}")
    
    # Setup wavenumbers
    k_dis = np.linspace(0, 1e2, 10001)[100:]
    k_cal = 2 * np.pi * 4320 / 40000 * k_dis
    
    # Identify the target indices for the visualization grids
    target_k_vals = [1, 5, 10, 15, 20, 25, 30]
    demo_kidx = np.array([np.argmin(np.abs(k_dis - target_k)) for target_k in target_k_vals])
    
    # Calculate Instability
    instab_array = np.array([-1 * value.imag for value in disp_roots.values()])
    
    # Calculate Phase Speed
    pspeed_array = np.array([(value.real / k_cal[:, None]) * 50 for value in disp_roots.values()])
    
    labels = np.array([float(key.split("=")[-1]) for key in disp_roots.keys()])
    labels_argsort = np.argsort(labels)

    x_ticks = k_dis[demo_kidx]
    
    # Slice the arrays to only include the target grid points
    instab_grid = instab_array[:, demo_kidx, :]
    pspeed_grid = pspeed_array[:, demo_kidx, :]

    # Sort the modes based on phase speed at each (file, k) point
    sort_idx = np.argsort(pspeed_grid, axis=2)
    instab_grid = np.take_along_axis(instab_grid, sort_idx, axis=2)
    pspeed_grid = np.take_along_axis(pspeed_grid, sort_idx, axis=2)
    
    print("Generating Combined Heatmap...")
    plot_combined_heatmaps(
        instab_grid=instab_grid[labels_argsort],
        pspeed_grid=pspeed_grid[labels_argsort],
        labels=labels[labels_argsort],
        x_ticks=x_ticks,
        title="Dispersion Relation Sensitivity",
        ylabel="Parameters",
        output_path=fig_dir / "sensitivity_heatmap.png"
    )
    
    print(f"Done! Figure saved to {fig_dir}/sensitivity_heatmap.png")

if __name__ == "__main__":
    main()
