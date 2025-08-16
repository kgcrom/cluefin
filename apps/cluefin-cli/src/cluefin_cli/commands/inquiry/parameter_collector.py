"""
Parameter collection system for interactive user input.

This module handles collecting and validating user input parameters for API calls.
"""

from typing import Any, Dict, Optional

import inquirer
from rich.console import Console

console = Console()


class ParameterCollector:
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
