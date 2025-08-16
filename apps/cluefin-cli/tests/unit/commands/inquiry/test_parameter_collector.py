"""Unit tests for parameter collection system."""

from typing import Any, Dict, List, Tuple
from unittest.mock import MagicMock, Mock, patch

import pytest

from cluefin_cli.commands.inquiry.config_models import APIConfig, ParameterConfig
from cluefin_cli.commands.inquiry.parameter_collector import BaseParameterCollector, ParameterCollector


class TestBaseParameterCollector:
    """Test the base parameter collector class."""

    @pytest.fixture
    def collector(self):
        """Create a parameter collector instance for testing."""
        return BaseParameterCollector()

    @pytest.fixture
    def select_param_config(self):
        """Create a select type parameter configuration for testing."""
        return ParameterConfig(
            name="market_type",
            korean_name="시장구분",
            param_type="select",
            choices=[("000", "전체"), ("001", "코스피"), ("101", "코스닥")],
            required=True,
        )

    @pytest.fixture
    def text_param_config(self):
        """Create a text type parameter configuration for testing."""
        return ParameterConfig(
            name="stock_code", korean_name="종목코드", param_type="text", validation=r"^\d{6}$", required=True
        )

    @pytest.fixture
    def date_param_config(self):
        """Create a date type parameter configuration for testing."""
        return ParameterConfig(name="query_date", korean_name="조회일자", param_type="date", required=True)

    @pytest.fixture
    def api_config(self, select_param_config, text_param_config, date_param_config):
        """Create an API configuration for testing."""
        optional_param = ParameterConfig(
            name="optional_field", korean_name="선택항목", param_type="text", required=False
        )

        return APIConfig(
            name="test_api",
            korean_name="테스트 API",
            api_method="test_method",
            required_params=[select_param_config, text_param_config],
            optional_params=[date_param_config, optional_param],
        )

    def test_collect_select_parameter_success(self, collector, select_param_config):
        """Test successful collection of select parameter."""
        with patch("inquirer.prompt") as mock_prompt:
            mock_prompt.return_value = {"market_type": "001"}

            result = collector._collect_select_parameter(select_param_config, required=True)

            assert result == "001"
            mock_prompt.assert_called_once()

    def test_collect_select_parameter_user_cancelled(self, collector, select_param_config):
        """Test select parameter collection when user cancels."""
        with patch("inquirer.prompt") as mock_prompt:
            mock_prompt.return_value = None

            result = collector._collect_select_parameter(select_param_config, required=True)

            assert result is None

    def test_collect_select_parameter_optional_skip(self, collector, select_param_config):
        """Test optional select parameter with skip option."""
        with patch("inquirer.prompt") as mock_prompt:
            mock_prompt.return_value = {"market_type": None}

            result = collector._collect_select_parameter(select_param_config, required=False)

            assert result is None

    def test_collect_text_parameter_success(self, collector, text_param_config):
        """Test successful collection of text parameter."""
        with patch("inquirer.prompt") as mock_prompt:
            mock_prompt.return_value = {"stock_code": "005930"}

            result = collector._collect_text_parameter(text_param_config, required=True)

            assert result == "005930"

    def test_collect_text_parameter_validation_failure(self, collector, text_param_config):
        """Test text parameter collection with validation failure."""
        with patch("inquirer.prompt") as mock_prompt, patch.object(collector.console, "print") as mock_print:
            # First call returns invalid input, second call returns valid input
            mock_prompt.side_effect = [{"stock_code": "invalid"}, {"stock_code": "005930"}]

            result = collector._collect_text_parameter(text_param_config, required=True)

            assert result == "005930"
            assert mock_prompt.call_count == 2
            mock_print.assert_called()

    def test_collect_text_parameter_empty_required(self, collector, text_param_config):
        """Test text parameter collection with empty required input."""
        with patch("inquirer.prompt") as mock_prompt, patch.object(collector.console, "print") as mock_print:
            # First call returns empty, second call returns valid input
            mock_prompt.side_effect = [{"stock_code": ""}, {"stock_code": "005930"}]

            result = collector._collect_text_parameter(text_param_config, required=True)

            assert result == "005930"
            assert mock_prompt.call_count == 2
            mock_print.assert_called()

    def test_collect_text_parameter_optional_empty(self, collector, text_param_config):
        """Test optional text parameter with empty input."""
        with patch("inquirer.prompt") as mock_prompt:
            mock_prompt.return_value = {"stock_code": ""}

            result = collector._collect_text_parameter(text_param_config, required=False)

            assert result is None

    def test_collect_date_parameter_success(self, collector, date_param_config):
        """Test successful collection of date parameter."""
        with patch("inquirer.prompt") as mock_prompt:
            mock_prompt.return_value = {"query_date": "20231201"}

            result = collector._collect_date_parameter(date_param_config, required=True)

            assert result == "20231201"

    def test_collect_date_parameter_invalid_format(self, collector, date_param_config):
        """Test date parameter collection with invalid format."""
        with patch("inquirer.prompt") as mock_prompt, patch.object(collector.console, "print") as mock_print:
            # First call returns invalid date, second call returns valid date
            mock_prompt.side_effect = [{"query_date": "2023-12-01"}, {"query_date": "20231201"}]

            result = collector._collect_date_parameter(date_param_config, required=True)

            assert result == "20231201"
            assert mock_prompt.call_count == 2
            mock_print.assert_called()

    def test_collect_date_parameter_invalid_date(self, collector, date_param_config):
        """Test date parameter collection with invalid date."""
        with patch("inquirer.prompt") as mock_prompt, patch.object(collector.console, "print") as mock_print:
            # First call returns invalid date, second call returns valid date
            mock_prompt.side_effect = [
                {"query_date": "20231301"},  # Invalid month
                {"query_date": "20231201"},
            ]

            result = collector._collect_date_parameter(date_param_config, required=True)

            assert result == "20231201"
            assert mock_prompt.call_count == 2
            mock_print.assert_called()

    def test_validate_date_valid_dates(self, collector):
        """Test date validation with valid dates."""
        valid_dates = ["20231201", "20240229", "19991231"]

        for date_str in valid_dates:
            assert collector._validate_date(date_str) is True

    def test_validate_date_invalid_dates(self, collector):
        """Test date validation with invalid dates."""
        invalid_dates = [
            "2023-12-01",  # Wrong format
            "20231301",  # Invalid month
            "20230229",  # Invalid leap year
            "202312",  # Too short
            "2023120100",  # Too long
            "abcd1201",  # Non-numeric
        ]

        for date_str in invalid_dates:
            assert collector._validate_date(date_str) is False

    def test_validate_text_regex_pattern(self, collector):
        """Test text validation with regex patterns."""
        # Test valid stock code pattern
        assert collector._validate_text("005930", r"^\d{6}$") is True
        assert collector._validate_text("12345", r"^\d{6}$") is False
        assert collector._validate_text("abc123", r"^\d{6}$") is False

    def test_validate_text_invalid_regex(self, collector):
        """Test text validation with invalid regex pattern."""
        # Invalid regex should return True (fallback)
        assert collector._validate_text("any_value", "[invalid") is True

    def test_collect_parameters_success(self, collector, api_config):
        """Test successful collection of all parameters."""
        with patch.object(collector, "_collect_single_parameter") as mock_collect:
            # Mock parameter collection results
            mock_collect.side_effect = ["001", "005930", "20231201", "optional_value"]

            result = collector.collect_parameters(api_config)

            expected = {
                "market_type": "001",
                "stock_code": "005930",
                "query_date": "20231201",
                "optional_field": "optional_value",
            }
            assert result == expected
            assert mock_collect.call_count == 4

    def test_collect_parameters_required_cancelled(self, collector, api_config):
        """Test parameter collection when required parameter is cancelled."""
        with (
            patch.object(collector, "_collect_single_parameter") as mock_collect,
            patch.object(collector.console, "print") as mock_print,
        ):
            # Mock cancellation on required parameter
            mock_collect.side_effect = ["001", None]  # Second required param cancelled

            result = collector.collect_parameters(api_config)

            assert result is None
            mock_print.assert_called_with("[red]Required parameter collection cancelled[/red]")

    def test_collect_parameters_optional_skipped(self, collector, api_config):
        """Test parameter collection with optional parameters skipped."""
        with patch.object(collector, "_collect_single_parameter") as mock_collect:
            # Mock required params success, optional params None
            mock_collect.side_effect = ["001", "005930", None, None]

            result = collector.collect_parameters(api_config)

            expected = {"market_type": "001", "stock_code": "005930"}
            assert result == expected

    def test_collect_parameters_keyboard_interrupt(self, collector, api_config):
        """Test parameter collection with keyboard interrupt."""
        with (
            patch.object(collector, "_collect_single_parameter") as mock_collect,
            patch.object(collector.console, "print") as mock_print,
        ):
            mock_collect.side_effect = KeyboardInterrupt()

            result = collector.collect_parameters(api_config)

            assert result is None
            mock_print.assert_called_with("\n[yellow]Parameter collection cancelled by user[/yellow]")

    def test_collect_parameters_exception(self, collector, api_config):
        """Test parameter collection with exception."""
        with (
            patch.object(collector, "_collect_single_parameter") as mock_collect,
            patch.object(collector.console, "print") as mock_print,
        ):
            mock_collect.side_effect = Exception("Test error")

            result = collector.collect_parameters(api_config)

            assert result is None
            mock_print.assert_called_with("[red]Error collecting parameters: Test error[/red]")

    def test_collect_single_parameter_unknown_type(self, collector):
        """Test collecting parameter with unknown type."""
        # Create a mock parameter config with unknown type
        invalid_param = Mock()
        invalid_param.param_type = "unknown"

        with pytest.raises(ValueError, match="Unknown parameter type: unknown"):
            collector._collect_single_parameter(invalid_param)

    def test_collect_select_parameter_no_choices(self, collector):
        """Test select parameter without choices raises error."""
        # Create a mock parameter config without choices
        invalid_select_param = Mock()
        invalid_select_param.name = "test"
        invalid_select_param.choices = None

        with pytest.raises(ValueError, match="No choices defined for select parameter: test"):
            collector._collect_select_parameter(invalid_select_param, required=True)


class TestParameterCollector:
    """Test the specialized parameter collector methods."""

    @pytest.fixture
    def collector(self):
        """Create a parameter collector instance for testing."""
        return ParameterCollector()

    def test_collect_market_type_with_all(self, collector):
        """Test market type collection with 전체 option."""
        with patch("inquirer.prompt") as mock_prompt:
            mock_prompt.return_value = {"market_type": "000"}

            result = collector.collect_market_type(include_all=True)

            assert result == "000"
            mock_prompt.assert_called_once()

    def test_collect_market_type_without_all(self, collector):
        """Test market type collection without 전체 option."""
        with patch("inquirer.prompt") as mock_prompt:
            mock_prompt.return_value = {"market_type": "001"}

            result = collector.collect_market_type(include_all=False)

            assert result == "001"
            mock_prompt.assert_called_once()

    def test_collect_market_type_cancelled(self, collector):
        """Test market type collection when user cancels."""
        with patch("inquirer.prompt") as mock_prompt:
            mock_prompt.return_value = None

            result = collector.collect_market_type()

            assert result is None

    def test_collect_date_input_success(self, collector):
        """Test successful date input collection."""
        with patch("inquirer.prompt") as mock_prompt:
            mock_prompt.return_value = {"date_input": "20231201"}

            result = collector.collect_date_input("기준일자", required=True)

            assert result == "20231201"

    def test_collect_date_input_invalid_format(self, collector):
        """Test date input with invalid format."""
        with patch("inquirer.prompt") as mock_prompt, patch.object(collector.console, "print") as mock_print:
            # First call returns invalid format, second call returns valid format
            mock_prompt.side_effect = [
                {"date_input": "2023-12-01"},
                {"date_input": "20231201"}
            ]

            result = collector.collect_date_input("기준일자", required=True)

            assert result == "20231201"
            assert mock_prompt.call_count == 2
            mock_print.assert_called()

    def test_collect_date_input_optional_empty(self, collector):
        """Test optional date input with empty value."""
        with patch("inquirer.prompt") as mock_prompt:
            mock_prompt.return_value = {"date_input": ""}

            result = collector.collect_date_input("기준일자", required=False)

            assert result is None

    def test_collect_date_input_required_empty(self, collector):
        """Test required date input with empty value."""
        with patch("inquirer.prompt") as mock_prompt, patch.object(collector.console, "print") as mock_print:
            # First call returns empty, second call returns valid date
            mock_prompt.side_effect = [
                {"date_input": ""},
                {"date_input": "20231201"}
            ]

            result = collector.collect_date_input("기준일자", required=True)

            assert result == "20231201"
            assert mock_prompt.call_count == 2
            mock_print.assert_called()

    def test_collect_date_input_cancelled(self, collector):
        """Test date input collection when user cancels."""
        with patch("inquirer.prompt") as mock_prompt:
            mock_prompt.return_value = None

            result = collector.collect_date_input("기준일자")

            assert result is None

    def test_collect_numeric_choice_success(self, collector):
        """Test successful numeric choice collection."""
        choices = [("첫번째 옵션", "1"), ("두번째 옵션", "2"), ("세번째 옵션", "3")]
        
        with patch("inquirer.prompt") as mock_prompt:
            mock_prompt.return_value = {"numeric_choice": "2"}

            result = collector.collect_numeric_choice("옵션을 선택하세요", choices, required=True)

            assert result == "2"

    def test_collect_numeric_choice_optional_skip(self, collector):
        """Test optional numeric choice with skip option."""
        choices = [("첫번째 옵션", "1"), ("두번째 옵션", "2")]
        
        with patch("inquirer.prompt") as mock_prompt:
            mock_prompt.return_value = {"numeric_choice": None}

            result = collector.collect_numeric_choice("옵션을 선택하세요", choices, required=False)

            assert result is None

    def test_collect_numeric_choice_cancelled(self, collector):
        """Test numeric choice collection when user cancels."""
        choices = [("첫번째 옵션", "1"), ("두번째 옵션", "2")]
        
        with patch("inquirer.prompt") as mock_prompt:
            mock_prompt.return_value = None

            result = collector.collect_numeric_choice("옵션을 선택하세요", choices)

            assert result is None

    def test_collect_stock_code_success(self, collector):
        """Test successful stock code collection."""
        with patch("inquirer.prompt") as mock_prompt:
            mock_prompt.return_value = {"stock_code": "005930"}

            result = collector.collect_stock_code("종목코드를 입력하세요", required=True)

            assert result == "005930"

    def test_collect_stock_code_invalid_format(self, collector):
        """Test stock code collection with invalid format."""
        with patch("inquirer.prompt") as mock_prompt, patch.object(collector.console, "print") as mock_print:
            # First call returns invalid format, second call returns valid format
            mock_prompt.side_effect = [
                {"stock_code": "12345"},  # Too short
                {"stock_code": "005930"}
            ]

            result = collector.collect_stock_code("종목코드를 입력하세요", required=True)

            assert result == "005930"
            assert mock_prompt.call_count == 2
            mock_print.assert_called()

    def test_collect_stock_code_non_numeric(self, collector):
        """Test stock code collection with non-numeric input."""
        with patch("inquirer.prompt") as mock_prompt, patch.object(collector.console, "print") as mock_print:
            # First call returns non-numeric, second call returns valid format
            mock_prompt.side_effect = [
                {"stock_code": "ABCD12"},
                {"stock_code": "005930"}
            ]

            result = collector.collect_stock_code("종목코드를 입력하세요", required=True)

            assert result == "005930"
            assert mock_prompt.call_count == 2
            mock_print.assert_called()

    def test_collect_stock_code_optional_empty(self, collector):
        """Test optional stock code with empty value."""
        with patch("inquirer.prompt") as mock_prompt:
            mock_prompt.return_value = {"stock_code": ""}

            result = collector.collect_stock_code("종목코드를 입력하세요", required=False)

            assert result is None

    def test_collect_stock_code_required_empty(self, collector):
        """Test required stock code with empty value."""
        with patch("inquirer.prompt") as mock_prompt, patch.object(collector.console, "print") as mock_print:
            # First call returns empty, second call returns valid code
            mock_prompt.side_effect = [
                {"stock_code": ""},
                {"stock_code": "005930"}
            ]

            result = collector.collect_stock_code("종목코드를 입력하세요", required=True)

            assert result == "005930"
            assert mock_prompt.call_count == 2
            mock_print.assert_called()

    def test_collect_stock_code_cancelled(self, collector):
        """Test stock code collection when user cancels."""
        with patch("inquirer.prompt") as mock_prompt:
            mock_prompt.return_value = None

            result = collector.collect_stock_code("종목코드를 입력하세요")

            assert result is None

    def test_validate_stock_code_valid(self, collector):
        """Test stock code validation with valid codes."""
        valid_codes = ["005930", "000660", "035720", "051910"]
        
        for code in valid_codes:
            assert collector._validate_stock_code(code) is True

    def test_validate_stock_code_invalid(self, collector):
        """Test stock code validation with invalid codes."""
        invalid_codes = [
            "12345",    # Too short
            "1234567",  # Too long
            "ABCD12",   # Contains letters
            "00593A",   # Contains letter
            "",         # Empty
            "005-30",   # Contains dash
        ]
        
        for code in invalid_codes:
            assert collector._validate_stock_code(code) is False
