"""
Rock property database.

NOTE:
Current values are preliminary literature-based ranges
used for software development and testing.

They will be updated with values extracted from
Clauser (2006) and other geothermal references.
"""

ROCK_PROPERTIES = {
    "granite": {
        "conductivity": (2.0, 5.0),
        "density": (2600, 2800),
        "heat_capacity": (700, 850),
        "reference": "Placeholder"
    },
    "sandstone": {
        "conductivity": (1.5, 6.0),
        "density": (2200, 2600),
        "heat_capacity": (700, 1000),
        "reference": "Placeholder"
    },
    "limestone": {
        "conductivity": (1.3, 5.0),
        "density": (2200, 2700),
        "heat_capacity": (800, 1000),
        "reference": "Placeholder"
    },
    "dolomite": {
        "conductivity": (3.0, 5.5),
        "density": (2600, 2900),
        "heat_capacity": (800, 950),
        "reference": "Placeholder"
    },
    "shale": {
        "conductivity": (0.5, 2.5),
        "density": (2200, 2800),
        "heat_capacity": (700, 1000),
        "reference": "Placeholder"
    },
    "basement_rock": {
        "conductivity": (2.0, 5.0),
        "density": (2600, 3000),
        "heat_capacity": (700, 900),
        "reference": "Placeholder"
    }
}
def get_rock_properties(rock_name):
    """
    Return properties for a rock type.
    """

    rock_name = rock_name.lower()

    if rock_name not in ROCK_PROPERTIES:
        raise ValueError(
            f"Unknown rock type: {rock_name}"
        )

    return ROCK_PROPERTIES[rock_name]