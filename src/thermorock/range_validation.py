from .database import get_rock_properties


def validate_property_range(value, rock_type, property_name):
    """
    Validate that a rock property is within the
    expected range for a given rock type.

    Parameters
    ----------
    value : float
        Property value to validate.
    rock_type : str
        Rock type name.
    property_name : str
        Property to validate
        (e.g., "conductivity", "density",
        or "heat_capacity").

    Raises
    ------
    ValueError
        If the property value is outside the
        expected range.
    """

    properties = get_rock_properties(rock_type)

    if property_name not in properties:
        raise ValueError(
            f"'{property_name}' is not available for {rock_type}."
        )

    min_value, max_value = properties[property_name]

    if value < min_value or value > max_value:
        raise ValueError(
            f"{property_name.capitalize()} for {rock_type} "
            f"must be between {min_value} and {max_value}."
        )