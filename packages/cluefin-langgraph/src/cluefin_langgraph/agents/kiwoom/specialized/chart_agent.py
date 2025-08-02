"""Chart agent for Kiwoom chart operations."""

from typing import Any, Dict, List, Optional

from langchain.tools import Tool

from ..base.base_agent import BaseKiwoomAgent
from ..base.kiwoom_tools import KiwoomToolFactory


class ChartAgent(BaseKiwoomAgent):
    """Specialized agent for chart and price data operations.
    
    This agent handles:
    - Daily/minute chart data retrieval
    - Current price queries
    - Price/volume rankings
    - Technical analysis data
    """
    
    def _get_agent_type(self) -> str:
        """Return the agent type identifier."""
        return "chart"
    
    def _initialize_tools(self) -> List[Tool]:
        """Initialize chart-specific tools.
        
        Returns:
            List of chart data tools
        """
        factory = KiwoomToolFactory(self.kiwoom_client)
        return factory.create_chart_tools()
    
    def process_request(
        self,
        request: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Process chart-related requests.
        
        Args:
            request: User's original request
            params: Extracted parameters from intent classification
            
        Returns:
            Chart operation results
        """
        self._log(f"Processing chart request: {request}")
        
        # Extract stock code from parameters
        stock_code = self._extract_stock_code(params)
        
        if not stock_code:
            return {"error": "종목코드가 필요합니다. 종목명 또는 종목코드를 입력해주세요."}
        
        # Determine the type of chart operation needed
        request_lower = request.lower()
        
        if any(keyword in request_lower for keyword in ["일봉", "daily", "일간"]):
            return self._handle_daily_chart_request(stock_code, params)
        
        elif any(keyword in request_lower for keyword in ["분봉", "minute", "분간"]):
            return self._handle_minute_chart_request(stock_code, params)
        
        elif any(keyword in request_lower for keyword in ["현재가", "시세", "호가"]):
            return self._handle_current_price_request(stock_code)
        
        elif any(keyword in request_lower for keyword in ["순위", "상위", "ranking"]):
            return self._handle_ranking_request(params)
        
        else:
            # Default to daily chart
            return self._handle_daily_chart_request(stock_code, params)
    
    def _handle_daily_chart_request(
        self, stock_code: str, params: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Handle daily chart requests."""
        self._log(f"Handling daily chart request for {stock_code}")
        
        # Extract period from parameters (default 30 days)
        period = 30
        if params and "period" in params:
            try:
                period = int(params["period"])
            except (ValueError, TypeError):
                period = 30
        
        daily_chart_tool = next(
            (tool for tool in self.tools if tool.name == "get_daily_chart"), None
        )
        
        if daily_chart_tool:
            try:
                result = daily_chart_tool.func(stock_code, period)
                return result if isinstance(result, list) else [result]
            except Exception as e:
                return [{"error": f"Failed to get daily chart: {str(e)}"}]
        else:
            return [{"error": "Daily chart tool not available"}]
    
    def _handle_minute_chart_request(
        self, stock_code: str, params: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Handle minute chart requests."""
        self._log(f"Handling minute chart request for {stock_code}")
        
        # Extract interval and count from parameters
        interval = 5  # Default 5-minute
        count = 100   # Default 100 records
        
        if params:
            if "interval" in params:
                try:
                    interval = int(params["interval"])
                except (ValueError, TypeError):
                    interval = 5
            if "count" in params:
                try:
                    count = int(params["count"])
                except (ValueError, TypeError):
                    count = 100
        
        minute_chart_tool = next(
            (tool for tool in self.tools if tool.name == "get_minute_chart"), None
        )
        
        if minute_chart_tool:
            try:
                result = minute_chart_tool.func(stock_code, interval, count)
                return result if isinstance(result, list) else [result]
            except Exception as e:
                return [{"error": f"Failed to get minute chart: {str(e)}"}]
        else:
            return [{"error": "Minute chart tool not available"}]
    
    def _handle_current_price_request(self, stock_code: str) -> Dict[str, Any]:
        """Handle current price requests."""
        self._log(f"Handling current price request for {stock_code}")
        
        current_price_tool = next(
            (tool for tool in self.tools if tool.name == "get_current_price"), None
        )
        
        if current_price_tool:
            try:
                result = current_price_tool.func(stock_code)
                return result
            except Exception as e:
                return {"error": f"Failed to get current price: {str(e)}"}
        else:
            return {"error": "Current price tool not available"}
    
    def _handle_ranking_request(
        self, params: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Handle ranking requests."""
        self._log("Handling ranking request")
        
        # Extract market and rank type from parameters
        market = "ALL"
        rank_type = "volume"
        
        if params:
            market = params.get("market", "ALL")
            rank_type = params.get("rank_type", "volume")
        
        ranking_tool = next(
            (tool for tool in self.tools if tool.name == "get_price_volume_rank"), None
        )
        
        if ranking_tool:
            try:
                result = ranking_tool.func(market, rank_type)
                return result if isinstance(result, list) else [result]
            except Exception as e:
                return [{"error": f"Failed to get ranking: {str(e)}"}]
        else:
            return [{"error": "Ranking tool not available"}]