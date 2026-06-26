"""System parameters and coefficients for the atmospheric wave dispersion relation."""

from dataclasses import dataclass

@dataclass
class WaveParameters:
    """
    Data model for atmospheric wave dispersion system parameters.

    The alpha CRI coupling parameters are fixed structurally and scale 
    dynamically based on the `scaling_factor`.

    Attributes:
        c1 (float): Phase speed of the first vertical mode (m/s). Default: 1.0.
        c2 (float): Phase speed of the second vertical mode (m/s). Default: 0.5.
        scaling_factor (float): Dimensionless scaling factor for cross-mode feedbacks. Default: 0.1.
        F (float): Bulk heating parameter. Default: 4.0.
        f (float): Fraction of heating applied to the first mode (0.0 to 1.0). Default: 0.5.
        b1 (float): Thermodynamic constant. Default: 1.0.
        m1 (float): Moisture coupling parameter for mode 1. Default: 0.3.
        m2 (float): Moisture coupling parameter for mode 2. Default: 1.0.
        gamma_q (float): Moisture relaxation rate (s^-1). Default: 0.7.
    """

    c1: float = 1.0
    c2: float = 0.5
    scaling_factor: float = 0.1
    F: float = 4.0
    f: float = 0.5
    b1: float = 1.0
    m1: float = 0.3
    m2: float = 1.0
    gamma_q: float = 0.7

    def __post_init__(self) -> None:
        """Validates constraints immediately after initialization."""
        # Validate constraint for 'f'
        if not (0.0 <= self.f <= 1.0):
            raise ValueError(f"Fraction of heating 'f' must be in range [0.0, 1.0]. Got: {self.f}")

    # ---------------------------------------------------------
    # Fixed Alpha Parameters (Scaled dynamically)
    # ---------------------------------------------------------

    @property
    def alpha_11(self) -> float:
        """CRI coupling parameter (mode 1 to 1)"""
        return 0.0763 * self.scaling_factor

    @property
    def alpha_12(self) -> float:
        """CRI coupling parameter (mode 2 to 1)"""
        return 0.118 * self.scaling_factor

    @property
    def alpha_21(self) -> float:
        """CRI coupling parameter (mode 1 to 2)"""
        return -0.0585 * self.scaling_factor

    @property
    def alpha_22(self) -> float:
        """CRI coupling parameter (mode 2 to 2)"""
        return -0.141 * self.scaling_factor

    # ---------------------------------------------------------
    # Derived Properties based on the Derivation Document
    # ---------------------------------------------------------

    @property
    def F1(self) -> float:
        """Fractional forcing coefficient 1"""
        return (self.F * self.f) / self.b1

    @property
    def F2(self) -> float:
        """Fractional forcing coefficient 2"""
        return (self.F * (1 - self.f)) / self.b1

    @property
    def Delta_alpha(self) -> float:
        return (1-self.alpha_11)*(1-self.alpha_22) - \
            self.alpha_12 * self.alpha_21
