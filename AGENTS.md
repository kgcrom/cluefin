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
