from cluefin_openapi.krx._client import Client
from cluefin_openapi.krx._factory import KrxApiMethodFactory
from cluefin_openapi.krx._index_types import (
    IndexBond,
    IndexDerivatives,
    IndexKosdaq,
    IndexKospi,
    IndexKrx,
)


class Index:
    def __init__(self, client: Client):
        self.client = client
        self.path = "/svc/apis/idx/{}"

        self.get_krx = KrxApiMethodFactory.create_single_param_method(
            client=self.client,
            path_template=self.path,
            endpoint="krx_dd_trd.json",
            response_model=IndexKrx,
            docstring="KRX 지수 일별 시세 조회\n\nArgs:\n    base_date (str): 조회할 날짜 (YYYYMMDD 형식)\n\nReturns:\n    KrxHttpResponse[IndexKrx]: KRX 지수 일별 시세 데이터",
        )

        self.get_kospi = KrxApiMethodFactory.create_single_param_method(
            client=self.client,
            path_template=self.path,
            endpoint="kospi_dd_trd.json",
            response_model=IndexKospi,
            docstring="KOSPI 지수 일별 시세 조회\n\nArgs:\n    base_date (str): 조회할 날짜 (YYYYMMDD 형식)\n\nReturns:\n    KrxHttpResponse[IndexKospi]: KOSPI 지수 일별 시세 데이터",
        )

        self.get_kosdaq = KrxApiMethodFactory.create_single_param_method(
            client=self.client,
            path_template=self.path,
            endpoint="kosdaq_dd_trd.json",
            response_model=IndexKosdaq,
            docstring="KOSDAQ 지수 일별 시세 조회\n\nArgs:\n    base_date (str): 조회할 날짜 (YYYYMMDD 형식)\n\nReturns:\n    KrxHttpResponse[IndexKosdaq]: KOSDAQ 지수 일별 시세 데이터",
        )

        self.get_bond = KrxApiMethodFactory.create_single_param_method(
            client=self.client,
            path_template=self.path,
            endpoint="bon_dd_trd.json",
            response_model=IndexBond,
            docstring="채권 지수 일별 시세 조회\n\nArgs:\n    base_date (str): 조회할 날짜 (YYYYMMDD 형식)\n\nReturns:\n    KrxHttpResponse[IndexBond]: 채권 지수 일별 시세 데이터",
        )

        self.get_derivatives = KrxApiMethodFactory.create_single_param_method(
            client=self.client,
            path_template=self.path,
            endpoint="drvprod_dd_trd.json",
            response_model=IndexDerivatives,
            docstring="파생상품 지수 일별 시세 조회\n\nArgs:\n    base_date (str): 조회할 날짜 (YYYYMMDD 형식)\n\nReturns:\n    KrxHttpResponse[IndexDerivatives]: 파생상품 지수 일별 시세 데이터",
        )
