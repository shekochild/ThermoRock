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

        result = self._finite_difference_steady_state_result(
            spacing,
            max_iterations,
            tolerance,
        )

        return result["depth"], result["temperature"]

    def finite_difference_steady_state_with_info(
        self,
        spacing: float = 100.0,
        max_iterations: int = 1000,
        tolerance: float = 1e-6,
    ) -> dict[str, object]:
        """
        Solve the one-dimensional steady-state heat equation
        and return convergence diagnostics.

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
        dict[str, object]
            Depths, temperatures, iteration count,
            convergence status, and final error.
        """

        return self._finite_difference_steady_state_result(
            spacing,
            max_iterations,
            tolerance,
        )

    def _finite_difference_steady_state_result(
        self,
        spacing: float,
        max_iterations: int,
        tolerance: float,
    ) -> dict[str, object]:
        """
        Shared finite-difference implementation with diagnostics.
        """

        if spacing <= 0:
            raise ValueError("spacing must be positive.")

        grid = self.create_grid(spacing)
        conductivity = self.conductivity_profile(spacing)
        heat_source = self.radiogenic_heat_profile(spacing)

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

        iteration_count = 0
        converged = False
        final_error = 0.0

        for _ in range(max_iterations):

            previous = temperatures.copy()

            for i in range(1, len(grid) - 1):
                left_conductivity = (
                    conductivity[i - 1] + conductivity[i]
                ) / 2

                right_conductivity = (
                    conductivity[i] + conductivity[i + 1]
                ) / 2

                temperatures[i] = (
                    left_conductivity * previous[i - 1]
                    + right_conductivity * previous[i + 1]
                    # Internal heat generation raises the
                    # steady-state interior temperature.
                    + heat_source[i] * spacing**2
                ) / (
                    left_conductivity
                    + right_conductivity
                )

            final_error = max(
                abs(a - b)
                for a, b in zip(previous, temperatures)
            )

            iteration_count += 1

            if final_error < tolerance:
                converged = True
                break

        return {
            "depth": grid,
            "temperature": temperatures,
            "iterations": iteration_count,
            "converged": converged,
            "final_error": final_error,
        }
    
    def conductivity_profile(
        self,
        spacing: float,
    ) -> list[float]:
        """
        Return the thermal conductivity at every grid node.

        Parameters
        ----------
        spacing : float
            Grid spacing (m).

        Returns
        -------
        list[float]
            Thermal conductivity (W/m/K) at each node.
        """

        grid = self.create_grid(spacing)

        conductivity = []

        for depth in grid:

            # Handle the bottom node, which coincides with the
            # bottom depth of the final layer.
            if depth == self.subsurface.total_depth():
                layer = self.subsurface.layers[-1]
            else:
                layer = self.subsurface.get_layer_at_depth(depth)

            conductivity.append(
                layer.rock.thermal_conductivity
            )

        return conductivity


    def radiogenic_heat_profile(
        self,
        spacing: float,
    ) -> list[float]:
        """
        Return radiogenic heat production at each grid node.

        Parameters
        ----------
        spacing : float
            Grid spacing (m).

        Returns
        -------
        list[float]
            Radiogenic heat production (W/m³).
        """

        grid = self.create_grid(spacing)

        profile = []

        for depth in grid:

            if depth == self.subsurface.total_depth():
                layer = self.subsurface.layers[-1]
            else:
                layer = self.subsurface.get_layer_at_depth(depth)

            profile.append(
                layer.rock.radiogenic_heat_production
            )

        return profile
    
  
    def heat_flux_profile(
        self,
        spacing: float,
    ) -> tuple[list[float], list[float]]:
        """
        Calculate heat flux at each grid node using
        Fourier's Law.

        Parameters
        ----------
        spacing : float
            Grid spacing (m).

        Returns
        -------
        tuple[list[float], list[float]]
            Grid depths and heat fluxes (W/m²).
        """

        grid, temperatures = self.finite_difference_steady_state(
            spacing=spacing
        )

        conductivity = self.conductivity_profile(spacing)

        heat_flux = [0.0]

        for i in range(1, len(grid) - 1):

            gradient = (
                temperatures[i + 1]
                - temperatures[i - 1]
            ) / (2 * spacing)

            flux = -conductivity[i] * gradient

            heat_flux.append(flux)

        heat_flux.append(heat_flux[-1])

        return grid, heat_flux
    
    
    
    def temperature_at_depth(
        self,
        depth: float,
        spacing: float,
    ) -> float:
        """
        Interpolate the temperature at an arbitrary depth.

        Parameters
        ----------
        depth : float
            Depth (m).
        spacing : float
            Grid spacing (m).

        Returns
        -------
        float
            Interpolated temperature (°C).
        """

        grid, temperatures = self.finite_difference_steady_state(
            spacing=spacing
        )

        if depth < grid[0] or depth > grid[-1]:
            raise ValueError(
                "Depth is outside the computational domain."
            )

        for i in range(len(grid) - 1):
            if grid[i] <= depth <= grid[i + 1]:
                fraction = (
                    (depth - grid[i]) /
                    (grid[i + 1] - grid[i])
                )

                return (
                    temperatures[i]
                    + fraction *
                    (temperatures[i + 1] - temperatures[i])
                )

        return temperatures[-1]
