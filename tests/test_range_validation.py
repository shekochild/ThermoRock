import pytest

from thermorock.range_validation import validate_property_range


def test_valid_conductivity():
    """
    Verify that a valid thermal conductivity
    passes range validation.
    """
    validate_property_range(
        3.0,
        "granite",
        "conductivity"
    )


def test_invalid_conductivity():
    """
    Verify that an invalid thermal conductivity
    raises a ValueError.
    """
    with pytest.raises(ValueError):
        validate_property_range(
            10.0,
            "granite",
            "conductivity"
        )


def test_valid_density():
    """
    Verify that a valid density
    passes range validation.
    """
    validate_property_range(
        2700,
        "granite",
        "density"
    )


def test_invalid_density():
    """
    Verify that an invalid density
    raises a ValueError.
    """
    with pytest.raises(ValueError):
        validate_property_range(
            3500,
            "granite",
            "density"
        )


def test_valid_heat_capacity():
    """
    Verify that a valid heat capacity
    passes range validation.
    """
    validate_property_range(
        800,
        "granite",
        "heat_capacity"
    )


def test_invalid_heat_capacity():
    """
    Verify that an invalid heat capacity
    raises a ValueError.
    """
    with pytest.raises(ValueError):
        validate_property_range(
            1500,
            "granite",
            "heat_capacity"
        )


def test_invalid_property_name():
    """
    Verify that requesting a property
    that does not exist raises a ValueError.
    """
    with pytest.raises(ValueError):
        validate_property_range(
            10,
            "granite",
            "permeability"
        )