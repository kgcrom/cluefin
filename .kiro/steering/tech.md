# Technology Stack

## Build System & Package Management

- **uv**: Primary package manager and build tool (Rust-based Python package manager)
- **Workspace Structure**: Multi-package monorepo using uv workspace
- **Build Backend**: Hatchling for package building

## Core Technologies

### Python Environment
- **Python Version**: >=3.10 required
- **Type System**: Pydantic v2 for data validation and serialization
- **Logging**: Loguru for structured logging

### AI & Agent Framework
- **LangGraph**: v0.6.0 for agent orchestration and workflows
- **LangChain**: >=0.3.27 for LLM integrations
- **OpenAI Integration**: Optional langchain-openai for GPT models

### HTTP & API Client
- **Requests**: HTTP client for API interactions
- **Rate Limiting**: Built-in request throttling for API compliance

## Development Tools

### Code Quality
- **Ruff**: Code formatting, linting, and import sorting (>=0.12.3)
- **Line Length**: 120 characters
- **Target Version**: Python 3.11
- **Auto-fix**: Enabled for most issues

### Testing
- **pytest**: Primary testing framework (>=8.4.1)
- **pytest-asyncio**: For async test support (>=0.25.0)
- **Coverage**: Code coverage reporting (>=7.10.1)
- **requests-mock**: HTTP request mocking for tests (>=1.12.1)

### Environment Management
- **python-dotenv**: Environment variable management (>=1.1.1)
- **Environment Files**: `.env.test` for test configuration

## Common Commands

### Development Setup
```bash
# Install all dependencies
uv sync --dev
uv sync --directory packages/cluefin-openapi

# Install specific package in development mode
uv sync --directory packages/cluefin-openapi --dev
```

### Code Quality
```bash
# Format code
uv run ruff format .

# Check linting
uv run ruff check .

# Auto-fix linting issues
uv run ruff check . --fix
```

### Testing
```bash
# Run all tests
uv run pytest

# Run specific package tests
uv run pytest packages/cluefin-openapi/tests/

# Run with coverage
uv run pytest --cov=cluefin_openapi

# Run only unit tests
uv run pytest -m "not integration"

# Run integration tests (requires API keys)
uv run pytest -m integration
```

### Package Building
```bash
# Build specific package
uv build --directory packages/cluefin-openapi
```

## CI/CD Pipeline

### GitHub Actions
- **CI Pipeline**: Automated linting, testing, building, and security scans
- **Release Pipeline**: Package publishing and deployment
- **Dependency Updates**: Automated dependency management

### Test Markers
- `integration`: Tests requiring external API access
- `requires_auth`: Tests needing authentication
- `slow`: Long-running tests

## API Integration Requirements

### Kiwoom Securities API
- APP_KEY and SECRET_KEY required
- Environment-specific endpoints (dev/prod)
- Rate limiting compliance

### KRX (Korea Exchange) API
- AUTH_KEY required for market data access
- Individual API approval needed per endpoint

## Performance Considerations

- **Request Throttling**: Automatic rate limiting for API compliance
- **Token Management**: Automatic token refresh for Kiwoom API
- **Timeout Configuration**: Configurable timeouts for large data queries
- **Caching**: Built-in response caching where appropriate