from cluefin_openapi.krx._bond_types import (
    BondGeneralBondMarket,
    BondKoreaTreasuryBondMarket,
    BondSmallBondMarket,
)
from cluefin_openapi.krx._client import Client
from cluefin_openapi.krx._model import KrxHttpResponse


class Bond:
    def __init__(self, client: Client):
        self.client = client
        self.path = "/svc/apis/bon/{}"

    def get_korea_treasury_bond_market(self, base_date: str) -> KrxHttpResponse[BondKoreaTreasuryBondMarket]:
        """국채전문유통시장 일별매매정보 조회

        Args:
            base_date (str): 기준일자 (YYYYMMDD)

        Returns:
            KrxHttpResponse[BondKoreaTreasuryBondMarket]: 국채전문유통시장 일별매매정보 응답
        """
        params = {"basDd": base_date}

        response = self.client._get(self.path.format("kts_bydd_trd.json"), params=params)
        body = BondKoreaTreasuryBondMarket.model_validate(response)
        return KrxHttpResponse(body=body)

    def get_general_bond_market(self, base_date: str) -> KrxHttpResponse[BondGeneralBondMarket]:
        """일반채권시장 일별매매정보 조회

        Args:
            base_date (str): 기준일자 (YYYYMMDD)

        Returns:
            KrxHttpResponse[BondGeneralBondMarket]: 일반채권시장 일별매매정보 응답
        """
        params = {"basDd": base_date}

        response = self.client._get(self.path.format("bnd_bydd_trd.json"), params=params)
        body = BondGeneralBondMarket.model_validate(response)
        return KrxHttpResponse(body=body)

    def get_small_bond_market(self, base_date: str) -> KrxHttpResponse[BondSmallBondMarket]:
        """소액채권시장 일별매매정보 조회

        Args:
            base_date (str): 기준일자 (YYYYMMDD)

        Returns:
            KrxHttpResponse[BondSmallBondMarket]: 소액채권시장 일별매매정보 응답
        """
        params = {"basDd": base_date}

        response = self.client._get(self.path.format("smb_bydd_trd.json"), params=params)
        body = BondSmallBondMarket.model_validate(response)
        return KrxHttpResponse(body=body)
