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

def plot_heatmaps(data_array: np.ndarray, labels: list, x_ticks: np.ndarray, 
                  title: str, ylabel: str, vmin: float, vmax: float, 
                  center: float, output_path: Path):
    """Generate and save a 3-panel heatmap for the given metrics."""
    plt.rcParams.update({"font.family": "serif"})
    fig, ax = plt.subplots(1, 3, figsize=(16, 4), sharey="col")
    
    mode_titles = ["Slow Mode", "Intermediate Mode", "Fast Mode"]
    
    for i in range(3):
        # We handle center differently if provided
        cmap_kwargs = {"vmin": vmin, "vmax": vmax}
        if center is not None:
            cmap_kwargs["center"] = center
            
        sns.heatmap(
            data_array[..., i],
            ax=ax[i],
            annot=True,
            fmt=".2f", 
            cmap="coolwarm",
            xticklabels=np.round(x_ticks, 1).astype(int),
            yticklabels=labels,
            **cmap_kwargs
        )
        ax[i].set_title(mode_titles[i], fontsize=14, fontweight="bold")
        if i == 0:
            ax[i].set_ylabel(ylabel, fontsize=12)

    fig.suptitle(title, x=0.5, y=1.1, fontsize=16, fontweight="bold")
    
    # Ensure the output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description="Analyze and visualize dispersion relation sensitivities.")
    parser.add_argument("--data_dir", type=str, default="/home/b11209013/KW_CRI/File/f_sensitivity",
                        help="Directory containing the output .npy files.")
    parser.add_argument("--fig_dir", type=str, default="/home/b11209013/KW_CRI/Figure/f_sensitivity",
                        help="Directory to save the generated heatmaps.")
    
    args = parser.parse_args()
    data_dir = Path(args.data_dir)
    fig_dir = Path(args.fig_dir)
    
    print(f"Loading data from {data_dir}...")
    disp_roots = load_data(data_dir)
    
    if not disp_roots:
        print(f"No .npy files found in {data_dir}. Exiting.")
        return
        
    print(f"Loaded {len(disp_roots)} parameter cases: {list(disp_roots.keys())}")
    
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
    
    labels = list(disp_roots.keys())
    x_ticks = k_dis[demo_kidx]
    
    # Slice the arrays to only include the target grid points
    instab_grid = instab_array[:, demo_kidx, :]
    pspeed_grid = pspeed_array[:, demo_kidx, :]
    
    print("Generating Linear Instability heatmap...")
    plot_heatmaps(
        data_array=instab_grid,
        labels=labels,
        x_ticks=x_ticks,
        title="Linear Instability",
        ylabel="Parameters",
        vmin=-2.0, vmax=2.0, center=None,
        output_path=fig_dir / "instability.png"
    )
    
    print("Generating Phase Speed heatmap...")
    plot_heatmaps(
        data_array=pspeed_grid,
        labels=labels,
        x_ticks=x_ticks,
        title="Phase Speed",
        ylabel="Parameters",
        vmin=-15.0, vmax=45.0, center=0.0,
        output_path=fig_dir / "phase_speed.png"
    )
    
    print(f"Done! Figures saved to {fig_dir}")

if __name__ == "__main__":
    main()
