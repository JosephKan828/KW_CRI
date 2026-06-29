# Kuang (2008) + CRI Dispersion Relation Deduction

## 1. Governing Equations and Assumptions

Assuming the following parameter simplifications:

* $b_2 = 0$
* $\epsilon = 0$
* $\tau_j = 0$
* Radiative feedback only exists between the 1st mode vertical motion and the 2nd mode vertical motion, implying $\alpha_{1,1} =  \alpha_{1,2} =  \alpha_{2,2} = 0$.

The linearized system of governing equations is given by:

$$\frac{\partial T_1}{\partial t} + c_1 \frac{\partial T_1}{\partial x} = J_1$$

$$\frac{\partial T_2}{\partial t} + c_2 \frac{\partial T_2}{\partial x} = J_2 + \alpha_{2,1} c_1 \frac{\partial T_1}{\partial x}$$

$$\frac{\partial q}{\partial t} = m_1 J_1 + m_2 J_2$$

Where the moisture/heating source functions are parameterized as:

$$J_1 = -\frac{E}{b_1} \frac{\partial}{\partial t}\left[f T_1 + (1-f) T_2\right]$$

$$J_2 = -\gamma_q q$$

---

## 2. Normal Mode Ansatz & Fourier Transformation

We substitute the plane-wave solutions of the form:

$$\begin{pmatrix} T_1 \\ T_2 \\ q \end{pmatrix} = \sum_{\omega, k} \begin{pmatrix} \hat{T}_1 \\ \hat{T}_2 \\ \hat{q} \end{pmatrix} \exp(i\omega t - ikx)$$

Substituting these forms transforms the spatial and temporal derivatives into algebraic terms ($\partial_t → i\omega$, $\partial_x → -ik$):

$$
\begin{aligned}
i\omega \hat{T}_1 - ikc_1 \hat{T}_1 &= -\frac{E}{b_1} f (i\omega) \hat{T}_1 - \frac{E}{b_1} (1-f) (i\omega) \hat{T}_2 \\
i\omega \hat{T}_2 - ikc_2 \hat{T}_2 &= -\gamma_q \hat{q} - ikc_1 \alpha_{2,1} \hat{T}_1 \\
i\omega \hat{q} &= -\frac{E}{b_1} m_1 (i\omega) \left[f \hat{T}_1 + (1-f) \hat{T}_2\right] - m_2 \gamma_q \hat{q}
\end{aligned}
$$

### Rearranging Terms

Grouping the frequency $\omega$ terms on the left-hand side and the wavenumber $k$ and damping terms on the right-hand side:

$$
\begin{aligned}
i\omega \hat{T}_1 + \frac{E}{b_1} f (i\omega) \hat{T}_1 + \frac{E}{b_1} (1-f) (i\omega) \hat{T}_2 &= ikc_1 \hat{T}_1 \\
i\omega \hat{T}_2 &= -ikc_1 \alpha_{2,1} \hat{T}_1 + ikc_2 \hat{T}_2 - \gamma_q \hat{q} \\
\frac{E}{b_1} m_1 (i\omega) f \hat{T}_1 + \frac{E}{b_1} m_1 (i\omega) (1-f) \hat{T}_2 + i\omega \hat{q} &= -m_2 \gamma_q \hat{q}
\end{aligned}
$$

---

## 3. Matrix Formulation

The system can be compactly expressed as a generalized eigenvalue problem:

$$(i\omega) \mathbf{M} \vec{\nu} = \mathbf{L} \vec{\nu} \implies (i\omega \mathbf{M} - \mathbf{L}) \vec{\nu} = \vec{0}$$

Where the state vector is $\vec{\nu} = \begin{pmatrix} \hat{T}_1 & \hat{T}_2 & \hat{q} \end{pmatrix}^T$, and the matrices $\mathbf{M}$ and $\mathbf{L}$ are:

$$
\begin{aligned}
\mathbf{M} &= \begin{pmatrix} 1 + \frac{E}{b_1}f & \frac{E}{b_1}(1-f) & 0 \\ 0 & 1 & 0 \\ \frac{E}{b_1} f m_1 & \frac{E}{b_1}(1-f)m_1 & 1 \end{pmatrix}, \\
\mathbf{L} &= \begin{pmatrix} ikc_1 & 0 & 0 \\ -ikc_1 \alpha_{2,1} & ikc_2 & -\gamma_q \\ 0 & 0 & -m_2 \gamma_q \end{pmatrix}
\end{aligned}
$$

To simplify notation, we define:
$$\beta_1 = \frac{E}{b_1}f, \quad \beta_2 = \frac{E}{b_1}(1-f)$$

Thus, the characteristic matrix $(i\omega \mathbf{M} - \mathbf{L})$ becomes:

$$(i\omega \mathbf{M} - \mathbf{L}) = \begin{pmatrix} i(1+\beta_1)\omega - ikc_1 & i\beta_2\omega & 0 \\ ikc_1 \alpha_{2,1} & i\omega - ikc_2 & \gamma_q \\ im_1\beta_1\omega & im_1\beta_2\omega & i\omega + m_2\gamma_q \end{pmatrix}$$

---

## 4. Determinant and Characteristic Equation

For non-trivial solutions, we require $\det(i\omega \mathbf{M} - \mathbf{L}) = 0$. Expanding along the third column:

$$
\begin{aligned}
\det(i\omega \mathbf{M} - \mathbf{L}) &= -\gamma_q \begin{vmatrix} i(1+\beta_1)\omega - ikc_1 & i\beta_2\omega \\ im_1\beta_1\omega & im_1\beta_2\omega \end{vmatrix} \\
&\quad + (i\omega + m_2\gamma_q) \begin{vmatrix} i(1+\beta_1)\omega - ikc_1 & i\beta_2\omega \\ ikc_1\alpha_{2,1} & i\omega - ikc_2 \end{vmatrix} \\
&= 0
\end{aligned}
$$

Evaluating the $2 \times 2$ determinants and gathering terms by powers of $\omega$ yields the cubic dispersion relation:

$$
\begin{aligned}
-i(1+\beta_1)\omega^3 &+
\left\{
\begin{aligned}
&\left[ m_1\beta_2 - m_2(1+\beta_1) \right]\gamma_q \\
&+ ik\left[ c_1(1+\beta_2\alpha_{2,1}) + c_2(1+\beta_1) \right]
\end{aligned}
\right\} \omega^2 \\
&+
\left\{
\begin{aligned}
&k \left[ c_1(1+\beta_2\alpha_{2,1}) + c_2(1+\beta_1) \right] m_2\gamma_q \\
&- kc_1 m_1\beta_2\gamma_q - ik^2 c_1 c_2
\end{aligned}
\right\} \omega \\
&- k^2 c_1 c_2 m_2 \gamma_q = 0
\end{aligned}
$$

---

## 5. Case 1: Low-Frequency Approximation ($|\omega^2| \ll 1$)

Under the low-frequency limit, we neglect terms of $\omega^2$ and $\omega^3$. The characteristic equation simplifies to a linear equation in $\omega$:

$$
\left\{
\begin{aligned}
&k \left[ c_1(1+\beta_2\alpha_{2,1}) + c_2(1+\beta_1) \right] m_2\gamma_q \\
&- kc_1 m_1\beta_2\gamma_q - ik^2 c_1 c_2
\end{aligned}
\right\} \omega
- k^2 c_1 c_2 m_2 \gamma_q = 0
$$

Let us define the following coefficients:

* $C_{1r} = k \left[ c_1(1+\beta_2\alpha_{2,1}) + c_2(1+\beta_1) \right] m_2\gamma_q - kc_1 m_1\beta_2\gamma_q$
* $C_{1i} = -k^2 c_1 c_2$
* $C_0 = k^2 c_1 c_2 m_2 \gamma_q$

The equation becomes:
$$(C_{1r} + i C_{1i})\omega - C_0 = 0 \implies \omega = \frac{C_0}{C_{1r} + i C_{1i}} = \frac{C_0 C_{1r} - i C_0 C_{1i}}{C_{1r}^2 + C_{1i}^2}$$

### Instability

The growth rate (imaginary part of frequency, where instability corresponds to $-\omega_i > 0$ if defined as $e^{i\omega t}$) is:

$$-\omega_i = \frac{C_0 C_{1i}}{C_{1r}^2 + C_{1i}^2}$$

Substituting back the coefficients and factoring out common terms:

$$
-\omega_i = \frac{-m_2 \gamma_q}{1 + \frac{\gamma_q^2}{k^2 c_1^2 c_2^2}
\left\{
\begin{aligned}
&\left[c_1(1+\beta_2\alpha_{2,1}) + c_2(1+\beta_1)\right]m_2 \\
&- c_1 m_1 \beta_2
\end{aligned}
\right\}^2
}
$$

Expanding and simplifying the algebraic expression inside the denominator brackets yields the final analytical form for the low-frequency growth rate:

$$
-\omega_i = \frac{-m_2 \gamma_q}{1 + \frac{ \gamma_q^2}{k^2 c_1^2 c_2^2}
\left\{
\begin{aligned}
&c_1^2(1+\beta_2\alpha_{2,1})^2 m_2^2 + c_2^2(1+\beta_1)^2 m_2^2 + c_1^2 m_1^2 \beta_2^2 \\
&+ 2c_1 c_2 (1+\beta_1)(1+\beta_2\alpha_{2,1})m_2^2 \\
&- 2c_1^2 (1+\beta_2\alpha_{2,1})\beta_2m_1 m_2 - 2c_1 c_2(1+\beta_1)\beta_2 m_1 m_2
\end{aligned}
\right\}
}
$$

### Phase Speed

The phase speed is formulated as $c=\frac{1}{k} \left[ \frac{C_0 C_{1r}}{C_{1r}^2 + C_{1i}^2} \right]$:

$$
c = \frac{\frac{\gamma_q^2 m_2}{k^2 c_1 c_2}
\left\{
\begin{aligned}
&\left[c_1(1+\beta_2\alpha_{2,1}) + c_2(1+\beta_1)\right]m_2 \\
&- c_1 m_1 \beta_2
\end{aligned}
\right\}
}{
1 + \frac{\gamma_q^2}{k^2 c_1^2 c_2^2}
\left\{
\begin{aligned}
&c_1^2(1+\beta_2\alpha_{2,1})^2 m_2^2 + c_2^2(1+\beta_1)^2 m_2^2 + c_1^2 m_1^2 \beta_2^2 \\
&+ 2c_1 c_2 (1+\beta_1)(1+\beta_2\alpha_{2,1})m_2^2 \\
&- 2c_1^2 (1+\beta_2\alpha_{2,1})\beta_2m_1 m_2 - 2c_1 c_2(1+\beta_1)\beta_2 m_1 m_2
\end{aligned}
\right\}
}
$$

Considering the shortwave limit, the instability is approached to $-m_2 \gamma_q$, which is close to 0.7 day$^{-1}$, consistent with the figure below.

![diagram](../Figure/f_sensitivity_simplified/single/f=0.5.png)
