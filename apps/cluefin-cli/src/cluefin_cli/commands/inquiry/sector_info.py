"""
Sector information module for stock inquiry.

This module handles all sector-related APIs (업종) including sector performance,
investor activity by sector, and sector indices.
"""

from datetime import datetime
from typing import Any, Optional

from cluefin_openapi.kiwoom import Client as KiwoomClient

from .base_api_module import BaseAPIModule
from .config_models import APICategory, APIConfig, ParameterConfig
from .display_formatter import SectorDataFormatter


class SectorInfoModule(BaseAPIModule):
    """
    Sector information module extending BaseAPIModule.

    Handles all sector-related APIs including sector performance,
    investor activity by sector, and sector indices.
    """

    def __init__(self, client: Optional[KiwoomClient] = None):
        """
        Initialize the sector information module.

        Args:
            client: Optional Kiwoom API client instance
        """
        super().__init__(client)
        # Use specialized formatter for sector data
        self.formatter = SectorDataFormatter()

    def get_api_category(self) -> APICategory:
        """
        Get the API category configuration for sector information.

        Returns:
            APICategory with all sector APIs configured
        """
        return APICategory(
            name="sector_info",
            korean_name="🏢 업종정보",
            description="업종별 투자자 활동, 현재가, 지수 등 업종 관련 정보를 제공합니다.",
            apis=[
                APIConfig(
                    name="industry_investor_net_buy",
                    korean_name="📊 업종별 투자자 순매수 요청",
                    api_method="get_industry_investor_net_buy",
                    description="업종별 투자자(개인, 외국인, 기관) 순매수 현황을 조회합니다.",
                    required_params=[
                        ParameterConfig(
                            name="mrkt_tp",
                            korean_name="시장구분",
                            param_type="select",
                            choices=[("코스피", "0"), ("코스닥", "1")],
                            required=True,
                            validation=None,
                        ),
                        ParameterConfig(
                            name="amt_qty_tp",
                            korean_name="금액수량구분",
                            param_type="select",
                            choices=[("금액", "0"), ("수량", "1")],
                            required=True,
                            validation=None,
                        ),
                        ParameterConfig(
                            name="base_dt",
                            korean_name="기준일자(YYYYMMDD)",
                            param_type="date",
                            required=True,
                            validation=r"r^\d{8}$",
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
                    name="industry_current_price",
                    korean_name="💰 업종현재가 요청",
                    api_method="get_industry_current_price",
                    description="업종별 현재가 정보를 조회합니다.",
                    required_params=[
                        ParameterConfig(
                            name="mrkt_tp",
                            korean_name="시장구분",
                            param_type="select",
                            choices=[("코스피", "0"), ("코스닥", "1"), ("코스피200", "2")],
                            required=True,
                            validation=None,
                        ),
                        ParameterConfig(
                            name="inds_cd",
                            korean_name="업종코드",
                            param_type="text",
                            validation=r"^\d{3}$",
                            required=True,
                            choices=None,
                        ),
                    ],
                ),
                APIConfig(
                    name="industry_price_by_sector",
                    korean_name="📈 업종별 주가요청",
                    api_method="get_industry_price_by_sector",
                    description="특정 업종의 주가 정보를 조회합니다.",
                    required_params=[
                        ParameterConfig(
                            name="mrkt_tp",
                            korean_name="시장구분",
                            param_type="select",
                            choices=[("코스피", "0"), ("코스닥", "1"), ("코스피200", "2")],
                            required=True,
                            validation=None,
                        ),
                        ParameterConfig(
                            name="inds_cd",
                            korean_name="업종코드",
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
                    name="all_industry_index",
                    korean_name="🌐 전업종 지수요청",
                    api_method="get_all_industry_index",
                    description="전체 업종의 지수 정보를 조회합니다.",
                    required_params=[
                        ParameterConfig(
                            name="inds_cd",
                            korean_name="업종코드",
                            param_type="select",
                            choices=[
                                ("종합(KOSPI)", "001"),
                                ("종합(KOSDAQ)", "101"),
                                ("KOSPI200", "201"),
                                ("대형주", "002"),
                                ("중형주", "003"),
                                ("소형주", "004"),
                                ("음식료품", "010"),
                                ("섬유의복", "020"),
                                ("종이목재", "030"),
                                ("화학", "040"),
                                ("의약품", "050"),
                                ("비금속광물", "060"),
                                ("철강금속", "070"),
                                ("기계", "080"),
                                ("전기전자", "090"),
                                ("의료정밀", "100"),
                                ("운수장비", "110"),
                                ("유통업", "120"),
                                ("전기가스업", "130"),
                                ("건설업", "140"),
                                ("운수창고", "150"),
                                ("통신업", "160"),
                                ("금융업", "170"),
                                ("은행", "180"),
                                ("증권", "190"),
                                ("보험", "200"),
                                ("서비스업", "210"),
                                ("제조업", "220"),
                            ],
                            required=True,
                            validation=None,
                        )
                    ],
                ),
                APIConfig(
                    name="daily_industry_current_price",
                    korean_name="📅 업종현재가 일별요청",
                    api_method="get_daily_industry_current_price",
                    description="업종별 일별 현재가 정보를 조회합니다.",
                    required_params=[
                        ParameterConfig(
                            name="mrkt_tp",
                            korean_name="시장구분",
                            param_type="select",
                            choices=[("코스피", "0"), ("코스닥", "1"), ("코스피200", "2")],
                            required=True,
                            validation=None,
                        ),
                        ParameterConfig(
                            name="inds_cd",
                            korean_name="업종코드",
                            param_type="text",
                            validation=r"^\d{3}$",
                            required=True,
                            choices=None,
                        ),
                        ParameterConfig(
                            name="strt_dt",
                            korean_name="시작일자(YYYYMMDD)",
                            param_type="date",
                            validation=r"r$\d{8}$",
                            required=True,
                            choices=None,
                        ),
                        ParameterConfig(
                            name="end_dt",
                            korean_name="종료일자(YYYYMMDD)",
                            param_type="date",
                            validation=r"r$\d{8}$",
                            required=True,
                            choices=None,
                        ),
                    ],
                ),
            ],
        )

    def _format_and_display_result(self, result: Any, api_config: APIConfig) -> None:
        """
        Format and display sector API results.

        Args:
            result: The API response data
            api_config: Configuration for the API that was called
        """
        self.formatter.format_sector_data(result, api_config.korean_name)
