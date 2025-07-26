from cluefin_openapi.krx._client import Client
from cluefin_openapi.krx._exchange_traded_product_types import (
    ExchangeTradedELW,
    ExchangeTradedETF,
    ExchangeTradedETN,
)
from cluefin_openapi.krx._model import KrxHttpResponse


class ExchangeTradedProduct:
    def __init__(self, client: Client):
        self.client = client
        self.path = "/svc/apis/etp/{}"

    def get_etf(self, base_date: str) -> KrxHttpResponse[ExchangeTradedETF]:
        """ETF 일별매매정보 조회

        Args:
            base_date (str): 조회할 날짜 (YYYYMMDD 형식)

        Returns:
            KrxHttpResponse[ExchangeTradedETF]: ETF 일별매매정보 데이터
        """
        params = {"basDd": base_date}
        response = self.client._get(self.path.format("etf_bydd_trd.json"), params=params)

        body = ExchangeTradedETF.model_validate(response)
        return KrxHttpResponse(body=body)

    def get_etn(self, base_date: str) -> KrxHttpResponse[ExchangeTradedETN]:
        """ETN 일별매매정보 조회

        Args:
            base_date (str): 조회할 날짜 (YYYYMMDD 형식)

        Returns:
            KrxHttpResponse[ExchangeTradedETN]: ETN 일별매매정보 데이터
        """
        params = {"basDd": base_date}
        response = self.client._get(self.path.format("etn_bydd_trd.json"), params=params)

        body = ExchangeTradedETN.model_validate(response)
        return KrxHttpResponse(body=body)

    def get_elw(self, base_date: str) -> KrxHttpResponse[ExchangeTradedELW]:
        """ELW 일별매매정보 조회

        Args:
            base_date (str): 조회할 날짜 (YYYYMMDD 형식)

        Returns:
            KrxHttpResponse[ExchangeTradedELW]: ELW 일별매매정보 데이터
        """
        params = {"basDd": base_date}
        response = self.client._get(self.path.format("elw_bydd_trd.json"), params=params)

        body = ExchangeTradedELW.model_validate(response)
        return KrxHttpResponse(body=body)
