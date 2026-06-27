"""Calculates the dispersion relation of the system using vectorized linear algebra."""

import numpy as np
from typing import Tuple, Union, List
from scipy.optimize import linear_sum_assignment

# Import the dataclass from your local parameter.py script
from parameter import WaveParameters

def track_roots(
    raw_roots: np.ndarray
) -> np.ndarray:

    n_modes, nk = raw_roots.shape
    sorted_roots: np.ndarray = np.zeros_like(raw_roots)

    sorted_roots[:, 0] = raw_roots[:, 0]

    for k in range(1, nk):
        prev_roots = sorted_roots[:, k-1]
        curr_roots = raw_roots[:, k]
        
        # Calculate the complex distance matrix between previous and current roots
        cost_matrix = np.abs(prev_roots[:, np.newaxis] - curr_roots[np.newaxis, :])
        
        # Solve bipartite matching to find optimal unique pairs
        row_ind, col_ind = linear_sum_assignment(cost_matrix)
        
        # Map the current roots to their assigned rows
        sorted_roots[row_ind, k] = curr_roots[col_ind]
        
    return sorted_roots

def compute_coefficients(
    params: WaveParameters, k_values: np.ndarray
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Compute the cubic polynomial coefficients Gamma3, Gamma2, Gamma1, and Gamma0.

    Matches the explicit dispersion relation: G3*w^3 + G2*w^2 + G1*w + G0 = 0.

    Args:
        params (WaveParameters): The initialized system parameters.
        k_values (np.ndarray): 1D array of wavenumbers (rad/m) to calculate.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: (G3, G2, G1, G0) arrays of shape (N,).
    """
    p = params



    # Vectorized computation mapping directly to the Markdown derivation
    G3 = np.full_like(k_values, 1+p.F1, dtype=np.complex128)
    
    G2 = p.gamma_q * (p.m2*(1+p.F1) - p.m1*p.F2) - \
        1j * k_values * (p.c2 * (1-p.alpha_22)*(1+p.F1) + p.c1 * (1-p.alpha_11) + p.c1*p.alpha_21*p.F2)
    
    G1 = -1 * k_values**2 * p.c1 * p.c2 * p.Delta_alpha - \
        1j * k_values * p.gamma_q * (
            p.m2*(p.c2*(1-p.alpha_22)*(1+p.F1)+p.c1*(1-p.alpha_11) + p.c1*p.alpha_21*p.F2) -\
                p.m1 * (p.c1*(1-p.alpha_11)*p.F2 + p.c2*p.alpha_12*p.F1)
        )
    
    G0 = -1 * k_values**2 * p.m2 * p.gamma_q * p.c1 * p.c2 *p.Delta_alpha

    return G3, G2, G1, G0


def solve_dispersion_roots(
    G3: Union[float, np.ndarray], 
    G2: Union[float, np.ndarray], 
    G1: Union[float, np.ndarray], 
    G0: Union[float, np.ndarray]
) -> np.ndarray:
    """Solve the dispersion relation roots given the coefficients G3, G2, G1, G0.
    Dynamically handles cubic, quadratic, and linear formulations.

    Args:
        G3 (Union[float, np.ndarray]): Coefficient array of cubic term.
        G2 (Union[float, np.ndarray]): Coefficient array of quadratic term.
        G1 (Union[float, np.ndarray]): Coefficient array of linear term.
        G0 (Union[float, np.ndarray]): Coefficient array of constant term.

    Returns:
        np.ndarray: Complex frequency roots (omega) of shape (N, M), sorted by real part.
    """
    # Standardize to arrays
    G0 = np.atleast_1d(G0)
    G3 = G3 * np.ones_like(G0) if np.isscalar(G3) else G3
    G2 = G2 * np.ones_like(G0) if np.isscalar(G2) else G2
    G1 = G1 * np.ones_like(G0) if np.isscalar(G1) else G1

    roots_omega = []
    
    for c3, c2, c1, c0 in zip(G3, G2, G1, G0):
        if c3 == 0 and c2 != 0:
            roots = np.roots([c2, c1, c0])
        elif c3 == 0 and c2 == 0:
            roots = np.roots([c1, c0])
        else:
            roots = np.roots([c3, c2, c1, c0])
            
        roots_omega.append(roots)

    roots_omega = np.array(roots_omega) * (-1j)
    
    return track_roots(roots_omega.T).T

def compute_dispersion(
    params: WaveParameters,
    k_values: np.ndarray,
    full_coeff: List[bool],
) -> np.ndarray:
    """Compute the complex frequencies omega for an array of wavenumbers.

    Args:
        params (WaveParameters): The system parameters.
        k_values (np.ndarray): 1D array of wavenumbers (rad/m) to calculate.
        full_coeff: Boolean or list of 4 booleans to mask [G3, G2, G1, G0].

    Returns:
        np.ndarray: Complex frequency roots of shape (len(k_values), 3) sorted
            by their real part.
    """

    if len(full_coeff) != 4:
        raise ValueError("The length of full_coeff list should be exactly 4.")

    # Compute the original arrays
    G3, G2, G1, G0 = compute_coefficients(params, k_values)

    # Mask arrays based on the boolean flags
    coeffs = [G3, G2, G1, G0]
    masked_coeffs = [
        arr if flag else np.zeros_like(arr)
        for arr, flag in zip(coeffs, full_coeff)
        ]

    return solve_dispersion_roots(*masked_coeffs)
