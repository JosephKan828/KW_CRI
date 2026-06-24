"""Calculates the dispersion relation of the system using vectorized linear algebra."""

import numpy as np
from typing import Tuple, Union, List

# Import the dataclass from your local parameter.py script
from parameter import WaveParameters


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
    G3 = np.full_like(k_values, p.A0, dtype=np.complex128)
    
    G2 = -p.B0 * k_values - 1j * p.gamma_q * (p.m2 * p.A0 - p.m1 * p.F2)
    
    G1 = (p.C0 * k_values**2) + 1j * p.gamma_q * k_values * (p.m2 * p.B0 - p.m1 * p.W0)
    
    G0 = -1j * p.gamma_q * p.m2 * p.C0 * k_values**2

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

    roots_omega = np.array(roots_omega)

    # Vectorized sorting of roots by their real part (phase speed)
    sorted_idx = np.argsort(np.real(roots_omega), axis=1)
    roots_omega = np.take_along_axis(roots_omega, sorted_idx, axis=1)

    return roots_omega


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
    print()
    return solve_dispersion_roots(*masked_coeffs)
