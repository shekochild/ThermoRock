from .database import get_rock_properties


def validate_conductivity_range(value, rock_type):
    """
    Validate conductivity against the expected
    range for a given rock type.

    Parameters
    ----------
    value : float
        Thermal conductivity (W/mK)
    rock_type : str
        Rock type name.

    Raises
    ------
    ValueError
        If conductivity is outside the
        expected range.
    """
    properties = get_rock_properties(rock_type)

    min_k, max_k = properties["conductivity"]

    if value < min_k or value > max_k:
        raise ValueError(
            f"Conductivity for {rock_type} "
            f"must be between {min_k} and {max_k} W/mK."
        )