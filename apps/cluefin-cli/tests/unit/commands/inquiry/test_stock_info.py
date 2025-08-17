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
        client.get_trading_volume_renewal = Mock(return_value={"output": []})
        client.get_supply_demand_concentration = Mock(return_value={"output": []})
        client.get_broker_supply_demand_analysis = Mock(return_value={"output": []})
        client.get_stock_investor_institutional_total = Mock(return_value={"output": []})
        client.get_stock_basic_info = Mock(return_value={"output": []})
        client.get_stock_price_info = Mock(return_value={"output": []})
        client.get_stock_order_book = Mock(return_value={"output": []})
        client.get_stock_daily_chart = Mock(return_value={"output": []})
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

    def test_get_api_category(self, stock_module):
        """Test API category configuration."""
        category = stock_module.get_api_category()
        
        assert category.name == "stock_info"
        assert category.korean_name == "💰 종목정보"
        assert len(category.apis) == 8  # Should have 8 stock APIs
        
        # Check that all expected APIs are present
        api_names = [api.name for api in category.apis]
        expected_apis = [
            "trading_volume_renewal",
            "supply_demand_concentration",
            "broker_supply_demand_analysis",
            "stock_investor_institutional_total",
            "stock_basic_info",
            "stock_price_info",
            "stock_order_book",
            "stock_daily_chart"
        ]
        
        for expected_api in expected_apis:
            assert expected_api in api_names

    def test_trading_volume_renewal_config(self, stock_module):
        """Test configuration for trading volume renewal API."""
        category = stock_module.get_api_category()
        api = category.get_api_by_name("trading_volume_renewal")
        
        assert api is not None
        assert api.korean_name == "📈 거래량갱신요청"
        assert api.api_method == "get_trading_volume_renewal"
        assert len(api.required_params) == 1
        assert len(api.optional_params) == 0
        
        # Check stock code parameter
        stk_cd_param = api.required_params[0]
        assert stk_cd_param.name == "stk_cd"
        assert stk_cd_param.param_type == "text"
        assert stk_cd_param.validation == r"^\d{6}$"

    def test_supply_demand_concentration_config(self, stock_module):
        """Test configuration for supply demand concentration API."""
        category = stock_module.get_api_category()
        api = category.get_api_by_name("supply_demand_concentration")
        
        assert api is not None
        assert api.korean_name == "💹 매출대집중요청"
        assert api.api_method == "get_supply_demand_concentration"
        assert len(api.required_params) == 2
        
        # Check parameters
        param_names = [param.name for param in api.required_params]
        assert "stk_cd" in param_names
        assert "prc_tp" in param_names
        
        # Check price type parameter choices
        prc_tp_param = next(p for p in api.required_params if p.name == "prc_tp")
        assert prc_tp_param.param_type == "select"
        assert len(prc_tp_param.choices) == 2
        choice_values = [choice[1] for choice in prc_tp_param.choices]
        assert "1" in choice_values  # 매도호가
        assert "2" in choice_values  # 매수호가

    def test_broker_supply_demand_analysis_config(self, stock_module):
        """Test configuration for broker supply demand analysis API."""
        category = stock_module.get_api_category()
        api = category.get_api_by_name("broker_supply_demand_analysis")
        
        assert api is not None
        assert api.korean_name == "🏢 거래원매물대분석요청"
        assert api.api_method == "get_broker_supply_demand_analysis"
        assert len(api.required_params) == 1
        
        # Should only require stock code
        assert api.required_params[0].name == "stk_cd"

    def test_stock_investor_institutional_total_config(self, stock_module):
        """Test configuration for stock investor institutional total API."""
        category = stock_module.get_api_category()
        api = category.get_api_by_name("stock_investor_institutional_total")
        
        assert api is not None
        assert api.korean_name == "👥 종목별투자자기관별합계요청"
        assert api.api_method == "get_stock_investor_institutional_total"
        assert len(api.required_params) == 2
        
        # Check trading date parameter
        trd_dt_param = next(p for p in api.required_params if p.name == "trd_dt")
        assert trd_dt_param.param_type == "select"
        choice_values = [choice[1] for choice in trd_dt_param.choices]
        assert "0" in choice_values  # 당일
        assert "1" in choice_values  # 전일

    def test_stock_basic_info_config(self, stock_module):
        """Test configuration for stock basic info API."""
        category = stock_module.get_api_category()
        api = category.get_api_by_name("stock_basic_info")
        
        assert api is not None
        assert api.korean_name == "📊 종목기본정보요청"
        assert api.api_method == "get_stock_basic_info"
        assert len(api.required_params) == 1

    def test_stock_price_info_config(self, stock_module):
        """Test configuration for stock price info API."""
        category = stock_module.get_api_category()
        api = category.get_api_by_name("stock_price_info")
        
        assert api is not None
        assert api.korean_name == "💲 종목현재가정보요청"
        assert api.api_method == "get_stock_price_info"
        assert len(api.required_params) == 1

    def test_stock_order_book_config(self, stock_module):
        """Test configuration for stock order book API."""
        category = stock_module.get_api_category()
        api = category.get_api_by_name("stock_order_book")
        
        assert api is not None
        assert api.korean_name == "📋 종목호가정보요청"
        assert api.api_method == "get_stock_order_book"
        assert len(api.required_params) == 1

    def test_stock_daily_chart_config(self, stock_module):
        """Test configuration for stock daily chart API."""
        category = stock_module.get_api_category()
        api = category.get_api_by_name("stock_daily_chart")
        
        assert api is not None
        assert api.korean_name == "📈 종목일봉차트요청"
        assert api.api_method == "get_stock_daily_chart"
        assert len(api.required_params) == 3
        assert len(api.optional_params) == 1
        
        # Check date parameters
        param_names = [param.name for param in api.required_params]
        assert "stk_cd" in param_names
        assert "strt_dt" in param_names
        assert "end_dt" in param_names
        
        # Check date parameter types
        strt_dt_param = next(p for p in api.required_params if p.name == "strt_dt")
        end_dt_param = next(p for p in api.required_params if p.name == "end_dt")
        assert strt_dt_param.param_type == "date"
        assert end_dt_param.param_type == "date"
        
        # Check optional parameter
        adj_prc_param = api.optional_params[0]
        assert adj_prc_param.name == "adj_prc_tp"
        assert adj_prc_param.required is False

    def test_stock_code_validation(self, stock_module):
        """Test that all stock code parameters have proper validation."""
        category = stock_module.get_api_category()
        
        for api in category.apis:
            for param in api.get_all_params():
                if param.name == "stk_cd":
                    assert param.param_type == "text"
                    assert param.validation == r"^\d{6}$"

    def test_parameter_choices_validation(self, stock_module):
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

    def test_format_and_display_result(self, stock_module):
        """Test result formatting and display."""
        mock_result = {"output": [{"stock_name": "삼성전자", "price": "70000"}]}
        
        category = stock_module.get_api_category()
        api_config = category.get_api_by_name("trading_volume_renewal")
        
        with patch.object(stock_module.formatter, 'format_stock_data') as mock_format:
            stock_module._format_and_display_result(mock_result, api_config)
            
            mock_format.assert_called_once_with(mock_result, api_config.korean_name)

    def test_execute_api_success(self, stock_module, mock_client):
        """Test successful API execution."""
        # Mock parameter collection
        with patch.object(stock_module.parameter_collector, 'collect_parameters') as mock_collect:
            mock_collect.return_value = {"stk_cd": "005930"}
            
            # Mock result formatting
            with patch.object(stock_module, '_format_and_display_result') as mock_format:
                result = stock_module.execute_api("trading_volume_renewal")
                
                assert result is True
                mock_client.get_trading_volume_renewal.assert_called_once()
                mock_format.assert_called_once()

    def test_execute_api_with_multiple_parameters(self, stock_module, mock_client):
        """Test API execution with multiple parameters."""
        with patch.object(stock_module.parameter_collector, 'collect_parameters') as mock_collect:
            mock_collect.return_value = {
                "stk_cd": "005930",
                "prc_tp": "1"
            }
            
            with patch.object(stock_module, '_format_and_display_result'):
                result = stock_module.execute_api("supply_demand_concentration")
                
                assert result is True
                # Verify parameters were passed
                call_args = mock_client.get_supply_demand_concentration.call_args
                assert call_args[1]["stk_cd"] == "005930"
                assert call_args[1]["prc_tp"] == "1"

    def test_execute_api_with_date_parameters(self, stock_module, mock_client):
        """Test API execution with date parameters."""
        with patch.object(stock_module.parameter_collector, 'collect_parameters') as mock_collect:
            mock_collect.return_value = {
                "stk_cd": "005930",
                "strt_dt": "20240101",
                "end_dt": "20240131"
            }
            
            with patch.object(stock_module, '_format_and_display_result'):
                result = stock_module.execute_api("stock_daily_chart")
                
                assert result is True
                # Verify date parameters were passed
                call_args = mock_client.get_stock_daily_chart.call_args
                assert call_args[1]["strt_dt"] == "20240101"
                assert call_args[1]["end_dt"] == "20240131"

    def test_execute_api_with_optional_parameters(self, stock_module, mock_client):
        """Test API execution with optional parameters."""
        with patch.object(stock_module.parameter_collector, 'collect_parameters') as mock_collect:
            mock_collect.return_value = {
                "stk_cd": "005930",
                "strt_dt": "20240101",
                "end_dt": "20240131",
                "adj_prc_tp": "1"  # Optional parameter
            }
            
            with patch.object(stock_module, '_format_and_display_result'):
                result = stock_module.execute_api("stock_daily_chart")
                
                assert result is True
                # Verify optional parameter was passed
                call_args = mock_client.get_stock_daily_chart.call_args
                assert call_args[1]["adj_prc_tp"] == "1"

    def test_execute_api_invalid_name(self, stock_module):
        """Test API execution with invalid API name."""
        result = stock_module.execute_api("invalid_api_name")
        
        assert result is False

    def test_execute_api_cancelled_parameters(self, stock_module):
        """Test API execution when parameter collection is cancelled."""
        with patch.object(stock_module.parameter_collector, 'collect_parameters') as mock_collect:
            mock_collect.return_value = None  # User cancelled
            
            result = stock_module.execute_api("trading_volume_renewal")
            
            assert result is False

    @patch('inquirer.prompt')
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

    def test_api_method_mapping(self, stock_module):
        """Test that all APIs have correct method mappings."""
        category = stock_module.get_api_category()
        
        expected_mappings = {
            "trading_volume_renewal": "get_trading_volume_renewal",
            "supply_demand_concentration": "get_supply_demand_concentration",
            "broker_supply_demand_analysis": "get_broker_supply_demand_analysis",
            "stock_investor_institutional_total": "get_stock_investor_institutional_total",
            "stock_basic_info": "get_stock_basic_info",
            "stock_price_info": "get_stock_price_info",
            "stock_order_book": "get_stock_order_book",
            "stock_daily_chart": "get_stock_daily_chart"
        }
        
        for api in category.apis:
            expected_method = expected_mappings.get(api.name)
            assert api.api_method == expected_method

    def test_korean_names_and_descriptions(self, stock_module):
        """Test that all APIs have proper Korean names and descriptions."""
        category = stock_module.get_api_category()
        
        for api in category.apis:
            # Korean name should contain Korean characters
            assert any('\uac00' <= char <= '\ud7af' for char in api.korean_name)
            
            # Should have description
            assert api.description is not None
            assert len(api.description) > 0
            
            # All parameters should have Korean names
            for param in api.get_all_params():
                assert any('\uac00' <= char <= '\ud7af' for char in param.korean_name)

    def test_stock_code_consistency(self, stock_module):
        """Test that stock code parameters are consistent across APIs."""
        category = stock_module.get_api_category()
        
        # All APIs should have stock code parameter with same validation
        for api in category.apis:
            stk_cd_params = [p for p in api.get_all_params() if p.name == "stk_cd"]
            assert len(stk_cd_params) == 1  # Each API should have exactly one stock code param
            
            stk_cd_param = stk_cd_params[0]
            assert stk_cd_param.param_type == "text"
            assert stk_cd_param.validation == r"^\d{6}$"
            assert stk_cd_param.korean_name == "종목코드"

    def test_date_parameter_types(self, stock_module):
        """Test that date parameters have correct types."""
        category = stock_module.get_api_category()
        
        for api in category.apis:
            for param in api.get_all_params():
                if param.name in ["strt_dt", "end_dt"]:
                    assert param.param_type == "date"


class TestStockInfoModuleIntegration:
    """Integration tests for StockInfoModule."""

    @pytest.fixture
    def integration_module(self):
        """Create a module for integration testing."""
        return StockInfoModule()

    def test_full_menu_flow(self, integration_module):
        """Test the complete menu flow."""
        mock_client = Mock()
        mock_client.get_trading_volume_renewal = Mock(
            return_value={"output": [{"stock_name": "삼성전자", "volume": "1000000"}]}
        )
        integration_module.set_client(mock_client)
        
        # Mock menu selection and parameter collection
        with patch('inquirer.prompt') as mock_prompt:
            mock_prompt.side_effect = [
                {"api_choice": "trading_volume_renewal"},  # API selection
                {"api_choice": "back"}  # Go back
            ]
            
            with patch.object(integration_module.parameter_collector, 'collect_parameters') as mock_collect:
                mock_collect.return_value = {"stk_cd": "005930"}
                
                with patch('builtins.input'):  # Mock pause input
                    integration_module.handle_menu_loop()
                
                # Verify API was called
                mock_client.get_trading_volume_renewal.assert_called_once()

    def test_client_status(self, integration_module):
        """Test client status reporting."""
        # Without client
        status = integration_module.get_client_status()
        assert status["client_initialized"] is False
        
        # With client
        mock_client = Mock()
        integration_module.set_client(mock_client)
        
        status = integration_module.get_client_status()
        assert status["client_initialized"] is True
        assert status["client_type"] == "Mock"

    def test_stock_code_validation_integration(self, integration_module):
        """Test stock code validation in integration context."""
        mock_client = Mock()
        mock_client.get_stock_basic_info = Mock(return_value={"output": []})
        integration_module.set_client(mock_client)
        
        # Test with valid stock code
        with patch.object(integration_module.parameter_collector, 'collect_parameters') as mock_collect:
            mock_collect.return_value = {"stk_cd": "005930"}  # Valid 6-digit code
            
            result = integration_module.execute_api("stock_basic_info")
            
            assert result is True
            mock_client.get_stock_basic_info.assert_called_once_with(stk_cd="005930")

    def test_chart_data_with_date_range(self, integration_module):
        """Test chart data API with date range parameters."""
        mock_client = Mock()
        mock_client.get_stock_daily_chart = Mock(return_value={"output": []})
        integration_module.set_client(mock_client)
        
        # Test with date range and optional parameter
        with patch.object(integration_module.parameter_collector, 'collect_parameters') as mock_collect:
            mock_collect.return_value = {
                "stk_cd": "005930",
                "strt_dt": "20240101",
                "end_dt": "20240131",
                "adj_prc_tp": "1"
            }
            
            result = integration_module.execute_api("stock_daily_chart")
            
            assert result is True
            mock_client.get_stock_daily_chart.assert_called_once_with(
                stk_cd="005930", strt_dt="20240101", end_dt="20240131", adj_prc_tp="1"
            )