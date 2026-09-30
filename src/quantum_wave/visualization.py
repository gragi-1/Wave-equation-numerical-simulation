"""Interactive Matplotlib views for 1D and 2D simulations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button

from quantum_wave.simulation import QuantumSimulation
from quantum_wave.theme import ACCENT, BACKGROUND, COLORMAP, GRID, MUTED, PANEL, TEXT, apply_theme


@dataclass(slots=True)
class _PlaybackController:
    simulation: QuantumSimulation
    steps_per_frame: int
    paused: bool = False

    def advance(self) -> np.ndarray:
        if not self.paused:
            return self.simulation.step(self.steps_per_frame)
        return self.simulation.probability_density

    def toggle(self, _event: Any) -> None:
        self.paused = not self.paused

    def reset(self, _event: Any) -> None:
        self.simulation.reset()
        self.paused = True


def _add_controls(
    figure: plt.Figure,
    controller: _PlaybackController,
) -> tuple[Button, Button]:
    toggle_axis = figure.add_axes((0.72, 0.035, 0.11, 0.05), facecolor=PANEL)
    reset_axis = figure.add_axes((0.845, 0.035, 0.11, 0.05), facecolor=PANEL)
    toggle_button = Button(toggle_axis, "Pause", color=PANEL, hovercolor=GRID)
    reset_button = Button(reset_axis, "Reset", color=PANEL, hovercolor=GRID)

    def toggle(event: Any) -> None:
        controller.toggle(event)
        toggle_button.label.set_text("Resume" if controller.paused else "Pause")

    def reset(event: Any) -> None:
        controller.reset(event)
        toggle_button.label.set_text("Resume")

    toggle_button.label.set_color(TEXT)
    reset_button.label.set_color(TEXT)
    toggle_button.on_clicked(toggle)
    reset_button.on_clicked(reset)
    return toggle_button, reset_button


def _status_text(figure: plt.Figure) -> plt.Text:
    return figure.text(0.08, 0.055, "", color=MUTED, fontsize=9, family="monospace")


def _status_line(simulation: QuantumSimulation) -> str:
    return (
        f"t = {simulation.solver.time:8.5f}    "
        f"step = {simulation.solver.step_index:6d}    "
        f"∫|ψ|² = {simulation.solver.total_probability:.8f}"
    )


def show_1d(
    simulation: QuantumSimulation,
    *,
    steps_per_frame: int = 8,
    interval_ms: int = 24,
) -> None:
    """Open an interactive line view of a 1D probability density."""

    apply_theme()
    figure, axis = plt.subplots(figsize=(11, 6.5))
    figure.subplots_adjust(left=0.09, right=0.96, top=0.86, bottom=0.18)
    controller = _PlaybackController(simulation, steps_per_frame)

    density = simulation.probability_density
    (line,) = axis.plot(simulation.axis, density, color=ACCENT, linewidth=2.4)
    fill = axis.fill_between(simulation.axis, density, color=ACCENT, alpha=0.12)
    axis.set(xlabel="Position, x", ylabel=r"Probability density, $|\psi(x,t)|^2$")
    axis.set_xlim(0.0, simulation.config.grid.length)
    axis.set_ylim(0.0, float(density.max()) * 1.25)
    figure.suptitle("Quantum Wave Lab", x=0.09, ha="left", fontsize=19, fontweight="bold")
    axis.set_title("1D Gaussian wave packet · infinite potential well", loc="left", pad=14)
    status = _status_text(figure)
    controls = _add_controls(figure, controller)

    def update(_frame: int) -> tuple[Any, ...]:
        nonlocal fill
        updated_density = controller.advance()
        line.set_ydata(updated_density)
        fill.remove()
        fill = axis.fill_between(simulation.axis, updated_density, color=ACCENT, alpha=0.12)
        current_limit = axis.get_ylim()[1]
        if updated_density.max() > current_limit * 0.92:
            axis.set_ylim(0.0, float(updated_density.max()) * 1.25)
        status.set_text(_status_line(simulation))
        return line, fill, status

    status.set_text(_status_line(simulation))
    animation = FuncAnimation(
        figure,
        update,
        interval=interval_ms,
        blit=False,
        cache_frame_data=False,
    )
    figure._quantum_wave_artists = (animation, controls)  # type: ignore[attr-defined]
    plt.show()


def show_2d_heatmap(
    simulation: QuantumSimulation,
    *,
    steps_per_frame: int = 3,
    interval_ms: int = 32,
) -> None:
    """Open an interactive heatmap of a 2D probability density."""

    apply_theme()
    figure, axis = plt.subplots(figsize=(9, 7.5))
    figure.subplots_adjust(left=0.11, right=0.86, top=0.86, bottom=0.16)
    controller = _PlaybackController(simulation, steps_per_frame)

    density = simulation.probability_density
    image = axis.imshow(
        density.T,
        origin="lower",
        extent=(0.0, simulation.config.grid.length, 0.0, simulation.config.grid.length),
        cmap=COLORMAP,
        interpolation="bicubic",
        aspect="equal",
        vmin=0.0,
        vmax=float(density.max()),
    )
    axis.grid(False)
    axis.set(xlabel="Position, x", ylabel="Position, y")
    figure.suptitle("Quantum Wave Lab", x=0.11, ha="left", fontsize=19, fontweight="bold")
    axis.set_title("2D probability density · infinite square well", loc="left", pad=14)
    colorbar = figure.colorbar(image, ax=axis, pad=0.03)
    colorbar.set_label(r"$|\psi(x,y,t)|^2$", color=MUTED)
    colorbar.outline.set_edgecolor(GRID)
    status = _status_text(figure)
    controls = _add_controls(figure, controller)

    def update(_frame: int) -> tuple[Any, ...]:
        updated_density = controller.advance()
        image.set_data(updated_density.T)
        status.set_text(_status_line(simulation))
        return image, status

    status.set_text(_status_line(simulation))
    animation = FuncAnimation(
        figure,
        update,
        interval=interval_ms,
        blit=False,
        cache_frame_data=False,
    )
    figure._quantum_wave_artists = (animation, controls)  # type: ignore[attr-defined]
    plt.show()


def show_2d_surface(
    simulation: QuantumSimulation,
    *,
    steps_per_frame: int = 3,
    interval_ms: int = 45,
) -> None:
    """Open an interactive 3D surface view of a 2D probability density."""

    apply_theme()
    figure = plt.figure(figsize=(10, 7.5))
    figure.subplots_adjust(left=0.02, right=0.98, top=0.88, bottom=0.14)
    axis = figure.add_subplot(111, projection="3d")
    axis.set_facecolor(BACKGROUND)
    controller = _PlaybackController(simulation, steps_per_frame)

    x, y = np.meshgrid(simulation.axis, simulation.axis, indexing="ij")
    density = simulation.probability_density
    surface = axis.plot_surface(
        x,
        y,
        density,
        cmap=COLORMAP,
        linewidth=0,
        antialiased=True,
        rcount=60,
        ccount=60,
    )
    surface_holder = [surface]
    axis.set(xlabel="Position, x", ylabel="Position, y", zlabel=r"$|\psi|^2$")
    axis.set_zlim(0.0, float(density.max()) * 1.25)
    axis.view_init(elev=32, azim=-58)
    figure.suptitle("Quantum Wave Lab", x=0.08, ha="left", fontsize=19, fontweight="bold")
    axis.set_title("2D probability density · surface view", pad=18)
    status = _status_text(figure)
    controls = _add_controls(figure, controller)

    def update(_frame: int) -> tuple[Any, ...]:
        updated_density = controller.advance()
        surface_holder[0].remove()
        surface_holder[0] = axis.plot_surface(
            x,
            y,
            updated_density,
            cmap=COLORMAP,
            linewidth=0,
            antialiased=True,
            rcount=60,
            ccount=60,
        )
        current_limit = axis.get_zlim()[1]
        if updated_density.max() > current_limit * 0.92:
            axis.set_zlim(0.0, float(updated_density.max()) * 1.25)
        status.set_text(_status_line(simulation))
        return surface_holder[0], status

    status.set_text(_status_line(simulation))
    animation = FuncAnimation(
        figure,
        update,
        interval=interval_ms,
        blit=False,
        cache_frame_data=False,
    )
    figure._quantum_wave_artists = (animation, controls)  # type: ignore[attr-defined]
    plt.show()


def show_2d(
    simulation: QuantumSimulation,
    *,
    view: Literal["heatmap", "surface"] = "heatmap",
    steps_per_frame: int = 3,
    interval_ms: int = 32,
) -> None:
    """Dispatch to one of the supported 2D visualizations."""

    if view == "heatmap":
        show_2d_heatmap(
            simulation,
            steps_per_frame=steps_per_frame,
            interval_ms=interval_ms,
        )
    elif view == "surface":
        show_2d_surface(
            simulation,
            steps_per_frame=steps_per_frame,
            interval_ms=interval_ms,
        )
    else:
        raise ValueError(f"Unsupported 2D view: {view!r}.")
