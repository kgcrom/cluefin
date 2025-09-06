---
inclusion: always
---

# Cluefin Product Guidelines

## Product Overview

Cluefin is a Korean financial investment toolkit for educational and research purposes. Focus exclusively on Korean markets (KOSPI, KOSDAQ, KONEX) with Korean language support throughout.

## Architecture Patterns

### Package Structure
- **cluefin-openapi**: Reusable API client library with domain-specific modules
- **cluefin-cli**: Terminal application consuming the library for analysis and visualization

### API Client Design
- All clients must implement: authentication, rate limiting, caching, retry logic
- Use Pydantic v2 models for all external API responses and validation
- Domain modules: `_domestic_account`, `_domestic_chart`, `_domestic_stock_info`, etc.
- Client properties match domain names: `client.account`, `client.chart`, `client.stock_info`

### Error Handling Patterns
- Create specific exceptions: `KiwoomAuthenticationError`, `KiwoomRateLimitError`
- Include Korean error messages and context in exception details
- Implement exponential backoff for retryable errors (network, rate limits)
- Log retry attempts with request context for debugging

## Korean Market Standards

### Data Formats
- Stock codes: 6-digit format only ("005930", "000660")
- Currency: KRW with Korean number formatting (천, 만, 억)
- Time zone: KST (UTC+9) for all market data
- Market hours: 09:00-15:30 KST (handle market closures gracefully)

### Language Support
- Include Korean company names (`name_kr`) alongside English (`name_en`)
- Support Korean sector classifications and industry names
- Use Korean market terminology in user-facing messages

## Code Conventions

### Naming & Structure
- Private modules: underscore prefix (`_client.py`, `_auth.py`)
- Type definitions: `_types.py` suffix (`_domestic_account_types.py`)
- Test markers: `@pytest.mark.integration`, `@pytest.mark.slow`
- Method naming: descriptive and consistent (`get_inquire_balance`, `get_daily_chart`)

### Data Validation
- All API responses must use Pydantic models with proper field validation
- Validate Korean stock codes with regex pattern: `^[0-9]{6}$`
- Handle missing or null data gracefully with Optional types
- Cache frequently accessed reference data (stock info, sector mappings)

## User Experience Requirements

### Terminal Interface
- Use Rich library for all formatting (tables, progress bars, colors)
- Implement interactive menus with clear navigation
- Provide batch processing modes for automation
- Include helpful error messages with suggested actions

### Educational Focus
- Always include investment risk disclaimers
- Explain technical indicators with educational context
- Provide market characteristic explanations for Korean markets
- Never give specific buy/sell recommendations - analysis only

### AI Integration Guidelines
- Use OpenAI for sentiment analysis and trend interpretation
- Include Korean market context in AI prompts
- Maintain objectivity in all AI-generated content
- Explain technical analysis results in educational terms

## Security & Compliance

### Data Handling
- Never log sensitive account information or API keys
- Implement secure credential storage and retrieval
- Respect API rate limits and terms of service
- Handle authentication tokens securely with proper expiration

### Ethical Guidelines
- Educational purpose only - include disclaimers prominently
- No investment advice or recommendations
- Transparent about data sources and limitations
- Respect user privacy and data protection requirements