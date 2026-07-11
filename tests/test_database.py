import pytest

from thermorock.database import get_rock_properties


def test_granite_lookup():

    granite = get_rock_properties("granite")

    assert "conductivity" in granite
    assert "density" in granite
    assert "heat_capacity" in granite


def test_unknown_rock():

    with pytest.raises(ValueError):
        get_rock_properties("moon_rock")