"""Unit tests for StockInfoAgent."""

import pytest
from unittest.mock import Mock, MagicMock

from cluefin_langgraph.agents.kiwoom.specialized.stock_info_agent import StockInfoAgent


class TestStockInfoAgent:
    """Test cases for StockInfoAgent."""

    @pytest.fixture
    def mock_kiwoom_client(self):
        """Create a mock Kiwoom client."""
        return Mock()

    @pytest.fixture
    def mock_llm(self):
        """Create a mock language model."""
        return Mock()

    @pytest.fixture
    def stock_info_agent(self, mock_kiwoom_client, mock_llm):
        """Create a StockInfoAgent instance for testing."""
        return StockInfoAgent(
            kiwoom_client=mock_kiwoom_client,
            llm=mock_llm,
            verbose=True
        )

    def test_get_agent_type(self, stock_info_agent):
        """Test that agent type is correctly returned."""
        assert stock_info_agent._get_agent_type() == "stock_info"

    def test_initialize_tools(self, stock_info_agent):
        """Test that tools are properly initialized."""
        tools = stock_info_agent._initialize_tools()
        assert isinstance(tools, list)
        assert len(tools) > 0
        
        # Check that expected tools are present
        tool_names = [tool.name for tool in tools]
        expected_tools = [
            "get_stock_info",
            "search_stock_by_name", 
            "get_stock_financial_data",
            "get_stock_fundamentals",
            "get_etf_info",
            "get_etf_nav"
        ]
        
        for expected_tool in expected_tools:
            assert expected_tool in tool_names

    def test_process_stock_search_request(self, stock_info_agent):
        """Test processing stock search requests."""
        # Mock the search tool
        mock_tool = Mock()
        mock_tool.name = "search_stock_by_name"
        mock_tool.func.return_value = [{"code": "005930", "name": "삼성전자"}]
        stock_info_agent.tools = [mock_tool]

        # Test search request
        result = stock_info_agent.process_request(
            "삼성전자 검색해줘",
            {"stock_name": "삼성전자"}
        )

        assert isinstance(result, list)
        assert len(result) > 0
        mock_tool.func.assert_called_once_with("삼성전자")

    def test_process_stock_info_request(self, stock_info_agent):
        """Test processing basic stock info requests."""
        # Mock the stock info tool
        mock_tool = Mock()
        mock_tool.name = "get_stock_info"
        mock_tool.func.return_value = {"code": "005930", "name": "삼성전자", "price": 70000}
        stock_info_agent.tools = [mock_tool]

        # Test stock info request
        result = stock_info_agent.process_request(
            "삼성전자 정보 알려줘",
            {"stock_code": "005930"}
        )

        assert isinstance(result, dict)
        assert "code" in result
        mock_tool.func.assert_called_once_with("005930")

    def test_process_etf_info_request(self, stock_info_agent):
        """Test processing ETF info requests."""
        # Mock the ETF info tool
        mock_tool = Mock()
        mock_tool.name = "get_etf_info"
        mock_tool.func.return_value = {"code": "069500", "name": "KODEX 200", "nav": 10000}
        stock_info_agent.tools = [mock_tool]

        # Test ETF info request
        result = stock_info_agent.process_request(
            "KODEX 200 ETF 정보 알려줘",
            {"etf_code": "069500"}
        )

        assert isinstance(result, dict)
        assert "code" in result
        mock_tool.func.assert_called_once_with("069500")

    def test_process_etf_nav_request(self, stock_info_agent):
        """Test processing ETF NAV requests."""
        # Mock the ETF NAV tool
        mock_tool = Mock()
        mock_tool.name = "get_etf_nav"
        mock_tool.func.return_value = {"code": "069500", "nav": 10000, "premium": 0.1}
        stock_info_agent.tools = [mock_tool]

        # Test ETF NAV request
        result = stock_info_agent.process_request(
            "KODEX 200 NAV 알려줘",
            {"etf_code": "069500"}
        )

        assert isinstance(result, dict)
        assert "nav" in result
        mock_tool.func.assert_called_once_with("069500")

    def test_process_financial_data_request(self, stock_info_agent):
        """Test processing financial data requests."""
        # Mock the financial data tool
        mock_tool = Mock()
        mock_tool.name = "get_stock_financial_data"
        mock_tool.func.return_value = {"code": "005930", "revenue": 1000000, "profit": 50000}
        stock_info_agent.tools = [mock_tool]

        # Test financial data request
        result = stock_info_agent.process_request(
            "삼성전자 재무제표 보여줘",
            {"stock_code": "005930"}
        )

        assert isinstance(result, dict)
        assert "revenue" in result
        mock_tool.func.assert_called_once_with("005930")

    def test_process_fundamentals_request(self, stock_info_agent):
        """Test processing fundamentals requests."""
        # Mock the fundamentals tool
        mock_tool = Mock()
        mock_tool.name = "get_stock_fundamentals"
        mock_tool.func.return_value = {"code": "005930", "per": 15.5, "pbr": 1.2}
        stock_info_agent.tools = [mock_tool]

        # Test fundamentals request
        result = stock_info_agent.process_request(
            "삼성전자 PER PBR 알려줘",
            {"stock_code": "005930"}
        )

        assert isinstance(result, dict)
        assert "per" in result
        mock_tool.func.assert_called_once_with("005930")

    def test_missing_stock_code_error(self, stock_info_agent):
        """Test error handling when stock code is missing."""
        result = stock_info_agent.process_request(
            "종목 정보 알려줘",
            {}
        )

        assert isinstance(result, dict)
        assert "error" in result
        assert "종목코드가 필요합니다" in result["error"]

    def test_missing_stock_name_error(self, stock_info_agent):
        """Test error handling when stock name is missing for search."""
        result = stock_info_agent.process_request(
            "종목 검색해줘",
            {}
        )

        assert isinstance(result, list)
        assert len(result) == 1
        assert "error" in result[0]
        assert "검색할 종목명이 필요합니다" in result[0]["error"]

    def test_tool_not_available_error(self, stock_info_agent):
        """Test error handling when required tool is not available."""
        # Set empty tools list
        stock_info_agent.tools = []

        result = stock_info_agent.process_request(
            "삼성전자 정보 알려줘",
            {"stock_code": "005930"}
        )

        assert isinstance(result, dict)
        assert "error" in result
        assert "도구를 사용할 수 없습니다" in result["error"]

    def test_extract_stock_code(self, stock_info_agent):
        """Test stock code extraction from various parameter formats."""
        # Test different parameter names
        test_cases = [
            ({"stock_code": "005930"}, "005930"),
            ({"etf_code": "069500"}, "069500"),
            ({"symbol": "AAPL"}, "AAPL"),
            ({"code": "123456"}, "123456"),
            ({"종목코드": "005930"}, "005930"),
            ({"종목": "005930"}, "005930"),
            ({"etf": "069500"}, "069500"),
            ({}, None),
            (None, None),
        ]

        for params, expected in test_cases:
            result = stock_info_agent._extract_stock_code(params)
            assert result == expected