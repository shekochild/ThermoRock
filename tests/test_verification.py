"""
Verification tests for ThermoRock numerical solvers.
"""

import pytest

from thermorock.heat_transfer import HeatTransferSolver
from thermorock.subsurface import Layer, Rock, Subsurface


def test_finite_difference_matches_linear_analytical_solution():
    """
    Verify the finite-difference solver against the analytical
    source-free homogeneous steady-state solution.
    """

    surface_temperature = 10.0
    geothermal_gradient = 30.0
    spacing = 100.0
    tolerance = 1e-10

    rock = Rock(
        "Homogeneous rock",
        thermal_conductivity=2.5,
        density=2500,
        heat_capacity=1000,
        radiogenic_heat_production=0.0,
    )

    subsurface = Subsurface(
        surface_temperature=surface_temperature,
        geothermal_gradient=geothermal_gradient,
    )

    subsurface.add_layer(
        Layer(
            0,
            1000,
            rock,
        )
    )

    solver = HeatTransferSolver(
        subsurface,
        surface_temperature=surface_temperature,
    )

    result = solver.finite_difference_steady_state_with_info(
        spacing=spacing,
        tolerance=tolerance,
    )

    grid = result["depth"]
    temperatures = result["temperature"]

    gradient_per_metre = geothermal_gradient / 1000

    # For homogeneous, source-free steady conduction, temperature
    # varies linearly with depth.
    analytical_temperatures = [
        surface_temperature + gradient_per_metre * depth
        for depth in grid
    ]

    assert temperatures == pytest.approx(
        analytical_temperatures,
        abs=1e-8,
    )

    assert result["converged"] is True
    assert result["iterations"] > 0
    assert result["final_error"] < tolerance
