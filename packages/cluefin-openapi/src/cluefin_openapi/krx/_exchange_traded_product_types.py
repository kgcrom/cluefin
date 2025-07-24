from pydantic import BaseModel, Field

from cluefin_openapi.krx._model import KrxHttpBody


class ExchangeTradedETFItem(BaseModel):
    base_date: str = Field(description="기준일자", alias="BAS_DD")
    issued_code: str = Field(description="종목코드", alias="ISU_CD")
    issued_name: str = Field(description="종목명", alias="ISU_NM")
    close_price: str = Field(description="종가", alias="TDD_CLSPRC")
    prev_close_price: str = Field(description="대비", alias="CMPPREVDD_PRC")
    fluctuation_rate: str = Field(description="등락률", alias="FLUC_RT")
    net_asset_value: str = Field(description="순자산가치(NAV)", alias="NAV")
    open_price: str = Field(description="시가", alias="TDD_OPNPRC")
    high_price: str = Field(description="고가", alias="TDD_HGPRC")
    low_price: str = Field(description="저가", alias="TDD_LWPRC")
    trading_volume: str = Field(description="거래량", alias="ACC_TRDVOL")
    trading_value: str = Field(description="거래대금", alias="ACC_TRDVAL")
    market_cap: str = Field(description="시가총액", alias="MKTCAP")
    net_asset_total_amount: str = Field(description="순자산총액", alias="INVSTASST_NETASST_TOTAMT")
    listed_shares: str = Field(description="상장증권수", alias="LIST_SHRS")
    index_name: str = Field(description="기초지수_지수명", alias="IDX_IND_NM")
    index_close_price: str = Field(description="기초지수_종가", alias="OBJ_STKPRC_IDX")
    index_prev_close_price: str = Field(description="기초지수_대비", alias="CMPPREVDD_IDX")
    index_fluctuation_rate: str = Field(description="기초지수_등락률", alias="FLUC_RT_IDX")


class ExchangeTradedETF(BaseModel, KrxHttpBody):
    """ETF 일별매매정보 응답"""

    data: list[ExchangeTradedETFItem] = Field(
        default_factory=list, description="ETF 일별매매정보 목록", alias="OutBlock_1"
    )


class ExchangeTradedETNItem(BaseModel):
    base_date: str = Field(description="기준일자", alias="BAS_DD")
    issued_code: str = Field(description="종목코드", alias="ISU_CD")
    issued_name: str = Field(description="종목명", alias="ISU_NM")
    close_price: str = Field(description="종가", alias="TDD_CLSPRC")
    prev_close_price: str = Field(description="대비", alias="CMPPREVDD_PRC")
    fluctuation_rate: str = Field(description="등락률", alias="FLUC_RT")
    indicative_value: str = Field(description="지표가치(IV)", alias="PER1SECU_INDIC_VAL")
    open_price: str = Field(description="시가", alias="TDD_OPNPRC")
    high_price: str = Field(description="고가", alias="TDD_HGPRC")
    low_price: str = Field(description="저가", alias="TDD_LWPRC")
    trading_volume: str = Field(description="거래량", alias="ACC_TRDVOL")
    trading_value: str = Field(description="거래대금", alias="ACC_TRDVAL")
    market_cap: str = Field(description="시가총액", alias="MKTCAP")
    indicative_value_total_amount: str = Field(description="지표가치총액", alias="INDIC_VAL_AMT")
    listed_shares: str = Field(description="상장증권수", alias="LIST_SHRS")
    index_name: str = Field(description="기초지수_지수명", alias="IDX_IND_NM")
    index_close_price: str = Field(description="기초지수_종가", alias="OBJ_STKPRC_IDX")
    index_prev_close_price: str = Field(description="기초지수_대비", alias="CMPPREVDD_IDX")
    index_fluctuation_rate: str = Field(description="기초지수_등락률", alias="FLUC_RT_IDX")


class ExchangeTradedETN(BaseModel, KrxHttpBody):
    """ETN 일별매매정보 응답"""

    data: list[ExchangeTradedETNItem] = Field(
        default_factory=list, description="ETN 일별매매정보 목록", alias="OutBlock_1"
    )


class ExchangeTradedELWItem(BaseModel):
    base_date: str = Field(description="기준일자", alias="BAS_DD")
    issued_code: str = Field(description="종목코드", alias="ISU_CD")
    issued_name: str = Field(description="종목명", alias="ISU_NM")
    close_price: str = Field(description="종가", alias="TDD_CLSPRC")
    prev_close_price: str = Field(description="대비", alias="CMPPREVDD_PRC")
    open_price: str = Field(description="시가", alias="TDD_OPNPRC")
    high_price: str = Field(description="고가", alias="TDD_HGPRC")
    low_price: str = Field(description="저가", alias="TDD_LWPRC")
    trading_volume: str = Field(description="거래량", alias="ACC_TRDVOL")
    trading_value: str = Field(description="거래대금", alias="ACC_TRDVAL")
    market_cap: str = Field(description="시가총액", alias="MKTCAP")
    listed_shares: str = Field(description="상장증권수", alias="LIST_SHRS")
    underlying_asset_name: str = Field(description="기초자산_자산명", alias="ULY_NM")
    underlying_asset_price: str = Field(description="기초자산_종가", alias="ULY_PRC")
    underlying_asset_prev_close_price: str = Field(description="기초자산_대비", alias="CMPPREVDD_PRC_ULY")
    underlying_asset_fluctuation_rate: str = Field(description="기초자산_등락률", alias="FLUC_RT_ULY")


class ExchangeTradedELW(BaseModel, KrxHttpBody):
    """ELW 일별매매정보 응답"""

    data: list[ExchangeTradedELWItem] = Field(
        default_factory=list, description="ELW 일별매매정보 목록", alias="OutBlock_1"
    )
