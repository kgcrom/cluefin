from pydantic import BaseModel, Field

from cluefin_openapi.krx._model import KrxHttpBody


class GeneralProductOilMarketItem(BaseModel):
    base_date: str = Field(description="기준일자 (YYYYMMDD)", alias="BAS_DD")
    oil_name: str = Field(description="유종구분", alias="OIL_NM")
    weighted_avg_price_competitive: str = Field(description="가중평균가격_경쟁", alias="WT_AVG_PRC")
    weighted_avg_price_agreed: str = Field(description="가중평균가격_협의", alias="WT_DIS_AVG_PRC")
    trading_volume: str = Field(description="거래량", alias="ACC_TRDVOL")
    trading_value: str = Field(description="거래대금", alias="ACC_TRDVAL")


class GeneralProductOilMarket(BaseModel, KrxHttpBody):
    """석유시장 일별매매정보 응답"""

    data: list[GeneralProductOilMarketItem] = Field(description="석유시장 일별매매정보", alias="OutBlock_1")


class GeneralProductGoldMarketItem(BaseModel):
    base_date: str = Field(description="기준일자 (YYYYMMDD)", alias="BAS_DD")
    issued_code: str = Field(description="종목코드", alias="ISU_CD")
    issued_name: str = Field(description="종목명", alias="ISU_NM")
    close_price: str = Field(description="종가", alias="TDD_CLSPRC")
    prev_close_price: str = Field(description="대비", alias="CMPPREVDD_PRC")
    fluctuation_rate: str = Field(description="등락률", alias="FLUC_RT")
    open_price: str = Field(description="시가", alias="TDD_OPNPRC")
    high_price: str = Field(description="고가", alias="TDD_HGPRC")
    low_price: str = Field(description="저가", alias="TDD_LWPRC")
    trading_volume: str = Field(description="거래량", alias="ACC_TRDVOL")
    trading_value: str = Field(description="거래대금", alias="ACC_TRDVAL")


class GeneralProductGoldMarket(BaseModel, KrxHttpBody):
    """금시장 일별매매정보 응답"""

    data: list[GeneralProductGoldMarketItem] = Field(description="금시장 일별매매정보", alias="OutBlock_1")


class GeneralProductEmissionsMarketItem(BaseModel):
    base_date: str = Field(description="기준일자 (YYYYMMDD)", alias="BAS_DD")
    issued_code: str = Field(description="종목코드", alias="ISU_CD")
    issued_name: str = Field(description="종목명", alias="ISU_NM")
    close_price: str = Field(description="종가", alias="TDD_CLSPRC")
    prev_close_price: str = Field(description="대비", alias="CMPPREVDD_PRC")
    fluctuation_rate: str = Field(description="등락률", alias="FLUC_RT")
    open_price: str = Field(description="시가", alias="TDD_OPNPRC")
    high_price: str = Field(description="고가", alias="TDD_HGPRC")
    low_price: str = Field(description="저가", alias="TDD_LWPRC")
    trading_volume: str = Field(description="거래량", alias="ACC_TRDVOL")
    trading_value: str = Field(description="거래대금", alias="ACC_TRDVAL")


class GeneralProductEmissionsMarket(BaseModel, KrxHttpBody):
    """탄소 배출권시장 일별매매정보 응답"""

    data: list[GeneralProductEmissionsMarketItem] = Field(
        description="탄소 배출권시장 일별매매정보", alias="OutBlock_1"
    )
