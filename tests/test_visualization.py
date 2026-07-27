"""
Unit tests for the visualization module.
"""

from pathlib import Path

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

    def test_plot_stratigraphy(self, model):
        solver = HeatTransferSolver(model)
        visualizer = Visualization(solver)

        fig, ax = visualizer.plot_stratigraphy()

        assert fig is not None
        assert ax is not None

    def test_plot_geothermal_profile(self, model):
        solver = HeatTransferSolver(model)
        visualizer = Visualization(solver)

        fig, (ax1, ax2) = visualizer.plot_geothermal_profile()

        assert fig is not None
        assert ax1 is not None
        assert ax2 is not None

    def test_plot_complete_geothermal_profile(self, model):
        solver = HeatTransferSolver(model)
        visualizer = Visualization(solver)

        fig, (ax1, ax2, ax3) = (
            visualizer.plot_complete_geothermal_profile()
        )

        assert fig is not None
        assert ax1 is not None
        assert ax2 is not None
        assert ax3 is not None

    def test_save_figure(self, model, tmp_path):
        solver = HeatTransferSolver(model)
        visualizer = Visualization(solver)

        fig, _ = visualizer.plot_temperature_profile()
        output = tmp_path / "figures" / "temperature.png"

        saved_path = visualizer.save_figure(
            fig,
            output,
        )

        assert isinstance(saved_path, Path)
        assert saved_path.exists()
        assert saved_path.suffix == ".png"
