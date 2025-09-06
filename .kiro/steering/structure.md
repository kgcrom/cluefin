---
inclusion: always
---

# Project Structure & Architecture Patterns

## Workspace Structure

**uv monorepo** with two main packages:
- `packages/cluefin-openapi/` - Korean financial API client library
- `apps/cluefin-cli/` - CLI application consuming the library

## File Organization Rules

### Module Naming Patterns
- **Private modules**: Underscore prefix (`_client.py`, `_auth.py`)
- **Type definitions**: `_types.py` suffix (`_domestic_account_types.py`)
- **Domain grouping**: Related functionality together (`_domestic_account.py`, `_domestic_chart.py`)
- **Test files**: `test_` prefix (`test_auth.py`)

### Directory Structure
- API modules in domain folders: `kiwoom/`, `krx/`
- Tests split: `tests/unit/` (mocked), `tests/integration/` (real API calls)
- Keep auth, client, and types in same domain folder

## Code Conventions

### Naming Standards
- **Classes**: PascalCase (`DomesticAccount`, `KiwoomClient`)
- **Functions/Methods**: snake_case (`get_stock_data`, `calculate_rsi`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_RETRIES`, `API_BASE_URL`)
- **Client properties**: Match domain names (`client.account`, `client.chart`)

### Import Order
```python
# 1. Standard library
import asyncio
from typing import Optional

# 2. Third-party
import click
import pandas as pd
from rich.console import Console

# 3. Local - relative imports within same package
from ._client import Client
from ._auth_types import TokenResponse

# 4. Cross-package workspace imports
from cluefin_openapi.kiwoom import Client
```

## API Client Architecture

### Required Implementations
- Rate limiting and caching for all API clients
- Pydantic v2 models for all external API responses
- Exponential backoff retry logic
- Domain-specific custom exceptions (`KiwoomAuthenticationError`, `KiwoomRateLimitError`)
- Consistent method naming (`get_inquire_balance`, `get_daily_chart`)

### Error Handling Patterns
- Specific exception types with context (request details, Korean error messages)
- Distinguish retryable (network, rate limit) vs non-retryable (auth, validation) errors
- Log retry attempts with debugging context
- Respect API rate limits with proper caching

## Testing Requirements

### Test Organization
- **Unit tests**: Mock all external dependencies using `unittest.mock`
- **Integration tests**: Real API calls, require credentials
- **Test markers**: Use `@pytest.mark.integration` and `@pytest.mark.slow`
- Mock API clients in CLI application tests

### Development Workflow
```bash
# Setup
uv sync --dev

# Code quality (run before commits)
uv run ruff format .
uv run ruff check . --fix

# Testing
uv run pytest -m "not integration"              # Unit tests only
uv run pytest packages/*/tests/unit/ -v        # Verbose unit tests
```