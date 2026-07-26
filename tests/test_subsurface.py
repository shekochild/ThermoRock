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
            
    def test_get_rock_at_depth_first_layer(self, sandstone):
        """Test retrieving the rock at a valid depth."""

        model = Subsurface()

        model.add_layer(Layer(0, 500, sandstone))

        rock = model.get_rock_at_depth(250)

        assert rock.name == "Sandstone"

    def test_get_rock_at_depth_not_found(self, sandstone):
        """Test that an error is raised for depths outside the model."""

        model = Subsurface()

        model.add_layer(Layer(0, 500, sandstone))

        with pytest.raises(ValueError):
            model.get_rock_at_depth(1000)  
            
    def test_temperature_at_depth_default(self):
        """Test temperature at depth using default thermal properties."""

        model = Subsurface()

        assert model.temperature_at_depth(1000) == 40.0

    def test_temperature_at_depth_custom(self):
        """Test temperature at depth using custom thermal properties."""

        model = Subsurface(
            surface_temperature=15,
            geothermal_gradient=35,
        )

        assert model.temperature_at_depth(2000) == 85.0

    def test_temperature_at_negative_depth(self):
        """Test that negative depths are rejected."""

        model = Subsurface()

        with pytest.raises(ValueError):
            model.temperature_at_depth(-100)  
                           
            
    def test_temperature_profile_default(self):
        model = Subsurface()

        profile = model.temperature_profile(
            [0, 1000, 2000]
        )

        assert profile == [10.0, 40.0, 70.0]

    def test_temperature_profile_custom(self):
        model = Subsurface(
            surface_temperature=15,
            geothermal_gradient=35,
        )

        profile = model.temperature_profile(
            [0, 1000]
        )

        assert profile == [15.0, 50.0]

    def test_temperature_profile_empty(self):
        model = Subsurface()

        assert model.temperature_profile([]) == []
    
    def test_heterogeneous_temperature(self, sandstone):
        model = Subsurface()

        model.add_layer(
            Layer(
                0,
                1000,
                sandstone,
                geothermal_gradient=20,
            )
        )

        model.add_layer(
            Layer(
                1000,
                2000,
                sandstone,
                geothermal_gradient=40,
            )
        )

        assert (
            model.heterogeneous_temperature_at_depth(
                1500
            )
            == 50.0
        )

    def test_heterogeneous_negative_depth(
        self,
        sandstone,
    ):
        model = Subsurface()

        model.add_layer(
            Layer(0, 1000, sandstone)
        )

        with pytest.raises(ValueError):
            model.heterogeneous_temperature_at_depth(
                -100
            )
        
        
    def test_heterogeneous_temperature_profile(self, sandstone):
        model = Subsurface()

        model.add_layer(
            Layer(
                0,
                1000,
                sandstone,
                geothermal_gradient=20,
            )
        )

        model.add_layer(
            Layer(
                1000,
                2000,
                sandstone,
                geothermal_gradient=40,
            )
        )

        profile = model.heterogeneous_temperature_profile(
            [0, 1000, 1500, 2000]
        )

        assert profile == [10.0, 30.0, 50.0, 70.0]

    def test_heterogeneous_temperature_profile_empty(self):
        model = Subsurface()

        assert (
            model.heterogeneous_temperature_profile([])
            == []
        )    
        
    def test_total_radiogenic_heat_production(self):
        sandstone = Rock(
            "Sandstone",
            2.5,
            2300,
            900,
            1.5e-6,
        )

        granite = Rock(
            "Granite",
            3.0,
            2700,
            790,
            3.0e-6,
        )

        model = Subsurface()

        model.add_layer(Layer(0, 500, sandstone))
        model.add_layer(Layer(500, 1500, granite))

        assert (
            model.total_radiogenic_heat_production()
            == 4.5e-6
        )

    def test_total_radiogenic_heat_empty(self):
        model = Subsurface()

        assert (
            model.total_radiogenic_heat_production()
            == 0
        )   
    def test_integrated_radiogenic_heat(self):
        sandstone = Rock(
            "Sandstone",
            2.5,
            2300,
            900,
            2e-6,
        )

        shale = Rock(
            "Shale",
            1.8,
            2500,
            850,
            1e-6,
        )

        granite = Rock(
            "Granite",
            3.0,
            2700,
            790,
            4e-6,
        )

        model = Subsurface()

        model.add_layer(
            Layer(0, 1000, sandstone)
        )

        model.add_layer(
            Layer(1000, 2500, shale)
        )

        model.add_layer(
            Layer(2500, 4000, granite)
        )

        expected = (
            2e-6 * 1000 +
            1e-6 * 1500 +
            4e-6 * 1500
        )

        assert (
            model.integrated_radiogenic_heat_production()
            == expected
        )   
        
    def test_effective_thermal_conductivity(self):
        sandstone = Rock(
            "Sandstone",
            2.0,
            2300,
            900,
            2e-6,
        )

        shale = Rock(
            "Shale",
            1.0,
            2500,
            850,
            1e-6,
        )

        granite = Rock(
            "Granite",
            4.0,
            2700,
            790,
            4e-6,
        )

        model = Subsurface()

        model.add_layer(Layer(0, 1000, sandstone))
        model.add_layer(Layer(1000, 2000, shale))
        model.add_layer(Layer(2000, 3000, granite))

        expected = 3000 / (
            1000 / 2.0
            + 1000 / 1.0
            + 1000 / 4.0
        )

        assert (
            model.effective_thermal_conductivity()
            == pytest.approx(expected)
        )


    def test_effective_thermal_conductivity_empty(self):
        model = Subsurface()

        with pytest.raises(ValueError):
            model.effective_thermal_conductivity()    
            
            
    def test_effective_thermal_diffusivity(self):
        sandstone = Rock(
            "Sandstone",
            2.5,
            2500,
            1000,
            2e-6,
        )

        granite = Rock(
            "Granite",
            3.5,
            2700,
            800,
            4e-6,
        )

        model = Subsurface()

        model.add_layer(
            Layer(0, 1000, sandstone)
        )

        model.add_layer(
            Layer(1000, 2000, granite)
        )

        diffusivity = (
            model.effective_thermal_diffusivity()
        )

        assert diffusivity > 0

    def test_effective_thermal_diffusivity_empty(self):
        model = Subsurface()

        with pytest.raises(ValueError):
            model.effective_thermal_diffusivity()  
   
    def test_gap_between_layers(self, sandstone):
        model = Subsurface()

        model.add_layer(
            Layer(0, 1000, sandstone)
        )

        model.add_layer(
            Layer(1200, 2000, sandstone)
        )

        with pytest.raises(ValueError):
            model.validate()


    def test_continuous_layers(self, sandstone):
        model = Subsurface()

        model.add_layer(
            Layer(0, 1000, sandstone)
        )

        model.add_layer(
            Layer(1000, 2000, sandstone)
        )

        model.validate()              