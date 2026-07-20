import pytest

from thermorock.geothermal import geothermal_gradient


def test_geothermal_gradient():
    """Test geothermal gradient calculation."""

    gradient = geothermal_gradient(
        surface_temperature=10,
        reservoir_temperature=100,
        depth=3,
    )

    assert abs(gradient - 30.0) < 1e-12


def test_geothermal_gradient_zero_depth():
    """Test that zero depth raises a ValueError."""

    with pytest.raises(ValueError):
        geothermal_gradient(10, 100, 0)


def test_geothermal_gradient_negative_depth():
    """Depth cannot be negative."""

    with pytest.raises(ValueError):
        geothermal_gradient(10, 100, -3)
        
def test_geothermal_gradient_non_numeric_depth():
    """Test that a non-numeric depth raises a TypeError."""

    with pytest.raises(TypeError):
        geothermal_gradient( 10, 100,"three",
        )