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
            
    def test_steady_state_temperature_profile(self, model):
        solver = HeatTransferSolver(model)

        profile = solver.steady_state_temperature_profile(
            [0, 500, 1000]
        )

        assert len(profile) == 3

        assert profile[0] == 10.0
        assert profile[1] == 25.0
        assert profile[2] == 40.0


    def test_empty_temperature_profile(self, model):
        solver = HeatTransferSolver(model)

        assert (
            solver.steady_state_temperature_profile([])
            == []
        )     
        
    def test_steady_state_distribution(self, model):
        solver = HeatTransferSolver(model)

        depths, temperatures = (
            solver.steady_state_distribution(
                depth_interval=500
            )
        )

        assert len(depths) == len(temperatures)

        assert depths[0] == 0
        assert temperatures[0] == 10.0


    def test_invalid_depth_interval(self, model):
        solver = HeatTransferSolver(model)

        with pytest.raises(ValueError):
            solver.steady_state_distribution(
                depth_interval=0
            ) 
            
    def create_grid(
        self,
        spacing: float,
    ) -> list[float]:
        """
        Create a one-dimensional computational grid.

        Parameters
        ----------
        spacing : float
            Distance between grid nodes (m).

        Returns
        -------
        list[float]
            Grid node depths (m).
        """

        if spacing <= 0:
            raise ValueError(
                "spacing must be positive."
            )

        maximum_depth = self.subsurface.total_depth()

        grid = []

        depth = 0.0

        while depth <= maximum_depth:
            grid.append(depth)
            depth += spacing

        return grid        

   
    def test_finite_difference_steady_state(self, model):
        solver = HeatTransferSolver(model)

        grid, temperatures = (
            solver.finite_difference_steady_state(
                spacing=250
            )
        )

        assert len(grid) == len(temperatures)

        assert temperatures[0] == 10.0

        assert temperatures[-1] > temperatures[0]


    def test_finite_difference_solution_is_monotonic(self, model):
        solver = HeatTransferSolver(model)

        _, temperatures = (
            solver.finite_difference_steady_state()
        )

        assert all(
            temperatures[i] <= temperatures[i + 1]
            for i in range(len(temperatures) - 1)
        )
        
    def test_conductivity_profile_length(self, model):
        solver = HeatTransferSolver(model)

        profile = solver.conductivity_profile(
            spacing=100
        )

        assert len(profile) == len(
            solver.create_grid(100)
        )


    def test_conductivity_profile_values(self):
        sandstone = Rock(
            "Sandstone",
            thermal_conductivity=2.5,
            density=2500,
            heat_capacity=1000,
            radiogenic_heat_production=1e-6,
        )

        shale = Rock(
            "Shale",
            thermal_conductivity=1.5,
            density=2600,
            heat_capacity=900,
            radiogenic_heat_production=1e-6,
        )

        model = Subsurface()

        model.add_layer(
            Layer(0, 500, sandstone)
        )

        model.add_layer(
            Layer(500, 1000, shale)
        )

        solver = HeatTransferSolver(model)

        profile = solver.conductivity_profile(
            spacing=250
        )

        assert profile == [
            2.5,
            2.5,
            1.5,
            1.5,
            1.5,
        ]     
        
    def test_variable_conductivity_solver(self):
        sandstone = Rock(
            "Sandstone",
            thermal_conductivity=2.5,
            density=2500,
            heat_capacity=1000,
            radiogenic_heat_production=1e-6,
        )

        shale = Rock(
            "Shale",
            thermal_conductivity=1.5,
            density=2600,
            heat_capacity=900,
            radiogenic_heat_production=1e-6,
        )

        model = Subsurface()

        model.add_layer(
            Layer(0, 500, sandstone)
        )

        model.add_layer(
            Layer(500, 1000, shale)
        )

        solver = HeatTransferSolver(model)

        grid, temperatures = (
            solver.finite_difference_steady_state(
                spacing=250
            )
        )

        assert len(grid) == len(temperatures)

        assert temperatures[0] == 10.0

        assert temperatures[-1] > temperatures[0]
            
            
    def test_radiogenic_heat_profile(self, model):
        solver = HeatTransferSolver(model)

        profile = solver.radiogenic_heat_profile(
            spacing=100
        )

        assert len(profile) == len(
            solver.create_grid(100)
        )


    def test_solver_with_radiogenic_heat(self, model):
        solver = HeatTransferSolver(model)

        grid, temperatures = (
            solver.finite_difference_steady_state(
                spacing=250
            )
        )

        assert len(grid) == len(temperatures)

        assert temperatures[0] == 10.0

        assert temperatures[-1] > temperatures[0]