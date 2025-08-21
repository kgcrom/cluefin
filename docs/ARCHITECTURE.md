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
│       └── tests/
│           ├── unit/             # Fast, isolated tests with mocks
│           └── integration/      # Real API tests (requires credentials)
├── apps/
│   └── cluefin-cli/              # Command-line interface application
│       ├── src/cluefin_cli/
│       │   ├── commands/         # CLI command implementations
│       │   ├── ml/              # ML pipeline and models
│       │   ├── analysis/        # Technical analysis modules
│       │   └── display/         # Rich UI components
│       └── tests/
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
├── analyze              # Quick stock analysis
├── inquiry             # Interactive menu-driven research
│   ├── stock-info      # Basic company information
│   ├── ranking-info    # Performance rankings
│   └── sector-info     # Industry analysis
└── ml                  # Machine learning commands
    ├── train           # Model training
    ├── predict         # Generate predictions
    └── explain         # SHAP-based explanations
```

## ML Pipeline Architecture

### Core Components

1. **StockPredictor** (`ml/models.py`)
   - LightGBM-based binary classification
   - Time-aware cross-validation with TimeSeriesSplit
   - Korean market trading hours consideration

2. **FeatureEngineering** (`ml/feature_engineering.py`)
   - 20+ technical indicators via TA-Lib
   - Price momentum and volatility features
   - Volume and market condition indicators

3. **ModelExplainer** (`ml/explainer.py`)
   - SHAP-based feature importance
   - Individual prediction explanations
   - Model interpretation for non-technical users

4. **Diagnostics** (`ml/diagnostics.py`)
   - Model performance evaluation
   - Precision, recall, F1-score, ROC-AUC metrics
   - Time series validation results

### Data Flow
```
Raw Market Data → Feature Engineering → ML Model → Predictions → SHAP Explanations → AI Insights
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
- Test files mirror source structure: `test_<module_name>.py`
- Integration tests marked with `@pytest.mark.integration`
- Authentication-required tests marked with `@pytest.mark.requires_auth`

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
