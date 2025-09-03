# Development Tech Stack & Tools

## Core Technology Stack

### Python Ecosystem
- **Python 3.10+**: Modern type hints and async support (workspace requirement)
- **uv**: Fast Python package installer and resolver for workspace management
- **Pydantic 2.11.7**: Data validation and serialization with type safety (pinned version)
- **Loguru 0.7.3+**: Modern logging library used across all packages

### CLI Framework & UI
- **Click 8.1.7+**: Command-line interface creation toolkit
- **Rich 13.7.0+**: Rich text and beautiful formatting in terminal
- **Inquirer 3.4.1+**: Interactive command-line user interfaces
- **Plotext 5.2.8+**: ASCII charts and plots for terminal visualization

### Machine Learning & Analysis
- **LightGBM 4.0.0+**: Gradient boosting framework for stock predictions
- **scikit-learn 1.3.0+**: Machine learning utilities, metrics, and TimeSeriesSplit
- **SHAP 0.47.2+**: Model explainability and feature importance analysis
- **TA-Lib 0.4.25+**: Technical analysis indicators (RSI, MACD, Bollinger Bands)
- **imbalanced-learn 0.14.0+**: Handling imbalanced financial datasets
- **NumPy 1.24.0+** & **Pandas 2.0.0+**: Numerical computing and data manipulation

### API & HTTP Client
- **Requests 2.32.4+**: HTTP library for API calls
- **Pydantic Settings 2.0.0+**: Environment variable and settings management

### AI Integration
- **OpenAI 1.0.0+**: GPT integration for market analysis and natural language insights

### Development & Testing Tools
- **pytest 8.4.1+**: Testing framework with async support
- **pytest-asyncio 0.25.0+**: Async test support
- **requests-mock 1.12.1+**: HTTP request mocking for unit tests
- **coverage 7.10.1+**: Code coverage measurement
- **python-dotenv 1.1.1+**: Environment variable loading
- **Ruff 0.12.3+**: Fast Python linter and formatter (replaces flake8/black)

### Build System
- **Hatchling**: Modern Python package build backend for both packages

## Project Structure & Workspace

### uv Workspace Configuration
```toml
[tool.uv.workspace]
members = [
    "packages/*",           # cluefin-openapi package
    "apps/cluefin-cli",     # Main CLI application
]
```

### Package Versions
- **cluefin-openapi**: v0.1.3 (API client package)
- **cluefin-cli**: v0.1.0 (CLI application)
- **cluefin**: v0.1.0 (workspace root)

## Essential Development Commands

### Project Setup
```bash
# Install all workspace dependencies
uv sync --dev

# Install specific package in development mode
cd packages/cluefin-openapi && uv pip install -e .
```

### Testing
```bash
# Run all tests across workspace
uv run pytest

# Run unit tests for API package
uv run pytest packages/cluefin-openapi/tests/unit/ -v

# Run integration tests (requires API keys)
uv run pytest packages/cluefin-openapi/tests/integration/ -v

# Run CLI app tests
uv run pytest apps/cluefin-cli/tests/ -v

# Run with coverage
uv run coverage run --source=packages/cluefin-openapi/src -m pytest packages/cluefin-openapi/tests/unit/
uv run coverage xml

# Run specific test file
uv run pytest packages/cluefin-openapi/tests/unit/kiwoom/test_auth.py -v
```

### Code Quality
```bash
# Lint check with Ruff
uv run ruff check .

# Format check with Ruff
uv run ruff format --check .

# Auto-fix and format (recommended workflow)
uv run ruff check . --fix
uv run ruff format .
```

### CLI Application Usage
```bash
# Interactive stock inquiry system
cluefin-cli inquiry

# Quick stock analysis
cluefin-cli analyze 005930

# AI-powered analysis with OpenAI
cluefin-cli analyze 005930 --ai-analysis

# ML prediction with SHAP explanations
cluefin-cli analyze 035720 --ml-predict --shap-analysis
```

### Machine Learning Operations
```bash
# Train ML model (example commands - actual implementation may vary)
uv run python -c "from cluefin_cli.ml.models import StockPredictor; StockPredictor().train('005930')"

# Generate predictions
uv run python -c "from cluefin_cli.ml.predictor import predict_stock; predict_stock('005930')"

# Model diagnostics
uv run python -c "from cluefin_cli.ml.diagnostics import evaluate_model; evaluate_model()"
```

## Environment Configuration

### Required Environment Variables

#### For cluefin-openapi package:
```bash
# Kiwoom Securities API credentials
KIWOOM_APP_KEY=your_app_key_here
KIWOOM_SECRET_KEY=your_secret_key_here
```

#### For cluefin-cli application:
```bash
# Kiwoom Securities API credentials
KIWOOM_APP_KEY=your_app_key_here
KIWOOM_SECRET_KEY=your_secret_key_here

# OpenAI API key for AI-powered analysis
OPENAI_API_KEY=your_openai_api_key_here
```

### Environment Setup
```bash
# Copy sample environment files
cp packages/cluefin-openapi/.env.sample packages/cluefin-openapi/.env
cp apps/cluefin-cli/.env.sample apps/cluefin-cli/.env

# Edit with your actual API keys
# vim packages/cluefin-openapi/.env
# vim apps/cluefin-cli/.env
```

## Tool Configurations

### Ruff Configuration
```toml
[tool.ruff]
line-length = 120
fix = true
target-version = "py311"

[tool.ruff.format]
docstring-code-format = true

[tool.ruff.lint]
select = ["E", "F", "W", "B", "Q", "I", "ASYNC", "T20"]
ignore = ["F401", "E501"]  # Allow unused imports, long lines
```

### Pytest Configuration
```toml
[tool.pytest.ini_options]
markers = [
    "integration: integration tests",
    "requires_auth: tests that require authentication",
    "slow: mark test as slow running",
]
addopts = "-ra"
testpaths = [
    "packages/cluefin-openapi/tests",
    "apps/cluefin-cli/tests",
]
```

## Package Management Best Practices

### Workspace Management
- **Root pyproject.toml**: Defines workspace members and shared dev dependencies
- **Package pyproject.toml**: Individual package dependencies and configuration
- **Always use `uv run`**: Never use `pip` directly - all Python commands via `uv run`

### Dependency Management
```bash
# Add production dependency to specific package
cd packages/cluefin-openapi
uv add requests

# Add development dependency to workspace root
uv add --dev pytest-cov

# Update all dependencies
uv lock --upgrade

# Sync dependencies after changes
uv sync --dev
```

## Installation & Troubleshooting

### TA-Lib Installation
```bash
# macOS with Homebrew
brew install ta-lib lightgbm
```

### OpenAI API Configuration
- Ensure `OPENAI_API_KEY` is set in `.env` file
- Verify API key has sufficient credits and permissions
- AI analysis features gracefully degrade if API unavailable

### ML Model Considerations
- Models are trained on Korean market data with KST timezone awareness
- Feature engineering accounts for Korean trading hours (9:00-15:30 KST)
- Uses TimeSeriesSplit for proper temporal validation of financial data
- Model artifacts cached in workspace for performance

## Development Workflow

### Testing Strategy
- **Unit tests**: Use `requests-mock` with realistic Korean stock codes (e.g., "005930" for Samsung Electronics)
- **Integration tests**: Require valid API credentials, marked with `@pytest.mark.integration`
- **ML tests**: Use TimeSeriesSplit for financial data temporal validation
- **Async tests**: Supported via pytest-asyncio for future async implementations

### Code Organization
- Internal modules prefixed with underscore: `_client.py`, `_auth.py`, `_types.py`
- Type definitions in dedicated `_types.py` files per module
- Test files mirror source structure: `test_<module_name>.py`
- Cross-package dependencies managed through workspace references

### Korean Financial Market Specifics
- **Timezone handling**: Korea Standard Time (KST) throughout the application
- **Trading hours**: 9:00-15:30 KST consideration in ML model features
- **Market data**: Uses actual Korean stock codes for realistic testing and development
- **API compatibility**: Designed for Korean financial service provider APIs (Kiwoom, KRX)

---

> **Note**: Always use `uv run` prefix for Python commands to ensure proper workspace dependency resolution.
