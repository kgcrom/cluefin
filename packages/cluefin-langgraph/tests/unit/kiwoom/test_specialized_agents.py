"""Unit tests for specialized Kiwoom agents."""

from typing import Any, Dict, List
from unittest.mock import Mock, patch

import pytest
from cluefin_langgraph.agents.kiwoom.specialized.account_agent import AccountAgent
from cluefin_langgraph.agents.kiwoom.specialized.chart_agent import ChartAgent


class TestAccountAgent:
    """Test cases for AccountAgent."""

    @pytest.fixture
    def mock_kiwoom_client(self):
        """Mock Kiwoom client for testing."""
        return Mock()

    @pytest.fixture
    def mock_llm(self):
        """Mock language model for testing."""
        return Mock()

    @pytest.fixture
    def mock_balance_tool(self):
        """Mock account balance tool."""
        tool = Mock()
        tool.name = "get_account_balance"
        tool.func.return_value = {
            "total_asset": 10000000,
            "deposit": 2000000,
            "stock_value": 8000000,
            "profit_loss": 500000,
        }
        return tool

    @pytest.fixture
    def mock_holdings_tool(self):
        """Mock account holdings tool."""
        tool = Mock()
        tool.name = "get_account_holdings"
        tool.func.return_value = [
            {
                "stock_code": "005930",
                "stock_name": "삼성전자",
                "quantity": 100,
                "avg_price": 70000,
                "current_price": 75000,
                "profit_loss": 500000,
            }
        ]
        return tool

    @pytest.fixture
    def mock_profit_loss_tool(self):
        """Mock profit/loss tool."""
        tool = Mock()
        tool.name = "get_account_profit_loss"
        tool.func.return_value = {
            "realized_profit": 100000,
            "unrealized_profit": 400000,
            "total_profit": 500000,
            "profit_rate": 5.26,
        }
        return tool

    @pytest.fixture
    def mock_purchasable_tool(self):
        """Mock purchasable amount tool."""
        tool = Mock()
        tool.name = "get_purchasable_amount"
        tool.func.return_value = {"purchasable_amount": 1900000, "margin_ratio": 40}
        return tool

    @pytest.fixture
    def account_agent(self, mock_kiwoom_client, mock_llm):
        """Create AccountAgent instance for testing."""
        agent = AccountAgent(mock_kiwoom_client, mock_llm)
        return agent

    def test_get_agent_type(self, account_agent):
        """Test agent type identification."""
        assert account_agent._get_agent_type() == "account"

    def test_balance_request_handling(self, account_agent, mock_balance_tool):
        """Test handling of balance requests."""
        account_agent.tools = [mock_balance_tool]

        result = account_agent.process_request("내 계좌 잔고를 알려줘")

        assert "total_asset" in result
        assert result["total_asset"] == 10000000
        mock_balance_tool.func.assert_called_once()

    def test_holdings_request_handling(self, account_agent, mock_holdings_tool):
        """Test handling of holdings requests."""
        account_agent.tools = [mock_holdings_tool]

        result = account_agent.process_request("보유종목을 알려줘")

        assert isinstance(result, list)
        assert len(result) > 0
        assert result[0]["stock_name"] == "삼성전자"
        mock_holdings_tool.func.assert_called_once()

    def test_profit_loss_request_handling(self, account_agent, mock_profit_loss_tool):
        """Test handling of profit/loss requests."""
        account_agent.tools = [mock_profit_loss_tool]

        result = account_agent.process_request("손익을 확인하고 싶어")

        assert "total_profit" in result
        assert result["total_profit"] == 500000
        mock_profit_loss_tool.func.assert_called_once()

    def test_purchasable_amount_request_handling(self, account_agent, mock_purchasable_tool):
        """Test handling of purchasable amount requests."""
        account_agent.tools = [mock_purchasable_tool]

        result = account_agent.process_request("매수가능금액이 얼마야?")

        assert "purchasable_amount" in result
        assert result["purchasable_amount"] == 1900000
        mock_purchasable_tool.func.assert_called_once()

    def test_default_to_balance_request(self, account_agent, mock_balance_tool):
        """Test that unclear requests default to balance inquiry."""
        account_agent.tools = [mock_balance_tool]

        result = account_agent.process_request("내 계좌 상황은?")

        assert "total_asset" in result
        mock_balance_tool.func.assert_called_once()

    def test_tool_not_available_error(self, account_agent):
        """Test error handling when tool is not available."""
        account_agent.tools = []  # No tools available

        result = account_agent.process_request("내 계좌 잔고를 알려줘")

        assert "error" in result
        assert "not available" in result["error"]

    def test_tool_execution_error(self, account_agent, mock_balance_tool):
        """Test error handling when tool execution fails."""
        mock_balance_tool.func.side_effect = Exception("API Error")
        account_agent.tools = [mock_balance_tool]

        result = account_agent.process_request("내 계좌 잔고를 알려줘")

        assert "error" in result
        assert "Failed to get account balance" in result["error"]

    def test_account_number_extraction(self, account_agent):
        """Test account number extraction from parameters."""
        params = {"account_number": "12345678"}

        account_number = account_agent._extract_account_number(params)

        assert account_number == "12345678"

    def test_account_number_extraction_none_params(self, account_agent):
        """Test account number extraction with None parameters."""
        account_number = account_agent._extract_account_number(None)

        assert account_number is None

    def test_keyword_matching_balance(self, account_agent, mock_balance_tool):
        """Test keyword matching for balance requests."""
        account_agent.tools = [mock_balance_tool]

        test_cases = ["잔고", "예수금", "총자산", "평가금액"]

        for keyword in test_cases:
            result = account_agent.process_request(f"내 {keyword}을 보여줘")
            assert "total_asset" in result

    def test_keyword_matching_holdings(self, account_agent, mock_holdings_tool):
        """Test keyword matching for holdings requests."""
        account_agent.tools = [mock_holdings_tool]

        test_cases = ["보유", "종목", "포트폴리오"]

        for keyword in test_cases:
            result = account_agent.process_request(f"내 {keyword}을 보여줘")
            assert isinstance(result, list)


class TestChartAgent:
    """Test cases for ChartAgent."""

    @pytest.fixture
    def mock_kiwoom_client(self):
        """Mock Kiwoom client for testing."""
        return Mock()

    @pytest.fixture
    def mock_llm(self):
        """Mock language model for testing."""
        return Mock()

    @pytest.fixture
    def mock_daily_chart_tool(self):
        """Mock daily chart tool."""
        tool = Mock()
        tool.name = "get_daily_chart"
        tool.func.return_value = [
            {"date": "20240101", "open": 70000, "high": 72000, "low": 69000, "close": 71000, "volume": 1000000}
        ]
        return tool

    @pytest.fixture
    def mock_minute_chart_tool(self):
        """Mock minute chart tool."""
        tool = Mock()
        tool.name = "get_minute_chart"
        tool.func.return_value = [
            {"time": "0900", "open": 70000, "high": 70500, "low": 69500, "close": 70200, "volume": 50000}
        ]
        return tool

    @pytest.fixture
    def mock_current_price_tool(self):
        """Mock current price tool."""
        tool = Mock()
        tool.name = "get_current_price"
        tool.func.return_value = {"current_price": 71000, "change": 1000, "change_rate": 1.43, "volume": 1000000}
        return tool

    @pytest.fixture
    def mock_ranking_tool(self):
        """Mock ranking tool."""
        tool = Mock()
        tool.name = "get_price_volume_rank"
        tool.func.return_value = [{"rank": 1, "stock_code": "005930", "stock_name": "삼성전자", "volume": 5000000}]
        return tool

    @pytest.fixture
    def chart_agent(self, mock_kiwoom_client, mock_llm):
        """Create ChartAgent instance for testing."""
        agent = ChartAgent(mock_kiwoom_client, mock_llm)
        return agent

    def test_get_agent_type(self, chart_agent):
        """Test agent type identification."""
        assert chart_agent._get_agent_type() == "chart"

    def test_daily_chart_request_handling(self, chart_agent, mock_daily_chart_tool):
        """Test handling of daily chart requests."""
        chart_agent.tools = [mock_daily_chart_tool]
        params = {"stock_code": "005930"}

        result = chart_agent.process_request("삼성전자 일봉 차트", params)

        assert isinstance(result, list)
        assert len(result) > 0
        assert result[0]["date"] == "20240101"
        mock_daily_chart_tool.func.assert_called_once()

    def test_minute_chart_request_handling(self, chart_agent, mock_minute_chart_tool):
        """Test handling of minute chart requests."""
        chart_agent.tools = [mock_minute_chart_tool]
        params = {"stock_code": "005930", "interval": "5", "count": "100"}

        result = chart_agent.process_request("삼성전자 5분봉", params)

        assert isinstance(result, list)
        assert len(result) > 0
        assert result[0]["time"] == "0900"
        mock_minute_chart_tool.func.assert_called_with("005930", 5, 100)

    def test_current_price_request_handling(self, chart_agent, mock_current_price_tool):
        """Test handling of current price requests."""
        chart_agent.tools = [mock_current_price_tool]
        params = {"stock_code": "005930"}

        result = chart_agent.process_request("삼성전자 현재가", params)

        assert "current_price" in result
        assert result["current_price"] == 71000
        mock_current_price_tool.func.assert_called_once()

    def test_ranking_request_handling(self, chart_agent, mock_ranking_tool):
        """Test handling of ranking requests."""
        chart_agent.tools = [mock_ranking_tool]
        params = {"market": "KOSPI", "rank_type": "volume"}

        result = chart_agent.process_request("거래량 순위", params)

        assert isinstance(result, list)
        assert len(result) > 0
        assert result[0]["rank"] == 1
        mock_ranking_tool.func.assert_called_with("KOSPI", "volume")

    def test_missing_stock_code_error(self, chart_agent):
        """Test error when stock code is missing."""
        result = chart_agent.process_request("차트를 보여줘", {})

        assert "error" in result
        assert "종목코드가 필요합니다" in result["error"]

    def test_stock_code_extraction(self, chart_agent):
        """Test stock code extraction from parameters."""
        params = {"stock_code": "005930"}

        stock_code = chart_agent._extract_stock_code(params)

        assert stock_code == "005930"

    def test_stock_code_extraction_from_name(self, chart_agent):
        """Test stock code extraction from stock name."""
        params = {"stock_name": "삼성전자", "stock_code": "005930"}

        stock_code = chart_agent._extract_stock_code(params)

        assert stock_code == "005930"

    def test_default_to_daily_chart(self, chart_agent, mock_daily_chart_tool):
        """Test that unclear chart requests default to daily chart."""
        chart_agent.tools = [mock_daily_chart_tool]
        params = {"stock_code": "005930"}

        result = chart_agent.process_request("삼성전자 차트", params)

        assert isinstance(result, list)
        mock_daily_chart_tool.func.assert_called_once()

    def test_tool_not_available_error(self, chart_agent):
        """Test error handling when tool is not available."""
        chart_agent.tools = []  # No tools available
        params = {"stock_code": "005930"}

        result = chart_agent.process_request("삼성전자 일봉", params)

        assert isinstance(result, list)
        assert "error" in result[0]
        assert "not available" in result[0]["error"]

    def test_tool_execution_error(self, chart_agent, mock_daily_chart_tool):
        """Test error handling when tool execution fails."""
        mock_daily_chart_tool.func.side_effect = Exception("API Error")
        chart_agent.tools = [mock_daily_chart_tool]
        params = {"stock_code": "005930"}

        result = chart_agent.process_request("삼성전자 일봉", params)

        assert isinstance(result, list)
        assert "error" in result[0]
        assert "Failed to get daily chart" in result[0]["error"]

    def test_keyword_matching_daily_chart(self, chart_agent, mock_daily_chart_tool):
        """Test keyword matching for daily chart requests."""
        chart_agent.tools = [mock_daily_chart_tool]
        params = {"stock_code": "005930"}

        test_cases = ["일봉", "daily", "일간"]

        for keyword in test_cases:
            result = chart_agent.process_request(f"삼성전자 {keyword}", params)
            assert isinstance(result, list)

    def test_keyword_matching_minute_chart(self, chart_agent, mock_minute_chart_tool):
        """Test keyword matching for minute chart requests."""
        chart_agent.tools = [mock_minute_chart_tool]
        params = {"stock_code": "005930"}

        test_cases = ["분봉", "minute", "분간"]

        for keyword in test_cases:
            result = chart_agent.process_request(f"삼성전자 {keyword}", params)
            assert isinstance(result, list)

    def test_keyword_matching_current_price(self, chart_agent, mock_current_price_tool):
        """Test keyword matching for current price requests."""
        chart_agent.tools = [mock_current_price_tool]
        params = {"stock_code": "005930"}

        test_cases = ["현재가", "시세", "호가"]

        for keyword in test_cases:
            result = chart_agent.process_request(f"삼성전자 {keyword}", params)
            assert "current_price" in result

    def test_period_parameter_extraction(self, chart_agent, mock_daily_chart_tool):
        """Test period parameter extraction for daily charts."""
        chart_agent.tools = [mock_daily_chart_tool]
        params = {"stock_code": "005930", "period": "60"}

        chart_agent.process_request("삼성전자 일봉", params)

        mock_daily_chart_tool.func.assert_called_with("005930", 60)

    def test_invalid_period_parameter(self, chart_agent, mock_daily_chart_tool):
        """Test handling of invalid period parameter."""
        chart_agent.tools = [mock_daily_chart_tool]
        params = {"stock_code": "005930", "period": "invalid"}

        chart_agent.process_request("삼성전자 일봉", params)

        # Should use default period of 30
        mock_daily_chart_tool.func.assert_called_with("005930", 30)

    def test_interval_and_count_parameters(self, chart_agent, mock_minute_chart_tool):
        """Test interval and count parameter extraction for minute charts."""
        chart_agent.tools = [mock_minute_chart_tool]
        params = {"stock_code": "005930", "interval": "10", "count": "200"}

        chart_agent.process_request("삼성전자 분봉", params)

        mock_minute_chart_tool.func.assert_called_with("005930", 10, 200)

    def test_default_parameters_minute_chart(self, chart_agent, mock_minute_chart_tool):
        """Test default parameters for minute chart when not specified."""
        chart_agent.tools = [mock_minute_chart_tool]
        params = {"stock_code": "005930"}

        chart_agent.process_request("삼성전자 분봉", params)

        # Should use defaults: interval=5, count=100
        mock_minute_chart_tool.func.assert_called_with("005930", 5, 100)

    def test_ranking_default_parameters(self, chart_agent, mock_ranking_tool):
        """Test default parameters for ranking requests."""
        chart_agent.tools = [mock_ranking_tool]

        chart_agent.process_request("거래량 순위")

        # Should use defaults: market="ALL", rank_type="volume"
        mock_ranking_tool.func.assert_called_with("ALL", "volume")
