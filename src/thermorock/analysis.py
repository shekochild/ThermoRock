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
        
    def heat_in_place(
        self,
        reservoir_area: float,
    ) -> float:
        """
        Calculate the total heat in place.

        Parameters
        ----------
        reservoir_area : float
            Reservoir area (m²).

        Returns
        -------
        float
            Heat in place (J).
        """

        if reservoir_area <= 0:
            raise ValueError(
                "reservoir_area must be positive."
            )

        return (
            self.total_heat_content()
            * reservoir_area
        )      
    
    def recoverable_heat(
        self,
        reservoir_area: float,
        recovery_factor: float,
    ) -> float:
        """
        Calculate the recoverable geothermal heat.

        Parameters
        ----------
        reservoir_area : float
            Reservoir area (m²).

        recovery_factor : float
            Fraction of heat that can be recovered.

        Returns
        -------
        float
            Recoverable heat (J).
        """

        if not 0 < recovery_factor <= 1:
            raise ValueError(
                "recovery_factor must be between 0 and 1."
            )

        return (
            self.heat_in_place(
                reservoir_area
            )
            * recovery_factor
        )    
        
    def recoverable_energy(
        self,
        reservoir_area: float,
        recovery_factor: float,
        conversion_efficiency: float,
    ) -> float:
        """
        Calculate the recoverable geothermal energy.

        Parameters
        ----------
        reservoir_area : float
            Reservoir area (m²).

        recovery_factor : float
            Fraction of recoverable heat.

        conversion_efficiency : float
            Fraction of heat converted into usable energy.

        Returns
        -------
        float
            Recoverable energy (J).
        """

        if not 0 < conversion_efficiency <= 1:
            raise ValueError(
                "conversion_efficiency must be between 0 and 1."
            )

        return (
            self.recoverable_heat(
                reservoir_area,
                recovery_factor,
            )
            * conversion_efficiency
        )    
        
    def geothermal_potential(
        self,
        reservoir_area: float,
        recovery_factor: float,
        conversion_efficiency: float,
    ) -> str:
        """
        Classify the geothermal potential of the reservoir.

        Parameters
        ----------
        reservoir_area : float
            Reservoir area (m²).

        recovery_factor : float
            Fraction of recoverable heat.

        conversion_efficiency : float
            Fraction of heat converted into usable energy.

        Returns
        -------
        str
            Geothermal potential classification.
        """

        energy = self.recoverable_energy(
            reservoir_area,
            recovery_factor,
            conversion_efficiency,
        )

        if energy < 1e12:
            return "Low"

        if energy < 1e14:
            return "Moderate"

        return "High"