# Technical Architecture & Structure

## Monorepo Structure

The project uses a **uv workspace monorepo** with the following organization:

```
cluefin/
├── packages/
│   └── cluefin-openapi/          # Korean financial API clients
│       ├── src/cluefin_openapi/
│       │   ├── kiwoom/           # Kiwoom Securities client modules
│       │   └── krx/              # Korea Exchange client modules
│       └── tests/                # Provider-based test organization
│           ├── kiwoom/           # Kiwoom API tests (unit & integration)
│           └── krx/              # KRX API tests (unit & integration)
├── apps/
│   └── cluefin-cli/              # Command-line interface application
│       ├── src/cluefin_cli/
│       │   ├── commands/         # CLI command implementations
│       │   │   ├── analysis/     # Technical analysis and AI modules
│       │   │   └── inquiry/      # Interactive menu system modules
│       │   ├── ml/              # ML pipeline and models
│       │   ├── data/            # Data fetching abstraction
│       │   ├── display/         # Rich UI components
│       │   ├── utils/           # Utility functions
│       │   └── config/          # Application settings
│       └── tests/unit/          # Unit tests mirroring src structure
└── docs/                        # Documentation
```

## Package Architecture

### cluefin-openapi Package
**Purpose**: Type-safe OpenAPI clients for Korean financial services

**Key Design Patterns**:
- **Modular Clients**: Each provider (Kiwoom, KRX) has dedicated client with domain modules
- **Type Safety**: Extensive Pydantic models with Korean-English field aliases
- **Response Wrapping**: All APIs return `KiwoomHttpResponse[T]` with typed headers and body
- **Rate Limiting**: Built-in configurable requests per second limiting
- **Error Handling**: Comprehensive exception hierarchy for different API error types

**Module Structure**:
```python
# Example: Kiwoom domestic stock module
kiwoom/
├── _client.py              # Main client class
├── _auth.py               # Authentication handling
├── _domestic_stock_info.py # Stock information APIs
├── _domestic_stock_info_types.py # Pydantic models
└── _exceptions.py         # Error handling
```

### cluefin-cli Application
**Purpose**: Interactive command-line interface with AI and ML capabilities

**Architecture Components**:
- **Click Framework**: Command structure and argument parsing
- **Rich UI**: Beautiful terminal output with tables, panels, and progress bars
- **Interactive Inquiry**: Menu-driven stock research system
- **ML Pipeline**: LightGBM models with feature engineering
- **AI Integration**: OpenAI GPT-4 for market analysis

**Command Structure**:
```bash
cluefin-cli
├── analyze              # Stock analysis with multiple options
│   ├── --chart         # Terminal ASCII charts
│   ├── --ai-analysis   # GPT-4 powered insights
│   ├── --ml-predict    # ML-based price predictions
│   ├── --feature-importance  # Basic feature importance
│   └── --shap-analysis # Detailed SHAP explanations
└── inquiry             # Interactive menu-driven research
    ├── stock-info      # Basic company information
    ├── ranking-info    # Performance rankings
    └── sector-info     # Industry analysis
```

## ML Pipeline Architecture

### Core Components

1. **StockMLPredictor** (`ml/predictor.py`)
   - Main orchestrator class integrating all ML components
   - End-to-end prediction pipeline with SHAP explanations
   - Korean market-specific configuration and optimization

2. **StockPredictor** (`ml/models.py`)
   - LightGBM-based binary classification for next-day price movement
   - Time-aware cross-validation with TimeSeriesSplit
   - Korean market trading hours consideration (9:00-15:30 KST)

3. **FeatureEngineer** (`ml/feature_engineering.py`)
   - 150+ technical indicators via TA-Lib integration
   - Price momentum, volatility, and trend features
   - Volume-based and market condition indicators
   - Lag features for temporal patterns

4. **SHAPExplainer** (`ml/explainer.py`)
   - SHAP TreeExplainer for feature importance
   - Individual prediction explanations with directional impact
   - Global feature rankings and model interpretation

5. **ModelDiagnostics** (`ml/diagnostics.py`)
   - Comprehensive model performance evaluation
   - Accuracy, precision, recall, F1-score, AUC metrics
   - Time series validation with proper temporal ordering

### ML Pipeline Data Flow
```
Korean Stock Data (OHLCV) → FeatureEngineer (150+ TA-Lib indicators) → 
StockPredictor (LightGBM) → SHAPExplainer (Feature Importance) → 
StockMLPredictor (Orchestration) → Rich UI Display
```

### Integration with CLI Commands
The ML pipeline integrates with the CLI through the analyze command:
```python
# apps/cluefin-cli/src/cluefin_cli/commands/analyze.py
if ml_predict:
    predictor = StockMLPredictor()
    result = predictor.analyze(stock_data)
    # Display predictions with SHAP explanations
```

## API Client Architecture

### Authentication Patterns
- **Kiwoom**: OAuth2-style token generation with app_key/secret_key
- **KRX**: Simple auth_key header authentication  
- **Environment Separation**: Development vs production trading environments

### Response Structure
All API responses follow a consistent pattern:
```python
@dataclass
class KiwoomHttpResponse(Generic[T_KiwoomHttpBody]):
    headers: KiwoomHttpHeader
    body: T_KiwoomHttpBody
```

### Error Handling Hierarchy
```python
KiwoomException
├── KiwoomAuthError       # Authentication failures
├── KiwoomRateLimitError  # Rate limiting violations
├── KiwoomAPIError        # API-specific errors
└── KiwoomNetworkError    # Network connectivity issues
```

## File Naming Conventions

### Internal Modules
- Underscore prefix for internal modules: `_client.py`, `_auth.py`, `_types.py`
- Type definitions in dedicated `_types.py` files per module
- Separate unit and integration test directories

### Test Structure
**Current Organization** (Provider-based):
```
packages/cluefin-openapi/tests/
├── kiwoom/
│   ├── test_auth_unit.py                    # Unit tests for authentication
│   ├── test_auth_integration.py             # Integration tests for authentication
│   ├── test_domestic_stock_info_unit.py     # Unit tests for stock info
│   ├── test_domestic_stock_info_integration.py # Integration tests for stock info
│   └── ... (other kiwoom modules)
└── krx/
    ├── test_stock_unit.py                   # Unit tests for KRX stock data
    ├── test_stock_integration.py            # Integration tests for KRX stock data
    └── ... (other krx modules)

apps/cluefin-cli/tests/unit/
├── commands/inquiry/                        # Inquiry command tests
├── ml/                                      # ML pipeline tests
└── ... (mirroring src structure)
```

**Test Naming Convention**:
- Unit tests: `test_<module_name>_unit.py`
- Integration tests: `test_<module_name>_integration.py`
- Integration tests marked with `@pytest.mark.integration`

## Korean Financial API Specifics

### Data Types & Validation
- Field aliases for Korean APIs: `cont_yn: Literal["Y", "N"] = Field(..., alias="cont-yn")`
- Response fields use Literal types for Y/N flags
- Korean stock codes validation (6-digit format)

### Market Considerations
- **Timezone**: Korea Standard Time (KST) handling throughout
- **Trading Hours**: 9:00-15:30 KST consideration in ML models
- **Market Holidays**: Korean market calendar awareness
- **Currency**: KRW formatting and calculations

### Rate Limiting
- Automatic rate limiting per Korean API requirements
- Configurable requests per second
- Graceful handling of quota exceeded responses

## CLI Inquiry System Architecture

### Interactive Menu System
The inquiry command provides a sophisticated menu-driven interface:

**Core Modules** (`apps/cluefin-cli/src/cluefin_cli/commands/inquiry/`):
- `main.py` - Main inquiry command logic and orchestration
- `menu_controller.py` - Interactive menu navigation and state management
- `display_formatter.py` - Rich-based display formatting for Korean financial data
- `parameter_collector.py` - User input collection with validation
- `config_models.py` - Pydantic configuration models for menu settings

**Domain-Specific Modules**:
- `stock_info.py` - Individual stock information and detailed analysis
- `ranking_info.py` - Stock rankings and performance comparisons
- `sector_info.py` - Sector-based analysis and industry groupings
- `base_api_module.py` - Base class for API integration patterns

### Data Integration
The CLI integrates with both API packages:
```python
# Data fetching abstraction
from cluefin_cli.data.fetcher import DataFetcher

# Integrates with:
# - cluefin-openapi.kiwoom for real-time data
# - cluefin-openapi.krx for market data
# - OpenAI for AI-powered analysis
```

### Display Architecture
**Rich UI Components**:
- Korean Won currency formatting with proper locale
- Color-coded tables for market data (red/green for price changes)
- Progress bars for data loading operations
- Panels and sections for organized information display
- ASCII charts via plotext for terminal visualization

**Korean Market UI Considerations**:
- Right-to-left number alignment for price data
- Korean company name display alongside stock codes
- KST timezone display for market hours
- Won currency symbol (₩) with comma separators
