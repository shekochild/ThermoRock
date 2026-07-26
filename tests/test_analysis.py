"""
Unit tests for the analysis module.
"""

import pytest

from thermorock.analysis import GeothermalAnalysis
from thermorock.subsurface import (
    Rock,
    Layer,
    Subsurface,
)


@pytest.fixture
def sandstone():
    return Rock(
        "Sandstone",
        2.5,
        2300,
        900,
        2e-6,
    )


@pytest.fixture
def model(sandstone):
    model = Subsurface()

    model.add_layer(
        Layer(
            0,
            1000,
            sandstone,
        )
    )

    return model


class TestGeothermalAnalysis:
    """Tests for the GeothermalAnalysis class."""

    def test_create_analysis(self, model):
        analysis = GeothermalAnalysis(model)

        assert analysis.subsurface is model

    def test_invalid_subsurface(self):
        with pytest.raises(TypeError):
            GeothermalAnalysis("not a subsurface")

    def test_layer_heat_content(self, model):
        analysis = GeothermalAnalysis(model)

        heat = analysis.layer_heat_content(0)

        assert heat > 0

    def test_layer_heat_content_invalid_index(self, model):
        analysis = GeothermalAnalysis(model)

        with pytest.raises(IndexError):
            analysis.layer_heat_content(1)
    
    def test_total_heat_content(self):
        sandstone = Rock(
            "Sandstone",
            2.5,
            2300,
            900,
            2e-6,
        )

        model = Subsurface()

        model.add_layer(
            Layer(0, 1000, sandstone)
        )

        model.add_layer(
            Layer(1000, 2000, sandstone)
        )

        analysis = GeothermalAnalysis(model)

        total = analysis.total_heat_content()

        assert total > 0


    def test_total_heat_content_empty(self):
        model = Subsurface()

        analysis = GeothermalAnalysis(model)

        assert analysis.total_heat_content() == 0        
        
    def test_heat_in_place(self):
        sandstone = Rock(
            "Sandstone",
            2.5,
            2300,
            900,
            2e-6,
        )

        model = Subsurface()

        model.add_layer(
            Layer(0, 1000, sandstone)
        )

        analysis = GeothermalAnalysis(model)

        heat = analysis.heat_in_place(
            reservoir_area=1000
        )

        assert heat > 0


    def test_heat_in_place_invalid_area(self):
        sandstone = Rock(
            "Sandstone",
            2.5,
            2300,
            900,
            2e-6,
        )

        model = Subsurface()

        model.add_layer(
            Layer(0, 1000, sandstone)
        )

        analysis = GeothermalAnalysis(model)

        with pytest.raises(ValueError):
            analysis.heat_in_place(0)
    
    def test_recoverable_heat(self):
        sandstone = Rock(
            "Sandstone",
            2.5,
            2300,
            900,
            2e-6,
        )

        model = Subsurface()

        model.add_layer(
            Layer(0, 1000, sandstone)
        )

        analysis = GeothermalAnalysis(model)

        heat = analysis.recoverable_heat(
            reservoir_area=1000,
            recovery_factor=0.2,
        )

        assert heat > 0


    def test_invalid_recovery_factor(self):
        sandstone = Rock(
            "Sandstone",
            2.5,
            2300,
            900,
            2e-6,
        )

        model = Subsurface()

        model.add_layer(
            Layer(0, 1000, sandstone)
        )

        analysis = GeothermalAnalysis(model)

        with pytest.raises(ValueError):
            analysis.recoverable_heat(
                reservoir_area=1000,
                recovery_factor=1.5,
            )        