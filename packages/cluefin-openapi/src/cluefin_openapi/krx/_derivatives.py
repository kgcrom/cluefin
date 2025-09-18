from cluefin_openapi.krx._client import Client
from cluefin_openapi.krx._derivatives_types import (
    DerivativesTradingOfFuturesExcludeStock,
    DerivativesTradingOfKosdaqFutures,
    DerivativesTradingOfKosdaqOption,
    DerivativesTradingOfKospiFutures,
    DerivativesTradingOfKospiOption,
    DerivativesTradingOfOptionExcludeStock,
)
from cluefin_openapi.krx._factory import KrxApiMethodFactory


class Derivatives:
    def __init__(self, client: Client):
        self.client = client
        self.path = "/svc/apis/drv/{}"

        self.get_trading_of_futures_exclude_stock = KrxApiMethodFactory.create_single_param_method(
            client=self.client,
            path_template=self.path,
            endpoint="fut_bydd_trd.json",
            response_model=DerivativesTradingOfFuturesExcludeStock,
            docstring="""선물 일별매매정보 (주식선물外)

        Args:
            base_date (str): 기준일자 (YYYYMMDD)

        Returns:
            KrxHttpResponse[DerivativesTradingOfFuturesExcludeStock]: 주식선물 거래정보 응답""",
        )

        self.get_trading_of_kospi_futures = KrxApiMethodFactory.create_single_param_method(
            client=self.client,
            path_template=self.path,
            endpoint="eqsfu_stk_bydd_trd.json",
            response_model=DerivativesTradingOfKospiFutures,
            docstring="""주식선물(코스피) 거래정보 조회

        Args:
            base_date (str): 기준일자 (YYYYMMDD)

        Returns:
            KrxHttpResponse[DerivativesTradingOfKospiFutures]: 주식선물 거래정보 응답""",
        )

        self.get_trading_of_kosdaq_futures = KrxApiMethodFactory.create_single_param_method(
            client=self.client,
            path_template=self.path,
            endpoint="eqkfu_ksq_bydd_trd.json",
            response_model=DerivativesTradingOfKosdaqFutures,
            docstring="""주식선물(코스닥) 거래정보 조회

        Args:
            base_date (str): 기준일자 (YYYYMMDD)

        Returns:
            KrxHttpResponse[DerivativesTradingOfKosdaqFutures]: 주식선물(코스닥) 거래정보 응답""",
        )

        self.get_trading_of_option_exclude_stock = KrxApiMethodFactory.create_single_param_method(
            client=self.client,
            path_template=self.path,
            endpoint="opt_bydd_trd.json",
            response_model=DerivativesTradingOfOptionExcludeStock,
            docstring="""주식옵션 거래정보 조회

        Args:
            base_date (str): 기준일자 (YYYYMMDD)

        Returns:
            KrxHttpResponse[DerivativesTradingOfOptionExcludeStock]: 주식옵션 거래정보 응답""",
        )

        self.get_trading_of_kospi_option = KrxApiMethodFactory.create_single_param_method(
            client=self.client,
            path_template=self.path,
            endpoint="eqsop_bydd_trd.json",
            response_model=DerivativesTradingOfKospiOption,
            docstring="""주식 옵션(코스피) 거래정보 조회

        Args:
            base_date (str): 기준일자 (YYYYMMDD)

        Returns:
            KrxHttpResponse[DerivativesTradingOfKospiOption]: 코스피 옵션 거래정보 응답""",
        )

        self.get_trading_of_kosdaq_option = KrxApiMethodFactory.create_single_param_method(
            client=self.client,
            path_template=self.path,
            endpoint="eqkop_bydd_trd.json",
            response_model=DerivativesTradingOfKosdaqOption,
            docstring="""주식 옵션(코스닥) 거래정보 조회

        Args:
            base_date (str): 기준일자 (YYYYMMDD)

        Returns:
            KrxHttpResponse[DerivativesTradingOfKosdaqOption]: 주식 옵션(코스닥) 거래정보 응답""",
        )
