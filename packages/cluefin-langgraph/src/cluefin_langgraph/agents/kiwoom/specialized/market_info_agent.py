"""Market info agent for Kiwoom market information operations."""

from typing import Any, Dict, List, Optional

from langchain.tools import Tool

from ..base.base_agent import BaseKiwoomAgent
from ..base.kiwoom_tools import KiwoomToolFactory


class MarketInfoAgent(BaseKiwoomAgent):
    """Specialized agent for market-wide information operations.
    
    This agent handles:
    - Short selling data (공매도)
    - Institutional/foreign trading data (기관/외국인)
    - Lending/borrowing data (대차거래)
    - Ranking information (순위정보)
    - Sector performance (업종)
    - Market indices and overall market data
    """

    def _get_agent_type(self) -> str:
        return "market_info"

    def _initialize_tools(self) -> List[Tool]:
        factory = KiwoomToolFactory(self.kiwoom_client)
        return factory.create_market_info_tools()

    def process_request(
        self,
        request: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Process market information requests.

        Args:
            request: User's original request
            params: Extracted parameters from intent classification

        Returns:
            Market information operation results
        """
        self._log(f"Processing market info request: {request}")

        request_lower = request.lower()

        # Handle short selling requests (공매도)
        if any(keyword in request_lower for keyword in ["공매도", "short", "숏", "공매"]):
            return self._handle_short_selling_request(params)

        # Handle institutional/foreign trading requests (기관/외국인)
        elif any(keyword in request_lower for keyword in ["기관", "외국인", "institutional", "foreign", "순매수", "순매도"]):
            return self._handle_institutional_trading_request(params)

        # Handle lending/borrowing requests (대차거래)
        elif any(keyword in request_lower for keyword in ["대차거래", "대차", "lending", "borrowing"]):
            return self._handle_lending_borrowing_request(params)

        # Handle ranking requests (순위정보)
        elif any(keyword in request_lower for keyword in ["순위", "상위", "ranking", "top", "랭킹"]):
            return self._handle_ranking_request(params)

        # Handle sector performance requests (업종)
        elif any(keyword in request_lower for keyword in ["업종", "섹터", "sector", "업종별", "섹터별"]):
            return self._handle_sector_performance_request(params)

        # Handle market index requests (지수)
        elif any(keyword in request_lower for keyword in ["지수", "코스피", "코스닥", "index", "kospi", "kosdaq"]):
            return self._handle_market_index_request(params)

        else:
            return {"error": "요청 유형을 인식할 수 없습니다. 공매도, 기관/외국인, 대차거래, 순위, 업종, 지수 중 하나를 선택해주세요."}

    def _handle_short_selling_request(self, params: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Handle short selling information requests.

        Args:
            params: Parameters that may contain stock code or market filter

        Returns:
            Short selling data
        """
        self._log("Handling short selling request")

        short_selling_tool = next((tool for tool in self.tools if tool.name == "get_short_selling_info"), None)

        if short_selling_tool:
            try:
                # Extract stock code if provided, otherwise get market-wide data
                stock_code = self._extract_stock_code(params) if params else None
                result = short_selling_tool.func(stock_code)
                return result if isinstance(result, list) else [result]
            except Exception as e:
                return [{"error": f"Failed to get short selling info: {str(e)}"}]
        else:
            return [{"error": "Short selling tool not available"}]

    def _handle_institutional_trading_request(self, params: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Handle institutional/foreign trading requests.

        Args:
            params: Parameters that may contain trading type or market filter

        Returns:
            Institutional trading data
        """
        self._log("Handling institutional trading request")

        institutional_tool = next((tool for tool in self.tools if tool.name == "get_institutional_trading"), None)

        if institutional_tool:
            try:
                # Extract trading type (buy/sell) and investor type (institutional/foreign)
                trading_type = params.get("trading_type", "net") if params else "net"
                investor_type = params.get("investor_type", "all") if params else "all"
                result = institutional_tool.func(trading_type, investor_type)
                return result if isinstance(result, list) else [result]
            except Exception as e:
                return [{"error": f"Failed to get institutional trading info: {str(e)}"}]
        else:
            return [{"error": "Institutional trading tool not available"}]

    def _handle_lending_borrowing_request(self, params: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Handle lending/borrowing information requests.

        Args:
            params: Parameters that may contain stock code or market filter

        Returns:
            Lending/borrowing data
        """
        self._log("Handling lending/borrowing request")

        lending_tool = next((tool for tool in self.tools if tool.name == "get_lending_borrowing_info"), None)

        if lending_tool:
            try:
                # Extract stock code if provided, otherwise get market-wide data
                stock_code = self._extract_stock_code(params) if params else None
                result = lending_tool.func(stock_code)
                return result if isinstance(result, list) else [result]
            except Exception as e:
                return [{"error": f"Failed to get lending/borrowing info: {str(e)}"}]
        else:
            return [{"error": "Lending/borrowing tool not available"}]

    def _handle_ranking_request(self, params: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Handle ranking information requests.

        Args:
            params: Parameters that may contain market and rank type

        Returns:
            Ranking data
        """
        self._log("Handling ranking request")

        # Extract market and rank type from parameters
        market = "ALL"
        rank_type = "volume"

        if params:
            market = params.get("market", "ALL")
            rank_type = params.get("rank_type", "volume")

        ranking_tool = next((tool for tool in self.tools if tool.name == "get_price_volume_rank"), None)

        if ranking_tool:
            try:
                result = ranking_tool.func(market, rank_type)
                return result if isinstance(result, list) else [result]
            except Exception as e:
                return [{"error": f"Failed to get ranking: {str(e)}"}]
        else:
            return [{"error": "Ranking tool not available"}]

    def _handle_sector_performance_request(self, params: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Handle sector performance requests.

        Args:
            params: Parameters that may contain date or sector filter

        Returns:
            Sector performance data
        """
        self._log("Handling sector performance request")

        sector_performance_tool = next((tool for tool in self.tools if tool.name == "get_sector_performance"), None)

        if sector_performance_tool:
            try:
                # Extract date if provided
                date = params.get("date") if params else None
                result = sector_performance_tool.func(date)
                return result if isinstance(result, list) else [result]
            except Exception as e:
                return [{"error": f"Failed to get sector performance: {str(e)}"}]
        else:
            return [{"error": "Sector performance tool not available"}]

    def _handle_market_index_request(self, params: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Handle market index requests.

        Args:
            params: Parameters that may contain index code

        Returns:
            Market index data
        """
        self._log("Handling market index request")

        index_tool = next((tool for tool in self.tools if tool.name == "get_market_index"), None)

        if index_tool:
            try:
                # Extract index code if provided, default to KOSPI
                index_code = params.get("index_code", "0001") if params else "0001"
                result = index_tool.func(index_code)
                return result
            except Exception as e:
                return {"error": f"Failed to get market index: {str(e)}"}
        else:
            return {"error": "Market index tool not available"}
