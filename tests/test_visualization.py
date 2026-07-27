"""
Unit tests for the visualization module.
"""

import matplotlib

matplotlib.use("Agg")

import pytest

from thermorock.heat_transfer import HeatTransferSolver
from thermorock.subsurface import Layer, Rock, Subsurface
from thermorock.visualization import Visualization


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


class TestVisualization:
    """Tests for the Visualization class."""

    def test_visualization_creation(self, model):
        solver = HeatTransferSolver(model)

        visualizer = Visualization(solver)

        assert visualizer.solver is solver

    def test_plot_temperature_profile(self, model):
        solver = HeatTransferSolver(model)
        visualizer = Visualization(solver)

        fig, ax = visualizer.plot_temperature_profile()

        assert fig is not None
        assert ax is not None

    def test_plot_heat_flux_profile(self, model):
        solver = HeatTransferSolver(model)
        visualizer = Visualization(solver)

        fig, ax = visualizer.plot_heat_flux_profile()

        assert fig is not None
        assert ax is not None
