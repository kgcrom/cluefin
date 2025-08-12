"""Theme/Sector agent for Kiwoom theme and sector operations."""

from typing import Any, Dict, List, Optional

from langchain.tools import Tool

from ..base.base_agent import BaseKiwoomAgent
from ..base.kiwoom_tools import KiwoomToolFactory


class ThemeSectorAgent(BaseKiwoomAgent):
    """Specialized agent for theme and sector-related operations.

    This agent handles:
    - Theme stock discovery and analysis
    - Sector performance tracking
    - Hot theme identification
    - Industry trend analysis
    """

    def _get_agent_type(self) -> str:
        """Return the agent type identifier."""
        return "theme_sector"

    def _initialize_tools(self) -> List[Tool]:
        """Initialize theme/sector-specific tools.

        Returns:
            List of theme and sector management tools
        """
        factory = KiwoomToolFactory(self.kiwoom_client)
        return factory.create_theme_sector_tools()

    def process_request(
        self,
        request: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Process theme/sector-related requests.

        Args:
            request: User's original request
            params: Extracted parameters from intent classification

        Returns:
            Theme/sector operation results
        """
        self._log(f"Processing theme/sector request: {request}")

        # Determine the type of theme/sector operation needed
        request_lower = request.lower()

        if any(keyword in request_lower for keyword in ["테마주", "테마 종목", "관련주", "테마별"]):
            theme_name = self._extract_theme_name(params, request)
            return self._handle_theme_stocks_request(theme_name)

        elif any(keyword in request_lower for keyword in ["섹터", "업종", "산업", "성과", "수익률"]):
            sector = self._extract_sector(params, request)
            return self._handle_sector_performance_request(sector)

        elif any(keyword in request_lower for keyword in ["핫", "인기", "주목", "상승", "급등", "트렌드"]):
            return self._handle_hot_themes_request()

        else:
            # Default to hot themes if no specific theme/sector is mentioned
            theme_name = self._extract_theme_name(params, request)
            if theme_name:
                return self._handle_theme_stocks_request(theme_name)
            else:
                return self._handle_hot_themes_request()

    def _handle_theme_stocks_request(self, theme_name: Optional[str]) -> List[Dict[str, Any]]:
        """Handle theme stocks requests.

        Args:
            theme_name: Name of the theme to query

        Returns:
            List of stocks in the theme
        """
        self._log(f"Handling theme stocks request for {theme_name}")

        if not theme_name:
            return [{"error": "테마명이 필요합니다"}]

        # Use the get_theme_stocks tool
        theme_tool = next((tool for tool in self.tools if tool.name == "get_theme_stocks"), None)

        if theme_tool:
            try:
                result = theme_tool.func(theme_name)
                return result if isinstance(result, list) else [result]
            except Exception as e:
                return [{"error": f"Failed to get theme stocks: {str(e)}"}]
        else:
            return [{"error": "Theme stocks tool not available"}]

    def _handle_sector_performance_request(self, sector: Optional[str]) -> List[Dict[str, Any]]:
        """Handle sector performance requests.

        Args:
            sector: Sector to analyze (optional, None for all sectors)

        Returns:
            Sector performance information
        """
        self._log(f"Handling sector performance request for {sector}")

        # Use the get_sector_performance tool
        sector_tool = next((tool for tool in self.tools if tool.name == "get_sector_performance"), None)

        if sector_tool:
            try:
                # Pass sector as date parameter if needed, or modify based on actual API
                result = sector_tool.func()

                # Filter by sector if specified
                if sector and isinstance(result, list):
                    filtered = [item for item in result if self._matches_sector(item, sector)]
                    return filtered if filtered else result

                return result if isinstance(result, list) else [result]
            except Exception as e:
                return [{"error": f"Failed to get sector performance: {str(e)}"}]
        else:
            return [{"error": "Sector performance tool not available"}]

    def _handle_hot_themes_request(self) -> List[Dict[str, Any]]:
        """Handle hot themes requests.

        Returns:
            List of currently hot themes
        """
        self._log("Handling hot themes request")

        # Use the get_hot_themes tool
        hot_themes_tool = next((tool for tool in self.tools if tool.name == "get_hot_themes"), None)

        if hot_themes_tool:
            try:
                result = hot_themes_tool.func(limit=10)
                return result if isinstance(result, list) else [result]
            except Exception as e:
                return [{"error": f"Failed to get hot themes: {str(e)}"}]
        else:
            return [{"error": "Hot themes tool not available"}]

    def _extract_theme_name(self, params: Optional[Dict[str, Any]] = None, request: str = "") -> Optional[str]:
        """Extract theme name from parameters or request.

        Args:
            params: Parameters that may contain theme name
            request: Original request text

        Returns:
            Theme name or None if not available
        """
        # First try to get from params
        if params:
            for key in ["theme", "theme_name", "테마", "테마명"]:
                if key in params:
                    return params[key]

        # Try to extract common themes from request
        common_themes = [
            "반도체",
            "2차전지",
            "배터리",
            "바이오",
            "AI",
            "인공지능",
            "메타버스",
            "NFT",
            "블록체인",
            "자율주행",
            "전기차",
            "수소경제",
            "신재생에너지",
            "태양광",
            "풍력",
            "원전",
            "방산",
            "우주항공",
            "로봇",
            "드론",
            "5G",
            "6G",
            "OTT",
            "게임",
            "엔터테인먼트",
            "K-POP",
            "화장품",
            "제약",
            "헬스케어",
            "의료기기",
            "진단키트",
            "백신",
            "친환경",
            "ESG",
            "탄소중립",
            "순환경제",
            "리사이클링",
            "부동산",
            "건설",
            "인프라",
            "SOC",
            "리츠",
            "금융",
            "은행",
            "증권",
            "보험",
            "핀테크",
        ]

        request_lower = request.lower()
        for theme in common_themes:
            if theme.lower() in request_lower:
                return theme

        return None

    def _extract_sector(self, params: Optional[Dict[str, Any]] = None, request: str = "") -> Optional[str]:
        """Extract sector from parameters or request.

        Args:
            params: Parameters that may contain sector
            request: Original request text

        Returns:
            Sector name or None if not available
        """
        # First try to get from params
        if params:
            for key in ["sector", "업종", "섹터", "산업"]:
                if key in params:
                    return params[key]

        # Try to extract common sectors from request
        common_sectors = [
            "전기전자",
            "화학",
            "의약품",
            "기계",
            "자동차",
            "철강",
            "금속",
            "건설",
            "유통",
            "운송",
            "통신",
            "금융",
            "증권",
            "보험",
            "서비스",
            "음식료",
            "섬유",
            "종이목재",
            "비금속",
            "전기가스",
        ]

        request_lower = request.lower()
        for sector in common_sectors:
            if sector.lower() in request_lower:
                return sector

        return None

    def _matches_sector(self, item: Dict[str, Any], sector: str) -> bool:
        """Check if an item matches the specified sector.

        Args:
            item: Data item to check
            sector: Sector to match against

        Returns:
            True if the item matches the sector
        """
        sector_lower = sector.lower()

        # Check various possible field names
        for key in ["sector", "업종", "섹터", "산업", "industry"]:
            if key in item:
                if sector_lower in str(item[key]).lower():
                    return True

        return False
