import pytest

from thermorock.validation import (
    validate_positive,
    validate_positive_inputs,
)


def test_positive_value():
    validate_positive(10, "Conductivity")


def test_negative_value():
    with pytest.raises(ValueError):
        validate_positive(-5, "Conductivity")
def test_zero_value():
    with pytest.raises(ValueError):
        validate_positive(0, "Conductivity")
def test_non_numeric_value():
    with pytest.raises(TypeError):
        validate_positive("abc", "Conductivity")  

def test_validate_positive_inputs():
    """Test validation of multiple positive inputs."""

    validate_positive_inputs(
        depth=3,
        geothermal_gradient=30,
        conductivity=2.5,
    )             
def test_validate_positive_inputs_negative_value():
    """Test that negative values raise a ValueError."""

    with pytest.raises(ValueError):
        validate_positive_inputs(
            depth=-3,
            geothermal_gradient=30,
        )