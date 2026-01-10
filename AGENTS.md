# AGENTS.md

## Project Summary
- Cluefin: Korean stock market analysis toolkit (educational/research only)
- uv workspace monorepo with three main parts:
  - `packages/cluefin-openapi/`: API clients (Kiwoom, KIS, KRX, DART)
  - `packages/cluefin-ta/`: Pure Python TA-Lib-compatible indicators
  - `apps/cluefin-cli/`: CLI with TA + LightGBM/SHAP features

## Dev Workflow (important)
- Always use `uv run` (do not run `python` directly)
- Python 3.10+
- macOS ML dependency: `brew install lightgbm`
- Set API keys in `.env` (see `apps/cluefin-cli/.env.sample`)

## Common Commands
```bash
uv sync --all-packages
uv run pytest -m "not integration"
uv run ruff format .
uv run ruff check . --fix
```

## Quick CLI Usage
```bash
cluefin-cli ta 005930
cluefin-cli ta 005930 --chart --ml-predict --shap-analysis
```
