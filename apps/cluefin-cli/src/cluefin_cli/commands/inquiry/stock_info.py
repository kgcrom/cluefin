"""
Stock information module for stock inquiry.

This module handles all stock-specific APIs (종목정보) including detailed stock
analysis, volume updates, and broker analysis.
"""

from typing import Any, Optional

from cluefin_openapi.kiwoom import Client as KiwoomClient

from .base_api_module import BaseAPIModule
from .config_models import APICategory, APIConfig, ParameterConfig
from .display_formatter import StockDataFormatter


class StockInfoModule(BaseAPIModule):
    """
    Stock information module extending BaseAPIModule.

    Handles all stock-specific APIs including detailed stock analysis,
    volume updates, and broker analysis.
    """

    def __init__(self, client: Optional[KiwoomClient] = None):
        """
        Initialize the stock information module.

        Args:
            client: Optional Kiwoom API client instance
        """
        super().__init__(client)
        # Use specialized formatter for stock data
        self.formatter = StockDataFormatter()

    def get_client_attribute_name(self) -> str:
        """Get the client attribute name for stock info APIs."""
        return "stock_info"

    def get_api_category(self) -> APICategory:
        """
        Get the API category configuration for stock information.

        Returns:
            APICategory with all stock APIs configured
        """
        return APICategory(
            name="stock_info",
            korean_name="💰 종목정보",
            description="개별 종목의 상세 정보, 거래량 분석, 거래원 분석 등을 제공합니다.",
            apis=[
                APIConfig(
                    name="trading_volume_renewal",
                    korean_name="📈 거래량갱신요청",
                    api_method="get_trading_volume_renewal",
                    description="시장의 거래량 갱신 정보를 조회합니다.",
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
                            name="cycle_tp",
                            korean_name="주기구분",
                            param_type="select",
                            choices=[("5일", "5"), ("10일", "10"), ("20일", "20"), ("60일", "60"), ("250일", "250")],
                            required=True,
                            validation=None,
                        ),
                        ParameterConfig(
                            name="trde_qty_tp",
                            korean_name="거래량구분",
                            param_type="select",
                            choices=[
                                ("5천주이상", "5"),
                                ("만주이상", "10"),
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
                    name="supply_demand_concentration",
                    korean_name="💹 매물대집중요청",
                    api_method="get_supply_demand_concentration",
                    description="시장의 매물대 집중도를 분석합니다.",
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
                            name="prps_cnctr_rt",
                            korean_name="매물집중비율",
                            param_type="text",
                            validation=r"^([0-9]|[1-9][0-9]|100)$",
                            required=True,
                            choices=None,
                        ),
                        ParameterConfig(
                            name="cur_prc_entry",
                            korean_name="현재가진입",
                            param_type="select",
                            choices=[("포함안함", "0"), ("포함", "1")],
                            required=True,
                            validation=None,
                        ),
                        ParameterConfig(
                            name="prpscnt",
                            korean_name="매물대수",
                            param_type="text",
                            validation=r"^\d+$",
                            required=True,
                            choices=None,
                        ),
                        ParameterConfig(
                            name="cycle_tp",
                            korean_name="주기구분",
                            param_type="select",
                            choices=[
                                ("50일", "50"),
                                ("100일", "100"),
                                ("150일", "150"),
                                ("200일", "200"),
                                ("250일", "250"),
                                ("300일", "300"),
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
                ),
                APIConfig(
                    name="trading_member_supply_demand_analysis",
                    korean_name="🏢 거래원매물대분석요청",
                    api_method="get_trading_member_supply_demand_analysis",
                    description="특정 종목의 거래원별 매물대 분석 정보를 조회합니다.",
                    required_params=[
                        ParameterConfig(
                            name="stk_cd",
                            korean_name="종목코드",
                            param_type="text",
                            validation=r"^\d{6}$",
                            required=True,
                            choices=None,
                        ),
                        ParameterConfig(
                            name="strt_dt",
                            korean_name="시작일자(YYYYMMDD)",
                            param_type="date",
                            validation=r"^\d{8}$",
                            required=True,
                            choices=None,
                        ),
                        ParameterConfig(
                            name="end_dt",
                            korean_name="종료일자(YYYYMMDD)",
                            param_type="date",
                            validation=r"^\d{8}$",
                            required=True,
                            choices=None,
                        ),
                        ParameterConfig(
                            name="qry_dt_tp",
                            korean_name="조회기간구분",
                            param_type="select",
                            choices=[("기간으로 조회", "0"), ("시작/종료일자로 조회", "1")],
                            required=True,
                            validation=None,
                        ),
                        ParameterConfig(
                            name="pot_tp",
                            korean_name="시점구분",
                            param_type="select",
                            choices=[("당일", "0"), ("전일", "1")],
                            required=True,
                            validation=None,
                        ),
                        ParameterConfig(
                            name="dt",
                            korean_name="기간",
                            param_type="select",
                            choices=[
                                ("5일", "5"),
                                ("10일", "10"),
                                ("20일", "20"),
                                ("40일", "40"),
                                ("60일", "60"),
                                ("120일", "120"),
                            ],
                            required=True,
                            validation=None,
                        ),
                        ParameterConfig(
                            name="sort_base",
                            korean_name="정렬기준",
                            param_type="select",
                            choices=[("종가순", "1"), ("날짜순", "2")],
                            required=True,
                            validation=None,
                        ),
                        ParameterConfig(
                            name="mmcm_cd",
                            korean_name="회원사코드",
                            param_type="text",
                            validation=r"^\d{3}$",
                            required=True,
                            choices=None,
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
                    name="total_institutional_investor_by_stock",
                    korean_name="👥 종목별투자자기관합계요청",
                    api_method="get_total_institutional_investor_by_stock",
                    description="특정 종목의 투자자별, 기관별 매매 합계를 조회합니다.",
                    required_params=[
                        ParameterConfig(
                            name="stk_cd",
                            korean_name="종목코드",
                            param_type="text",
                            validation=r"^\d{6}$",
                            required=True,
                            choices=None,
                        ),
                        ParameterConfig(
                            name="strt_dt",
                            korean_name="시작일자(YYYYMMDD)",
                            param_type="date",
                            validation=r"^\d{8}$",
                            required=True,
                            choices=None,
                        ),
                        ParameterConfig(
                            name="end_dt",
                            korean_name="종료일자(YYYYMMDD)",
                            param_type="date",
                            validation=r"^\d{8}$",
                            required=True,
                            choices=None,
                        ),
                        ParameterConfig(
                            name="amt_qty_tp",
                            korean_name="금액수량구분",
                            param_type="select",
                            choices=[("금액", "1"), ("수량", "2")],
                            required=True,
                            validation=None,
                        ),
                        ParameterConfig(
                            name="trde_tp",
                            korean_name="매매구분",
                            param_type="select",
                            choices=[("순매수", "0"), ("매수", "1"), ("매도", "2")],
                            required=True,
                            validation=None,
                        ),
                        ParameterConfig(
                            name="unit_tp",
                            korean_name="단위구분",
                            param_type="select",
                            choices=[("천주", "1000"), ("단주", "1")],
                            required=True,
                            validation=None,
                        ),
                    ],
                ),
                APIConfig(
                    name="stock_info",
                    korean_name="📊 주식기본정보요청",
                    api_method="get_stock_info",
                    description="특정 종목의 기본 정보를 조회합니다.",
                    required_params=[
                        ParameterConfig(
                            name="stk_cd",
                            korean_name="종목코드",
                            param_type="text",
                            validation=r"^\d{6}$",
                            required=True,
                            choices=None,
                        )
                    ],
                ),
            ],
        )

    def _format_and_display_result(self, result: Any, api_config: APIConfig) -> None:
        """
        Format and display stock API results.

        Args:
            result: The API response data
            api_config: Configuration for the API that was called
        """
        self.formatter.format_stock_data(result, api_config)
