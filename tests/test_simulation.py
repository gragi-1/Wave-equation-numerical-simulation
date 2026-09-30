import numpy as np
import pytest

from quantum_wave.config import GridConfig, SimulationConfig
from quantum_wave.simulation import create_1d_simulation, create_2d_simulation


def test_1d_state_is_normalized_and_respects_boundaries() -> None:
    simulation = create_1d_simulation(
        SimulationConfig(GridConfig(dimensions=1, points=96), time_step=2e-5)
    )

    assert simulation.solver.total_probability == pytest.approx(1.0)
    assert simulation.wave_function.shape == (96,)
    assert simulation.wave_function[0] == 0.0
    assert simulation.wave_function[-1] == 0.0


def test_crank_nicolson_conserves_probability() -> None:
    simulation = create_1d_simulation(
        SimulationConfig(GridConfig(dimensions=1, points=80), time_step=5e-5)
    )

    simulation.step(250)

    assert simulation.solver.total_probability == pytest.approx(1.0, abs=2e-12)


def test_reset_restores_state_and_time() -> None:
    simulation = create_1d_simulation(
        SimulationConfig(GridConfig(dimensions=1, points=64), time_step=1e-4)
    )
    initial_state = simulation.wave_function

    simulation.step(10)
    simulation.reset()

    np.testing.assert_allclose(simulation.wave_function, initial_state)
    assert simulation.solver.step_index == 0
    assert simulation.solver.time == 0.0


def test_2d_simulation_returns_full_square_field() -> None:
    simulation = create_2d_simulation(
        SimulationConfig(GridConfig(dimensions=2, points=18), time_step=1e-4)
    )

    density = simulation.step(2)

    assert density.shape == (18, 18)
    assert np.all(density[[0, -1], :] == 0.0)
    assert np.all(density[:, [0, -1]] == 0.0)
    assert simulation.solver.total_probability == pytest.approx(1.0, abs=2e-12)
