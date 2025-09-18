from cluefin_openapi.krx._client import Client
from cluefin_openapi.krx._factory import KrxApiMethodFactory
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

        # Factory-generated methods to eliminate code duplication
        self.get_kospi = KrxApiMethodFactory.create_single_param_method(
            client=self.client,
            path_template=self.path,
            endpoint="stk_bydd_trd.json",
            response_model=StockKospi,
            docstring="KOSPI 일별매매정보 조회\n\nArgs:\n    base_date (str): 조회할 날짜 (YYYYMMDD 형식)\n\nReturns:\n    KrxHttpResponse[StockKospi]: KOSPI 일별매매정보 데이터",
        )

        self.get_kosdaq = KrxApiMethodFactory.create_single_param_method(
            client=self.client,
            path_template=self.path,
            endpoint="ksq_bydd_trd.json",
            response_model=StockKosdaq,
            docstring="KOSDAQ 일별매매정보 조회\n\nArgs:\n    base_date (str): 조회할 날짜 (YYYYMMDD 형식)\n\nReturns:\n    KrxHttpResponse[StockKosdaq]: KOSDAQ 일별매매정보 데이터",
        )

        self.get_konex = KrxApiMethodFactory.create_single_param_method(
            client=self.client,
            path_template=self.path,
            endpoint="knx_bydd_trd.json",
            response_model=StockKonex,
            docstring="KONEX 일별매매정보 조회\n\nArgs:\n    base_date (str): 조회할 날짜 (YYYYMMDD 형식)\n\nReturns:\n    KrxHttpResponse[StockKonex]: KONEX 일별매매정보 데이터",
        )

        self.get_warrant = KrxApiMethodFactory.create_single_param_method(
            client=self.client,
            path_template=self.path,
            endpoint="sw_bydd_trd.json",
            response_model=StockWarrant,
            docstring="신주인수권증권 일별매매정보 조회\n\nArgs:\n    base_date (str): 조회할 날짜 (YYYYMMDD 형식)\n\nReturns:\n    KrxHttpResponse[StockWarrant]: 신주인수권증권 일별매매정보 데이터",
        )

        self.get_subscription_warrant = KrxApiMethodFactory.create_single_param_method(
            client=self.client,
            path_template=self.path,
            endpoint="sr_bydd_trd.json",
            response_model=StockSubscriptionWarrant,
            docstring="신주인수권증서 일별매매정보 조회\n\nArgs:\n    base_date (str): 조회할 날짜 (YYYYMMDD 형식)\n\nReturns:\n    KrxHttpResponse[StockSubscriptionWarrant]: 신주인수권증서 일별매매정보 데이터",
        )

        self.get_kospi_base_info = KrxApiMethodFactory.create_single_param_method(
            client=self.client,
            path_template=self.path,
            endpoint="stk_isu_base_info.json",
            response_model=StockKospiBaseInfo,
            docstring="KOSPI 기본 정보 조회\n\nArgs:\n    base_date (str): 조회할 날짜 (YYYYMMDD 형식)\n\nReturns:\n    KrxHttpResponse[StockKospiBaseInfo]: KOSPI 기본 정보 데이터",
        )

    def get_kosdaq_base_info(self, base_date: str) -> KrxHttpResponse[StockKosdaqBaseInfo]:
        """KOSDAQ 기본 정보 조회

        Args:
            base_date (str): 조회할 날짜 (YYYYMMDD 형식)

        Returns:
            KrxHttpResponse[StockKosdaqBaseInfo]: KOSDAQ 기본 정보 데이터
        """
        params = {"basDd": base_date}
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
        params = {"basDd": base_date}
        response = self.client._get(self.path.format("knx_isu_base_info.json"), params=params)

        body = StockKonexBaseInfo.model_validate(response)
        return KrxHttpResponse(body=body)
