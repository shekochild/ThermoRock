"""Classes for representing a layered geological subsurface."""

from dataclasses import dataclass


@dataclass
class Rock:
    """
    Represents the thermal properties of a rock.
    """

    name: str
    thermal_conductivity: float
    density: float
    heat_capacity: float
    radiogenic_heat_production: float

    def __post_init__(self):
        """Validate rock properties."""

        if not self.name.strip():
            raise ValueError("Rock name cannot be empty.")

        if self.thermal_conductivity <= 0:
            raise ValueError("thermal_conductivity must be positive.")

        if self.density <= 0:
            raise ValueError("density must be positive.")

        if self.heat_capacity <= 0:
            raise ValueError("heat_capacity must be positive.")

        if self.radiogenic_heat_production < 0:
            raise ValueError(
                "radiogenic_heat_production cannot be negative."
            )


@dataclass
class Layer:
    """
    Represents a geological layer.
    """

    top_depth: float
    bottom_depth: float
    rock: Rock

    def __post_init__(self):
        """Validate layer geometry."""

        if self.top_depth < 0:
            raise ValueError("top_depth must be non-negative.")

        if self.bottom_depth <= self.top_depth:
            raise ValueError(
                "bottom_depth must be greater than top_depth."
            )

        if not isinstance(self.rock, Rock):
            raise TypeError("rock must be a Rock object.")

    @property
    def thickness(self) -> float:
        """
        Return the thickness of the layer in metres.
        """
        return self.bottom_depth - self.top_depth


class Subsurface:
    """
    Represents a layered geological subsurface.
    """

    def __init__(self):
        """Initialize an empty subsurface."""
        self.layers = []

    def add_layer(self, layer: Layer):
        """
        Add a geological layer to the subsurface.
        """
        if not isinstance(layer, Layer):
            raise TypeError("layer must be a Layer object.")

        self.layers.append(layer)

    def remove_layer(self, index: int):
        """
        Remove a layer by index.
        """
        del self.layers[index]

    def number_of_layers(self) -> int:
        """
        Return the number of layers.
        """
        return len(self.layers)

    def total_depth(self) -> float:
        """
        Return the maximum depth of the subsurface.
        """
        if not self.layers:
            return 0.0

        return max(layer.bottom_depth for layer in self.layers)

    def validate(self):
        """
        Validate the subsurface geometry.

        Checks that layers do not overlap and are ordered by depth.
        """
        if not self.layers:
            return

        layers = sorted(self.layers, key=lambda layer: layer.top_depth)

        for i in range(len(layers) - 1):
            if layers[i].bottom_depth > layers[i + 1].top_depth:
                raise ValueError(
                    "Layers overlap in the subsurface."
                )

    def summary(self) -> dict:
        """
        Return a summary of the subsurface.
        """
        return {
            "number_of_layers": self.number_of_layers(),
            "total_depth": self.total_depth(),
            "rock_types": [
                layer.rock.name for layer in self.layers
            ],
        }