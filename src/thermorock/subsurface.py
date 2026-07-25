"""Classes for representing a layered geological subsurface."""

from dataclasses import dataclass


@dataclass
class Rock:
    """
    Represents the thermal properties of a rock.
    """

    name: str
    thermal_conductivity: float
    density: float
    heat_capacity: float
    radiogenic_heat_production: float

    def __post_init__(self):
        """Validate rock properties."""

        if not self.name.strip():
            raise ValueError("Rock name cannot be empty.")

        if self.thermal_conductivity <= 0:
            raise ValueError("thermal_conductivity must be positive.")

        if self.density <= 0:
            raise ValueError("density must be positive.")

        if self.heat_capacity <= 0:
            raise ValueError("heat_capacity must be positive.")

        if self.radiogenic_heat_production < 0:
            raise ValueError(
                "radiogenic_heat_production cannot be negative."
            )


@dataclass
class Layer:
    """
    Represents a geological layer.
    """

    top_depth: float
    bottom_depth: float
    rock: Rock
    geothermal_gradient: float = 30.0
    def __post_init__(self):
        """Validate layer geometry."""

        if self.top_depth < 0:
            raise ValueError("top_depth must be non-negative.")

        if self.bottom_depth <= self.top_depth:
            raise ValueError(
                "bottom_depth must be greater than top_depth."
            )

        if self.geothermal_gradient <= 0:
            raise ValueError(
                "geothermal_gradient must be positive."
            )

        if not isinstance(self.rock, Rock):
            raise TypeError("rock must be a Rock object.")

    @property
    def thickness(self) -> float:
        """
        Return the thickness of the layer in metres.
        """
        return self.bottom_depth - self.top_depth


class Subsurface:
    """
    Represents a layered geological subsurface.

    """
    
    def __init__(
        self,
        surface_temperature: float = 10.0,
        geothermal_gradient: float = 30.0,
    ):
        """
        Initialize a layered subsurface model.

        Parameters
        ----------
        surface_temperature : float, optional
            Surface temperature in °C.

        geothermal_gradient : float, optional
            Geothermal gradient in °C/km.
        """

        if geothermal_gradient <= 0:
            raise ValueError(
                "geothermal_gradient must be positive."
            )

        self.layers = []

        self.surface_temperature = surface_temperature
        self.geothermal_gradient = geothermal_gradient

    def add_layer(self, layer: Layer):
        """
        Add a geological layer to the subsurface.
        """
        if not isinstance(layer, Layer):
            raise TypeError("layer must be a Layer object.")

        self.layers.append(layer)

    def remove_layer(self, index: int):
        """
        Remove a layer by index.
        """
        del self.layers[index]

    def number_of_layers(self) -> int:
        """
        Return the number of layers.
        """
        return len(self.layers)
    def total_depth(self) -> float:
        """
        Return the maximum depth of the subsurface.
        """
        if not self.layers:
            return 0.0

        return max(layer.bottom_depth for layer in self.layers)

    def get_layer_at_depth(self, depth: float) -> Layer:
        """
        Return the geological layer containing the specified depth.

        Parameters
        ----------
        depth : float
            Depth below the surface (m).

        Returns
        -------
        Layer
            The layer containing the specified depth.

        Raises
        ------
        ValueError
            If no layer contains the specified depth.
        """

        if depth < 0:
            raise ValueError("Depth must be non-negative.")

        for layer in self.layers:
            if layer.top_depth <= depth < layer.bottom_depth:
                return layer

        raise ValueError(f"No layer found at depth {depth} m.")
    
    def get_rock_at_depth(self, depth: float) -> Rock:
             """
             Return the rock present at the specified depth.
     
             Parameters
             ----------
             depth : float
                 Depth below the surface (m).
     
             Returns
             -------
             Rock
                 The rock occupying the specified depth.
             """
             return self.get_layer_at_depth(depth).rock  
    
   
    def temperature_at_depth(self, depth: float) -> float:
        """
        Calculate the temperature at a specified depth.

        Parameters
        ----------
        depth : float
            Depth below the surface (m).

        Returns
        -------
        float
            Temperature (°C).
        """

        if depth < 0:
            raise ValueError("Depth must be non-negative.")

        gradient_per_m = self.geothermal_gradient / 1000

        return (
            self.surface_temperature
            + gradient_per_m * depth
        )
        
    def temperature_profile(
        self,
        depths: list[float],
    ) -> list[float]:
        """
        Calculate temperatures for multiple depths.

        Parameters
        ----------
        depths : list[float]
            Depths below the surface (m).

        Returns
        -------
        list[float]
            Temperatures (°C).
        """

        return [
            self.temperature_at_depth(depth)
            for depth in depths
        ] 
        
        
    def heterogeneous_temperature_at_depth(
        self,
        depth: float,
    ) -> float:
        """
        Calculate the temperature at a specified depth using
        layer-specific geothermal gradients.

        Parameters
        ----------
        depth : float
            Depth below the surface (m).

        Returns
        -------
        float
            Temperature (°C).
        """

        if depth < 0:
            raise ValueError(
                "Depth must be non-negative."
            )

        if depth > self.total_depth():
            raise ValueError(
                "Depth exceeds the subsurface model."
            )

        temperature = self.surface_temperature

        for layer in sorted(
            self.layers,
            key=lambda layer: layer.top_depth,
        ):

            gradient = (
                layer.geothermal_gradient / 1000
            )

            if depth >= layer.bottom_depth:

                temperature += (
                    layer.thickness * gradient
                )

            else:

                temperature += (
                    (depth - layer.top_depth)
                    * gradient
                )

                break

        return temperature     
        
    def heterogeneous_temperature_profile(
        self,
        depths: list[float],
    ) -> list[float]:
        """
        Calculate temperatures at multiple depths using
        layer-specific geothermal gradients.

        Parameters
        ----------
        depths : list[float]
            Depths below the surface (m).

        Returns
        -------
        list[float]
            Temperatures (°C).
        """

        return [
            self.heterogeneous_temperature_at_depth(depth)
            for depth in depths
        ]    
        
    def total_radiogenic_heat_production(self) -> float:
        """
        Calculate the total radiogenic heat production of
        the subsurface.

        Returns
        -------
        float
            Total radiogenic heat production (W/m³).
        """

        return sum(
            layer.rock.radiogenic_heat_production
            for layer in self.layers
        )    
        
        
    def integrated_radiogenic_heat_production(self) -> float:
        """
        Calculate the vertically integrated radiogenic heat
        production of the subsurface.

        Returns
        -------
        float
            Integrated radiogenic heat production (W/m²).
        """

        return sum(
            layer.rock.radiogenic_heat_production
            * layer.thickness
            for layer in self.layers
        )
        
        
        
    def effective_thermal_conductivity(self) -> float:
        """
        Calculate the effective vertical thermal conductivity
        of the layered subsurface.

        Returns
        -------
        float
            Effective thermal conductivity (W/m/K).
        """

        if not self.layers:
            raise ValueError(
                "Subsurface contains no layers."
            )

        total_thickness = sum(
            layer.thickness
            for layer in self.layers
        )

        total_resistance = sum(
            layer.thickness
            / layer.rock.thermal_conductivity
            for layer in self.layers
        )

        return total_thickness / total_resistance    
     
    def effective_thermal_diffusivity(self) -> float:
        """
        Calculate the effective thermal diffusivity of the
        layered subsurface.

        Returns
        -------
        float
            Effective thermal diffusivity (m²/s).
        """

        if not self.layers:
            raise ValueError(
                "Subsurface contains no layers."
            )

        total_thickness = sum(
            layer.thickness
            for layer in self.layers
        )

        average_density = sum(
            layer.thickness * layer.rock.density
            for layer in self.layers
        ) / total_thickness

        average_heat_capacity = sum(
            layer.thickness * layer.rock.heat_capacity
            for layer in self.layers
        ) / total_thickness

        return (
            self.effective_thermal_conductivity()
            / (
                average_density
                * average_heat_capacity
            )
        )  
        
    def validate(self):
        """
        Validate the subsurface geometry.

        Checks that layers do not overlap and are ordered by depth.
        """
        if not self.layers:
            return

        layers = sorted(self.layers, key=lambda layer: layer.top_depth)

        for i in range(len(layers) - 1):
            if layers[i].bottom_depth > layers[i + 1].top_depth:
                raise ValueError(
                    "Layers overlap in the subsurface."
                )

    def summary(self) -> dict:
        """
        Return a summary of the subsurface.
        """
        return {
            "number_of_layers": self.number_of_layers(),
            "total_depth": self.total_depth(),
            "rock_types": [
                layer.rock.name for layer in self.layers
            ],
        }
