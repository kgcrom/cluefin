"""Market info agent for Kiwoom market information operations."""

from typing import Any, Dict, List, Optional

from langchain.tools import Tool

from ..base.base_agent import BaseKiwoomAgent
from ..base.kiwoom_tools import KiwoomToolFactory


class MarketInfoAgent(BaseKiwoomAgent):
    """Specialized agent for market information operations."""
    
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
        self._log(f"Processing market info request: {request}")
        
        request_lower = request.lower()
        
        if any(keyword in request_lower for keyword in ["종목정보", "기업정보", "info"]):
            stock_code = self._extract_stock_code(params)
            if not stock_code:
                return {"error": "종목코드가 필요합니다."}
            
            info_tool = next(
                (tool for tool in self.tools if tool.name == "get_stock_info"), None
            )
            if info_tool:
                try:
                    return info_tool.func(stock_code)
                except Exception as e:
                    return {"error": f"Failed to get stock info: {str(e)}"}
            else:
                return {"error": "Stock info tool not available"}
        
        elif any(keyword in request_lower for keyword in ["검색", "search"]):
            stock_name = params.get("stock_name") if params else None
            if not stock_name:
                return {"error": "검색할 종목명이 필요합니다."}
            
            search_tool = next(
                (tool for tool in self.tools if tool.name == "search_stock_by_name"), None
            )
            if search_tool:
                try:
                    result = search_tool.func(stock_name)
                    return result if isinstance(result, list) else [result]
                except Exception as e:
                    return [{"error": f"Failed to search stock: {str(e)}"}]
            else:
                return [{"error": "Stock search tool not available"}]
        
        elif any(keyword in request_lower for keyword in ["지수", "코스피", "코스닥"]):
            index_tool = next(
                (tool for tool in self.tools if tool.name == "get_market_index"), None
            )
            if index_tool:
                try:
                    return index_tool.func()
                except Exception as e:
                    return {"error": f"Failed to get market index: {str(e)}"}
            else:
                return {"error": "Market index tool not available"}
        
        elif any(keyword in request_lower for keyword in ["섹터", "업종"]):
            sector_tool = next(
                (tool for tool in self.tools if tool.name == "get_sector_info"), None
            )
            if sector_tool:
                try:
                    result = sector_tool.func()
                    return result if isinstance(result, list) else [result]
                except Exception as e:
                    return [{"error": f"Failed to get sector info: {str(e)}"}]
            else:
                return [{"error": "Sector info tool not available"}]
        
        else:
            return {"error": "요청 유형을 인식할 수 없습니다. 종목정보, 검색, 지수, 섹터 중 하나를 선택해주세요."}
EOF < /dev/null