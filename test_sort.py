import numpy as np
from scipy.optimize import linear_sum_assignment

def track_roots_old(raw_roots: np.ndarray) -> np.ndarray:
    n_modes, nk = raw_roots.shape
    sorted_roots: np.ndarray = np.zeros_like(raw_roots)
    sorted_roots[:, 0] = raw_roots[:, 0]
    for k in range(1, nk):
        prev_roots = sorted_roots[:, k-1]
        curr_roots = raw_roots[:, k]
        cost_matrix = np.abs(prev_roots[:, np.newaxis] - curr_roots[np.newaxis, :])
        row_ind, col_ind = linear_sum_assignment(cost_matrix)
        sorted_roots[row_ind, k] = curr_roots[col_ind]
    return sorted_roots

def track_roots_new(raw_roots: np.ndarray) -> np.ndarray:
    n_modes, nk = raw_roots.shape
    sorted_roots: np.ndarray = np.zeros_like(raw_roots)
    
    # Sort the initial roots by real part to ensure consistent ordering across parameters
    initial_idx = np.argsort(np.real(raw_roots[:, 0]))
    sorted_roots[:, 0] = raw_roots[initial_idx, 0]

    for k in range(1, nk):
        # Use simple linear extrapolation for better tracking during mode crossings
        if k == 1:
            predicted = sorted_roots[:, 0]
        else:
            predicted = sorted_roots[:, k-1] + (sorted_roots[:, k-1] - sorted_roots[:, k-2])
            
        curr_roots = raw_roots[:, k]
        
        # Calculate the complex distance matrix between predicted and current roots
        cost_matrix = np.abs(predicted[:, np.newaxis] - curr_roots[np.newaxis, :])
        
        # Solve bipartite matching to find optimal unique pairs
        row_ind, col_ind = linear_sum_assignment(cost_matrix)
        
        # Map the current roots to their assigned rows
        sorted_roots[row_ind, k] = curr_roots[col_ind]
        
    return sorted_roots

# create mock data where initial order flips
k_vals = np.linspace(0, 10, 50)
root1 = 1 + 1j + 0.1*k_vals
root2 = 2 + 2j + 0.2*k_vals
root3 = 3 + 3j + 0.3*k_vals

# param1: roots returned as [1, 2, 3]
raw1 = np.vstack([root1, root2, root3])
# param2: roots returned as [3, 2, 1]
raw2 = np.vstack([root3, root2, root1])

print("Old tracker:")
print("Param1 initial:", np.real(track_roots_old(raw1)[:, 0]))
print("Param2 initial:", np.real(track_roots_old(raw2)[:, 0]))

print("\nNew tracker:")
print("Param1 initial:", np.real(track_roots_new(raw1)[:, 0]))
print("Param2 initial:", np.real(track_roots_new(raw2)[:, 0]))

