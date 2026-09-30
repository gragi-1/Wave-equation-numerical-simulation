"""Sparse finite-difference operators for the Schrödinger equation."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike
from scipy.sparse import csc_matrix, diags, eye, kron

from quantum_wave.config import SimulationConfig


def _laplacian_1d(interior_points: int, spacing: float) -> csc_matrix:
    """Return the centered second-derivative operator on interior nodes."""

    main = np.full(interior_points, -2.0)
    off_diagonal = np.ones(interior_points - 1)
    return (
        diags(
            (off_diagonal, main, off_diagonal),
            offsets=(-1, 0, 1),
            format="csc",
        )
        / spacing**2
    )


def build_laplacian(config: SimulationConfig) -> csc_matrix:
    """Build a 1D or 2D Cartesian Laplacian with zero Dirichlet boundaries."""

    grid = config.grid
    laplacian_1d = _laplacian_1d(grid.points - 2, grid.spacing)
    if grid.dimensions == 1:
        return laplacian_1d

    identity = eye(grid.points - 2, format="csc")
    return (
        kron(laplacian_1d, identity, format="csc") + kron(identity, laplacian_1d, format="csc")
    ).tocsc()


def _interior_potential(config: SimulationConfig, potential: ArrayLike | None) -> np.ndarray:
    grid = config.grid
    if potential is None:
        return np.zeros(grid.interior_size)

    values = np.asarray(potential, dtype=float)
    if values.shape == grid.shape:
        interior = values[(slice(1, -1),) * grid.dimensions]
    elif values.shape == grid.interior_shape:
        interior = values
    else:
        raise ValueError(
            "potential must match either the full grid shape "
            f"{grid.shape} or the interior shape {grid.interior_shape}; received {values.shape}."
        )

    if not np.all(np.isfinite(interior)):
        raise ValueError("potential must contain only finite values.")
    return interior.reshape(-1)


def build_hamiltonian(
    config: SimulationConfig,
    potential: ArrayLike | None = None,
) -> csc_matrix:
    """Construct ``H = -(ℏ² / 2m)∇² + V`` as a sparse Hermitian matrix."""

    kinetic = -(config.hbar**2 / (2.0 * config.mass)) * build_laplacian(config)
    potential_operator = diags(_interior_potential(config, potential), format="csc")
    return (kinetic + potential_operator).tocsc()
