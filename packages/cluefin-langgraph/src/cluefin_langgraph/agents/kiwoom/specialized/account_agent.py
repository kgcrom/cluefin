"""Account agent for Kiwoom account operations."""

from typing import Any, Dict, List, Optional

from langchain.tools import Tool

from ..base.base_agent import BaseKiwoomAgent
from ..base.kiwoom_tools import KiwoomToolFactory


class AccountAgent(BaseKiwoomAgent):
    """Specialized agent for account-related operations.
    
    This agent handles:
    - Account balance inquiries
    - Holdings retrieval
    - Profit/loss calculations
    - Purchase power queries
    """
    
    def _get_agent_type(self) -> str:
        """Return the agent type identifier."""
        return "account"
    
    def _initialize_tools(self) -> List[Tool]:
        """Initialize account-specific tools.
        
        Returns:
            List of account management tools
        """
        factory = KiwoomToolFactory(self.kiwoom_client)
        return factory.create_account_tools()
    
    def process_request(
        self,
        request: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Process account-related requests.
        
        Args:
            request: User's original request
            params: Extracted parameters from intent classification
            
        Returns:
            Account operation results
        """
        self._log(f"Processing account request: {request}")
        
        # Extract account number from parameters or use default
        account_number = self._extract_account_number(params)
        
        # Determine the type of account operation needed
        request_lower = request.lower()
        
        if any(keyword in request_lower for keyword in ["잔고", "예수금", "총자산", "평가금액"]):
            return self._handle_balance_request(account_number)
        
        elif any(keyword in request_lower for keyword in ["보유", "종목", "포트폴리오"]):
            return self._handle_holdings_request(account_number)
        
        elif any(keyword in request_lower for keyword in ["손익", "수익률", "평가손익", "실현손익"]):
            return self._handle_profit_loss_request(account_number)
        
        elif any(keyword in request_lower for keyword in ["매수가능", "주문가능", "가용자금"]):
            return self._handle_purchasable_amount_request(account_number)
        
        else:
            # Default to balance inquiry
            return self._handle_balance_request(account_number)
    
    def _handle_balance_request(self, account_number: Optional[str]) -> Dict[str, Any]:
        """Handle account balance requests.
        
        Args:
            account_number: Account number to query
            
        Returns:
            Account balance information
        """
        self._log("Handling balance request")
        
        # Use the get_account_balance tool
        balance_tool = next(
            (tool for tool in self.tools if tool.name == "get_account_balance"),
            None
        )
        
        if balance_tool:
            try:
                result = balance_tool.func(account_number)
                return result
            except Exception as e:
                return {"error": f"Failed to get account balance: {str(e)}"}
        else:
            return {"error": "Account balance tool not available"}
    
    def _handle_holdings_request(self, account_number: Optional[str]) -> List[Dict[str, Any]]:
        """Handle holdings requests.
        
        Args:
            account_number: Account number to query
            
        Returns:
            List of holdings information
        """
        self._log("Handling holdings request")
        
        # Use the get_account_holdings tool
        holdings_tool = next(
            (tool for tool in self.tools if tool.name == "get_account_holdings"),
            None
        )
        
        if holdings_tool:
            try:
                result = holdings_tool.func(account_number)
                return result if isinstance(result, list) else [result]
            except Exception as e:
                return [{"error": f"Failed to get holdings: {str(e)}"}]
        else:
            return [{"error": "Holdings tool not available"}]
    
    def _handle_profit_loss_request(self, account_number: Optional[str]) -> Dict[str, Any]:
        """Handle profit/loss requests.
        
        Args:
            account_number: Account number to query
            
        Returns:
            Profit/loss information
        """
        self._log("Handling profit/loss request")
        
        # Use the get_account_profit_loss tool
        pnl_tool = next(
            (tool for tool in self.tools if tool.name == "get_account_profit_loss"),
            None
        )
        
        if pnl_tool:
            try:
                result = pnl_tool.func(account_number)
                return result
            except Exception as e:
                return {"error": f"Failed to get profit/loss: {str(e)}"}
        else:
            return {"error": "Profit/loss tool not available"}
    
    def _handle_purchasable_amount_request(self, account_number: Optional[str]) -> Dict[str, Any]:
        """Handle purchasable amount requests.
        
        Args:
            account_number: Account number to query
            
        Returns:
            Purchasable amount information
        """
        self._log("Handling purchasable amount request")
        
        # Use the get_purchasable_amount tool
        purchasable_tool = next(
            (tool for tool in self.tools if tool.name == "get_purchasable_amount"),
            None
        )
        
        if purchasable_tool:
            try:
                result = purchasable_tool.func(account_number)
                return result
            except Exception as e:
                return {"error": f"Failed to get purchasable amount: {str(e)}"}
        else:
            return {"error": "Purchasable amount tool not available"}