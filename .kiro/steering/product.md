---
inclusion: always
---

# Product Guidelines

Cluefin is a Python toolkit for Korean financial market APIs and AI-powered investment analysis. Follow these product conventions when working with this codebase.

## Core Architecture

### Package Structure
- **cluefin-openapi**: Low-level API client library for Korean financial APIs (Kiwoom Securities, KRX)

### Design Principles
- **API-First**: All functionality exposed through clean, typed Python APIs
- **Type Safety**: Pydantic models for all data structures and API responses
- **Domain Separation**: Clear boundaries between different financial domains (account, market data, orders)
- **Educational Focus**: Code should be readable and well-documented for learning purposes

## Development Conventions

### API Client Patterns
- Use private module naming (`_client.py`, `_auth.py`) for internal implementation
- Separate type definitions in `_types.py` files using Pydantic models
- Domain-specific modules for each API area (`_domestic_account.py`, `_domestic_chart.py`)
- Consistent error handling with custom exception classes

### Data Handling
- All API responses must be validated through Pydantic models
- Use `SecretStr` for sensitive data (API keys, tokens)
- Implement proper rate limiting for API compliance
- Cache responses where appropriate to reduce API calls

### Authentication & Security
- Never hardcode credentials - use environment variables
- Implement automatic token refresh for session-based APIs
- Follow principle of least privilege for API permissions
- Log security events appropriately without exposing sensitive data

## Code Style Guidelines

### Naming Conventions
- Classes: PascalCase (`DomesticAccountClient`)
- Functions/methods: snake_case (`get_account_balance`)
- Constants: UPPER_SNAKE_CASE (`DEFAULT_TIMEOUT`)
- Private attributes: Leading underscore (`_session`)

### Documentation Requirements
- All public classes and methods must have docstrings
- Include usage examples in docstrings for complex APIs
- Document rate limits and authentication requirements
- Provide clear error handling guidance

### Error Handling
- Use domain-specific exceptions (`KiwoomAPIError`, `KRXAPIError`)
- Include original API error codes and messages
- Provide actionable error messages for common issues
- Log errors with appropriate context

## Financial Domain Rules

### Market Data
- Always include timezone information for timestamps
- Use appropriate data types for financial values (Decimal for precision)
- Validate market hours and trading calendars
- Handle market holidays and non-trading periods

### Order Management
- Implement proper order validation before submission
- Include risk management checks where applicable
- Log all order-related operations for audit trails
- Handle partial fills and order status updates

### Account Information
- Protect sensitive account data in logs and error messages
- Implement proper data retention policies
- Validate account permissions before operations
- Handle multiple account scenarios

## Integration Guidelines

### External APIs
- Respect rate limits and implement backoff strategies
- Handle API versioning and deprecation gracefully
- Provide fallback mechanisms for critical operations
- Monitor API health and availability

### Testing Strategy
- Unit tests for all business logic
- Integration tests for API interactions (marked appropriately)
- Mock external dependencies in unit tests
- Test error conditions and edge cases

## Compliance & Disclaimers

### Legal Requirements
- This is educational/research software only - not financial advice
- Users are responsible for their own investment decisions
- Comply with Korean financial regulations and API terms of service
- Include appropriate disclaimers in documentation

### Data Usage
- Respect data licensing agreements
- Implement proper data attribution where required
- Handle personal financial data with appropriate security
- Follow data retention and deletion policies