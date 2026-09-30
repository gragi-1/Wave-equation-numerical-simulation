"""Wave-function construction and normalization utilities."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from quantum_wave.config import GaussianPacket1D, GaussianPacket2D, GridConfig

ComplexArray = NDArray[np.complex128]


def coordinate_axis(grid: GridConfig) -> NDArray[np.float64]:
    """Return all grid coordinates, including both boundary nodes."""

    return np.linspace(0.0, grid.length, grid.points)


def normalize(state: ComplexArray, cell_measure: float) -> ComplexArray:
    """Return a copy of ``state`` with unit integrated probability."""

    probability = float(np.sum(np.abs(state) ** 2) * cell_measure)
    if not np.isfinite(probability) or probability <= np.finfo(float).eps:
        raise ValueError("Cannot normalize a state with zero or non-finite probability.")
    return np.asarray(state, dtype=np.complex128) / np.sqrt(probability)


def gaussian_packet_1d(grid: GridConfig, packet: GaussianPacket1D) -> ComplexArray:
    """Create a Gaussian packet on the interior of a 1D box."""

    if grid.dimensions != 1:
        raise ValueError("gaussian_packet_1d requires a one-dimensional grid.")
    if not 0.0 < packet.center < grid.length:
        raise ValueError("The packet center must lie inside the simulation domain.")

    x = coordinate_axis(grid)[1:-1]
    envelope = np.exp(-((x - packet.center) ** 2) / (2.0 * packet.width**2))
    phase = np.exp(1j * packet.wave_number * x)
    return normalize(envelope * phase, grid.cell_measure)


def gaussian_packet_2d(grid: GridConfig, packet: GaussianPacket2D) -> ComplexArray:
    """Create a Gaussian packet on the interior of a 2D square box."""

    if grid.dimensions != 2:
        raise ValueError("gaussian_packet_2d requires a two-dimensional grid.")
    centers = (packet.center_x, packet.center_y)
    if not all(0.0 < center < grid.length for center in centers):
        raise ValueError("Both packet centers must lie inside the simulation domain.")

    axis = coordinate_axis(grid)[1:-1]
    x, y = np.meshgrid(axis, axis, indexing="ij")
    distance_squared = (x - packet.center_x) ** 2 + (y - packet.center_y) ** 2
    envelope = np.exp(-distance_squared / (2.0 * packet.width**2))
    phase = np.exp(1j * (packet.wave_number_x * x + packet.wave_number_y * y))
    return normalize((envelope * phase).reshape(-1), grid.cell_measure)
