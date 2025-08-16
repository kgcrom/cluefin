# Project Structure

## Repository Organization

Cluefin follows a **monorepo workspace structure** with packages under `packages/` and applications under `apps/`.

## Root Level Structure

```
cluefin/
├── packages/                    # Reusable library packages
│   └── cluefin-openapi/        # Korean financial API clients
├── apps/                       # Application packages
│   └── cluefin-cli/           # Command-line interface
├── docs/                       # Documentation
├── .kiro/                      # Kiro IDE configuration
├── .github/                    # GitHub Actions workflows
├── pyproject.toml              # Workspace configuration
└── uv.lock                     # Dependency lock file
```

## Package Structure Conventions

### cluefin-openapi Package (Library)
```
packages/cluefin-openapi/
├── src/cluefin_openapi/
│   ├── kiwoom/                 # Kiwoom Securities API client
│   │   ├── _auth.py           # Authentication handling
│   │   ├── _client.py         # Main client class
│   │   ├── _domestic_*.py     # Domain-specific modules
│   │   └── _*_types.py        # Pydantic type definitions
│   └── krx/                   # Korea Exchange API client
│       ├── _client.py         # KRX client class
│       ├── _*.py              # Feature modules
│       └── _*_types.py        # Type definitions
├── tests/
│   ├── unit/                  # Unit tests
│   └── integration/           # Integration tests
└── pyproject.toml
```

### cluefin-cli Application
```
apps/cluefin-cli/
├── src/cluefin_cli/
│   ├── commands/              # CLI command implementations
│   ├── analysis/              # Technical indicators & AI analysis
│   ├── data/                  # Data fetching and processing
│   ├── display/               # Terminal charts and formatting
│   ├── config/                # Configuration management
│   └── main.py               # CLI entry point
├── main.py                   # Application entry point
├── tests/                    # Application tests
└── pyproject.toml           # App-specific dependencies
```

## Naming Conventions

### File Naming
- **Private modules**: Prefix with underscore (`_client.py`, `_auth.py`)
- **Type definitions**: Suffix with `_types.py` (`_domestic_account_types.py`)
- **Test files**: Prefix with `test_` (`test_client.py`)

### Module Organization
- **Domain separation**: Each API domain gets its own module (account, chart, etf, etc.)
- **Client pattern**: Each package has a main `_client.py` as the entry point
- **Type safety**: Separate `_types.py` files for Pydantic models

## Configuration Files

### Workspace Level
- `pyproject.toml`: Workspace configuration, shared tools (ruff, pytest)
- `uv.lock`: Locked dependencies for reproducible builds
- `.env.test`: Test environment variables

### Package Level
- `pyproject.toml`: Package-specific dependencies and metadata
- `README.md`: Package documentation
- `.coverage`: Coverage reports

## Test Organization

### Test Structure
```
tests/
├── unit/                      # Fast, isolated tests
│   ├── kiwoom/               # Kiwoom-specific unit tests
│   └── krx/                  # KRX-specific unit tests
└── integration/              # Tests requiring external APIs
    ├── kiwoom/               # Kiwoom integration tests
    └── krx/                  # KRX integration tests
```

### Test Markers
- `@pytest.mark.integration`: Requires external API access
- `@pytest.mark.requires_auth`: Needs authentication credentials
- `@pytest.mark.slow`: Long-running tests

## Import Patterns

### Internal Imports
```python
# Within same package
from ._client import Client
from ._auth_types import TokenResponse

# Cross-package imports
from cluefin_openapi.kiwoom import Client
```

### External Dependencies
```python
# Standard pattern for external libs
from loguru import logger
from pydantic import BaseModel, SecretStr
```

## Documentation Structure

### Package Documentation
- Each package has comprehensive README.md
- API examples and usage patterns
- Environment setup instructions

### Code Documentation
- Docstrings for all public classes and methods
- Type hints for all function parameters and returns
- Inline comments for complex business logic

## Development Workflow

### Adding New Features
1. **API Client**: Add to appropriate domain module in `cluefin-openapi`
2. **CLI Commands**: Add to `apps/cluefin-cli/src/cluefin_cli/commands/`
3. **Analysis Features**: Add to `apps/cluefin-cli/src/cluefin_cli/analysis/`
4. **Tests**: Add both unit and integration tests
5. **Types**: Define Pydantic models in `_types.py` files

### Package Types
- **Libraries** (`packages/`): Reusable components, follow private module conventions
- **Applications** (`apps/`): End-user applications, can use public module naming

### Cross-Package Dependencies
- Use workspace dependencies in `pyproject.toml`
- Apps can depend on packages, but packages should not depend on apps
- Maintain clear separation of concerns between packages and applications