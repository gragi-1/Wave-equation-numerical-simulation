import pytest

from quantum_wave.cli import build_parser, main


def test_1d_command_uses_documented_defaults() -> None:
    arguments = build_parser().parse_args(["1d"])

    assert arguments.command == "1d"
    assert arguments.points == 256
    assert arguments.time_step == pytest.approx(5e-5)
    assert arguments.steps_per_frame == 8


def test_2d_view_can_be_selected() -> None:
    arguments = build_parser().parse_args(["2d", "--view", "surface", "--points", "48"])

    assert arguments.view == "surface"
    assert arguments.points == 48


@pytest.mark.parametrize(
    "arguments",
    [
        ["1d", "--points", "4"],
        ["1d", "--time-step", "0"],
        ["1d", "--width", "nan"],
        ["2d", "--steps-per-frame", "0"],
    ],
)
def test_cli_rejects_invalid_numerical_values(arguments: list[str]) -> None:
    with pytest.raises(SystemExit):
        build_parser().parse_args(arguments)


def test_main_reports_packet_outside_domain_as_usage_error(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit):
        main(["1d", "--center", "2.0"])

    assert "packet center must lie inside" in capsys.readouterr().err
