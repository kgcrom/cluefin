"""
Ranking information module for stock inquiry.

This module handles all ranking-related APIs (순위정보) including volume rankings,
trading value rankings, and foreign investor activity rankings.
"""

from typing import Any, Optional

from cluefin_openapi.kiwoom import Client as KiwoomClient

from .base_api_module import BaseAPIModule
from .config_models import APICategory, APIConfig, ParameterConfig
from .display_formatter import RankingDataFormatter


class RankingInfoModule(BaseAPIModule):
    """
    Ranking information module extending BaseAPIModule.

    Handles all ranking-related APIs including volume rankings,
    trading value rankings, and foreign investor activity.
    """

    def __init__(self, client: Optional[KiwoomClient] = None):
        """
        Initialize the ranking information module.

        Args:
            client: Optional Kiwoom API client instance
        """
        super().__init__(client)
        # Use specialized formatter for ranking data
        self.formatter = RankingDataFormatter()

    def get_client_attribute_name(self) -> str:
        """Get the client attribute name for ranking info APIs."""
        return "rank_info"

    def get_api_category(self) -> APICategory:
        """
        Get the API category configuration for ranking information.

        Returns:
            APICategory with all ranking APIs configured
        """
        return APICategory(
            name="ranking_info",
            korean_name="📈 순위정보",
            description="거래량, 거래대금, 외국인 매매 등 다양한 순위 정보를 제공합니다.",
            apis=[
                APIConfig(
                    name="rapidly_increasing_trading_volume",
                    korean_name="🚀 거래량급증요청",
                    api_method="get_rapidly_increasing_trading_volume",
                    description="거래량이 급증한 종목들의 순위를 조회합니다.",
                    required_params=[
                        ParameterConfig(
                            name="mrkt_tp",
                            korean_name="시장구분",
                            param_type="select",
                            choices=[("전체", "000"), ("코스피", "001"), ("코스닥", "101")],
                            required=True,
                            validation=None,
                        ),
                        ParameterConfig(
                            name="sort_tp",
                            korean_name="정렬구분",
                            param_type="select",
                            choices=[("급증량", "1"), ("급증률", "2"), ("급감량", "3"), ("급감률", "4")],
                            required=True,
                            validation=None,
                        ),
                        ParameterConfig(
                            name="tm_tp",
                            korean_name="시간구분",
                            param_type="select",
                            choices=[("분 입력", "1"), ("전일 입력", "2")],
                            required=True,
                            validation=None,
                        ),
                        ParameterConfig(
                            name="trde_qty_tp",
                            korean_name="거래량구분",
                            param_type="select",
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
                            required=True,
                            validation=None,
                        ),
                        ParameterConfig(
                            name="stk_cnd",
                            korean_name="종목조건",
                            param_type="select",
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
                            required=True,
                            validation=None,
                        ),
                        ParameterConfig(
                            name="pric_tp",
                            korean_name="가격구분",
                            param_type="select",
                            choices=[
                                ("전체조회", "0"),
                                ("1천원~2천원", "2"),
                                ("1만원이상", "5"),
                                ("1천원이상", "6"),
                                ("1만원미만", "9"),
                            ],
                            required=True,
                            validation=None,
                        ),
                        ParameterConfig(
                            name="stex_tp",
                            korean_name="거래소구분",
                            param_type="select",
                            choices=[("KRX", "1"), ("NXT", "2")],
                            required=True,
                            validation=None,
                        ),
                    ],
                    optional_params=[
                        ParameterConfig(
                            name="tm",
                            korean_name="시간(분)",
                            param_type="text",
                            required=False,
                            validation=r"^\d{2}$",
                            choices=None,
                        )
                    ],
                ),
                APIConfig(
                    name="current_day_trading_volume_top",
                    korean_name="📊 당일거래량상위요청",
                    api_method="get_current_day_trading_volume_top",
                    description="당일 거래량 상위 종목들을 조회합니다.",
                    required_params=[
                        ParameterConfig(
                            name="mrkt_tp",
                            korean_name="시장구분",
                            param_type="select",
                            choices=[("전체", "000"), ("코스피", "001"), ("코스닥", "101")],
                            required=True,
                            validation=None,
                        ),
                        ParameterConfig(
                            name="sort_tp",
                            korean_name="정렬구분",
                            param_type="select",
                            choices=[("거래량", "1"), ("거래회전율", "2"), ("거래대금", "3")],
                            required=True,
                            validation=None,
                        ),
                        ParameterConfig(
                            name="mang_stk_incls",
                            korean_name="관리종목포함",
                            param_type="select",
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
                            required=True,
                            validation=None,
                        ),
                        ParameterConfig(
                            name="crd_tp",
                            korean_name="신용구분",
                            param_type="select",
                            choices=[
                                ("전체조회", "0"),
                                ("신용융자A군", "1"),
                                ("신용융자B군", "2"),
                                ("신용융자C군", "3"),
                                ("신용융자D군", "4"),
                                ("신용대주", "8"),
                            ],
                            required=True,
                            validation=None,
                        ),
                        ParameterConfig(
                            name="trde_qty_tp",
                            korean_name="거래량구분",
                            param_type="select",
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
                            required=True,
                            validation=None,
                        ),
                        ParameterConfig(
                            name="pric_tp",
                            korean_name="가격구분",
                            param_type="select",
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
                            required=True,
                            validation=None,
                        ),
                        ParameterConfig(
                            name="trde_prica_tp",
                            korean_name="거래대금구분",
                            param_type="select",
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
                            required=True,
                            validation=None,
                        ),
                        ParameterConfig(
                            name="mrkt_open_tp",
                            korean_name="장운영구분",
                            param_type="select",
                            choices=[("전체조회", "0"), ("장중", "1"), ("장전시간외", "2"), ("장후시간외", "3")],
                            required=True,
                            validation=None,
                        ),
                    ],
                ),
                APIConfig(
                    name="previous_day_trading_volume_top",
                    korean_name="📉 전일거래량상위요청",
                    api_method="get_previous_day_trading_volume_top",
                    description="전일 거래량 상위 종목들을 조회합니다.",
                    required_params=[
                        ParameterConfig(
                            name="mrkt_tp",
                            korean_name="시장구분",
                            param_type="select",
                            choices=[("전체", "000"), ("코스피", "001"), ("코스닥", "101")],
                            required=True,
                            validation=None,
                        ),
                        ParameterConfig(
                            name="qry_tp",
                            korean_name="조회구분",
                            param_type="select",
                            choices=[("전일거래량 상위100종목", "1"), ("전일거래대금 상위100종목", "2")],
                            required=True,
                            validation=None,
                        ),
                        ParameterConfig(
                            name="rank_strt",
                            korean_name="순위시작",
                            param_type="text",
                            validation=r"^[0-9]{1,3}$",
                            required=True,
                            choices=None,
                        ),
                        ParameterConfig(
                            name="rank_end",
                            korean_name="순위끝",
                            param_type="text",
                            validation=r"^[0-9]{1,3}$",
                            required=True,
                            choices=None,
                        ),
                        ParameterConfig(
                            name="stex_tp",
                            korean_name="거래소구분",
                            param_type="select",
                            choices=[("KRX", "1"), ("NXT", "2")],
                            required=True,
                            validation=None,
                        ),
                    ],
                ),
                APIConfig(
                    name="trading_value_top",
                    korean_name="💵 거래대금상위요청",
                    api_method="get_trading_value_top",
                    description="거래대금 상위 종목들을 조회합니다.",
                    required_params=[
                        ParameterConfig(
                            name="mrkt_tp",
                            korean_name="시장구분",
                            param_type="select",
                            choices=[("전체", "000"), ("코스피", "001"), ("코스닥", "101")],
                            required=True,
                            validation=None,
                        ),
                        ParameterConfig(
                            name="mang_stk_incls",
                            korean_name="관리종목포함",
                            param_type="select",
                            choices=[("미포함", "0"), ("포함", "1")],
                            required=True,
                            validation=None,
                        ),
                        ParameterConfig(
                            name="stex_tp",
                            korean_name="거래소구분",
                            param_type="select",
                            choices=[("KRX", "1"), ("NXT", "2")],
                            required=True,
                            validation=None,
                        ),
                    ],
                ),
                APIConfig(
                    name="foreign_period_trading_top",
                    korean_name="🌍 외인기간별매매상위요청",
                    api_method="get_foreign_period_trading_top",
                    description="외국인 기간별 매매 상위 종목들을 조회합니다.",
                    required_params=[
                        ParameterConfig(
                            name="mrkt_tp",
                            korean_name="시장구분",
                            param_type="select",
                            choices=[("전체", "000"), ("코스피", "001"), ("코스닥", "101")],
                            required=True,
                            validation=None,
                        ),
                        ParameterConfig(
                            name="trde_tp",
                            korean_name="매매구분",
                            param_type="select",
                            choices=[("순매도", "1"), ("순매수", "2"), ("순매매", "3")],
                            required=True,
                            validation=None,
                        ),
                        ParameterConfig(
                            name="dt",
                            korean_name="기간",
                            param_type="select",
                            choices=[
                                ("당일", "0"),
                                ("전일", "1"),
                                ("5일", "5"),
                                ("10일", "10"),
                                ("20일", "20"),
                                ("60일", "60"),
                            ],
                            required=True,
                            validation=None,
                        ),
                        ParameterConfig(
                            name="stex_tp",
                            korean_name="거래소구분",
                            param_type="select",
                            choices=[("KRX", "1"), ("NXT", "2"), ("통합", "3")],
                            required=True,
                            validation=None,
                        ),
                    ],
                ),
                APIConfig(
                    name="foreign_consecutive_trading_top",
                    korean_name="🔄 외인연속순매매상위요청",
                    api_method="get_foreign_consecutive_trading_top",
                    description="외국인 연속 순매매 상위 종목들을 조회합니다.",
                    required_params=[
                        ParameterConfig(
                            name="mrkt_tp",
                            korean_name="시장구분",
                            param_type="select",
                            choices=[("전체", "000"), ("코스피", "001"), ("코스닥", "101")],
                            required=True,
                            validation=None,
                        ),
                        ParameterConfig(
                            name="trde_tp",
                            korean_name="매매구분",
                            param_type="select",
                            choices=[("연속순매도", "1"), ("연속순매수", "2")],
                            required=True,
                            validation=None,
                        ),
                        ParameterConfig(
                            name="base_dt_tp",
                            korean_name="기준일구분",
                            param_type="select",
                            choices=[("당일기준", "0"), ("전일기준", "1")],
                            required=True,
                            validation=None,
                        ),
                        ParameterConfig(
                            name="stex_tp",
                            korean_name="거래소구분",
                            param_type="select",
                            choices=[("KRX", "1"), ("NXT", "2"), ("통합", "3")],
                            required=True,
                            validation=None,
                        ),
                    ],
                ),
                APIConfig(
                    name="foreign_institutional_trading_top",
                    korean_name="🏛️ 외국인기관매매상위요청",
                    api_method="get_foreign_institutional_trading_top",
                    description="외국인 기관 매매 상위 종목들을 조회합니다.",
                    required_params=[
                        ParameterConfig(
                            name="mrkt_tp",
                            korean_name="시장구분",
                            param_type="select",
                            choices=[("전체", "000"), ("코스피", "001"), ("코스닥", "101")],
                            required=True,
                            validation=None,
                        ),
                        ParameterConfig(
                            name="trde_tp",
                            korean_name="매매구분",
                            param_type="select",
                            choices=[("순매도", "1"), ("순매수", "2"), ("순매매", "3")],
                            required=True,
                            validation=None,
                        ),
                        ParameterConfig(
                            name="dt",
                            korean_name="기간",
                            param_type="select",
                            choices=[
                                ("당일", "0"),
                                ("전일", "1"),
                                ("5일", "5"),
                                ("10일", "10"),
                                ("20일", "20"),
                                ("60일", "60"),
                            ],
                            required=True,
                            validation=None,
                        ),
                        ParameterConfig(
                            name="inv_tp",
                            korean_name="투자자구분",
                            param_type="select",
                            choices=[("외국인", "1"), ("기관", "2"), ("기타법인", "3"), ("개인", "4")],
                            required=True,
                            validation=None,
                        ),
                        ParameterConfig(
                            name="stex_tp",
                            korean_name="거래소구분",
                            param_type="select",
                            choices=[("KRX", "1"), ("NXT", "2"), ("통합", "3")],
                            required=True,
                            validation=None,
                        ),
                    ],
                ),
            ],
        )

    def _format_and_display_result(self, result: Any, api_config: APIConfig) -> None:
        """
        Format and display ranking API results.

        Args:
            result: The API response data
            api_config: Configuration for the API that was called
        """
        self.formatter.format_ranking_data(result, api_config)
