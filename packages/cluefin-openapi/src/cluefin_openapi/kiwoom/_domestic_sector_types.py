from typing import Optional

from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

from cluefin_openapi.kiwoom._model import KiwoomHttpBody


class DomesticSectorIndustryProgram(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="업종프로그램요청 응답")

    dfrt_trst_sell_qty: str = Field(default="", description="차익위탁매도수량", max_length=20)
    dfrt_trst_sell_amt: str = Field(default="", description="차익위탁매도금액", max_length=20)
    dfrt_trst_buy_qty: str = Field(default="", description="차익위탁매수수량", max_length=20)
    dfrt_trst_buy_amt: str = Field(default="", description="차익위탁매수금액", max_length=20)
    dfrt_trst_netprps_qty: str = Field(default="", description="차익위탁순매수수량", max_length=20)
    dfrt_trst_netprps_amt: str = Field(default="", description="차익위탁순매수금액", max_length=20)
    ndiffpro_trst_sell_qty: str = Field(default="", description="비차익위탁매도수량", max_length=20)
    ndiffpro_trst_sell_amt: str = Field(default="", description="비차익위탁매도금액", max_length=20)
    ndiffpro_trst_buy_qty: str = Field(default="", description="비차익위탁매수수량", max_length=20)
    ndiffpro_trst_buy_amt: str = Field(default="", description="비차익위탁매수금액", max_length=20)
    ndiffpro_trst_netprps_qty: str = Field(default="", description="비차익위탁순매수수량", max_length=20)
    ndiffpro_trst_netprps_amt: str = Field(default="", description="비차익위탁순매수금액", max_length=20)
    all_dfrt_trst_sell_qty: str = Field(default="", description="전체차익위탁매도수량", max_length=20)
    all_dfrt_trst_sell_amt: str = Field(default="", description="전체차익위탁매도금액", max_length=20)
    all_dfrt_trst_buy_qty: str = Field(default="", description="전체차익위탁매수수량", max_length=20)
    all_dfrt_trst_buy_amt: str = Field(default="", description="전체차익위탁매수금액", max_length=20)
    all_dfrt_trst_netprps_qty: str = Field(default="", description="전체차익위탁순매수수량", max_length=20)
    all_dfrt_trst_netprps_amt: str = Field(default="", description="전체차익위탁순매수금액", max_length=20)


class DomesticSectorIndustryInvestorNetBuyItem(BaseModel):
    inds_cd: str = Field(default="", description="업종코드", max_length=20)
    inds_nm: str = Field(default="", description="업종명", max_length=20)
    cur_prc: str = Field(default="", description="현재가", max_length=20)
    pre_smbol: str = Field(default="", description="대비부호", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    flu_rt: str = Field(default="", description="등락율", max_length=20)
    trde_qty: str = Field(default="", description="거래량", max_length=20)
    sc_netprps: str = Field(default="", description="증권순매수", max_length=20)
    insrnc_netprps: str = Field(default="", description="보험순매수", max_length=20)
    invtrt_netprps: str = Field(default="", description="투신순매수", max_length=20)
    bank_netprps: str = Field(default="", description="은행순매수", max_length=20)
    jnsinkm_netprps: str = Field(default="", description="종신금순매수", max_length=20)
    endw_netprps: str = Field(default="", description="기금순매수", max_length=20)
    etc_corp_netprps: str = Field(default="", description="기타법인순매수", max_length=20)
    ind_netprps: str = Field(default="", description="개인순매수", max_length=20)
    frgnr_netprps: str = Field(default="", description="외국인순매수", max_length=20)
    native_trmt_frgnr_netprps: Optional[str] = Field(default=None, description="내국인대우외국인순매수", max_length=20)
    natn_netprps: Optional[str] = Field(default=None, description="국가순매수", max_length=20)
    samo_fund_netprps: Optional[str] = Field(default=None, description="사모펀드순매수", max_length=20)
    orgn_netprps: Optional[str] = Field(default=None, description="기관계순매수", max_length=20)


class DomesticSectorIndustryInvestorNetBuy(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="업종별투자자순매수요청 응답")

    inds_netprps: list[DomesticSectorIndustryInvestorNetBuyItem] = Field(
        default_factory=list, description="업종별 순매수 데이터"
    )


class DomesticSectorIndustryCurrentPriceItem(BaseModel):
    tm_n: str = Field(default="", description="시간n", max_length=20)
    cur_prc_n: str = Field(default="", description="현재가n", max_length=20)
    pred_pre_sig_n: str = Field(default="", description="전일대비기호n", max_length=20)
    pred_pre_n: str = Field(default="", description="전일대비n", max_length=20)
    flu_rt_n: str = Field(default="", description="등락률n", max_length=20)
    trde_qty_n: str = Field(default="", description="거래량n", max_length=20)
    acc_trde_qty_n: str = Field(default="", description="누적거래량n", max_length=20)


class DomesticSectorIndustryCurrentPrice(BaseModel, KiwoomHttpBody):
    cur_prc: str = Field(default="", description="현재가", max_length=20)
    pred_pre_sig: str = Field(default="", description="전일대비기호", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    flu_rt: str = Field(default="", description="등락률", max_length=20)
    trde_qty: str = Field(default="", description="거래량", max_length=20)
    trde_prica: str = Field(default="", description="거래대금", max_length=20)
    trde_frmatn_stk_num: str = Field(default="", description="거래형성종목수", max_length=20)
    trde_frmatn_rt: str = Field(default="", description="거래형성비율", max_length=20)
    open_pric: str = Field(default="", description="시가", max_length=20)
    high_pric: str = Field(default="", description="고가", max_length=20)
    low_pric: str = Field(default="", description="저가", max_length=20)
    upl: str = Field(default="", description="상한", max_length=20)
    rising: str = Field(default="", description="상승", max_length=20)
    stdns: str = Field(default="", description="보합", max_length=20)
    fall: str = Field(default="", description="하락", max_length=20)
    lst: str = Field(default="", description="하한", max_length=20)
    week52_hgst_pric: str = Field(default="", description="52주최고가", alias="52wk_hgst_pric", max_length=20)
    week52_hgst_pric_dt: str = Field(default="", description="52주최고가일", alias="52wk_hgst_pric_dt", max_length=20)
    week52_hgst_pric_pre_rt: str = Field(
        default="", description="52주최고가대비율", alias="52wk_hgst_pric_pre_rt", max_length=20
    )
    week52_lwst_pric: str = Field(default="", description="52주최저가", alias="52wk_lwst_pric", max_length=20)
    week52_lwst_pric_dt: str = Field(default="", description="52주최저가일", alias="52wk_lwst_pric_dt", max_length=20)
    week52_lwst_pric_pre_rt: str = Field(
        default="", description="52주최저가대비율", alias="52wk_lwst_pric_pre_rt", max_length=20
    )
    inds_cur_prc_tm: list[DomesticSectorIndustryCurrentPriceItem] = Field(
        default_factory=list, description="업종현재가_시간별"
    )


class DomesticSectorIndustryPriceBySectorItem(BaseModel):
    stk_cd: str = Field(default="", description="종목코드", max_length=20)
    stk_nm: str = Field(default="", description="종목명", max_length=40)
    cur_prc: str = Field(default="", description="현재가", max_length=20)
    pred_pre_sig: str = Field(default="", description="전일대비기호", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    flu_rt: str = Field(default="", description="등락률", max_length=20)
    now_trde_qty: str = Field(default="", description="현재거래량", max_length=20)
    sel_bid: str = Field(default="", description="매도호가", max_length=20)
    buy_bid: str = Field(default="", description="매수호가", max_length=20)
    open_pric: str = Field(default="", description="시가", max_length=20)
    high_pric: str = Field(default="", description="고가", max_length=20)
    low_pric: str = Field(default="", description="저가", max_length=20)


class DomesticSectorIndustryPriceBySector(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="업종별주가요청 응답")

    inds_stkpc: list[DomesticSectorIndustryPriceBySectorItem] = Field(default_factory=list, description="업종별주가")


class DomesticSectorAllIndustryIndexItem(BaseModel):
    stk_cd: str = Field(default="", description="종목코드", max_length=20)
    stk_nm: str = Field(default="", description="종목명", max_length=40)
    cur_prc: str = Field(default="", description="현재가", max_length=20)
    pre_sig: str = Field(default="", description="대비기호", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    flu_rt: str = Field(default="", description="등락률", max_length=20)
    trde_qty: str = Field(default="", description="거래량", max_length=20)
    wght: str = Field(default="", description="비중", max_length=20)
    trde_prica: str = Field(default="", description="거래대금", max_length=20)
    upl: str = Field(default="", description="상한", max_length=20)
    rising: str = Field(default="", description="상승", max_length=20)
    stdns: str = Field(default="", description="보합", max_length=20)
    fall: str = Field(default="", description="하락", max_length=20)
    lst: str = Field(default="", description="하한", max_length=20)
    flo_stk_num: str = Field(default="", description="상장종목수", max_length=20)


class DomesticSectorAllIndustryIndex(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="전업종지수요청 응답")

    all_inds_index: list[DomesticSectorAllIndustryIndexItem] = Field(
        default_factory=list, description="전업종지수 데이터"
    )


class DomesticSectorDailyIndustryCurrentPriceItem(BaseModel):
    dt_n: str = Field(default="", description="일자n", max_length=20)
    cur_prc_n: str = Field(default="", description="현재가n", max_length=20)
    pred_pre_sig_n: str = Field(default="", description="전일대비기호n", max_length=20)
    pred_pre_n: str = Field(default="", description="전일대비n", max_length=20)
    flu_rt_n: str = Field(default="", description="등락률n", max_length=20)
    acc_trde_qty_n: str = Field(default="", description="누적거래량n", max_length=20)


class DomesticSectorDailyIndustryCurrentPrice(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="업종현재가일별요청 응답")

    cur_prc: str = Field(default="", description="현재가", max_length=20)
    pred_pre_sig: str = Field(default="", description="전일대비기호", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    flu_rt: str = Field(default="", description="등락률", max_length=20)
    trde_qty: str = Field(default="", description="거래량", max_length=20)
    trde_prica: str = Field(default="", description="거래대금", max_length=20)
    trde_frmatn_stk_num: str = Field(default="", description="거래형성종목수", max_length=20)
    trde_frmatn_rt: str = Field(default="", description="거래형성비율", max_length=20)
    open_pric: str = Field(default="", description="시가", max_length=20)
    high_pric: str = Field(default="", description="고가", max_length=20)
    low_pric: str = Field(default="", description="저가", max_length=20)
    upl: str = Field(default="", description="상한", max_length=20)
    rising: str = Field(default="", description="상승", max_length=20)
    stdns: str = Field(default="", description="보합", max_length=20)
    fall: str = Field(default="", description="하락", max_length=20)
    lst: str = Field(default="", description="하한", max_length=20)
    week52_hgst_pric: str = Field(default="", description="52주최고가", alias="52wk_hgst_pric", max_length=20)
    week52_hgst_pric_dt: str = Field(default="", description="52주최고가일", alias="52wk_hgst_pric_dt", max_length=20)
    week52_hgst_pric_pre_rt: str = Field(
        default="", description="52주최고가대비율", alias="52wk_hgst_pric_pre_rt", max_length=20
    )
    week52_lwst_pric: str = Field(default="", description="52주최저가", alias="52wk_lwst_pric", max_length=20)
    week52_lwst_pric_dt: str = Field(default="", description="52주최저가일", alias="52wk_lwst_pric_dt", max_length=20)
    week52_lwst_pric_pre_rt: str = Field(
        default="", description="52주최저가대비율", alias="52wk_lwst_pric_pre_rt", max_length=20
    )
    inds_cur_prc_daly_rept: list[DomesticSectorDailyIndustryCurrentPriceItem] = Field(
        default_factory=list, description="업종현재가_일별반복"
    )
