from pydantic import BaseModel, Field

from cluefin_openapi.krx._model import KrxHttpBody


class StockKospiItem(BaseModel):
    base_date: str = Field(description="기준일자 (YYYYMMDD 형식)", alias="BAS_DD")
    issued_code: str = Field(description="종목코드", alias="ISU_CD")
    issued_name: str = Field(description="종목명", alias="ISU_NM")
    market_name: str = Field(description="시장구분", alias="MKT_NM")
    sector_type_name: str = Field(description="소속부", alias="SECT_TP_NM")
    close_price: str = Field(description="종가", alias="TDD_CLSPRC")
    compare_prev_day_price: str = Field(description="대비", alias="CMPPREVDD_PRC")
    fluctuation_rate: str = Field(description="등락률", alias="FLUC_RT")
    open_price: str = Field(description="시가", alias="TDD_OPNPRC")
    high_price: str = Field(description="고가", alias="TDD_HGPRC")
    low_price: str = Field(description="저가", alias="TDD_LWPRC")
    accumulated_trading_volume: str = Field(description="거래량", alias="ACC_TRDVOL")
    accumulated_trading_value: str = Field(description="거래대금", alias="ACC_TRDVAL")
    market_cap: str = Field(description="시가총액", alias="MKTCAP")
    listed_shares: str = Field(description="상장주식수", alias="LIST_SHRS")


class StockKospi(BaseModel, KrxHttpBody):
    """KOSPI 일별매매정보 응답"""

    data: list[StockKospiItem] = Field(default_factory=list, description="KOSPI 일별매매정보 목록", alias="OutBlock_1")


class StockKosdaqItem(BaseModel):
    base_date: str = Field(description="기준일자 (YYYYMMDD 형식)", alias="BAS_DD")
    issued_code: str = Field(description="종목코드", alias="ISU_CD")
    issued_name: str = Field(description="종목명", alias="ISU_NM")
    market_name: str = Field(description="시장구분", alias="MKT_NM")
    sector_type_name: str = Field(description="소속부", alias="SECT_TP_NM")
    close_price: str = Field(description="종가", alias="TDD_CLSPRC")
    compare_prev_day_price: str = Field(description="대비", alias="CMPPREVDD_PRC")
    fluctuation_rate: str = Field(description="등락률", alias="FLUC_RT")
    open_price: str = Field(description="시가", alias="TDD_OPNPRC")
    high_price: str = Field(description="고가", alias="TDD_HGPRC")
    low_price: str = Field(description="저가", alias="TDD_LWPRC")
    accumulated_trading_volume: str = Field(description="거래량", alias="ACC_TRDVOL")
    accumulated_trading_value: str = Field(description="거래대금", alias="ACC_TRDVAL")
    market_cap: str = Field(description="시가총액", alias="MKTCAP")
    listed_shares: str = Field(description="상장주식수", alias="LIST_SHRS")


class StockKosdaq(BaseModel, KrxHttpBody):
    """KOSDAQ 일별매매정보 응답"""

    data: list[StockKosdaqItem] = Field(
        default_factory=list, description="KOSDAQ 일별매매정보 목록", alias="OutBlock_1"
    )


class StockKonexItem(BaseModel):
    base_date: str = Field(description="기준일자 (YYYYMMDD 형식)", alias="BAS_DD")
    issued_code: str = Field(description="종목코드", alias="ISU_CD")
    issued_name: str = Field(description="종목명", alias="ISU_NM")
    market_name: str = Field(description="시장구분", alias="MKT_NM")
    sector_type_name: str = Field(description="소속부", alias="SECT_TP_NM")
    close_price: str = Field(description="종가", alias="TDD_CLSPRC")
    compare_prev_day_price: str = Field(description="대비", alias="CMPPREVDD_PRC")
    fluctuation_rate: str = Field(description="등락률", alias="FLUC_RT")
    open_price: str = Field(description="시가", alias="TDD_OPNPRC")
    high_price: str = Field(description="고가", alias="TDD_HGPRC")
    low_price: str = Field(description="저가", alias="TDD_LWPRC")
    accumulated_trading_volume: str = Field(description="거래량", alias="ACC_TRDVOL")
    accumulated_trading_value: str = Field(description="거래대금", alias="ACC_TRDVAL")
    market_cap: str = Field(description="시가총액", alias="MKTCAP")
    listed_shares: str = Field(description="상장주식수", alias="LIST_SHRS")


class StockKonex(BaseModel, KrxHttpBody):
    """KONEX 일별매매정보 응답"""

    data: list[StockKonexItem] = Field(default_factory=list, description="KONEX 일별매매정보 목록", alias="OutBlock_1")


class StockWarrantItem(BaseModel):
    base_date: str = Field(description="기준일자 (YYYYMMDD 형식)", alias="BAS_DD")
    market_name: str = Field(description="시장구분", alias="MKT_NM")
    issued_code: str = Field(description="종목코드", alias="ISU_CD")
    issued_name: str = Field(description="종목명", alias="ISU_NM")
    close_price: str = Field(description="종가", alias="TDD_CLSPRC")
    compare_prev_day_price: str = Field(description="대비", alias="CMPPREVDD_PRC")
    fluctuation_rate: str = Field(description="등락률", alias="FLUC_RT")
    open_price: str = Field(description="시가", alias="TDD_OPNPRC")
    high_price: str = Field(description="고가", alias="TDD_HGPRC")
    low_price: str = Field(description="저가", alias="TDD_LWPRC")
    accumulated_trading_volume: str = Field(description="거래량", alias="ACC_TRDVOL")
    accumulated_trading_value: str = Field(description="거래대금", alias="ACC_TRDVAL")
    market_cap: str = Field(description="시가총액", alias="MKTCAP")
    listed_shares: str = Field(description="상장증권수", alias="LIST_SHRS")
    exercise_price: str = Field(description="행사가격", alias="EXER_PRC")
    exercise_start_date: str = Field(description="존속기간 시작일", alias="EXST_STRT_DD")
    exercise_end_date: str = Field(description="존속기간 종료일", alias="EXST_END_DD")
    target_stock_code: str = Field(description="목적주권 종목코드", alias="TARSTK_ISU_SRT_CD")
    target_stock_name: str = Field(description="목적주권 종목명", alias="TARSTK_ISU_NM")
    target_stock_present_price: str = Field(description="목적주권 종가", alias="TARSTK_ISU_PRSNT_PRC")


class StockWarrant(BaseModel, KrxHttpBody):
    """신주인수권증권 일별매매정보 응답"""

    data: list[StockWarrantItem] = Field(
        default_factory=list, description="신주인수권증권 일별매매정보 목록", alias="OutBlock_1"
    )


class StockSubscriptionWarrantItem(BaseModel):
    base_date: str = Field(description="기준일자 (YYYYMMDD 형식)", alias="BAS_DD")
    market_name: str = Field(description="시장구분", alias="MKT_NM")
    issued_code: str = Field(description="종목코드", alias="ISU_CD")
    issued_name: str = Field(description="종목명", alias="ISU_NM")
    close_price: str = Field(description="종가", alias="TDD_CLSPRC")
    compare_prev_day_price: str = Field(description="대비", alias="CMPPREVDD_PRC")
    fluctuation_rate: str = Field(description="등락률", alias="FLUC_RT")
    open_price: str = Field(description="시가", alias="TDD_OPNPRC")
    high_price: str = Field(description="고가", alias="TDD_HGPRC")
    low_price: str = Field(description="저가", alias="TDD_LWPRC")
    accumulated_trading_volume: str = Field(description="거래량", alias="ACC_TRDVOL")
    accumulated_trading_value: str = Field(description="거래대금", alias="ACC_TRDVAL")
    market_cap: str = Field(description="시가총액", alias="MKTCAP")
    listed_shares: str = Field(description="상장증서수", alias="LIST_SHRS")
    issue_price: str = Field(description="신주발행가", alias="ISU_PRC")
    delist_date: str = Field(description="상장폐지일", alias="DELIST_DD")
    target_stock_code: str = Field(description="목적주권 종목코드", alias="TARSTK_ISU_SRT_CD")
    target_stock_name: str = Field(description="목적주권 종목명", alias="TARSTK_ISU_NM")
    target_stock_present_price: str = Field(description="목적주권 종목가", alias="TARSTK_ISU_PRSNT_PRC")


class StockSubscriptionWarrant(BaseModel, KrxHttpBody):
    """신주인수권증서 일별매매정보 응답"""

    data: list[StockSubscriptionWarrantItem] = Field(
        default_factory=list, description="신주인수권증서 일별매매정보 목록", alias="OutBlock_1"
    )


class StockKospiBaseInfoItem(BaseModel):
    issued_code: str = Field(description="표준코드", alias="ISU_CD")
    issued_short_code: str = Field(description="단축코드", alias="ISU_SRT_CD")
    issued_name: str = Field(description="한글 종목명", alias="ISU_NM")
    issued_abbreviation: str = Field(description="한글 종목약명", alias="ISU_ABBRV")
    issued_english_name: str = Field(description="영문 종목명", alias="ISU_ENG_NM")
    listing_date: str = Field(description="상장일", alias="LIST_DD")
    market_type_name: str = Field(description="시장구분", alias="MKT_TP_NM")
    security_group_name: str = Field(description="증권구분", alias="SECUGRP_NM")
    sector_type_name: str = Field(description="소속부", alias="SECT_TP_NM")
    stock_type_name: str = Field(description="주식종류", alias="KIND_STKCERT_TP_NM")
    par_value: str = Field(description="액면가", alias="PARVAL")
    listed_shares: str = Field(description="상장주식수", alias="LIST_SHRS")


class StockKospiBaseInfo(BaseModel, KrxHttpBody):
    """KOSPI 기본 정보 응답"""

    data: list[StockKospiBaseInfoItem] = Field(
        default_factory=list, description="KOSPI 기본 정보 목록", alias="OutBlock_1"
    )


class StockKosdaqBaseInfoItem(BaseModel):
    issued_code: str = Field(description="표준코드", alias="ISU_CD")
    issued_short_code: str = Field(description="단축코드", alias="ISU_SRT_CD")
    issued_name: str = Field(description="한글 종목명", alias="ISU_NM")
    issued_abbreviation: str = Field(description="한글 종목약명", alias="ISU_ABBRV")
    issued_english_name: str = Field(description="영문 종목명", alias="ISU_ENG_NM")
    listing_date: str = Field(description="상장일", alias="LIST_DD")
    market_type_name: str = Field(description="시장구분", alias="MKT_TP_NM")
    security_group_name: str = Field(description="증권구분", alias="SECUGRP_NM")
    sector_type_name: str = Field(description="소속부", alias="SECT_TP_NM")
    stock_type_name: str = Field(description="주식종류", alias="KIND_STKCERT_TP_NM")
    par_value: str = Field(description="액면가", alias="PARVAL")
    listed_shares: str = Field(description="상장주식수", alias="LIST_SHRS")


class StockKosdaqBaseInfo(BaseModel, KrxHttpBody):
    """KOSDAQ 기본 정보 응답"""

    data: list[StockKosdaqBaseInfoItem] = Field(
        default_factory=list, description="KOSDAQ 기본 정보 목록", alias="OutBlock_1"
    )


class StockKonexBaseInfoItem(BaseModel):
    issued_code: str = Field(description="표준코드", alias="ISU_CD")
    issued_short_code: str = Field(description="단축코드", alias="ISU_SRT_CD")
    issued_name: str = Field(description="한글 종목명", alias="ISU_NM")
    issued_abbreviation: str = Field(description="한글 종목약명", alias="ISU_ABBRV")
    issued_english_name: str = Field(description="영문 종목명", alias="ISU_ENG_NM")
    listing_date: str = Field(description="상장일", alias="LIST_DD")
    market_type_name: str = Field(description="시장구분", alias="MKT_TP_NM")
    security_group_name: str = Field(description="증권구분", alias="SECUGRP_NM")
    sector_type_name: str = Field(description="소속부", alias="SECT_TP_NM")
    stock_type_name: str = Field(description="주식종류", alias="KIND_STKCERT_TP_NM")
    par_value: str = Field(description="액면가", alias="PARVAL")
    listed_shares: str = Field(description="상장주식수", alias="LIST_SHRS")


class StockKonexBaseInfo(BaseModel, KrxHttpBody):
    """KONEX 기본 정보 응답"""

    data: list[StockKonexBaseInfoItem] = Field(
        default_factory=list, description="KONEX 기본 정보 목록", alias="OutBlock_1"
    )
