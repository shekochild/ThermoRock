from dataclasses import dataclass, field
from typing import List
@dataclass
class Rock:
    """Represents the thermal properties of a rock."""

    name: str
    thermal_conductivity: float
    density: float
    heat_capacity: float
    radiogenic_heat_production: float

    def __post_init__(self):
        if self.thermal_conductivity <= 0:
            raise ValueError("thermal_conductivity must be positive.")

        if self.density <= 0:
            raise ValueError("density must be positive.")

        if self.heat_capacity <= 0:
            raise ValueError("heat_capacity must be positive.")

        if self.radiogenic_heat_production < 0:
            raise ValueError("radiogenic_heat_production cannot be negative.")
        
        
@dataclass
class Layer:
    top_depth: float
    bottom_depth: float
    rock: Rock
    @property
    def thickness(self):
        self.bottom_depth - self.top_depth
        class Subsurface:
            def __init__(self):
                self.layers = []
def add_layer(self, layer):
    ...

def remove_layer(self, index):
    ...

def number_of_layers(self):
    ...

def total_depth(self):
    ...

def validate(self):
    ...

def summary(self):
    ...            