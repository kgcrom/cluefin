from pydantic import BaseModel, Field

from cluefin_openapi.krx._model import KrxHttpBody


class BondKoreaTreasuryBondMarketItem(BaseModel):
    base_date: str = Field(description="기준일자", alias="BAS_DD")
    market_name: str = Field(description="시장구분", alias="MKT_NM")
    issued_code: str = Field(description="종목코드", alias="ISU_CD")
    issued_name: str = Field(description="종목명", alias="ISU_NM")
    term_to_maturity: str = Field(description="만기년수", alias="BND_EXP_TP_NM")
    issued_code_type: str = Field(description="종목구분", alias="GOVBND_ISU_TP_NM")
    close_price: str = Field(description="종가_가격", alias="CLSPRC")
    close_price_prev: str = Field(description="종가_대비", alias="CMPPREVDD_PRC")
    close_price_yield: str = Field(description="종가_수익률", alias="CLSPRC_YD")
    open_price: str = Field(description="시가_가격", alias="OPNPRC")
    open_price_yield: str = Field(description="시가_수익률", alias="OPNPRC_YD")
    high_price: str = Field(description="고가_가격", alias="HGPRC")
    high_price_yield: str = Field(description="고가_수익률", alias="HGPRC_YD")
    low_price: str = Field(description="저가_가격", alias="LWPRC")
    low_price_yield: str = Field(description="저가_수익률", alias="LWPRC_YD")
    trading_volume: str = Field(description="거래량", alias="ACC_TRDVOL")
    trading_value: str = Field(description="거래대금", alias="ACC_TRDVAL")


class BondKoreaTreasuryBondMarket(BaseModel, KrxHttpBody):
    """국채전문유통시장 일별매매정보"""

    data: list[BondKoreaTreasuryBondMarketItem] = Field(
        description="국채전문유통시장 일별매매정보 목록", alias="OutBlock_1"
    )


class BondGeneralBondMarketItem(BaseModel):
    base_date: str = Field(description="기준일자", alias="BAS_DD")
    market_name: str = Field(description="시장구분", alias="MKT_NM")
    issued_code: str = Field(description="종목코드", alias="ISU_CD")
    issued_name: str = Field(description="종목명", alias="ISU_NM")
    close_price: str = Field(description="종가_가격", alias="CLSPRC")
    prev_close_price: str = Field(description="종가_대비", alias="CMPPREVDD_PRC")
    close_price_yield: str = Field(description="종가_수익률", alias="CLSPRC_YD")
    open_price: str = Field(description="시가_가격", alias="OPNPRC")
    open_price_yield: str = Field(description="시가_수익률", alias="OPNPRC_YD")
    high_price: str = Field(description="고가_가격", alias="HGPRC")
    high_price_yield: str = Field(description="고가_수익률", alias="HGPRC_YD")
    low_price: str = Field(description="저가_가격", alias="LWPRC")
    low_price_yield: str = Field(description="저가_수익률", alias="LWPRC_YD")
    trading_volume: str = Field(description="거래량", alias="ACC_TRDVOL")
    trading_value: str = Field(description="거래대금", alias="ACC_TRDVAL")


class BondGeneralBondMarket(BaseModel, KrxHttpBody):
    """일반채권시장 일별매매정보"""

    data: list[BondGeneralBondMarketItem] = Field(description="일반채권시장 일별매매정보 목록", alias="OutBlock_1")


class BondSmallBondMarketItem(BaseModel):
    base_date: str = Field(description="기준일자", alias="BAS_DD")
    market_name: str = Field(description="시장구분", alias="MKT_NM")
    issued_code: str = Field(description="종목코드", alias="ISU_CD")
    issued_name: str = Field(description="종목명", alias="ISU_NM")
    close_price: str = Field(description="종가_가격", alias="CLSPRC")
    prev_close_price: str = Field(description="종가_대비", alias="CMPPREVDD_PRC")
    close_price_yield: str = Field(description="종가_수익률", alias="CLSPRC_YD")
    open_price: str = Field(description="시가_가격", alias="OPNPRC")
    open_price_yield: str = Field(description="시가_수익률", alias="OPNPRC_YD")
    high_price: str = Field(description="고가_가격", alias="HGPRC")
    high_price_yield: str = Field(description="고가_수익률", alias="HGPRC_YD")
    low_price: str = Field(description="저가_가격", alias="LWPRC")
    low_price_yield: str = Field(description="저가_수익률", alias="LWPRC_YD")
    trading_volume: str = Field(description="거래량", alias="ACC_TRDVOL")
    trading_value: str = Field(description="거래대금", alias="ACC_TRDVAL")


class BondSmallBondMarket(BaseModel, KrxHttpBody):
    """소액채권시장 일별매매정보 조회"""

    data: list[BondSmallBondMarketItem] = Field(description="소액채권시장 일별매매정보 목록", alias="OutBlock_1")
