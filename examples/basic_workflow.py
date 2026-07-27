"""
Basic ThermoRock workflow example.
"""

from thermorock.heat_transfer import HeatTransferSolver
from thermorock.subsurface import Layer, Rock, Subsurface


def main() -> None:
    """
    Build a simple subsurface model and compute temperatures.
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

    model = Subsurface(
        surface_temperature=10.0,
        geothermal_gradient=30.0,
    )

    model.add_layer(
        Layer(
            0,
            500,
            sandstone,
        )
    )

    model.add_layer(
        Layer(
            500,
            1500,
            shale,
        )
    )

    solver = HeatTransferSolver(model)

    depths, temperatures = solver.finite_difference_steady_state(
        spacing=250
    )

    print("Depth (m), Temperature (deg C)")

    for depth, temperature in zip(depths, temperatures):
        print(f"{depth:.0f}, {temperature:.2f}")


if __name__ == "__main__":
    main()
