# Project Structure

## Repository Organization

Cluefin follows a **monorepo workspace structure** with two main packages under the `packages/` directory.

## Root Level Structure

```
cluefin/
├── packages/                    # Workspace packages
│   ├── cluefin-openapi/        # API client library
│   └── cluefin-langgraph/      # AI agent system
├── docs/                       # Documentation
├── .kiro/                      # Kiro IDE configuration
├── .github/                    # GitHub Actions workflows
├── pyproject.toml              # Workspace configuration
└── uv.lock                     # Dependency lock file
```

## Package Structure Conventions

### cluefin-openapi Package
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

### cluefin-langgraph Package
```
packages/cluefin-langgraph/
├── src/cluefin_langgraph/
│   └── agents/
│       └── kiwoom/
│           ├── base/          # Base agent classes and tools
│           ├── routing/       # Router agent implementation
│           └── specialized/   # Specialized domain agents
├── tests/
│   ├── unit/
│   └── integration/
└── pyproject.toml
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

### Agent Architecture (cluefin-langgraph)
- **Base layer**: Common functionality in `base/` directory
- **Routing layer**: Intent classification and agent routing
- **Specialized layer**: Domain-specific agents (account, market_data, discovery, etf)

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
2. **Agent Logic**: Add to relevant agent in `cluefin-langgraph`
3. **Tests**: Add both unit and integration tests
4. **Types**: Define Pydantic models in `_types.py` files

### Cross-Package Dependencies
- `cluefin-langgraph` depends on `cluefin-openapi`
- Use workspace dependencies in `pyproject.toml`
- Maintain clear separation of concerns between packages