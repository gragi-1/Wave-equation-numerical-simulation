"""High-level simulation factories used by both the API and the UI."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike, NDArray

from quantum_wave.config import (
    GaussianPacket1D,
    GaussianPacket2D,
    GridConfig,
    SimulationConfig,
)
from quantum_wave.operators import build_hamiltonian
from quantum_wave.solver import CrankNicolsonSolver
from quantum_wave.states import coordinate_axis, gaussian_packet_1d, gaussian_packet_2d


@dataclass(slots=True)
class QuantumSimulation:
    """A shape-aware façade around the vector-based numerical solver."""

    config: SimulationConfig
    solver: CrankNicolsonSolver

    @property
    def axis(self) -> NDArray[np.float64]:
        """Uniform coordinate axis shared by every spatial dimension."""

        return coordinate_axis(self.config.grid)

    @property
    def wave_function(self) -> NDArray[np.complex128]:
        """Current field with explicit zero values on the box boundary."""

        grid = self.config.grid
        full_state = np.zeros(grid.shape, dtype=np.complex128)
        interior_slice = (slice(1, -1),) * grid.dimensions
        full_state[interior_slice] = self.solver.state.reshape(grid.interior_shape)
        return full_state

    @property
    def probability_density(self) -> NDArray[np.float64]:
        """The observable probability density ``|ψ|²`` on the full grid."""

        return np.abs(self.wave_function) ** 2

    def step(self, count: int = 1) -> NDArray[np.float64]:
        """Advance the simulation and return the updated probability density."""

        self.solver.step(count)
        return self.probability_density

    def reset(self) -> NDArray[np.float64]:
        """Restore the initial wave packet and return its probability density."""

        self.solver.reset()
        return self.probability_density


def create_1d_simulation(
    config: SimulationConfig | None = None,
    packet: GaussianPacket1D | None = None,
    potential: ArrayLike | None = None,
) -> QuantumSimulation:
    """Create a ready-to-run 1D infinite-well simulation."""

    resolved_config = config or SimulationConfig(
        grid=GridConfig(dimensions=1, points=256),
        time_step=5e-5,
    )
    if resolved_config.grid.dimensions != 1:
        raise ValueError("create_1d_simulation requires a one-dimensional grid.")

    initial_state = gaussian_packet_1d(resolved_config.grid, packet or GaussianPacket1D())
    solver = CrankNicolsonSolver(
        build_hamiltonian(resolved_config, potential),
        initial_state,
        time_step=resolved_config.time_step,
        hbar=resolved_config.hbar,
        cell_measure=resolved_config.grid.cell_measure,
    )
    return QuantumSimulation(resolved_config, solver)


def create_2d_simulation(
    config: SimulationConfig | None = None,
    packet: GaussianPacket2D | None = None,
    potential: ArrayLike | None = None,
) -> QuantumSimulation:
    """Create a ready-to-run 2D infinite-square-well simulation."""

    resolved_config = config or SimulationConfig(
        grid=GridConfig(dimensions=2, points=64),
        time_step=1e-4,
    )
    if resolved_config.grid.dimensions != 2:
        raise ValueError("create_2d_simulation requires a two-dimensional grid.")

    initial_state = gaussian_packet_2d(resolved_config.grid, packet or GaussianPacket2D())
    solver = CrankNicolsonSolver(
        build_hamiltonian(resolved_config, potential),
        initial_state,
        time_step=resolved_config.time_step,
        hbar=resolved_config.hbar,
        cell_measure=resolved_config.grid.cell_measure,
    )
    return QuantumSimulation(resolved_config, solver)
