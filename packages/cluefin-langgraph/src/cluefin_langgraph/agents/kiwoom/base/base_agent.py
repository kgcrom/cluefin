"""Base agent class for Kiwoom specialized agents."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from cluefin_openapi.kiwoom import Client as KiwoomClient
from langchain.tools import Tool
from langchain_core.language_models.base import BaseLanguageModel
from loguru import logger


class BaseKiwoomAgent(ABC):
    """Abstract base class for all Kiwoom specialized agents.

    This class provides common functionality and interface that all specialized
    agents must implement. Each agent handles specific domain tasks using
    Kiwoom API tools.
    """

    def __init__(
        self,
        kiwoom_client: KiwoomClient,
        llm: BaseLanguageModel,
        verbose: bool = False,
    ):
        """Initialize the base agent.

        Args:
            kiwoom_client: Kiwoom API client instance
            llm: Language model for agent reasoning
            verbose: Enable verbose logging
        """
        self.kiwoom_client = kiwoom_client
        self.llm = llm
        self.verbose = verbose
        self.tools = self._initialize_tools()
        self.agent_type = self._get_agent_type()

    @abstractmethod
    def _get_agent_type(self) -> str:
        """Return the agent type identifier.

        This should match one of the AgentType enum values.
        """
        pass

    @abstractmethod
    def _initialize_tools(self) -> List[Tool]:
        """Initialize agent-specific tools.

        Each specialized agent must implement this to provide
        its own set of tools based on the Kiwoom API capabilities.

        Returns:
            List of LangChain Tool instances
        """
        pass

    @abstractmethod
    def process_request(
        self,
        request: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Process a user request with extracted parameters.

        This is the main entry point for handling requests routed
        to this agent.

        Args:
            request: The user's original request
            params: Extracted parameters from intent classification

        Returns:
            The result of processing the request
        """
        pass

    def _format_response(self, data: Any) -> str:
        """Format raw API response data for user presentation.

        Args:
            data: Raw response data from API calls

        Returns:
            Formatted string suitable for user display
        """
        # Default implementation - can be overridden by subclasses
        if isinstance(data, dict):
            return self._format_dict_response(data)
        elif isinstance(data, list):
            return self._format_list_response(data)
        else:
            return str(data)

    def _format_dict_response(self, data: Dict[str, Any]) -> str:
        """Format dictionary response data."""
        lines = []
        for key, value in data.items():
            # Convert key from snake_case to human readable
            display_key = key.replace("_", " ").title()
            lines.append(f"{display_key}: {value}")
        return "\n".join(lines)

    def _format_list_response(self, data: List[Any]) -> str:
        """Format list response data."""
        if not data:
            return "조회된 데이터가 없습니다."

        # If list of dicts, format as table-like structure
        if all(isinstance(item, dict) for item in data):
            return self._format_table_response(data)

        # Simple list formatting
        return "\n".join(f"- {item}" for item in data)

    def _format_table_response(self, data: List[Dict[str, Any]]) -> str:
        """Format list of dictionaries as a table-like structure."""
        if not data:
            return ""

        # Get all unique keys
        all_keys = set()
        for item in data:
            all_keys.update(item.keys())

        # Create header
        headers = sorted(all_keys)
        lines = [" | ".join(headers)]
        lines.append("-" * len(lines[0]))

        # Add data rows
        for item in data:
            row = []
            for header in headers:
                value = item.get(header, "")
                row.append(str(value))
            lines.append(" | ".join(row))

        return "\n".join(lines)

    def _extract_account_number(
        self,
        params: Optional[Dict[str, Any]] = None,
    ) -> Optional[str]:
        """Extract account number from parameters or use default.

        Args:
            params: Parameters that may contain account number

        Returns:
            Account number or None if not available
        """
        if params and "account_number" in params:
            return params["account_number"]

        # Try to get default account from client
        # This would need to be implemented in the Kiwoom client
        return None

    def _extract_stock_code(
        self,
        params: Optional[Dict[str, Any]] = None,
    ) -> Optional[str]:
        """Extract stock code from parameters.

        Args:
            params: Parameters that may contain stock code

        Returns:
            Stock code or None if not available
        """
        if not params:
            return None

        # Try different possible parameter names
        for key in ["stock_code", "symbol", "종목코드", "종목"]:
            if key in params:
                return params[key]

        return None

    def _log(self, message: str) -> None:
        """Log a message if verbose mode is enabled.

        Args:
            message: Message to log
        """
        if self.verbose:
            logger.info(f"[{self.agent_type}] {message}")
