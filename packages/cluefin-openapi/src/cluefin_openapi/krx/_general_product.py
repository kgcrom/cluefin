from cluefin_openapi.krx._client import Client
from cluefin_openapi.krx._general_product_types import (
    GeneralProductEmissionsMarket,
    GeneralProductGoldMarket,
    GeneralProductOilMarket,
)
from cluefin_openapi.krx._model import KrxHttpResponse


class GeneralProduct:
    def __init__(self, client: Client):
        self.client = client
        self.path = "/svc/apis/gen/{}"

    def get_oil_market(self, base_date: str) -> KrxHttpResponse[GeneralProductOilMarket]:
        """석유시장 일별매매정보 조회

        Args:
            base_date (str): 기준일자 (YYYYMMDD)

        Returns:
            KrxHttpResponse[GeneralProductOilMarket]: 석유시장 일별매매정보
        """
        params = {"baseDd": base_date}
        response = self.client._get(self.path.format("oil_bydd_trd.json"), params=params)
        body = GeneralProductOilMarket.model_validate(response)
        return KrxHttpResponse(body=body)

    def get_gold_market(self, base_date: str) -> KrxHttpResponse[GeneralProductGoldMarket]:
        """금시장 일별매매정보 조회

        Args:
            base_date (str): 기준일자 (YYYYMMDD)

        Returns:
            KrxHttpResponse[GeneralProductGoldMarket]: 금시장 일별매매정보
        """
        params = {"baseDd": base_date}
        response = self.client._get(self.path.format("gold_bydd_trd.json"), params=params)
        body = GeneralProductGoldMarket.model_validate(response)
        return KrxHttpResponse(body=body)

    def get_emissions_market(self, base_date: str) -> KrxHttpResponse[GeneralProductEmissionsMarket]:
        """탄소 배출권시장 일별매매정보 조회

        Args:
            base_date (str): 기준일자 (YYYYMMDD)

        Returns:
            KrxHttpResponse[GeneralProductEmissionsMarket]: 탄소시장 일별매매정보
        """
        params = {"baseDd": base_date}
        response = self.client._get(self.path.format("carbon_bydd_trd.json"), params=params)
        body = GeneralProductEmissionsMarket.model_validate(response)
        return KrxHttpResponse(body=body)
