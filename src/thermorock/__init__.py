"""
ThermoRock

A Python package for thermal rock properties and geothermal calculations.
"""

from .database import get_rock_properties
from .diffusivity import thermal_diffusivity
from .geothermal import (
    geothermal_gradient,
    temperature_at_depth,
    heat_flow,
)
from .range_validation import validate_property_range
from .validation import (
    validate_positive,
    validate_positive_inputs,
)

__all__ = [
    "get_rock_properties",
    "thermal_diffusivity",
    "geothermal_gradient",
    "temperature_at_depth",
    "heat_flow",
    "validate_positive",
    "validate_positive_inputs",
    "validate_property_range",
]