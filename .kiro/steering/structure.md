---
inclusion: always
---

# Project Structure & Architecture Patterns

## Workspace Organization

**uv workspace** with monorepo structure:
- `packages/cluefin-openapi/` - Reusable Korean financial API client library
- `apps/cluefin-cli/` - Command-line interface application

## Architecture Rules

### Module Organization
- **Private modules**: Prefix with underscore (`_client.py`, `_auth.py`)
- **Type definitions**: Suffix with `_types.py` (`_auth_types.py`)
- **Domain grouping**: Group related functionality (`_domestic_account.py`, `_domestic_chart.py`)
- **Client structure**: Match domain names as properties (`client.account`, `client.chart`)

### API Client Patterns
- All API clients must implement rate limiting and caching
- Use Pydantic models for all external API responses
- Implement proper retry logic with exponential backoff
- Custom exceptions with context (`KiwoomAuthenticationError`, `KiwoomRateLimitError`)
- Method naming: Descriptive and consistent (`get_inquire_balance`, `get_daily_chart`)

## Code Style & Naming

### Naming Conventions
- **Classes**: PascalCase (`DomesticAccount`, `TechnicalAnalyzer`)
- **Functions/Methods**: snake_case (`get_stock_data`, `calculate_rsi`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_RETRIES`, `DEFAULT_TIMEOUT`)
- **Test files**: Prefix with `test_` (`test_auth.py`)

### File Organization Rules
- Place new API modules in appropriate domain folders (`kiwoom/`, `krx/`)
- Use `_types.py` suffix for Pydantic model definitions
- Keep related functionality together (auth, client, types in same domain)

## Testing Requirements

### Test Structure
- **Unit tests**: `tests/unit/` with mocking for external dependencies
- **Integration tests**: `tests/integration/` for real API calls (require credentials)
- Use `@pytest.mark.integration` and `@pytest.mark.requires_auth` markers
- Mock API clients in CLI tests using `unittest.mock`

## Import & Dependency Patterns

### Import Rules
```python
# Within same package - use relative imports
from ._client import Client
from ._auth_types import TokenResponse

# Cross-package workspace imports
from cluefin_openapi.kiwoom import Client

# Standard library first, then third-party, then local
import asyncio
from typing import Optional
import click
import pandas as pd
from rich.console import Console
```

## Error Handling Requirements

### Exception Patterns
- Create specific exception types for different error conditions
- Include context information (request details, status codes, Korean error messages)
- Inherit from appropriate base exception classes
- Use descriptive names: `KiwoomAuthenticationError`, `KiwoomRateLimitError`

### Retry & Resilience
- Implement exponential backoff for retryable errors
- Distinguish between retryable (network, rate limit) and non-retryable (auth, validation) errors
- Log retry attempts with context for debugging
- Respect API rate limits and implement proper caching

## Development Commands

```bash
# Setup and dependencies
uv sync --dev
uv sync --directory packages/cluefin-openapi
uv sync --directory apps/cluefin-cli

# Code quality
uv run ruff format .
uv run ruff check . --fix

# Testing
uv run pytest                                    # All tests
uv run pytest packages/cluefin-openapi/tests/unit/ -v    # Unit tests only
uv run pytest -m "not integration"              # Skip integration tests
```