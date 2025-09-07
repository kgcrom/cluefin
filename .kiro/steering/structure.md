# Project Structure & Organization

## Monorepo Layout
This is a **uv workspace monorepo** with clear separation between packages and applications:

```
cluefin/
├── packages/
│   └── cluefin-openapi/          # Korean financial API clients
└── apps/
    └── cluefin-cli/              # Interactive CLI application
```

## Package Structure

### cluefin-openapi (API Client Package)
```
packages/cluefin-openapi/
├── src/cluefin_openapi/
│   ├── kiwoom/                   # Kiwoom Securities API modules
│   │   ├── _client.py           # Main client class
│   │   ├── _auth.py             # Authentication handling
│   │   ├── _domestic_*.py       # Domain-specific API modules
│   │   ├── _domestic_*_types.py # Pydantic models for each domain
│   │   └── _exceptions.py       # Error handling hierarchy
│   └── krx/                     # Korea Exchange API modules
│       ├── _client.py           # KRX client implementation
│       ├── _*_types.py          # Type definitions per domain
│       └── _exceptions.py       # KRX-specific exceptions
└── tests/                       # Provider-based test organization
    ├── kiwoom/                  # Kiwoom API tests
    │   ├── test_*_unit.py       # Unit tests with requests_mock
    │   └── test_*_integration.py # Integration tests (requires API keys)
    └── krx/                     # KRX API tests
        ├── test_*_unit.py       # Unit tests
        └── test_*_integration.py # Integration tests
```

### cluefin-cli (CLI Application)
```
apps/cluefin-cli/
├── src/cluefin_cli/
│   ├── commands/                # CLI command implementations
│   │   ├── analysis/           # Technical analysis and AI modules
│   │   ├── inquiry/            # Interactive menu system modules
│   │   ├── analyze.py          # Stock analysis command
│   │   └── inquiry.py          # Interactive inquiry command
│   ├── ml/                     # ML pipeline and models
│   │   ├── predictor.py        # Main ML orchestrator
│   │   ├── models.py           # LightGBM model implementation
│   │   ├── feature_engineering.py # TA-Lib feature generation
│   │   ├── explainer.py        # SHAP explanations
│   │   └── diagnostics.py      # Model evaluation
│   ├── data/                   # Data fetching abstraction
│   ├── display/                # Rich UI components
│   ├── utils/                  # Utility functions
│   ├── config/                 # Application settings
│   └── main.py                 # CLI entry point
└── tests/unit/                 # Unit tests mirroring src structure
    ├── commands/inquiry/       # Inquiry system tests
    └── ml/                     # ML pipeline tests
```

## File Naming Conventions

### Internal Modules
- **Underscore prefix**: Internal modules use `_client.py`, `_auth.py`, `_types.py`
- **Type definitions**: Separate `_types.py` files for each domain module
- **Domain separation**: Each API domain gets its own module pair (e.g., `_domestic_stock_info.py` + `_domestic_stock_info_types.py`)

### Test Organization
- **Provider-based**: Tests organized by API provider (`kiwoom/`, `krx/`)
- **Test suffixes**: `test_<module_name>_unit.py` and `test_<module_name>_integration.py`
- **Integration markers**: Integration tests marked with `@pytest.mark.integration`
- **Realistic data**: Use actual Korean stock codes like "005930" (Samsung Electronics)

## Architecture Patterns

### API Client Design
- **Response wrapping**: All APIs return `KiwoomHttpResponse[T]` with typed headers and body
- **Type safety**: Extensive Pydantic models with Korean field aliases
- **Error hierarchy**: Comprehensive exception classes for different error types
- **Rate limiting**: Built-in configurable requests per second limiting

### CLI Command Structure
- **Click framework**: Command structure with clear argument parsing
- **Rich UI**: Beautiful terminal output with Korean market formatting
- **Async support**: Commands use `asyncio.run()` for async operations
- **Modular design**: Separate modules for different analysis types

### ML Pipeline Organization
- **Orchestrator pattern**: `StockMLPredictor` coordinates all ML components
- **Feature engineering**: Dedicated module for TA-Lib indicator generation
- **Model explainability**: SHAP integration for feature importance
- **Time series validation**: Proper temporal splitting for financial data

## Korean Market Conventions
- **Stock codes**: 6-digit format (e.g., "005930", "035720")
- **Field aliases**: Pydantic models with Korean API field mappings
- **Timezone handling**: KST awareness throughout the application
- **Currency formatting**: Korean Won (₩) with proper comma separators
- **Trading hours**: 9:00-15:30 KST consideration in ML features

## Cross-Package Dependencies
- CLI application depends on API client package via workspace reference
- Shared development dependencies defined at workspace root
- Individual package dependencies managed in respective `pyproject.toml` files