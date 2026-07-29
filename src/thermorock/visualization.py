"""
Visualization utilities for ThermoRock.
"""

from pathlib import Path

from matplotlib.pylab import spacing
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from thermorock.heat_transfer import HeatTransferSolver


FIGURE_DPI = 300
SINGLE_FIGURE_SIZE = (8, 6)
STRATIGRAPHY_FIGURE_SIZE = (8, 8)
GEOTHERMAL_FIGURE_SIZE = (14, 8)
COMPLETE_PROFILE_FIGURE_SIZE = (18, 8)

TITLE_SIZE = 17
LABEL_SIZE = 15
TICK_SIZE = 12
LEGEND_SIZE = 12
ROCK_LABEL_SIZE = 14
DEPTH_LABEL_SIZE = 13
LINE_WIDTH = 3.0

TEMPERATURE_COLOUR = "#C62828"
HEAT_FLUX_COLOUR = "#D55E00"
DEFAULT_FIGURE_DIR = (
    Path(__file__).resolve().parents[2] / "examples" / "figures"
)

GRID_STYLE = {
    "linestyle": "--",
    "linewidth": 0.6,
    "alpha": 0.4,
    "color": "0.70",
}

LITHOLOGY_COLOURS = {
    "sandstone": "#E4C985",
    "shale": "#A9BFA8",
    "limestone": "#A9CFE5",
    "granite": "#D7AED2",
    "basalt": "#7D7D7D",
    "gneiss": "#C8BBD9",
    "dolomite": "#B9DCE8",
    "mudstone": "#B5B5B5",
    "claystone": "#C8BFDF",
    "siltstone": "#EBCB88",
}
FALLBACK_LITHOLOGY_COLOURS = [
    "#E4C985",
    "#A9BFA8",
    "#A9CFE5",
    "#D7AED2",
    "#F4C58C",
    "#C7DB9B",
    "#D0B6D4",
    "#D5E8D0",
]


class Visualization:
    """
    Contains visualization utilities for ThermoRock numerical simulations.
    """

    def __init__(
        self,
        solver: HeatTransferSolver,
        output_dir=None,
        auto_save: bool = True,
    ):
        """
        Initialize a visualization helper.

        Parameters
        ----------
        solver : HeatTransferSolver
            Numerical heat transfer solver.

        output_dir : str or pathlib.Path, optional
            Directory used for automatic PNG exports.

        auto_save : bool, optional
            Save each generated figure automatically when True.
        """

        self.solver = solver
        self.output_dir = Path(output_dir or DEFAULT_FIGURE_DIR)
        self.auto_save = auto_save
        self._apply_publication_style()

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

        depth, temperature = self.solver.finite_difference_steady_state(
            spacing=spacing
        )

        fig, ax = self._create_figure(SINGLE_FIGURE_SIZE)

        ax.plot(
            temperature,
            depth,
            color=TEMPERATURE_COLOUR,
            linewidth=LINE_WIDTH,
            label="Temperature",
        )

        ax.set_xlabel("Temperature (°C)")
        ax.set_ylabel("Depth (m)")
        ax.set_title("Steady-State Temperature Profile")
        self._style_profile_axis(ax, legend=True)
        self._set_depth_axis(ax)
        self._finish_figure(fig, "temperature_profile.png")

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

        fig, ax = self._create_figure(SINGLE_FIGURE_SIZE)

        ax.plot(
            heat_flux,
            depth,
            color=HEAT_FLUX_COLOUR,
            linewidth=LINE_WIDTH,
            label="Heat flux (W/m²)",
        )

        ax.set_xlabel("Heat Flux (W/m²)")
        ax.set_ylabel("Depth (m)")
        ax.set_title("Vertical Heat Flux Profile")
        self._style_profile_axis(ax, legend=True)
        self._set_depth_axis(ax)
        self._finish_figure(fig, "heat_flux_profile.png")

        return fig, ax

    def plot_stratigraphy(self):
        """
        Plot the geological stratigraphy of the subsurface model.

        Returns
        -------
        tuple
            Matplotlib figure and axes objects.
        """

        fig, ax = self._create_figure(STRATIGRAPHY_FIGURE_SIZE)

        self._plot_stratigraphy_axis(ax)
        self._finish_figure(
            fig,
            "stratigraphy.png",
            margins={
                "left": 0.12,
                "right": 0.93,
                "top": 0.90,
                "bottom": 0.10,
            },
        )

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

        depth, temperature = self.solver.finite_difference_steady_state(
            spacing=spacing
        )

        fig, (ax1, ax2) = plt.subplots(
            1,
            2,
            figsize=GEOTHERMAL_FIGURE_SIZE,
            sharey=True,
            dpi=FIGURE_DPI,
            gridspec_kw={
                "width_ratios": [1.0, 1.7],
                "wspace": 0.30,
            },
        )

        self._plot_stratigraphy_axis(
            ax1,
            invert_axis=False,
        )

        ax2.plot(
            temperature,
            depth,
            color=TEMPERATURE_COLOUR,
            linewidth=LINE_WIDTH,
            label="Temperature",
        )

        ax2.set_xlabel("Temperature (°C)")
        ax2.set_title("Temperature Profile")
        self._style_profile_axis(ax2, legend=True)
        self._set_depth_axis(ax2)
        self._finish_figure(
            fig,
            "geothermal_profile.png",
            margins={
                "wspace": 0.30,
                "left": 0.07,
                "right": 0.98,
                "top": 0.90,
                "bottom": 0.10,
            },
        )

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

        depth, temperature = self.solver.finite_difference_steady_state(
            spacing=spacing
        )

        _, heat_flux = self.solver.heat_flux_profile(
            spacing=spacing
        )

        fig, (ax1, ax2, ax3) = plt.subplots(
            1,
            3,
            figsize=COMPLETE_PROFILE_FIGURE_SIZE,
            sharey=True,
            dpi=FIGURE_DPI,
            gridspec_kw={
                "width_ratios": [1.05, 1.4, 1.4],
                "wspace": 0.30,
            },
        )

        self._plot_stratigraphy_axis(
            ax1,
            invert_axis=False,
        )

        ax2.plot(
            temperature,
            depth,
            color=TEMPERATURE_COLOUR,
            linewidth=LINE_WIDTH,
            label="Temperature",
        )

        ax2.set_xlabel("Temperature (°C)")
        ax2.set_title("Temperature Profile")
        self._style_profile_axis(ax2, legend=True)

        ax3.plot(
            heat_flux,
            depth,
            color=HEAT_FLUX_COLOUR,
            linewidth=LINE_WIDTH,
            label="Heat flux (W/m²)",
        )

        ax3.set_xlabel("Heat Flux (W/m²)")
        ax3.set_title("Heat Flux Profile")
        self._style_profile_axis(ax3, legend=True)
        self._set_depth_axis(ax3)
        self._finish_figure(
            fig,
            "complete_geothermal_profile.png",
            margins={
                "wspace": 0.30,
                "left": 0.07,
                "right": 0.98,
                "top": 0.90,
                "bottom": 0.10,
            },
        )

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

    def _apply_publication_style(self) -> None:
        """Apply ThermoRock's publication plotting style."""

        plt.rcParams.update(
            {
                "font.family": "DejaVu Sans",
                "figure.dpi": FIGURE_DPI,
                "savefig.dpi": FIGURE_DPI,
                "axes.titlesize": TITLE_SIZE,
                "axes.titleweight": "bold",
                "axes.labelsize": LABEL_SIZE,
                "xtick.labelsize": TICK_SIZE,
                "ytick.labelsize": TICK_SIZE,
                "legend.fontsize": LEGEND_SIZE,
            }
        )

    def _create_figure(self, figsize):
        """Return a figure and axis with the requested export geometry."""

        return plt.subplots(figsize=figsize, dpi=FIGURE_DPI)

    def _finish_figure(
        self,
        figure,
        filename: str,
        margins=None,
    ) -> None:
        """Finalize layout and optionally save the figure as a PNG."""

        if margins:
            figure.subplots_adjust(**margins)
        else:
            figure.tight_layout()

        if self.auto_save:
            self.save_figure(
                figure,
                self.output_dir / filename,
            )

    def _style_profile_axis(self, ax, legend: bool = False) -> None:
        """Style profile axes with subtle grids and balanced legends."""

        ax.grid(
            True,
            which="major",
            **GRID_STYLE,
        )
        ax.tick_params(
            axis="both",
            which="major",
            labelsize=TICK_SIZE,
        )

        if legend:
            ax.legend(
                loc="best",
                frameon=True,
                framealpha=0.95,
                edgecolor="0.35",
                borderpad=0.5,
                handlelength=2.0,
            )

    def _set_depth_axis(self, ax) -> None:
        """Configure the depth axis so depth increases downward."""

        total_depth = self._total_depth()
        if total_depth > 0:
            ax.set_ylim(total_depth, 0)
        else:
            ax.invert_yaxis()

    def _total_depth(self) -> float:
        """Return the model depth represented in the visualization."""

        return self.solver.subsurface.total_depth()

    def _plot_stratigraphy_axis(
        self,
        ax,
        invert_axis: bool = True,
    ) -> None:
        """Draw the subsurface stratigraphy on an existing axis."""

        total_depth = max(self._total_depth(), 1)

        for index, layer in enumerate(self.solver.subsurface.layers):
            colour = self._lithology_colour(layer.rock.name, index)
            centre_depth = layer.top_depth + layer.thickness / 2

            ax.add_patch(
                Rectangle(
                    (0, layer.top_depth),
                    1,
                    layer.thickness,
                    facecolor=colour,
                    edgecolor="black",
                    linewidth=1.1,
                )
            )

            label = (
                f"{layer.rock.name}\n"
                f"{layer.top_depth:.0f}-{layer.bottom_depth:.0f} m"
            )
            if layer.thickness >= 0.08 * total_depth:
                self._add_layer_label(
                    ax,
                    0.50,
                    centre_depth,
                    label,
                    ha="center",
                    fontsize=ROCK_LABEL_SIZE,
                )
            else:
                self._add_layer_label(
                    ax,
                    1.05,
                    centre_depth,
                    label,
                    ha="left",
                    fontsize=ROCK_LABEL_SIZE - 1,
                )

        for depth in self._layer_boundaries():
            ax.text(
                1.03,
                depth,
                f"{depth:.0f} m",
                ha="left",
                va="center",
                fontsize=DEPTH_LABEL_SIZE,
                color="0.25",
            )

        ax.set_ylabel("Depth (m)")
        ax.set_title("Geological Stratigraphy")
        ax.set_xticks([])
        ax.set_xlim(0, 1.34)
        ax.set_ylim(0, total_depth)
        ax.tick_params(
            axis="y",
            which="major",
            labelsize=TICK_SIZE,
        )
        ax.tick_params(
            axis="x",
            bottom=False,
            labelbottom=False,
        )

        for spine in ("top", "right", "bottom"):
            ax.spines[spine].set_visible(False)

        if invert_axis:
            self._set_depth_axis(ax)

    def _add_layer_label(
        self,
        ax,
        x_position: float,
        y_position: float,
        label: str,
        ha: str,
        fontsize: int,
    ) -> None:
        """Add a vertically centred lithology label."""

        ax.text(
            x_position,
            y_position,
            label,
            ha=ha,
            va="center",
            fontsize=fontsize,
            color="black",
            linespacing=1.25,
        )

    def _lithology_colour(self, rock_name: str, index: int) -> str:
        """Return a soft professional geological colour for a lithology."""

        key = rock_name.lower()

        for lithology, colour in LITHOLOGY_COLOURS.items():
            if lithology in key:
                return colour

        return FALLBACK_LITHOLOGY_COLOURS[
            index % len(FALLBACK_LITHOLOGY_COLOURS)
        ]

    def _layer_boundaries(self) -> list[float]:
        """Return unique top and bottom depths for all plotted layers."""

        boundaries = set()

        for layer in self.solver.subsurface.layers:
            boundaries.add(layer.top_depth)
            boundaries.add(layer.bottom_depth)

        return sorted(boundaries)

    def plot_thermal_properties_dashboard(
        self,
        spacing: float = 100,
    ):
        """
        Publication-quality dashboard showing thermal diffusivity
        and radiogenic heat production.
        """

        import numpy as np

        layers = self.solver.subsurface.layers

        names = [layer.rock.name for layer in layers]

        diffusivity = [
            layer.rock.thermal_conductivity /
            (layer.rock.density * layer.rock.heat_capacity)
            for layer in layers
        ]

        radiogenic = [
            getattr(layer.rock, "radiogenic_heat_production", 0.0)
            for layer in layers
        ]

        depth = self.solver.create_grid(
            spacing
        )

        radiogenic_profile = (
            self.solver.radiogenic_heat_profile(
                spacing
            )
        )

        fig, axs = plt.subplots(
            2,
            2,
            figsize=(14,10),
            dpi=300
        )

        # -------------------------------------------------
        # Panel A
        # -------------------------------------------------

        axs[0,0].barh(
            names,
            diffusivity,
            color="steelblue"
        )

        axs[0,0].set_title(
            "Thermal Diffusivity"
        )

        axs[0,0].set_xlabel(
            r"Diffusivity (m$^2$/s)"
        )

        # -------------------------------------------------
        # Panel B
        # -------------------------------------------------

        axs[0,1].barh(
            names,
            radiogenic,
            color="firebrick"
        )

        axs[0,1].set_title(
            "Radiogenic Heat Production"
        )

        axs[0,1].set_xlabel(
           "Heat Production (µW/m³)"
        )

        # -------------------------------------------------
        # Panel C
        # -------------------------------------------------

        axs[1,0].plot(
            radiogenic_profile,
            depth,
            color="darkred",
            linewidth=3
        )

        axs[1,0].invert_yaxis()

        axs[1,0].grid(True)

        axs[1,0].set_title(
            "Radiogenic Heat Profile"
        )

        axs[1,0].set_ylabel(
            "Depth (m)"
        )

        axs[1,0].set_xlabel(
            "Heat Production (µW/m³)"
        )

        self._style_profile_axis(axs[1,0], legend=False)
        self._set_depth_axis(axs[1,0])


        # -------------------------------------------------
        # Panel D
        # -------------------------------------------------

        axs[1,1].axis("off")

        summary = (
            f"Number of Layers : {len(layers)}\n\n"
            f"Mean Diffusivity\n"
            f"{np.mean(diffusivity):.2e} m²/s\n\n"
            f"Maximum Diffusivity\n"
            f"{np.max(diffusivity):.2e} m²/s\n\n"
            f"Minimum Diffusivity\n"
            f"{np.min(diffusivity):.2e} m²/s\n\n"
            f"Mean Radiogenic Heat\n"
            f"{np.mean(radiogenic):.2f} µW/m³\n\n"
            f"Maximum Heat Production\n"
            f"{np.max(radiogenic):.2f} µW/m³\n\n"
            f"Integrated Heat Production\n"
            f"{np.sum(radiogenic):.2f} µW/m³"
        )

        axs[1,1].text(
            0.02,
            0.98,
            summary,
            fontsize=12,
            va="top",
            family="monospace",
            bbox=dict(
                facecolor="#F5F5F5",
                edgecolor="black",
                boxstyle="round"
            ),
        )

        axs[1,1].set_title(
            "Summary Statistics"
        )
        
        
        plt.suptitle(
            "ThermoRock Thermal Properties Dashboard",
            fontsize=18,
            fontweight="bold"
        )

        plt.tight_layout()

        self.save_figure(
            fig,
            self.output_dir /
            "thermal_properties_dashboard.png"
        )

        self.save_figure(
            fig,
            self.output_dir /
            "thermal_properties_dashboard.pdf"
        )

        self.save_figure(
            fig,
            self.output_dir /
            "thermal_properties_dashboard.svg"
        )

        return fig, axs