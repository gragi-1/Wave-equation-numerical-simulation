import numpy as np
import pytest
from scipy.sparse import eye

from quantum_wave.solver import CrankNicolsonSolver


def test_solver_rejects_incompatible_shapes() -> None:
    with pytest.raises(ValueError, match="Hamiltonian shape"):
        CrankNicolsonSolver(
            eye(3, format="csc"),
            np.ones(4),
            time_step=0.1,
            hbar=1.0,
            cell_measure=1.0,
        )


def test_step_count_must_be_positive_integer() -> None:
    solver = CrankNicolsonSolver(
        eye(2, format="csc"),
        np.array([1.0, 0.0]),
        time_step=0.1,
        hbar=1.0,
        cell_measure=1.0,
    )

    with pytest.raises(ValueError, match="positive integer"):
        solver.step(0)
