from thermorock import thermal_diffusivity


def test_thermal_diffusivity():
    result = thermal_diffusivity(2.5, 2700, 800)

    expected = 2.5 / (2700 * 800)

    assert result == expected