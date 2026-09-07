from pydantic import BaseModel, ConfigDict, Field

from cluefin_openapi.kiwoom._model import (
    KiwoomHttpBody,
)


class DomesticChartIndividualStockInstitutionalItem(BaseModel):
    dt: str = Field(
        default="",
        description="일자 (YYYYMMDD)",
    )
    cur_prc: str = Field(
        default="",
        description="현재가",
    )
    pred_pre: str = Field(
        default="",
        description="전일대비",
    )
    acc_trde_prica: str = Field(
        default="",
        description="누적거래대금",
    )
    ind_invsr: str = Field(
        default="",
        description="개인투자자",
    )
    frgnr_invsr: str = Field(
        default="",
        description="외국인투자자",
    )
    orgn: str = Field(
        default="",
        description="기관계",
    )
    fnnc_invt: str = Field(
        default="",
        description="금융투자",
    )
    insrnc: str = Field(
        default="",
        description="보험",
    )
    invtrt: str = Field(
        default="",
        description="투신",
    )
    etc_fnnc: str = Field(
        default="",
        description="기타금융",
    )
    bank: str = Field(
        default="",
        description="은행",
    )
    penfnd_etc: str = Field(
        default="",
        description="연기금등",
    )
    samo_fund: str = Field(
        default="",
        description="사모펀드",
    )
    natn: str = Field(
        default="",
        description="국가",
    )
    etc_corp: str = Field(
        default="",
        description="기타법인",
    )
    natfor: str = Field(
        default="",
        description="내외국인",
    )


class DomesticChartIndividualStockInstitutional(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="종목별투자자기관별차트요청 응답")

    stk_invsr_orgn_chart: list[DomesticChartIndividualStockInstitutionalItem] = Field(
        default_factory=list,
        description="종목별 투자자 기관별 차트 데이터",
        json_schema_extra={"title": "종목별투자자기관별차트", "type": "array"},
    )


class DomesticChartIntradayInvestorTradingItem(BaseModel):
    tm: str = Field(
        default="",
        description="시간",
    )
    frgnr_invsr: str = Field(
        default="",
        description="외국인투자자",
    )
    orgn: str = Field(
        default="",
        description="기관계",
    )
    invtrt: str = Field(
        default="",
        description="투신",
    )
    insrnc: str = Field(
        default="",
        description="보험",
    )
    bank: str = Field(
        default="",
        description="은행",
    )
    penfnd_etc: str = Field(
        default="",
        description="연기금등",
    )
    etc_corp: str = Field(
        default="",
        description="기타법인",
    )
    natn: str = Field(
        default="",
        description="국가",
    )


class DomesticChartIntradayInvestorTrading(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="장중투자자매매차트요청 응답")

    opmr_invsr_trde_chart: list[DomesticChartIntradayInvestorTradingItem] = Field(
        default_factory=list,
        description="장중 투자자별 매매 차트 데이터",
        json_schema_extra={"title": "장중투자자별매매차트", "type": "array"},
    )


class DomesticChartStockTickItem(BaseModel):
    cur_prc: str = Field(
        default="",
        description="현재가",
    )
    trde_qty: str = Field(
        default="",
        description="거래량",
    )
    cntr_tm: str = Field(
        default="",
        description="체결시간",
    )
    open_pric: str = Field(
        default="",
        description="시가",
    )
    high_pric: str = Field(
        default="",
        description="고가",
    )
    low_pric: str = Field(
        default="",
        description="저가",
    )
    pred_pre: str = Field(
        default="",
        description="전일대비",
    )
    pred_pre_sig: str = Field(
        default="",
        description="전일대비 기호",
    )


class DomesticChartStockTick(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="종목틱차트요청 응답")

    stk_cd: str = Field(default="", description="종목코드", json_schema_extra={"max_length": 6})
    last_tic_cnt: str = Field(
        default="",
        description="마지막틱갯수",
    )
    stk_tic_chart_qry: list[DomesticChartStockTickItem] = Field(
        default_factory=list,
        description="주식틱차트조회 데이터",
        json_schema_extra={"title": "주식틱차트조회", "type": "array"},
    )


class DomesticChartStockMinuteItem(BaseModel):
    cur_prc: str = Field(
        default="",
        description="현재가",
    )
    trde_qty: str = Field(
        default="",
        description="거래량",
    )
    cntr_tm: str = Field(
        default="",
        description="체결시간",
    )
    open_pric: str = Field(
        default="",
        description="시가",
    )
    high_pric: str = Field(
        default="",
        description="고가",
    )
    low_pric: str = Field(
        default="",
        description="저가",
    )
    pred_pre: str = Field(
        default="",
        description="전일대비",
    )
    pred_pre_sig: str = Field(
        default="",
        description="전일대비 기호",
    )


class DomesticChartStockMinute(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="주식분봉차트조회요청 응답")

    stk_cd: str = Field(default="", description="종목코드", json_schema_extra={"max_length": 6})
    stk_min_pole_chart_qry: list[DomesticChartStockMinuteItem] = Field(
        default_factory=list,
        description="주식분봉차트조회 데이터",
        json_schema_extra={"title": "주식분봉차트조회", "type": "array"},
    )


class DomesticChartStockDailyItem(BaseModel):
    dt: str = Field(description="일자 (YYYYMMDD)")
    cur_prc: str = Field(description="현재가")
    trde_qty: str = Field(description="거래량")
    trde_prica: str = Field(description="거래대금")
    open_pric: str = Field(description="시가")
    high_pric: str = Field(description="고가")
    low_pric: str = Field(description="저가")
    pred_pre: str = Field(description="전일대비")
    pred_pre_sig: str = Field(description="전일대비부호")
    trde_tern_rt: str = Field(description="거래전환율")


class DomesticChartStockDaily(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="주식일봉차트조회요청 응답")

    stk_cd: str = Field(default="", description="종목코드", json_schema_extra={"max_length": 6})
    stk_dt_pole_chart_qry: list[DomesticChartStockDailyItem] = Field(
        default_factory=list,
        description="주식일봉차트조회 데이터",
        json_schema_extra={"title": "주식일봉차트조회", "type": "array"},
    )


class DomesticChartStockWeeklyItem(BaseModel):
    dt: str = Field(description="일자 (YYYYMMDD)")
    cur_prc: str = Field(description="현재가")
    trde_qty: str = Field(description="거래량")
    trde_prica: str = Field(description="거래대금")
    open_pric: str = Field(description="시가")
    high_pric: str = Field(description="고가")
    low_pric: str = Field(description="저가")
    pred_pre: str = Field(description="전일대비")
    pred_pre_sig: str = Field(description="전일대비부호")
    trde_tern_rt: str = Field(description="거래전환율")


class DomesticChartStockWeekly(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="주식주봉차트조회요청 응답")

    stk_cd: str = Field(default="", description="종목코드", json_schema_extra={"max_length": 6})
    stk_stk_pole_chart_qry: list[DomesticChartStockWeeklyItem] = Field(
        default_factory=list,
        description="주식주봉차트조회 데이터",
        json_schema_extra={"title": "주식주봉차트조회", "type": "array"},
    )


class DomesticChartStockMonthlyItem(BaseModel):
    dt: str = Field(description="일자 (YYYYMMDD)")
    cur_prc: str = Field(description="현재가")
    trde_qty: str = Field(description="거래량")
    trde_prica: str = Field(description="거래대금")
    open_pric: str = Field(description="시가")
    high_pric: str = Field(description="고가")
    low_pric: str = Field(description="저가")
    pred_pre: str = Field(description="전일대비")
    pred_pre_sig: str = Field(description="전일대비부호")
    trde_tern_rt: str = Field(description="거래전환율")


class DomesticChartStockMonthly(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="주식월봉차트조회요청 응답")

    stk_cd: str = Field(default="", description="종목코드", json_schema_extra={"max_length": 6})
    stk_mth_pole_chart_qry: list[DomesticChartStockMonthlyItem] = Field(
        default_factory=list,
        description="주식월봉차트조회 데이터",
        json_schema_extra={"title": "주식월봉차트조회", "type": "array"},
    )


class DomesticChartStockYearlyItem(BaseModel):
    dt: str = Field(description="일자 (YYYYMMDD)")
    cur_prc: str = Field(description="현재가")
    trde_qty: str = Field(description="거래량")
    trde_prica: str = Field(description="거래대금")
    open_pric: str = Field(description="시가")
    high_pric: str = Field(description="고가")
    low_pric: str = Field(description="저가")


class DomesticChartStockYearly(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="주식년봉차트조회요청 응답")

    stk_cd: str = Field(default="", description="종목코드", json_schema_extra={"max_length": 6})
    stk_yr_pole_chart_qry: list[DomesticChartStockYearlyItem] = Field(
        default_factory=list,
        description="주식년봉차트조회 데이터",
        json_schema_extra={"title": "주식년봉차트조회", "type": "array"},
    )


class DomesticChartIndustryTickItem(BaseModel):
    cur_prc: str = Field(
        default="",
        description="현재가",
    )
    trde_qty: str = Field(
        default="",
        description="거래량",
    )
    cntr_tm: str = Field(
        default="",
        description="체결시간",
    )
    open_pric: str = Field(
        default="",
        description="시가",
    )
    high_pric: str = Field(
        default="",
        description="고가",
    )
    low_pric: str = Field(
        default="",
        description="저가",
    )
    pred_pre: str = Field(
        default="",
        description="전일대비",
    )
    pred_pre_sig: str = Field(
        default="",
        description="전일대비 기호",
    )


class DomesticChartIndustryTick(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="업종틱차트조회요청 응답")

    inds_cd: str = Field(
        default="",
        description="업종코드",
    )
    inds_tic_chart_qry: list[DomesticChartIndustryTickItem] = Field(
        default_factory=list,
        description="업종틱차트조회 데이터",
        json_schema_extra={"title": "업종틱차트조회", "type": "array"},
    )


class DomesticChartIndustryMinuteItem(BaseModel):
    cur_prc: str = Field(
        default="",
        description="현재가",
    )
    trde_qty: str = Field(
        default="",
        description="거래량",
    )
    cntr_tm: str = Field(
        default="",
        description="체결시간",
    )
    open_pric: str = Field(
        default="",
        description="시가",
    )
    high_pric: str = Field(
        default="",
        description="고가",
    )
    low_pric: str = Field(
        default="",
        description="저가",
    )
    acc_trde_qty: str = Field(
        default="",
        description="누적거래량",
    )
    pred_pre: str = Field(
        default="",
        description="전일대비",
    )
    pred_pre_sig: str = Field(
        default="",
        description="전일대비 기호",
    )


class DomesticChartIndustryMinute(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="업종분봉조회요청 응답")
    inds_cd: str = Field(
        default="",
        description="업종코드",
    )
    inds_min_pole_qry: list[DomesticChartIndustryMinuteItem] = Field(
        default_factory=list,
        description="업종분봉조회 데이터",
        json_schema_extra={"title": "업종분봉조회", "type": "array"},
    )


class DomesticChartIndustryDailyItem(BaseModel):
    cur_prc: str = Field(
        default="",
        description="현재가",
    )
    trde_qty: str = Field(
        default="",
        description="거래량",
    )
    dt: str = Field(
        default="",
        description="일자 (YYYYMMDD)",
    )
    open_pric: str = Field(
        default="",
        description="시가",
    )
    high_pric: str = Field(
        default="",
        description="고가",
    )
    low_pric: str = Field(
        default="",
        description="저가",
    )
    trde_prica: str = Field(
        default="",
        description="거래대금",
    )


class DomesticChartIndustryDaily(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="업종일봉조회요청 응답")

    inds_cd: str = Field(
        default="",
        description="업종코드",
    )
    inds_dt_pole_qry: list[DomesticChartIndustryDailyItem] = Field(
        default_factory=list,
        description="업종일봉조회 데이터",
        json_schema_extra={"title": "업종일봉조회", "type": "array"},
    )


class DomesticChartIndustryWeeklyItem(BaseModel):
    cur_prc: str = Field(
        default="",
        description="현재가",
    )
    trde_qty: str = Field(
        default="",
        description="거래량",
    )
    dt: str = Field(
        default="",
        description="일자 (YYYYMMDD)",
    )
    open_pric: str = Field(
        default="",
        description="시가",
    )
    high_pric: str = Field(
        default="",
        description="고가",
    )
    low_pric: str = Field(
        default="",
        description="저가",
    )
    trde_prica: str = Field(
        default="",
        description="거래대금",
    )


class DomesticChartIndustryWeekly(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="업종주봉조회요청 응답")

    inds_cd: str = Field(
        default="",
        description="업종코드",
    )
    inds_stk_pole_qry: list[DomesticChartIndustryWeeklyItem] = Field(
        default_factory=list,
        description="업종주봉조회 데이터",
        json_schema_extra={"title": "업종주봉조회", "type": "array"},
    )


class DomesticChartIndustryMonthlyItem(BaseModel):
    cur_prc: str = Field(
        default="",
        description="현재가",
    )
    trde_qty: str = Field(
        default="",
        description="거래량",
    )
    dt: str = Field(
        default="",
        description="일자 (YYYYMMDD)",
    )
    open_pric: str = Field(
        default="",
        description="시가",
    )
    high_pric: str = Field(
        default="",
        description="고가",
    )
    low_pric: str = Field(
        default="",
        description="저가",
    )
    trde_prica: str = Field(
        default="",
        description="거래대금",
    )


class DomesticChartIndustryMonthly(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="업종월봉조회요청 응답")

    inds_cd: str = Field(
        default="",
        description="업종코드",
    )
    inds_mth_pole_qry: list[DomesticChartIndustryMonthlyItem] = Field(
        default_factory=list,
        description="업종월봉조회 데이터",
        json_schema_extra={"title": "업종월봉조회", "type": "array"},
    )


class DomesticChartIndustryYearlyItem(BaseModel):
    cur_prc: str = Field(
        default="",
        description="현재가",
    )
    trde_qty: str = Field(
        default="",
        description="거래량",
    )
    dt: str = Field(
        default="",
        description="일자 (YYYYMMDD)",
    )
    open_pric: str = Field(
        default="",
        description="시가",
    )
    high_pric: str = Field(
        default="",
        description="고가",
    )
    low_pric: str = Field(
        default="",
        description="저가",
    )
    trde_prica: str = Field(
        default="",
        description="거래대금",
    )


class DomesticChartIndustryYearly(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="업종년봉조회요청 응답")

    inds_cd: str = Field(
        default="",
        description="업종코드",
    )
    inds_yr_pole_qry: list[DomesticChartIndustryYearlyItem] = Field(
        default_factory=list,
        description="업종년봉조회 데이터",
        json_schema_extra={"title": "업종년봉조회", "type": "array"},
    )
