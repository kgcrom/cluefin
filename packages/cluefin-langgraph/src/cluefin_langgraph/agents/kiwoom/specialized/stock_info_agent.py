"""Stock info agent for Kiwoom stock information operations."""

from typing import Any, Dict, List, Optional

from langchain.tools import Tool

from ..base.base_agent import BaseKiwoomAgent
from ..base.kiwoom_tools import KiwoomToolFactory


class StockInfoAgent(BaseKiwoomAgent):
    """Specialized agent for stock information operations.

    This agent handles:
    - Basic stock information (company overview and key metrics)
    - Financial data (financial statements and ratios)
    - Stock search by name
    - Stock fundamentals (valuation metrics and analysis)
    - ETF information and NAV data
    """

    def _get_agent_type(self) -> str:
        """Return the agent type identifier."""
        return "stock_info"

    def _initialize_tools(self) -> List[Tool]:
        """Initialize stock information tools.

        Returns:
            List of stock information tools
        """
        factory = KiwoomToolFactory(self.kiwoom_client)
        return factory.create_stock_info_tools()

    def process_request(
        self,
        request: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Process stock information requests.

        Args:
            request: User's original request
            params: Extracted parameters from intent classification

        Returns:
            Stock information results
        """
        self._log(f"Processing stock info request: {request}")

        request_lower = request.lower()

        # Handle stock search requests
        if any(keyword in request_lower for keyword in ["검색", "search", "찾기", "종목명"]):
            return self._handle_stock_search_request(params)

        # Handle ETF information requests
        elif any(keyword in request_lower for keyword in ["etf", "상장지수펀드", "nav", "순자산가치"]):
            return self._handle_etf_request(request_lower, params)

        # Handle financial data requests
        elif any(keyword in request_lower for keyword in ["재무", "재무제표", "financial", "손익계산서", "대차대조표"]):
            return self._handle_financial_data_request(params)

        # Handle fundamentals requests
        elif any(keyword in request_lower for keyword in ["펀더멘털", "fundamental", "밸류에이션", "per", "pbr", "배당"]):
            return self._handle_fundamentals_request(params)

        # Handle basic stock info requests (default)
        else:
            return self._handle_stock_info_request(params)

    def _handle_stock_search_request(self, params: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Handle stock search by name requests.

        Args:
            params: Parameters containing stock name to search

        Returns:
            List of matching stocks with codes and basic info
        """
        self._log("Handling stock search request")

        # Extract stock name from parameters
        stock_name = None
        if params:
            for key in ["stock_name", "name", "종목명", "회사명"]:
                if key in params:
                    stock_name = params[key]
                    break

        if not stock_name:
            return [{"error": "검색할 종목명이 필요합니다."}]

        # Use the search_stock_by_name tool
        search_tool = next((tool for tool in self.tools if tool.name == "search_stock_by_name"), None)

        if search_tool:
            try:
                result = search_tool.func(stock_name)
                return result if isinstance(result, list) else [result]
            except Exception as e:
                return [{"error": f"종목 검색 실패: {str(e)}"}]
        else:
            return [{"error": "종목 검색 도구를 사용할 수 없습니다."}]

    def _handle_stock_info_request(self, params: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Handle basic stock information requests.

        Args:
            params: Parameters containing stock code

        Returns:
            Basic stock information including company overview and key metrics
        """
        self._log("Handling stock info request")

        stock_code = self._extract_stock_code(params)
        if not stock_code:
            return {"error": "종목코드가 필요합니다."}

        # Use the get_stock_info tool
        info_tool = next((tool for tool in self.tools if tool.name == "get_stock_info"), None)

        if info_tool:
            try:
                result = info_tool.func(stock_code)
                return result
            except Exception as e:
                return {"error": f"종목 정보 조회 실패: {str(e)}"}
        else:
            return {"error": "종목 정보 조회 도구를 사용할 수 없습니다."}

    def _handle_financial_data_request(self, params: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Handle financial data requests.

        Args:
            params: Parameters containing stock code

        Returns:
            Financial statements and ratios
        """
        self._log("Handling financial data request")

        stock_code = self._extract_stock_code(params)
        if not stock_code:
            return {"error": "종목코드가 필요합니다."}

        # Use the get_stock_financial_data tool if available
        financial_tool = next((tool for tool in self.tools if tool.name == "get_stock_financial_data"), None)

        if financial_tool:
            try:
                result = financial_tool.func(stock_code)
                return result
            except Exception as e:
                return {"error": f"재무 데이터 조회 실패: {str(e)}"}
        else:
            # Fallback to basic stock info which may include some financial metrics
            return self._handle_stock_info_request(params)

    def _handle_fundamentals_request(self, params: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Handle stock fundamentals requests.

        Args:
            params: Parameters containing stock code

        Returns:
            Valuation metrics and analysis
        """
        self._log("Handling fundamentals request")

        stock_code = self._extract_stock_code(params)
        if not stock_code:
            return {"error": "종목코드가 필요합니다."}

        # Use the get_stock_fundamentals tool if available
        fundamentals_tool = next((tool for tool in self.tools if tool.name == "get_stock_fundamentals"), None)

        if fundamentals_tool:
            try:
                result = fundamentals_tool.func(stock_code)
                return result
            except Exception as e:
                return {"error": f"펀더멘털 분석 실패: {str(e)}"}
        else:
            # Fallback to basic stock info which includes key metrics
            return self._handle_stock_info_request(params)

    def _handle_etf_request(self, request_lower: str, params: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Handle ETF information requests.

        Args:
            request_lower: Lowercase request string for keyword matching
            params: Parameters containing ETF code

        Returns:
            ETF information or NAV data
        """
        self._log("Handling ETF request")

        etf_code = self._extract_stock_code(params)
        if not etf_code:
            return {"error": "ETF 코드가 필요합니다."}

        # Handle NAV requests specifically
        if any(keyword in request_lower for keyword in ["nav", "순자산가치", "괴리율"]):
            return self._handle_etf_nav_request(etf_code)
        else:
            return self._handle_etf_info_request(etf_code)

    def _handle_etf_info_request(self, etf_code: str) -> Dict[str, Any]:
        """Handle ETF basic information requests.

        Args:
            etf_code: ETF code to query

        Returns:
            ETF basic information and composition
        """
        self._log(f"Handling ETF info request for {etf_code}")

        # Use the get_etf_info tool
        etf_info_tool = next((tool for tool in self.tools if tool.name == "get_etf_info"), None)

        if etf_info_tool:
            try:
                result = etf_info_tool.func(etf_code)
                return result
            except Exception as e:
                return {"error": f"ETF 정보 조회 실패: {str(e)}"}
        else:
            return {"error": "ETF 정보 조회 도구를 사용할 수 없습니다."}

    def _handle_etf_nav_request(self, etf_code: str) -> Dict[str, Any]:
        """Handle ETF NAV requests.

        Args:
            etf_code: ETF code to query

        Returns:
            ETF NAV and premium/discount information
        """
        self._log(f"Handling ETF NAV request for {etf_code}")

        # Use the get_etf_nav tool
        etf_nav_tool = next((tool for tool in self.tools if tool.name == "get_etf_nav"), None)

        if etf_nav_tool:
            try:
                result = etf_nav_tool.func(etf_code)
                return result
            except Exception as e:
                return {"error": f"ETF NAV 조회 실패: {str(e)}"}
        else:
            return {"error": "ETF NAV 조회 도구를 사용할 수 없습니다."}

    def _extract_stock_code(self, params: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """Extract stock code from parameters.

        Args:
            params: Parameters that may contain stock code

        Returns:
            Stock code or None if not available
        """
        if not params:
            return None

        # Try different possible parameter names for stock/ETF codes
        for key in ["stock_code", "etf_code", "symbol", "code", "종목코드", "종목", "etf"]:
            if key in params:
                return params[key]

        return None