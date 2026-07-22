import pytest

from thermorock.geothermal import (
    geothermal_gradient,
    temperature_at_depth,
    heat_flow,
)

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
       geothermal_gradient(
    surface_temperature=10,
    reservoir_temperature=100,
    depth=0,
)


def test_geothermal_gradient_negative_depth():
    """Depth cannot be negative."""

    with pytest.raises(ValueError):
        geothermal_gradient(
    surface_temperature=10,
    reservoir_temperature=100,
    depth=-3,
)
        
def test_geothermal_gradient_non_numeric_depth():
    """Test that a non-numeric depth raises a TypeError."""

    with pytest.raises(TypeError):
        geothermal_gradient(
    surface_temperature=10,
    reservoir_temperature=100,
    depth="three",
)
def test_temperature_at_depth():
    """Test temperature at a specified depth."""

    temperature = temperature_at_depth(
        surface_temperature=12,
        geothermal_gradient=30,
        depth=3,
    )

    assert temperature == pytest.approx(102.0)   
def test_temperature_at_depth_zero_depth():
    """Test that zero depth raises a ValueError."""

    with pytest.raises(ValueError):
        temperature_at_depth(
            surface_temperature=12,
            geothermal_gradient=30,
            depth=0,
        )
def test_temperature_at_depth_negative_gradient():
    """Test that a negative geothermal gradient raises a ValueError."""

    with pytest.raises(ValueError):
        temperature_at_depth(
            surface_temperature=12,
            geothermal_gradient=-30,
            depth=3,
        )
def test_temperature_at_depth_non_numeric_depth():
    """Test that a non-numeric depth raises a TypeError."""

    with pytest.raises(TypeError):
        temperature_at_depth(
            surface_temperature=12,
            geothermal_gradient=30,
            depth="three",
        )              

def test_heat_flow():
    assert heat_flow(
        thermal_conductivity=2.5,
        geothermal_gradient=30,
    ) == pytest.approx(75.0)
def test_heat_flow_zero_thermal_conductivity():
    with pytest.raises(ValueError):
        heat_flow(
            thermal_conductivity=0,
            geothermal_gradient=30,
        )
def test_heat_flow_zero_geothermal_gradient():
    with pytest.raises(ValueError):
        heat_flow(
            thermal_conductivity=2.5,
            geothermal_gradient=0,
        )
def test_heat_flow_non_numeric_input():
    with pytest.raises(TypeError):
        heat_flow(
            thermal_conductivity="high",
            geothermal_gradient=30,
        )
def test_heat_flow_negative_thermal_conductivity():
    """Test that a negative thermal conductivity raises a ValueError."""

    with pytest.raises(ValueError):
        heat_flow(
            thermal_conductivity=-2.5,
            geothermal_gradient=30,
        )