from typing import Optional

from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

from cluefin_openapi.kiwoom._model import KiwoomHttpBody


class DomesticSectorIndustryProgram(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="업종프로그램요청 응답")

    dfrt_trst_sell_qty: str = Field(default="", description="차익위탁매도수량")
    dfrt_trst_sell_amt: str = Field(default="", description="차익위탁매도금액")
    dfrt_trst_buy_qty: str = Field(default="", description="차익위탁매수수량")
    dfrt_trst_buy_amt: str = Field(default="", description="차익위탁매수금액")
    dfrt_trst_netprps_qty: str = Field(default="", description="차익위탁순매수수량")
    dfrt_trst_netprps_amt: str = Field(default="", description="차익위탁순매수금액")
    ndiffpro_trst_sell_qty: str = Field(default="", description="비차익위탁매도수량")
    ndiffpro_trst_sell_amt: str = Field(default="", description="비차익위탁매도금액")
    ndiffpro_trst_buy_qty: str = Field(default="", description="비차익위탁매수수량")
    ndiffpro_trst_buy_amt: str = Field(default="", description="비차익위탁매수금액")
    ndiffpro_trst_netprps_qty: str = Field(default="", description="비차익위탁순매수수량")
    ndiffpro_trst_netprps_amt: str = Field(default="", description="비차익위탁순매수금액")
    all_dfrt_trst_sell_qty: str = Field(default="", description="전체차익위탁매도수량")
    all_dfrt_trst_sell_amt: str = Field(default="", description="전체차익위탁매도금액")
    all_dfrt_trst_buy_qty: str = Field(default="", description="전체차익위탁매수수량")
    all_dfrt_trst_buy_amt: str = Field(default="", description="전체차익위탁매수금액")
    all_dfrt_trst_netprps_qty: str = Field(default="", description="전체차익위탁순매수수량")
    all_dfrt_trst_netprps_amt: str = Field(default="", description="전체차익위탁순매수금액")


class DomesticSectorIndustryInvestorNetBuyItem(BaseModel):
    inds_cd: str = Field(default="", description="업종코드")
    inds_nm: str = Field(default="", description="업종명")
    cur_prc: str = Field(default="", description="현재가")
    pre_smbol: str = Field(default="", description="대비부호")
    pred_pre: str = Field(default="", description="전일대비")
    flu_rt: str = Field(default="", description="등락율")
    trde_qty: str = Field(default="", description="거래량")
    sc_netprps: str = Field(default="", description="증권순매수")
    insrnc_netprps: str = Field(default="", description="보험순매수")
    invtrt_netprps: str = Field(default="", description="투신순매수")
    bank_netprps: str = Field(default="", description="은행순매수")
    jnsinkm_netprps: str = Field(default="", description="종신금순매수")
    endw_netprps: str = Field(default="", description="기금순매수")
    etc_corp_netprps: str = Field(default="", description="기타법인순매수")
    ind_netprps: str = Field(default="", description="개인순매수")
    frgnr_netprps: str = Field(default="", description="외국인순매수")
    native_trmt_frgnr_netprps: Optional[str] = Field(default=None, description="내국인대우외국인순매수")
    natn_netprps: Optional[str] = Field(default=None, description="국가순매수")
    samo_fund_netprps: Optional[str] = Field(default=None, description="사모펀드순매수")
    orgn_netprps: Optional[str] = Field(default=None, description="기관계순매수")


class DomesticSectorIndustryInvestorNetBuy(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="업종별투자자순매수요청 응답")

    inds_netprps: list[DomesticSectorIndustryInvestorNetBuyItem] = Field(
        default_factory=list, description="업종별 순매수 데이터"
    )


class DomesticSectorIndustryCurrentPriceItem(BaseModel):
    tm_n: str = Field(default="", description="시간n")
    cur_prc_n: str = Field(default="", description="현재가n")
    pred_pre_sig_n: str = Field(default="", description="전일대비기호n")
    pred_pre_n: str = Field(default="", description="전일대비n")
    flu_rt_n: str = Field(default="", description="등락률n")
    trde_qty_n: str = Field(default="", description="거래량n")
    acc_trde_qty_n: str = Field(default="", description="누적거래량n")


class DomesticSectorIndustryCurrentPrice(BaseModel, KiwoomHttpBody):
    cur_prc: str = Field(default="", description="현재가")
    pred_pre_sig: str = Field(default="", description="전일대비기호")
    pred_pre: str = Field(default="", description="전일대비")
    flu_rt: str = Field(default="", description="등락률")
    trde_qty: str = Field(default="", description="거래량")
    trde_prica: str = Field(default="", description="거래대금")
    trde_frmatn_stk_num: str = Field(default="", description="거래형성종목수")
    trde_frmatn_rt: str = Field(default="", description="거래형성비율")
    open_pric: str = Field(default="", description="시가")
    high_pric: str = Field(default="", description="고가")
    low_pric: str = Field(default="", description="저가")
    upl: str = Field(default="", description="상한")
    rising: str = Field(default="", description="상승")
    stdns: str = Field(default="", description="보합")
    fall: str = Field(default="", description="하락")
    lst: str = Field(default="", description="하한")
    week52_hgst_pric: str = Field(default="", description="52주최고가", alias="52wk_hgst_pric")
    week52_hgst_pric_dt: str = Field(default="", description="52주최고가일", alias="52wk_hgst_pric_dt")
    week52_hgst_pric_pre_rt: str = Field(default="", description="52주최고가대비율", alias="52wk_hgst_pric_pre_rt")
    week52_lwst_pric: str = Field(default="", description="52주최저가", alias="52wk_lwst_pric")
    week52_lwst_pric_dt: str = Field(default="", description="52주최저가일", alias="52wk_lwst_pric_dt")
    week52_lwst_pric_pre_rt: str = Field(default="", description="52주최저가대비율", alias="52wk_lwst_pric_pre_rt")
    inds_cur_prc_tm: list[DomesticSectorIndustryCurrentPriceItem] = Field(
        default_factory=list, description="업종현재가_시간별"
    )


class DomesticSectorIndustryPriceBySectorItem(BaseModel):
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    cur_prc: str = Field(default="", description="현재가")
    pred_pre_sig: str = Field(default="", description="전일대비기호")
    pred_pre: str = Field(default="", description="전일대비")
    flu_rt: str = Field(default="", description="등락률")
    now_trde_qty: str = Field(default="", description="현재거래량")
    sel_bid: str = Field(default="", description="매도호가")
    buy_bid: str = Field(default="", description="매수호가")
    open_pric: str = Field(default="", description="시가")
    high_pric: str = Field(default="", description="고가")
    low_pric: str = Field(default="", description="저가")


class DomesticSectorIndustryPriceBySector(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="업종별주가요청 응답")

    inds_stkpc: list[DomesticSectorIndustryPriceBySectorItem] = Field(default_factory=list, description="업종별주가")


class DomesticSectorAllIndustryIndexItem(BaseModel):
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    cur_prc: str = Field(default="", description="현재가")
    pre_sig: str = Field(default="", description="대비기호")
    pred_pre: str = Field(default="", description="전일대비")
    flu_rt: str = Field(default="", description="등락률")
    trde_qty: str = Field(default="", description="거래량")
    wght: str = Field(default="", description="비중")
    trde_prica: str = Field(default="", description="거래대금")
    upl: str = Field(default="", description="상한")
    rising: str = Field(default="", description="상승")
    stdns: str = Field(default="", description="보합")
    fall: str = Field(default="", description="하락")
    lst: str = Field(default="", description="하한")
    flo_stk_num: str = Field(default="", description="상장종목수")


class DomesticSectorAllIndustryIndex(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="전업종지수요청 응답")

    all_inds_idex: list[DomesticSectorAllIndustryIndexItem] = Field(
        default_factory=list, description="전업종지수 데이터"
    )


class DomesticSectorDailyIndustryCurrentPriceItem(BaseModel):
    dt_n: str = Field(default="", description="일자n")
    cur_prc_n: str = Field(default="", description="현재가n")
    pred_pre_sig_n: str = Field(default="", description="전일대비기호n")
    pred_pre_n: str = Field(default="", description="전일대비n")
    flu_rt_n: str = Field(default="", description="등락률n")
    acc_trde_qty_n: str = Field(default="", description="누적거래량n")


class DomesticSectorDailyIndustryCurrentPrice(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="업종현재가일별요청 응답")

    cur_prc: str = Field(default="", description="현재가")
    pred_pre_sig: str = Field(default="", description="전일대비기호")
    pred_pre: str = Field(default="", description="전일대비")
    flu_rt: str = Field(default="", description="등락률")
    trde_qty: str = Field(default="", description="거래량")
    trde_prica: str = Field(default="", description="거래대금")
    trde_frmatn_stk_num: str = Field(default="", description="거래형성종목수")
    trde_frmatn_rt: str = Field(default="", description="거래형성비율")
    open_pric: str = Field(default="", description="시가")
    high_pric: str = Field(default="", description="고가")
    low_pric: str = Field(default="", description="저가")
    upl: str = Field(default="", description="상한")
    rising: str = Field(default="", description="상승")
    stdns: str = Field(default="", description="보합")
    fall: str = Field(default="", description="하락")
    lst: str = Field(default="", description="하한")
    week52_hgst_pric: str = Field(default="", description="52주최고가", alias="52wk_hgst_pric")
    week52_hgst_pric_dt: str = Field(default="", description="52주최고가일", alias="52wk_hgst_pric_dt")
    week52_hgst_pric_pre_rt: str = Field(default="", description="52주최고가대비율", alias="52wk_hgst_pric_pre_rt")
    week52_lwst_pric: str = Field(default="", description="52주최저가", alias="52wk_lwst_pric")
    week52_lwst_pric_dt: str = Field(default="", description="52주최저가일", alias="52wk_lwst_pric_dt")
    week52_lwst_pric_pre_rt: str = Field(default="", description="52주최저가대비율", alias="52wk_lwst_pric_pre_rt")
    inds_cur_prc_daly_rept: list[DomesticSectorDailyIndustryCurrentPriceItem] = Field(
        default_factory=list, description="업종현재가_일별반복"
    )
