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
                    description="특정 종목의 거래량 갱신 정보를 실시간으로 조회합니다.",
                    required_params=[
                        ParameterConfig(
                            name="stk_cd",
                            korean_name="종목코드",
                            param_type="text",
                            validation=r"^\d{6}$"
                        )
                    ]
                ),
                APIConfig(
                    name="supply_demand_concentration",
                    korean_name="💹 매출대집중요청",
                    api_method="get_supply_demand_concentration",
                    description="특정 종목의 매도/매수 호가 집중도를 분석합니다.",
                    required_params=[
                        ParameterConfig(
                            name="stk_cd",
                            korean_name="종목코드",
                            param_type="text",
                            validation=r"^\d{6}$"
                        ),
                        ParameterConfig(
                            name="prc_tp",
                            korean_name="가격구분",
                            param_type="select",
                            choices=[("매도호가", "1"), ("매수호가", "2")]
                        )
                    ]
                ),
                APIConfig(
                    name="broker_supply_demand_analysis",
                    korean_name="🏢 거래원매물대분석요청",
                    api_method="get_broker_supply_demand_analysis",
                    description="특정 종목의 거래원별 매물대 분석 정보를 조회합니다.",
                    required_params=[
                        ParameterConfig(
                            name="stk_cd",
                            korean_name="종목코드",
                            param_type="text",
                            validation=r"^\d{6}$"
                        )
                    ]
                ),
                APIConfig(
                    name="stock_investor_institutional_total",
                    korean_name="👥 종목별투자자기관별합계요청",
                    api_method="get_stock_investor_institutional_total",
                    description="특정 종목의 투자자별, 기관별 매매 합계를 조회합니다.",
                    required_params=[
                        ParameterConfig(
                            name="stk_cd",
                            korean_name="종목코드",
                            param_type="text",
                            validation=r"^\d{6}$"
                        ),
                        ParameterConfig(
                            name="trd_dt",
                            korean_name="거래일자구분",
                            param_type="select",
                            choices=[("당일", "0"), ("전일", "1")]
                        )
                    ]
                ),
                APIConfig(
                    name="stock_basic_info",
                    korean_name="📊 종목기본정보요청",
                    api_method="get_stock_basic_info",
                    description="특정 종목의 기본 정보를 조회합니다.",
                    required_params=[
                        ParameterConfig(
                            name="stk_cd",
                            korean_name="종목코드",
                            param_type="text",
                            validation=r"^\d{6}$"
                        )
                    ]
                ),
                APIConfig(
                    name="stock_price_info",
                    korean_name="💲 종목현재가정보요청",
                    api_method="get_stock_price_info",
                    description="특정 종목의 현재가 및 관련 정보를 조회합니다.",
                    required_params=[
                        ParameterConfig(
                            name="stk_cd",
                            korean_name="종목코드",
                            param_type="text",
                            validation=r"^\d{6}$"
                        )
                    ]
                ),
                APIConfig(
                    name="stock_order_book",
                    korean_name="📋 종목호가정보요청",
                    api_method="get_stock_order_book",
                    description="특정 종목의 매도/매수 호가 정보를 조회합니다.",
                    required_params=[
                        ParameterConfig(
                            name="stk_cd",
                            korean_name="종목코드",
                            param_type="text",
                            validation=r"^\d{6}$"
                        )
                    ]
                ),
                APIConfig(
                    name="stock_daily_chart",
                    korean_name="📈 종목일봉차트요청",
                    api_method="get_stock_daily_chart",
                    description="특정 종목의 일봉 차트 데이터를 조회합니다.",
                    required_params=[
                        ParameterConfig(
                            name="stk_cd",
                            korean_name="종목코드",
                            param_type="text",
                            validation=r"^\d{6}$"
                        ),
                        ParameterConfig(
                            name="strt_dt",
                            korean_name="시작일자",
                            param_type="date"
                        ),
                        ParameterConfig(
                            name="end_dt",
                            korean_name="종료일자",
                            param_type="date"
                        )
                    ],
                    optional_params=[
                        ParameterConfig(
                            name="adj_prc_tp",
                            korean_name="수정주가구분",
                            param_type="select",
                            choices=[("수정안함", "0"), ("수정주가", "1")],
                            required=False
                        )
                    ]
                )
            ]
        )

    def _format_and_display_result(self, result: Any, api_config: APIConfig) -> None:
        """
        Format and display stock API results.
        
        Args:
            result: The API response data
            api_config: Configuration for the API that was called
        """
        self.formatter.format_stock_data(result, api_config.korean_name)


