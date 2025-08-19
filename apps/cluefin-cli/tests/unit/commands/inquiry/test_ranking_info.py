"""
Unit tests for the ranking information module.

Tests the ranking-specific API configurations and functionality.
"""

from unittest.mock import Mock, patch

import pytest

from cluefin_cli.commands.inquiry.ranking_info import RankingInfoModule


class TestRankingInfoModule:
    """Test cases for RankingInfoModule functionality."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock Kiwoom client with ranking API methods."""
        client = Mock()
        client.get_rapidly_increasing_trading_volume = Mock(return_value={"output": []})
        client.get_top_current_day_trading_volume = Mock(return_value={"output": []})
        client.get_previous_day_trading_volume_top = Mock(return_value={"output": []})
        client.get_trading_value_top = Mock(return_value={"output": []})
        client.get_foreign_period_trading_top = Mock(return_value={"output": []})
        client.get_foreign_consecutive_trading_top = Mock(return_value={"output": []})
        client.get_foreign_institutional_trading_top = Mock(return_value={"output": []})
        return client

    @pytest.fixture
    def ranking_module(self, mock_client):
        """Create a ranking info module with mock client."""
        return RankingInfoModule(mock_client)

    def test_initialization(self, mock_client):
        """Test proper initialization of RankingInfoModule."""
        module = RankingInfoModule(mock_client)

        assert module.client == mock_client
        assert module.parameter_collector is not None
        assert module.formatter is not None
        assert module.console is not None

    def test_initialization_without_client(self):
        """Test initialization without providing a client."""
        module = RankingInfoModule()

        assert module.client is None
        assert module.parameter_collector is not None

    def test_get_api_category(self, ranking_module):
        """Test API category configuration."""
        category = ranking_module.get_api_category()

        assert category.name == "ranking_info"
        assert category.korean_name == "📈 순위정보"
        assert len(category.apis) == 7  # Should have 7 ranking APIs

        # Check that all expected APIs are present
        api_names = [api.name for api in category.apis]
        expected_apis = [
            "rapidly_increasing_trading_volume",
            "current_day_trading_volume_top",
            "previous_day_trading_volume_top",
            "trading_value_top",
            "foreign_period_trading_top",
            "foreign_consecutive_trading_top",
            "foreign_institutional_trading_top",
        ]

        for expected_api in expected_apis:
            assert expected_api in api_names

    def test_rapidly_increasing_trading_volume_config(self, ranking_module):
        """Test configuration for rapidly increasing trading volume API."""
        category = ranking_module.get_api_category()
        api = category.get_api_by_name("rapidly_increasing_trading_volume")

        assert api is not None
        assert api.korean_name == "🚀 거래량급증요청"
        assert api.api_method == "get_rapidly_increasing_trading_volume"
        assert len(api.required_params) == 7
        assert len(api.optional_params) == 1

        # Check required parameters
        param_names = [param.name for param in api.required_params]
        expected_params = ["mrkt_tp", "sort_tp", "tm_tp", "trde_qty_tp", "stk_cnd", "pric_tp", "stex_tp"]

        for expected_param in expected_params:
            assert expected_param in param_names

        # Check optional parameter
        assert api.optional_params[0].name == "tm"
        assert api.optional_params[0].required is False

    def test_current_day_trading_volume_config(self, ranking_module):
        """Test configuration for current day trading volume API."""
        category = ranking_module.get_api_category()
        api = category.get_api_by_name("current_day_trading_volume_top")

        assert api is not None
        assert api.korean_name == "📊 당일거래량상위요청"
        assert api.api_method == "get_current_day_trading_volume_top"
        assert len(api.required_params) == 8
        assert len(api.optional_params) == 0

    def test_previous_day_trading_volume_config(self, ranking_module):
        """Test configuration for previous day trading volume API."""
        category = ranking_module.get_api_category()
        api = category.get_api_by_name("previous_day_trading_volume_top")

        assert api is not None
        assert api.korean_name == "📉 전일거래량상위요청"
        assert api.api_method == "get_previous_day_trading_volume_top"

        # Check that rank parameters have proper validation
        rank_start_param = None
        rank_end_param = None

        for param in api.required_params:
            if param.name == "rank_strt":
                rank_start_param = param
            elif param.name == "rank_end":
                rank_end_param = param

        assert rank_start_param is not None
        assert rank_end_param is not None
        assert rank_start_param.validation == r"^[0-9]{1,3}$"
        assert rank_end_param.validation == r"^[0-9]{1,3}$"

    def test_trading_value_top_config(self, ranking_module):
        """Test configuration for trading value top API."""
        category = ranking_module.get_api_category()
        api = category.get_api_by_name("trading_value_top")

        assert api is not None
        assert api.korean_name == "💵 거래대금상위요청"
        assert api.api_method == "get_trading_value_top"
        assert len(api.required_params) == 3

    def test_foreign_period_trading_config(self, ranking_module):
        """Test configuration for foreign period trading API."""
        category = ranking_module.get_api_category()
        api = category.get_api_by_name("foreign_period_trading_top")

        assert api is not None
        assert api.korean_name == "🌍 외인기간별매매상위요청"
        assert api.api_method == "get_foreign_period_trading_top"
        assert len(api.required_params) == 4

    def test_foreign_consecutive_trading_config(self, ranking_module):
        """Test configuration for foreign consecutive trading API."""
        category = ranking_module.get_api_category()
        api = category.get_api_by_name("foreign_consecutive_trading_top")

        assert api is not None
        assert api.korean_name == "🔄 외인연속순매매상위요청"
        assert api.api_method == "get_foreign_consecutive_trading_top"
        assert len(api.required_params) == 4

    def test_foreign_institutional_trading_config(self, ranking_module):
        """Test configuration for foreign institutional trading API."""
        category = ranking_module.get_api_category()
        api = category.get_api_by_name("foreign_institutional_trading_top")

        assert api is not None
        assert api.korean_name == "🏛️ 외국인기관매매상위요청"
        assert api.api_method == "get_foreign_institutional_trading_top"
        assert len(api.required_params) == 5

    def test_parameter_choices_validation(self, ranking_module):
        """Test that all select parameters have proper choices defined."""
        category = ranking_module.get_api_category()

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

    def test_format_and_display_result(self, ranking_module):
        """Test result formatting and display."""
        mock_result = {"output": [{"stock_name": "테스트주식", "price": "10000"}]}

        category = ranking_module.get_api_category()
        api_config = category.get_api_by_name("rapidly_increasing_trading_volume")

        with patch.object(ranking_module.formatter, "format_ranking_data") as mock_format:
            ranking_module._format_and_display_result(mock_result, api_config)

            mock_format.assert_called_once_with(mock_result, api_config.korean_name)

    def test_execute_api_success(self, ranking_module, mock_client):
        """Test successful API execution."""
        # Mock parameter collection
        with patch.object(ranking_module.parameter_collector, "collect_parameters") as mock_collect:
            mock_collect.return_value = {
                "mrkt_tp": "001",
                "sort_tp": "1",
                "tm_tp": "1",
                "trde_qty_tp": "10",
                "stk_cnd": "0",
                "pric_tp": "0",
                "stex_tp": "1",
            }

            # Mock result formatting
            with patch.object(ranking_module, "_format_and_display_result") as mock_format:
                result = ranking_module.execute_api("rapidly_increasing_trading_volume")

                assert result is True
                mock_client.get_rapidly_increasing_trading_volume.assert_called_once()
                mock_format.assert_called_once()

    def test_execute_api_with_optional_parameters(self, ranking_module, mock_client):
        """Test API execution with optional parameters."""
        with patch.object(ranking_module.parameter_collector, "collect_parameters") as mock_collect:
            mock_collect.return_value = {
                "mrkt_tp": "001",
                "sort_tp": "1",
                "tm_tp": "1",
                "trde_qty_tp": "10",
                "stk_cnd": "0",
                "pric_tp": "0",
                "stex_tp": "1",
                "tm": "30",  # Optional parameter
            }

            with patch.object(ranking_module, "_format_and_display_result"):
                result = ranking_module.execute_api("rapidly_increasing_trading_volume")

                assert result is True
                # Verify optional parameter was passed
                call_args = mock_client.get_rapidly_increasing_trading_volume.call_args
                assert call_args[1]["tm"] == "30"

    def test_execute_api_invalid_name(self, ranking_module):
        """Test API execution with invalid API name."""
        result = ranking_module.execute_api("invalid_api_name")

        assert result is False

    def test_execute_api_cancelled_parameters(self, ranking_module):
        """Test API execution when parameter collection is cancelled."""
        with patch.object(ranking_module.parameter_collector, "collect_parameters") as mock_collect:
            mock_collect.return_value = None  # User cancelled

            result = ranking_module.execute_api("rapidly_increasing_trading_volume")

            assert result is False

    @patch("inquirer.prompt")
    def test_show_api_menu(self, mock_prompt, ranking_module):
        """Test API menu display."""
        mock_prompt.return_value = {"api_choice": "rapidly_increasing_trading_volume"}

        result = ranking_module.show_api_menu()

        assert result == "rapidly_increasing_trading_volume"
        mock_prompt.assert_called_once()

        # Check that the prompt includes all ranking APIs
        call_args = mock_prompt.call_args[0][0][0]
        choices = [choice.value for choice in call_args.choices]

        assert "rapidly_increasing_trading_volume" in choices
        assert "current_day_trading_volume_top" in choices
        assert "back" in choices

    def test_api_method_mapping(self, ranking_module):
        """Test that all APIs have correct method mappings."""
        category = ranking_module.get_api_category()

        expected_mappings = {
            "rapidly_increasing_trading_volume": "get_rapidly_increasing_trading_volume",
            "current_day_trading_volume_top": "get_current_day_trading_volume_top",
            "previous_day_trading_volume_top": "get_previous_day_trading_volume_top",
            "trading_value_top": "get_trading_value_top",
            "foreign_period_trading_top": "get_foreign_period_trading_top",
            "foreign_consecutive_trading_top": "get_foreign_consecutive_trading_top",
            "foreign_institutional_trading_top": "get_foreign_institutional_trading_top",
        }

        for api in category.apis:
            expected_method = expected_mappings.get(api.name)
            assert api.api_method == expected_method

    def test_korean_names_and_descriptions(self, ranking_module):
        """Test that all APIs have proper Korean names and descriptions."""
        category = ranking_module.get_api_category()

        for api in category.apis:
            # Korean name should contain Korean characters
            assert any("\uac00" <= char <= "\ud7af" for char in api.korean_name)

            # Should have description
            assert api.description is not None
            assert len(api.description) > 0

            # All parameters should have Korean names
            for param in api.get_all_params():
                assert any("\uac00" <= char <= "\ud7af" for char in param.korean_name)


class TestRankingInfoModuleIntegration:
    """Integration tests for RankingInfoModule."""

    @pytest.fixture
    def integration_module(self):
        """Create a module for integration testing."""
        return RankingInfoModule()

    def test_full_menu_flow(self, integration_module):
        """Test the complete menu flow."""
        mock_client = Mock()
        mock_client.get_rapidly_increasing_trading_volume = Mock(
            return_value={"output": [{"stock_name": "테스트", "volume": "1000"}]}
        )
        integration_module.set_client(mock_client)

        # Mock menu selection and parameter collection
        with patch("inquirer.prompt") as mock_prompt:
            mock_prompt.side_effect = [
                {"api_choice": "rapidly_increasing_trading_volume"},  # API selection
                {"api_choice": "back"},  # Go back
            ]

            with patch.object(integration_module.parameter_collector, "collect_parameters") as mock_collect:
                mock_collect.return_value = {
                    "mrkt_tp": "001",
                    "sort_tp": "1",
                    "tm_tp": "1",
                    "trde_qty_tp": "10",
                    "stk_cnd": "0",
                    "pric_tp": "0",
                    "stex_tp": "1",
                }

                with patch("builtins.input"):  # Mock pause input
                    integration_module.handle_menu_loop()

                # Verify API was called
                mock_client.get_rapidly_increasing_trading_volume.assert_called_once()

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
