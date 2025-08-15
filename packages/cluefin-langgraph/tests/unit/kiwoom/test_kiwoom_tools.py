"""Unit tests for Kiwoom API tool wrappers."""

from typing import Any, Dict, List
from unittest.mock import Mock

import pytest
from cluefin_langgraph.agents.kiwoom.base.kiwoom_tools import KiwoomToolFactory
from langchain.tools import Tool


class TestKiwoomToolFactory:
    """Test cases for KiwoomToolFactory."""

    @pytest.fixture
    def mock_kiwoom_client(self):
        """Mock Kiwoom client for testing."""
        return Mock()

    @pytest.fixture
    def tool_factory(self, mock_kiwoom_client):
        """Create KiwoomToolFactory instance for testing."""
        return KiwoomToolFactory(mock_kiwoom_client)

    def test_initialization(self, tool_factory, mock_kiwoom_client):
        """Test factory initialization."""
        assert tool_factory.client == mock_kiwoom_client

    def test_create_account_tools(self, tool_factory):
        """Test creation of account tools."""
        tools = tool_factory.create_account_tools()

        assert isinstance(tools, list)
        assert len(tools) == 4

        tool_names = [tool.name for tool in tools]
        expected_names = [
            "get_account_balance",
            "get_account_holdings",
            "get_account_profit_loss",
            "get_purchasable_amount",
        ]

        assert all(name in tool_names for name in expected_names)

        # Test that all tools are Tool instances
        for tool in tools:
            assert isinstance(tool, Tool)
            assert hasattr(tool, "func")
            assert hasattr(tool, "description")

    def test_create_chart_tools(self, tool_factory):
        """Test creation of chart tools."""
        tools = tool_factory.create_chart_tools()

        assert isinstance(tools, list)
        assert len(tools) == 4

        tool_names = [tool.name for tool in tools]
        expected_names = ["get_daily_chart", "get_minute_chart", "get_current_price", "get_technical_indicators"]

        assert all(name in tool_names for name in expected_names)

        for tool in tools:
            assert isinstance(tool, Tool)

    def test_create_market_info_tools(self, tool_factory):
        """Test creation of market info tools."""
        tools = tool_factory.create_market_info_tools()

        assert isinstance(tools, list)
        assert len(tools) == 6

        tool_names = [tool.name for tool in tools]
        expected_names = ["get_stock_info", "search_stock_by_name", "get_market_index", "get_sector_info"]

        assert all(name in tool_names for name in expected_names)

    def test_create_etf_tools(self, tool_factory):
        """Test creation of ETF tools."""
        tools = tool_factory.create_etf_tools()

        assert isinstance(tools, list)
        assert len(tools) == 3

        tool_names = [tool.name for tool in tools]
        expected_names = ["get_etf_info", "get_etf_nav", "search_etf_by_theme"]

        assert all(name in tool_names for name in expected_names)

    def test_account_balance_tool_execution(self, tool_factory):
        """Test account balance tool execution."""
        result = tool_factory._get_account_balance()

        assert isinstance(result, dict)
        assert "message" in result
        assert "not yet implemented" in result["message"]

    def test_account_balance_tool_with_account_number(self, tool_factory):
        """Test account balance tool with account number."""
        result = tool_factory._get_account_balance("12345678")

        assert isinstance(result, dict)
        assert "message" in result

    def test_account_holdings_tool_execution(self, tool_factory):
        """Test account holdings tool execution."""
        result = tool_factory._get_account_holdings()

        assert isinstance(result, list)
        assert len(result) > 0
        assert isinstance(result[0], dict)
        assert "message" in result[0]

    def test_account_profit_loss_tool_execution(self, tool_factory):
        """Test account profit/loss tool execution."""
        result = tool_factory._get_account_profit_loss()

        assert isinstance(result, dict)
        assert "message" in result

    def test_purchasable_amount_tool_execution(self, tool_factory):
        """Test purchasable amount tool execution."""
        result = tool_factory._get_purchasable_amount()

        assert isinstance(result, dict)
        assert "message" in result

    def test_daily_chart_tool_execution(self, tool_factory):
        """Test daily chart tool execution."""
        result = tool_factory._get_daily_chart("005930")

        assert isinstance(result, list)
        assert len(result) > 0
        assert isinstance(result[0], dict)
        assert "005930" in result[0]["message"]

    def test_daily_chart_tool_with_period(self, tool_factory):
        """Test daily chart tool with custom period."""
        result = tool_factory._get_daily_chart("005930", 60)

        assert isinstance(result, list)
        assert "005930" in result[0]["message"]

    def test_minute_chart_tool_execution(self, tool_factory):
        """Test minute chart tool execution."""
        result = tool_factory._get_minute_chart("005930")

        assert isinstance(result, list)
        assert len(result) > 0
        assert "005930" in result[0]["message"]

    def test_minute_chart_tool_with_parameters(self, tool_factory):
        """Test minute chart tool with custom parameters."""
        result = tool_factory._get_minute_chart("005930", 10, 200)

        assert isinstance(result, list)
        assert "005930" in result[0]["message"]

    def test_current_price_tool_execution(self, tool_factory):
        """Test current price tool execution."""
        result = tool_factory._get_current_price("005930")

        assert isinstance(result, dict)
        assert "005930" in result["message"]

    def test_technical_indicators_tool_execution(self, tool_factory):
        """Test technical indicators tool execution."""
        result = tool_factory._get_technical_indicators("005930")

        assert isinstance(result, dict)
        assert "stock_code" in result
        assert result["stock_code"] == "005930"
        assert "indicators" in result
        assert "supported_indicators" in result

    def test_technical_indicators_tool_with_parameters(self, tool_factory):
        """Test technical indicators tool with custom indicators."""
        indicators = ["MA5", "RSI", "MACD"]
        result = tool_factory._get_technical_indicators("005930", indicators)

        assert isinstance(result, dict)
        assert result["stock_code"] == "005930"
        assert result["indicators"] == indicators

    def test_stock_info_tool_execution(self, tool_factory):
        """Test stock info tool execution."""
        result = tool_factory._get_stock_info("005930")

        assert isinstance(result, dict)
        assert "005930" in result["message"]

    def test_search_stock_by_name_tool_execution(self, tool_factory):
        """Test search stock by name tool execution."""
        result = tool_factory._search_stock_by_name("삼성전자")

        assert isinstance(result, list)
        assert len(result) > 0
        assert "삼성전자" in result[0]["message"]

    def test_market_index_tool_execution(self, tool_factory):
        """Test market index tool execution."""
        result = tool_factory._get_market_index()

        assert isinstance(result, dict)
        assert "message" in result

    def test_market_index_tool_with_code(self, tool_factory):
        """Test market index tool with specific index code."""
        result = tool_factory._get_market_index("1001")

        assert isinstance(result, dict)
        assert "message" in result

    def test_sector_info_tool_execution(self, tool_factory):
        """Test sector info tool execution."""
        result = tool_factory._get_sector_info()

        assert isinstance(result, list)
        assert len(result) > 0
        assert "message" in result[0]

    def test_sector_info_tool_with_code(self, tool_factory):
        """Test sector info tool with sector code."""
        result = tool_factory._get_sector_info("001")

        assert isinstance(result, list)
        assert "message" in result[0]

    def test_etf_info_tool_execution(self, tool_factory):
        """Test ETF info tool execution."""
        result = tool_factory._get_etf_info("069500")

        assert isinstance(result, dict)
        assert "069500" in result["message"]

    def test_etf_nav_tool_execution(self, tool_factory):
        """Test ETF NAV tool execution."""
        result = tool_factory._get_etf_nav("069500")

        assert isinstance(result, dict)
        assert "069500" in result["message"]

    def test_search_etf_by_theme_tool_execution(self, tool_factory):
        """Test search ETF by theme tool execution."""
        result = tool_factory._search_etf_by_theme("반도체")

        assert isinstance(result, list)
        assert len(result) > 0
        assert "반도체" in result[0]["message"]

    def test_theme_stocks_tool_execution(self, tool_factory):
        """Test theme stocks tool execution."""
        result = tool_factory._get_theme_stocks("바이오")

        assert isinstance(result, list)
        assert len(result) > 0
        assert "바이오" in result[0]["message"]

    def test_sector_performance_tool_execution(self, tool_factory):
        """Test sector performance tool execution."""
        result = tool_factory._get_sector_performance()

        assert isinstance(result, list)
        assert len(result) > 0
        assert "message" in result[0]

    def test_sector_performance_tool_with_date(self, tool_factory):
        """Test sector performance tool with date."""
        result = tool_factory._get_sector_performance("20240101")

        assert isinstance(result, list)
        assert "message" in result[0]

    def test_hot_themes_tool_execution(self, tool_factory):
        """Test hot themes tool execution."""
        result = tool_factory._get_hot_themes()

        assert isinstance(result, list)
        assert len(result) > 0
        assert "message" in result[0]

    def test_hot_themes_tool_with_limit(self, tool_factory):
        """Test hot themes tool with custom limit."""
        result = tool_factory._get_hot_themes(5)

        assert isinstance(result, list)
        assert "message" in result[0]

    def test_tool_descriptions_korean(self, tool_factory):
        """Test that tool descriptions are in Korean."""
        all_tools = (
            tool_factory.create_account_tools()
            + tool_factory.create_chart_tools()
            + tool_factory.create_market_info_tools()
            + tool_factory.create_etf_tools()
            + tool_factory.create_theme_tools()
        )

        for tool in all_tools:
            # Check that description contains Korean characters
            description = tool.description
            assert len(description) > 10  # Should have meaningful description
            # Basic check for Korean characters (Hangul)
            has_korean = any("\uac00" <= char <= "\ud7a3" for char in description)
            assert has_korean, f"Tool {tool.name} description should be in Korean"

    def test_tool_function_callable(self, tool_factory):
        """Test that all tool functions are callable."""
        all_tools = (
            tool_factory.create_account_tools()
            + tool_factory.create_chart_tools()
            + tool_factory.create_market_info_tools()
            + tool_factory.create_etf_tools()
            + tool_factory.create_theme_tools()
        )

        for tool in all_tools:
            assert callable(tool.func), f"Tool {tool.name} function should be callable"

    def test_tool_names_unique(self, tool_factory):
        """Test that all tool names are unique."""
        all_tools = (
            tool_factory.create_account_tools()
            + tool_factory.create_chart_tools()
            + tool_factory.create_market_info_tools()
            + tool_factory.create_etf_tools()
            + tool_factory.create_theme_tools()
        )

        tool_names = [tool.name for tool in all_tools]
        unique_names = set(tool_names)

        assert len(tool_names) == len(unique_names), "All tool names should be unique"

    def test_parameter_handling_optional_account_number(self, tool_factory):
        """Test handling of optional account number parameter."""
        # Test with None (default)
        result1 = tool_factory._get_account_balance(None)
        result2 = tool_factory._get_account_balance()

        assert result1 == result2

        # Test with specific account number
        result3 = tool_factory._get_account_balance("12345678")
        assert isinstance(result3, dict)

    def test_parameter_handling_stock_codes(self, tool_factory):
        """Test handling of stock code parameters."""
        test_codes = ["005930", "000660", "035420"]

        for code in test_codes:
            result = tool_factory._get_current_price(code)
            assert isinstance(result, dict)
            assert code in result["message"]

    def test_parameter_handling_chart_parameters(self, tool_factory):
        """Test handling of various chart parameters."""
        # Test different periods for daily chart
        periods = [7, 30, 90, 365]
        for period in periods:
            result = tool_factory._get_daily_chart("005930", period)
            assert isinstance(result, list)

        # Test different intervals and counts for minute chart
        intervals = [1, 5, 10, 30, 60]
        counts = [50, 100, 200, 500]

        for interval in intervals:
            for count in counts:
                result = tool_factory._get_minute_chart("005930", interval, count)
                assert isinstance(result, list)

    def test_error_handling_graceful_fallback(self, tool_factory):
        """Test that methods return graceful fallback responses."""
        # All tool methods should return structured data even when not implemented

        # Test account tools
        assert isinstance(tool_factory._get_account_balance(), dict)
        assert isinstance(tool_factory._get_account_holdings(), list)
        assert isinstance(tool_factory._get_account_profit_loss(), dict)
        assert isinstance(tool_factory._get_purchasable_amount(), dict)

        # Test chart tools
        assert isinstance(tool_factory._get_daily_chart("005930"), list)
        assert isinstance(tool_factory._get_minute_chart("005930"), list)
        assert isinstance(tool_factory._get_current_price("005930"), dict)
        assert isinstance(tool_factory._get_technical_indicators("005930"), dict)

        # Test market info tools
        assert isinstance(tool_factory._get_stock_info("005930"), dict)
        assert isinstance(tool_factory._search_stock_by_name("삼성전자"), list)
        assert isinstance(tool_factory._get_market_index(), dict)
        assert isinstance(tool_factory._get_sector_info(), list)

        # Test ETF tools
        assert isinstance(tool_factory._get_etf_info("069500"), dict)
        assert isinstance(tool_factory._get_etf_nav("069500"), dict)
        assert isinstance(tool_factory._search_etf_by_theme("반도체"), list)

        # Test theme/sector tools
        assert isinstance(tool_factory._get_theme_stocks("AI"), list)
        assert isinstance(tool_factory._get_sector_performance(), list)
        assert isinstance(tool_factory._get_hot_themes(), list)

    def test_todo_implementation_messages(self, tool_factory):
        """Test that TODO messages indicate implementation is needed."""
        # All methods should return messages indicating they need implementation
        result = tool_factory._get_account_balance()
        assert "not yet implemented" in result["message"]

        result = tool_factory._get_daily_chart("005930")
        assert "not yet implemented" in result[0]["message"]

        result = tool_factory._get_stock_info("005930")
        assert "not yet implemented" in result["message"]
