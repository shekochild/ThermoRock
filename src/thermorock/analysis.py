"""
Tools for geothermal resource analysis.
"""

from thermorock.subsurface import Subsurface


class GeothermalAnalysis:
    """
    Perform geothermal resource analyses using a layered
    geological subsurface model.
    """

    def __init__(self, subsurface: Subsurface):
        """
        Initialise a geothermal analysis.

        Parameters
        ----------
        subsurface : Subsurface
            Layered geological subsurface model.
        """
        if not isinstance(subsurface, Subsurface):
            raise TypeError(
                "subsurface must be a Subsurface object."
            )

        self.subsurface = subsurface
        
    def layer_heat_content(
        self,
        layer_index: int,
    ) -> float:
        """
        Calculate the stored heat content of a layer.

        Parameters
        ----------
        layer_index : int
            Index of the geological layer.

        Returns
        -------
        float
            Heat content per unit area (J/m²).
        """

        layer = self.subsurface.layers[layer_index]

        temperature = self.subsurface.temperature_at_depth(
            layer.bottom_depth
        )

        delta_temperature = (
            temperature
            - self.subsurface.surface_temperature
        )

        return (
            layer.rock.density
            * layer.rock.heat_capacity
            * layer.thickness
            * delta_temperature
        )
    def total_heat_content(self) -> float:
        """
        Calculate the total stored heat content of the
        subsurface.

        Returns
        -------
        float
            Total heat content per unit area (J/m²).
        """

        return sum(
            self.layer_heat_content(index)
            for index in range(
                self.subsurface.number_of_layers()
            )
        )     