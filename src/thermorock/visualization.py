"""
Visualization utilities for ThermoRock.
"""

from pathlib import Path

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

    def plot_stratigraphy(self):
        """
        Plot the geological stratigraphy of the subsurface model.

        Returns
        -------
        tuple
            Matplotlib figure and axes objects.
        """

        fig, ax = plt.subplots(figsize=(4, 8))

        self._plot_stratigraphy_axis(ax)

        return fig, ax

    def plot_geothermal_profile(
        self,
        spacing: float = 100,
    ):
        """
        Plot geological stratigraphy beside the temperature profile.

        Parameters
        ----------
        spacing : float, optional
            Grid spacing (m).

        Returns
        -------
        tuple
            Matplotlib figure and stratigraphy/temperature axes.
        """

        depth, temperature = (
            self.solver.finite_difference_steady_state(
                spacing=spacing
            )
        )

        fig, (ax1, ax2) = plt.subplots(
            1,
            2,
            figsize=(10, 8),
            sharey=True,
        )

        self._plot_stratigraphy_axis(
            ax1,
            invert_axis=False,
        )

        ax2.plot(
            temperature,
            depth,
            linewidth=2,
            label="Temperature",
        )

        ax2.set_xlabel("Temperature (°C)")
        ax2.set_title("Temperature Profile")
        ax2.grid(True)
        ax2.invert_yaxis()

        fig.tight_layout()

        return fig, (ax1, ax2)

    def plot_complete_geothermal_profile(
        self,
        spacing: float = 100,
    ):
        """
        Plot stratigraphy, temperature, and heat-flux profiles.

        Parameters
        ----------
        spacing : float, optional
            Grid spacing (m).

        Returns
        -------
        tuple
            Matplotlib figure and stratigraphy, temperature,
            and heat-flux axes.
        """

        depth, temperature = (
            self.solver.finite_difference_steady_state(
                spacing=spacing
            )
        )

        _, heat_flux = self.solver.heat_flux_profile(
            spacing=spacing
        )

        fig, (ax1, ax2, ax3) = plt.subplots(
            1,
            3,
            figsize=(14, 8),
            sharey=True,
        )

        self._plot_stratigraphy_axis(
            ax1,
            invert_axis=False,
        )

        ax2.plot(
            temperature,
            depth,
            linewidth=2,
            label="Temperature",
        )

        ax2.set_xlabel("Temperature (°C)")
        ax2.set_title("Temperature Profile")
        ax2.grid(True)

        ax3.plot(
            heat_flux,
            depth,
            linewidth=2,
            label="Heat flux",
        )

        ax3.set_xlabel("Heat Flux (W/m²)")
        ax3.set_title("Heat Flux Profile")
        ax3.grid(True)
        ax3.invert_yaxis()

        fig.tight_layout()

        return fig, (ax1, ax2, ax3)

    def save_figure(
        self,
        figure,
        filename,
        dpi: int = 300,
    ) -> Path:
        """
        Save a Matplotlib figure to disk.

        Parameters
        ----------
        figure
            Matplotlib figure to save.

        filename
            Output file path.

        dpi : int, optional
            Output resolution in dots per inch.

        Returns
        -------
        Path
            Path to the saved figure.
        """

        path = Path(filename)
        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        figure.savefig(
            path,
            dpi=dpi,
            bbox_inches="tight",
        )

        return path

    def _plot_stratigraphy_axis(
        self,
        ax,
        invert_axis: bool = True,
    ) -> None:
        """
        Draw the subsurface stratigraphy on an existing axis.
        """

        colours = [
            "#8da0cb",
            "#fc8d62",
            "#66c2a5",
            "#e78ac3",
            "#a6d854",
            "#ffd92f",
        ]

        for index, layer in enumerate(self.solver.subsurface.layers):
            colour = colours[index % len(colours)]
            centre_depth = (
                layer.top_depth
                + layer.thickness / 2
            )

            ax.barh(
                centre_depth,
                1,
                height=layer.thickness,
                color=colour,
                edgecolor="black",
            )

            ax.text(
                0.5,
                centre_depth,
                layer.rock.name,
                ha="center",
                va="center",
            )

        ax.set_ylabel("Depth (m)")
        ax.set_title("Geological Stratigraphy")
        ax.set_xticks([])
        ax.set_xlim(0, 1)

        if invert_axis:
            ax.invert_yaxis()
