from cluefin_openapi.krx._client import Client
from cluefin_openapi.krx._model import KrxHttpResponse
from cluefin_openapi.krx._stock_types import (
    StockKonex,
    StockKonexBaseInfo,
    StockKosdaq,
    StockKosdaqBaseInfo,
    StockKospi,
    StockKospiBaseInfo,
    StockSubscriptionWarrant,
    StockWarrant,
)


class Stock:
    def __init__(self, client: Client):
        self.client = client
        self.path = "/svc/apis/sto/{}"

    def get_kospi(self, base_date: str) -> KrxHttpResponse[StockKospi]:
        """KOSPI 일별매매정보 조회

        Args:
            base_date (str): 조회할 날짜 (YYYYMMDD 형식)

        Returns:
            KrxHttpResponse[StockKospi]: KOSPI 일별매매정보 데이터
        """
        params = {"baseDd": base_date}
        response = self.client._get(self.path.format("stk_bydd_trd.json"), params=params)

        body = StockKospi.model_validate(response)
        return KrxHttpResponse(body=body)

    def get_kosdaq(self, base_date: str) -> KrxHttpResponse[StockKosdaq]:
        """KOSDAQ 일별매매정보 조회

        Args:
            base_date (str): 조회할 날짜 (YYYYMMDD 형식)

        Returns:
            KrxHttpResponse[StockKosdaq]: KOSDAQ 일별매매정보 데이터
        """
        params = {"baseDd": base_date}
        response = self.client._get(self.path.format("ksq_bydd_trd.json"), params=params)

        body = StockKosdaq.model_validate(response)
        return KrxHttpResponse(body=body)

    def get_konex(self, base_date: str) -> KrxHttpResponse[StockKonex]:
        """KONEX 일별매매정보 조회

        Args:
            base_date (str): 조회할 날짜 (YYYYMMDD 형식)

        Returns:
            KrxHttpResponse[StockKonex]: KONEX 일별매매정보 데이터
        """
        params = {"baseDd": base_date}
        response = self.client._get(self.path.format("knx_bydd_trd.json"), params=params)

        body = StockKonex.model_validate(response)
        return KrxHttpResponse(body=body)

    def get_warrant(self, base_date: str) -> KrxHttpResponse[StockWarrant]:
        """신주인수권증권 일별매매정보 조회

        Args:
            base_date (str): 조회할 날짜 (YYYYMMDD 형식)

        Returns:
            KrxHttpResponse[StockWarrant]: KOSDAQ 일별매매정보 데이터
        """
        params = {"baseDd": base_date}
        response = self.client._get(self.path.format("warrant_bydd_trd.json"), params=params)

        body = StockWarrant.model_validate(response)
        return KrxHttpResponse(body=body)

    def get_subscription_warrant(self, base_date: str) -> KrxHttpResponse[StockSubscriptionWarrant]:
        """신주인수권증서 일별매매정보 조회

        Args:
            base_date (str): 조회할 날짜 (YYYYMMDD 형식)

        Returns:
            KrxHttpResponse[StockSubscriptionWarrant]: 신주인수권증서 일별매매정보 데이터
        """
        params = {"baseDd": base_date}
        response = self.client._get(self.path.format("sr_bydd_trd.json"), params=params)

        body = StockSubscriptionWarrant.model_validate(response)
        return KrxHttpResponse(body=body)

    def get_kospi_base_info(self, base_date: str) -> KrxHttpResponse[StockKospiBaseInfo]:
        """KOSPI 기본 정보 조회

        Args:
            base_date (str): 조회할 날짜 (YYYYMMDD 형식)

        Returns:
            KrxHttpResponse[StockKospiBaseInfo]: KOSPI 기본 정보 데이터
        """
        params = {"baseDd": base_date}
        response = self.client._get(self.path.format("stk_isu_base_info.json"), params=params)

        body = StockKospiBaseInfo.model_validate(response)
        return KrxHttpResponse(body=body)

    def get_kosdaq_base_info(self, base_date: str) -> KrxHttpResponse[StockKosdaqBaseInfo]:
        """KOSDAQ 기본 정보 조회

        Args:
            base_date (str): 조회할 날짜 (YYYYMMDD 형식)

        Returns:
            KrxHttpResponse[StockKosdaqBaseInfo]: KOSDAQ 기본 정보 데이터
        """
        params = {"baseDd": base_date}
        response = self.client._get(self.path.format("ksq_isu_base_info.json"), params=params)

        body = StockKosdaqBaseInfo.model_validate(response)
        return KrxHttpResponse(body=body)

    def get_konex_base_info(self, base_date: str) -> KrxHttpResponse[StockKonexBaseInfo]:
        """KONEX 기본 정보 조회

        Args:
            base_date (str): 조회할 날짜 (YYYYMMDD 형식)

        Returns:
            KrxHttpResponse[StockKonexBaseInfo]: KONEX 기본 정보 데이터
        """
        params = {"baseDd": base_date}
        response = self.client._get(self.path.format("knx_isu_base_info.json"), params=params)

        body = StockKonexBaseInfo.model_validate(response)
        return KrxHttpResponse(body=body)
