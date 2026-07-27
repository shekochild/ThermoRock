"""
End-to-end ThermoRock demonstration workflow for presentations.
"""

from pathlib import Path
import sys


# Allow direct execution from the examples directory without requiring
# an editable install of the package.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from thermorock.heat_transfer import HeatTransferSolver
from thermorock.subsurface import Layer, Rock, Subsurface
from thermorock.visualization import Visualization


def save_if_available(
    visualizer: Visualization,
    method_name: str,
    filename: Path,
    spacing: float,
) -> None:
    """
    Generate and save a visualization if the method is available.
    """

    if not hasattr(visualizer, method_name):
        print(f"Skipping {method_name}: method is not available.")
        return

    print(f"Generating {method_name}...")

    method = getattr(visualizer, method_name)
    figure, _ = method(spacing=spacing)

    saved_path = visualizer.save_figure(
        figure,
        filename,
    )

    print(f"Saved figure: {saved_path}")


def save_stratigraphy_if_available(
    visualizer: Visualization,
    filename: Path,
) -> None:
    """
    Generate and save the stratigraphy figure if available.
    """

    if not hasattr(visualizer, "plot_stratigraphy"):
        print("Skipping plot_stratigraphy: method is not available.")
        return

    print("Generating plot_stratigraphy...")

    figure, _ = visualizer.plot_stratigraphy()
    saved_path = visualizer.save_figure(
        figure,
        filename,
    )

    print(f"Saved figure: {saved_path}")


def main() -> None:
    """
    Run a complete ThermoRock geothermal modelling demonstration.
    """

    print("ThermoRock presentation demo")
    print("============================")

    # -----------------------------------------------------------------
    # Define realistic lithologies used in the layered model.
    # -----------------------------------------------------------------
    print("Defining representative rock types...")

    sandstone = Rock(
        "Sandstone",
        thermal_conductivity=2.5,
        density=2300,
        heat_capacity=900,
        radiogenic_heat_production=1.5e-6,
    )

    shale = Rock(
        "Shale",
        thermal_conductivity=1.6,
        density=2550,
        heat_capacity=850,
        radiogenic_heat_production=1.2e-6,
    )

    limestone = Rock(
        "Limestone",
        thermal_conductivity=2.8,
        density=2700,
        heat_capacity=880,
        radiogenic_heat_production=0.7e-6,
    )

    granite = Rock(
        "Granite",
        thermal_conductivity=3.2,
        density=2700,
        heat_capacity=790,
        radiogenic_heat_production=3.0e-6,
    )

    # -----------------------------------------------------------------
    # Build a four-layer subsurface model.
    # The 35 C/km gradient gives 150 C at 4000 m for Ts = 10 C.
    # -----------------------------------------------------------------
    print("Building layered subsurface model...")

    surface_temperature = 10.0
    geothermal_gradient = 35.0
    spacing = 100.0

    model = Subsurface(
        surface_temperature=surface_temperature,
        geothermal_gradient=geothermal_gradient,
    )

    model.add_layer(Layer(0, 800, sandstone))
    model.add_layer(Layer(800, 1800, shale))
    model.add_layer(Layer(1800, 2800, limestone))
    model.add_layer(Layer(2800, 4000, granite))
    model.validate()

    print(f"Total model depth: {model.total_depth():.0f} m")
    print("Approximate basal temperature: 150 C")

    # -----------------------------------------------------------------
    # Create the heat-transfer solver with realistic boundary settings.
    # -----------------------------------------------------------------
    print("Creating heat-transfer solver...")

    solver = HeatTransferSolver(
        model,
        surface_temperature=surface_temperature,
        basal_heat_flow=0.065,
    )

    # -----------------------------------------------------------------
    # Run the finite-difference solver and report convergence.
    # -----------------------------------------------------------------
    print("Running steady-state finite-difference solver...")

    result = solver.finite_difference_steady_state_with_info(
        spacing=spacing,
        max_iterations=5000,
        tolerance=1e-6,
    )

    print(f"Grid nodes: {len(result['depth'])}")
    print(f"Converged: {result['converged']}")
    print(f"Iterations: {result['iterations']}")
    print(f"Final error: {result['final_error']:.3e}")

    # -----------------------------------------------------------------
    # Generate and save all available presentation figures.
    # -----------------------------------------------------------------
    print("Creating visualization outputs...")

    visualizer = Visualization(solver)
    figures_dir = Path(__file__).resolve().parent / "figures"
    figures_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    save_if_available(
        visualizer,
        "plot_temperature_profile",
        figures_dir / "temperature_profile.png",
        spacing,
    )

    save_if_available(
        visualizer,
        "plot_heat_flux_profile",
        figures_dir / "heat_flux_profile.png",
        spacing,
    )

    save_stratigraphy_if_available(
        visualizer,
        figures_dir / "stratigraphy.png",
    )

    save_if_available(
        visualizer,
        "plot_geothermal_profile",
        figures_dir / "geothermal_profile.png",
        spacing,
    )

    save_if_available(
        visualizer,
        "plot_complete_geothermal_profile",
        figures_dir / "complete_geothermal_profile.png",
        spacing,
    )

    print("Presentation demo complete.")
    print(f"Figures are available in: {figures_dir}")


if __name__ == "__main__":
    main()
