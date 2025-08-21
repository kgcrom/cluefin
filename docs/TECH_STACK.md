# Development Tech Stack & Tools

## Core Technology Stack

### Python Ecosystem
- **Python 3.10+**: Modern type hints and async support
- **uv**: Fast Python package installer and resolver for workspace management
- **Pydantic 2.11+**: Data validation and serialization with type safety

### CLI Framework
- **Click 8.1+**: Command-line interface creation
- **Rich 13.7+**: Rich text and beautiful formatting in terminal
- **Inquirer**: Interactive command-line user interfaces
- **Plotext**: ASCII charts for terminal visualization

### Machine Learning & Analysis
- **LightGBM 4.0+**: Gradient boosting framework for predictions
- **scikit-learn 1.3+**: Machine learning utilities and metrics
- **SHAP 0.47+**: Model explainability and feature importance
- **TA-Lib 0.4+**: Technical analysis indicators
- **imbalanced-learn**: Handling imbalanced datasets
- **NumPy & Pandas**: Numerical computing and data manipulation

### AI Integration
- **OpenAI 1.0+**: GPT-4 integration for market analysis
- **Pydantic Settings**: Environment variable management

### Development Tools
- **uv workspace**: Monorepo package management
- **Ruff**: Fast Python linter and formatter
- **pytest**: Testing framework with async support
- **Coverage**: Code coverage measurement
- **requests-mock**: HTTP request mocking for tests

## Essential Commands

### Development Setup
```bash
# Install all dependencies
uv sync --dev

# Install specific package in editable mode
uv pip install -e packages/cluefin-openapi
```

### Testing
```bash
# Run all tests
uv run pytest

# Run unit tests for cluefin-openapi
uv run pytest packages/cluefin-openapi/tests/unit/ -v

# Run integration tests (requires API keys)
uv run pytest packages/cluefin-openapi/tests/integration/ -v

# Run tests with coverage
uv run coverage run --source=packages/cluefin-openapi/src -m pytest packages/cluefin-openapi/tests/unit/
uv run coverage xml

# Run single test file
uv run pytest packages/cluefin-openapi/tests/unit/kiwoom/test_auth.py -v

# Run tests for specific package from root
PYTHONPATH=packages/cluefin-openapi/src uv run -m pytest -s packages/cluefin-openapi/tests/unit
```

### Code Quality
```bash
# Run linting check
uv run ruff check .

# Run formatting check  
uv run ruff format --check .

# Auto-fix linting issues and format code
uv run ruff check . --fix
uv run ruff format .
```

### CLI Usage
```bash
# Basic stock analysis
cluefin-cli analyze <stock_code>

# Interactive inquiry system
cluefin-cli inquiry

# AI-powered analysis
cluefin-cli analyze <stock_code> --ai-analysis
```

### ML Model Operations
```bash
# Train ML model on historical data
uv run python -m cluefin_cli.ml.models --train --symbol 005930

# Generate predictions with explanations
uv run python -m cluefin_cli.ml.predictor --predict --symbol 005930 --explain

# Run model diagnostics
uv run python -m cluefin_cli.ml.diagnostics --evaluate --model-path models/stock_predictor.pkl
```

## Environment Configuration

### Required Environment Variables
```bash
# Copy sample environment files
cp packages/cluefin-openapi/.env.sample packages/cluefin-openapi/.env
cp apps/cluefin-cli/.env.sample apps/cluefin-cli/.env
```

### API Access
```bash
# Kiwoom Securities API
KIWOOM_APP_KEY=your_app_key
KIWOOM_SECRET_KEY=your_secret_key

# OpenAI for AI analysis
OPENAI_API_KEY=your_openai_api_key
```

### ML Configuration
```bash
# Optional ML settings
ML_MODEL_PATH=path/to/saved/models
ML_CACHE_DIR=path/to/ml/cache
```

## Tool Configuration

### Ruff Configuration
```toml
[tool.ruff]
line-length = 120
fix = true
target-version = "py311"

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
testpaths = [
    "packages/cluefin-openapi/tests",
    "apps/cluefin-cli/tests",
]
```

## Package Management

### Workspace Structure
- **Root pyproject.toml**: Defines workspace members and shared dev dependencies
- **Package pyproject.toml**: Individual package dependencies and configuration
- **Always use `uv run`**: Never use `pip` directly, all Python commands via `uv run`

### Dependency Management
```bash
# Add production dependency to specific package
cd packages/cluefin-openapi
uv add requests

# Add development dependency to workspace
uv add --dev pytest coverage

# Update all dependencies
uv lock --upgrade
```

## Troubleshooting

### TA-Lib Installation
```bash
# macOS with Homebrew
brew install ta-lib
uv run pip install TA-Lib

# Ubuntu/Debian
sudo apt-get install libta-lib0-dev
uv run pip install TA-Lib

# Windows (requires Visual Studio Build Tools)
# Download wheel from https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
uv run pip install TA_Lib‑0.4.xx‑cpxx‑cpxxm‑win_amd64.whl
```

### OpenAI API Issues
- Ensure `OPENAI_API_KEY` is set in environment or `.env` file
- Verify API key has sufficient credits and permissions
- AI analysis features gracefully degrade if API unavailable

### ML Model Performance
- Models trained on Korean market data (KST timezone)
- Feature engineering accounts for Korean trading hours (9:00-15:30 KST)
- Use TimeSeriesSplit for proper temporal validation
- Model cache stored in `ML_CACHE_DIR` or default `.ml_cache/`

## Development Workflow

### Package Management Best Practices
- All Python commands prefixed with `uv run`
- Dependencies managed at workspace level with package-specific configurations
- Use relative imports within packages, absolute for cross-package dependencies

### Testing Strategy
- Unit tests use `requests_mock` for API mocking with realistic Korean financial data
- Integration tests require valid API credentials and use `@pytest.mark.integration`
- ML tests use TimeSeriesSplit for financial data temporal validation
- Mock data uses actual Korean stock codes (e.g., "005930" for Samsung Electronics)
