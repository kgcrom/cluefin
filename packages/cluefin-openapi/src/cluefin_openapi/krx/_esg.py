from cluefin_openapi.krx._client import Client
from cluefin_openapi.krx._esg_types import (
    EsgSociallyResponsibleInvestmentBond,
)
from cluefin_openapi.krx._factory import KrxApiMethodFactory


class Esg:
    def __init__(self, client: Client):
        self.client = client
        self.path = "/svc/apis/esg/{}"

        # 사회책임투자채권 정보 조회
        self.get_socially_responsible_investment_bond = KrxApiMethodFactory.create_single_param_method(
            client=self.client,
            path_template=self.path,
            endpoint="sri_bond_info.json",
            response_model=EsgSociallyResponsibleInvestmentBond,
            docstring="사회책임투자채권 정보 조회\n\nArgs:\n    base_date (str): 기준일자 (YYYYMMDD)\n\nReturns:\n    KrxHttpResponse[EsgSociallyResponsibleInvestmentBond]: 사회책임투자채권 정보",
        )
