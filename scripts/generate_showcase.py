"""Regenerate the README artwork from actual simulation data."""

from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")

import matplotlib.pyplot as plt

from quantum_wave.config import GridConfig, SimulationConfig
from quantum_wave.simulation import create_1d_simulation, create_2d_simulation
from quantum_wave.theme import ACCENT, BACKGROUND, COLORMAP, MUTED, TEXT, apply_theme

OUTPUT_DIRECTORY = Path(__file__).resolve().parents[1] / "docs" / "assets"


def generate_showcase() -> Path:
    """Render a reproducible two-panel overview for the project README."""

    apply_theme()
    simulation_1d = create_1d_simulation(
        SimulationConfig(GridConfig(dimensions=1, points=220), time_step=5e-5)
    )
    simulation_2d = create_2d_simulation(
        SimulationConfig(GridConfig(dimensions=2, points=56), time_step=1e-4)
    )
    simulation_1d.step(180)
    simulation_2d.step(75)

    figure = plt.figure(figsize=(16, 8.8), facecolor=BACKGROUND)
    grid = figure.add_gridspec(
        2,
        2,
        height_ratios=(0.18, 0.82),
        width_ratios=(1.05, 0.95),
        hspace=0.05,
        wspace=0.18,
    )
    heading = figure.add_subplot(grid[0, :])
    heading.axis("off")
    heading.text(
        0.0,
        0.76,
        "QUANTUM WAVE LAB",
        color=ACCENT,
        fontsize=12,
        fontweight="bold",
        family="monospace",
        transform=heading.transAxes,
    )
    heading.text(
        0.0,
        0.25,
        "Sparse numerical physics, made visible.",
        color=TEXT,
        fontsize=25,
        fontweight="bold",
        transform=heading.transAxes,
    )
    heading.text(
        1.0,
        0.33,
        "CRANK–NICOLSON  /  1D + 2D  /  NORM PRESERVING",
        color=MUTED,
        fontsize=10,
        ha="right",
        family="monospace",
        transform=heading.transAxes,
    )

    axis_1d = figure.add_subplot(grid[1, 0])
    density_1d = simulation_1d.probability_density
    axis_1d.plot(simulation_1d.axis, density_1d, color=ACCENT, linewidth=2.3)
    axis_1d.fill_between(simulation_1d.axis, density_1d, color=ACCENT, alpha=0.14)
    axis_1d.set(
        xlabel="Position, x",
        ylabel=r"Probability density, $|\psi|^2$",
        xlim=(0.0, 1.0),
        ylim=(0.0, float(density_1d.max()) * 1.22),
    )
    axis_1d.set_title("01  WAVE-PACKET EVOLUTION", loc="left", family="monospace", fontsize=11)
    axis_1d.text(
        0.03,
        0.94,
        (
            f"t = {simulation_1d.solver.time:.4f}\n"
            f"∫|ψ|² = {simulation_1d.solver.total_probability:.8f}"
        ),
        transform=axis_1d.transAxes,
        va="top",
        color=MUTED,
        fontsize=9,
        family="monospace",
    )

    axis_2d = figure.add_subplot(grid[1, 1])
    density_2d = simulation_2d.probability_density
    image = axis_2d.imshow(
        density_2d.T,
        origin="lower",
        extent=(0.0, 1.0, 0.0, 1.0),
        cmap=COLORMAP,
        interpolation="bicubic",
    )
    axis_2d.grid(False)
    axis_2d.set(xlabel="Position, x", ylabel="Position, y")
    axis_2d.set_title("02  2D PROBABILITY FIELD", loc="left", family="monospace", fontsize=11)
    colorbar = figure.colorbar(image, ax=axis_2d, fraction=0.046, pad=0.04)
    colorbar.set_label(r"$|\psi|^2$", color=MUTED)

    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIRECTORY / "quantum-wave-lab.png"
    figure.savefig(output_path, dpi=180, facecolor=BACKGROUND)
    plt.close(figure)
    return output_path


if __name__ == "__main__":
    print(generate_showcase())
