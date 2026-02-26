# CLAUDE.md

## Overview

**Cluefin**: Korean stock market analysis toolkit (Python, uv workspace monorepo)

### Packages
- `cluefin-openapi` — API clients (Kiwoom, KIS, KRX, DART)
- `cluefin-ta` — Technical analysis (TA-Lib compatible, pure Python)
- `cluefin-xbrl` — XBRL/DART financial statement parser

### Apps
- `cluefin-cli` — CLI (TA, ML predictions, SHAP)
- `cluefin-desk` — TUI dashboard
- `cluefin-rpc` — RPC server

## Commands

```bash
uv sync --all-packages                        # Setup
uv run pytest -m "not integration"             # Unit tests
uv run ruff format . && uv run ruff check . --fix  # Lint
```

## Conventions

- Always use `uv run`, never bare `python`
- Pydantic aliasing: Korean API fields → English (`stck_prpr` → `current_price`)
- Auth: Kiwoom (OAuth2), KIS (token cache), KRX/DART (auth_key)
- Secrets in `.env` only, managed via `pydantic_settings.BaseSettings`
- Rate limiting: `TokenBucket` from `cluefin_openapi._rate_limiter`
- Unit tests use mocks; integration tests (`@pytest.mark.integration`) need real API keys
- Ruff: line 120, target py311, rules `E,F,W,B,Q,I,ASYNC,T20`
- Python 3.10+, stock codes are 6-digit strings (e.g., `"005930"`)
