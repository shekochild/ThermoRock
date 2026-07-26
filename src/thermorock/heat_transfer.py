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
    ):
        """
        Initialise the heat transfer solver.

        Parameters
        ----------
        subsurface : Subsurface
            Geological subsurface model.
        """

        if not isinstance(subsurface, Subsurface):
            raise TypeError(
                "subsurface must be a Subsurface object."
            )

        self.subsurface = subsurface