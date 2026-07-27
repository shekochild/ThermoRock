"""
ThermoRock figure export example.
"""

from pathlib import Path

from thermorock.heat_transfer import HeatTransferSolver
from thermorock.subsurface import Layer, Rock, Subsurface
from thermorock.visualization import Visualization


def main() -> None:
    """
    Generate a figure and save it using the Visualization API.
    """

    sandstone = Rock(
        "Sandstone",
        thermal_conductivity=2.5,
        density=2300,
        heat_capacity=900,
        radiogenic_heat_production=1.5e-6,
    )

    model = Subsurface(
        surface_temperature=10.0,
        geothermal_gradient=30.0,
    )

    model.add_layer(
        Layer(
            0,
            1000,
            sandstone,
        )
    )

    solver = HeatTransferSolver(model)
    visualizer = Visualization(solver)

    figure, _ = visualizer.plot_temperature_profile(spacing=100)

    output = Path("outputs") / "temperature_profile.png"
    saved_path = visualizer.save_figure(
        figure,
        output,
    )

    print(f"Saved figure to: {saved_path}")


if __name__ == "__main__":
    main()
