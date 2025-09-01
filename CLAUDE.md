# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Start

**Essential Commands:**
```bash
# Setup with Python 3.10
uv venv --python 3.10
source .venv/bin/activate
uv sync --all-packages

# Test
uv run pytest
uv run ruff check . --fix

# CLI
cluefin-cli inquiry
```

**Key Info:**
- **Always use `uv run`** for Python commands (never `pip` directly)
- Type-safe Korean financial APIs with Pydantic models
- ML pipeline with LightGBM + SHAP explainability
- Interactive CLI with Rich UI and OpenAI integration

## Detailed Documentation

For comprehensive information, see these detailed guides:

### 📋 [Project Overview](docs/PROJECT_OVERVIEW.md)
- Vision, goals, and key features
- Korean market specialization
- Target users and use cases
- Current development status (Phase 2)

### 🏗️ [Architecture](docs/ARCHITECTURE.md)  
- Monorepo structure and package organization
- ML pipeline architecture with LightGBM
- API client patterns and response handling
- Korean financial API specifics

### 🛠️ [Tech Stack & Tools](docs/TECH_STACK.md)
- Complete technology stack
- Essential development commands
- Environment setup and configuration
- Troubleshooting guide

## Critical Implementation Patterns

### API Client Development
```python
# All responses wrapped with typed headers/body
@dataclass
class KiwoomHttpResponse(Generic[T]):
    headers: KiwoomHttpHeader  
    body: T

# Korean field aliases
cont_yn: Literal["Y", "N"] = Field(..., alias="cont-yn")
```

### File Naming Conventions
- Internal modules: `_client.py`, `_auth.py`, `_types.py`
- Type definitions: `_<module>_types.py` 
- Tests mirror source: `test_<module_name>.py`

### Testing Approach
- **Unit**: `requests_mock` with Korean stock codes (e.g., "005930")
- **Integration**: `@pytest.mark.integration` (requires API keys)
- **ML**: TimeSeriesSplit for financial data temporal validation

### Korean Market Considerations
- **Timezone**: Korea Standard Time (KST) throughout
- **Trading Hours**: 9:00-15:30 KST in ML models
- **Authentication**: OAuth2 for Kiwoom, simple auth for KRX
- **Rate Limiting**: Built-in per Korean API requirements

## Common Development Tasks

### Adding New API Endpoint
1. Define types in `_<module>_types.py`
2. Implement in corresponding module with `KiwoomHttpResponse[T]`
3. Add unit tests with `requests_mock`
4. Add integration tests with `@pytest.mark.integration`

### ML Model Development
1. Feature engineering in `ml/feature_engineering.py`
2. Model training in `ml/models.py` with TimeSeriesSplit
3. SHAP explanations in `ml/explainer.py`
4. Performance evaluation in `ml/diagnostics.py`

### Environment Variables
```bash
# Required
KIWOOM_APP_KEY=your_key
KIWOOM_SECRET_KEY=your_secret
OPENAI_API_KEY=your_openai_key

# Optional ML
ML_MODEL_PATH=models/
ML_CACHE_DIR=.ml_cache/
```

---

*For questions about specific components, consult the detailed documentation in the `docs/` directory.*
