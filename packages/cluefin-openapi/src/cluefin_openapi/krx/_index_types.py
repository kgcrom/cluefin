from pydantic import BaseModel, Field

from cluefin_openapi.krx._model import KrxHttpBody


class IndexKrxItem(BaseModel):
    """KRX 지수 일별 시세 정보"""

    base_date: str = Field(description="기준일자 (YYYYMMDD 형식)", alias="BAS_DD")
    index_class: str = Field(description="계열 구분", alias="IDX_CLSS")
    index_name: str = Field(description="지수명", alias="IDX_NM")
    close_price_index: str = Field(description="종가", alias="CLSPRC_IDX")
    compare_prev_date_index: str = Field(description="전일 대비", alias="CMPPREVDD_IDX")
    fluctuation_rate: str = Field(description="등락률", alias="FLUC_RT")
    open_price_index: str = Field(description="시가", alias="OPNPRC_IDX")
    high_price_index: str = Field(description="고가", alias="HGPRC_IDX")
    low_price_index: str = Field(description="저가", alias="LWPRC_IDX")
    accumulated_trading_volume: str = Field(description="거래량", alias="ACC_TRDVOL")
    accumulated_trading_value: str = Field(description="거래대금", alias="ACC_TRDVAL")
    market_cap: str = Field(description="상장시가총액", alias="MKTCAP")


class IndexKrx(BaseModel, KrxHttpBody):
    """KRX 시리즈 지수의 시세정보 제공 응답"""

    data: list[IndexKrxItem] = Field(default_factory=list, description="KRX 지수의 시세정보 목록", alias="OutBlock_1")


class IndexKospiItem(BaseModel):
    """KOSPI 지수 일별 시세 정보"""

    base_date: str = Field(description="기준일자 (YYYYMMDD 형식)", alias="BAS_DD")
    index_class: str = Field(description="계열 구분", alias="IDX_CLSS")
    index_name: str = Field(description="지수명", alias="IDX_NM")
    close_price_index: str = Field(description="종가", alias="CLSPRC_IDX")
    compare_prev_date_index: str = Field(description="전일 대비", alias="CMPPREVDD_IDX")
    fluctuation_rate: str = Field(description="등락률", alias="FLUC_RT")
    open_price_index: str = Field(description="시가", alias="OPNPRC_IDX")
    high_price_index: str = Field(description="고가", alias="HGPRC_IDX")
    low_price_index: str = Field(description="저가", alias="LWPRC_IDX")
    accumulated_trading_volume: str = Field(description="거래량", alias="ACC_TRDVOL")
    accumulated_trading_value: str = Field(description="거래대금", alias="ACC_TRDVAL")
    market_cap: str = Field(description="상장시가총액", alias="MKTCAP")


class IndexKospi(BaseModel, KrxHttpBody):
    """KOSPI 시리즈 지수의 시세정보 제공 응답"""

    data: list[IndexKrxItem] = Field(default_factory=list, description="KOSPI 지수의 시세정보 목록", alias="OutBlock_1")


class IndexKosdaqItem(BaseModel):
    """KOSDAQ 지수 일별 시세 정보"""

    base_date: str = Field(description="기준일자 (YYYYMMDD 형식)", alias="BAS_DD")
    index_class: str = Field(description="계열 구분", alias="IDX_CLSS")
    index_name: str = Field(description="지수명", alias="IDX_NM")
    close_price_index: str = Field(description="종가", alias="CLSPRC_IDX")
    compare_prev_date_index: str = Field(description="전일 대비", alias="CMPPREVDD_IDX")
    fluctuation_rate: str = Field(description="등락률", alias="FLUC_RT")
    open_price_index: str = Field(description="시가", alias="OPNPRC_IDX")
    high_price_index: str = Field(description="고가", alias="HGPRC_IDX")
    low_price_index: str = Field(description="저가", alias="LWPRC_IDX")
    accumulated_trading_volume: str = Field(description="거래량", alias="ACC_TRDVOL")
    accumulated_trading_value: str = Field(description="거래대금", alias="ACC_TRDVAL")
    market_cap: str = Field(description="상장시가총액", alias="MKTCAP")


class IndexKosdaq(BaseModel, KrxHttpBody):
    """KOSDAQ 시리즈 지수의 시세정보 제공 응답"""

    data: list[IndexKosdaqItem] = Field(
        default_factory=list, description="KOSDAQ 지수의 시세정보 목록", alias="OutBlock_1"
    )


class IndexBondItem(BaseModel):
    """채권 지수 일별 시세 정보"""

    base_date: str = Field(description="기준일자 (YYYYMMDD 형식)", alias="BAS_DD")
    index_name: str = Field(description="지수명", alias="BND_IDX_GRP_NM")
    total_earning_index: str = Field(description="총수익지수 종가", alias="TOT_EARNG_IDX")
    total_earning_index_compare_prev_date: str = Field(description="총수익지수 대비", alias="TOT_EARNG_IDX_CMPPREVDD")
    net_price_index: str = Field(description="순가격지수 종가", alias="NETPRC_IDX")
    net_price_index_compare_prev_date: str = Field(description="순가격지수 대비", alias="NETPRC_IDX_CMPPREVDD")
    zero_reinvest_index: str = Field(description="제로재투자지수 종가", alias="ZERO_REINVST_IDX")
    zero_reinvest_index_compare_prev_date: str = Field(
        description="제로재투자지수 대비", alias="ZERO_REINVST_IDX_CMPPREVDD"
    )
    call_reinvest_index: str = Field(description="콜재투자지수 종가", alias="CALL_REINVST_IDX")
    call_reinvest_index_compare_prev_date: str = Field(
        description="콜재투자지수 대비", alias="CALL_REINVST_IDX_CMPPREVDD"
    )
    market_price_index: str = Field(description="시장가격지수 종가", alias="MKT_PRC_IDX")
    market_price_index_compare_prev_date: str = Field(description="시장가격지수 대비", alias="MKT_PRC_IDX_CMPPREVDD")
    average_duration: str = Field(description="듀레이션", alias="AVG_DURATION")
    average_convexity_price: str = Field(description="컨벡시티", alias="AVG_CONVEXITY_PRC")
    ytm: str = Field(description="YTM", alias="BND_IDX_AVG_YD")


class IndexBond(BaseModel, KrxHttpBody):
    """채권 시리즈 지수의 시세정보 제공 응답"""

    data: list[IndexBondItem] = Field(default_factory=list, description="채권 지수의 시세정보 목록", alias="OutBlock_1")


class IndexDerivativesItem(BaseModel):
    """파생상품 지수 일별 시세 정보"""

    base_date: str = Field(description="기준일자 (YYYYMMDD 형식)", alias="BAS_DD")
    index_class: str = Field(description="계열 구분", alias="IDX_CLSS")
    index_name: str = Field(description="지수명", alias="IDX_NM")
    close_price_index: str = Field(description="종가", alias="CLSPRC_IDX")
    compare_prev_date_index: str = Field(description="전일 대비", alias="CMPPREVDD_IDX")
    fluctuation_rate: str = Field(description="등락률", alias="FLUC_RT")
    open_price_index: str = Field(description="시가", alias="OPNPRC_IDX")
    high_price_index: str = Field(description="고가", alias="HGPRC_IDX")
    low_price_index: str = Field(description="저가", alias="LWPRC_IDX")


class IndexDerivatives(BaseModel, KrxHttpBody):
    """파생상품 지수 일별 시세 정보 응답"""

    data: list[IndexDerivativesItem] = Field(
        default_factory=list, description="파생상품 지수의 시세정보 목록", alias="OutBlock_1"
    )
