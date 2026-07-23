"""
Unit tests for the subsurface module.
"""

import pytest

from thermorock.subsurface import Layer, Rock, Subsurface


@pytest.fixture
def sandstone():
    """Return a valid sandstone rock."""

    return Rock(
        name="Sandstone",
        thermal_conductivity=2.5,
        density=2300,
        heat_capacity=900,
        radiogenic_heat_production=1.5e-6,
    )


class TestRock:
    """Tests for the Rock class."""

    def test_create_rock(self, sandstone):
        assert sandstone.name == "Sandstone"

    def test_negative_conductivity(self):
        with pytest.raises(ValueError):
            Rock(
                name="Sandstone",
                thermal_conductivity=-2.5,
                density=2300,
                heat_capacity=900,
                radiogenic_heat_production=1.5e-6,
            )

    def test_negative_density(self):
        with pytest.raises(ValueError):
            Rock(
                name="Sandstone",
                thermal_conductivity=2.5,
                density=-2300,
                heat_capacity=900,
                radiogenic_heat_production=1.5e-6,
            )

    def test_negative_heat_capacity(self):
        with pytest.raises(ValueError):
            Rock(
                name="Sandstone",
                thermal_conductivity=2.5,
                density=2300,
                heat_capacity=-900,
                radiogenic_heat_production=1.5e-6,
            )

    def test_negative_radiogenic_heat(self):
        with pytest.raises(ValueError):
            Rock(
                name="Sandstone",
                thermal_conductivity=2.5,
                density=2300,
                heat_capacity=900,
                radiogenic_heat_production=-1,
            )


class TestLayer:
    """Tests for the Layer class."""

    def test_layer_thickness(self, sandstone):
        layer = Layer(0, 500, sandstone)

        assert layer.thickness == 500

    def test_invalid_layer_depth(self, sandstone):
        with pytest.raises(ValueError):
            Layer(500, 0, sandstone)

    def test_invalid_rock_type(self):
        with pytest.raises(TypeError):
            Layer(0, 500, "Sandstone")


class TestSubsurface:
    """Tests for the Subsurface class."""

    def test_add_layer(self, sandstone):
        model = Subsurface()

        model.add_layer(Layer(0, 500, sandstone))

        assert model.number_of_layers() == 1

    def test_remove_layer(self, sandstone):
        model = Subsurface()

        model.add_layer(Layer(0, 500, sandstone))
        model.remove_layer(0)

        assert model.number_of_layers() == 0

    def test_total_depth(self, sandstone):
        model = Subsurface()

        model.add_layer(Layer(0, 500, sandstone))
        model.add_layer(Layer(500, 1500, sandstone))

        assert model.total_depth() == 1500

    def test_empty_subsurface(self):
        model = Subsurface()

        assert model.number_of_layers() == 0
        assert model.total_depth() == 0.0

    def test_summary(self, sandstone):
        model = Subsurface()

        model.add_layer(Layer(0, 500, sandstone))

        summary = model.summary()

        assert summary["number_of_layers"] == 1
        assert summary["total_depth"] == 500
        assert summary["rock_types"] == ["Sandstone"]

    def test_overlapping_layers(self, sandstone):
        model = Subsurface()

        model.add_layer(Layer(0, 1000, sandstone))
        model.add_layer(Layer(500, 1500, sandstone))

        with pytest.raises(ValueError):
            model.validate()

    def test_add_invalid_layer(self):
        model = Subsurface()

        with pytest.raises(TypeError):
            model.add_layer("not a layer")
            