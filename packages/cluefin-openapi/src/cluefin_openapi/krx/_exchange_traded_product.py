from cluefin_openapi.krx._client import Client
from cluefin_openapi.krx._exchange_traded_product_types import (
    ExchangeTradedELW,
    ExchangeTradedETF,
    ExchangeTradedETN,
)
from cluefin_openapi.krx._factory import KrxApiMethodFactory
from cluefin_openapi.krx._model import KrxHttpResponse


class ExchangeTradedProduct:
    def __init__(self, client: Client):
        self.client = client
        self.path = "/svc/apis/etp/{}"

        # ETF 일별매매정보 조회
        self.get_etf = KrxApiMethodFactory.create_single_param_method(
            client=self.client,
            path_template=self.path,
            endpoint="etf_bydd_trd.json",
            response_model=ExchangeTradedETF,
            docstring="ETF 일별매매정보 조회\n\nArgs:\n    base_date (str): 조회할 날짜 (YYYYMMDD 형식)\n\nReturns:\n    KrxHttpResponse[ExchangeTradedETF]: ETF 일별매매정보 데이터"
        )

        # ETN 일별매매정보 조회
        self.get_etn = KrxApiMethodFactory.create_single_param_method(
            client=self.client,
            path_template=self.path,
            endpoint="etn_bydd_trd.json",
            response_model=ExchangeTradedETN,
            docstring="ETN 일별매매정보 조회\n\nArgs:\n    base_date (str): 조회할 날짜 (YYYYMMDD 형식)\n\nReturns:\n    KrxHttpResponse[ExchangeTradedETN]: ETN 일별매매정보 데이터"
        )

        # ELW 일별매매정보 조회
        self.get_elw = KrxApiMethodFactory.create_single_param_method(
            client=self.client,
            path_template=self.path,
            endpoint="elw_bydd_trd.json",
            response_model=ExchangeTradedELW,
            docstring="ELW 일별매매정보 조회\n\nArgs:\n    base_date (str): 조회할 날짜 (YYYYMMDD 형식)\n\nReturns:\n    KrxHttpResponse[ExchangeTradedELW]: ELW 일별매매정보 데이터"
        )
