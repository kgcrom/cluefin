# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Start

**Essential Commands:**
```bash
# Setup with Python 3.10
uv venv --python 3.10
source .venv/bin/activate
uv sync --all-packages

# Install system dependencies (macOS) - Required for ML features
brew install ta-lib lightgbm

# Run all tests
uv run pytest
# Unit tests only (excludes integration tests)
uv run pytest -m "not integration"
# Integration tests only (requires API keys)
uv run pytest -m "integration"
uv run ruff check . --fix

# CLI Usage
cluefin-cli inquiry
cluefin-cli analyze 005930 --chart --ai-analysis --ml-predict --shap-analysis

# Single test execution
uv run pytest packages/cluefin-openapi/tests/kiwoom/test_auth_unit.py::test_generate_token_success -v
```

**Key Info:**
- **Always use `uv run`** for Python commands (never `pip` directly)
- Type-safe Korean financial APIs with Pydantic models
- ML pipeline with LightGBM + SHAP explainability
- Interactive CLI with Rich UI and OpenAI integration
- TA-Lib system dependency required for technical analysis features

## Detailed Documentation

For comprehensive information, see these detailed guides:

### 📋 [Project Overview](docs/PROJECT_OVERVIEW.md)
- Vision, goals, and key features
- Korean market specialization
- Target users and use cases
- Current development status (Phase 2)

### 🏗️ [Architecture](docs/ARCHITECTURE.md)  
- Monorepo structure and package organization
- ML pipeline architecture with LightGBM
- API client patterns and response handling
- Korean financial API specifics

### 🛠️ [Tech Stack & Tools](docs/TECH_STACK.md)
- Complete technology stack
- Essential development commands
- Environment setup and configuration
- Troubleshooting guide

## Critical Implementation Patterns

### Workspace Architecture
This is a **uv workspace monorepo** with:
- `packages/cluefin-openapi/`: Korean financial API clients (Kiwoom Securities & KRX)
- `apps/cluefin-cli/`: Interactive CLI application with ML predictions
- Root `pyproject.toml` defines workspace members and shared dev dependencies
- Individual packages have their own `pyproject.toml` with specific dependencies

### Response Handling Pattern
Always return structured responses with Korean financial API specifics:
```python
@dataclass
class KiwoomHttpResponse(Generic[T_KiwoomHttpBody]):
    headers: KiwoomHttpHeader
    body: T_KiwoomHttpBody
```

### Korean Field Aliases
```python
# Korean API field names require aliases
cont_yn: Literal["Y", "N"] = Field(..., alias="cont-yn")
```

### File Naming Conventions
- Internal modules: `_client.py`, `_auth.py`, `_types.py`
- Type definitions: `_<module>_types.py` 
- Test files: `test_<module_name>_unit.py` for unit tests, `test_<module_name>_integration.py` for integration tests

### Testing Approach
- **Unit**: `requests_mock` with Korean stock codes (e.g., "005930")  
- **Integration**: `@pytest.mark.integration` (requires API keys)
- **ML**: TimeSeriesSplit for financial data temporal validation
- **Test Structure**: Organized by provider (`kiwoom/`, `krx/`) with `_unit.py` and `_integration.py` suffixes

### Korean Market Considerations
- **Timezone**: Korea Standard Time (KST) throughout
- **Trading Hours**: 9:00-15:30 KST in ML models  
- **Authentication**: OAuth2-style token generation for Kiwoom (app_key/secret_key), simple auth_key for KRX
- **Rate Limiting**: Built-in per Korean API requirements
- **Stock Codes**: Use Korean stock codes (e.g., "005930" for Samsung) in tests and examples

## Common Development Tasks

### Adding New API Endpoint
1. Define types in `_<module>_types.py` with Korean field aliases using Pydantic `Field(..., alias="korean-name")`
2. Implement in corresponding module with `KiwoomHttpResponse[T]` wrapper
3. Add unit tests with `requests_mock` in `test_<module>_unit.py` using Korean stock codes (e.g., "005930")
4. Add integration tests with `@pytest.mark.integration` in `test_<module>_integration.py`
5. Follow structured response handling: `(headers, body)` tuple pattern

### ML Model Development
1. Feature engineering in `apps/cluefin-cli/src/cluefin_cli/ml/feature_engineering.py` with TA-Lib integration
2. Model training in `ml/models.py` with TimeSeriesSplit for temporal validation
3. SHAP explanations in `ml/explainer.py` using TreeExplainer
4. Performance evaluation in `ml/diagnostics.py`
5. Integration with CLI commands in `commands/analyze.py`

### Adding New CLI Commands
1. Create command module in `apps/cluefin-cli/src/cluefin_cli/commands/`
2. Use Click decorators with Rich Console for UI consistency
3. Integrate with data fetcher: `from cluefin_cli.data.fetcher import DataFetcher`
4. Add unit tests in `apps/cluefin-cli/tests/unit/commands/`
5. Update main CLI entry point in `apps/cluefin-cli/src/cluefin_cli/main.py`

### Environment Variables
```bash
# Required for full functionality
KIWOOM_APP_KEY=your_key
KIWOOM_SECRET_KEY=your_secret
OPENAI_API_KEY=your_openai_key
KRX_AUTH_KEY=your_auth_key_here

# Optional ML configuration
ML_MODEL_PATH=models/
ML_CACHE_DIR=.ml_cache/

# Environment setup location: workspace root (.env file)
cp apps/cluefin-cli/.env.sample .env
```

## Critical Architecture Notes

### ML Pipeline Architecture
- **StockMLPredictor**: Main pipeline class integrating all ML components
- **150+ Technical Indicators**: Generated via TA-Lib in FeatureEngineer
- **SHAP Integration**: TreeExplainer provides feature importance and explanations
- **Korean Market Specifics**: Trading hours (9:00-15:30 KST) embedded in features

### Test Structure Organization
Recent reorganization moved tests from `unit/` and `integration/` subdirectories to provider-based organization:
```
packages/cluefin-openapi/tests/
├── kiwoom/
│   ├── test_auth_unit.py
│   ├── test_auth_integration.py
│   ├── test_domestic_stock_info_unit.py
│   └── test_domestic_stock_info_integration.py
└── krx/
    ├── test_stock_unit.py
    └── test_stock_integration.py
```

---

*For detailed technical documentation, consult the `docs/` directory including ARCHITECTURE.md and TECH_STACK.md.*
