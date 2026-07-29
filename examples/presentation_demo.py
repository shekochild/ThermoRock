"""
End-to-end ThermoRock demonstration workflow for presentations.
"""

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import FancyArrowPatch
from matplotlib.ticker import ScalarFormatter

# Allow direct execution from the examples directory without requiring
# an editable install of the package.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from thermorock.analysis import GeothermalAnalysis
from thermorock.heat_transfer import HeatTransferSolver
from thermorock.subsurface import Layer, Rock, Subsurface
from thermorock.visualization import Visualization


RESULTS_DIR = PROJECT_ROOT / "results"
RESERVOIR_AREA = 10_000_000.0
RECOVERY_FACTOR = 0.15
CONVERSION_EFFICIENCY = 0.12

FIGURE_DPI = 300
TITLE_SIZE = 16
LABEL_SIZE = 14
TICK_SIZE = 12
LEGEND_SIZE = 12
GRID_STYLE = {
    "linestyle": "--",
    "linewidth": 0.6,
    "alpha": 0.35,
    "color": "0.70",
}
THERMOROCK_BLUE = "#2F6F9F"
THERMOROCK_TEAL = "#2A9D8F"
THERMOROCK_GREEN = "#6BAA75"
THERMOROCK_GOLD = "#D99A2B"
THERMOROCK_RED = "#B95B50"
THERMOROCK_GRAY = "#D9DEE3"
TEXT_COLOR = "#1F2933"


def apply_publication_style() -> None:
    """
    Apply consistent ThermoRock publication styling to Matplotlib.
    """

    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.edgecolor": "0.25",
            "axes.labelcolor": TEXT_COLOR,
            "axes.titlecolor": TEXT_COLOR,
            "font.family": "DejaVu Sans",
            "font.size": 12,
            "savefig.facecolor": "white",
            "xtick.color": TEXT_COLOR,
            "ytick.color": TEXT_COLOR,
        }
    )


def format_scientific(value: float) -> str:
    """
    Format numerical results in compact scientific notation.
    """

    return f"{value:.3e}"


def save_publication_figure(
    figure,
    output_path: Path,
    suffixes: tuple[str, ...] = (".png", ".pdf"),
) -> None:
    """
    Save a figure in one or more publication-ready formats.
    """

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    figure.tight_layout()

    for suffix in suffixes:
        figure.savefig(
            output_path.with_suffix(suffix),
            dpi=FIGURE_DPI,
            bbox_inches="tight",
            facecolor="white",
        )


def apply_scientific_axis(axis, axis_name: str = "x") -> None:
    """
    Use scientific notation for a Matplotlib axis.
    """

    formatter = ScalarFormatter(useMathText=True)
    formatter.set_powerlimits((0, 0))

    if axis_name == "x":
        axis.xaxis.set_major_formatter(formatter)
    else:
        axis.yaxis.set_major_formatter(formatter)


def build_geothermal_summary(
    total_heat_content: float,
    heat_in_place: float,
    recoverable_heat: float,
    recoverable_energy: float,
    potential: str,
) -> pd.DataFrame:
    """
    Build a formatted geothermal resource summary table.
    """

    return pd.DataFrame(
        [
            (
                "Total Heat Content",
                format_scientific(total_heat_content),
                "J/m²",
            ),
            ("Heat in Place", format_scientific(heat_in_place), "J"),
            (
                "Recoverable Heat",
                format_scientific(recoverable_heat),
                "J",
            ),
            (
                "Recoverable Energy",
                format_scientific(recoverable_energy),
                "J",
            ),
            ("Geothermal Potential", potential, "-"),
        ],
        columns=["Quantity", "Value", "Unit"],
    )


def export_summary_table(
    summary: pd.DataFrame,
    results_dir: Path,
) -> None:
    """
    Export the geothermal summary table as CSV, PNG, PDF, and LaTeX.
    """

    results_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    summary.to_csv(
        results_dir / "geothermal_summary.csv",
        index=False,
    )
    summary.to_latex(
        results_dir / "geothermal_summary.tex",
        index=False,
        escape=False,
        caption="ThermoRock geothermal resource summary.",
        label="tab:geothermal_summary",
    )

    figure, axis = plt.subplots(
        figsize=(8, 3.2),
        dpi=FIGURE_DPI,
    )
    axis.axis("off")
    table = axis.table(
        cellText=summary.values,
        colLabels=summary.columns,
        loc="center",
        cellLoc="center",
        colLoc="center",
        colWidths=[0.44, 0.34, 0.22],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.0, 1.45)

    for (row, _), cell in table.get_celld().items():
        cell.set_edgecolor("0.35")
        cell.set_linewidth(0.6)
        cell.set_facecolor("white")
        if row == 0:
            cell.set_text_props(weight="bold")
            cell.set_facecolor("#EAEAEA")

    axis.set_title(
        "Geothermal Resource Summary",
        fontsize=TITLE_SIZE,
        fontweight="bold",
        pad=14,
    )
    save_publication_figure(
        figure,
        results_dir / "geothermal_summary.png",
    )
    plt.close(figure)


def plot_layer_heat_content(
    layer_names: list[str],
    layer_heat: list[float],
    results_dir: Path,
) -> None:
    """
    Plot heat content for each geological layer.
    """

    figure, axis = plt.subplots(
        figsize=(9, 5.5),
        dpi=FIGURE_DPI,
    )
    axis.barh(
        layer_names,
        layer_heat,
        color="#8FB9D9",
        edgecolor="black",
        linewidth=0.8,
    )
    axis.invert_yaxis()
    axis.set_xlabel("Heat Content (J/m²)", fontsize=LABEL_SIZE)
    axis.set_ylabel("Geological Layer", fontsize=LABEL_SIZE)
    axis.set_title(
        "Layer Heat Content",
        fontsize=TITLE_SIZE,
        fontweight="bold",
    )
    axis.tick_params(
        axis="both",
        labelsize=TICK_SIZE,
    )
    axis.grid(
        True,
        axis="x",
        **GRID_STYLE,
    )
    apply_scientific_axis(axis, "x")

    save_publication_figure(
        figure,
        results_dir / "layer_heat_content.png",
    )
    plt.close(figure)


def plot_energy_flow(
    heat_in_place: float,
    recoverable_heat: float,
    recoverable_energy: float,
    results_dir: Path,
) -> None:
    """
    Plot the reduction from heat in place to recoverable energy.
    """

    labels = [
        "Heat in Place",
        "Recoverable Heat",
        "Recoverable Energy",
    ]
    values = [
        heat_in_place,
        recoverable_heat,
        recoverable_energy,
    ]
    colours = [
        "#6BAED6",
        "#FD8D3C",
        "#74C476",
    ]

    figure, axis = plt.subplots(
        figsize=(10, 5.5),
        dpi=FIGURE_DPI,
    )
    bars = axis.barh(
        labels,
        values,
        color=colours,
        edgecolor="black",
        linewidth=0.8,
    )
    axis.invert_yaxis()
    axis.set_xlabel("Energy (J)", fontsize=LABEL_SIZE)
    axis.set_title(
        "Geothermal Energy Flow",
        fontsize=TITLE_SIZE,
        fontweight="bold",
    )
    axis.tick_params(
        axis="both",
        labelsize=TICK_SIZE,
    )
    axis.grid(
        True,
        axis="x",
        **GRID_STYLE,
    )
    apply_scientific_axis(axis, "x")

    x_max = max(values)
    for bar, value in zip(bars, values):
        axis.text(
            value + 0.015 * x_max,
            bar.get_y() + bar.get_height() / 2,
            format_scientific(value),
            va="center",
            fontsize=TICK_SIZE,
        )

    save_publication_figure(
        figure,
        results_dir / "energy_flow.png",
    )
    plt.close(figure)


def plot_energy_comparison(
    heat_in_place: float,
    recoverable_heat: float,
    recoverable_energy: float,
    results_dir: Path,
) -> None:
    """
    Plot a grouped comparison of geothermal energy quantities.
    """

    labels = [
        "Heat in Place",
        "Recoverable Heat",
        "Recoverable Energy",
    ]
    values = [
        heat_in_place,
        recoverable_heat,
        recoverable_energy,
    ]
    colours = [
        "#6BAED6",
        "#FD8D3C",
        "#74C476",
    ]

    figure, axis = plt.subplots(
        figsize=(9, 5.5),
        dpi=FIGURE_DPI,
    )
    bars = axis.bar(
        labels,
        values,
        color=colours,
        edgecolor="black",
        linewidth=0.8,
    )
    axis.set_ylabel("Energy (J)", fontsize=LABEL_SIZE)
    axis.set_title(
        "Geothermal Energy Comparison",
        fontsize=TITLE_SIZE,
        fontweight="bold",
    )
    axis.tick_params(
        axis="both",
        labelsize=TICK_SIZE,
    )
    axis.grid(
        True,
        axis="y",
        **GRID_STYLE,
    )
    apply_scientific_axis(axis, "y")

    y_max = max(values)
    axis.set_ylim(0, y_max * 1.18)

    for bar, value in zip(bars, values):
        axis.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.025 * y_max,
            format_scientific(value),
            ha="center",
            va="bottom",
            fontsize=TICK_SIZE,
        )

    save_publication_figure(
        figure,
        results_dir / "energy_comparison.png",
    )
    plt.close(figure)


def calculate_geothermal_dashboard_values(
    model: Subsurface,
    analysis: GeothermalAnalysis,
) -> dict:
    """
    Gather geothermal assessment values from existing analysis methods.
    """

    midpoint_depths = [
        (layer.top_depth + layer.bottom_depth) / 2
        for layer in model.layers
    ]
    reservoir_temperatures = [
        model.temperature_at_depth(depth)
        for depth in midpoint_depths
    ]
    average_temperature = (
        sum(reservoir_temperatures) / len(reservoir_temperatures)
        if reservoir_temperatures
        else model.surface_temperature
    )

    layer_heat = [
        analysis.layer_heat_content(index)
        for index in range(model.number_of_layers())
    ]
    total_heat_content = analysis.total_heat_content()
    heat_in_place = analysis.heat_in_place(RESERVOIR_AREA)
    recoverable_heat = analysis.recoverable_heat(
        RESERVOIR_AREA,
        RECOVERY_FACTOR,
    )
    recoverable_energy = analysis.recoverable_energy(
        RESERVOIR_AREA,
        RECOVERY_FACTOR,
        CONVERSION_EFFICIENCY,
    )
    potential = analysis.geothermal_potential(
        RESERVOIR_AREA,
        RECOVERY_FACTOR,
        CONVERSION_EFFICIENCY,
    )

    return {
        "layer_names": [layer.rock.name for layer in model.layers],
        "layer_heat": layer_heat,
        "total_heat_content": total_heat_content,
        "heat_in_place": heat_in_place,
        "recoverable_heat": recoverable_heat,
        "recoverable_energy": recoverable_energy,
        "recovery_factor": RECOVERY_FACTOR,
        "conversion_efficiency": CONVERSION_EFFICIENCY,
        "potential": potential,
        "reservoir_area": RESERVOIR_AREA,
        "number_of_layers": model.number_of_layers(),
        "average_geothermal_gradient": model.geothermal_gradient,
        "surface_temperature": model.surface_temperature,
        "average_reservoir_temperature": average_temperature,
    }


def build_publication_summary(metrics: dict) -> pd.DataFrame:
    """
    Build the dashboard energy summary table.
    """

    return pd.DataFrame(
        [
            (
                "Total Heat Content",
                format_scientific(metrics["total_heat_content"]),
                "J/m^2",
            ),
            (
                "Heat in Place",
                format_scientific(metrics["heat_in_place"]),
                "J",
            ),
            (
                "Recoverable Heat",
                format_scientific(metrics["recoverable_heat"]),
                "J",
            ),
            (
                "Recoverable Energy",
                format_scientific(metrics["recoverable_energy"]),
                "J",
            ),
            (
                "Recovery Factor",
                format_scientific(metrics["recovery_factor"]),
                "fraction",
            ),
            (
                "Conversion Efficiency",
                format_scientific(metrics["conversion_efficiency"]),
                "fraction",
            ),
            (
                "Geothermal Potential",
                metrics["potential"],
                "class",
            ),
        ],
        columns=["Quantity", "Value", "Unit"],
    )


def render_publication_table(
    axis,
    summary: pd.DataFrame,
    title: str,
) -> None:
    """
    Render a minimalist publication-quality table on an axis.
    """

    axis.axis("off")
    table = axis.table(
        cellText=summary.values,
        colLabels=summary.columns,
        loc="center",
        cellLoc="center",
        colLoc="center",
        colWidths=[0.47, 0.30, 0.23],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10.5)
    table.scale(1.0, 1.32)

    for (row, _), cell in table.get_celld().items():
        cell.set_edgecolor("0.45")
        cell.set_linewidth(0.6)
        cell.set_facecolor("white")
        cell.set_text_props(color=TEXT_COLOR)
        if row == 0:
            cell.set_facecolor(THERMOROCK_BLUE)
            cell.set_text_props(weight="bold", color="white")
        elif row % 2 == 0:
            cell.set_facecolor("#F6F8FA")

    axis.set_title(
        title,
        fontsize=TITLE_SIZE,
        fontweight="bold",
        pad=14,
    )


def render_publication_layer_heat(
    axis,
    layer_names: list[str],
    layer_heat: list[float],
    title: str,
) -> None:
    """
    Render layer heat content with labels and scientific notation.
    """

    axis.barh(
        layer_names,
        layer_heat,
        color=THERMOROCK_BLUE,
        edgecolor="0.20",
        linewidth=0.8,
    )
    axis.invert_yaxis()
    axis.set_xlabel("Heat Content (J/m^2)", fontsize=LABEL_SIZE)
    axis.set_ylabel("Geological Layer", fontsize=LABEL_SIZE)
    axis.set_title(title, fontsize=TITLE_SIZE, fontweight="bold")
    axis.tick_params(axis="both", labelsize=TICK_SIZE)
    axis.grid(True, axis="x", **GRID_STYLE)
    axis.set_axisbelow(True)
    apply_scientific_axis(axis, "x")

    x_max = max(layer_heat) if layer_heat else 1.0
    axis.set_xlim(0, x_max * 1.26)
    for y_position, value in enumerate(layer_heat):
        axis.text(
            value + 0.025 * x_max,
            y_position,
            format_scientific(value),
            va="center",
            fontsize=10.5,
            color=TEXT_COLOR,
        )


def render_publication_energy_flow(
    axis,
    metrics: dict,
    title: str,
) -> None:
    """
    Render proportional energy flow with recovery and conversion losses.
    """

    labels = [
        "Heat in Place",
        "Recoverable Heat",
        "Recoverable Energy",
    ]
    values = [
        metrics["heat_in_place"],
        metrics["recoverable_heat"],
        metrics["recoverable_energy"],
    ]
    y_positions = [2, 1, 0]
    colours = [THERMOROCK_BLUE, THERMOROCK_GREEN, THERMOROCK_TEAL]

    bars = axis.barh(
        y_positions,
        values,
        color=colours,
        edgecolor="0.20",
        linewidth=0.8,
        height=0.34,
    )
    x_max = max(values)
    loss_to_recovery = values[0] - values[1]
    loss_to_energy = values[1] - values[2]

    axis.barh(
        1,
        loss_to_recovery,
        left=values[1],
        color=THERMOROCK_GRAY,
        edgecolor="0.65",
        linewidth=0.5,
        height=0.34,
    )
    axis.barh(
        0,
        loss_to_energy,
        left=values[2],
        color="#E9C6A7",
        edgecolor="0.65",
        linewidth=0.5,
        height=0.34,
    )

    axis.set_yticks(y_positions)
    axis.set_yticklabels(labels)
    axis.set_xlim(0, x_max * 1.33)
    axis.set_xlabel("Energy (J)", fontsize=LABEL_SIZE)
    axis.set_title(title, fontsize=TITLE_SIZE, fontweight="bold")
    axis.tick_params(axis="both", labelsize=TICK_SIZE)
    axis.grid(True, axis="x", **GRID_STYLE)
    axis.set_axisbelow(True)
    apply_scientific_axis(axis, "x")

    for bar, value in zip(bars, values):
        axis.text(
            value + 0.025 * x_max,
            bar.get_y() + bar.get_height() / 2,
            format_scientific(value),
            va="center",
            fontsize=10.5,
            color=TEXT_COLOR,
        )

    for y_start, y_end in ((1.82, 1.18), (0.82, 0.18)):
        axis.add_patch(
            FancyArrowPatch(
                (x_max * 0.09, y_start),
                (x_max * 0.09, y_end),
                arrowstyle="-|>",
                mutation_scale=14,
                linewidth=1.3,
                color=TEXT_COLOR,
            )
        )

    axis.text(
        x_max * 0.53,
        1.22,
        f"Recovery factor: {metrics['recovery_factor']:.0%}",
        fontsize=10.5,
        color=TEXT_COLOR,
    )
    axis.text(
        x_max * 0.53,
        0.22,
        (
            "Conversion efficiency: "
            f"{metrics['conversion_efficiency']:.0%}"
        ),
        fontsize=10.5,
        color=TEXT_COLOR,
    )
    axis.text(
        values[1] + loss_to_recovery / 2,
        1,
        "Unrecovered heat",
        ha="center",
        va="center",
        fontsize=9.5,
        color="0.30",
    )
    axis.text(
        values[2] + loss_to_energy / 2,
        0,
        "Conversion loss",
        ha="center",
        va="center",
        fontsize=9.5,
        color="0.30",
    )


def render_reservoir_classification(axis, metrics: dict) -> None:
    """
    Render geothermal potential and reservoir descriptors.
    """

    axis.axis("off")
    potential = metrics["potential"].upper()
    badge_colours = {
        "LOW": THERMOROCK_RED,
        "MODERATE": THERMOROCK_GOLD,
        "HIGH": THERMOROCK_GREEN,
    }
    badge_colour = badge_colours.get(potential, THERMOROCK_GRAY)

    axis.text(
        0.5,
        0.78,
        potential,
        transform=axis.transAxes,
        ha="center",
        va="center",
        fontsize=24,
        fontweight="bold",
        color="white",
        bbox={
            "boxstyle": "round,pad=0.55,rounding_size=0.12",
            "facecolor": badge_colour,
            "edgecolor": "none",
        },
    )

    information = [
        (
            "Reservoir Area",
            f"{format_scientific(metrics['reservoir_area'])} m^2",
        ),
        ("Number of Layers", f"{metrics['number_of_layers']:.0f}"),
        (
            "Average Geothermal Gradient",
            f"{metrics['average_geothermal_gradient']:.1f} C/km",
        ),
        (
            "Surface Temperature",
            f"{metrics['surface_temperature']:.1f} C",
        ),
        (
            "Average Reservoir Temperature",
            f"{metrics['average_reservoir_temperature']:.1f} C",
        ),
    ]

    y_position = 0.56
    for label, value in information:
        axis.text(
            0.08,
            y_position,
            label,
            transform=axis.transAxes,
            ha="left",
            va="center",
            fontsize=12.5,
            color="0.35",
        )
        axis.text(
            0.92,
            y_position,
            value,
            transform=axis.transAxes,
            ha="right",
            va="center",
            fontsize=12.5,
            fontweight="bold",
            color=TEXT_COLOR,
        )
        axis.plot(
            [0.08, 0.92],
            [y_position - 0.055, y_position - 0.055],
            transform=axis.transAxes,
            color="0.88",
            linewidth=0.8,
        )
        y_position -= 0.12


def latex_escape(value: object) -> str:
    """
    Escape a table cell for a simple LaTeX tabular export.
    """

    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    text = str(value)

    for original, escaped in replacements.items():
        text = text.replace(original, escaped)

    return text


def dataframe_to_latex_table(
    dataframe: pd.DataFrame,
    caption: str,
    label: str,
) -> str:
    """
    Convert a small DataFrame to LaTeX without optional pandas styling.
    """

    columns = " & ".join(latex_escape(column) for column in dataframe.columns)
    rows = [
        " & ".join(latex_escape(value) for value in row)
        for row in dataframe.to_numpy()
    ]
    body = " \\\\\n".join(rows)

    return (
        "\\begin{table}\n"
        "\\centering\n"
        f"\\caption{{{latex_escape(caption)}}}\n"
        f"\\label{{{latex_escape(label)}}}\n"
        "\\begin{tabular}{lll}\n"
        "\\hline\n"
        f"{columns} \\\\\n"
        "\\hline\n"
        f"{body} \\\\\n"
        "\\hline\n"
        "\\end{tabular}\n"
        "\\end{table}\n"
    )


def export_publication_summary_table(
    summary: pd.DataFrame,
    results_dir: Path,
) -> None:
    """
    Save the requested standalone summary table outputs.
    """

    results_dir.mkdir(parents=True, exist_ok=True)
    summary.to_csv(results_dir / "geothermal_summary.csv", index=False)
    (results_dir / "geothermal_summary.tex").write_text(
        dataframe_to_latex_table(
            summary,
            "ThermoRock geothermal resource summary.",
            "tab:geothermal_summary",
        ),
        encoding="utf-8",
    )

    figure, axis = plt.subplots(figsize=(8, 3.8), dpi=FIGURE_DPI)
    render_publication_table(
        axis,
        summary,
        "Geothermal Resource Summary",
    )
    save_publication_figure(figure, results_dir / "summary_table.png")
    plt.close(figure)


def export_publication_layer_heat(
    metrics: dict,
    results_dir: Path,
) -> None:
    """
    Save the requested standalone layer heat content outputs.
    """

    figure, axis = plt.subplots(figsize=(9, 5.5), dpi=FIGURE_DPI)
    render_publication_layer_heat(
        axis,
        metrics["layer_names"],
        metrics["layer_heat"],
        "Layer Heat Content",
    )
    save_publication_figure(figure, results_dir / "layer_heat_content.png")
    plt.close(figure)


def export_publication_energy_flow(
    metrics: dict,
    results_dir: Path,
) -> None:
    """
    Save the requested standalone energy flow outputs.
    """

    figure, axis = plt.subplots(figsize=(10, 5.5), dpi=FIGURE_DPI)
    render_publication_energy_flow(axis, metrics, "Geothermal Energy Flow")
    save_publication_figure(figure, results_dir / "energy_flow.png")
    plt.close(figure)


def export_publication_dashboard(
    metrics: dict,
    summary: pd.DataFrame,
    results_dir: Path,
) -> None:
    """
    Save the four-panel geothermal dashboard.
    """

    figure, axes = plt.subplots(2, 2, figsize=(14, 8), dpi=FIGURE_DPI)
    figure.patch.set_facecolor("white")
    figure.suptitle(
        "ThermoRock Geothermal Resource Assessment",
        fontsize=18,
        fontweight="bold",
        color=TEXT_COLOR,
        y=0.985,
    )

    render_publication_layer_heat(
        axes[0, 0],
        metrics["layer_names"],
        metrics["layer_heat"],
        "A - Layer Heat Content",
    )
    render_publication_table(axes[0, 1], summary, "B - Energy Summary")
    render_publication_energy_flow(axes[1, 0], metrics, "C - Energy Flow")
    render_reservoir_classification(axes[1, 1], metrics)
    axes[1, 1].set_title(
        "D - Reservoir Classification",
        fontsize=TITLE_SIZE,
        fontweight="bold",
        pad=14,
    )

    figure.tight_layout(rect=(0, 0, 1, 0.955))
    save_publication_figure(
        figure,
        results_dir / "geothermal_dashboard.png",
        suffixes=(".png", ".pdf", ".svg"),
    )
    plt.close(figure)

    # Thermal properties dashboard is generated separately in main().
    # Do not attempt to access visualizer or figures_dir here.
def run_geothermal_resource_analysis(
    model: Subsurface,
    results_dir: Path,
) -> None:
    """
    Run geothermal resource analysis and export publication outputs.
    """

    apply_publication_style()
    analysis = GeothermalAnalysis(model)
    metrics = calculate_geothermal_dashboard_values(model, analysis)
    summary = build_publication_summary(metrics)

    export_publication_summary_table(summary, results_dir)
    export_publication_layer_heat(metrics, results_dir)
    export_publication_energy_flow(metrics, results_dir)
    plot_energy_comparison(
        metrics["heat_in_place"],
        metrics["recoverable_heat"],
        metrics["recoverable_energy"],
        results_dir,
    )
    export_publication_dashboard(metrics, summary, results_dir)

    print()
    print("=====================================")
    print("THERMOROCK GEOTHERMAL ANALYSIS")
    print("=====================================")
    print(
        "Heat in Place          "
        f"{format_scientific(metrics['heat_in_place'])} J"
    )
    print(
        "Recoverable Heat       "
        f"{format_scientific(metrics['recoverable_heat'])} J"
    )
    print(
        "Recoverable Energy     "
        f"{format_scientific(metrics['recoverable_energy'])} J"
    )
    print(f"Potential              {metrics['potential']}")
    print()
    print("Figures saved to:")
    print(f"{results_dir}/")


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
    print("Generating thermal properties dashboard...")

    figure, _ = visualizer.plot_thermal_properties_dashboard()

    saved_path = visualizer.save_figure(
        figure,
        filename,
    )
    plt.close(figure)

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

    # -----------------------------------------------------------------
    # Geothermal Resource Analysis
    # -----------------------------------------------------------------
    run_geothermal_resource_analysis(
        model,
        RESULTS_DIR,
    )

    print("Presentation demo complete.")
    print(f"Figures are available in: {figures_dir}")


if __name__ == "__main__":
    main()
