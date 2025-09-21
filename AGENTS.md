# Repository Guidelines

## Project Structure & Module Organization
Cluefin uses a uv workspace monorepo. Core APIs live in `packages/cluefin-openapi/src`, the interactive CLI lives in `apps/cluefin-cli`, shared docs stay in `docs/`, and repository-wide settings (pyproject, uv.lock) sit at the root. Tests mirror their packages under `packages/cluefin-openapi/tests` and `apps/cluefin-cli/tests`.

## Build, Test, and Development Commands
Run `uv sync --all-packages` after pulling to align virtualenvs. Use `uv run cluefin-cli inquiry` for the interactive stock analysis CLI and `uv run cluefin-cli analyze 005930 --chart --ai-analysis --ml-predict --shap-analysis` when validating advanced flows. Execute `uv run pytest -m "not integration"` for fast checks, `uv run pytest` for the full suite, and `uv run pytest -m integration` when KIWOOM credentials are available. Format and lint with `uv run ruff format .` and `uv run ruff check . --fix`.

## Coding Style & Naming Conventions
Python code uses 4-space indentation, 120-character lines, and Python 3.11 typing. Favor descriptive snake_case for functions and modules, and PascalCase for classes. Validate style with Ruff; do not hand-edit imports. Keep docstrings concise and prefer Korean descriptors only when the upstream API demands them.

## Testing Guidelines
Prefer pytest fixtures over ad-hoc helpers. Name integration tests with `_integration` suffix and guard them with the `integration` marker. Slow external calls should use the `slow` marker. Mock outbound HTTP in unit tests via `requests_mock`. Record new regression scenarios close to the code they verify inside the corresponding package test tree.

## Commit & Pull Request Guidelines
Follow Conventional Commits (e.g., `feat: add dart disclosure fetcher`). Combine related changes into one commit and include breaking changes in the footer. PRs must describe user impact, list verification commands, and link related issues. Attach terminal or screenshot evidence for CLI-facing updates; note any configuration prerequisites. Confirm CI passes before requesting review.

## Security & Configuration Tips
Never commit `.env` or API keys. Start from `apps/cluefin-cli/.env.sample`, keeping KIWOOM and OpenAI secrets local. Rotate tokens when running integration tests. Review `docs/ARCHITECTURE.md` if you extend authentication flows, and notify maintainers of any discovered security gaps.
