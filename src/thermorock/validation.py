def validate_positive(value, name):
    """
    Validate that a parameter is positive.
    """

    if value <= 0:
        raise ValueError(
            f"{name} must be positive."
        )