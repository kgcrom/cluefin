# Technology Stack & Build System

## Package Management & Build System

- **uv**: Primary package manager (Rust-based Python package manager)
- **Workspace Structure**: Multi-package workspace with `packages/` and `apps/` directories
- **Python Version**: 3.10+ (specified in `.python-version`)

## Core Technologies

### Backend & APIs
- **Python 3.10+**: Core language
- **Pydantic**: Data validation and serialization (v2.11.7)
- **Requests**: HTTP client for API interactions
- **Loguru**: Structured logging

### CLI & User Interface
- **Click**: Command-line interface framework
- **Rich**: Terminal formatting and tables
- **Inquirer**: Interactive CLI prompts
- **Plotext**: Terminal-based charts and visualizations

### Data & Analysis
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **OpenAI**: AI-powered market analysis integration

### Development Tools
- **Ruff**: Code formatting and linting (replaces black, isort, flake8)
- **pytest**: Testing framework with asyncio support
- **pytest-mock**: Mocking for tests
- **Coverage**: Code coverage reporting

## Common Commands

### Development Setup
```bash
# Install all dependencies
uv sync --dev
uv sync --directory packages/cluefin-openapi

# Install specific workspace member
uv sync --directory apps/cluefin-cli
```

### Code Quality
```bash
# Format code
uv run ruff format .

# Lint code
uv run ruff check .
uv run ruff check . --fix

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=cluefin_openapi --cov-report=html
```

### Running Applications
```bash
# Run CLI tool
uv run python apps/cluefin-cli/main.py analyze 005930

# Run with specific options
uv run python apps/cluefin-cli/main.py analyze 005930 --chart --ai-analysis
```

### Testing
```bash
# Run all tests
uv run pytest

# Run unit tests only
uv run pytest packages/cluefin-openapi/tests/unit/ -v
uv run pytest apps/cluefin-cli/tests/unit/ -v

# Run integration tests (requires API keys)
uv run pytest packages/cluefin-openapi/tests/integration/ -v

# Run with markers
uv run pytest -m "not integration"
uv run pytest -m "requires_auth"
```

## Configuration

### Environment Variables
- **KIWOOM_APP_KEY**: Kiwoom Securities API key
- **KIWOOM_SECRET_KEY**: Kiwoom Securities secret key
- **KIWOOM_ENVIRONMENT**: dev/prod environment setting
- **OPENAI_API_KEY**: OpenAI API key for AI analysis
- **KRX_AUTH_KEY**: Korea Exchange API authentication key

### Ruff Configuration
- Line length: 120 characters
- Target version: Python 3.11
- Auto-fix enabled
- Specific rule selections for Korean financial domain