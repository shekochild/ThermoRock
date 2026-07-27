"""
Visualization utilities for ThermoRock.
"""

import matplotlib.pyplot as plt

from thermorock.heat_transfer import HeatTransferSolver


class Visualization:
    """
    Contains visualization utilities for ThermoRock numerical simulations.
    """

    def __init__(self, solver: HeatTransferSolver):
        """
        Initialize a visualization helper.

        Parameters
        ----------
        solver : HeatTransferSolver
            Numerical heat transfer solver.
        """

        self.solver = solver

    def plot_temperature_profile(
        self,
        spacing: float = 100,
    ):
        """
        Plot the steady-state temperature profile.

        Parameters
        ----------
        spacing : float, optional
            Grid spacing (m).

        Returns
        -------
        tuple
            Matplotlib figure and axes objects.
        """

        depth, temperature = (
            self.solver.finite_difference_steady_state(
                spacing=spacing
            )
        )

        fig, ax = plt.subplots(figsize=(6, 8))

        ax.plot(
            temperature,
            depth,
            linewidth=2,
            label="Temperature",
        )

        ax.set_xlabel("Temperature (°C)")
        ax.set_ylabel("Depth (m)")
        ax.set_title("Steady-State Temperature Profile")
        ax.grid(True)
        ax.legend()
        ax.invert_yaxis()

        return fig, ax

    def plot_heat_flux_profile(
        self,
        spacing: float = 100,
    ):
        """
        Plot the vertical heat-flux profile.

        Parameters
        ----------
        spacing : float, optional
            Grid spacing (m).

        Returns
        -------
        tuple
            Matplotlib figure and axes objects.
        """

        depth, heat_flux = self.solver.heat_flux_profile(
            spacing=spacing
        )

        fig, ax = plt.subplots(figsize=(6, 8))

        ax.plot(
            heat_flux,
            depth,
            linewidth=2,
            label="Heat flux",
        )

        ax.set_xlabel("Heat Flux (W/m²)")
        ax.set_ylabel("Depth (m)")
        ax.set_title("Vertical Heat Flux")
        ax.grid(True)
        ax.legend()
        ax.invert_yaxis()

        return fig, ax
