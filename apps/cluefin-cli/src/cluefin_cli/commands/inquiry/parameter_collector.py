"""
Parameter collection system for interactive user input.

This module handles collecting and validating user input parameters for API calls.
"""

import re
from datetime import datetime
from typing import Any, Dict, List, Optional

import inquirer
from rich.console import Console

from .config_models import APIConfig, ParameterConfig

console = Console()


class BaseParameterCollector:
    """Base class for collecting user input parameters with validation."""

    def __init__(self):
        """Initialize the parameter collector."""
        self.console = Console()

    def collect_parameters(self, api_config: APIConfig) -> Optional[Dict[str, Any]]:
        """
        Collect all parameters for an API based on its configuration.

        Args:
            api_config: Configuration for the API including all parameters

        Returns:
            Dictionary of collected parameters or None if user cancelled
        """
        try:
            # Collect required parameters first
            params = {}

            for param_config in api_config.required_params:
                value = self._collect_single_parameter(param_config)
                if value is None:
                    self.console.print("[red]Required parameter collection cancelled[/red]")
                    return None
                params[param_config.name] = value

            # Collect optional parameters
            for param_config in api_config.optional_params:
                value = self._collect_single_parameter(param_config, required=False)
                if value is not None:
                    params[param_config.name] = value

            return params

        except KeyboardInterrupt:
            self.console.print("\n[yellow]Parameter collection cancelled by user[/yellow]")
            return None
        except Exception as e:
            self.console.print(f"[red]Error collecting parameters: {e}[/red]")
            return None

    def _collect_single_parameter(self, param_config: ParameterConfig, required: bool = True) -> Optional[Any]:
        """
        Collect a single parameter based on its configuration.

        Args:
            param_config: Configuration for the parameter
            required: Whether this parameter is required

        Returns:
            The collected parameter value or None
        """
        if param_config.param_type == "select":
            return self._collect_select_parameter(param_config, required)
        elif param_config.param_type == "text":
            return self._collect_text_parameter(param_config, required)
        elif param_config.param_type == "date":
            return self._collect_date_parameter(param_config, required)
        else:
            raise ValueError(f"Unknown parameter type: {param_config.param_type}")

    def _collect_select_parameter(self, param_config: ParameterConfig, required: bool = True) -> Optional[str]:
        """
        Collect a select parameter using inquirer.List.

        Args:
            param_config: Configuration for the select parameter
            required: Whether this parameter is required

        Returns:
            Selected value or None
        """
        if not param_config.choices:
            raise ValueError(f"No choices defined for select parameter: {param_config.name}")

        # Create choices list with proper type handling
        choices: List[tuple[str, Optional[str]]] = [(label, value) for value, label in param_config.choices]
        if not required:
            choices.insert(0, ("건너뛰기", None))

        question = inquirer.List(param_config.name, message=param_config.korean_name, choices=choices)

        answer = inquirer.prompt([question])
        if not answer:
            return None

        return answer[param_config.name]

    def _collect_text_parameter(self, param_config: ParameterConfig, required: bool = True) -> Optional[str]:
        """
        Collect a text parameter using inquirer.Text with validation.

        Args:
            param_config: Configuration for the text parameter
            required: Whether this parameter is required

        Returns:
            Text value or None
        """
        message = param_config.korean_name
        if not required:
            message += " (선택사항, Enter로 건너뛰기)"

        while True:
            question = inquirer.Text(param_config.name, message=message)
            answer = inquirer.prompt([question])

            if not answer:
                return None

            value = answer[param_config.name].strip()

            # If not required and empty, return None
            if not required and not value:
                return None

            # If required but empty, ask again
            if required and not value:
                self.console.print("[red]이 값은 필수입니다. 다시 입력해주세요.[/red]")
                continue

            # Validate if validation pattern is provided
            if param_config.validation and not self._validate_text(value, param_config.validation):
                self.console.print(f"[red]올바르지 않은 형식입니다. {param_config.validation}[/red]")
                continue

            return value

    def _collect_date_parameter(self, param_config: ParameterConfig, required: bool = True) -> Optional[str]:
        """
        Collect a date parameter with YYYYMMDD format validation.

        Args:
            param_config: Configuration for the date parameter
            required: Whether this parameter is required

        Returns:
            Date string in YYYYMMDD format or None
        """
        message = f"{param_config.korean_name} (YYYYMMDD 형식)"
        if not required:
            message += " (선택사항, Enter로 건너뛰기)"

        while True:
            question = inquirer.Text(param_config.name, message=message)
            answer = inquirer.prompt([question])

            if not answer:
                return None

            value = answer[param_config.name].strip()

            # If not required and empty, return None
            if not required and not value:
                return None

            # If required but empty, ask again
            if required and not value:
                self.console.print("[red]이 값은 필수입니다. 다시 입력해주세요.[/red]")
                continue

            # Validate date format
            if not self._validate_date(value):
                self.console.print("[red]올바르지 않은 날짜 형식입니다. YYYYMMDD 형식으로 입력해주세요.[/red]")
                continue

            return value

    def _validate_text(self, value: str, validation_pattern: str) -> bool:
        """
        Validate text input against a pattern.

        Args:
            value: The text value to validate
            validation_pattern: The validation pattern or rule

        Returns:
            True if valid, False otherwise
        """
        try:
            # Try to match as regex pattern
            return bool(re.match(validation_pattern, value))
        except re.error:
            # If not a valid regex, assume it's a custom validation rule
            # For now, just return True for custom rules
            return True

    def _validate_date(self, date_str: str) -> bool:
        """
        Validate date string in YYYYMMDD format.

        Args:
            date_str: Date string to validate

        Returns:
            True if valid date, False otherwise
        """
        if len(date_str) != 8 or not date_str.isdigit():
            return False

        try:
            datetime.strptime(date_str, "%Y%m%d")
            return True
        except ValueError:
            return False


class ParameterCollector(BaseParameterCollector):
    """Legacy parameter collector with specific methods for existing APIs."""

    def collect_market_type(self, include_all: bool = True) -> Optional[str]:
        """
        Collect market type selection (KOSPI/KOSDAQ/전체).

        Args:
            include_all: Whether to include "전체" option

        Returns:
            Market type code or None if cancelled
        """
        choices = []
        if include_all:
            choices.append(("전체", "000"))
        choices.extend([("코스피", "001"), ("코스닥", "101")])

        question = inquirer.List("market_type", message="시장구분을 선택하세요", choices=choices)

        answer = inquirer.prompt([question])
        if not answer:
            return None

        return answer["market_type"]

    def collect_date_input(self, prompt: str, required: bool = True) -> Optional[str]:
        """
        Collect date input with YYYYMMDD format validation.

        Args:
            prompt: Korean prompt message for the date input
            required: Whether the date input is required

        Returns:
            Date string in YYYYMMDD format or None
        """
        message = f"{prompt} (YYYYMMDD 형식)"
        if not required:
            message += " (선택사항, Enter로 건너뛰기)"

        while True:
            question = inquirer.Text("date_input", message=message)
            answer = inquirer.prompt([question])

            if not answer:
                return None

            value = answer["date_input"].strip()

            # If not required and empty, return None
            if not required and not value:
                return None

            # If required but empty, ask again
            if required and not value:
                self.console.print("[red]날짜는 필수입니다. 다시 입력해주세요.[/red]")
                continue

            # Validate date format
            if not self._validate_date(value):
                self.console.print("[red]올바르지 않은 날짜 형식입니다. YYYYMMDD 형식으로 입력해주세요.[/red]")
                continue

            return value

    def collect_numeric_choice(
        self, prompt: str, choices: List[tuple[str, str]], required: bool = True
    ) -> Optional[str]:
        """
        Collect numeric choice selection with Korean labels.

        Args:
            prompt: Korean prompt message for the selection
            choices: List of (korean_label, value) tuples
            required: Whether the selection is required

        Returns:
            Selected value or None
        """
        choice_list = [(label, value) for label, value in choices]
        if not required:
            choice_list.insert(0, ("건너뛰기", None))

        question = inquirer.List("numeric_choice", message=prompt, choices=choice_list)

        answer = inquirer.prompt([question])
        if not answer:
            return None

        return answer["numeric_choice"]

    def collect_stock_code(self, prompt: str = "종목코드를 입력하세요", required: bool = True) -> Optional[str]:
        """
        Collect stock code input with validation.

        Args:
            prompt: Korean prompt message for stock code input
            required: Whether the stock code is required

        Returns:
            Stock code or None
        """
        message = prompt
        if not required:
            message += " (선택사항, Enter로 건너뛰기)"

        while True:
            question = inquirer.Text("stock_code", message=message)
            answer = inquirer.prompt([question])

            if not answer:
                return None

            value = answer["stock_code"].strip()

            # If not required and empty, return None
            if not required and not value:
                return None

            # If required but empty, ask again
            if required and not value:
                self.console.print("[red]종목코드는 필수입니다. 다시 입력해주세요.[/red]")
                continue

            # Validate stock code format (6 digits)
            if not self._validate_stock_code(value):
                self.console.print("[red]올바르지 않은 종목코드 형식입니다. 6자리 숫자로 입력해주세요.[/red]")
                continue

            return value

    def _validate_stock_code(self, stock_code: str) -> bool:
        """
        Validate Korean stock code format (6 digits).

        Args:
            stock_code: Stock code to validate

        Returns:
            True if valid stock code format, False otherwise
        """
        # Korean stock codes are typically 6 digits
        return len(stock_code) == 6 and stock_code.isdigit()

    def collect_volume_surge_params(self) -> Optional[Dict[str, Any]]:
        """거래량급증요청 파라미터를 수집합니다."""
        questions = [
            inquirer.List(
                "mrkt_tp",
                message="시장구분을 선택하세요",
                choices=[("전체", "000"), ("코스피", "001"), ("코스닥", "101")],
            ),
            inquirer.List(
                "sort_tp",
                message="정렬구분을 선택하세요",
                choices=[("급증량", "1"), ("급증률", "2"), ("급감량", "3"), ("급감률", "4")],
            ),
            inquirer.List(
                "tm_tp",
                message="시간구분을 선택하세요",
                choices=[("분 입력", "1"), ("전일 입력", "2")],
            ),
            inquirer.List(
                "trde_qty_tp",
                message="거래량구분을 선택하세요",
                choices=[
                    ("5천주이상", "5"),
                    ("1만주이상", "10"),
                    ("5만주이상", "50"),
                    ("10만주이상", "100"),
                    ("20만주이상", "200"),
                    ("30만주이상", "300"),
                    ("50만주이상", "500"),
                    ("백만주이상", "1000"),
                ],
            ),
            inquirer.List(
                "stk_cnd",
                message="종목조건을 선택하세요",
                choices=[
                    ("전체조회", "0"),
                    ("관리종목제외", "1"),
                    ("우선주제외", "3"),
                    ("관리종목+우선주제외", "4"),
                    ("증100제외", "5"),
                    ("증100만보기", "6"),
                    ("증40만보기", "7"),
                    ("증30만보기", "8"),
                    ("증20만보기", "9"),
                ],
            ),
            inquirer.List(
                "pric_tp",
                message="가격구분을 선택하세요",
                choices=[
                    ("전체조회", "0"),
                    ("1천원~2천원", "2"),
                    ("1만원이상", "5"),
                    ("1천원이상", "6"),
                    ("1천원이상", "8"),
                    ("1만원미만", "9"),
                ],
            ),
            inquirer.List(
                "stex_tp",
                message="거래소구분을 선택하세요",
                choices=[("KRX", "1"), ("NXT", "2")],
            ),
        ]

        answers = inquirer.prompt(questions)
        if not answers:
            return None

        # tm_tp가 "1"일 때 시간 입력 받기
        if answers["tm_tp"] == "1":
            time_question = [inquirer.Text("tm", message="시간을 입력하세요 (분 단위)")]
            time_answer = inquirer.prompt(time_question)
            if time_answer:
                answers["tm"] = time_answer["tm"]
        else:
            answers["tm"] = ""

        return answers

    def collect_current_day_volume_params(self) -> Optional[Dict[str, Any]]:
        """당일거래량상위요청 파라미터를 수집합니다."""
        questions = [
            inquirer.List(
                "mrkt_tp",
                message="시장구분을 선택하세요",
                choices=[("전체", "000"), ("코스피", "001"), ("코스닥", "101")],
            ),
            inquirer.List(
                "sort_tp",
                message="정렬구분을 선택하세요",
                choices=[("거래량", "1"), ("거래회전율", "2"), ("거래대금", "3")],
            ),
            inquirer.List(
                "mang_stk_incls",
                message="관리종목포함을 선택하세요",
                choices=[
                    ("관리종목 포함", "0"),
                    ("관리종목 미포함", "1"),
                    ("우선주제외", "3"),
                    ("관리종목+우선주제외", "4"),
                    ("증100제외", "5"),
                    ("증100만보기", "6"),
                    ("증40만보기", "7"),
                    ("증30만보기", "8"),
                    ("증20만보기", "9"),
                ],
            ),
            inquirer.List(
                "crd_tp",
                message="신용구분을 선택하세요",
                choices=[
                    ("전체조회", "0"),
                    ("신용융자A군", "1"),
                    ("신용융자B군", "2"),
                    ("신용융자C군", "3"),
                    ("신용융자D군", "4"),
                    ("신용대주", "8"),
                ],
            ),
            inquirer.List(
                "trde_qty_tp",
                message="거래량구분을 선택하세요",
                choices=[
                    ("전체조회", "0"),
                    ("5천주이상", "5"),
                    ("1만주이상", "10"),
                    ("5만주이상", "50"),
                    ("10만주이상", "100"),
                    ("20만주이상", "200"),
                    ("30만주이상", "300"),
                    ("50만주이상", "500"),
                    ("백만주이상", "1000"),
                ],
            ),
            inquirer.List(
                "pric_tp",
                message="가격구분을 선택하세요",
                choices=[
                    ("전체조회", "0"),
                    ("1천원미만", "1"),
                    ("1천원이상", "2"),
                    ("1천원~2천원", "3"),
                    ("2천원~5천원", "4"),
                    ("5천원이상", "5"),
                    ("5천원~1만원", "6"),
                    ("1만원미만", "7"),
                    ("1만원이상", "8"),
                    ("5만원이상", "9"),
                ],
            ),
            inquirer.List(
                "trde_prica_tp",
                message="거래대금구분을 선택하세요",
                choices=[
                    ("전체조회", "0"),
                    ("1천만원이상", "1"),
                    ("3천만원이상", "3"),
                    ("5천만원이상", "4"),
                    ("1억원이상", "10"),
                    ("3억원이상", "30"),
                    ("5억원이상", "50"),
                    ("10억원이상", "100"),
                    ("30억원이상", "300"),
                    ("50억원이상", "500"),
                    ("100억원이상", "1000"),
                    ("300억원이상", "3000"),
                    ("500억원이상", "5000"),
                ],
            ),
            inquirer.List(
                "mrkt_open_tp",
                message="장운영구분을 선택하세요",
                choices=[("전체조회", "0"), ("장중", "1"), ("장전시간외", "2"), ("장후시간외", "3")],
            ),
        ]

        answers = inquirer.prompt(questions)
        if not answers:
            return None

        # 기본값 설정
        answers["stex_tp"] = "1"  # KRX
        return answers

    def collect_previous_day_volume_params(self) -> Optional[Dict[str, Any]]:
        """전일거래량상위요청 파라미터를 수집합니다."""
        questions = [
            inquirer.List(
                "mrkt_tp",
                message="시장구분을 선택하세요",
                choices=[("전체", "000"), ("코스피", "001"), ("코스닥", "101")],
            ),
            inquirer.List(
                "qry_tp",
                message="조회구분을 선택하세요",
                choices=[("전일거래량 상위100종목", "1"), ("전일거래대금 상위100종목", "2")],
            ),
            inquirer.Text("rank_strt", message="순위시작 (0~100)", default="1"),
            inquirer.Text("rank_end", message="순위끝 (0~100)", default="20"),
            inquirer.List(
                "stex_tp",
                message="거래소구분을 선택하세요",
                choices=[("KRX", "1"), ("NXT", "2")],
            ),
        ]

        answers = inquirer.prompt(questions)
        return answers

    def collect_transaction_value_params(self) -> Optional[Dict[str, Any]]:
        """거래대금상위요청 파라미터를 수집합니다."""
        questions = [
            inquirer.List(
                "mrkt_tp",
                message="시장구분을 선택하세요",
                choices=[("전체", "000"), ("코스피", "001"), ("코스닥", "101")],
            ),
            inquirer.List(
                "mang_stk_incls",
                message="관리종목포함 여부를 선택하세요",
                choices=[("미포함", "0"), ("포함", "1")],
            ),
            inquirer.List(
                "stex_tp",
                message="거래소구분을 선택하세요",
                choices=[("KRX", "1"), ("NXT", "2")],
            ),
        ]

        answers = inquirer.prompt(questions)
        return answers

    def collect_foreign_period_trading_params(self) -> Optional[Dict[str, Any]]:
        """외인기간별매매상위요청 파라미터를 수집합니다."""
        questions = [
            inquirer.List(
                "mrkt_tp",
                message="시장구분을 선택하세요",
                choices=[("전체", "000"), ("코스피", "001"), ("코스닥", "101")],
            ),
            inquirer.List(
                "trde_tp",
                message="매매구분을 선택하세요",
                choices=[("순매도", "1"), ("순매수", "2"), ("순매매", "3")],
            ),
            inquirer.List(
                "dt",
                message="기간을 선택하세요",
                choices=[("당일", "0"), ("전일", "1"), ("5일", "5"), ("10일", "10"), ("20일", "20"), ("60일", "60")],
            ),
            inquirer.List(
                "stex_tp",
                message="거래소구분을 선택하세요",
                choices=[("KRX", "1"), ("NXT", "2"), ("통합", "3")],
            ),
        ]

        answers = inquirer.prompt(questions)
        return answers

    def collect_foreign_consecutive_trading_params(self) -> Optional[Dict[str, Any]]:
        """외인연속순매매상위요청 파라미터를 수집합니다."""
        questions = [
            inquirer.List(
                "mrkt_tp",
                message="시장구분을 선택하세요",
                choices=[("전체", "000"), ("코스피", "001"), ("코스닥", "101")],
            ),
            inquirer.List(
                "trde_tp",
                message="매매구분을 선택하세요",
                choices=[("연속순매도", "1"), ("연속순매수", "2")],
            ),
            inquirer.List(
                "base_dt_tp",
                message="기준일구분을 선택하세요",
                choices=[("당일기준", "0"), ("전일기준", "1")],
            ),
            inquirer.List(
                "stex_tp",
                message="거래소구분을 선택하세요",
                choices=[("KRX", "1"), ("NXT", "2"), ("통합", "3")],
            ),
        ]

        answers = inquirer.prompt(questions)
        return answers

    def collect_foreign_institutional_trading_params(self) -> Optional[Dict[str, Any]]:
        """외국인기관매매상위요청 파라미터를 수집합니다."""
        questions = [
            inquirer.List(
                "mrkt_tp",
                message="시장구분을 선택하세요",
                choices=[("전체", "000"), ("코스피", "001"), ("코스닥", "101")],
            ),
            inquirer.List(
                "dt",
                message="기간을 선택하세요",
                choices=[("당일", "0"), ("전일", "1"), ("5일", "5"), ("10일", "10"), ("20일", "20"), ("60일", "60")],
            ),
            inquirer.List(
                "trde_tp",
                message="매매구분을 선택하세요",
                choices=[("순매수", "1"), ("순매도", "2"), ("매수", "3"), ("매도", "4")],
            ),
            inquirer.List(
                "sort_tp",
                message="정렬구분을 선택하세요",
                choices=[("금액", "1"), ("수량", "2")],
            ),
            inquirer.List(
                "stex_tp",
                message="거래소구분을 선택하세요",
                choices=[("KRX", "1"), ("NXT", "2"), ("통합", "3")],
            ),
        ]

        answers = inquirer.prompt(questions)
        return answers
