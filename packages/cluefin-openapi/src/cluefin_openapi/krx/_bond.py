from cluefin_openapi.krx._bond_types import (
    BondGeneralBondMarket,
    BondKoreaTreasuryBondMarket,
    BondSmallBondMarket,
)
from cluefin_openapi.krx._client import Client
from cluefin_openapi.krx._factory import KrxApiMethodFactory


class Bond:
    def __init__(self, client: Client):
        self.client = client
        self.path = "/svc/apis/bon/{}"

        # Use factory to create methods and eliminate code duplication
        self.get_korea_treasury_bond_market = KrxApiMethodFactory.create_single_param_method(
            client=self.client,
            path_template=self.path,
            endpoint="kts_bydd_trd.json",
            response_model=BondKoreaTreasuryBondMarket,
            docstring="""국채전문유통시장 일별매매정보 조회

        Args:
            base_date (str): 기준일자 (YYYYMMDD)

        Returns:
            KrxHttpResponse[BondKoreaTreasuryBondMarket]: 국채전문유통시장 일별매매정보 응답
        """,
        )

        self.get_general_bond_market = KrxApiMethodFactory.create_single_param_method(
            client=self.client,
            path_template=self.path,
            endpoint="bnd_bydd_trd.json",
            response_model=BondGeneralBondMarket,
            docstring="""일반채권시장 일별매매정보 조회

        Args:
            base_date (str): 기준일자 (YYYYMMDD)

        Returns:
            KrxHttpResponse[BondGeneralBondMarket]: 일반채권시장 일별매매정보 응답
        """,
        )

        self.get_small_bond_market = KrxApiMethodFactory.create_single_param_method(
            client=self.client,
            path_template=self.path,
            endpoint="smb_bydd_trd.json",
            response_model=BondSmallBondMarket,
            docstring="""소액채권시장 일별매매정보 조회

        Args:
            base_date (str): 기준일자 (YYYYMMDD)

        Returns:
            KrxHttpResponse[BondSmallBondMarket]: 소액채권시장 일별매매정보 응답
        """,
        )
