from pydantic import BaseModel, ConfigDict, Field

from cluefin_openapi.nhplug._model import NHPlugMessage


class OverseasStockCurrentPriceItem(BaseModel):
    """해외주식 현재가상세 조회 결과 (`Output_0`)."""

    model_config = ConfigDict(extra="allow")

    iem_cd: str | None = Field(default=None, description="종목코드 / 길이 15")
    kor_name: str | None = Field(default=None, description="종목명 / 길이 40")
    industry_code: str | None = Field(default=None, description="업종코드 / 길이 4")
    industry_name: str | None = Field(default=None, description="업종명 / 길이 100")
    trdprc: float | None = Field(default=None, description="현재가 / 길이 17")
    netchng_cls: str | None = Field(
        default=None,
        description=(
            "전일대비구분 / 길이 1 / 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보함+리버스(기세)"
        ),
    )
    netchng: float | None = Field(default=None, description="전일대비 / 길이 17")
    pctchng: float | None = Field(default=None, description="전일대비율 / 길이 8")
    open_prc: float | None = Field(default=None, description="시가 / 길이 17")
    high: float | None = Field(default=None, description="고가 / 길이 17")
    low: float | None = Field(default=None, description="저가 / 길이 17")
    acvol: int | None = Field(default=None, description="거래량 / 길이 15")
    uplimit: float | None = Field(default=None, description="상한가 / 길이 17")
    uplimit_rate: float | None = Field(default=None, description="상한가비율 / 길이 8")
    lolimit: float | None = Field(default=None, description="하한가 / 길이 17")
    lolimit_rate: float | None = Field(default=None, description="하한가비율 / 길이 8")
    w52high_prc: float | None = Field(default=None, description="52주최고가 / 길이 17")
    w52highprc_netchng: float | None = Field(default=None, description="52주최고가대비 / 길이 17")
    w52high_date: str | None = Field(default=None, description="52주최고일자 / 길이 8")
    w52low_prc: float | None = Field(default=None, description="52주최저가 / 길이 17")
    w52lowprc_netchng: float | None = Field(default=None, description="52주최저가대비 / 길이 17")
    w52low_date: str | None = Field(default=None, description="52주최저일자 / 길이 8")
    quote_time: str | None = Field(default=None, description="호가시간 / 길이 6")
    best_ask1: float | None = Field(default=None, description="매도1호가 / 길이 17")
    best_bid1: float | None = Field(default=None, description="매수1호가 / 길이 17")
    best_asiz1: int | None = Field(default=None, description="매도1호가수량 / 길이 15")
    best_bsiz1: int | None = Field(default=None, description="매수1호가수량 / 길이 15")
    best_ask2: float | None = Field(default=None, description="매도2호가 / 길이 17")
    best_bid2: float | None = Field(default=None, description="매수2호가 / 길이 17")
    best_asiz2: int | None = Field(default=None, description="매도2호가수량 / 길이 15")
    best_bsiz2: int | None = Field(default=None, description="매수2호가수량 / 길이 15")
    best_ask3: float | None = Field(default=None, description="매도3호가 / 길이 17")
    best_bid3: float | None = Field(default=None, description="매수3호가 / 길이 17")
    best_asiz3: int | None = Field(default=None, description="매도3호가수량 / 길이 15")
    best_bsiz3: int | None = Field(default=None, description="매수3호가수량 / 길이 15")
    best_ask4: float | None = Field(default=None, description="매도4호가 / 길이 17")
    best_bid4: float | None = Field(default=None, description="매수4호가 / 길이 17")
    best_asiz4: int | None = Field(default=None, description="매도4호가수량 / 길이 15")
    best_bsiz4: int | None = Field(default=None, description="매수4호가수량 / 길이 15")
    best_ask5: float | None = Field(default=None, description="매도5호가 / 길이 17")
    best_bid5: float | None = Field(default=None, description="매수5호가 / 길이 17")
    best_asiz5: int | None = Field(default=None, description="매도5호가수량 / 길이 15")
    best_bsiz5: int | None = Field(default=None, description="매수5호가수량 / 길이 15")
    asksize: int | None = Field(default=None, description="총매도잔량 / 길이 15")
    bidsize: int | None = Field(default=None, description="총매수잔량 / 길이 15")
    cov_pric: float | None = Field(default=None, description="환산가 / 길이 17")
    currency_prc: float | None = Field(default=None, description="환율 / 길이 17")
    list_num: float | None = Field(default=None, description="발행주식수 / 길이 17")
    list_amt: float | None = Field(default=None, description="시가총액 / 길이 17")
    list_amt_2: float | None = Field(default=None, description="시가총액(원화) / 길이 17")
    turnover: float | None = Field(default=None, description="거래대금 / 길이 17")
    currency_unit: str | None = Field(default=None, description="거래통화 / 길이 3")
    hst_trdprc: float | None = Field(default=None, description="전일종가 / 길이 17")
    capital_amt: float | None = Field(default=None, description="자본금 / 길이 17")
    base_prc: float | None = Field(default=None, description="기준가 / 길이 17")
    eps_date: str | None = Field(default=None, description="EPS일자 / 길이 8")
    eps_prc: float | None = Field(default=None, description="EPS / 길이 17")
    per_prc: float | None = Field(default=None, description="PER / 길이 17")
    trading_unit: float | None = Field(default=None, description="매매단위 / 길이 17")
    hst_acvol: int | None = Field(default=None, description="전일거래량 / 길이 15")
    trade_date: str | None = Field(default=None, description="거래일자 / 길이 8")
    exch_id: str | None = Field(default=None, description="거래소ID / 길이 3")
    exch_name: str | None = Field(default=None, description="거래소명 / 길이 40")
    com_kind: str | None = Field(default=None, description="자산구분코드 / 길이 2")
    com_kind_name: str | None = Field(default=None, description="자산구분명 / 길이 40")
    pf_jgubun: str | None = Field(default=None, description="(PF)장구분 / 길이 1")
    pf_trdprc: float | None = Field(default=None, description="(PF)현재가 / 길이 17")
    pf_netchng_cls: str | None = Field(default=None, description="(PF)전일대비구분 / 길이 1")
    pf_netchng: float | None = Field(default=None, description="(PF)전일대비 / 길이 17")
    pf_pctchng: float | None = Field(default=None, description="(PF)전일대비율 / 길이 8")
    best_ask6: float | None = Field(default=None, description="매도6호가 / 길이 17")
    best_bid6: float | None = Field(default=None, description="매수6호가 / 길이 17")
    best_asiz6: int | None = Field(default=None, description="매도6호가수량 / 길이 15")
    best_bsiz6: int | None = Field(default=None, description="매수6호가수량 / 길이 15")
    best_ask7: float | None = Field(default=None, description="매도7호가 / 길이 17")
    best_bid7: float | None = Field(default=None, description="매수7호가 / 길이 17")
    best_asiz7: int | None = Field(default=None, description="매도7호가수량 / 길이 15")
    best_bsiz7: int | None = Field(default=None, description="매수7호가수량 / 길이 15")
    best_ask8: float | None = Field(default=None, description="매도8호가 / 길이 17")
    best_bid8: float | None = Field(default=None, description="매수8호가 / 길이 17")
    best_asiz8: int | None = Field(default=None, description="매도8호가수량 / 길이 15")
    best_bsiz8: int | None = Field(default=None, description="매수8호가수량 / 길이 15")
    best_ask9: float | None = Field(default=None, description="매도9호가 / 길이 17")
    best_bid9: float | None = Field(default=None, description="매수9호가 / 길이 17")
    best_asiz9: int | None = Field(default=None, description="매도9호가수량 / 길이 15")
    best_bsiz9: int | None = Field(default=None, description="매수9호가수량 / 길이 15")
    best_ask10: float | None = Field(default=None, description="매도10호가 / 길이 17")
    best_bid10: float | None = Field(default=None, description="매수10호가 / 길이 17")
    best_asiz10: int | None = Field(default=None, description="매도10호가수량 / 길이 15")
    best_bsiz10: int | None = Field(default=None, description="매수10호가수량 / 길이 15")
    marketperiod_cls: str | None = Field(default=None, description="현재시장구분 / 길이 1")
    normal_trdprc: float | None = Field(default=None, description="정규장종가 / 길이 17")
    normal_netchng_cls: str | None = Field(default=None, description="정규장대비구분 / 길이 1 / 2.상승 3.보합 5.하락")
    normal_netchng: float | None = Field(default=None, description="정규장전일대비 / 길이 17")
    normal_pctchng: float | None = Field(default=None, description="정규장전일대비율 / 길이 8")
    normal_acvol: float | None = Field(default=None, description="정규장누적거래량 / 길이 15")
    normal_open_prc: float | None = Field(default=None, description="정규장시가 / 길이 17")
    normal_high: float | None = Field(default=None, description="정규장고가 / 길이 17")
    normal_low: float | None = Field(default=None, description="정규장저가 / 길이 17")


class OverseasStockExecutionTrendItem(BaseModel):
    """해외주식 체결추이 조회 결과 (`Output_0`) 항목."""

    model_config = ConfigDict(extra="allow")

    iem_cd: str | None = Field(default=None, description="종목코드 / 길이 15")
    trade_date: str | None = Field(default=None, description="체결일자 / 길이 8 / YYYYMMDD")
    trade_time: str | None = Field(default=None, description="체결시간 / 길이 6 / HHMMSS")
    trdprc: float | None = Field(default=None, description="체결가 / 길이 17")
    netchng_cls: str | None = Field(
        default=None,
        description=(
            "전일대비구분 / 길이 1 / 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보함+리버스(기세)"
        ),
    )
    netchng: float | None = Field(default=None, description="전일대비가 / 길이 17")
    pctchng: float | None = Field(default=None, description="전일대비율 / 길이 8")
    turnover: float | None = Field(default=None, description="거래대금 / 길이 17")
    fill_size: int | None = Field(default=None, description="변동량 / 길이 15")
    acvol: int | None = Field(default=None, description="체결량 / 길이 15")
    open_prc: float | None = Field(default=None, description="시가 / 길이 17")
    high: float | None = Field(default=None, description="고가 / 길이 17")
    low: float | None = Field(default=None, description="저가 / 길이 17")
    best_ask1: float | None = Field(default=None, description="매도1호가 / 길이 17")
    best_bid1: float | None = Field(default=None, description="매수1호가 / 길이 17")
    cont_rate: float | None = Field(default=None, description="당일체결강도 / 길이 8")
    nextbutton: str | None = Field(default=None, description="NEXTBUTTON / 길이 1")
    ctsz18: str | None = Field(default=None, description="CTSz18 / 길이 18")


class OverseasStockExecutionTrend(BaseModel):
    """해외주식 체결추이 (`POST /gbstock/quote/v1/executionTrend`) 응답.

    응답 블록은 데이터가 있을 때만 내려오므로 모두 Optional.
    """

    model_config = ConfigDict(extra="allow")

    rsp_cd: str | None = Field(default=None, description="응답코드")
    rsp_msg: str | None = Field(default=None, description="응답메시지")
    output_0: list[OverseasStockExecutionTrendItem] | None = Field(
        default=None, alias="Output_0", description="해외주식 체결추이 조회 결과"
    )
    message: NHPlugMessage | None = Field(default=None, description="공통 응답 메시지 봉투")


class OverseasStockCurrentPrice(BaseModel):
    """해외주식 현재가상세 (`POST /gbstock/quote/v1/current`) 응답.

    응답 블록은 데이터가 있을 때만 내려오므로 모두 Optional.
    """

    model_config = ConfigDict(extra="allow")

    rsp_cd: str | None = Field(default=None, description="응답코드")
    rsp_msg: str | None = Field(default=None, description="응답메시지")
    output_0: OverseasStockCurrentPriceItem | None = Field(
        default=None, alias="Output_0", description="해외주식 현재가상세 조회 결과"
    )
    message: NHPlugMessage | None = Field(default=None, description="공통 응답 메시지 봉투")
