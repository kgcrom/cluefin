"""
Unit tests for the base API module.

Tests the common functionality including error handling, retry logic,
and client management.
"""

import time
from unittest.mock import MagicMock, Mock, patch

import pytest
from cluefin_openapi.kiwoom._exceptions import KiwoomAPIError

from cluefin_cli.commands.inquiry.base_api_module import BaseAPIModule
from cluefin_cli.commands.inquiry.config_models import APICategory, APIConfig, ParameterConfig


class TestBaseAPIModule:
    """Test cases for BaseAPIModule functionality."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock Kiwoom client."""
        client = Mock()
        client.get_test_api = Mock(return_value={"status": "success", "data": []})
        return client

    @pytest.fixture
    def sample_api_config(self):
        """Create a sample API configuration for testing."""
        return APIConfig(
            name="test_api",
            korean_name="테스트 API",
            api_method="get_test_api",
            required_params=[ParameterConfig(name="param1", korean_name="파라미터1", param_type="text", required=True)],
        )

    @pytest.fixture
    def sample_category(self, sample_api_config):
        """Create a sample API category for testing."""
        return APICategory(name="test_category", korean_name="테스트 카테고리", apis=[sample_api_config])

    @pytest.fixture
    def concrete_module(self, mock_client, sample_category):
        """Create a concrete implementation of BaseAPIModule for testing."""

        class ConcreteAPIModule(BaseAPIModule):
            def get_api_category(self):
                return sample_category

            def _format_and_display_result(self, result, api_config):
                self.console.print(f"Result: {result}")

        return ConcreteAPIModule(mock_client)

    def test_initialization(self, mock_client):
        """Test proper initialization of BaseAPIModule."""

        class TestModule(BaseAPIModule):
            def get_api_category(self):
                return APICategory(name="test", korean_name="테스트", apis=[])

            def _format_and_display_result(self, result, api_config):
                pass

        module = TestModule(mock_client)

        assert module.client == mock_client
        assert module.parameter_collector is not None
        assert module.formatter is not None
        assert module.console is not None
        assert module.max_retries == 3
        assert module.retry_delay == 1.0
        assert module.backoff_multiplier == 2.0
        assert module.min_call_interval == 0.1

    def test_initialization_without_client(self):
        """Test initialization without providing a client."""

        class TestModule(BaseAPIModule):
            def get_api_category(self):
                return APICategory(name="test", korean_name="테스트", apis=[])

            def _format_and_display_result(self, result, api_config):
                pass

        module = TestModule()

        assert module.client is None
        assert module.parameter_collector is not None

    @patch("inquirer.prompt")
    def test_show_api_menu_success(self, mock_prompt, concrete_module):
        """Test successful API menu display and selection."""
        mock_prompt.return_value = {"api_choice": "test_api"}

        result = concrete_module.show_api_menu()

        assert result == "test_api"
        mock_prompt.assert_called_once()

    @patch("inquirer.prompt")
    def test_show_api_menu_back_selection(self, mock_prompt, concrete_module):
        """Test menu selection when user chooses to go back."""
        mock_prompt.return_value = {"api_choice": "back"}

        result = concrete_module.show_api_menu()

        assert result is None

    @patch("inquirer.prompt")
    def test_show_api_menu_cancelled(self, mock_prompt, concrete_module):
        """Test menu selection when user cancels."""
        mock_prompt.return_value = None

        result = concrete_module.show_api_menu()

        assert result is None

    def test_get_api_parameters(self, concrete_module, sample_api_config):
        """Test parameter collection for an API."""
        with patch.object(concrete_module.parameter_collector, "collect_parameters") as mock_collect:
            mock_collect.return_value = {"param1": "value1"}

            result = concrete_module.get_api_parameters(sample_api_config)

            assert result == {"param1": "value1"}
            mock_collect.assert_called_once_with(sample_api_config)

    def test_execute_api_success(self, concrete_module, mock_client):
        """Test successful API execution."""
        with patch.object(concrete_module, "get_api_parameters") as mock_params:
            mock_params.return_value = {"param1": "value1"}

            with patch.object(concrete_module, "_execute_api_with_retry") as mock_execute:
                mock_execute.return_value = {"status": "success"}

                with patch.object(concrete_module, "_format_and_display_result") as mock_format:
                    result = concrete_module.execute_api("test_api")

                    assert result is True
                    mock_params.assert_called_once()
                    mock_execute.assert_called_once()
                    mock_format.assert_called_once()

    def test_execute_api_invalid_name(self, concrete_module):
        """Test API execution with invalid API name."""
        result = concrete_module.execute_api("invalid_api")

        assert result is False

    def test_execute_api_cancelled_parameters(self, concrete_module):
        """Test API execution when parameter collection is cancelled."""
        with patch.object(concrete_module, "get_api_parameters") as mock_params:
            mock_params.return_value = None

            result = concrete_module.execute_api("test_api")

            assert result is False

    def test_execute_api_with_retry_success(self, concrete_module, mock_client, sample_api_config):
        """Test successful API execution with retry logic."""
        params = {"param1": "value1"}
        expected_result = {"status": "success", "data": []}

        result = concrete_module._execute_api_with_retry(sample_api_config, params)

        assert result == expected_result
        mock_client.get_test_api.assert_called_once_with(**params)

    def test_execute_api_with_retry_no_client(self, sample_api_config):
        """Test API execution when no client is available."""

        class TestModule(BaseAPIModule):
            def get_api_category(self):
                return APICategory(name="test", korean_name="테스트", apis=[])

            def _format_and_display_result(self, result, api_config):
                pass

        module = TestModule()  # No client provided

        result = module._execute_api_with_retry(sample_api_config, {})

        assert result is None

    def test_execute_api_with_retry_method_not_found(self, concrete_module, sample_api_config):
        """Test API execution when method doesn't exist on client."""
        # Remove the method from mock client
        del concrete_module.client.get_test_api

        result = concrete_module._execute_api_with_retry(sample_api_config, {})

        assert result is None

    def test_execute_api_with_retry_kiwoom_error_retryable(self, concrete_module, mock_client, sample_api_config):
        """Test retry logic with retryable Kiwoom API error."""
        params = {"param1": "value1"}

        # Mock the API method to raise retryable error first, then succeed
        error = KiwoomAPIError("RATE_LIMIT_EXCEEDED", "Rate limit exceeded")
        success_result = {"status": "success"}

        mock_client.get_test_api.side_effect = [error, success_result]

        with patch.object(concrete_module, "_is_retryable_error", return_value=True):
            with patch("time.sleep"):  # Mock sleep to speed up test
                result = concrete_module._execute_api_with_retry(sample_api_config, params)

        assert result == success_result
        assert mock_client.get_test_api.call_count == 2

    def test_execute_api_with_retry_kiwoom_error_non_retryable(self, concrete_module, mock_client, sample_api_config):
        """Test retry logic with non-retryable Kiwoom API error."""
        params = {"param1": "value1"}

        error = KiwoomAPIError("Invalid credentials", status_code=401)
        mock_client.get_test_api.side_effect = error

        with patch.object(concrete_module, "_is_retryable_error", return_value=False):
            result = concrete_module._execute_api_with_retry(sample_api_config, params)

        assert result is None
        assert mock_client.get_test_api.call_count == 1  # No retry

    def test_execute_api_with_retry_max_retries_exceeded(self, concrete_module, mock_client, sample_api_config):
        """Test retry logic when max retries are exceeded."""
        params = {"param1": "value1"}

        error = KiwoomAPIError("Rate limit exceeded", status_code=429)
        mock_client.get_test_api.side_effect = error

        with patch.object(concrete_module, "_is_retryable_error", return_value=True):
            with patch("time.sleep"):  # Mock sleep to speed up test
                result = concrete_module._execute_api_with_retry(sample_api_config, params)

        assert result is None
        assert mock_client.get_test_api.call_count == concrete_module.max_retries

    def test_enforce_rate_limit(self, concrete_module):
        """Test rate limiting enforcement."""
        # Set a recent last call time
        concrete_module.last_api_call = time.time() - 0.05  # 50ms ago

        with patch("time.sleep") as mock_sleep:
            concrete_module._enforce_rate_limit()

            # Should sleep for remaining time to reach min_call_interval
            mock_sleep.assert_called_once()
            sleep_time = mock_sleep.call_args[0][0]
            assert 0.04 < sleep_time < 0.06  # Approximately 50ms

    def test_enforce_rate_limit_no_sleep_needed(self, concrete_module):
        """Test rate limiting when no sleep is needed."""
        # Set an old last call time
        concrete_module.last_api_call = time.time() - 1.0  # 1 second ago

        with patch("time.sleep") as mock_sleep:
            concrete_module._enforce_rate_limit()

            # Should not sleep
            mock_sleep.assert_not_called()

    def test_is_retryable_error(self, concrete_module):
        """Test retryable error detection."""
        retryable_error = KiwoomAPIError("Rate limit exceeded", status_code=429)
        non_retryable_error = KiwoomAPIError("Invalid credentials", status_code=401)

        assert concrete_module._is_retryable_error(retryable_error) is True
        assert concrete_module._is_retryable_error(non_retryable_error) is False

    @patch("inquirer.prompt")
    def test_handle_menu_loop_success(self, mock_prompt, concrete_module):
        """Test successful menu loop execution."""
        # Simulate user selecting API, then going back
        mock_prompt.side_effect = [
            {"api_choice": "test_api"},  # First selection
            {"api_choice": "back"},  # Second selection (go back)
        ]

        with patch.object(concrete_module, "execute_api", return_value=True):
            with patch("builtins.input"):  # Mock input for pause
                concrete_module.handle_menu_loop()

        assert mock_prompt.call_count == 2

    @patch("inquirer.prompt")
    def test_handle_menu_loop_keyboard_interrupt(self, mock_prompt, concrete_module):
        """Test menu loop handling keyboard interrupt."""
        mock_prompt.side_effect = KeyboardInterrupt()

        # Should not raise exception
        concrete_module.handle_menu_loop()

    def test_set_client(self, concrete_module):
        """Test setting a new client."""
        new_client = Mock()

        concrete_module.set_client(new_client)

        assert concrete_module.client == new_client

    def test_get_client_status_with_client(self, concrete_module, mock_client):
        """Test getting client status when client is available."""
        status = concrete_module.get_client_status()

        assert status["client_initialized"] is True
        assert status["client_type"] == "Mock"
        assert status["max_retries"] == 3
        assert status["retry_delay"] == 1.0
        assert status["min_call_interval"] == 0.1

    def test_get_client_status_without_client(self):
        """Test getting client status when no client is available."""

        class TestModule(BaseAPIModule):
            def get_api_category(self):
                return APICategory(name="test", korean_name="테스트", apis=[])

            def _format_and_display_result(self, result, api_config):
                pass

        module = TestModule()  # No client
        status = module.get_client_status()

        assert status["client_initialized"] is False
        assert status["client_type"] is None


class TestBaseAPIModuleIntegration:
    """Integration tests for BaseAPIModule with real components."""

    @pytest.fixture
    def integration_module(self):
        """Create a module for integration testing."""

        class IntegrationModule(BaseAPIModule):
            def get_api_category(self):
                return APICategory(
                    name="integration_test",
                    korean_name="통합 테스트",
                    apis=[
                        APIConfig(
                            name="test_api",
                            korean_name="테스트 API",
                            api_method="get_test_data",
                            required_params=[
                                ParameterConfig(
                                    name="market_type",
                                    korean_name="시장구분",
                                    param_type="select",
                                    choices=[("코스피", "001"), ("코스닥", "101")],
                                )
                            ],
                        )
                    ],
                )

            def _format_and_display_result(self, result, api_config):
                self.formatter.display_info(f"API {api_config.korean_name} 실행 완료")

        return IntegrationModule()

    def test_full_api_execution_flow(self, integration_module):
        """Test the complete API execution flow."""
        # Mock client with test method
        mock_client = Mock()
        mock_client.get_test_data = Mock(return_value={"data": "test_result"})
        integration_module.set_client(mock_client)

        # Mock parameter collection
        with patch.object(integration_module.parameter_collector, "collect_parameters") as mock_collect:
            mock_collect.return_value = {"market_type": "001"}

            # Execute API
            result = integration_module.execute_api("test_api")

            assert result is True
            mock_client.get_test_data.assert_called_once_with(market_type="001")
