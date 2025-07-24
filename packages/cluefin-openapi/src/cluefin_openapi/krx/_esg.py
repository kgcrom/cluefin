from cluefin_openapi.krx._client import Client
from cluefin_openapi.krx._esg_types import (
    EsgSociallyResponsibleInvestmentBond,
)
from cluefin_openapi.krx._model import KrxHttpResponse


class Esg:
    def __init__(self, client: Client):
        self.client = client
        self.path = "/svc/apis/esg/{}"

    def get_socially_responsible_investment_bond(
        self, base_data
    ) -> KrxHttpResponse[EsgSociallyResponsibleInvestmentBond]:
        """사회책임투자채권 정보 조회

        Args:
            base_data (str): 기준일자 (YYYYMMDD)

        Returns:
            KrxHttpResponse[EsgSociallyResponsibleInvestmentBond]: 사회책임투자채권 정보
        """
        params = {"baseDd": base_data}

        response = self.client._get(self.path.format("sri_bond_info.json"), params=params)
        body = EsgSociallyResponsibleInvestmentBond.model_validate(response)
        return KrxHttpResponse(body=body)
