# Test Fix Implementation Plan

## Overview
This document outlines the systematic approach to fix 7 failing tests and 20 error conditions in the cluefin-cli inquiry module tests.

## Test Failure Summary
- [ ] **Failed Tests (7 total):**
  - [ ] `test_base_api_module.py`: 4 failures
  - [ ] `test_display_formatter.py`: 3 failures
- [ ] **Error Tests (20 total):**
  - [ ] All in `test_base_api_module.py` due to missing abstract method implementations

## Root Cause Analysis
- [ ] **1. BaseAPIModule Architecture Changes**
  - [ ] New Abstract Method: `get_client_attribute_name()` added but not implemented in test mocks
  - [ ] Client Access Pattern: Changed from `client.method()` to `client.{attribute}.method()`
  - [ ] Import Issues: Missing required imports in test files

- [ ] **2. DisplayFormatter API Changes**
  - [ ] Parameter Changes: Methods now expect `APIConfig` objects instead of strings
  - [ ] Data Structure Changes: Different expected data formats in formatters
  - [ ] Behavior Changes: Empty data handling logic modified

- [ ] **3. Configuration Issues**
  - [ ] Regex Patterns: Invalid regex validation patterns in sector_info.py
  - [ ] Parameter Validation: Inconsistent validation patterns

## Implementation Plan

### Phase 1: Fix BaseAPIModule Test Failures

- [ ] **1.1 Update Abstract Method Implementations**
  - [ ] File: `apps/cluefin-cli/tests/unit/commands/inquiry/test_base_api_module.py`
  - [ ] Add `get_client_attribute_name()` method to all test concrete classes
  - [ ] Update client mock structure to match new architecture
  - [ ] Required changes:
    ```python
    class ConcreteAPIModule(BaseAPIModule):
        def get_api_category(self):
            return sample_category

        def get_client_attribute_name(self):  # NEW - Add this method
            return "test_attr"

        def _format_and_display_result(self, result, api_config):
            self.console.print(f"Result: {result}")
    ```

- [ ] **1.2 Fix Client Mock Structure**
  - [ ] Current Problem: Tests mock `client.get_test_api()` directly
  - [ ] New Requirement: Mock `client.test_attr.get_test_api()`
  - [ ] Required changes:
    ```python
    @pytest.fixture
    def mock_client(self):
        client = Mock()
        # Old: client.get_test_api = Mock(...)
        # New: client.test_attr.get_test_api = Mock(...)
        client.test_attr = Mock()
        client.test_attr.get_test_api = Mock(return_value={"status": "success", "data": []})
        return client
    ```

- [ ] **1.3 Update Test Method Expectations**
  - [ ] Update `test_execute_api_with_retry_success`
  - [ ] Update `test_execute_api_with_retry_method_not_found`
  - [ ] Update all retry-related tests
  - [ ] Changes: Update assertions to check `client.test_attr.get_test_api.assert_called_once_with(**params)`

### Phase 2: Fix DisplayFormatter Test Failures

- [ ] **2.1 Fix Empty Data Handling Test**
  - [ ] File: `apps/cluefin-cli/tests/unit/commands/inquiry/test_display_formatter.py`
  - [ ] Method: `test_format_ranking_data_empty_output`
  - [ ] Issue: Test expects `display_error` but code calls `display_table`
  - [ ] Solution: Update test expectation to match actual behavior
    ```python
    def test_format_ranking_data_empty_output(self):
        mock_data = Mock()
        mock_data.output = []
        
        mock_api_config = APIConfig(
            name="test_api", 
            korean_name="테스트 API", 
            api_method="test_method"
        )
        
        with patch.object(self.formatter, "display_error") as mock_error:  # Change expectation
            self.formatter.format_ranking_data(mock_data, mock_api_config)
            mock_error.assert_called_once()
    ```

- [ ] **2.2 Fix APIConfig Parameter Issues**
  - [ ] Update volume renewal test method
  - [ ] Update broker analysis test method
  - [ ] Issue: Tests pass `Mock()` objects instead of proper `APIConfig`
  - [ ] Solution: Create proper APIConfig objects:
    ```python
    mock_api_config = APIConfig(
        name="broker_trading_analysis",
        korean_name="거래원매물대분석요청", 
        api_method="test_method",
        description="Test description"  # Add required fields
    )
    ```

- [ ] **2.3 Update Mock Data Structures**
  - [ ] Issue: Mock data doesn't match expected formatter input structure
  - [ ] Solution: Update mock data to include proper attributes and nested structures

### Phase 3: Fix SectorInfo Configuration Issues

- [ ] **3.1 Fix Regex Validation Patterns**
  - [ ] File: `apps/cluefin-cli/src/cluefin_cli/commands/inquiry/sector_info.py`
  - [ ] Line 80: Change `validation=r"r^\d{8}$"` → `validation=r"^\d{8}$"`  
  - [ ] Line 220: Change `validation=r"r$\d{8}$"` → `validation=r"^\d{8}$"`
  - [ ] Line 228: Change `validation=r"r$\d{8}$"` → `validation=r"^\d{8}$"`
  - [ ] Fix: Remove duplicate "r" prefix and fix regex anchors

### Phase 4: Comprehensive Test Updates

- [ ] **4.1 Update Import Statements**
  - [ ] Ensure all test files have proper imports:
    ```python
    from cluefin_cli.commands.inquiry.config_models import APICategory, APIConfig, ParameterConfig
    ```

- [ ] **4.2 Standardize Mock Patterns**
  - [ ] Create consistent mock patterns across all test files following the new client architecture

- [ ] **4.3 Update Assertions**
  - [ ] Modify all test assertions to match current code behavior and expected outcomes

## Implementation Order

### Step 1: Core Architecture Fixes
- [ ] **1.1** Fix `BaseAPIModule` abstract method implementations
- [ ] **1.2** Update client mock structures  
- [ ] **1.3** Fix regex patterns in sector_info.py

### Step 2: Test Behavior Updates
- [ ] **2.1** Update display formatter test expectations
- [ ] **2.2** Fix API config parameter passing
- [ ] **2.3** Correct mock data structures

### Step 3: Integration Testing
- [ ] **3.1** Run tests after each major change
- [ ] **3.2** Validate no regressions introduced  
- [ ] **3.3** Ensure realistic test data works properly

### Step 4: Cleanup and Validation
- [ ] **4.1** Standardize patterns across all test files
- [ ] **4.2** Add any missing test coverage
- [ ] **4.3** Final validation run

## Success Criteria

- [ ] All 7 failing tests pass
- [ ] All 20 error conditions resolved
- [ ] No test regressions introduced
- [ ] Tests accurately validate current implementation
- [ ] Consistent test patterns across all files

## Risk Mitigation

- [ ] **Fix one file at a time** to isolate issues
- [ ] **Run tests frequently** to catch regressions early
- [ ] **Validate against actual client behavior** to ensure mocks are realistic
- [ ] **Keep changes minimal** to reduce risk of introducing new issues

## Estimated Effort

- [ ] **Phase 1**: 2-3 hours (BaseAPIModule fixes)
- [ ] **Phase 2**: 1-2 hours (DisplayFormatter fixes)  
- [ ] **Phase 3**: 30 minutes (Configuration fixes)
- [ ] **Phase 4**: 1 hour (Integration and validation)
- [ ] **Total**: 4.5-6.5 hours of focused development time

# User prompt
1. fix test error. one by one. please describe plan and spec first, and then execute one by one.
2. write plan to markdown file.
3. convert todo markdown format(- [ ]) and numbering. because it's easy to recognize and execute step by step.
