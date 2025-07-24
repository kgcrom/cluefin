from pydantic import BaseModel, Field

from cluefin_openapi.krx._model import KrxHttpBody


class DerivativesTradingOfFuturesExcludeStockItem(BaseModel):
    base_date: str = Field(description="기준일자", alias="BAS_DD")
    product_name: str = Field(description="상품구분", alias="PROD_NM")
    market_name: str = Field(description="시장구분(정규/야간)", alias="MKT_NM")
    issued_code: str = Field(description="종목코드", alias="ISU_CD")
    issued_name: str = Field(description="종목명", alias="ISU_NM")
    close_price: str = Field(description="종가", alias="TDD_CLSPRC")
    prev_close_price: str = Field(description="대비", alias="CMPPREVDD_PRC")
    open_price: str = Field(description="시가", alias="TDD_OPNPRC")
    high_price: str = Field(description="고가", alias="TDD_HGPRC")
    low_price: str = Field(description="저가", alias="TDD_LWPRC")
    spot_price: str = Field(description="현물가", alias="SPOT_PRC")
    settlement_price: str = Field(description="정산가", alias="SETL_PRC")
    trading_volume: str = Field(description="거래량", alias="ACC_TRDVOL")
    trading_value: str = Field(description="거래대금", alias="ACC_TRDVAL")
    open_interest: str = Field(description="미결제약정", alias="ACC_OPNINT_QTY")


class DerivativesTradingOfFuturesExcludeStock(BaseModel, KrxHttpBody):
    """선물 일별매매정보 (주식선물外)"""

    data: list[DerivativesTradingOfFuturesExcludeStockItem] = Field(description="주식선물 거래정보", alias="OutBlock_1")


class DerivativesTradingOfKospiFuturesItem(BaseModel):
    base_date: str = Field(description="기준일자", alias="BAS_DD")
    product_name: str = Field(description="상품구분", alias="PROD_NM")
    market_name: str = Field(description="시장구분(정규/야간)", alias="MKT_NM")
    issued_code: str = Field(description="종목코드", alias="ISU_CD")
    issued_name: str = Field(description="종목명", alias="ISU_NM")
    close_price: str = Field(description="종가", alias="TDD_CLSPRC")
    prev_close_price: str = Field(description="대비", alias="CMPPREVDD_PRC")
    open_price: str = Field(description="시가", alias="TDD_OPNPRC")
    high_price: str = Field(description="고가", alias="TDD_HGPRC")
    low_price: str = Field(description="저가", alias="TDD_LWPRC")
    spot_price: str = Field(description="현물가", alias="SPOT_PRC")
    settlement_price: str = Field(description="정산가", alias="SETL_PRC")
    trading_volume: str = Field(description="거래량", alias="ACC_TRDVOL")
    trading_value: str = Field(description="거래대금", alias="ACC_TRDVAL")
    open_interest: str = Field(description="미결제약정", alias="ACC_OPNINT_QTY")


class DerivativesTradingOfKospiFutures(BaseModel, KrxHttpBody):
    """주식선물(코스피) 거래정보"""

    data: list[DerivativesTradingOfKospiFuturesItem] = Field(
        description="주식선물(코스피) 거래정보", alias="OutBlock_1"
    )


class DerivativesTradingOfKosdaqFuturesItem(BaseModel):
    base_date: str = Field(description="기준일자", alias="BAS_DD")
    product_name: str = Field(description="상품구분", alias="PROD_NM")
    market_name: str = Field(description="시장구분(정규/야간)", alias="MKT_NM")
    issued_code: str = Field(description="종목코드", alias="ISU_CD")
    issued_name: str = Field(description="종목명", alias="ISU_NM")
    close_price: str = Field(description="종가", alias="TDD_CLSPRC")
    prev_close_price: str = Field(description="대비", alias="CMPPREVDD_PRC")
    open_price: str = Field(description="시가", alias="TDD_OPNPRC")
    high_price: str = Field(description="고가", alias="TDD_HGPRC")
    low_price: str = Field(description="저가", alias="TDD_LWPRC")
    spot_price: str = Field(description="현물가", alias="SPOT_PRC")
    settlement_price: str = Field(description="정산가", alias="SETL_PRC")
    trading_volume: str = Field(description="거래량", alias="ACC_TRDVOL")
    trading_value: str = Field(description="거래대금", alias="ACC_TRDVAL")
    open_interest: str = Field(description="미결제약정", alias="ACC_OPNINT_QTY")


class DerivativesTradingOfKosdaqFutures(BaseModel, KrxHttpBody):
    """주식선물(코스닥) 거래정보"""

    data: list[DerivativesTradingOfKosdaqFuturesItem] = Field(
        description="주식선물(코스닥) 거래정보", alias="OutBlock_1"
    )


class DerivativesTradingOfOptionExcludeStockItem(BaseModel):
    base_date: str = Field(description="기준일자", alias="BAS_DD")
    product_name: str = Field(description="상품구분", alias="PROD_NM")
    right_type_name: str = Field(description="권리유형(CALL/PUT)", alias="RGHT_TP_NM")
    issued_code: str = Field(description="종목코드", alias="ISU_CD")
    issued_name: str = Field(description="종목명", alias="ISU_NM")
    close_price: str = Field(description="종가", alias="TDD_CLSPRC")
    prev_close_price: str = Field(description="대비", alias="CMPPREVDD_PRC")
    open_price: str = Field(description="시가", alias="TDD_OPNPRC")
    high_price: str = Field(description="고가", alias="TDD_HGPRC")
    low_price: str = Field(description="저가", alias="TDD_LWPRC")
    implied_volatility: str = Field(description="내재변동성", alias="IMP_VOLT")
    next_day_settlement_price: str = Field(description="익일정산가", alias="NXTDD_BAS_PRC")
    trading_volume: str = Field(description="거래량", alias="ACC_TRDVOL")
    trading_value: str = Field(description="거래대금", alias="ACC_TRDVAL")
    open_interest: str = Field(description="미결제약정", alias="ACC_OPNINT_QTY")


class DerivativesTradingOfOptionExcludeStock(BaseModel, KrxHttpBody):
    """주식옵션 거래정보"""

    data: list[DerivativesTradingOfOptionExcludeStockItem] = Field(description="주식옵션 거래정보", alias="OutBlock_1")


class DerivativesTradingOfKospiOptionItem(BaseModel):
    base_date: str = Field(description="기준일자", alias="BAS_DD")
    product_name: str = Field(description="상품구분", alias="PROD_NM")
    right_type_name: str = Field(description="권리유형(CALL/PUT)", alias="RGHT_TP_NM")
    issued_code: str = Field(description="종목코드", alias="ISU_CD")
    issued_name: str = Field(description="종목명", alias="ISU_NM")
    close_price: str = Field(description="종가", alias="TDD_CLSPRC")
    prev_close_price: str = Field(description="대비", alias="CMPPREVDD_PRC")
    open_price: str = Field(description="시가", alias="TDD_OPNPRC")
    high_price: str = Field(description="고가", alias="TDD_HGPRC")
    low_price: str = Field(description="저가", alias="TDD_LWPRC")
    implied_volatility: str = Field(description="내재변동성", alias="IMP_VOLT")
    next_day_settlement_price: str = Field(description="익일정산가", alias="NXTDD_BAS_PRC")
    trading_volume: str = Field(description="거래량", alias="ACC_TRDVOL")
    trading_value: str = Field(description="거래대금", alias="ACC_TRDVAL")
    open_interest: str = Field(description="미결제약정", alias="ACC_OPNINT_QTY")


class DerivativesTradingOfKospiOption(BaseModel, KrxHttpBody):
    """주식옵션(코스피) 거래정보"""

    data: list[DerivativesTradingOfKospiOptionItem] = Field(description="주식옵션 거래정보", alias="OutBlock_1")


class DerivativesTradingOfKosdaqOptionItem(BaseModel):
    base_date: str = Field(description="기준일자", alias="BAS_DD")
    product_name: str = Field(description="상품구분", alias="PROD_NM")
    right_type_name: str = Field(description="권리유형(CALL/PUT)", alias="RGHT_TP_NM")
    issued_code: str = Field(description="종목코드", alias="ISU_CD")
    issued_name: str = Field(description="종목명", alias="ISU_NM")
    close_price: str = Field(description="종가", alias="TDD_CLSPRC")
    prev_close_price: str = Field(description="대비", alias="CMPPREVDD_PRC")
    open_price: str = Field(description="시가", alias="TDD_OPNPRC")
    high_price: str = Field(description="고가", alias="TDD_HGPRC")
    low_price: str = Field(description="저가", alias="TDD_LWPRC")
    implied_volatility: str = Field(description="내재변동성", alias="IMP_VOLT")
    next_day_settlement_price: str = Field(description="익일정산가", alias="NXTDD_BAS_PRC")
    trading_volume: str = Field(description="거래량", alias="ACC_TRDVOL")
    trading_value: str = Field(description="거래대금", alias="ACC_TRDVAL")
    open_interest: str = Field(description="미결제약정", alias="ACC_OPNINT_QTY")


class DerivativesTradingOfKosdaqOption(BaseModel, KrxHttpBody):
    """주식옵션(코스닥) 거래정보"""

    data: list[DerivativesTradingOfKosdaqOptionItem] = Field(
        description="주식옵션(코스닥) 거래정보", alias="OutBlock_1"
    )
