---
inclusion: always
---

# Cluefin Product Guidelines

Cluefin is a Python toolkit for Korean financial market APIs. When working with this codebase, follow these conventions to maintain consistency and quality.

## Architecture Patterns

### Module Organization
- **Library packages** (`packages/`): Use private module naming with underscore prefix
- **Application packages** (`apps/`): Use public module naming for CLI commands and features
- **Type definitions**: Separate `_types.py` files with Pydantic models
- **Domain modules**: One module per API domain or CLI feature area
- **Entry points**: Libraries use `_client.py`, apps use `main.py`

### Data Validation
- All API responses MUST use Pydantic models for validation
- Use `SecretStr` for credentials and sensitive data
- Include timezone info for all timestamps
- Use `Decimal` for financial values requiring precision

## Code Conventions

### Naming Standards
- Classes: `PascalCase` (`DomesticAccountClient`)
- Functions/methods: `snake_case` (`get_account_balance`)
- Constants: `UPPER_SNAKE_CASE` (`DEFAULT_TIMEOUT`)
- Private attributes: `_leading_underscore`

### Error Handling
- Use domain-specific exceptions (`KiwoomAPIError`, `KRXAPIError`)
- Include original API error codes in custom exceptions
- Provide actionable error messages
- Never expose sensitive data in error messages or logs

### Documentation Requirements
- All public classes and methods need docstrings
- Include usage examples for complex APIs
- Document rate limits and auth requirements
- Specify return types and possible exceptions

## Security & Compliance

### Credentials Management
- Never hardcode API keys or secrets
- Use environment variables for all credentials
- Implement automatic token refresh for session APIs
- Log security events without exposing sensitive data

### Financial Data Handling
- Protect account data in logs and error messages
- Validate account permissions before operations
- Handle market hours and trading calendar validation
- Include appropriate disclaimers (educational use only)

## API Integration Rules

### Rate Limiting & Reliability
- Implement proper rate limiting for API compliance
- Use backoff strategies for failed requests
- Cache responses where appropriate to reduce API calls
- Handle API versioning and deprecation gracefully

### Testing Requirements
- Unit tests for all business logic (mock external dependencies)
- Integration tests marked with `@pytest.mark.integration`
- Test error conditions and edge cases
- Separate unit and integration test directories

## Financial Domain Specifics

### Order Management
- Validate orders before submission
- Log all order operations for audit trails
- Handle partial fills and status updates
- Include risk management checks where applicable

### Market Data
- Validate market hours before data requests
- Handle market holidays and non-trading periods
- Include proper data attribution where required
- Respect data licensing agreements

### CLI Application Patterns
- **Command structure**: Use Click or similar for CLI command organization
- **Terminal output**: Rich formatting with color-coded data and ASCII charts
- **Configuration**: Environment variables for API keys and settings
- **Analysis modules**: Separate technical indicators, AI analysis, and data fetching
- **Display modules**: Terminal charts and formatted output rendering