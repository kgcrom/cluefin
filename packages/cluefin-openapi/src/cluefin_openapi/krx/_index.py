from cluefin_openapi.krx._client import Client
from cluefin_openapi.krx._index_types import (
    IndexBondByDate,
    IndexDerivativesByDate,
    IndexKosdaqByDate,
    IndexKospiByDate,
    IndexKrxByDate,
)
from cluefin_openapi.krx._model import KrxHttpResponse


class Index:
    def __init__(self, client: Client):
        self.client = client
        self.path = "/svc/apis/idx/{}"

    def get_krx_by_date(self, base_date: str) -> KrxHttpResponse[IndexKrxByDate]:
        """KRX 지수 일별 시세 조회

        Args:
            base_date (str): 조회할 날짜 (YYYYMMDD 형식)

        Returns:
            KrxHttpResponse[IndexKrxByDate]: KRX 지수 일별 시세 데이터
        """
        params = {"baseDd": base_date}
        response = self.client._get(self.path.format("krx_dd_trd.json"), params=params)

        body = IndexKrxByDate.model_validate(response)
        return KrxHttpResponse(body=body)

    def get_kospi_by_date(self, base_date: str) -> KrxHttpResponse[IndexKospiByDate]:
        """KOSPI 지수 일별 시세 조회

        Args:
            base_date (str): 조회할 날짜 (YYYYMMDD 형식)

        Returns:
            KrxHttpResponse[IndexKospiByDate]: KOSPI 지수 일별 시세 데이터
        """
        params = {"baseDd": base_date}
        response = self.client._get(self.path.format("kospi_dd_trd.json"), params=params)

        body = IndexKospiByDate.model_validate(response)
        return KrxHttpResponse(body=body)

    def get_kosdaq_by_date(self, base_date: str) -> KrxHttpResponse[IndexKosdaqByDate]:
        """KOSDAQ 지수 일별 시세 조회

        Args:
            base_date (str): 조회할 날짜 (YYYYMMDD 형식)

        Returns:
            KrxHttpResponse[IndexKosdaqByDate]: KOSDAQ 지수 일별 시세 데이터
        """
        params = {"baseDd": base_date}
        response = self.client._get(self.path.format("kosdaq_dd_trd.json"), params=params)

        body = IndexKosdaqByDate.model_validate(response)
        return KrxHttpResponse(body=body)

    def get_bond_by_date(self, base_date: str) -> KrxHttpResponse[IndexBondByDate]:
        """채권 지수 일별 시세 조회

        Args:
            base_date (str): 조회할 날짜 (YYYYMMDD 형식)

        Returns:
            KrxHttpResponse[IndexBondByDate]: 채권 지수 일별 시세 데이터
        """
        params = {"baseDd": base_date}
        response = self.client._get(self.path.format("bond_dd_trd.json"), params=params)

        body = IndexBondByDate.model_validate(response)
        return KrxHttpResponse(body=body)

    def get_derivatives_by_date(self, base_date: str) -> KrxHttpResponse[IndexDerivativesByDate]:
        """파생상품 지수 일별 시세 조회

        Args:
            base_date (str): 조회할 날짜 (YYYYMMDD 형식)

        Returns:
            KrxHttpResponse[IndexDerivativesByDate]: 파생상품 지수 일별 시세 데이터
        """
        params = {"baseDd": base_date}
        response = self.client._get(self.path.format("derivatives_dd_trd.json"), params=params)

        body = IndexDerivativesByDate.model_validate(response)
        return KrxHttpResponse(body=body)
