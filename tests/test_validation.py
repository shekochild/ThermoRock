import pytest

from thermorock.validation import validate_positive


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