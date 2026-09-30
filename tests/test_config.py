import pytest

from quantum_wave.config import GridConfig, SimulationConfig


def test_grid_exposes_consistent_geometry() -> None:
    grid = GridConfig(dimensions=2, length=2.0, points=11)

    assert grid.spacing == pytest.approx(0.2)
    assert grid.shape == (11, 11)
    assert grid.interior_shape == (9, 9)
    assert grid.interior_size == 81
    assert grid.cell_measure == pytest.approx(0.04)


@pytest.mark.parametrize(
    ("field", "value"),
    [("length", 0.0), ("points", 4), ("dimensions", 3)],
)
def test_grid_rejects_invalid_values(field: str, value: float) -> None:
    arguments = {"dimensions": 1, "length": 1.0, "points": 32, field: value}

    with pytest.raises(ValueError):
        GridConfig(**arguments)


def test_simulation_requires_positive_physical_values() -> None:
    grid = GridConfig(dimensions=1)

    with pytest.raises(ValueError, match="mass"):
        SimulationConfig(grid=grid, mass=0.0)
