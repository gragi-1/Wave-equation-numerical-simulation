import numpy as np
import pytest

from quantum_wave.config import GridConfig, SimulationConfig
from quantum_wave.operators import build_hamiltonian


@pytest.mark.parametrize(("dimensions", "points"), [(1, 12), (2, 8)])
def test_hamiltonian_is_sparse_hermitian(dimensions: int, points: int) -> None:
    config = SimulationConfig(GridConfig(dimensions=dimensions, points=points))

    hamiltonian = build_hamiltonian(config)
    difference = hamiltonian - hamiltonian.getH()

    assert hamiltonian.shape == (config.grid.interior_size,) * 2
    assert difference.nnz == 0


def test_full_grid_potential_is_restricted_to_interior() -> None:
    config = SimulationConfig(GridConfig(dimensions=1, points=7))
    potential = np.arange(7, dtype=float)

    free = build_hamiltonian(config).diagonal()
    shifted = build_hamiltonian(config, potential).diagonal()

    np.testing.assert_allclose(shifted - free, potential[1:-1])


def test_potential_shape_is_validated() -> None:
    config = SimulationConfig(GridConfig(dimensions=2, points=7))

    with pytest.raises(ValueError, match="potential must match"):
        build_hamiltonian(config, np.zeros((3, 3)))
