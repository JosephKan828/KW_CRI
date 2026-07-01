# Elimination of $\beta_2$ in the Full CRI Dispersion Relation

This note documents the limiting case in which

$$
\beta_2 = 0
$$

is applied to the full cubic dispersion relation. The purpose is to show that, in this limit, the full dispersion relation factorizes into three independent branches: two neutral propagating modes and one non-propagating pure growth/decay mode.

---

## 1. Starting Point: Full Dispersion Relation

The full cubic dispersion relation is

$$
\begin{aligned}
-i(1+\beta_1)\omega^3
&+
\left\{
\begin{aligned}
&\left[ m_1\beta_2 - m_2(1+\beta_1) \right]\gamma_q \\
&+ ik\left[ c_1(1+\beta_2\alpha_{2,1}) + c_2(1+\beta_1) \right]
\end{aligned}
\right\}\omega^2 \\
&+
\left\{
\begin{aligned}
&k \left[ c_1(1+\beta_2\alpha_{2,1}) + c_2(1+\beta_1) \right] m_2\gamma_q \\
&- kc_1m_1\beta_2\gamma_q - ik^2c_1c_2
\end{aligned}
\right\}\omega \\
&- k^2c_1c_2m_2\gamma_q
=0.
\end{aligned}
$$

The normal-mode convention is

$$
\exp(i\omega t - ikx),
$$

and the complex frequency is written as

$$
\omega = \omega_r + i\omega_i.
$$

Therefore,

$$
\exp(i\omega t)
=
\exp(i\omega_r t-\omega_i t).
$$

With this convention, the growth rate is

$$
-\omega_i.
$$

---

## 2. Applying the Limit \(\beta_2=0\)

We now impose

$$
\beta_2 = 0.
$$

Then the following terms vanish:

$$
m_1\beta_2 = 0,
$$

$$
\beta_2\alpha_{2,1}=0,
$$

and

$$
c_1m_1\beta_2 = 0.
$$

Therefore,

$$
c_1(1+\beta_2\alpha_{2,1})
\rightarrow
c_1,
$$

and

$$
m_1\beta_2 - m_2(1+\beta_1)
\rightarrow
-m_2(1+\beta_1).
$$

Substituting these into the full cubic relation gives

$$
\boxed{
\begin{aligned}
-i(1+\beta_1)\omega^3
&+
\left\{
-m_2(1+\beta_1)\gamma_q
+
ik\left[c_1+c_2(1+\beta_1)\right]
\right\}\omega^2 \\
&+
\left\{
k\left[c_1+c_2(1+\beta_1)\right]m_2\gamma_q
-
ik^2c_1c_2
\right\}\omega \\
&-
k^2c_1c_2m_2\gamma_q
=0.
\end{aligned}
}
$$

---

## 3. Coefficient Form

The simplified cubic can be written as

$$
A_3\omega^3 + A_2\omega^2 + A_1\omega + A_0 = 0,
$$

where

$$
A_3 = -i(1+\beta_1),
$$

$$
A_2 =
-m_2(1+\beta_1)\gamma_q
+
ik\left[c_1+c_2(1+\beta_1)\right],
$$

$$
A_1 =
k\left[c_1+c_2(1+\beta_1)\right]m_2\gamma_q
-
ik^2c_1c_2,
$$

and

$$
A_0 =
-k^2c_1c_2m_2\gamma_q.
$$

---

## 4. Factorized Form

The simplified cubic can be factorized as

$$
\boxed{
\left[i(1+\beta_1)\omega-ikc_1\right]
\left[i\omega-ikc_2\right]
\left[i\omega+m_2\gamma_q\right]
=0.
}
$$

Equivalently,

$$
\boxed{
i\left[(1+\beta_1)\omega-kc_1\right]
\cdot
i\left[\omega-kc_2\right]
\cdot
\left[i\omega+m_2\gamma_q\right]
=0.
}
$$

---

## 5. Verification by Expansion

First multiply the first two factors:

$$
\left[i(1+\beta_1)\omega-ikc_1\right]
\left[i\omega-ikc_2\right]
=
-\left[(1+\beta_1)\omega-kc_1\right]
\left[\omega-kc_2\right].
$$

Expanding,

$$
\begin{aligned}
&-\left[(1+\beta_1)\omega-kc_1\right]
\left[\omega-kc_2\right] \\
&=
-(1+\beta_1)\omega^2
+
k\left[c_1+c_2(1+\beta_1)\right]\omega
-
k^2c_1c_2.
\end{aligned}
$$

Now multiply by the third factor:

$$
i\omega + m_2\gamma_q.
$$

Thus,

$$
\begin{aligned}
&\left\{
-(1+\beta_1)\omega^2
+
k\left[c_1+c_2(1+\beta_1)\right]\omega
-
k^2c_1c_2
\right\}
\left(i\omega+m_2\gamma_q\right)
\\
&=
-i(1+\beta_1)\omega^3
\\
&\quad+
\left\{
-m_2(1+\beta_1)\gamma_q
+
ik\left[c_1+c_2(1+\beta_1)\right]
\right\}\omega^2
\\
&\quad+
\left\{
k\left[c_1+c_2(1+\beta_1)\right]m_2\gamma_q
-
ik^2c_1c_2
\right\}\omega
\\
&\quad
-
k^2c_1c_2m_2\gamma_q.
\end{aligned}
$$

This exactly recovers the simplified cubic dispersion relation obtained after setting \(\beta_2=0\).

---

## 6. Roots of the Simplified Dispersion Relation

Because the dispersion relation factorizes into three factors, each factor gives one root.

### Root 1: First Propagating Mode

From

$$
i(1+\beta_1)\omega-ikc_1=0,
$$

we obtain

$$
(1+\beta_1)\omega-kc_1=0.
$$

Therefore,

$$
\boxed{
\omega_1=\frac{kc_1}{1+\beta_1}.
}
$$

The real and imaginary parts are

$$
\omega_{1,r}=\frac{kc_1}{1+\beta_1},
\qquad
\omega_{1,i}=0.
$$

The phase speed is

$$
c_{p,1}
=
\frac{\omega_{1,r}}{k}
=
\boxed{
\frac{c_1}{1+\beta_1}
}.
$$

The growth rate is

$$
-\omega_{1,i}=0.
$$

Therefore, this branch is a neutral propagating mode.

---

### Root 2: Second Propagating Mode

From

$$
i\omega-ikc_2=0,
$$

we obtain

$$
\omega-kc_2=0.
$$

Therefore,

$$
\boxed{
\omega_2=kc_2.
}
$$

The real and imaginary parts are

$$
\omega_{2,r}=kc_2,
\qquad
\omega_{2,i}=0.
$$

The phase speed is

$$
c_{p,2}
=
\frac{\omega_{2,r}}{k}
=
\boxed{
c_2
}.
$$

The growth rate is

$$
-\omega_{2,i}=0.
$$

Therefore, this branch is also a neutral propagating mode.

---

### Root 3: Non-Propagating Growth/Decay Mode

From

$$
i\omega+m_2\gamma_q=0,
$$

we obtain

$$
i\omega=-m_2\gamma_q.
$$

Dividing by \(i\),

$$
\omega=\frac{-m_2\gamma_q}{i}.
$$

Since

$$
\frac{1}{i}=-i,
$$

we get

$$
\boxed{
\omega_3=im_2\gamma_q.
}
$$

Thus,

$$
\omega_{3,r}=0,
\qquad
\omega_{3,i}=m_2\gamma_q.
$$

The phase speed is

$$
c_{p,3}
=
\frac{\omega_{3,r}}{k}
=
0.
$$

The growth rate is

$$
-\omega_{3,i}
=
-m_2\gamma_q.
$$

Therefore, this branch is non-propagating because

$$
\omega_{3,r}=0.
$$

It is a pure growth or decay mode depending on the sign of \(m_2\gamma_q\).

If

$$
m_2<0,
\qquad
\gamma_q>0,
$$

then

$$
-\omega_{3,i}
=
-m_2\gamma_q
>0,
$$

so the mode is unstable.

If

$$
m_2>0,
\qquad
\gamma_q>0,
$$

then

$$
-\omega_{3,i}<0,
$$

so the mode decays.

---

## 7. Physical Interpretation

When

$$
\beta_2=0,
$$

the first-mode heating feedback does not project onto the second-mode temperature component through the \(\beta_2\)-dependent terms. In the full dispersion relation, the CRI-related coupling involving \(\alpha_{2,1}\) appears through the product

$$
\beta_2\alpha_{2,1}.
$$

Therefore, when

$$
\beta_2=0,
$$

the \(\alpha_{2,1}\)-dependent CRI correction disappears from the dispersion relation.

The three branches become dynamically separated:

| Branch | Root | Phase Speed | Growth Rate | Interpretation |
|---|---:|---:|---:|---|
| 1 | \(\omega_1=\dfrac{kc_1}{1+\beta_1}\) | \(\dfrac{c_1}{1+\beta_1}\) | \(0\) | neutral propagating mode |
| 2 | \(\omega_2=kc_2\) | \(c_2\) | \(0\) | neutral propagating mode |
| 3 | \(\omega_3=im_2\gamma_q\) | \(0\) | \(-m_2\gamma_q\) | non-propagating pure growth/decay mode |

Thus, in the \(\beta_2=0\) limit,

$$
\boxed{
\text{two roots are neutral propagating modes, and one root is a non-propagating pure growth/decay mode.}
}
$$

It is better to describe the third branch as a non-propagating growth/decay mode, rather than a standing oscillator, because

$$
\omega_{3,r}=0,
$$

so the mode does not oscillate in time.

---

## 8. Summary

Setting

$$
\beta_2=0
$$

reduces the full cubic dispersion relation to

$$
\boxed{
\begin{aligned}
-i(1+\beta_1)\omega^3
&+
\left\{
-m_2(1+\beta_1)\gamma_q
+
ik\left[c_1+c_2(1+\beta_1)\right]
\right\}\omega^2 \\
&+
\left\{
k\left[c_1+c_2(1+\beta_1)\right]m_2\gamma_q
-
ik^2c_1c_2
\right\}\omega \\
&-
k^2c_1c_2m_2\gamma_q
=0.
\end{aligned}
}
$$

This can be factorized as

$$
\boxed{
\left[i(1+\beta_1)\omega-ikc_1\right]
\left[i\omega-ikc_2\right]
\left[i\omega+m_2\gamma_q\right]
=0.
}
$$

The three roots are

$$
\boxed{
\omega_1=\frac{kc_1}{1+\beta_1},
\qquad
\omega_2=kc_2,
\qquad
\omega_3=im_2\gamma_q.
}
$$

Therefore, the \(\beta_2=0\) limit produces two neutral propagating modes and one non-propagating pure growth/decay mode.
