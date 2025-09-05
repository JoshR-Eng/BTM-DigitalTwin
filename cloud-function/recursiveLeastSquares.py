# Cloud/recursiveLeastSquares.py
class RLS:
    """
    An adaptive filter algorithm that recursively finds the coefficients that minimize 
    a weighted linear least squares cost function relating to the input signals.

        These specific args estimate internal resistance parameter of battery for MPC controller
        Update() method is the general formualas for RLS
        compute_regressors_power is only for my Energy Balance model

        Arg - forgetting_factor
            <1 exponentially downweights previous data

    """
    def __init__(self, forgetting_factor: float = 0.995):
        self.forgetting_factor = forgetting_factor
        
        self.Cm = 76.8 * 520    # Variables unique to my model
        self.R_th = 0.23        # |
        self.T_ambient = 295.0  # |_

    def compute_regressors_power(self, new_temperature, prev_temperature, cooling_power, current, dt):
        """
        Based on Energy balance equation:
            Cm * dT/dt = (I^2 * r) - P_cool - (T-Tamb)/Rth
        Rearranged into form: y = φ r
            (Cm/dt)*(T_n+1 - T_n) + P_cool + (1/Rth)*(T-Tamb) = I^2 * r
        """
        # True power from measured values
        y = (
            (self.Cm / dt) * (new_temperature - prev_temperature) + 
            cooling_power + (prev_temperature - self.T_ambient) / self.R_th
        )
        # Regressor
        phi = current ** 2

        return phi, y

    def update(self, phi, y, r, p):
        """Perform one RLS update step using stored state."""

        if r is None or p is None:
            raise ValueError("Inital conditions not defined")

        # Innovation
        e = y - (phi * r)

        # Gain
        k = (p * phi) / (self.forgetting_factor + (phi * phi * p))

        # Update estimates
        updated_r = r + (k * e)
        updated_p = (1 - (k * phi)) * (p / self.forgetting_factor)

        return {"r": updated_r, "p": updated_p, "e": e}
