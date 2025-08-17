"""
Base API module for stock inquiry system.

This module provides the common functionality for all API modules including
error handling, retry logic, logging, and client management.
"""

import time
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

from cluefin_openapi.kiwoom import Client as KiwoomClient
from cluefin_openapi.kiwoom._exceptions import KiwoomAPIError
from loguru import logger
from rich.console import Console

from .config_models import APICategory, APIConfig
from .display_formatter import DisplayFormatter
from .parameter_collector import BaseParameterCollector


class BaseAPIModule(ABC):
    """
    Base class for all API modules with common functionality.

    Provides error handling, retry logic, logging, and standardized
    API execution patterns for all inquiry modules.
    """

    def __init__(self, client: Optional[KiwoomClient] = None):
        """
        Initialize the base API module.

        Args:
            client: Optional Kiwoom API client instance
        """
        self.client = client
        self.parameter_collector = BaseParameterCollector()
        self.formatter = DisplayFormatter()
        self.console = Console()

        # Configuration for retry logic
        self.max_retries = 3
        self.retry_delay = 1.0  # seconds
        self.backoff_multiplier = 2.0

        # Rate limiting
        self.last_api_call = 0
        self.min_call_interval = 0.1  # 100ms between calls

    @abstractmethod
    def get_api_category(self) -> APICategory:
        """
        Get the API category configuration for this module.

        Returns:
            APICategory configuration with all APIs for this module
        """
        pass

    def show_api_menu(self) -> Optional[str]:
        """
        Display available APIs for this category and get user selection.

        Returns:
            Selected API name or None if cancelled
        """
        category = self.get_api_category()

        self.console.print(f"\n[bold blue]{category.korean_name} 메뉴[/bold blue]")

        # Create choices from API configurations
        choices = [(api.korean_name, api.name) for api in category.apis]
        choices.append(("⬅️ 메인메뉴로 돌아가기", "back"))

        import inquirer

        question = inquirer.List("api_choice", message=f"조회할 {category.korean_name}를 선택하세요", choices=choices)

        answer = inquirer.prompt([question])
        if not answer or answer["api_choice"] == "back":
            return None

        return answer["api_choice"]

    def execute_api(self, api_name: str) -> bool:
        """
        Execute the selected API with parameter collection and error handling.

        Args:
            api_name: Name of the API to execute

        Returns:
            True if successful, False if failed or cancelled
        """
        category = self.get_api_category()
        api_config = category.get_api_by_name(api_name)

        if not api_config:
            self.formatter.display_error(f"API '{api_name}'을 찾을 수 없습니다.", "설정 오류")
            return False

        try:
            # Display API information
            self.console.print(f"[cyan]{api_config.korean_name} - 파라미터 입력[/cyan]")

            # Collect parameters
            params = self.get_api_parameters(api_config)
            if params is None:
                self.console.print("[yellow]파라미터 입력이 취소되었습니다.[/yellow]")
                return False

            # Execute API call with retry logic
            self.formatter.display_loading(f"{api_config.korean_name} 데이터를 가져오는 중...")

            result = self._execute_api_with_retry(api_config, params)
            if result is None:
                return False

            # Format and display results
            self._format_and_display_result(result, api_config)
            return True

        except KeyboardInterrupt:
            self.console.print("\n[yellow]사용자에 의해 취소되었습니다.[/yellow]")
            return False
        except Exception as e:
            logger.error(f"API execution failed for {api_name}: {e}")
            self.formatter.display_error(f"API 실행 중 오류가 발생했습니다: {str(e)}", "실행 오류")
            return False

    def get_api_parameters(self, api_config: APIConfig) -> Optional[Dict[str, Any]]:
        """
        Collect required parameters for an API based on its configuration.

        Args:
            api_config: Configuration for the API

        Returns:
            Dictionary of collected parameters or None if cancelled
        """
        return self.parameter_collector.collect_parameters(api_config)

    def _execute_api_with_retry(self, api_config: APIConfig, params: Dict[str, Any]) -> Optional[Any]:
        """
        Execute API call with retry logic and rate limiting.

        Args:
            api_config: API configuration
            params: Parameters for the API call

        Returns:
            API response or None if failed
        """
        if not self.client:
            self.formatter.display_error("API 클라이언트가 초기화되지 않았습니다.", "클라이언트 오류")
            return None

        # Rate limiting
        self._enforce_rate_limit()

        last_exception = None

        for attempt in range(self.max_retries):
            try:
                logger.info(f"Executing API {api_config.api_method} (attempt {attempt + 1})")

                # Get the API method from client
                api_method = getattr(self.client, api_config.api_method, None)
                if not api_method:
                    raise AttributeError(f"API method '{api_config.api_method}' not found on client")

                # Execute the API call
                result = api_method(**params)

                logger.info(f"API {api_config.api_method} executed successfully")
                return result

            except KiwoomAPIError as e:
                last_exception = e
                logger.warning(f"Kiwoom API error on attempt {attempt + 1}: {e}")

                # Check if this is a retryable error
                if not self._is_retryable_error(e):
                    break

                if attempt < self.max_retries - 1:
                    delay = self.retry_delay * (self.backoff_multiplier**attempt)
                    logger.info(f"Retrying in {delay} seconds...")
                    time.sleep(delay)

            except Exception as e:
                last_exception = e
                logger.error(f"Unexpected error on attempt {attempt + 1}: {e}")
                break

        # All retries failed
        if isinstance(last_exception, KiwoomAPIError):
            error_title = f"오류 코드: {last_exception.status_code}" if last_exception.status_code else "API 오류"
            self.formatter.display_error(f"API 호출 실패: {last_exception.message}", error_title)
        else:
            self.formatter.display_error(f"API 호출 실패: {str(last_exception)}", "네트워크 오류")

        return None

    def _enforce_rate_limit(self) -> None:
        """Enforce minimum interval between API calls."""
        current_time = time.time()
        time_since_last_call = current_time - self.last_api_call

        if time_since_last_call < self.min_call_interval:
            sleep_time = self.min_call_interval - time_since_last_call
            time.sleep(sleep_time)

        self.last_api_call = time.time()

    def _is_retryable_error(self, error: KiwoomAPIError) -> bool:
        """
        Determine if an API error is retryable.

        Args:
            error: The Kiwoom API error

        Returns:
            True if the error should be retried
        """
        # Define retryable status codes and error types
        retryable_status_codes = [429, 500, 502, 503, 504]  # Rate limit and server errors
        retryable_error_types = [
            "KiwoomRateLimitError",
            "KiwoomServerError",
            "KiwoomNetworkError",
            "KiwoomTimeoutError",
        ]

        # Check by status code
        if error.status_code and error.status_code in retryable_status_codes:
            return True

        # Check by error type
        error_type = type(error).__name__
        return error_type in retryable_error_types

    @abstractmethod
    def _format_and_display_result(self, result: Any, api_config: APIConfig) -> None:
        """
        Format and display the API result.

        Args:
            result: The API response data
            api_config: Configuration for the API that was called
        """
        pass

    def handle_menu_loop(self) -> None:
        """
        Handle the main menu loop for this API category.

        Displays the menu, processes user selections, and executes APIs
        until the user chooses to go back.
        """
        while True:
            try:
                api_name = self.show_api_menu()
                if not api_name:
                    break

                success = self.execute_api(api_name)

                if success:
                    # Pause to let user review results
                    self.console.print("\n[dim]계속하려면 엔터를 누르세요...[/dim]")
                    input()

            except KeyboardInterrupt:
                self.console.print("\n[yellow]메뉴로 돌아갑니다.[/yellow]")
                break
            except Exception as e:
                logger.error(f"Menu loop error: {e}")
                self.formatter.display_error(f"메뉴 처리 중 오류가 발생했습니다: {str(e)}", "시스템 오류")

                # Pause before continuing
                self.console.print("\n[dim]계속하려면 엔터를 누르세요...[/dim]")
                input()

    def set_client(self, client: KiwoomClient) -> None:
        """
        Set the Kiwoom API client for this module.

        Args:
            client: The Kiwoom API client instance
        """
        self.client = client
        logger.info(f"Client set for {self.__class__.__name__}")

    def get_client_status(self) -> Dict[str, Any]:
        """
        Get the current status of the API client.

        Returns:
            Dictionary with client status information
        """
        return {
            "client_initialized": self.client is not None,
            "client_type": type(self.client).__name__ if self.client else None,
            "max_retries": self.max_retries,
            "retry_delay": self.retry_delay,
            "min_call_interval": self.min_call_interval,
        }
