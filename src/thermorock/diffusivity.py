from .validation import validate_positive


def thermal_diffusivity(k, rho, cp):
    """
    Calculate thermal diffusivity.

    Parameters
    ----------
    k : float
        Thermal conductivity (W/mK)
    rho : float
        Density (kg/m³)
    cp : float
        Specific heat capacity (J/kgK)

    Returns
    -------
    float
        Thermal diffusivity (m²/s)
    """

    validate_positive(k, "Thermal conductivity")
    validate_positive(rho, "Density")
    validate_positive(cp, "Specific heat capacity")

    return k / (rho * cp)