"""
Integrated geothermal profile visualization example.
"""

import matplotlib.pyplot as plt

from thermorock.heat_transfer import HeatTransferSolver
from thermorock.subsurface import Layer, Rock, Subsurface
from thermorock.visualization import Visualization


def build_model() -> Subsurface:
    """
    Create a layered geothermal subsurface model.
    """

    sandstone = Rock(
        "Sandstone",
        thermal_conductivity=2.5,
        density=2300,
        heat_capacity=900,
        radiogenic_heat_production=1.5e-6,
    )

    shale = Rock(
        "Shale",
        thermal_conductivity=1.8,
        density=2500,
        heat_capacity=850,
        radiogenic_heat_production=1.0e-6,
    )

    granite = Rock(
        "Granite",
        thermal_conductivity=3.2,
        density=2700,
        heat_capacity=790,
        radiogenic_heat_production=3.0e-6,
    )

    model = Subsurface(
        surface_temperature=10.0,
        geothermal_gradient=30.0,
    )

    model.add_layer(Layer(0, 600, sandstone))
    model.add_layer(Layer(600, 1800, shale))
    model.add_layer(Layer(1800, 3000, granite))

    return model


def main() -> None:
    """
    Generate and display an integrated geothermal figure.
    """

    solver = HeatTransferSolver(build_model())
    visualizer = Visualization(solver)

    visualizer.plot_complete_geothermal_profile(spacing=250)

    # Use plt.show() only in examples, not inside the library.
    plt.show()


if __name__ == "__main__":
    main()
