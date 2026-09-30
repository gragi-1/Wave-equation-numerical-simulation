"""Command-line interface for launching interactive simulations."""

from __future__ import annotations

import argparse
import math
from collections.abc import Sequence

from quantum_wave import __version__
from quantum_wave.config import (
    GaussianPacket1D,
    GaussianPacket2D,
    GridConfig,
    SimulationConfig,
)
from quantum_wave.simulation import create_1d_simulation, create_2d_simulation


def _positive_int(value: str) -> int:
    parsed = int(value)
    if parsed < 1:
        raise argparse.ArgumentTypeError("value must be a positive integer")
    return parsed


def _grid_points(value: str) -> int:
    parsed = int(value)
    if parsed < 5:
        raise argparse.ArgumentTypeError("value must be an integer greater than or equal to 5")
    return parsed


def _positive_float(value: str) -> float:
    parsed = float(value)
    if not math.isfinite(parsed) or parsed <= 0:
        raise argparse.ArgumentTypeError("value must be a positive, finite number")
    return parsed


def _finite_float(value: str) -> float:
    parsed = float(value)
    if not math.isfinite(parsed):
        raise argparse.ArgumentTypeError("value must be finite")
    return parsed


def _add_runtime_options(parser: argparse.ArgumentParser, *, default_points: int) -> None:
    parser.add_argument(
        "--points", type=_grid_points, default=default_points, help="grid points per axis"
    )
    parser.add_argument(
        "--time-step", type=_positive_float, default=1e-4, help="integration time step"
    )
    parser.add_argument(
        "--steps-per-frame",
        type=_positive_int,
        default=4,
        help="solver steps between rendered frames",
    )
    parser.add_argument(
        "--interval",
        type=_positive_int,
        default=30,
        metavar="MS",
        help="target delay between frames in milliseconds",
    )


def build_parser() -> argparse.ArgumentParser:
    """Build the public command-line parser."""

    parser = argparse.ArgumentParser(
        prog="quantum-wave",
        description="Explore Gaussian quantum wave packets in infinite potential wells.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    one_dimensional = subparsers.add_parser("1d", help="launch the 1D line visualization")
    _add_runtime_options(one_dimensional, default_points=256)
    one_dimensional.set_defaults(time_step=5e-5, steps_per_frame=8, interval=24)
    one_dimensional.add_argument("--center", type=_finite_float, default=0.35)
    one_dimensional.add_argument("--width", type=_positive_float, default=0.06)
    one_dimensional.add_argument("--wave-number", type=_finite_float, default=30.0)

    two_dimensional = subparsers.add_parser("2d", help="launch a 2D visualization")
    _add_runtime_options(two_dimensional, default_points=64)
    two_dimensional.set_defaults(time_step=1e-4, steps_per_frame=3, interval=32)
    two_dimensional.add_argument(
        "--view",
        choices=("heatmap", "surface"),
        default="heatmap",
        help="rendering mode (default: heatmap)",
    )
    two_dimensional.add_argument("--center-x", type=_finite_float, default=0.35)
    two_dimensional.add_argument("--center-y", type=_finite_float, default=0.50)
    two_dimensional.add_argument("--width", type=_positive_float, default=0.075)
    two_dimensional.add_argument("--wave-number-x", type=_finite_float, default=22.0)
    two_dimensional.add_argument("--wave-number-y", type=_finite_float, default=8.0)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Parse command-line options and open the requested visualization."""

    parser = build_parser()
    args = parser.parse_args(argv)
    dimensions = 1 if args.command == "1d" else 2
    try:
        config = SimulationConfig(
            grid=GridConfig(dimensions=dimensions, points=args.points),
            time_step=args.time_step,
        )

        if args.command == "1d":
            packet = GaussianPacket1D(args.center, args.width, args.wave_number)
            simulation = create_1d_simulation(config, packet)
        else:
            packet = GaussianPacket2D(
                args.center_x,
                args.center_y,
                args.width,
                args.wave_number_x,
                args.wave_number_y,
            )
            simulation = create_2d_simulation(config, packet)
    except ValueError as error:
        parser.error(str(error))

    if args.command == "1d":
        from quantum_wave.visualization import show_1d

        show_1d(
            simulation,
            steps_per_frame=args.steps_per_frame,
            interval_ms=args.interval,
        )
        return 0

    from quantum_wave.visualization import show_2d

    show_2d(
        simulation,
        view=args.view,
        steps_per_frame=args.steps_per_frame,
        interval_ms=args.interval,
    )
    return 0
