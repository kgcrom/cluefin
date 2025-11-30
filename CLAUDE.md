# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Cluefin** is a Python toolkit for Korean stock market analysis. It's structured as a **uv workspace monorepo** with three main components:

- **cluefin-openapi** (`packages/cluefin-openapi/`): Type-safe Python clients for Korean financial APIs (Kiwoom, KIS, KRX, DART)
- **cluefin-ta** (`packages/cluefin-ta/`): Pure Python technical analysis library (TA-Lib compatible API, no system dependencies)
- **cluefin-cli** (`apps/cluefin-cli/`): Interactive CLI with technical analysis, ML predictions (LightGBM), and SHAP explainability

This is an **educational/research project**—not for production trading systems.

## Development Commands

### CRITICAL: Always use `uv run` instead of `python`

```bash
# CORRECT
uv run pytest apps/cluefin-cli/tests/unit/ml/test_feature_engineering.py

# INCORRECT - Will use wrong environment
python -m pytest apps/cluefin-cli/tests/unit/ml/test_feature_engineering.py
```

### Setup
```bash
uv venv --python 3.10
uv sync --all-packages
brew install lightgbm  # macOS only: LightGBM system dependency for ML features

cp apps/cluefin-cli/.env.sample .env
# Edit .env: KIWOOM_APP_KEY, KIWOOM_SECRET_KEY, KIS_APP_KEY, KIS_SECRET_KEY, KRX_AUTH_KEY, DART_AUTH_KEY
```

### Testing
```bash
uv run pytest -m "not integration"  # Unit tests only (no API keys needed)
uv run pytest -m "not slow"          # Exclude slow tests
uv run pytest                        # All tests
uv run pytest packages/cluefin-openapi/tests/ -v
uv run pytest packages/cluefin-ta/tests/ -v
uv run pytest apps/cluefin-cli/tests/ -v
```

### Code Quality
```bash
uv run ruff format .       # Format code
uv run ruff check . --fix  # Lint and auto-fix
```

### CLI Usage
```bash
cluefin-cli ta 005930                                    # Basic technical analysis
cluefin-cli ta 005930 --chart --ml-predict --shap-analysis  # Full analysis
cluefin-cli fa 005930 --year 2023 --report annual        # Fundamental analysis (DART)
cluefin-cli import --stock --start 20250101 --end 20250131
cluefin-cli --debug ta 005930                            # Enable debug logging
```

## Architecture

### Project Structure
```
cluefin/
├── packages/
│   ├── cluefin-openapi/            # Reusable API clients
│   │   └── src/cluefin_openapi/
│   │       ├── kiwoom/             # Kiwoom Securities (OAuth2-style)
│   │       ├── kis/                # Korea Investment Securities (token-based)
│   │       ├── krx/                # Korea Exchange (simple auth_key)
│   │       ├── dart/               # DART corporate disclosures
│   │       └── _rate_limiter.py    # Shared TokenBucket rate limiter
│   │
│   └── cluefin-ta/                 # Pure Python TA library (TA-Lib drop-in replacement)
│       └── src/cluefin_ta/
│           ├── overlap.py          # SMA, EMA, BBANDS, KAMA, etc.
│           ├── momentum.py         # RSI, MACD, STOCH, ADX, CCI, etc.
│           ├── volatility.py       # ATR, NATR, TRANGE
│           ├── volume.py           # OBV, AD, ADOSC
│           ├── pattern.py          # Candlestick patterns (CDLDOJI, CDLHAMMER, etc.)
│           ├── portfolio.py        # MDD, SHARPE, SORTINO, CALMAR, CAGR
│           └── _core/              # NumPy/Numba implementations
│
└── apps/cluefin-cli/               # Interactive CLI application
    └── src/cluefin_cli/
        ├── commands/               # Click-based CLI handlers
        │   ├── technical_analysis.py
        │   ├── fundamental_analysis.py
        │   ├── import_cmd.py
        │   └── analysis/indicators.py
        ├── config/                 # Settings (Pydantic) & logging (ContextVar)
        ├── data/                   # DuckDB persistence & API data fetching
        │   ├── duckdb_manager.py
        │   ├── stock_fetcher.py
        │   ├── stock_importer.py
        │   └── industry_chart_importer.py
        ├── display/charts.py       # ASCII charts (plotext)
        └── ml/                     # LightGBM + SHAP pipeline
            ├── feature_engineering.py  # 150+ technical indicators
            ├── models.py               # LightGBM classifier
            ├── predictor.py            # Pipeline orchestration
            ├── explainer.py            # SHAP TreeExplainer
            └── diagnostics.py          # Model evaluation
```

### Key Design Patterns

**Response Wrapper Pattern**: API responses wrapped in `KiwoomHttpResponse[T]` for unified pagination/status handling.

**Pydantic Model Aliasing**: Korean API fields aliased to English:
```python
class QuoteResponse(BaseModel):
    current_price: int = Field(..., alias="stck_prpr")
```

**Authentication by API**:
- **Kiwoom**: OAuth2-style with `Auth.generate_token()` (1-hour validity)
- **KIS**: Token-based with 1-minute generation interval limit (cached tokens essential)
- **KRX/DART**: Simple `auth_key` per request

**Data Pipeline** (`import_cmd.py` orchestration):
1. Fetch via `StockChartImporter`/`IndustryChartImporter`
2. Transform to DuckDB schema
3. Insert with `ON CONFLICT ... DO UPDATE` for idempotency
4. Date chunking (KIS API: max 50 weekdays per request)

**ML Pipeline** (`ml/predictor.py`):
1. Feature engineering: 150+ technical indicators via cluefin-ta
2. Time-series cross-validation (prevents data leakage)
3. LightGBM with early stopping
4. SHAP TreeExplainer for interpretability

**cluefin-ta Design** (`packages/cluefin-ta/`):
- Drop-in replacement for TA-Lib: `import cluefin_ta as talib`
- Pure NumPy implementation (no C dependencies)
- Optional Numba JIT acceleration (`_core/numba_impl.py`)
- TA-Lib compatible function signatures and return values

## Testing Strategy

**Unit Tests** (`tests/unit/` or `test_*_unit.py`):
- Mock HTTP with `requests_mock`
- Test Pydantic deserialization, indicator calculations
- No API keys needed

**Integration Tests** (`test_*_integration.py`, `@pytest.mark.integration`):
- Real API calls (CI only with `ENABLE_INTEGRATION_TESTS=true`)

## Important Notes

- **Python**: 3.10+ (see `.python-version`)
- **Stock Codes**: 6-digit Korean format (e.g., "005930" for Samsung)
- **Trading Hours**: 9:00-15:30 KST (UTC+9)
- **Secrets**: `.env` file only (gitignored), loaded via `pydantic_settings.BaseSettings`
- **Thread Safety**: Use `ContextVar` for async-safe context
- **Rate Limiting**: Use shared `TokenBucket` from `cluefin_openapi._rate_limiter` for API clients

## Linting Rules (from pyproject.toml)

- Line length: 120 chars
- Target: Python 3.11+
- Ruff: `E, F, W, B, Q, I, ASYNC, T20`
- Ignored: `F401` (unused imports), `E501` (line too long)

## CI/CD

CI runs on push to `main` branch only (not on PRs).

- **Lint**: Ruff check + format
- **Test**: Unit tests across Python 3.10/3.11/3.12
- **Integration**: Only when `ENABLE_INTEGRATION_TESTS=true`
- **Coverage**: Reports to Codacy
- **Security**: pip-audit vulnerability scan

