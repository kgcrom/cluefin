# Implementation Plan

## Current Status
✅ **Core Infrastructure Complete**: The `KrxApiMethodFactory` has been implemented in `packages/cluefin-openapi/src/cluefin_openapi/krx/_factory.py` with full functionality including:
- `create_single_param_method()` for single-parameter API methods
- `create_multi_param_method()` for future extensibility
- `_api_method_template()` core template function
- `TypedApiMethod[T]` protocol for type safety
- Korean field alias preservation ("basDd" parameter mapping)

## Implementation Tasks

- [x] 1. Create Core Abstraction Infrastructure ✅ **COMPLETED**
  Create the `KrxApiMethodFactory` class in a new `_factory.py` module within the KRX package. This factory will contain the core logic for generating partial functions that abstract common API patterns. The factory should handle single-parameter methods (like base_date), preserve type hints, and maintain Korean field aliases. Include comprehensive docstring templates and parameter mapping capabilities.

  **Status**: ✅ Implemented in `_factory.py` with full type safety and Korean API support.
  _Requirements: 1.1, 2.1, 2.3_

- [x] 2. Implement Single Parameter API Method Template ✅ **COMPLETED**
  Develop the `_api_method_template` function that serves as the base template for single-parameter API calls. This template should handle parameter processing, URL path formatting, HTTP client calls through `client._get()`, and response validation with Pydantic models. Ensure the template preserves Korean API specifics like "basDd" parameter mapping and maintains identical error handling.

  **Status**: ✅ `_api_method_template()` implemented with full Korean API support and error handling.
  _Requirements: 1.1, 2.2, 5.1, 5.3_

- [x] 3. Add Type Safety Infrastructure ✅ **COMPLETED**
  Implement proper TypeScript-style type hints and generic type parameters for the factory methods. Create the `TypedApiMethod` wrapper class to ensure mypy compatibility and proper type inference. Add Protocol definitions for method signature validation and ensure `KrxHttpResponse[T]` generic typing is preserved throughout the abstraction layer.

  **Status**: ✅ `TypedApiMethod[T]` protocol implemented with full mypy compatibility.
  _Requirements: 3.1, 3.2, 3.3_

- [x] 4. Create Comprehensive Unit Tests for Factory ✅ **COMPLETED**
  Develop unit tests for the existing `KrxApiMethodFactory` class covering:
  - Partial function creation and execution
  - Type hint preservation and mypy compatibility
  - Korean parameter mapping ("basDd" field alias)
  - Method signature validation with `TypedApiMethod[T]` protocol
  - Error condition testing with Korean stock codes (e.g., "005930")
  - Use `requests_mock` to simulate API responses

  **Status**: ✅ Comprehensive unit tests implemented in `packages/cluefin-openapi/tests/krx/test_factory_unit.py` with 14 test cases covering all factory functionality including type safety, Korean parameter mapping, error handling, and multi-parameter support.
  _Requirements: 6.2, 6.4_

- [x] 5. Refactor Stock Module Using Existing Factory ✅ **COMPLETED**
  Replace all duplicate method implementations in `_stock.py` with `KrxApiMethodFactory.create_single_param_method()` calls:
  - `get_kospi()` → use existing factory with "stk_bydd_trd.json"
  - `get_kosdaq()` → use existing factory with "ksq_bydd_trd.json"
  - `get_konex()` → use existing factory with "knx_bydd_trd.json"
  - `get_warrant()` → use existing factory with "sw_bydd_trd.json"
  - `get_subscription_warrant()` → use existing factory with "sr_bydd_trd.json"
  - `get_kospi_base_info()` → use existing factory with "stk_isu_base_info.json"

  **Status**: ✅ Successfully refactored all 6 specified methods to use `KrxApiMethodFactory.create_single_param_method()`. Eliminated code duplication while preserving identical behavior, type safety, and Korean API specifics. All unit tests pass.
  _Requirements: 1.2, 1.3, 4.1, 4.2_

- [x] 6. Validate Stock Module Refactoring ✅ **COMPLETED**
  ~~Run all existing unit tests for the Stock module to ensure no regressions. Execute integration tests with real KRX endpoints to validate identical behavior. Compare error handling, response formats, and edge cases between original and refactored implementations. Verify that Korean date format (YYYYMMDD) and stock codes are handled identically.~~

  **Status**: ✅ Comprehensive validation completed successfully:
  - All unit tests pass (8/8 ✅)
  - All integration tests pass with real KRX endpoints (8/8 ✅)
  - Error handling behavior identical (KrxServerError preserved)
  - Korean date format (YYYYMMDD) handling verified ✅
  - Korean stock codes and names preserved ✅ ("005930", "삼성전자")
  - Response formats and edge cases identical ✅
  - `KrxHttpResponse[T]` typing preserved ✅
  - Empty response handling confirmed ✅
  _Requirements: 4.3, 6.1, 6.3_

- [ ] 7. Extend Factory for Multi-Parameter Methods ✅ **COMPLETED**
  Analyze and implement support for methods with multiple parameters beyond single base_date. Create `create_multi_param_method` in the factory to handle more complex API endpoints. Ensure parameter mapping flexibility while maintaining type safety and Korean field alias support.

  **Status**: ✅ `create_multi_param_method()` already implemented in the existing factory.
  _Requirements: 2.1, 2.4, 5.1_

- [ ] 8. Refactor Bond Module Using Existing Factory
  Apply the existing factory pattern to `_bond.py` module using `KrxApiMethodFactory.create_single_param_method()`:
  - `get_korea_treasury_bond_market()` → use factory with "kts_bydd_trd.json"
  - `get_general_bond_market()` → use factory with "bnd_bydd_trd.json"
  - `get_small_bond_market()` → use factory with "smb_bydd_trd.json"

  **Result**: Eliminate 3 duplicated implementations while preserving Korean bond market specifics.
  _Requirements: 1.2, 1.3, 4.1_

- [ ] 9. Refactor Index Module Using Factory Pattern
  Update `_index.py` module methods including `get_krx()`, `get_kospi()`, `get_kosdaq()`, `get_bond()`, and `get_derivatives()` to use partial function templates. Maintain all existing functionality and Korean index-specific handling while eliminating code duplication.
  _Requirements: 1.2, 1.3, 4.1_

- [ ] 10. Refactor Derivatives Module Using Factory Pattern
  Apply factory pattern to `_derivatives.py` module's complex methods like `get_trading_of_futures_exclude_stock()`, `get_trading_of_kospi_futures()`, and related option methods. Handle longer method names and more complex Korean financial terminology while maintaining identical functionality.
  _Requirements: 1.2, 1.3, 4.1, 5.4_

- [ ] 11. Update Remaining KRX Modules
  Apply the factory pattern to other KRX modules including `_exchange_traded_product.py`, `_general_product.py`, and `_esg.py`. Identify and abstract common patterns while preserving module-specific functionality and Korean financial API requirements.
  _Requirements: 1.2, 4.1, 5.1_

- [ ] 12. Implement Error Compatibility Validation
  Create comprehensive error handling validation that compares original methods with refactored implementations. Ensure identical exception types, messages, and error codes. Test with various failure scenarios including authentication errors, malformed dates, and network timeouts to guarantee backward compatibility.
  _Requirements: 4.2, 6.4_

- [ ] 13. Add Performance Benchmarking
  Implement performance comparison testing between original and refactored methods. Measure method creation overhead, execution time, and memory usage. Ensure that refactoring introduces minimal performance impact and document any measurable differences. Include benchmarks for both unit test scenarios and real API calls.
  _Requirements: Performance considerations from design document_

- [ ] 14. Comprehensive Integration Testing
  Execute full integration test suite against real KRX endpoints using actual API keys. Test all refactored modules to ensure identical behavior with live data. Validate Korean date formats, authentication mechanisms, and market-specific responses. Include edge cases like market holidays and non-trading days.
  _Requirements: 6.3, 5.2, 5.3_

- [ ] 15. Update Documentation and Type Hints
  Update all docstrings to reflect the new factory-based approach while maintaining user-facing documentation identical. Ensure all type hints are properly updated for mypy compatibility. Add internal documentation for the factory pattern and partial function usage for future maintainers.
  _Requirements: 3.4, 4.1_

- [ ] 16. Code Review and Quality Assurance
  Conduct thorough code review of all refactored modules focusing on maintainability, readability, and adherence to Python best practices. Validate that the DRY principle objectives are achieved with measurable code duplication reduction. Ensure Korean financial API specifics are properly preserved throughout.
  _Requirements: 1.2, 5.1, 5.4_

- [ ] 17. Final Regression Testing
  Execute complete test suite including unit, integration, and performance tests to validate the entire refactoring effort. Ensure all existing functionality works identically to the original implementation. Verify that Korean stock codes (e.g., "005930"), date formats, and API responses are handled without any behavioral changes.
  _Requirements: 6.1, 6.2, 6.3, 4.3_

- [ ] 18. Migration Documentation and Deployment Preparation
  Create migration documentation for other developers working with the KRX module. Document the new factory pattern, how to add new endpoints, and maintain the abstraction layer. Prepare deployment checklist and rollback procedures in case of issues during production deployment.
  _Requirements: Future enhancement considerations from design document_

## Implementation Examples

### Example 1: Stock Module Refactoring
**Before (duplicated code):**
```python
def get_kospi(self, base_date: str) -> KrxHttpResponse[StockKospi]:
    params = {"basDd": base_date}
    response = self.client._get(self.path.format("stk_bydd_trd.json"), params=params)
    body = StockKospi.model_validate(response)
    return KrxHttpResponse(body=body)
```

**After (using factory):**
```python
def __init__(self, client: Client):
    self.client = client
    self.path = "/svc/apis/sto/{}"

    self.get_kospi = KrxApiMethodFactory.create_single_param_method(
        client=self.client,
        path_template=self.path,
        endpoint="stk_bydd_trd.json",
        response_model=StockKospi,
        docstring="KOSPI 일별매매정보 조회\n\nArgs:\n    base_date (str): 조회할 날짜 (YYYYMMDD 형식)"
    )
```

### Example 2: Factory Unit Test Structure
```python
# packages/cluefin-openapi/tests/krx/test_factory_unit.py
import pytest
from requests_mock import Mocker
from cluefin_openapi.krx._factory import KrxApiMethodFactory
from cluefin_openapi.krx._stock_types import StockKospi

def test_create_single_param_method_with_korean_stock_code(requests_mock: Mocker):
    # Test with Korean stock code "005930" (Samsung)
    mock_response = {"OutBlock_1": [{"stk_cd": "005930", "stk_nm": "삼성전자"}]}
    requests_mock.get("http://test.krx.co.kr/svc/apis/sto/stk_bydd_trd.json", json=mock_response)

    method = KrxApiMethodFactory.create_single_param_method(
        client=client, path_template="/svc/apis/sto/{}",
        endpoint="stk_bydd_trd.json", response_model=StockKospi,
        docstring="Test method"
    )

    result = method("20241201")
    assert isinstance(result, KrxHttpResponse)
    assert len(result.body.data) == 1
```

### Future Enhancement Tasks

- [ ] 19. Implement Declarative Configuration System
  Create a configuration-based system where new API endpoints can be added through JSON/YAML configuration files rather than code changes. This would further reduce maintenance overhead and make the system more extensible for new KRX API endpoints.
  _Requirements: Future enhancements - Code generation possibilities_

- [ ] 20. Add Automatic Code Generation Capabilities
  Develop tooling to automatically generate new KRX module methods from API documentation or OpenAPI specifications. This would streamline the process of adding new endpoints and ensure consistency across the codebase.
  _Requirements: Future enhancements - Code generation possibilities_

- [ ] 21. Implement Advanced Caching Integration
  Abstract caching mechanisms into the factory pattern to provide consistent caching behavior across all KRX API methods. Include Korean timezone-aware cache invalidation and market-specific caching strategies.
  _Requirements: Future enhancements - Caching integration_

- [ ] 22. Add Method Usage Analytics and Monitoring
  Integrate performance monitoring and usage analytics into the factory pattern to track method performance, error rates, and usage patterns. This data can inform future optimizations and identify potential issues proactively.
  _Requirements: Future enhancements - Performance monitoring integration_