---
inclusion: always
---

# Technology Stack & Development Guidelines

## Core Stack
- **uv**: Package manager - use for all dependency management and command execution
- **Python 3.10+**: Required version (check `.python-version`)
- **Workspace**: Multi-package structure (`packages/cluefin-openapi`, `apps/cluefin-cli`)

## Key Dependencies
- **Pydantic v2**: All API models and validation
- **Rich**: Terminal UI formatting and tables
- **Click**: CLI framework
- **Requests**: HTTP client
- **Pandas/NumPy**: Data analysis
- **pytest**: Testing with markers (`@pytest.mark.integration`, `@pytest.mark.requires_auth`)

## Development Commands

**Setup & Dependencies:**
```bash
uv sync --dev                                    # Install all dependencies
uv sync --directory packages/cluefin-openapi    # Install specific package
```

**Code Quality (always run before commits):**
```bash
uv run ruff format .        # Format code
uv run ruff check . --fix   # Lint and auto-fix
```

**Testing:**
```bash
uv run pytest                                   # All tests
uv run pytest packages/*/tests/unit/ -v        # Unit tests only
uv run pytest -m "not integration"             # Skip integration tests
```

**Running CLI:**
```bash
uv run python apps/cluefin-cli/main.py analyze 005930
```

## Code Standards
- **Line length**: 120 characters
- **Formatting**: Use Ruff (replaces black/isort/flake8)
- **Type hints**: Required for all public APIs
- **Docstrings**: Required for all public functions/classes

## Environment Variables
- `KIWOOM_APP_KEY`, `KIWOOM_SECRET_KEY`: Kiwoom API credentials
- `OPENAI_API_KEY`: AI analysis features
- `KRX_AUTH_KEY`: Korea Exchange API
- `KIWOOM_ENVIRONMENT`: dev/prod setting

## Testing Rules
- Unit tests: Mock all external dependencies
- Integration tests: Require real API credentials, use markers
- All new features must include tests
- Use `pytest-mock` for mocking in tests