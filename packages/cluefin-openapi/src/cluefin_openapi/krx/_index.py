from cluefin_openapi.krx._client import Client
from cluefin_openapi.krx._index_types import (
    IndexBond,
    IndexDerivatives,
    IndexKosdaq,
    IndexKospi,
    IndexKrx,
)
from cluefin_openapi.krx._model import KrxHttpResponse


class Index:
    def __init__(self, client: Client):
        self.client = client
        self.path = "/svc/apis/idx/{}"

    def get_krx(self, base_date: str) -> KrxHttpResponse[IndexKrx]:
        """KRX 지수 일별 시세 조회

        Args:
            base_date (str): 조회할 날짜 (YYYYMMDD 형식)

        Returns:
            KrxHttpResponse[IndexKrx]: KRX 지수 일별 시세 데이터
        """
        params = {"basDd": base_date}
        response = self.client._get(self.path.format("krx_dd_trd.json"), params=params)

        body = IndexKrx.model_validate(response)
        return KrxHttpResponse(body=body)

    def get_kospi(self, base_date: str) -> KrxHttpResponse[IndexKospi]:
        """KOSPI 지수 일별 시세 조회

        Args:
            base_date (str): 조회할 날짜 (YYYYMMDD 형식)

        Returns:
            KrxHttpResponse[IndexKospi]: KOSPI 지수 일별 시세 데이터
        """
        params = {"basDd": base_date}
        response = self.client._get(self.path.format("kospi_dd_trd.json"), params=params)

        body = IndexKospi.model_validate(response)
        return KrxHttpResponse(body=body)

    def get_kosdaq(self, base_date: str) -> KrxHttpResponse[IndexKosdaq]:
        """KOSDAQ 지수 일별 시세 조회

        Args:
            base_date (str): 조회할 날짜 (YYYYMMDD 형식)

        Returns:
            KrxHttpResponse[IndexKosdaq]: KOSDAQ 지수 일별 시세 데이터
        """
        params = {"basDd": base_date}
        response = self.client._get(self.path.format("kosdaq_dd_trd.json"), params=params)

        body = IndexKosdaq.model_validate(response)
        return KrxHttpResponse(body=body)

    def get_bond(self, base_date: str) -> KrxHttpResponse[IndexBond]:
        """채권 지수 일별 시세 조회

        Args:
            base_date (str): 조회할 날짜 (YYYYMMDD 형식)

        Returns:
            KrxHttpResponse[IndexBond]: 채권 지수 일별 시세 데이터
        """
        params = {"basDd": base_date}
        response = self.client._get(self.path.format("bon_dd_trd.json"), params=params)

        body = IndexBond.model_validate(response)
        return KrxHttpResponse(body=body)

    def get_derivatives(self, base_date: str) -> KrxHttpResponse[IndexDerivatives]:
        """파생상품 지수 일별 시세 조회

        Args:
            base_date (str): 조회할 날짜 (YYYYMMDD 형식)

        Returns:
            KrxHttpResponse[IndexDerivatives]: 파생상품 지수 일별 시세 데이터
        """
        params = {"basDd": base_date}
        response = self.client._get(self.path.format("drvprod_dd_trd.json"), params=params)

        body = IndexDerivatives.model_validate(response)
        return KrxHttpResponse(body=body)
