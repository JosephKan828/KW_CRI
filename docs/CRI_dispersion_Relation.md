# Derivation of the Dispersion Relation

This document details the step-by-step mathematical deduction of the dispersion relation for the given coupled thermodynamic system.

## 1. Initial System of Equations

The original system consists of three prognostic equations for $T_1$, $T_2$, and $q$, and two diagnostic equations for the forcing terms $J_1$ and $J_2$:

$$\frac{\partial T_{1}}{\partial t} + c_{1}\frac{\partial T_{1}}{\partial x} = J_{1} + \alpha_{1, 1} c_1 \frac{\partial T_1}{\partial x} + \alpha_{1, 2} c_2 \frac{\partial T_2}{\partial x} \quad (1)$$
$$\frac{\partial T_{2}}{\partial t} + c_{2}\frac{\partial T_{2}}{\partial x} = J_{2} + \alpha_{2, 1} c_1 \frac{\partial T_1}{\partial x} + \alpha_{2, 2} c_2 \frac{\partial T_2}{\partial x} \quad (2)$$
$$\frac{\partial q}{\partial t} = m_{1}J_{1} + m_{2}J_{2} \quad (3)$$
$$J_{1} = -\frac{F}{b_{1}}\left( f\frac{\partial T_{1}}{\partial t} + (1-f)\frac{\partial T_{2}}{\partial t} \right) \quad (4)$$
$$J_{2} = -\gamma_{q}q \quad (5)$$

### Substitution
Substituting $J_1$ and $J_2$ into equations (1)-(3) yields:
1. $\frac{\partial T_{1}}{\partial t} + c_{1}\frac{\partial T_{1}}{\partial x} = -\frac{F}{b_{1}}\left( f\frac{\partial T_{1}}{\partial t} + (1-f)\frac{\partial T_{2}}{\partial t} \right) +\alpha_{1, 1} c_1 \frac{\partial T_1}{\partial x} +\alpha_{1, 2} c_2 \frac{\partial T_2}{\partial x}$
2. $\frac{\partial T_{2}}{\partial t} + c_{2}\frac{\partial T_{2}}{\partial x} = -\gamma_{q}q +\alpha_{2, 1} c_1 \frac{\partial T_1}{\partial x} +\alpha_{2, 2} c_2 \frac{\partial T_2}{\partial x}$
3. $\frac{\partial q}{\partial t} = -\frac{m_{1}F}{b_{1}}\left( f\frac{\partial T_{1}}{\partial t} + (1-f)\frac{\partial T_{2}}{\partial t} \right) - m_{2}\gamma_{q}q$

---

## 2. Plane Wave Projection (Polarized Equations)

We project the variables onto the normal mode solutions:
$$(T_1, T_2, q) = (\hat{T}_1, \hat{T}_2, \hat{q}) e^{i(\omega t - kx)}$$
This maps the operators as follows: $\frac{\partial}{\partial t} \rightarrow i\omega$ and $\frac{\partial}{\partial x} \rightarrow -ik$.

Multiplying the entire system by $-i$ (since $(-i)(i) = 1$) to keep terms real, and defining the fractional forcing coefficients:
* $F_1 = \frac{Ff}{b_1}$
* $F_2 = \frac{F(1-f)}{b_1}$

The algebraic system becomes:
1. $\left[ \omega(1 + F_{1}) - kc_{1}(1 - \alpha_{1,1}) \right]\hat{T}_{1} + \left[ \omega F_{2} + kc_{2}\alpha_{1,2} \right]\hat{T}_{2} = 0$
2. $(kc_{1}\alpha_{2,1})\hat{T}_{1} + \left[ \omega - kc_{2}(1 - \alpha_{2,2}) \right]\hat{T}_{2} - i\gamma_{q}\hat{q} = 0$
3. $(\omega m_{1}F_{1})\hat{T}_{1} + (\omega m_{1}F_{2})\hat{T}_{2} + (\omega - i m_{2}\gamma_{q})\hat{q} = 0$

---

## 3. Matrix Formulation

The system can be written as a homogeneous matrix equation $\mathbf{M}' \mathbf{v} = 0$, where $\mathbf{v} = [\hat{T}_1, \hat{T}_2, \hat{q}]^T$:

$$
\mathbf{M}' = 
\begin{bmatrix}
\omega(1 + F_{1}) - kc_{1}(1 - \alpha_{1,1}) & \omega F_{2} + kc_{2}\alpha_{1,2} & 0 \\
kc_{1}\alpha_{2,1} & \omega - kc_{2}(1 - \alpha_{2,2}) & -i\gamma_{q} \\
\omega m_{1}F_{1} & \omega m_{1}F_{2} & \omega - i m_{2}\gamma_{q}
\end{bmatrix}
$$

To define the dispersion relation cleanly, we define effective velocity variables:
* $U_{1} = c_{1}(1 - \alpha_{1,1})$
* $U_{2} = c_{2}(1 - \alpha_{2,2})$
* $V_{1} = c_{1}\alpha_{2,1}$
* $V_{2} = c_{2}\alpha_{1,2}$

---

## 4. Determinant Expansion

The dispersion relation requires $\det(\mathbf{M}') = 0$. Expanding along the first row:
$$\det(\mathbf{M}') = M_{33}(M_{11}M_{22} - M_{12}M_{21}) - M_{23}(M_{11}M_{32} - M_{12}M_{31})$$

The $2 \times 2$ sub-determinant $(M_{11}M_{22} - M_{12}M_{21})$ expands into a quadratic form in $\omega$:
$$A_0 \omega^2 - B_0 k \omega + C_0 k^2$$

Where the newly-defined polynomial coefficients are:
* $A_{0} = 1+F_{1}$
* $B_{0} = U_{1} + U_{2}(1+F_{1}) + V_{1}F_{2}$
* $C_{0} = U_{1}U_{2} - V_{1}V_{2}$

The second half of the determinant (the cross-coupling term) simplifies to:
$$i\omega m_{1}\gamma_{q} \left( \omega F_{2} - k W_0 \right)$$
Where we define the cross-forcing variable:
* $W_{0} = U_{1}F_{2} + V_{2}F_{1}$

---

## 5. Final Dispersion Relation $\omega(k)$

Combining all expanded terms, the explicit dispersion relation organizes into a cubic polynomial in terms of angular frequency $\omega$:

$$\Gamma_{3}\omega^{3} + \Gamma_{2}\omega^{2} + \Gamma_{1}\omega + \Gamma_{0} = 0$$

Where the final $\Gamma$ coefficients governing the system's normal modes are defined entirely by the given parameters and wavenumber $k$:
* **$\Gamma_{3}$** $= A_{0}$
* **$\Gamma_{2}$** $= - B_{0}k - i\gamma_{q}(m_{2}A_{0} - m_{1}F_{2})$
* **$\Gamma_{1}$** $= C_{0}k^{2} + i\gamma_{q}k(m_{2}B_{0} - m_{1}W_{0})$
* **$\Gamma_{0}$** $= - i\gamma_{q}m_{2}C_{0}k^{2}$

Solving this cubic equation for a given $k$ will yield the three distinct wave modes $\omega(k)$ of the system.