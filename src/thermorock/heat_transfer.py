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