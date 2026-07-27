"""
Numerical heat transfer solvers.
"""

from thermorock.subsurface import Subsurface

class HeatTransferSolver:
    """
    Solve heat transfer problems for a geological subsurface.
    """

    def __init__(
        self,
        subsurface: Subsurface,
        surface_temperature: float = 10.0,
        basal_heat_flow: float = 0.06,
    ):
        """
        Initialise the heat transfer solver.

        Parameters
        ----------
        subsurface : Subsurface
            Geological subsurface model.

        surface_temperature : float, optional
            Surface temperature (°C).

        basal_heat_flow : float, optional
            Basal heat flow (W/m²).
        """

        if not isinstance(subsurface, Subsurface):
            raise TypeError(
                "subsurface must be a Subsurface object."
            )

        if basal_heat_flow <= 0:
            raise ValueError(
                "basal_heat_flow must be positive."
            )

        self.subsurface = subsurface
        self.surface_temperature = surface_temperature
        self.basal_heat_flow = basal_heat_flow
        
    def steady_state_temperature_profile(
        self,
        depths: list[float],
    ) -> list[float]:
        """
        Calculate the steady-state temperature profile.

        Parameters
        ----------
        depths : list[float]
            Depths below the surface (m).

        Returns
        -------
        list[float]
            Temperatures (°C).
        """

        return self.subsurface.temperature_profile(depths)
        
        
    def steady_state_distribution(
        self,
        depth_interval: float = 100,
    ) -> tuple[list[float], list[float]]:
        """
        Calculate a steady-state temperature distribution.

        Parameters
        ----------
        depth_interval : float, optional
            Distance between calculated depths (m).

        Returns
        -------
        tuple[list[float], list[float]]
            Depths and temperatures.
        """

        if depth_interval <= 0:
            raise ValueError(
                "depth_interval must be positive."
            )

        depths = self.create_grid(depth_interval)

        temperatures = (
            self.steady_state_temperature_profile(
                depths
            )
        )

        return depths, temperatures 
        
        
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

  
   
    def finite_difference_steady_state(
        self,
        spacing: float = 100.0,
        max_iterations: int = 1000,
        tolerance: float = 1e-6,
    ) -> tuple[list[float], list[float]]:
        """
        Solve the one-dimensional steady-state heat equation
        using the finite-difference method.

        Parameters
        ----------
        spacing : float, optional
            Grid spacing (m).

        max_iterations : int, optional
            Maximum number of solver iterations.

        tolerance : float, optional
            Convergence tolerance.

        Returns
        -------
        tuple[list[float], list[float]]
            Grid depths and temperatures.
        """

        if spacing <= 0:
            raise ValueError("spacing must be positive.")

        grid = self.create_grid(spacing)

        gradient = self.subsurface.geothermal_gradient / 1000

        temperatures = [
            self.surface_temperature + gradient * depth
            for depth in grid
        ]

        # Surface boundary condition
        temperatures[0] = self.surface_temperature

        # Bottom boundary condition
        temperatures[-1] = (
            self.surface_temperature
            + gradient * grid[-1]
        )

        for _ in range(max_iterations):

            previous = temperatures.copy()

            for i in range(1, len(grid) - 1):
                temperatures[i] = (
                    previous[i - 1]
                    + previous[i + 1]
                ) / 2

            error = max(
                abs(a - b)
                for a, b in zip(previous, temperatures)
            )

            if error < tolerance:
                break

        return grid, temperatures