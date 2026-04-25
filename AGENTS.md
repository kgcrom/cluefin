# AGENTS.md

## Project

Cluefin is a uv workspace for Korean market research tools.

- `packages/cluefin-openapi`: broker and disclosure clients
- `packages/cluefin-ta`: technical indicators
- `packages/cluefin-xbrl`: XBRL parsing
- `apps/cluefin-cli`: user-facing CLI
- `apps/cluefin-openapi-cli`: broker command CLI

## Working Rules

- Always use `uv run`
- Python 3.10+
- Set API keys in `.env`
- On macOS, install `lightgbm` with `brew install lightgbm`

## Agent Workflow

- Keep the uv workspace structure as-is: reusable libraries under `packages/`, runnable tools under `apps/`.
- Prefer fast local verification first: `uv run pytest -m "not integration and not slow"`.
- For broker command discovery, use JSON-friendly CLI commands:
  - `uv run cluefin-openapi-cli list --json`
  - `uv run cluefin-openapi-cli describe <broker> <category> <method> --json`
  - `uv run cluefin-openapi-cli describe dart <method> --json`
- Do not add repo-local `.pi/` or `SYSTEM.md` files unless a task explicitly asks for Pi package/runtime customization.

## Common Commands

```bash
uv sync --all-packages
uv run pytest -m "not integration"
uv run ruff format .
uv run ruff check . --fix
```

## Quick Usage

```bash
cluefin-cli ta 005930
cluefin-cli ta 005930 --chart --ml-predict --shap-analysis
```
