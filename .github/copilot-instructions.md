# Cluefin Project Guidelines

## Project Architecture

This is a **financial API toolkit** organized as a **uv workspace monorepo** with multiple packages:
- `packages/cluefin-openapi/`: OpenAPI clients for Kiwoom Securities and Korea Exchange (KRX)
- `packages/cluefin-langgraph/`: LangGraph-based AI agent framework (in development)

### Key Design Patterns

**Client Architecture**: Each provider has a dedicated client with modular API 

**Type Safety**: Extensive use of Pydantic models for API responses with proper Korean financial data types:
- `KiwoomHttpResponse[T]` generic wrapper for all Kiwoom responses
- Dedicated `_types.py` files for each API module (e.g., `_domestic_stock_info_types.py`)
- Field aliases for Korean API field names: `cont_yn: Literal["Y", "N"] = Field(..., alias="cont-yn")`

## Development Workflows

**Testing Structure**: 
```bash
# Run tests for specific package (must set PYTHONPATH)
cd packages/cluefin-openapi
uv run -m pytest -s tests/unit

# Or from root with explicit path
PYTHONPATH=packages/cluefin-openapi/src uv run -m pytest -s packages/cluefin-openapi/tests/unit
```

**Package Management**: Uses `uv` workspace with shared dev dependencies:
- Root `pyproject.toml` defines workspace members and shared tools (ruff, pytest)
- Individual packages have their own dependencies
- Use `uv run` for all Python commands

**Code Quality**: Configured ruff with Korean financial domain considerations:
- Line length: 120 (accommodates Korean field names)
- Ignores F401 (unused imports common with extensive type definitions)

## Korean Financial API Specifics

**Authentication Patterns**:
- Kiwoom: OAuth2-style token generation with app_key/secret_key
- KRX: Simple auth_key header authentication
- Environment separation for development vs production trading

**Mock Data**: Integration tests use `requests_mock` for Korean financial data simulation

## Critical Conventions

**File Naming**: Underscore-prefixed for internal modules (`_client.py`, `_auth.py`, `_types.py`)

**Response Handling**: Always return structured `(headers, body)` tuples:
```python
@dataclass
class KiwoomHttpResponse(Generic[T_KiwoomHttpBody]):
    headers: KiwoomHttpHeader
    body: T_KiwoomHttpBody
```

**Import Organization**: Relative imports within packages, absolute for cross-package dependencies

**Environment Variables**: Use `.env` files for API credentials (see `.env.sample` pattern in README)

When working with financial data APIs, always consider rate limiting, proper error handling for network issues, and Korean market timezone considerations (KST).
