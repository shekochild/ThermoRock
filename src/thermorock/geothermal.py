
"""
Functions for analytical geothermal calculations.

This module contains functions used to estimate geothermal
properties such as geothermal gradient, temperature at depth,
heat flow, and radiogenic heat production.
"""

from .validation import validate_positive_inputs


def geothermal_gradient(
    *,
    surface_temperature,
    reservoir_temperature,
    depth,
):
    """
    Calculate the geothermal gradient.

    Parameters
    ----------
    surface_temperature : float
        Surface temperature in degrees Celsius (°C).
    reservoir_temperature : float
        Temperature at the specified depth in degrees Celsius (°C).
    depth : float
        Depth below the surface in kilometres (km).

    Returns
    -------
    float
        Geothermal gradient in degrees Celsius per kilometre (°C/km).

    Raises
    ------
    TypeError
        If any input is not numeric.
    ValueError
        If depth is zero or negative.
    """
    validate_positive_inputs(
        depth=depth,
    )

    gradient = (reservoir_temperature - surface_temperature) / depth

    return gradient



def temperature_at_depth(
    *,
    surface_temperature,
    geothermal_gradient,
    depth,
):
    """
    Calculate the temperature at a specified depth.

    Parameters
    ----------
    surface_temperature : float
        Surface temperature in degrees Celsius (°C).
    geothermal_gradient : float
        Geothermal gradient in degrees Celsius per kilometre (°C/km).
    depth : float
        Depth below the surface in kilometres (km).

    Returns
    -------
    float
        Temperature at the specified depth in degrees Celsius (°C).

    Raises
    ------
    TypeError
        If any input is not numeric.
    ValueError
        If depth or geothermal_gradient is zero or negative.
    """
    validate_positive_inputs(
        geothermal_gradient=geothermal_gradient,
        depth=depth,
    )
    
 
    temperature = (
        surface_temperature
        + geothermal_gradient * depth
    )

    return temperature


def heat_flow(
    *,
    thermal_conductivity,
    geothermal_gradient,
):
    """
    Calculate conductive heat flow using Fourier's Law.

    Parameters
    ----------
    thermal_conductivity : float
        Thermal conductivity in W/(m·K).
    geothermal_gradient : float
        Geothermal gradient in °C/km.

    Returns
    -------
    float
        Conductive heat flow in mW/m².

    Raises
    ------
    TypeError
        If any input is not numeric.
    ValueError
        If any input is zero or negative.
    """
    validate_positive_inputs(
        thermal_conductivity=thermal_conductivity,
        geothermal_gradient=geothermal_gradient,
    )

    gradient_k_per_m = geothermal_gradient / 1000

    heat_flow_value= (
        thermal_conductivity
        * gradient_k_per_m
    )

    return heat_flow_value * 1000