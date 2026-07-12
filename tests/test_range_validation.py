import pytest

from thermorock.range_validation import validate_conductivity_range


def test_valid_granite_conductivity():
    """
    Verify that a conductivity value within the
    expected granite range passes validation.
    """
    validate_conductivity_range(3.0, "granite")


def test_invalid_granite_conductivity():
    """
    Verify that a conductivity value outside the
    expected granite range raises a ValueError.
    """
    with pytest.raises(ValueError):
        validate_conductivity_range(10.0, "granite")