# Design Document

## Overview

This document outlines the technical design for refactoring the KRX module using `functools.partial` to eliminate code duplication. The core factory infrastructure (`_factory.py`) has been implemented with the `KrxApiMethodFactory` class that provides a common abstraction layer while preserving type safety and reducing repetitive patterns across multiple KRX API modules.

**Implementation Status**: The `KrxApiMethodFactory` in `packages/cluefin-openapi/src/cluefin_openapi/krx/_factory.py` provides the core infrastructure. This design document shows how to integrate this existing factory into all KRX modules to eliminate code duplication.

The core approach involves using the existing factory's `create_single_param_method()` to replace duplicated implementations across different market segments.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    KRX Client Architecture                  │
├─────────────────────────────────────────────────────────────┤
│  Public API Methods (Stock, Bond, Index, Derivatives)      │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│  │   Stock     │ │    Bond     │ │   Index     │   ...    │
│  │ .get_kospi()│ │ .get_ktb()  │ │ .get_krx()  │          │
│  └─────────────┘ └─────────────┘ └─────────────┘          │
├─────────────────────────────────────────────────────────────┤
│                 Factory Layer (IMPLEMENTED)                 │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              KrxApiMethodFactory                        │ │
│  │  • create_single_param_method() ✓ IMPLEMENTED          │ │
│  │  • create_multi_param_method() ✓ IMPLEMENTED           │ │
│  │  • _api_method_template() ✓ IMPLEMENTED                │ │
│  │  • TypedApiMethod[T] Protocol ✓ IMPLEMENTED            │ │
│  └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                    Core Client Layer                        │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                Client._get()                            │ │
│  │  • HTTP request handling                               │ │
│  │  • Authentication (AUTH_KEY)                           │ │
│  │  • Error handling & status codes                       │ │
│  │  • Korean API specifics                                │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Integration Points

The refactoring integrates with existing systems while maintaining compatibility:

- **Pydantic Models**: All existing type definitions remain unchanged
- **Client Authentication**: Preserves AUTH_KEY header mechanism
- **Error Handling**: Maintains KRX-specific exception hierarchy
- **Korean API Conventions**: Retains field aliases and parameter names

## Components and Interfaces

### Core Abstraction Interface

```typescript
// Type definitions for the abstraction layer
interface ApiEndpointConfig {
    path_template: string;           // e.g., "/svc/apis/sto/{}"
    endpoint_file: string;           // e.g., "stk_bydd_trd.json"
    response_model: Type[BaseModel]; // Pydantic model class
}

interface ApiMethodTemplate {
    name: str;
    endpoint_config: ApiEndpointConfig;
    param_mapping: Dict[str, str];   // parameter name mappings
    docstring_template: str;
}
```

### Implemented Factory Infrastructure

The `KrxApiMethodFactory` has been implemented in `packages/cluefin-openapi/src/cluefin_openapi/krx/_factory.py`:

```python
# Actual implementation from _factory.py
from functools import partial
from typing import Callable, Dict, Generic, Protocol, Type, TypeVar
from cluefin_openapi.krx._client import Client
from cluefin_openapi.krx._model import KrxHttpBody, KrxHttpResponse

T = TypeVar("T", bound=KrxHttpBody)

class TypedApiMethod(Protocol, Generic[T]):
    """Protocol for type-safe API method signatures with proper mypy compatibility."""
    def __call__(self, base_date: str) -> KrxHttpResponse[T]: ...

def _api_method_template(
    client: Client, path_template: str, endpoint: str,
    response_model: Type[T], base_date: str, **kwargs: Dict[str, str]
) -> KrxHttpResponse[T]:
    """Core template function for single-parameter API calls."""
    params = {"basDd": base_date}  # Korean API parameter mapping
    if kwargs:
        params.update(kwargs)
    response = client._get(path_template.format(endpoint), params=params)
    body = response_model.model_validate(response)
    return KrxHttpResponse(body=body)

class KrxApiMethodFactory:
    """Factory class for generating partial functions that abstract common KRX API patterns."""

    @staticmethod
    def create_single_param_method(
        client: Client, path_template: str, endpoint: str,
        response_model: Type[T], docstring: str
    ) -> TypedApiMethod[T]:
        """Create a partial function for single-parameter base_date API methods."""
        method = partial(
            _api_method_template,
            client=client,
            path_template=path_template,
            endpoint=endpoint,
            response_model=response_model,
        )
        method.__doc__ = docstring
        method.__name__ = f"krx_api_method_{endpoint.replace('.', '_')}"
        return method
```

### Stock Module Refactoring Example

**Current Implementation (with duplication):**
```python
class Stock:
    def __init__(self, client: Client):
        self.client = client
        self.path = "/svc/apis/sto/{}"

    def get_kospi(self, base_date: str) -> KrxHttpResponse[StockKospi]:
        """KOSPI 일별매매정보 조회"""
        params = {"basDd": base_date}
        response = self.client._get(self.path.format("stk_bydd_trd.json"), params=params)
        body = StockKospi.model_validate(response)
        return KrxHttpResponse(body=body)

    def get_kosdaq(self, base_date: str) -> KrxHttpResponse[StockKosdaq]:
        """KOSDAQ 일별매매정보 조회"""
        params = {"basDd": base_date}
        response = self.client._get(self.path.format("ksq_bydd_trd.json"), params=params)
        body = StockKosdaq.model_validate(response)
        return KrxHttpResponse(body=body)
```

**Refactored Implementation (using factory):**
```python
from cluefin_openapi.krx._factory import KrxApiMethodFactory

class Stock:
    def __init__(self, client: Client):
        self.client = client
        self.path = "/svc/apis/sto/{}"

        # Use factory to eliminate duplication
        self.get_kospi = KrxApiMethodFactory.create_single_param_method(
            client=self.client,
            path_template=self.path,
            endpoint="stk_bydd_trd.json",
            response_model=StockKospi,
            docstring="KOSPI 일별매매정보 조회\n\nArgs:\n    base_date (str): 조회할 날짜 (YYYYMMDD 형식)\n\nReturns:\n    KrxHttpResponse[StockKospi]: KOSPI 일별매매정보 데이터"
        )

        self.get_kosdaq = KrxApiMethodFactory.create_single_param_method(
            client=self.client,
            path_template=self.path,
            endpoint="ksq_bydd_trd.json",
            response_model=StockKosdaq,
            docstring="KOSDAQ 일별매매정보 조회\n\nArgs:\n    base_date (str): 조회할 날짜 (YYYYMMDD 형식)\n\nReturns:\n    KrxHttpResponse[StockKosdaq]: KOSDAQ 일별매매정보 데이터"
        )
```

## Data Models

### Refactoring Configuration Schema

```python
from typing import Dict, List, Optional, Type
from pydantic import BaseModel, Field

class EndpointConfig(BaseModel):
    """Configuration for a single API endpoint"""
    path_template: str = Field(..., description="URL path template")
    endpoint_file: str = Field(..., description="Specific endpoint file")
    response_model_name: str = Field(..., description="Response model class name")
    method_name: str = Field(..., description="Generated method name")
    docstring: str = Field(..., description="Method documentation")
    
class ModuleRefactorConfig(BaseModel):
    """Configuration for refactoring a complete module"""
    module_name: str = Field(..., description="Module name (e.g., 'stock')")
    base_path_template: str = Field(..., description="Base path template")
    endpoints: List[EndpointConfig] = Field(..., description="List of endpoints")
    
class RefactorPlan(BaseModel):
    """Complete refactoring plan for all modules"""
    modules: Dict[str, ModuleRefactorConfig] = Field(..., description="Module configurations")
    common_patterns: List[str] = Field(..., description="Identified common patterns")
```

### Method Signature Preservation

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class KrxApiMethod(Protocol):
    """Protocol ensuring method signature compatibility"""
    def __call__(self, base_date: str) -> KrxHttpResponse[Any]:
        """Standard signature for single-parameter KRX API methods"""
        ...

class TypedApiMethod(Generic[T]):
    """Type-safe wrapper for generated API methods"""
    def __init__(self, partial_method: Callable[[str], KrxHttpResponse[T]]):
        self._method = partial_method
        self.__doc__ = partial_method.__doc__
    
    def __call__(self, base_date: str) -> KrxHttpResponse[T]:
        return self._method(base_date)
```

## Error Handling

### Error Handling Strategy

The refactoring maintains identical error handling behavior:

```python
class RefactoredMethodError(Exception):
    """Errors specific to the refactored method implementation"""
    pass

class PartialFunctionError(RefactoredMethodError):
    """Errors in partial function creation or execution"""
    pass

def error_preserving_wrapper(original_method: Callable) -> Callable:
    """Wrapper ensuring error handling behavior is preserved"""
    def wrapper(*args, **kwargs):
        try:
            return original_method(*args, **kwargs)
        except Exception as e:
            # Re-raise with identical exception hierarchy
            raise e
    return wrapper
```

### Error Response Validation

```python
def validate_error_compatibility(
    original_method: Callable,
    refactored_method: Callable,
    test_cases: List[Dict]
) -> bool:
    """Validates that error handling behavior is preserved"""
    for test_case in test_cases:
        try:
            orig_result = original_method(**test_case['params'])
            refact_result = refactored_method(**test_case['params'])
            assert type(orig_result) == type(refact_result)
        except Exception as orig_error:
            try:
                refactored_method(**test_case['params'])
                assert False, "Expected same exception"
            except Exception as refact_error:
                assert type(orig_error) == type(refact_error)
    return True
```

## Testing Strategy

### Unit Tests

```python
import pytest
from functools import partial
from unittest.mock import Mock

class TestPartialFunctionFactory:
    """Test the core factory functionality"""
    
    def test_single_param_method_creation(self):
        """Test basic partial function creation"""
        client = Mock()
        factory = KrxApiMethodFactory(client)
        
        method = factory.create_single_param_method(
            path_template="/test/{}",
            endpoint_file="test.json",
            response_model=StockKospi,
            param_name="base_date",
            param_key="basDd"
        )
        
        assert callable(method)
        assert hasattr(method, '__doc__')
    
    def test_method_signature_preservation(self):
        """Test that generated methods have correct signatures"""
        # Implementation validates partial methods maintain expected signatures
        pass
    
    def test_korean_parameter_mapping(self):
        """Test Korean field alias preservation"""
        # Validate that basDd parameter mapping is preserved
        pass

class TestRefactoredMethods:
    """Test individual refactored methods"""
    
    def test_stock_methods_identical_behavior(self):
        """Test that Stock methods behave identically"""
        # Requirements: 4.1, 4.2, 4.3
        pass
    
    def test_bond_methods_identical_behavior(self):
        """Test that Bond methods behave identically"""
        # Requirements: 4.1, 4.2, 4.3
        pass
```

### Integration Tests

```python
class TestKrxApiIntegration:
    """Integration tests with real KRX endpoints"""
    
    @pytest.mark.integration
    def test_refactored_stock_api_calls(self):
        """Test refactored Stock API calls with real endpoints"""
        # Requirements: 6.3
        pass
    
    @pytest.mark.integration  
    def test_korean_date_format_handling(self):
        """Test Korean date format (YYYYMMDD) handling"""
        # Requirements: 5.2
        pass
    
    @pytest.mark.integration
    def test_authentication_preservation(self):
        """Test that AUTH_KEY authentication still works"""
        # Requirements: 5.3
        pass
```

### Performance Tests

```python
class TestPerformanceImpact:
    """Measure performance impact of refactoring"""
    
    def test_method_creation_overhead(self):
        """Measure overhead of partial function creation"""
        # Should be minimal since creation happens at initialization
        pass
    
    def test_method_execution_performance(self):
        """Compare execution speed of original vs refactored methods"""
        # Should be identical or imperceptibly different
        pass
```

## Performance Considerations

### Initialization Performance
- **Partial Function Creation**: Occurs once during module initialization
- **Memory Overhead**: Minimal additional memory for partial function objects
- **Import Time**: Slight increase due to factory initialization

### Runtime Performance
- **Method Execution**: Identical performance to original implementation
- **Function Call Overhead**: Negligible additional overhead from partial functions
- **Type Checking**: Preserved mypy performance with proper type hints

### Memory Usage
```python
# Memory usage comparison analysis
original_method_memory = sys.getsizeof(original_method)
partial_method_memory = sys.getsizeof(partial_method)
memory_overhead = partial_method_memory - original_method_memory
# Expected: < 200 bytes additional per method
```

## Security Considerations

### Authentication Preservation
- **AUTH_KEY Header**: Maintained in all API calls through client._get()
- **Token Security**: No changes to token handling mechanisms
- **Request Signing**: Korean API request patterns preserved

### Input Validation
- **Parameter Validation**: Preserved through Pydantic model validation
- **Date Format Validation**: YYYYMMDD format requirements maintained
- **Korean Stock Code Validation**: Existing validation patterns preserved

### Error Information Disclosure
- **Error Messages**: Identical error disclosure behavior
- **Exception Details**: Same level of information exposure
- **Debug Information**: Consistent debug output patterns

## Migration and Deployment

### Migration Strategy (Factory Infrastructure Complete)

**Current Status**: ✅ Phase 1 Complete - Factory infrastructure exists in `_factory.py`

**Phase 2: Stock Module Integration**
1. Refactor `_stock.py` using existing `KrxApiMethodFactory.create_single_param_method()`
2. Replace all 6 duplicated methods (get_kospi, get_kosdaq, get_konex, etc.)
3. Validate identical behavior with existing unit tests
4. Run integration tests to ensure no regressions

**Phase 3: Bond Module Integration**
1. Apply factory pattern to `_bond.py` methods
2. Refactor get_korea_treasury_bond_market, get_general_bond_market, get_small_bond_market
3. Validate all Korean field aliases and API specifics

**Phase 4: Remaining Module Integration**
1. Apply pattern to `_index.py`, `_derivatives.py`, `_exchange_traded_product.py`
2. Handle any module-specific variations using factory parameters
3. Cross-module integration testing

**Phase 5: Testing and Validation**
1. Create comprehensive unit tests for `KrxApiMethodFactory`
2. Performance benchmarking to measure duplication reduction
3. Final regression testing with all existing test suites

### Deployment Strategy

```python
# Feature flag approach for safe deployment
class KrxClientConfig:
    use_refactored_methods: bool = Field(default=False)
    
class Client:
    def __init__(self, auth_key: str, config: Optional[KrxClientConfig] = None):
        self.config = config or KrxClientConfig()
        # Initialize both old and new implementations during transition
```

### Rollback Plan
- **Version Control**: Tagged releases for each phase
- **Feature Toggle**: Ability to switch between implementations
- **Test Coverage**: 100% test coverage ensures safe rollback
- **Monitoring**: Performance and error rate monitoring

## Future Enhancements

### Additional Abstraction Opportunities
- **Multi-parameter Methods**: Extend pattern to complex parameter methods
- **Response Transformation**: Common response processing patterns
- **Caching Integration**: Abstract caching mechanisms
- **Rate Limiting**: Common rate limiting patterns

### Code Generation Possibilities
```python
# Future: Generate methods from configuration files
def generate_krx_module_from_config(config: ModuleRefactorConfig) -> str:
    """Generate complete module code from configuration"""
    # Auto-generate module files from declarative configuration
    pass
```

### Enhanced Type Safety
```python
# Future: Enhanced generic typing
class TypedKrxClient(Generic[T]):
    """Type-safe client with compile-time endpoint validation"""
    def get_endpoint(self, endpoint_name: Literal["kospi", "kosdaq"]) -> T:
        pass
```

### Performance Monitoring Integration
- **Method Call Metrics**: Automatic performance tracking
- **Error Rate Monitoring**: Built-in error rate analysis  
- **Usage Analytics**: Method usage pattern analysis

_Requirements: All sections reference specific requirements as indicated (e.g., 1.1, 2.1, etc.)_