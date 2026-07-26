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

        return [
            self.subsurface.temperature_at_depth(depth)
            for depth in depths
        ]
        
        
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

        maximum_depth = self.subsurface.total_depth()

        depths = []

        depth = 0.0

        while depth <= maximum_depth:
            depths.append(depth)
            depth += depth_interval

        temperatures = (
            self.steady_state_temperature_profile(
                depths
            )
        )

        return depths, temperatures 
        
        
        