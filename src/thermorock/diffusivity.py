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
    return k / (rho * cp)