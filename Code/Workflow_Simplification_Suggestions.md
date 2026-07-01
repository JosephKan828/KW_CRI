# Implementation Guide: Configuration-Driven Dispersion Workflow

This guide demonstrates how to implement a configuration-driven framework to easily modify the dispersion relation calculation. It covers creating the configuration file, updating the Python scripts to parse inline arguments, and running it all via your shell script.

## 1. Create the Configuration File (`schemes.json`)

Create a JSON file in your `Code` directory named `schemes.json`. This file acts as a catalog of all your predefined simplifications and physical assumptions.

**Example `schemes.json`:**
```json
{
  "full": {
    "param_overrides": {},
    "coeff_mask": [true, true, true, true]
  },
  "simplified_alpha": {
    "description": "Zeros out coupling terms for testing uncoupled modes",
    "param_overrides": {
      "alpha_11_o": 0.0,
      "alpha_12_o": 0.0,
      "alpha_22_o": 0.0
    },
    "coeff_mask": [true, true, true, true]
  },
  "no_linear_term": {
    "description": "Tests dispersion without the G1 * omega linear term",
    "param_overrides": {},
    "coeff_mask": [true, true, false, true]
  }
}
```
*Note: `coeff_mask` corresponds to `[G3, G2, G1, G0]`.*

## 2. Refactor `CRI_dispersion.py` to Parse Config and Inline Arguments

Update your Python script to load the base scheme from the JSON file, and then allow **inline arguments** to override those base settings on the fly.

### Update `argparse` in `main()`:
```python
import json

def main():
    parser = argparse.ArgumentParser()
    # Replace --mode with configuration arguments
    parser.add_argument("--scheme", type=str, default="full", help="Name of scheme in schemes.json")
    parser.add_argument("--scheme_file", type=str, default="schemes.json", help="Path to scheme config")
    
    # Inline override arguments
    parser.add_argument("--override_params", type=str, nargs="+", default=[], 
                        help="Key=Value pairs to override params inline, e.g., alpha_11_o=0")
    parser.add_argument("--coeff_mask", type=int, nargs=4, 
                        help="4 binary values to mask [G3, G2, G1, G0], e.g., 1 1 0 1")
    
    # ... existing arguments for sweep (c1, c2, etc.) ...
    args = parser.parse_args()

    # Load base configuration
    with open(args.scheme_file, 'r') as f:
        schemes = json.load(f)
    base_config = schemes.get(args.scheme, schemes["full"])

    # 1. Parse inline parameter overrides
    param_overrides = base_config.get("param_overrides", {})
    for override in args.override_params:
        key, val = override.split("=")
        param_overrides[key] = float(val)

    # 2. Parse inline coefficient mask (1 or 0 -> True or False)
    if args.coeff_mask is not None:
        coeff_mask = [bool(m) for m in args.coeff_mask]
    else:
        coeff_mask = base_config.get("coeff_mask", [True, True, True, True])

    # Pass the resolved dictionary and mask into the grid calculation
    omega = calc_dispersion_grid(k_cal, k_dis, param_overrides, coeff_mask, param_grids)
```

### Update `calc_dispersion_grid()`:
```python
def calc_dispersion_grid(k_cal, k_dis, param_overrides, coeff_mask, param_grids):
    # ... existing chunk setup ...

    def _core_dispersion_wrapper_closure(k_arr, *p_vals):
        try:
            p_dict = {k: float(v) for k, v in zip(p_keys, p_vals)}
            params = WaveParameters(**p_dict)
            
            # Apply our resolved parameter overrides
            for k_override, v_override in param_overrides.items():
                setattr(params, k_override, v_override)
                
            # Pass the mask array to the calculation
            disp_rel = compute_dispersion(params, k_arr, coeff_mask)
            return disp_rel
        except Exception as e:
            return np.full((len(k_arr), 3), np.nan + 1j*np.nan, dtype=np.complex128)
```

## 3. Controlling via the Shell Script (`CRI_dispersion.sh`)

Now that the Python script accepts both JSON-backed schemes and inline arguments, you can easily trigger different setups from your bash script.

### Using a predefined scheme from `schemes.json`
To run a standard sweep using one of your predefined simplifications:
```bash
python3 "$root/Code/CRI_dispersion.py" \
    --scheme "simplified_alpha" \
    --$VAR_NAME $VAR_LIST
```

### Using Inline Arguments for Ad-hoc Testing
If you want to test turning off $G_0$ and setting `m1 = 0` quickly, you don't need to touch `schemes.json`. Use inline arguments to override the `"full"` base scheme on the fly:
```bash
python3 "$root/Code/CRI_dispersion.py" \
    --scheme "full" \
    --override_params "m1=0.0" "alpha_22_o=0.0" \
    --coeff_mask 1 1 1 0 \
    --$VAR_NAME $VAR_LIST
```

### Updating `CRI_dispersion.sh` arguments:
You can modify the top of your `CRI_dispersion.sh` to accept these options so you can trigger them directly from the terminal:

```bash
# CRI_dispersion.sh
EXPERIMENT_DESC=${1:-"Routine sensitivity sweep"}
SCHEME=${2:-"full"}
TARGET=${3:-"all"}

# Allows you to pass extra overrides directly when calling the script
# e.g. ./CRI_dispersion.sh "test" "full" "f" "--override_params m1=0 --coeff_mask 1 1 1 0"
EXTRA_ARGS=${4:-""}

# ...
run_sweep() {
    # ...
    python3 "$root/Code/CRI_dispersion.py" \
        --scheme "$SCHEME" \
        $EXTRA_ARGS \
        --$VAR_NAME $VAR_LIST
}
```

This setup gives you the best of both worlds: strict, reproducible tracking of schemes via `schemes.json` for major tests, and complete, instant flexibility via inline arguments for debugging and exploratory runs.
