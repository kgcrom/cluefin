# Project Structure & Organization

## Workspace Layout

This is a **uv workspace** with a monorepo structure containing multiple packages and applications:

```
cluefin/
├── packages/           # Reusable library packages
│   └── cluefin-openapi/   # Korean financial API client library
└── apps/              # Standalone applications
    └── cluefin-cli/       # Command-line interface application
```

## Package Structure: cluefin-openapi

**Location**: `packages/cluefin-openapi/`
**Purpose**: Python client library for Korean financial APIs

```
packages/cluefin-openapi/
├── src/cluefin_openapi/
│   ├── kiwoom/           # Kiwoom Securities API client
│   │   ├── _auth.py         # Authentication handling
│   │   ├── _client.py       # Main client with rate limiting & caching
│   │   ├── _domestic_*.py   # Domain-specific API modules
│   │   ├── _exceptions.py   # Custom exception classes
│   │   └── _*_types.py      # Pydantic data models
│   └── krx/              # Korea Exchange API client
│       ├── _client.py       # KRX client implementation
│       ├── _*.py           # Market-specific modules (stock, bond, etc.)
│       └── _*_types.py      # KRX data models
└── tests/
    ├── unit/             # Unit tests with mocking
    └── integration/      # Integration tests (require API keys)
```

## Application Structure: cluefin-cli

**Location**: `apps/cluefin-cli/`
**Purpose**: Command-line interface for stock analysis

```
apps/cluefin-cli/
├── src/cluefin_cli/
│   ├── commands/         # CLI command implementations
│   │   ├── analyze.py       # Stock analysis command
│   │   └── inquiry/         # Interactive inquiry system
│   ├── analysis/         # Technical analysis & AI
│   │   ├── indicators.py    # Technical indicators (RSI, MACD, etc.)
│   │   └── ai_analyzer.py   # OpenAI integration
│   ├── data/             # Data fetching and processing
│   ├── display/          # Terminal UI and charts
│   ├── config/           # Configuration management
│   └── utils/            # Utility functions
├── main.py              # CLI entry point
└── tests/
    └── unit/            # Unit tests for CLI components
```

## Naming Conventions

### Files & Modules
- **Private modules**: Prefix with underscore (`_client.py`, `_auth.py`)
- **Type definitions**: Suffix with `_types.py` (`_auth_types.py`)
- **Test files**: Prefix with `test_` (`test_auth.py`)

### Classes & Functions
- **Classes**: PascalCase (`DomesticAccount`, `TechnicalAnalyzer`)
- **Functions/Methods**: snake_case (`get_stock_data`, `calculate_rsi`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_RETRIES`, `DEFAULT_TIMEOUT`)

### API & Domain Patterns
- **API modules**: Group by domain (`_domestic_account.py`, `_domestic_chart.py`)
- **Client properties**: Match domain names (`client.account`, `client.chart`)
- **Method names**: Descriptive and consistent (`get_inquire_balance`, `get_daily_chart`)

## Configuration Files

### Root Level
- **pyproject.toml**: Workspace configuration, shared tools (ruff, pytest)
- **uv.lock**: Dependency lock file
- **.python-version**: Python version specification (3.10)

### Package Level
- **pyproject.toml**: Package-specific dependencies and metadata
- **.env**: Environment variables (not committed)
- **.env.sample**: Environment variable template

## Testing Structure

### Test Organization
- **Unit tests**: `tests/unit/` - Fast, isolated tests with mocking
- **Integration tests**: `tests/integration/` - Real API calls (require credentials)

### Test Markers
- `@pytest.mark.integration`: Integration tests
- `@pytest.mark.requires_auth`: Tests requiring API authentication
- `@pytest.mark.slow`: Long-running tests

### Mock Patterns
- Use `unittest.mock` for external dependencies
- Mock API clients in CLI tests
- Use `requests_mock` for HTTP interactions

## Import Patterns

### Internal Imports
```python
# Within same package
from ._client import Client
from ._auth_types import TokenResponse

# Cross-package (workspace)
from cluefin_openapi.kiwoom import Client
```

### External Dependencies
```python
# Standard library
import asyncio
from typing import Optional

# Third-party
import click
import pandas as pd
from rich.console import Console
```

## Error Handling Patterns

### Custom Exceptions
- Inherit from base exception classes
- Include context information (request details, status codes)
- Use specific exception types (`KiwoomAuthenticationError`, `KiwoomRateLimitError`)

### Retry Logic
- Implement exponential backoff
- Distinguish between retryable and non-retryable errors
- Log retry attempts for debugging