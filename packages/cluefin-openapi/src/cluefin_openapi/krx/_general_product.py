from cluefin_openapi.krx._client import Client
from cluefin_openapi.krx._factory import KrxApiMethodFactory
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

        # 석유시장 일별매매정보 조회
        self.get_oil_market = KrxApiMethodFactory.create_single_param_method(
            client=self.client,
            path_template=self.path,
            endpoint="oil_bydd_trd.json",
            response_model=GeneralProductOilMarket,
            docstring="석유시장 일별매매정보 조회\n\nArgs:\n    base_date (str): 기준일자 (YYYYMMDD)\n\nReturns:\n    KrxHttpResponse[GeneralProductOilMarket]: 석유시장 일별매매정보"
        )

        # 금시장 일별매매정보 조회
        self.get_gold_market = KrxApiMethodFactory.create_single_param_method(
            client=self.client,
            path_template=self.path,
            endpoint="gold_bydd_trd.json",
            response_model=GeneralProductGoldMarket,
            docstring="금시장 일별매매정보 조회\n\nArgs:\n    base_date (str): 기준일자 (YYYYMMDD)\n\nReturns:\n    KrxHttpResponse[GeneralProductGoldMarket]: 금시장 일별매매정보"
        )

        # 탄소 배출권시장 일별매매정보 조회
        self.get_emissions_market = KrxApiMethodFactory.create_single_param_method(
            client=self.client,
            path_template=self.path,
            endpoint="ets_bydd_trd.json",
            response_model=GeneralProductEmissionsMarket,
            docstring="탄소 배출권시장 일별매매정보 조회\n\nArgs:\n    base_date (str): 기준일자 (YYYYMMDD)\n\nReturns:\n    KrxHttpResponse[GeneralProductEmissionsMarket]: 탄소시장 일별매매정보"
        )
