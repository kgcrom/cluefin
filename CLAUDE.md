# CLAUDE.md

## Project Overview

**Cluefin**: Python toolkit for Korean stock market analysis (uv workspace monorepo)

- **cluefin-openapi** (`packages/cluefin-openapi/`): API clients for Kiwoom, KIS, KRX, DART
- **cluefin-ta** (`packages/cluefin-ta/`): Pure Python TA library (TA-Lib compatible, no C deps)
- **cluefin-cli** (`apps/cluefin-cli/`): CLI with TA, ML predictions (LightGBM), SHAP

Educational/research project—not for production trading.

## Development Commands

**CRITICAL: Always use `uv run` instead of `python`**

```bash
# Setup
uv venv --python 3.10 && uv sync --all-packages
cp apps/cluefin-cli/.env.sample .env  # Add API keys

# Testing
uv run pytest -m "not integration"  # Unit tests (no API keys)
uv run pytest                        # All tests

# Code Quality
uv run ruff format . && uv run ruff check . --fix

# CLI
cluefin-cli ta 005930 --chart --ml-predict --shap-analysis
```

## Architecture

### Key Directories
```
packages/cluefin-openapi/src/cluefin_openapi/{kiwoom,kis,krx,dart}/
packages/cluefin-ta/src/cluefin_ta/{overlap,momentum,volatility,volume,pattern,portfolio}.py
apps/cluefin-cli/src/cluefin_cli/{commands,config,data,display,ml}/
```

### Design Patterns
- **Response Wrapper**: `KiwoomHttpResponse[T]` for unified pagination/status
- **Pydantic Aliasing**: Korean API fields → English (e.g., `stck_prpr` → `current_price`)
- **Auth**: Kiwoom (OAuth2, 1hr), KIS (token, 1min interval cache), KRX/DART (simple auth_key)
- **Data Pipeline**: Fetch → Transform → DuckDB upsert (date chunking for KIS 50-day limit)
- **ML Pipeline**: 150+ TA features → time-series CV → LightGBM → SHAP explainer

## Testing

- **Unit** (`tests/unit/`): Mock HTTP, Pydantic tests, no API keys
- **Integration** (`@pytest.mark.integration`): Real API calls, CI only with `ENABLE_INTEGRATION_TESTS=true`

## Important Notes

- Python 3.10+, Stock codes: 6-digit (e.g., "005930")
- Trading hours: 9:00-15:30 KST
- Secrets: `.env` only (gitignored), `pydantic_settings.BaseSettings`
- Rate limiting: `TokenBucket` from `cluefin_openapi._rate_limiter`
- Ruff: line 120, target py311, rules `E,F,W,B,Q,I,ASYNC,T20`, ignore `F401,E501`
- CI: push to `main` only (lint, test py3.10-3.12, coverage, pip-audit)
