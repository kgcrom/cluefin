# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Start

**Essential Commands:**
```bash
# Setup
uv sync --dev

# Test & Quality
uv run pytest
uv run ruff check . --fix
uv run ruff format .

# CLI Usage
cluefin-cli analyze 005930 --chart --ai-analysis --ml-predict --shap-analysis
cluefin-cli inquiry
```

**Key Info:**
- **Always use `uv run`** for Python commands (never `pip` directly)
- CLI tool for Korean stock market analysis with ML predictions
- Rich-based interactive terminal UI with SHAP explainability
- Dependencies on TA-Lib (requires system installation) and cluefin-openapi

## Architecture Overview

### Command Structure
The CLI is built with Click and uses a two-command architecture:

1. **`analyze`** - Stock analysis with technical indicators, AI insights, and ML predictions
2. **`inquiry`** - Interactive menu-driven market exploration

### Core Components

**ML Pipeline** (`src/cluefin_cli/ml/`):
- `StockMLPredictor` - Main pipeline integrating feature engineering, LightGBM training, and SHAP explanations
- `FeatureEngineer` - TA-Lib-based technical indicator generation (150+ features)
- `StockPredictor` - LightGBM classifier with TimeSeriesSplit for temporal validation
- `SHAPExplainer` - Model interpretability with TreeExplainer

**Commands Architecture** (`src/cluefin_cli/commands/`):
- `analyze.py` - Main analysis command with ML/AI/chart flags
- `analysis/` - Technical indicators and AI-powered analysis modules
- `inquiry/` - Interactive menu system with API integration using cluefin-openapi

**Data & Display** (`src/cluefin_cli/`):
- `data/fetcher.py` - Data retrieval abstraction layer
- `display/charts.py` - Terminal-based chart rendering with plotext
- `utils/formatters.py` - Korean currency and number formatting

## Critical Implementation Patterns

### ML Model Workflow
```python
# Initialize with optional model parameters
predictor = StockMLPredictor(model_params={"n_estimators": 100})

# Fit with historical data
predictor.fit(stock_data)  # DataFrame with OHLCV columns

# Predict with SHAP explanations
prediction, confidence, shap_values = predictor.predict_with_shap(current_data)
```

### Command Integration
```python
# Commands must use Rich Console for consistent UI
console = Console()

# ML prediction integration pattern
if ml_predict:
    predictor = StockMLPredictor()
    result = predictor.analyze(stock_data)
    console.print(result.formatted_output)
```

### Korean Market Data Handling
- Stock codes: 6-digit format (e.g., "005930" for Samsung)
- Timezone: All processing assumes KST (Korea Standard Time)
- Trading hours: 9:00-15:30 KST for model feature engineering
- Currency formatting: Korean Won (₩) with comma separators

## Development Workflows

### Testing Strategy
```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/unit/ml/test_ml_pipeline.py

# Run ML-specific tests (requires sample data)
uv run pytest tests/unit/ml/ -v
```

**Test Structure**:
- Unit tests in `tests/unit/` mirror `src/` structure
- ML tests use synthetic Korean stock data
- Command tests use Click testing utilities

### Adding New Features

**New Technical Indicators**:
1. Add to `FeatureEngineer` in `ml/feature_engineering.py`
2. Update feature count in docstrings and comments
3. Add unit tests with sample OHLCV data

**New CLI Options**:
1. Add Click options to `commands/analyze.py` 
2. Integrate with existing display logic
3. Update help text and README examples

**New ML Models**:
1. Extend `StockPredictor` in `ml/models.py`
2. Update SHAP explainer if needed
3. Add model-specific diagnostics

### Environment Setup
```bash
# Required system dependency (macOS)
brew install ta-lib lightgbm

# Required environment variables
KIWOOM_APP_KEY=your_key
KIWOOM_SECRET_KEY=your_secret  
OPENAI_API_KEY=your_openai_key

# Optional ML configuration
ML_MODEL_PATH=models/
ML_CACHE_DIR=.ml_cache/
```

## Code Quality Standards

- **Ruff Configuration**: Extends root `pyproject.toml`, includes `src/**` and `tests/**`
- **Rich UI Consistency**: All user output must use Rich Console for formatting
- **Error Handling**: ML operations should gracefully handle insufficient data
- **Korean Text**: Support Korean company names and financial terminology
- **Logging**: Use loguru for debugging and error tracking

## Dependencies Management

**Key Dependencies**:
- `click` - CLI framework
- `rich` - Terminal UI and formatting
- `lightgbm` - ML model training
- `shap` - Model explainability
- `TA-Lib` - Technical analysis (requires system installation)
- `cluefin-openapi` - Korean financial API clients
- `plotext` - Terminal-based charting

**Development Dependencies**: Managed at workspace root level with shared ruff/pytest configuration.