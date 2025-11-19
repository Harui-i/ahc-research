# Repository Guidelines

## Project Structure & Module Organization
This repository explores high-speed matrix–vector kernels for AtCoder reinforcement-learning agents. The entry point `main.py` is for quick experiments; promote reusable code into a package directory such as `ahc_research/` so it can be imported cleanly. Store judge snapshots or benchmark fixtures inside `inputs/` with filenames that capture seed and scenario metadata. Keep `pyproject.toml` as the single source of project metadata and update it whenever you add dependencies or scripts to keep environments reproducible.

## Build, Test, and Development Commands
Create an isolated environment with `python -m venv .venv && source .venv/bin/activate`. Install the package locally via `pip install -e .` so iterative changes are immediately available. Run `python main.py` to verify wiring and quick experiments. Use `python -m pytest` for the automated test suite, adding `-k <pattern>` for focused runs. When benchmarking kernels, script the workflow (e.g., `python scripts/benchmark.py --size 200`) and record invocation details in commit messages.

## Coding Style & Naming Conventions
Follow PEP 8: four-space indentation, snake_case for functions/modules, and CamelCase for classes encapsulating kernels or evaluators. Keep modules single-purpose and prefer pure functions for mathematical kernels. Document non-obvious optimizations with short comments above the block they explain. Add type hints to public APIs and performance-critical code paths to clarify shapes and catch regressions early. Run `ruff check .` and `ruff format .` before pushing; add `ruff` to `pyproject.toml` if it is not yet listed.

## Testing Guidelines
Place unit and micro-benchmark tests under `tests/`, mirroring the package layout (e.g., `tests/test_kernels.py`). Name tests `test_<behavior>` and cover multiple matrix sizes (64, 128, 200) plus degenerate cases. For performance assertions, capture baseline timings in fixtures and assert against acceptable thresholds. Document deterministic seeds and input sources inside test docstrings so others can reproduce results.

## Commit & Pull Request Guidelines
Current history favors compact lowercase summaries (`init`, `readme`); continue with imperative, present-tense messages and keep body lines under 72 characters. Reference specific benchmarks, seeds, or AtCoder tasks whenever possible. Pull requests should outline motivation, complexity impact, and benchmark deltas; attach or link relevant files in `inputs/` and provide reproduction commands. Request review only after linting and tests pass locally, and note any follow-up work required.
