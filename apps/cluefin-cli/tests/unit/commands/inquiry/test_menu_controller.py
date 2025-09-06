"""
Unit tests for the menu controller.

Tests the main menu navigation logic and module integration.
"""

from unittest.mock import Mock, patch

import pytest

from cluefin_cli.commands.inquiry.menu_controller import MenuController


class TestMenuController:
    """Test cases for MenuController functionality."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock Kiwoom client."""
        return Mock()

    @pytest.fixture
    def menu_controller(self, mock_client):
        """Create a menu controller with mock client."""
        return MenuController(mock_client)

    @pytest.fixture
    def menu_controller_no_client(self):
        """Create a menu controller without client."""
        return MenuController()

    def test_initialization_with_client(self, mock_client):
        """Test proper initialization with client."""
        controller = MenuController(mock_client)

        assert controller.client == mock_client
        assert controller.ranking_module is not None
        assert controller.sector_module is not None
        assert controller.stock_module is not None

        # Verify modules have the client
        assert controller.ranking_module.client == mock_client
        assert controller.sector_module.client == mock_client
        assert controller.stock_module.client == mock_client

    def test_initialization_without_client(self):
        """Test initialization without client."""
        controller = MenuController()

        assert controller.client is None
        assert controller.ranking_module is not None
        assert controller.sector_module is not None
        assert controller.stock_module is not None

        # Verify modules don't have client
        assert controller.ranking_module.client is None
        assert controller.sector_module.client is None
        assert controller.stock_module.client is None

    def test_set_client(self, menu_controller_no_client, mock_client):
        """Test setting client after initialization."""
        menu_controller_no_client.set_client(mock_client)

        assert menu_controller_no_client.client == mock_client
        assert menu_controller_no_client.ranking_module.client == mock_client
        assert menu_controller_no_client.sector_module.client == mock_client
        assert menu_controller_no_client.stock_module.client == mock_client

    @patch("inquirer.prompt")
    def test_run_main_menu_ranking_selection(self, mock_prompt, menu_controller):
        """Test main menu with ranking selection."""
        # Mock user selecting ranking, then exit
        mock_prompt.side_effect = [
            {"main_choice": "ranking"},  # First selection
            {"main_choice": "exit"},     # Second selection
        ]

        with patch.object(menu_controller, "_handle_module_execution") as mock_handle:
            menu_controller.run_main_menu()

            # Verify ranking module was called
            mock_handle.assert_called_with(menu_controller.ranking_module, "순위정보")

    @patch("inquirer.prompt")
    def test_run_main_menu_sector_selection(self, mock_prompt, menu_controller):
        """Test main menu with sector selection."""
        mock_prompt.side_effect = [
            {"main_choice": "sector"},
            {"main_choice": "exit"},
        ]

        with patch.object(menu_controller, "_handle_module_execution") as mock_handle:
            menu_controller.run_main_menu()

            mock_handle.assert_called_with(menu_controller.sector_module, "업종정보")

    @patch("inquirer.prompt")
    def test_run_main_menu_stock_selection(self, mock_prompt, menu_controller):
        """Test main menu with stock selection."""
        mock_prompt.side_effect = [
            {"main_choice": "stock"},
            {"main_choice": "exit"},
        ]

        with patch.object(menu_controller, "_handle_module_execution") as mock_handle:
            menu_controller.run_main_menu()

            mock_handle.assert_called_with(menu_controller.stock_module, "종목정보")

    @patch("inquirer.prompt")
    def test_run_main_menu_exit_selection(self, mock_prompt, menu_controller):
        """Test main menu with direct exit selection."""
        mock_prompt.return_value = {"main_choice": "exit"}

        with patch.object(menu_controller, "_handle_module_execution") as mock_handle:
            menu_controller.run_main_menu()

            # Should not call any module
            mock_handle.assert_not_called()

    @patch("inquirer.prompt")
    def test_run_main_menu_user_cancelled(self, mock_prompt, menu_controller):
        """Test main menu when user cancels (Ctrl+C)."""
        mock_prompt.return_value = None  # User cancelled

        with patch.object(menu_controller, "_handle_module_execution") as mock_handle:
            menu_controller.run_main_menu()

            mock_handle.assert_not_called()

    @patch("inquirer.prompt")
    def test_run_main_menu_invalid_choice(self, mock_prompt, menu_controller):
        """Test main menu with invalid choice."""
        mock_prompt.side_effect = [
            {"main_choice": None},  # Invalid choice
            {"main_choice": "exit"},  # Then exit
        ]

        with patch.object(menu_controller, "_handle_module_execution") as mock_handle:
            menu_controller.run_main_menu()

            # Should not call module for invalid choice
            mock_handle.assert_not_called()

    @patch("inquirer.prompt")
    def test_run_main_menu_unknown_choice(self, mock_prompt, menu_controller):
        """Test main menu with unknown choice value."""
        mock_prompt.side_effect = [
            {"main_choice": "unknown"},  # Unknown choice
            {"main_choice": "exit"},     # Then exit
        ]

        with patch.object(menu_controller, "_handle_module_execution") as mock_handle:
            menu_controller.run_main_menu()

            mock_handle.assert_not_called()

    @patch("inquirer.prompt")
    def test_run_main_menu_keyboard_interrupt(self, mock_prompt, menu_controller):
        """Test main menu handling keyboard interrupt."""
        mock_prompt.side_effect = KeyboardInterrupt()

        with patch.object(menu_controller, "_handle_module_execution") as mock_handle:
            # Should not raise exception
            menu_controller.run_main_menu()

            mock_handle.assert_not_called()

    @patch("inquirer.prompt")
    def test_run_main_menu_exception_handling(self, mock_prompt, menu_controller):
        """Test main menu handling unexpected exceptions."""
        mock_prompt.side_effect = [
            Exception("Test error"),  # Unexpected error
            {"main_choice": "exit"},  # Then exit
        ]

        with patch("builtins.input"):  # Mock input for error recovery
            menu_controller.run_main_menu()

        # Should handle exception gracefully and continue

    def test_handle_module_execution_success(self, menu_controller):
        """Test successful module execution."""
        mock_module = Mock()
        mock_module.handle_menu_loop = Mock()

        menu_controller._handle_module_execution(mock_module, "테스트모듈")

        mock_module.handle_menu_loop.assert_called_once()

    def test_handle_module_execution_keyboard_interrupt(self, menu_controller):
        """Test module execution with keyboard interrupt."""
        mock_module = Mock()
        mock_module.handle_menu_loop = Mock(side_effect=KeyboardInterrupt())

        # Should not raise exception
        menu_controller._handle_module_execution(mock_module, "테스트모듈")

        mock_module.handle_menu_loop.assert_called_once()

    def test_handle_module_execution_exception(self, menu_controller):
        """Test module execution with exception."""
        mock_module = Mock()
        mock_module.handle_menu_loop = Mock(side_effect=Exception("Test error"))

        with patch("builtins.input"):  # Mock input for error recovery
            menu_controller._handle_module_execution(mock_module, "테스트모듈")

        mock_module.handle_menu_loop.assert_called_once()

    @patch("inquirer.prompt")
    def test_multiple_selections_before_exit(self, mock_prompt, menu_controller):
        """Test multiple menu selections before exit."""
        mock_prompt.side_effect = [
            {"main_choice": "ranking"},
            {"main_choice": "sector"},
            {"main_choice": "stock"},
            {"main_choice": "exit"},
        ]

        with patch.object(menu_controller, "_handle_module_execution") as mock_handle:
            menu_controller.run_main_menu()

            # Should have called all three modules
            assert mock_handle.call_count == 3
            
            # Verify the calls were made with correct modules
            calls = mock_handle.call_args_list
            assert calls[0][0][0] == menu_controller.ranking_module
            assert calls[0][0][1] == "순위정보"
            assert calls[1][0][0] == menu_controller.sector_module
            assert calls[1][0][1] == "업종정보"
            assert calls[2][0][0] == menu_controller.stock_module
            assert calls[2][0][1] == "종목정보"

    def test_menu_choices_format(self, menu_controller):
        """Test that menu choices are properly formatted."""
        # This test verifies the menu structure without actually running it
        # We can't easily test the exact inquirer choices, but we can verify
        # the controller has the right modules and they're properly initialized
        
        assert hasattr(menu_controller, 'ranking_module')
        assert hasattr(menu_controller, 'sector_module')
        assert hasattr(menu_controller, 'stock_module')
        
        # Verify modules are the correct types
        from cluefin_cli.commands.inquiry.ranking_info import RankingInfoModule
        from cluefin_cli.commands.inquiry.sector_info import SectorInfoModule
        from cluefin_cli.commands.inquiry.stock_info import StockInfoModule
        
        assert isinstance(menu_controller.ranking_module, RankingInfoModule)
        assert isinstance(menu_controller.sector_module, SectorInfoModule)
        assert isinstance(menu_controller.stock_module, StockInfoModule)


class TestMenuControllerIntegration:
    """Integration tests for MenuController with real modules."""

    @pytest.fixture
    def integration_controller(self):
        """Create a controller for integration testing."""
        return MenuController()

    def test_client_propagation(self, integration_controller):
        """Test that client is properly propagated to all modules."""
        mock_client = Mock()
        
        integration_controller.set_client(mock_client)
        
        # Verify client is set on controller
        assert integration_controller.client == mock_client
        
        # Verify client is propagated to all modules
        assert integration_controller.ranking_module.client == mock_client
        assert integration_controller.sector_module.client == mock_client
        assert integration_controller.stock_module.client == mock_client

    def test_module_independence(self, integration_controller):
        """Test that modules can operate independently."""
        # Each module should have its own parameter collector and formatter
        ranking_collector = integration_controller.ranking_module.parameter_collector
        sector_collector = integration_controller.sector_module.parameter_collector
        stock_collector = integration_controller.stock_module.parameter_collector
        
        # They should be different instances
        assert ranking_collector is not sector_collector
        assert sector_collector is not stock_collector
        assert ranking_collector is not stock_collector
        
        # Same for formatters
        ranking_formatter = integration_controller.ranking_module.formatter
        sector_formatter = integration_controller.sector_module.formatter
        stock_formatter = integration_controller.stock_module.formatter
        
        assert ranking_formatter is not sector_formatter
        assert sector_formatter is not stock_formatter
        assert ranking_formatter is not stock_formatter

    def test_error_isolation(self, integration_controller):
        """Test that errors in one module don't affect others."""
        mock_client = Mock()
        integration_controller.set_client(mock_client)
        
        # Simulate error in one module
        integration_controller.ranking_module.client = None
        
        # Other modules should still have client
        assert integration_controller.sector_module.client == mock_client
        assert integration_controller.stock_module.client == mock_client
        
        # Controller should still have client
        assert integration_controller.client == mock_client