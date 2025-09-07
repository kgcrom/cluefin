# Technology Stack & Development

## Build System & Package Management
- **uv workspace**: Modern Python package manager with workspace support
- **Python 3.10+**: Required minimum version for modern type hints
- **Hatchling**: Build backend for both packages and applications

## Core Dependencies
- **Pydantic 2.11.7**: Data validation with Korean field aliases (pinned version)
- **Click 8.1.7+**: CLI framework for command structure
- **Rich 13.7.0+**: Terminal UI with Korean market formatting
- **Requests 2.32.4+**: HTTP client for Korean financial APIs
- **Loguru 0.7.3+**: Modern logging across all modules

## ML & Analysis Stack
- **LightGBM 4.0.0+**: Gradient boosting for stock predictions
- **scikit-learn 1.3.0+**: ML utilities with TimeSeriesSplit for financial data
- **SHAP 0.47.2+**: Model explainability and feature importance
- **TA-Lib 0.4.25+**: Technical analysis indicators
- **OpenAI 1.0.0+**: GPT-4 integration for market insights

## Development Tools
- **Ruff 0.12.3+**: Fast linting and formatting (replaces black/flake8)
- **pytest 8.4.1+**: Testing framework with async support
- **requests-mock 1.12.1+**: HTTP mocking for unit tests
- **coverage 7.10.1+**: Code coverage measurement

## Common Commands

### Project Setup
```bash
# Install all workspace dependencies
uv sync --all-packages

# Install system dependencies (macOS)
brew install ta-lib lightgbm
```

### Development Workflow
```bash
# Run all tests (unit only, excludes integration)
uv run pytest -m "not integration"

# Run integration tests (requires API keys)
uv run pytest -m "integration"

# Code quality checks and fixes
uv run ruff check . --fix
uv run ruff format .

# Coverage reporting
uv run coverage run --source=packages/cluefin-openapi/src -m pytest -m "not integration"
uv run coverage xml
```

### CLI Usage
```bash
# Interactive stock inquiry
cluefin-cli inquiry

# Stock analysis with AI and ML
cluefin-cli analyze 005930 --ai-analysis --ml-predict --shap-analysis
```

## Environment Configuration
Required environment variables:
- `KIWOOM_APP_KEY`: Kiwoom Securities API key
- `KIWOOM_SECRET_KEY`: Kiwoom Securities secret key  
- `OPENAI_API_KEY`: OpenAI API key for AI analysis
- `KRX_AUTH_KEY`: Korea Exchange API key

## Korean Market Specifics
- **Timezone**: Korea Standard Time (KST) handling throughout
- **Trading Hours**: 9:00-15:30 KST consideration in ML models
- **Stock Codes**: 6-digit Korean stock codes (e.g., "005930" for Samsung)
- **Currency**: Korean Won (₩) formatting with comma separators