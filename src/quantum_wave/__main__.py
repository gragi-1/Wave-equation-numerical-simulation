"""Allow the application to be launched with ``python -m quantum_wave``."""

from quantum_wave.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
