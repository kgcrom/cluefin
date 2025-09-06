"""
Unit tests for the sector information module.

Tests the sector-specific API configurations and functionality.
"""

from unittest.mock import Mock, patch

import pytest

from cluefin_cli.commands.inquiry.sector_info import SectorInfoModule


class TestSectorInfoModule:
    """Test cases for SectorInfoModule functionality."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock Kiwoom client with sector API methods."""
        client = Mock()
        client.get_industry_investor_net_buy = Mock(return_value={"output": []})
        client.get_industry_current_price = Mock(return_value={"output": []})
        client.get_industry_price_by_sector = Mock(return_value={"output": []})
        client.get_all_industry_index = Mock(return_value={"output": []})
        client.get_daily_industry_current_price = Mock(return_value={"output": []})
        return client

    @pytest.fixture
    def sector_module(self, mock_client):
        """Create a sector info module with mock client."""
        return SectorInfoModule(mock_client)

    def test_initialization(self, mock_client):
        """Test proper initialization of SectorInfoModule."""
        module = SectorInfoModule(mock_client)

        assert module.client == mock_client
        assert module.parameter_collector is not None
        assert module.formatter is not None
        assert module.console is not None

    def test_initialization_without_client(self):
        """Test initialization without providing a client."""
        module = SectorInfoModule()

        assert module.client is None
        assert module.parameter_collector is not None

    def test_get_api_category(self, sector_module):
        """Test API category configuration."""
        category = sector_module.get_api_category()

        assert category.name == "sector_info"
        assert category.korean_name == "🏢 업종정보"
        assert len(category.apis) == 5  # Should have 5 sector APIs

        # Check that all expected APIs are present
        api_names = [api.name for api in category.apis]
        expected_apis = [
            "industry_investor_net_buy",
            "industry_current_price",
            "industry_price_by_sector",
            "all_industry_index",
            "daily_industry_current_price",
        ]

        for expected_api in expected_apis:
            assert expected_api in api_names

    def test_industry_investor_net_buy_config(self, sector_module):
        """Test configuration for industry investor net buy API."""
        category = sector_module.get_api_category()
        api = category.get_api_by_name("industry_investor_net_buy")

        assert api is not None
        assert api.korean_name == "📊 업종별 투자자 순매수 요청"
        assert api.api_method == "get_industry_investor_net_buy"
        assert len(api.required_params) == 4
        assert len(api.optional_params) == 0

        # Check required parameters
        param_names = [param.name for param in api.required_params]
        expected_params = ["mrkt_tp", "amt_qty_tp", "base_dt", "stex_tp"]

        for expected_param in expected_params:
            assert expected_param in param_names

        # Check that base_dt is a date parameter
        base_dt_param = next(p for p in api.required_params if p.name == "base_dt")
        assert base_dt_param.param_type == "date"

    def test_industry_current_price_config(self, sector_module):
        """Test configuration for industry current price API."""
        category = sector_module.get_api_category()
        api = category.get_api_by_name("industry_current_price")

        assert api is not None
        assert api.korean_name == "💰 업종현재가 요청"
        assert api.api_method == "get_industry_current_price"
        assert len(api.required_params) == 2

        # Check industry code validation
        inds_cd_param = next(p for p in api.required_params if p.name == "inds_cd")
        assert inds_cd_param.param_type == "text"
        assert inds_cd_param.validation == r"^\d{3}$"

    def test_industry_price_by_sector_config(self, sector_module):
        """Test configuration for industry price by sector API."""
        category = sector_module.get_api_category()
        api = category.get_api_by_name("industry_price_by_sector")

        assert api is not None
        assert api.korean_name == "📈 업종별 주가요청"
        assert api.api_method == "get_industry_price_by_sector"
        assert len(api.required_params) == 3

    def test_all_industry_index_config(self, sector_module):
        """Test configuration for all industry index API."""
        category = sector_module.get_api_category()
        api = category.get_api_by_name("all_industry_index")

        assert api is not None
        assert api.korean_name == "🌐 전업종 지수요청"
        assert api.api_method == "get_all_industry_index"
        assert len(api.required_params) == 1

        # Check that industry code has comprehensive choices
        inds_cd_param = api.required_params[0]
        assert inds_cd_param.name == "inds_cd"
        assert inds_cd_param.param_type == "select"
        assert len(inds_cd_param.choices) >= 25  # Should have many industry choices

        # Check some specific industry codes
        choice_values = [choice[1] for choice in inds_cd_param.choices]
        assert "001" in choice_values  # KOSPI 종합
        assert "101" in choice_values  # KOSDAQ 종합
        assert "201" in choice_values  # KOSPI200

    def test_daily_industry_current_price_config(self, sector_module):
        """Test configuration for daily industry current price API."""
        category = sector_module.get_api_category()
        api = category.get_api_by_name("daily_industry_current_price")

        assert api is not None
        assert api.korean_name == "📅 업종현재가 일별요청"
        assert api.api_method == "get_daily_industry_current_price"
        assert len(api.required_params) == 2

        # Check parameter types
        param_names = [param.name for param in api.required_params]
        assert "mrkt_tp" in param_names
        assert "inds_cd" in param_names

        # Check market type parameter
        mrkt_tp_param = next(p for p in api.required_params if p.name == "mrkt_tp")
        assert mrkt_tp_param.param_type == "select"

    def test_parameter_choices_validation(self, sector_module):
        """Test that all select parameters have proper choices defined."""
        category = sector_module.get_api_category()

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

    def test_text_parameter_validation(self, sector_module):
        """Test that text parameters have proper validation patterns."""
        category = sector_module.get_api_category()

        for api in category.apis:
            for param in api.get_all_params():
                if param.param_type == "text" and param.validation:
                    # Industry code should be 3 digits
                    if param.name == "inds_cd":
                        assert param.validation == r"^\d{3}$"

    def test_format_and_display_result(self, sector_module):
        """Test result formatting and display."""
        mock_result = {"output": [{"sector_name": "테스트업종", "index": "1000.0"}]}

        category = sector_module.get_api_category()
        api_config = category.get_api_by_name("industry_investor_net_buy")

        with patch.object(sector_module.formatter, "format_sector_data") as mock_format:
            sector_module._format_and_display_result(mock_result, api_config)

            mock_format.assert_called_once_with(mock_result, api_config)

    def test_execute_api_invalid_name(self, sector_module):
        """Test API execution with invalid API name."""
        result = sector_module.execute_api("invalid_api_name")

        assert result is False

    def test_execute_api_cancelled_parameters(self, sector_module):
        """Test API execution when parameter collection is cancelled."""
        with patch.object(sector_module.parameter_collector, "collect_parameters") as mock_collect:
            mock_collect.return_value = None  # User cancelled

            result = sector_module.execute_api("industry_investor_net_buy")

            assert result is False

    @patch("inquirer.prompt")
    def test_show_api_menu(self, mock_prompt, sector_module):
        """Test API menu display."""
        mock_prompt.return_value = {"api_choice": "industry_investor_net_buy"}

        result = sector_module.show_api_menu()

        assert result == "industry_investor_net_buy"
        mock_prompt.assert_called_once()

        # Check that the prompt includes all sector APIs
        call_args = mock_prompt.call_args[0][0][0]
        choices = [choice.value for choice in call_args.choices]

        assert "industry_investor_net_buy" in choices
        assert "industry_current_price" in choices
        assert "back" in choices

    def test_api_method_mapping(self, sector_module):
        """Test that all APIs have correct method mappings."""
        category = sector_module.get_api_category()

        expected_mappings = {
            "industry_investor_net_buy": "get_industry_investor_net_buy",
            "industry_current_price": "get_industry_current_price",
            "industry_price_by_sector": "get_industry_price_by_sector",
            "all_industry_index": "get_all_industry_index",
            "daily_industry_current_price": "get_daily_industry_current_price",
        }

        for api in category.apis:
            expected_method = expected_mappings.get(api.name)
            assert api.api_method == expected_method

    def test_korean_names_and_descriptions(self, sector_module):
        """Test that all APIs have proper Korean names and descriptions."""
        category = sector_module.get_api_category()

        for api in category.apis:
            # Korean name should contain Korean characters
            assert any("\uac00" <= char <= "\ud7af" for char in api.korean_name)

            # Should have description
            assert api.description is not None
            assert len(api.description) > 0

            # All parameters should have Korean names
            for param in api.get_all_params():
                assert any("\uac00" <= char <= "\ud7af" for char in param.korean_name)

    def test_market_type_choices_consistency(self, sector_module):
        """Test that market type choices are consistent across APIs."""
        category = sector_module.get_api_category()

        # Find all market type parameters
        market_type_choices = []
        for api in category.apis:
            for param in api.get_all_params():
                if param.name == "mrkt_tp":
                    market_type_choices.append(param.choices)

        # Most should have similar choices (some may have additional options like KOSPI200)
        assert len(market_type_choices) > 0

        # All should include basic KOSPI and KOSDAQ options
        for choices in market_type_choices:
            choice_values = [choice[1] for choice in choices]
            assert "0" in choice_values  # KOSPI
            assert "1" in choice_values  # KOSDAQ

    def test_industry_code_parameter_types(self, sector_module):
        """Test that industry code parameters have appropriate types."""
        category = sector_module.get_api_category()

        for api in category.apis:
            for param in api.get_all_params():
                if param.name == "inds_cd":
                    # Should be either select (with predefined choices) or text (with validation)
                    assert param.param_type in ["select", "text"]

                    if param.param_type == "text":
                        assert param.validation is not None
                    elif param.param_type == "select":
                        assert param.choices is not None
                        assert len(param.choices) > 0
