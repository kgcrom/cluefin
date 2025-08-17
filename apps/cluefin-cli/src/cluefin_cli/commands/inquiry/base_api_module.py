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

        # Display breadcrumb navigation and clear menu title
        self.console.print("\n[bold green]─" * 60 + "[/bold green]")
        self.console.print(f"[bold cyan]📊 메인 메뉴 > {category.korean_name} 📊[/bold cyan]")
        self.console.print("[bold green]─" * 60 + "[/bold green]")
        self.console.print(f"[dim]총 {len(category.apis)}개의 {category.korean_name} API를 사용할 수 있습니다.[/dim]\n")

        # Create choices from API configurations with consistent formatting
        choices = []
        for i, api in enumerate(category.apis, 1):
            choice_text = f"{i:2d}. {api.korean_name}"
            choices.append((choice_text, api.name))

        choices.append(("⬅️  메인메뉴로 돌아가기", "back"))

        import inquirer

        question = inquirer.List(
            "api_choice", message=f"조회할 {category.korean_name} API를 선택하세요", choices=choices
        )

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
            # Display API information with breadcrumb navigation
            category = self.get_api_category()
            self.console.print("\n[bold green]─" * 60 + "[/bold green]")
            self.console.print(
                f"[bold cyan]📊 메인 메뉴 > {category.korean_name} > {api_config.korean_name} 📊[/bold cyan]"
            )
            self.console.print("[bold green]─" * 60 + "[/bold green]")

            if api_config.description:
                self.console.print(f"[dim]{api_config.description}[/dim]\n")
            else:
                self.console.print(f"[dim]{api_config.korean_name} API 파라미터를 입력하세요.[/dim]\n")

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

            # Check for partial data and handle gracefully
            processed_result = self._handle_partial_data(result, api_config)
            if processed_result is None:
                self.formatter.display_error("데이터 처리 중 오류가 발생했습니다.", "데이터 오류")
                return False

            # Format and display results
            self._format_and_display_result(processed_result, api_config)
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

        # All retries failed - provide detailed error information
        if isinstance(last_exception, KiwoomAPIError):
            error_title = self._get_user_friendly_error_title(last_exception)
            error_message = self._get_user_friendly_error_message(last_exception)
            self.formatter.display_error(error_message, error_title)

            # Show retry suggestion for certain errors
            if self._is_retryable_error(last_exception):
                self.console.print("[yellow]💡 잠시 후 다시 시도해 보세요.[/yellow]")
        else:
            self.formatter.display_error(f"예상치 못한 오류가 발생했습니다: {str(last_exception)}", "시스템 오류")
            self.console.print("[yellow]💡 네트워크 연결을 확인하고 다시 시도해 보세요.[/yellow]")

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

        # Specific error message patterns that are retryable
        retryable_message_patterns = [
            "일시적",  # Temporary issues
            "서버 점검",  # Server maintenance
            "과도한 요청",  # Too many requests
            "연결 시간 초과",  # Connection timeout
            "네트워크",  # Network issues
        ]

        # Check by status code
        if error.status_code and error.status_code in retryable_status_codes:
            return True

        # Check by error type
        error_type = type(error).__name__
        if error_type in retryable_error_types:
            return True

        # Check by error message patterns
        error_message = str(error.message) if hasattr(error, "message") else str(error)
        for pattern in retryable_message_patterns:
            if pattern in error_message:
                return True

        return False

    def _get_user_friendly_error_title(self, error: KiwoomAPIError) -> str:
        """
        Get a user-friendly error title based on the error type and status code.

        Args:
            error: The Kiwoom API error

        Returns:
            User-friendly error title in Korean
        """
        status_code = getattr(error, "status_code", None)
        error_type = type(error).__name__

        # Map common status codes to Korean titles
        status_code_titles = {
            400: "잘못된 요청",
            401: "인증 실패",
            403: "접근 배인",
            404: "API 링크 찾을 수 없음",
            429: "요청 한도 초과",
            500: "서버 내부 오류",
            502: "서버 연결 오류",
            503: "서비스 일시 중단",
            504: "서버 응답 시간 초과",
        }

        # Map error types to Korean titles
        error_type_titles = {
            "KiwoomRateLimitError": "요청 한도 초과",
            "KiwoomServerError": "서버 오류",
            "KiwoomNetworkError": "네트워크 오류",
            "KiwoomTimeoutError": "시간 초과",
            "KiwoomAuthError": "인증 실패",
        }

        if status_code and status_code in status_code_titles:
            return f"{status_code_titles[status_code]} ({status_code})"
        elif error_type in error_type_titles:
            return error_type_titles[error_type]
        elif status_code:
            return f"API 오류 ({status_code})"
        else:
            return "API 오류"

    def _get_user_friendly_error_message(self, error: KiwoomAPIError) -> str:
        """
        Get a user-friendly error message based on the error type and message.

        Args:
            error: The Kiwoom API error

        Returns:
            User-friendly error message in Korean
        """
        original_message = getattr(error, "message", str(error))
        status_code = getattr(error, "status_code", None)

        # Common error patterns and their user-friendly messages
        error_patterns = {
            "unauthorized": "인증 정보가 올바르지 않습니다. API 키를 확인해 보세요.",
            "forbidden": "이 API에 대한 접근 권한이 없습니다.",
            "not found": "요청한 데이터를 찾을 수 없습니다.",
            "too many requests": "요청이 너무 많습니다. 잠시 후 다시 시도해 보세요.",
            "rate limit": "요청 한도를 초과했습니다. 잠시 후 다시 시도해 보세요.",
            "server error": "서버에 일시적인 문제가 발생했습니다.",
            "timeout": "서버 응답 시간이 초과되었습니다.",
            "network": "네트워크 연결에 문제가 있습니다.",
        }

        message_lower = original_message.lower()
        for pattern, friendly_message in error_patterns.items():
            if pattern in message_lower:
                return friendly_message

        # Status code specific messages
        if status_code == 429:
            return "요청 한도를 초과했습니다. 1분 후 다시 시도해 보세요."
        elif status_code == 401:
            return "API 인증에 실패했습니다. 환경변수를 확인해 보세요."
        elif status_code == 500:
            return "서버에 일시적인 문제가 발생했습니다. 잠시 후 다시 시도해 보세요."

        # If no pattern matches, return a generic message with the original error
        return f"API 호출 중 오류가 발생했습니다: {original_message}"

    def _handle_partial_data(self, result: Any, api_config: APIConfig) -> Optional[Any]:
        """
        Handle partial data and implement graceful degradation.

        Args:
            result: The raw API response
            api_config: The API configuration

        Returns:
            Processed result or None if data is unusable
        """
        try:
            # Handle different result types
            if result is None:
                return None

            # If result is a dictionary, check for error indicators
            if isinstance(result, dict):
                # Check for common error fields
                if "error" in result or "msg_cd" in result:
                    error_msg = result.get("error", result.get("msg_cd", "Unknown error"))
                    logger.warning(f"API returned error: {error_msg}")

                    # If it's a partial failure, try to extract useful data
                    if "data" in result or "output" in result:
                        partial_data = result.get("data", result.get("output"))
                        if partial_data:
                            self.console.print("[yellow]⚠️  부분적인 데이터만 가져왔습니다.[/yellow]")
                            return partial_data
                    return None

                # Check if data array is empty or malformed
                data_fields = ["data", "output", "result", "list"]
                for field in data_fields:
                    if field in result:
                        data = result[field]
                        if isinstance(data, list) and len(data) == 0:
                            self.console.print("[yellow]해당 조건에 맞는 데이터가 없습니다.[/yellow]")
                            return result  # Still return the structure for proper handling
                        elif isinstance(data, list) and len(data) > 0:
                            # Check for data quality issues
                            valid_items = [item for item in data if item and len(str(item).strip()) > 0]
                            if len(valid_items) < len(data):
                                self.console.print(
                                    f"[yellow]⚠️  전체 {len(data)}건 중 {len(valid_items)}건의 유효 데이터를 가져왔습니다.[/yellow]"
                                )
                                result[field] = valid_items
                            return result

            # If result is a list, check for emptiness or quality
            elif isinstance(result, list):
                if len(result) == 0:
                    self.console.print("[yellow]해당 조건에 맞는 데이터가 없습니다.[/yellow]")
                    return result

                # Filter out invalid items
                valid_items = [item for item in result if item and len(str(item).strip()) > 0]
                if len(valid_items) < len(result):
                    self.console.print(
                        f"[yellow]⚠️  전체 {len(result)}건 중 {len(valid_items)}건의 유효 데이터를 가져왔습니다.[/yellow]"
                    )
                    return valid_items

            return result

        except Exception as e:
            logger.error(f"Error handling partial data: {e}")
            # Return original result if processing fails
            return result

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
                    # Show options after successful execution
                    self.console.print("\n[bold green]조회가 완료되었습니다![/bold green]")
                    self.console.print("[dim]• 엔터: 메뉴로 돌아가기[/dim]")
                    self.console.print("[dim]• Ctrl+C: 프로그램 종료[/dim]")
                    input()
                else:
                    # Show retry option after failure
                    self.console.print("\n[yellow]조회에 실패했습니다.[/yellow]")
                    self.console.print("[dim]• 엔터: 메뉴로 돌아가기[/dim]")
                    self.console.print("[dim]• Ctrl+C: 프로그램 종료[/dim]")
                    input()

            except KeyboardInterrupt:
                self.console.print("\n[yellow]메뉴로 돌아갑니다.[/yellow]")
                break
            except Exception as e:
                logger.error(f"Menu loop error: {e}")
                self.formatter.display_error(f"메뉴 처리 중 오류가 발생했습니다: {str(e)}", "시스템 오류")

                # Pause before continuing with recovery options
                self.console.print("\n[yellow]오류가 발생했지만 계속 진행할 수 있습니다.[/yellow]")
                self.console.print("[dim]• 엔터: 메뉴로 돌아가기[/dim]")
                self.console.print("[dim]• Ctrl+C: 프로그램 종료[/dim]")
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
