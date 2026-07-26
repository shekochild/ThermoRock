"""
Unit tests for the heat transfer module.
"""

import pytest

from thermorock.heat_transfer import HeatTransferSolver
from thermorock.subsurface import (
    Rock,
    Layer,
    Subsurface,
)


@pytest.fixture
def model():
    sandstone = Rock(
        "Sandstone",
        2.5,
        2300,
        900,
        2e-6,
    )

    model = Subsurface()

    model.add_layer(
        Layer(
            0,
            1000,
            sandstone,
        )
    )

    return model


class TestHeatTransferSolver:
    """Tests for the HeatTransferSolver."""

    def test_create_solver(self, model):
        solver = HeatTransferSolver(model)

        assert solver.subsurface is model

    def test_invalid_subsurface(self):
        with pytest.raises(TypeError):
            HeatTransferSolver("invalid")
    
    
    def test_default_boundary_conditions(self, model):
        solver = HeatTransferSolver(model)

        assert solver.surface_temperature == 10.0
        assert solver.basal_heat_flow == 0.06


    def test_custom_boundary_conditions(self, model):
        solver = HeatTransferSolver(
            model,
            surface_temperature=15,
            basal_heat_flow=0.08,
        )

        assert solver.surface_temperature == 15
        assert solver.basal_heat_flow == 0.08


    def test_invalid_basal_heat_flow(self, model):
        with pytest.raises(ValueError):
            HeatTransferSolver(
                model,
                basal_heat_flow=0,
            )        