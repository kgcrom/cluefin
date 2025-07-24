from cluefin_openapi.krx._client import Client
from cluefin_openapi.krx._derivatives_types import (
    DerivativesTradingOfFuturesExcludeStock,
    DerivativesTradingOfKosdaqFutures,
    DerivativesTradingOfKosdaqOption,
    DerivativesTradingOfKospiFutures,
    DerivativesTradingOfKospiOption,
    DerivativesTradingOfOptionExcludeStock,
)
from cluefin_openapi.krx._model import KrxHttpResponse


class Derivatives:
    def __init__(self, client: Client):
        self.client = client
        self.path = "/svc/apis/drv/{}"

    def get_trading_of_futures_exclude_stock(
        self, base_date: str
    ) -> KrxHttpResponse[DerivativesTradingOfFuturesExcludeStock]:
        """선물 일별매매정보 (주식선물外)

        Args:
            base_date (str): 기준일자 (YYYYMMDD)

        Returns:
            KrxHttpResponse[DerivativesTradingOfFuturesExcludeStock]: 주식선물 거래정보 응답
        """
        params = {"baseDd": base_date}

        response = self.client._get(self.path.format("fut_bydd_trd.json"), params=params)
        body = DerivativesTradingOfFuturesExcludeStock.model_validate(response)
        return KrxHttpResponse(body=body)

    def get_trading_of_kospi_futures(self, base_date: str) -> KrxHttpResponse[DerivativesTradingOfKospiFutures]:
        """주식선물(코스피) 거래정보 조회

        Args:
            base_date (str): 기준일자 (YYYYMMDD)

        Returns:
            KrxHttpResponse[DerivativesTradingOfKospiFutures]: 주식선물 거래정보 응답
        """
        params = {"baseDd": base_date}

        response = self.client._get(self.path.format("eqsfu_stk_bydd_trd.json"), params=params)
        body = DerivativesTradingOfKospiFutures.model_validate(response)
        return KrxHttpResponse(body=body)

    def get_trading_of_kosdaq_futures(self, base_date: str) -> KrxHttpResponse[DerivativesTradingOfKosdaqFutures]:
        """주식선물(코스닥) 거래정보 조회

        Args:
            base_date (str): 기준일자 (YYYYMMDD)

        Returns:
            KrxHttpResponse[DerivativesTradingOfKosdaqFutures]: 주식선물(코스닥) 거래정보 응답
        """
        params = {"baseDd": base_date}

        response = self.client._get(self.path.format("eqkfu_ksq_bydd_trd.json"), params=params)
        body = DerivativesTradingOfKosdaqFutures.model_validate(response)
        return KrxHttpResponse(body=body)

    def get_trading_of_option_exclude_stock(
        self, base_date: str
    ) -> KrxHttpResponse[DerivativesTradingOfOptionExcludeStock]:
        """주식옵션 거래정보 조회

        Args:
            base_date (str): 기준일자 (YYYYMMDD)

        Returns:
            KrxHttpResponse[DerivativesTradingOfOption]: 주식옵션 거래정보 응답
        """
        params = {"baseDd": base_date}

        response = self.client._get(self.path.format("opt_bydd_trd.json"), params=params)
        body = DerivativesTradingOfOptionExcludeStock.model_validate(response)
        return KrxHttpResponse(body=body)

    def get_trading_of_kospi_option(self, base_date: str) -> KrxHttpResponse[DerivativesTradingOfKospiOption]:
        """주식 옵션(코스피) 거래정보 조회

        Args:
            base_date (str): 기준일자 (YYYYMMDD)

        Returns:
            KrxHttpResponse[DerivativesTradingOfKospiOption]: 코스피 옵션 거래정보 응답
        """
        params = {"baseDd": base_date}

        response = self.client._get(self.path.format("eqsop_bydd_trd.json"), params=params)
        body = DerivativesTradingOfKospiOption.model_validate(response)
        return KrxHttpResponse(body=body)

    def get_trading_of_kosdaq_option(self, base_date: str) -> KrxHttpResponse[DerivativesTradingOfKosdaqOption]:
        """주식 옵션(코스닥) 거래정보 조회

        Args:
            base_date (str): 기준일자 (YYYYMMDD)

        Returns:
            KrxHttpResponse[DerivativesTradingOfKosdaqOption]: 주식 옵션(코스닥) 거래정보 응답
        """

        params = {"baseDd": base_date}

        response = self.client._get(self.path.format("eqkop_bydd_trd.json"), params=params)
        body = DerivativesTradingOfKosdaqOption.model_validate(response)
        return KrxHttpResponse(body=body)
