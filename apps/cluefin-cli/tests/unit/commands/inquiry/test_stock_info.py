"""
Unit tests for the stock information module.

Tests the stock-specific API configurations and functionality.
"""

from unittest.mock import Mock, patch

import pytest

from cluefin_cli.commands.inquiry.stock_info import StockInfoModule


class TestStockInfoModule:
    """Test cases for StockInfoModule functionality."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock Kiwoom client with stock API methods."""
        client = Mock()
        # Create nested structure to match actual client attribute access
        client.stock_info = Mock()
        client.stock_info.get_trading_volume_renewal = Mock(return_value={"output": []})
        client.stock_info.get_supply_demand_concentration = Mock(return_value={"output": []})
        client.stock_info.get_trading_member_supply_demand_analysis = Mock(return_value={"output": []})
        client.stock_info.get_total_institutional_investor_by_stock = Mock(return_value={"output": []})
        client.stock_info.get_stock_info = Mock(return_value={"output": []})
        return client

    @pytest.fixture
    def stock_module(self, mock_client):
        """Create a stock info module with mock client."""
        return StockInfoModule(mock_client)

    def test_initialization(self, mock_client):
        """Test proper initialization of StockInfoModule."""
        module = StockInfoModule(mock_client)

        assert module.client == mock_client
        assert module.parameter_collector is not None
        assert module.formatter is not None
        assert module.console is not None

    def test_initialization_without_client(self):
        """Test initialization without providing a client."""
        module = StockInfoModule()

        assert module.client is None
        assert module.parameter_collector is not None

    def test_get_api_category(self, stock_module: StockInfoModule):
        """Test API category configuration."""
        category = stock_module.get_api_category()

        assert category.name == "stock_info"
        assert category.korean_name == "💰 종목정보"
        assert len(category.apis) == 5  # Should have 5 stock APIs

        # Check that all expected APIs are present
        api_names = [api.name for api in category.apis]
        expected_apis = [
            "trading_volume_renewal",
            "supply_demand_concentration",
            "trading_member_supply_demand_analysis",
            "total_institutional_investor_by_stock",
            "stock_info",
        ]

        for expected_api in expected_apis:
            assert expected_api in api_names

    def test_trading_volume_renewal_config(self, stock_module: StockInfoModule):
        """Test configuration for trading volume renewal API."""
        category = stock_module.get_api_category()
        api = category.get_api_by_name("trading_volume_renewal")

        assert api is not None
        assert api.korean_name == "📈 거래량갱신요청"
        assert api.api_method == "get_trading_volume_renewal"
        assert len(api.required_params) == 4
        assert len(api.optional_params) == 0

        # Check stock code parameter
        stk_cd_param = api.required_params[0]
        assert stk_cd_param.name == "mrkt_tp"
        assert stk_cd_param.param_type == "select"
        assert stk_cd_param.validation is None

    def test_supply_demand_concentration_config(self, stock_module: StockInfoModule):
        """Test configuration for supply demand concentration API."""
        category = stock_module.get_api_category()
        api = category.get_api_by_name("supply_demand_concentration")

        assert api is not None
        assert api.korean_name == "💹 매물대집중요청"
        assert api.api_method == "get_supply_demand_concentration"
        assert len(api.required_params) == 6

        # Check parameters
        param_names = [param.name for param in api.required_params]
        assert "mrkt_tp" in param_names
        assert "prpscnt" in param_names

        # Check current price entry parameter choices
        cur_prc_param = next(p for p in api.required_params if p.name == "cur_prc_entry")
        assert cur_prc_param.param_type == "select"
        assert cur_prc_param.choices is not None
        assert len(cur_prc_param.choices) == 2
        choice_values = [choice[1] for choice in cur_prc_param.choices]
        assert "0" in choice_values  # 포함안함
        assert "1" in choice_values  # 포함

    def test_trading_member_supply_demand_analysis_config(self, stock_module: StockInfoModule):
        """Test configuration for broker supply demand analysis API."""
        category = stock_module.get_api_category()
        api = category.get_api_by_name("trading_member_supply_demand_analysis")

        assert api is not None
        assert api.korean_name == "🏢 거래원매물대분석요청"
        assert api.api_method == "get_trading_member_supply_demand_analysis"
        assert len(api.required_params) == 9

    def test_stock_info_config(self, stock_module: StockInfoModule):
        """Test configuration for stock basic info API."""
        category = stock_module.get_api_category()
        api = category.get_api_by_name("stock_info")

        assert api is not None
        assert api.korean_name == "📊 주식기본정보요청"
        assert api.api_method == "get_stock_info"
        assert len(api.required_params) == 1

    def test_stock_code_validation(self, stock_module: StockInfoModule):
        """Test that all stock code parameters have proper validation."""
        category = stock_module.get_api_category()

        for api in category.apis:
            for param in api.get_all_params():
                if param.name == "stk_cd":
                    assert param.param_type == "text"
                    assert param.validation == r"^\d{6}$"

    def test_parameter_choices_validation(self, stock_module: StockInfoModule):
        """Test that all select parameters have proper choices defined."""
        category = stock_module.get_api_category()

        for api in category.apis:
            for param in api.get_all_params():
                if param.param_type == "select":
                    assert param.choices is not None
                    assert len(param.choices) > 0

                    # Each choice should be a tuple of (label, value)
                    for choice in param.choices:
                        assert isinstance(choice, tuple)
                        assert len(choice) == 2
                        assert isinstance(choice[0], str)  # Korean label
                        assert isinstance(choice[1], str)  # Value

    def test_format_and_display_result(self, stock_module: StockInfoModule):
        """Test result formatting and display."""
        mock_result = {"output": [{"stock_name": "삼성전자", "price": "70000"}]}

        category = stock_module.get_api_category()
        api_config = category.get_api_by_name("trading_volume_renewal")

        assert api_config is not None

        with patch.object(stock_module.formatter, "format_stock_data") as mock_format:
            stock_module._format_and_display_result(mock_result, api_config)

            mock_format.assert_called_once_with(mock_result, api_config)

    def test_execute_api_success(self, stock_module: StockInfoModule, mock_client):
        """Test successful API execution."""
        # Mock parameter collection
        with patch.object(stock_module.parameter_collector, "collect_parameters") as mock_collect:
            mock_collect.return_value = {"stk_cd": "005930"}

            # Mock result formatting
            with patch.object(stock_module, "_format_and_display_result") as mock_format:
                result = stock_module.execute_api("trading_volume_renewal")

                assert result is True
                mock_client.stock_info.get_trading_volume_renewal.assert_called_once()
                mock_format.assert_called_once()

    def test_execute_api_with_multiple_parameters(self, stock_module: StockInfoModule, mock_client):
        """Test API execution with multiple parameters."""
        with patch.object(stock_module.parameter_collector, "collect_parameters") as mock_collect:
            mock_collect.return_value = {"stk_cd": "005930", "prc_tp": "1"}

            with patch.object(stock_module, "_format_and_display_result"):
                result = stock_module.execute_api("supply_demand_concentration")

                assert result is True
                # Verify parameters were passed
                call_args = mock_client.stock_info.get_supply_demand_concentration.call_args
                assert call_args[1]["stk_cd"] == "005930"

    def test_execute_api_invalid_name(self, stock_module: StockInfoModule):
        """Test API execution with invalid API name."""
        result = stock_module.execute_api("invalid_api_name")

        assert result is False

    def test_execute_api_cancelled_parameters(self, stock_module: StockInfoModule):
        """Test API execution when parameter collection is cancelled."""
        with patch.object(stock_module.parameter_collector, "collect_parameters") as mock_collect:
            mock_collect.return_value = None  # User cancelled

            result = stock_module.execute_api("trading_volume_renewal")

            assert result is False

    @patch("inquirer.prompt")
    def test_show_api_menu(self, mock_prompt, stock_module):
        """Test API menu display."""
        mock_prompt.return_value = {"api_choice": "trading_volume_renewal"}

        result = stock_module.show_api_menu()

        assert result == "trading_volume_renewal"
        mock_prompt.assert_called_once()

        # Check that the prompt includes all stock APIs
        call_args = mock_prompt.call_args[0][0][0]
        choices = [choice.value for choice in call_args.choices]

        assert "trading_volume_renewal" in choices
        assert "supply_demand_concentration" in choices
        assert "back" in choices

    def test_api_method_mapping(self, stock_module: StockInfoModule):
        """Test that all APIs have correct method mappings."""
        category = stock_module.get_api_category()

        expected_mappings = {
            "trading_volume_renewal": "get_trading_volume_renewal",
            "supply_demand_concentration": "get_supply_demand_concentration",
            "broker_supply_demand_analysis": "get_broker_supply_demand_analysis",
            "stock_investor_institutional_total": "get_stock_investor_institutional_total",
            "stock_info": "get_stock_info",
            "total_institutional_investor_by_stock": "get_total_institutional_investor_by_stock",
            "trading_member_supply_demand_analysis": "get_trading_member_supply_demand_analysis",
        }

        for api in category.apis:
            expected_method = expected_mappings.get(api.name)
            assert api.api_method == expected_method

    def test_korean_names_and_descriptions(self, stock_module: StockInfoModule):
        """Test that all APIs have proper Korean names and descriptions."""
        category = stock_module.get_api_category()

        for api in category.apis:
            # Korean name should contain Korean characters
            assert any("\uac00" <= char <= "\ud7af" for char in api.korean_name)

            # Should have description
            assert api.description is not None
            assert len(api.description) > 0

            # All parameters should have Korean names
            for param in api.get_all_params():
                assert any("\uac00" <= char <= "\ud7af" for char in param.korean_name)

    def test_stock_code_consistency(self, stock_module: StockInfoModule):
        """Test that APIs have either market type or stock code parameters consistently."""
        category = stock_module.get_api_category()

        # APIs should have either mrkt_tp or stk_cd parameters
        for api in category.apis:
            mrkt_tp_params = [p for p in api.get_all_params() if p.name == "mrkt_tp"]
            stk_cd_params = [p for p in api.get_all_params() if p.name == "stk_cd"]

            # Each API should have either market type OR stock code parameter
            assert len(mrkt_tp_params) + len(stk_cd_params) >= 1

            # Check mrkt_tp parameter consistency if present
            if mrkt_tp_params:
                mrkt_tp_param = mrkt_tp_params[0]
                assert mrkt_tp_param.param_type == "select"
                assert mrkt_tp_param.korean_name == "시장구분"

            # Check stk_cd parameter consistency if present
            if stk_cd_params:
                stk_cd_param = stk_cd_params[0]
                assert stk_cd_param.param_type == "text"
                assert stk_cd_param.korean_name == "종목코드"
                assert stk_cd_param.validation == r"^\d{6}$"

    def test_date_parameter_types(self, stock_module: StockInfoModule):
        """Test that date parameters have correct types."""
        category = stock_module.get_api_category()

        for api in category.apis:
            for param in api.get_all_params():
                if param.name in ["strt_dt", "end_dt"]:
                    assert param.param_type == "date"
