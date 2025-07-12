from pydantic import BaseModel, ConfigDict, Field

from cluefin_openapi.kiwoom._model import KiwoomHttpBody


class DomesticEtfReturnRateItem(BaseModel):
    etfprft_rt: str = Field(default="", description="ETF수익률", max_length=20)
    cntr_prft_rt: str = Field(default="", description="체결수익률", max_length=20)
    for_netprps_qty: str = Field(default="", description="외인순매수수량", max_length=20)
    orgn_netprps_qty: str = Field(default="", description="기관순매수수량", max_length=20)


class DomesticEtfReturnRate(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="ETF수익률 응답")

    etfprft_rt_lst: list[DomesticEtfReturnRateItem] = Field(default_factory=list, description="ETF수익율 리스트")


class DomesticEtfItemInfo(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="ETF종목정보 응답")

    stk_nm: str = Field(default="", description="종목명", max_length=40)
    etfobjt_idex_nm: str = Field(default="", description="ETF대상지수명", max_length=20)
    wonju_pric: str = Field(default="", description="원주가격", max_length=20)
    etftxon_type: str = Field(default="", description="ETF과세유형", max_length=20)
    etntxon_type: str = Field(default="", description="ETN과세유형", max_length=20)


class DomesticEtfDailyTrendItem(BaseModel):
    cntr_dt: str = Field(default="", description="체결일자", max_length=20)
    cur_prc: str = Field(default="", description="현재가", max_length=20)
    pre_sig: str = Field(default="", description="대비기호", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    pre_rt: str = Field(default="", description="대비율", max_length=20)
    trde_qty: str = Field(default="", description="거래량", max_length=20)
    nav: str = Field(default="", description="NAV", max_length=20)
    acc_trde_prica: str = Field(default="", description="누적거래대금", max_length=20)
    navidex_dispty_rt: str = Field(default="", description="NAV/지수괴리율", max_length=20)
    navetfdispty_rt: str = Field(default="", description="NAV/ETF괴리율", max_length=20)
    trace_eor_rt: str = Field(default="", description="추적오차율", max_length=20)
    trace_cur_prc: str = Field(default="", description="추적현재가", max_length=20)
    trace_pred_pre: str = Field(default="", description="추적전일대비", max_length=20)
    trace_pre_sig: str = Field(default="", description="추적대비기호", max_length=20)


class DomesticEtfDailyTrend(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="ETF일별추이 응답")

    etfdaly_trnsn: list[DomesticEtfDailyTrendItem] = Field(default_factory=list, description="ETF일별추이 리스트")


class DomesticEtfFullPriceItem(BaseModel):
    stk_cd: str = Field(default="", description="종목코드", max_length=20)
    stk_cls: str = Field(default="", description="종목분류", max_length=20)
    stk_nm: str = Field(default="", description="종목명", max_length=40)
    close_pric: str = Field(default="", description="종가", max_length=20)
    pre_sig: str = Field(default="", description="대비기호", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    pre_rt: str = Field(default="", description="대비율", max_length=20)
    trde_qty: str = Field(default="", description="거래량", max_length=20)
    nav: str = Field(default="", description="NAV", max_length=20)
    trace_eor_rt: str = Field(default="", description="추적오차율", max_length=20)
    txbs: str = Field(default="", description="과표기준", max_length=20)
    dvid_bf_base: str = Field(default="", description="배당전기준", max_length=20)
    pred_dvida: str = Field(default="", description="전일배당금", max_length=20)
    trace_idex_nm: str = Field(default="", description="추적지수명", max_length=40)
    drng: str = Field(default="", description="배수", max_length=20)
    trace_idex_cd: str = Field(default="", description="추적지수코드", max_length=20)
    trace_idex: str = Field(default="", description="추적지수", max_length=20)
    trace_flu_rt: str = Field(default="", description="추적등락율", max_length=20)


class DomesticEtfFullPrice(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="ETF전체시세 응답")

    etfall_mrpr: list[DomesticEtfFullPriceItem] = Field(default_factory=list, description="ETF전체시세 리스트")


class DomesticEtfHourlyTrendItem(BaseModel):
    tm: str = Field(default="", description="시간", max_length=20)
    close_pric: str = Field(default="", description="종가", max_length=20)
    pre_sig: str = Field(default="", description="대비기호", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    flu_rt: str = Field(default="", description="등락율", max_length=20)
    trde_qty: str = Field(default="", description="거래량", max_length=20)
    nav: str = Field(default="", description="NAV", max_length=20)
    trde_prica: str = Field(default="", description="거래대금", max_length=20)
    navidex: str = Field(default="", description="NAV지수", max_length=20)
    navetf: str = Field(default="", description="NAVETF", max_length=20)
    trace: str = Field(default="", description="추적", max_length=20)
    trace_idex: str = Field(default="", description="추적지수", max_length=20)
    trace_idex_pred_pre: str = Field(default="", description="추적지수전일대비", max_length=20)
    trace_idex_pred_pre_sig: str = Field(default="", description="추적지수전일대비기호", max_length=20)


class DomesticEtfHourlyTrend(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="ETF시간대별추이 응답")

    stk_nm: str = Field(default="", description="종목명", max_length=40)
    etfobjt_idex_nm: str = Field(default="", description="ETF대상지수명", max_length=20)
    wonju_pric: str = Field(default="", description="원주가격", max_length=20)
    etftxon_type: str = Field(default="", description="ETF과세유형", max_length=20)
    etntxon_type: str = Field(default="", description="ETN과세유형", max_length=20)
    etftisl_trnsn: list[DomesticEtfHourlyTrendItem] = Field(default_factory=list, description="ETF시간대별추이 리스트")


class DomesticEtfHourlyExecutionItem(BaseModel):
    cntr_tm: str = Field(default="", description="체결시간", max_length=20)
    cur_prc: str = Field(default="", description="현재가", max_length=20)
    pre_sig: str = Field(default="", description="대비기호", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    trde_qty: str = Field(default="", description="거래량", max_length=20)
    stex_tp: str = Field(default="", description="거래소구분. KRX, NXT, 통합", max_length=20)


class DomesticEtfHourlyExecution(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="ETF시간대별체결 응답")

    stk_cls: str = Field(default="", description="종목분류", max_length=20)
    stk_nm: str = Field(default="", description="종목명", max_length=40)
    etfobjt_idex_nm: str = Field(default="", description="ETF대상지수명", max_length=20)
    etfobjt_idex_cd: str = Field(default="", description="ETF대상지수코드", max_length=20)
    objt_idex_pre_rt: str = Field(default="", description="대상지수대비율", max_length=20)
    wonju_pric: str = Field(default="", description="원주가격", max_length=20)
    etftisl_cntr_array: list[DomesticEtfHourlyExecutionItem] = Field(
        default_factory=list, description="ETF시간대별체결배열 리스트"
    )


class DomesticEtfDailyExecutionItem(BaseModel):
    dt: str = Field(default="", description="일자", max_length=20)
    cur_prc_n: str = Field(default="", description="현재가n", max_length=20)
    pre_sig_n: str = Field(default="", description="대비기호n", max_length=20)
    pred_pre_n: str = Field(default="", description="전일대비n", max_length=20)
    acc_trde_qty: str = Field(default="", description="누적거래량", max_length=20)
    for_netprps_qty: str = Field(default="", description="외인순매수수량", max_length=20)
    orgn_netprps_qty: str = Field(default="", description="기관순매수수량", max_length=20)


class DomesticEtfDailyExecution(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="ETF일별체결 응답")

    cntr_tm: str = Field(default="", description="체결시간", max_length=20)
    cur_prc: str = Field(default="", description="현재가", max_length=20)
    pre_sig: str = Field(default="", description="대비기호", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    trde_qty: str = Field(default="", description="거래량", max_length=20)
    etfnetprps_qty_array: list[DomesticEtfDailyExecutionItem] = Field(
        default_factory=list, description="ETF순매수수량배열 리스트"
    )


class DomesticEtfHourlyExecutionV2Item(BaseModel):
    nav: str = Field(default="", description="NAV", max_length=20)
    navpred_pre: str = Field(default="", description="NAV전일대비", max_length=20)
    navflu_rt: str = Field(default="", description="NAV등락율", max_length=20)
    trace_eor_rt: str = Field(default="", description="추적오차율", max_length=20)
    dispty_rt: str = Field(default="", description="괴리율", max_length=20)
    stkcnt: str = Field(default="", description="주식수", max_length=20)
    base_pric: str = Field(default="", description="기준가", max_length=20)
    for_rmnd_qty: str = Field(default="", description="외인보유수량", max_length=20)
    repl_pric: str = Field(default="", description="대용가", max_length=20)
    conv_pric: str = Field(default="", description="환산가격", max_length=20)
    drstk: str = Field(default="", description="DR/주", max_length=20)
    wonju_pric: str = Field(default="", description="원주가격", max_length=20)


class DomesticEtfHourlyExecutionV2(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="ETF시간대별체결V2 응답")

    etfnavarray: list[DomesticEtfHourlyExecutionV2Item] = Field(default_factory=list, description="ETF NAV배열 리스트")


class DomesticEtfHourlyTrendV2Item(BaseModel):
    cntr_tm: str = Field(default="", description="체결시간", max_length=20)
    cur_prc: str = Field(default="", description="현재가", max_length=20)
    pre_sig: str = Field(default="", description="대비기호", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    trde_qty: str = Field(default="", description="거래량", max_length=20)
    for_netprps: str = Field(default="", description="외인순매수", max_length=20)


class DomesticEtfHourlyTrendV2(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="ETF시간대별추이V2 응답")

    etftisl_trnsn: list[DomesticEtfHourlyTrendV2Item] = Field(
        default_factory=list, description="ETF시간대별추이 리스트"
    )
