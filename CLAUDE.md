# CLAUDE.md

## Overview

**Cluefin**: Korean stock market analysis toolkit (Python, uv workspace monorepo)

### Packages
- `cluefin-openapi` — API clients (Kiwoom, KIS, DART)
- `cluefin-openapi-ts` — TypeScript OpenAPI client (npm/biome, independent of uv workspace)
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
uv run pytest -m integration                   # Integration tests (needs API keys in .env)
uv run pytest packages/cluefin-openapi         # Single package tests
uv run ruff format . && uv run ruff check . --fix  # Lint
```

### TypeScript (cluefin-openapi-ts)
```bash
cd packages/cluefin-openapi-ts
npm install                                    # Setup
npm run test:unit                              # Unit tests
npm run lint                                   # Biome lint
npm run build                                  # Build
```

## Conventions

- Git hooks via lefthook: pre-commit runs ruff (Python) + biome (TS), pre-push runs tests
- Always use `uv run`, never bare `python`
- Pydantic aliasing: Korean API fields → English (`stck_prpr` → `current_price`)
- Auth: Kiwoom (OAuth2), KIS (token cache), DART (auth_key)
- Secrets in `.env` only, managed via `pydantic_settings.BaseSettings`
- Rate limiting: `TokenBucket` from `cluefin_openapi._rate_limiter`
- Unit tests use mocks; integration tests (`@pytest.mark.integration`) need real API keys
- Ruff: line 120, target py311, rules `E,F,W,B,Q,I,ASYNC,T20`
- Python 3.10+, stock codes are 6-digit strings (e.g., `"005930"`)
- TypeScript: Biome (not ESLint), Vitest (not Jest), tsup for bundling
- TS package uses Zod schemas for runtime API response validation
