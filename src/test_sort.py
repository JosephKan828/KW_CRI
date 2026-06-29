import numpy as np
from parameter import WaveParameters
from calc_dispersion import compute_coefficients, solve_dispersion_roots

params = WaveParameters()
k_dis = np.linspace(0, 1e2, 10001)[1:]
k_cal = 2 * np.pi * 4320 / 40000 * k_dis

G3, G2, G1, G0 = compute_coefficients(params, k_cal)
# solve_dispersion_roots uses track_roots internally
omega = solve_dispersion_roots(G3, G2, G1, G0)

print("Omega shape:", omega.shape)
print("Frequencies at k=0:")
print(np.real(omega[0, :]))
print("Frequencies at large k:")
print(np.real(omega[-1, :]))
