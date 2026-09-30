"""Visual identity shared by interactive views and generated artwork."""

from __future__ import annotations

from matplotlib import pyplot as plt

BACKGROUND = "#07111f"
PANEL = "#0d1b2a"
GRID = "#24364f"
TEXT = "#eef6ff"
MUTED = "#91a4bc"
ACCENT = "#5eead4"
COLORMAP = "magma"


def apply_theme() -> None:
    """Apply a compact dark theme suited to scientific visualization."""

    plt.rcParams.update(
        {
            "figure.facecolor": BACKGROUND,
            "axes.facecolor": PANEL,
            "axes.edgecolor": GRID,
            "axes.labelcolor": MUTED,
            "axes.titlecolor": TEXT,
            "axes.titleweight": "bold",
            "axes.grid": True,
            "axes.grid.which": "major",
            "axes.axisbelow": True,
            "grid.color": GRID,
            "grid.alpha": 0.55,
            "grid.linewidth": 0.7,
            "text.color": TEXT,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "font.family": "sans-serif",
            "font.size": 10,
            "savefig.facecolor": BACKGROUND,
            "savefig.bbox": "tight",
        }
    )
