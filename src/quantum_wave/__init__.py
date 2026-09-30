"""Numerical tools for simulating confined quantum wave packets."""

from quantum_wave.config import (
    GaussianPacket1D,
    GaussianPacket2D,
    GridConfig,
    SimulationConfig,
)
from quantum_wave.simulation import (
    QuantumSimulation,
    create_1d_simulation,
    create_2d_simulation,
)
from quantum_wave.solver import CrankNicolsonSolver

__all__ = [
    "CrankNicolsonSolver",
    "GaussianPacket1D",
    "GaussianPacket2D",
    "GridConfig",
    "QuantumSimulation",
    "SimulationConfig",
    "create_1d_simulation",
    "create_2d_simulation",
]

__version__ = "1.0.0"
