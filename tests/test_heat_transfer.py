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