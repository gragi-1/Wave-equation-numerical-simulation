"""Validated configuration objects for quantum wave simulations."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal


def _require_positive(name: str, value: float) -> None:
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be a positive, finite number; received {value!r}.")


@dataclass(frozen=True, slots=True)
class GridConfig:
    """A uniform Cartesian grid including its boundary nodes."""

    dimensions: Literal[1, 2]
    length: float = 1.0
    points: int = 256

    def __post_init__(self) -> None:
        if self.dimensions not in (1, 2):
            raise ValueError("Only one- and two-dimensional grids are supported.")
        _require_positive("length", self.length)
        if isinstance(self.points, bool) or not isinstance(self.points, int) or self.points < 5:
            raise ValueError("points must be an integer greater than or equal to 5.")

    @property
    def spacing(self) -> float:
        """Distance between adjacent grid nodes."""

        return self.length / (self.points - 1)

    @property
    def shape(self) -> tuple[int, ...]:
        """Shape of a full field, including zero-valued boundary nodes."""

        return (self.points,) * self.dimensions

    @property
    def interior_shape(self) -> tuple[int, ...]:
        """Shape of the unknown field evolved by the numerical solver."""

        return (self.points - 2,) * self.dimensions

    @property
    def interior_size(self) -> int:
        """Number of unknowns after removing the Dirichlet boundary."""

        return (self.points - 2) ** self.dimensions

    @property
    def cell_measure(self) -> float:
        """Integration weight: ``dx`` in 1D and ``dx²`` in 2D."""

        return self.spacing**self.dimensions


@dataclass(frozen=True, slots=True)
class SimulationConfig:
    """Physical constants and integration settings for a simulation."""

    grid: GridConfig
    time_step: float = 1e-4
    mass: float = 1.0
    hbar: float = 1.0

    def __post_init__(self) -> None:
        _require_positive("time_step", self.time_step)
        _require_positive("mass", self.mass)
        _require_positive("hbar", self.hbar)


@dataclass(frozen=True, slots=True)
class GaussianPacket1D:
    """Parameters of a normalized Gaussian wave packet in one dimension."""

    center: float = 0.35
    width: float = 0.06
    wave_number: float = 30.0

    def __post_init__(self) -> None:
        _require_positive("width", self.width)
        if not math.isfinite(self.center) or not math.isfinite(self.wave_number):
            raise ValueError("center and wave_number must be finite.")


@dataclass(frozen=True, slots=True)
class GaussianPacket2D:
    """Parameters of a normalized Gaussian wave packet in two dimensions."""

    center_x: float = 0.35
    center_y: float = 0.50
    width: float = 0.075
    wave_number_x: float = 22.0
    wave_number_y: float = 8.0

    def __post_init__(self) -> None:
        _require_positive("width", self.width)
        values = (self.center_x, self.center_y, self.wave_number_x, self.wave_number_y)
        if not all(math.isfinite(value) for value in values):
            raise ValueError("Packet centers and wave numbers must be finite.")
