# Contributing

Contributions that improve numerical correctness, performance, documentation, or the user
experience are welcome.

## Development setup

```bash
python -m venv .venv
```

Activate the environment with `.venv\Scripts\activate` on Windows or
`source .venv/bin/activate` on macOS and Linux, then install the development dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Quality checks

Run the complete local quality gate before opening a pull request:

```bash
ruff format --check .
ruff check .
pytest --cov=quantum_wave --cov-report=term-missing
```

Use `ruff format .` to apply the repository's formatting rules.

## Design expectations

- Keep the numerical core independent from Matplotlib.
- Prefer sparse operators for every production-sized simulation.
- Add tests for numerical behavior, not only code paths.
- Explain the reason behind a decision; avoid comments that merely restate the code.
- Keep all source code, UI copy, documentation, and commit messages in English.
