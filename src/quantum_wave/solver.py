"""A reusable sparse Crank-Nicolson time integrator."""

from __future__ import annotations

import math

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.sparse import csc_matrix, eye
from scipy.sparse.linalg import SuperLU, splu


class CrankNicolsonSolver:
    """Evolve a state under a time-independent sparse Hamiltonian.

    The left-hand matrix is factorized once and reused at every time step.
    This keeps the interactive animation responsive without sacrificing the
    norm-preserving behavior of the Crank-Nicolson scheme.
    """

    def __init__(
        self,
        hamiltonian: csc_matrix,
        initial_state: ArrayLike,
        *,
        time_step: float,
        hbar: float,
        cell_measure: float,
    ) -> None:
        state = np.asarray(initial_state, dtype=np.complex128).reshape(-1)
        if hamiltonian.shape != (state.size, state.size):
            raise ValueError("The Hamiltonian shape must match the state-vector size.")
        numerical_parameters = (time_step, hbar, cell_measure)
        if not all(math.isfinite(value) and value > 0 for value in numerical_parameters):
            raise ValueError("time_step, hbar, and cell_measure must be positive and finite.")
        if not np.all(np.isfinite(state)):
            raise ValueError("The initial state must contain only finite values.")

        self._initial_state = state.copy()
        self._state = state.copy()
        self._time_step = float(time_step)
        self._cell_measure = float(cell_measure)
        self._step_index = 0

        identity = eye(state.size, format="csc", dtype=np.complex128)
        scaled_hamiltonian = (0.5j * time_step / hbar) * hamiltonian
        self._right_operator = (identity - scaled_hamiltonian).tocsc()
        self._left_factorization: SuperLU = splu((identity + scaled_hamiltonian).tocsc())

    @property
    def state(self) -> NDArray[np.complex128]:
        """A defensive copy of the current state vector."""

        return self._state.copy()

    @property
    def time(self) -> float:
        """Current simulated time."""

        return self._step_index * self._time_step

    @property
    def step_index(self) -> int:
        """Number of completed integration steps."""

        return self._step_index

    @property
    def total_probability(self) -> float:
        """Numerical integral of the current probability density."""

        return float(np.sum(np.abs(self._state) ** 2) * self._cell_measure)

    def step(self, count: int = 1) -> NDArray[np.complex128]:
        """Advance the state by ``count`` time steps and return a copy."""

        if isinstance(count, bool) or not isinstance(count, int) or count < 1:
            raise ValueError("count must be a positive integer.")
        for _ in range(count):
            right_hand_side = self._right_operator @ self._state
            self._state = self._left_factorization.solve(right_hand_side)
        self._step_index += count
        return self.state

    def reset(self) -> NDArray[np.complex128]:
        """Restore the normalized initial state and reset simulated time."""

        self._state = self._initial_state.copy()
        self._step_index = 0
        return self.state
