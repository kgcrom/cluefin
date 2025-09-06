---
inclusion: always
---

# Technology Stack & Development Guidelines

## Required Tools & Commands

**Package Management**: Always use `uv` for all operations
- Dependencies: `uv sync --dev` or `uv sync --directory <package>`
- Code execution: `uv run <command>` (never use bare `python` or `pip`)
- Python version: 3.10+ (enforced by `.python-version`)

**Code Quality**: Run before any commits
```bash
uv run ruff format .        # Format all code
uv run ruff check . --fix   # Lint and auto-fix issues
```

**Testing Commands**:
```bash
uv run pytest -m "not integration"             # Unit tests only (default)
uv run pytest packages/*/tests/unit/ -v        # Verbose unit tests
uv run pytest -m integration                   # Integration tests (requires auth)
```

## Mandatory Code Standards

**Formatting & Style**:
- Line length: 120 characters maximum
- Use Ruff for all formatting/linting (replaces black, isort, flake8)
- Type hints required for all public functions, methods, and class attributes
- Docstrings required for all public APIs

**Dependencies**:
- Pydantic v2: All data models and validation (never use v1 syntax)
- Rich: All terminal output formatting and tables
- Click: CLI framework with proper decorators
- pytest: Testing with proper markers (`@pytest.mark.integration`, `@pytest.mark.slow`)

## Workspace Structure Rules

**Multi-package monorepo**:
- `packages/cluefin-openapi/`: Reusable API client library
- `apps/cluefin-cli/`: CLI application consuming the library
- Never create circular dependencies between packages

**Import Patterns**:
```python
# Correct cross-package imports
from cluefin_openapi.kiwoom import Client
from cluefin_cli.commands import analyze

# Correct relative imports within same package
from ._client import KiwoomClient
from ._auth_types import TokenResponse
```

## Environment & Security

**Required Environment Variables**:
- `KIWOOM_APP_KEY`, `KIWOOM_SECRET_KEY`: Kiwoom API credentials
- `OPENAI_API_KEY`: AI analysis features
- `KRX_AUTH_KEY`: Korea Exchange API access

**Security Rules**:
- Never log API keys or sensitive credentials
- Use environment variables for all external service credentials
- Implement proper rate limiting and caching for all API clients

## Testing Requirements

**Unit Tests** (default for all new code):
- Mock all external dependencies using `unittest.mock` or `pytest-mock`
- Test files: `test_*.py` in `tests/unit/` directories
- Run with: `uv run pytest -m "not integration"`

**Integration Tests** (optional, requires credentials):
- Use `@pytest.mark.integration` and `@pytest.mark.slow` markers
- Real API calls allowed, but must handle rate limits
- Run with: `uv run pytest -m integration`

**Coverage Requirements**:
- All new public functions must have unit tests
- All new API endpoints must have integration tests
- Use descriptive test names that explain the scenario being tested