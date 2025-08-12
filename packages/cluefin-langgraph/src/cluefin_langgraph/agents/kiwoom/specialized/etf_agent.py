"""ETF agent for Kiwoom ETF operations."""

from typing import Any, Dict, List, Optional

from langchain.tools import Tool

from ..base.base_agent import BaseKiwoomAgent
from ..base.kiwoom_tools import KiwoomToolFactory


class ETFAgent(BaseKiwoomAgent):
    """Specialized agent for ETF-related operations.

    This agent handles:
    - ETF information queries
    - ETF NAV and tracking error analysis
    - Theme-based ETF search
    - ETF component analysis
    """

    def _get_agent_type(self) -> str:
        """Return the agent type identifier."""
        return "etf"

    def _initialize_tools(self) -> List[Tool]:
        """Initialize ETF-specific tools.

        Returns:
            List of ETF management tools
        """
        factory = KiwoomToolFactory(self.kiwoom_client)
        return factory.create_etf_tools()

    def process_request(
        self,
        request: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Process ETF-related requests.

        Args:
            request: User's original request
            params: Extracted parameters from intent classification

        Returns:
            ETF operation results
        """
        self._log(f"Processing ETF request: {request}")

        # Extract ETF code from parameters
        etf_code = self._extract_etf_code(params)

        # Determine the type of ETF operation needed
        request_lower = request.lower()

        if any(keyword in request_lower for keyword in ["정보", "구성", "종목", "포트폴리오", "비중"]):
            return self._handle_etf_info_request(etf_code)

        elif any(keyword in request_lower for keyword in ["nav", "순자산", "괴리율", "추적오차"]):
            return self._handle_etf_nav_request(etf_code)

        elif any(keyword in request_lower for keyword in ["테마", "섹터", "검색", "찾기", "추천"]):
            theme = self._extract_theme(params, request)
            return self._handle_etf_search_request(theme)

        else:
            # Default to ETF info if ETF code is provided
            if etf_code:
                return self._handle_etf_info_request(etf_code)
            else:
                # Search for ETFs if no specific code is given
                theme = self._extract_theme(params, request)
                return self._handle_etf_search_request(theme)

    def _handle_etf_info_request(self, etf_code: Optional[str]) -> Dict[str, Any]:
        """Handle ETF information requests.

        Args:
            etf_code: ETF code to query

        Returns:
            ETF information
        """
        self._log(f"Handling ETF info request for {etf_code}")

        if not etf_code:
            return {"error": "ETF 코드가 필요합니다"}

        # Use the get_etf_info tool
        info_tool = next((tool for tool in self.tools if tool.name == "get_etf_info"), None)

        if info_tool:
            try:
                result = info_tool.func(etf_code)
                return result
            except Exception as e:
                return {"error": f"Failed to get ETF info: {str(e)}"}
        else:
            return {"error": "ETF info tool not available"}

    def _handle_etf_nav_request(self, etf_code: Optional[str]) -> Dict[str, Any]:
        """Handle ETF NAV requests.

        Args:
            etf_code: ETF code to query

        Returns:
            ETF NAV information
        """
        self._log(f"Handling ETF NAV request for {etf_code}")

        if not etf_code:
            return {"error": "ETF 코드가 필요합니다"}

        # Use the get_etf_nav tool
        nav_tool = next((tool for tool in self.tools if tool.name == "get_etf_nav"), None)

        if nav_tool:
            try:
                result = nav_tool.func(etf_code)
                return result
            except Exception as e:
                return {"error": f"Failed to get ETF NAV: {str(e)}"}
        else:
            return {"error": "ETF NAV tool not available"}

    def _handle_etf_search_request(self, theme: Optional[str]) -> List[Dict[str, Any]]:
        """Handle ETF search requests.

        Args:
            theme: Theme to search for

        Returns:
            List of matching ETFs
        """
        self._log(f"Handling ETF search request for theme: {theme}")

        if not theme:
            theme = "전체"  # Default to all ETFs

        # Use the search_etf_by_theme tool
        search_tool = next((tool for tool in self.tools if tool.name == "search_etf_by_theme"), None)

        if search_tool:
            try:
                result = search_tool.func(theme)
                return result if isinstance(result, list) else [result]
            except Exception as e:
                return [{"error": f"Failed to search ETFs: {str(e)}"}]
        else:
            return [{"error": "ETF search tool not available"}]

    def _extract_etf_code(self, params: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """Extract ETF code from parameters.

        Args:
            params: Parameters that may contain ETF code

        Returns:
            ETF code or None if not available
        """
        if not params:
            return None

        # Try different possible parameter names
        for key in ["etf_code", "code", "symbol", "종목코드", "ETF코드"]:
            if key in params:
                return params[key]

        return None

    def _extract_theme(self, params: Optional[Dict[str, Any]] = None, request: str = "") -> Optional[str]:
        """Extract theme from parameters or request.

        Args:
            params: Parameters that may contain theme
            request: Original request text

        Returns:
            Theme name or None if not available
        """
        # First try to get from params
        if params:
            for key in ["theme", "테마", "섹터", "sector", "category"]:
                if key in params:
                    return params[key]

        # Try to extract common themes from request
        common_themes = [
            "반도체",
            "배터리",
            "바이오",
            "2차전지",
            "AI",
            "인공지능",
            "자동차",
            "금융",
            "IT",
            "헬스케어",
            "엔터",
            "게임",
            "리츠",
            "원자재",
            "에너지",
            "친환경",
            "메타버스",
            "NFT",
        ]

        request_lower = request.lower()
        for theme in common_themes:
            if theme.lower() in request_lower:
                return theme

        return None
