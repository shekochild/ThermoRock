def validate_positive(value, name):
    """
    Validate that a parameter is positive.
    """

    if value <= 0:
        raise ValueError(
            f"{name} must be positive."
        )
def validate_positive(value, name):
    """
    Validate that a parameter is numeric and positive.
    """

    if not isinstance(value, (int, float)):
        raise TypeError(
            f"{name} must be a number."
        )

    if value <= 0:
        raise ValueError(
            f"{name} must be positive."
        )     

def validate_positive_inputs(**kwargs):
    """
    Validate that multiple inputs are numeric and positive.

    Parameters
    ----------
    **kwargs
        Named input values to validate.

    Raises
    ------
    TypeError
        If any input is not numeric.
    ValueError
        If any input is zero or negative.
    """
    for name, value in kwargs.items():
        validate_positive(value, name)