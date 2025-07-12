from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

from cluefin_openapi.kiwoom._model import (
    KiwoomHttpBody,
)


class DomesticMarketConditionStockQuote(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="주식호가요청")

    bid_req_base_tm: str = Field(default="", description="호가잔량기준시간", max_length=20)
    sel_10th_pre_req_pre: str = Field(default="", description="매도10차선잔량대비", max_length=20)
    sel_10th_pre_req: str = Field(default="", description="매도10차선잔량", max_length=20)
    sel_10th_pre_bid: str = Field(default="", description="매도10차선호가", max_length=20)
    sel_9th_pre_req_pre: str = Field(default="", description="매도9차선잔량대비", max_length=20)
    sel_9th_pre_req: str = Field(default="", description="매도9차선잔량", max_length=20)
    sel_9th_pre_bid: str = Field(default="", description="매도9차선호가", max_length=20)
    sel_8th_pre_req_pre: str = Field(default="", description="매도8차선잔량대비", max_length=20)
    sel_8th_pre_req: str = Field(default="", description="매도8차선잔량", max_length=20)
    sel_8th_pre_bid: str = Field(default="", description="매도8차선호가", max_length=20)
    sel_7th_pre_req_pre: str = Field(default="", description="매도7차선잔량대비", max_length=20)
    sel_7th_pre_req: str = Field(default="", description="매도7차선잔량", max_length=20)
    sel_7th_pre_bid: str = Field(default="", description="매도7차선호가", max_length=20)
    sel_6th_pre_req_pre: str = Field(default="", description="매도6차선잔량대비", max_length=20)
    sel_6th_pre_req: str = Field(default="", description="매도6차선잔량", max_length=20)
    sel_6th_pre_bid: str = Field(default="", description="매도6차선호가", max_length=20)
    sel_5th_pre_req_pre: str = Field(default="", description="매도5차선잔량대비", max_length=20)
    sel_5th_pre_req: str = Field(default="", description="매도5차선잔량", max_length=20)
    sel_5th_pre_bid: str = Field(default="", description="매도5차선호가", max_length=20)
    sel_4th_pre_req_pre: str = Field(default="", description="매도4차선잔량대비", max_length=20)
    sel_4th_pre_req: str = Field(default="", description="매도4차선잔량", max_length=20)
    sel_4th_pre_bid: str = Field(default="", description="매도4차선호가", max_length=20)
    sel_3th_pre_req_pre: str = Field(default="", description="매도3차선잔량대비", max_length=20)
    sel_3th_pre_req: str = Field(default="", description="매도3차선잔량", max_length=20)
    sel_3th_pre_bid: str = Field(default="", description="매도3차선호가", max_length=20)
    sel_2th_pre_req_pre: str = Field(default="", description="매도2차선잔량대비", max_length=20)
    sel_2th_pre_req: str = Field(default="", description="매도2차선잔량", max_length=20)
    sel_2th_pre_bid: str = Field(default="", description="매도2차선호가", max_length=20)
    sel_1th_pre_req_pre: str = Field(default="", description="매도1차선잔량대비", max_length=20)
    sel_fpr_req: str = Field(default="", description="매도최우선잔량", max_length=20)
    sel_fpr_bid: str = Field(default="", description="매도최우선호가", max_length=20)
    buy_fpr_bid: str = Field(default="", description="매수최우선호가", max_length=20)
    buy_fpr_req: str = Field(default="", description="매수최우선잔량", max_length=20)
    buy_1th_pre_req_pre: str = Field(default="", description="매수1차선잔량대비", max_length=20)
    buy_2th_pre_bid: str = Field(default="", description="매수2차선호가", max_length=20)
    buy_2th_pre_req: str = Field(default="", description="매수2차선잔량", max_length=20)
    buy_2th_pre_req_pre: str = Field(default="", description="매수2차선잔량대비", max_length=20)
    buy_3th_pre_bid: str = Field(default="", description="매수3차선호가", max_length=20)
    buy_3th_pre_req: str = Field(default="", description="매수3차선잔량", max_length=20)
    buy_3th_pre_req_pre: str = Field(default="", description="매수3차선잔량대비", max_length=20)
    buy_4th_pre_bid: str = Field(default="", description="매수4차선호가", max_length=20)
    buy_4th_pre_req: str = Field(default="", description="매수4차선잔량", max_length=20)
    buy_4th_pre_req_pre: str = Field(default="", description="매수4차선잔량대비", max_length=20)
    buy_5th_pre_bid: str = Field(default="", description="매수5차선호가", max_length=20)
    buy_5th_pre_req: str = Field(default="", description="매수5차선잔량", max_length=20)
    buy_5th_pre_req_pre: str = Field(default="", description="매수5차선잔량대비", max_length=20)
    buy_6th_pre_bid: str = Field(default="", description="매수6차선호가", max_length=20)
    buy_6th_pre_req: str = Field(default="", description="매수6차선잔량", max_length=20)
    buy_6th_pre_req_pre: str = Field(default="", description="매수6차선잔량대비", max_length=20)
    buy_7th_pre_bid: str = Field(default="", description="매수7차선호가", max_length=20)
    buy_7th_pre_req: str = Field(default="", description="매수7차선잔량", max_length=20)
    buy_7th_pre_req_pre: str = Field(default="", description="매수7차선잔량대비", max_length=20)
    buy_8th_pre_bid: str = Field(default="", description="매수8차선호가", max_length=20)
    buy_8th_pre_req: str = Field(default="", description="매수8차선잔량", max_length=20)
    buy_8th_pre_req_pre: str = Field(default="", description="매수8차선잔량대비", max_length=20)
    buy_9th_pre_bid: str = Field(default="", description="매수9차선호가", max_length=20)
    buy_9th_pre_req: str = Field(default="", description="매수9차선잔량", max_length=20)
    buy_9th_pre_req_pre: str = Field(default="", description="매수9차선잔량대비", max_length=20)
    buy_10th_pre_bid: str = Field(default="", description="매수10차선호가", max_length=20)
    buy_10th_pre_req: str = Field(default="", description="매수10차선잔량", max_length=20)
    buy_10th_pre_req_pre: str = Field(default="", description="매수10차선잔량대비", max_length=20)
    tot_sel_req_jub_pre: str = Field(default="", description="총매도잔량직전대비", max_length=20)
    tot_sel_req: str = Field(default="", description="총매도잔량", max_length=20)
    tot_buy_req: str = Field(default="", description="총매수잔량", max_length=20)
    tot_buy_req_jub_pre: str = Field(default="", description="총매수잔량직전대비", max_length=20)
    ovt_sel_req_pre: str = Field(default="", description="시간외매도잔량대비", max_length=20)
    ovt_sel_req: str = Field(default="", description="시간외매도잔량", max_length=20)
    ovt_buy_req: str = Field(default="", description="시간외매수잔량", max_length=20)
    ovt_buy_req_pre: str = Field(default="", description="시간외매수잔량대비", max_length=20)


class DomesticMarketConditionStockQuoteByDateItem(BaseModel):
    date: str = Field(default="", description="날짜", max_length=20)
    open_pric: str = Field(default="", description="시가", max_length=20)
    high_pric: str = Field(default="", description="고가", max_length=20)
    low_pric: str = Field(default="", description="저가", max_length=20)
    close_pric: str = Field(default="", description="종가", max_length=20)
    pre: str = Field(default="", description="대비", max_length=20)
    flu_rt: str = Field(default="", description="등락률", max_length=20)
    trde_qty: str = Field(default="", description="거래량", max_length=20)
    trde_prica: str = Field(default="", description="거래대금", max_length=20)
    for_poss: str = Field(default="", description="외인보유", max_length=20)
    for_wght: str = Field(default="", description="외인비중", max_length=20)
    for_netprps: str = Field(default="", description="외인순매수", max_length=20)
    orgn_netprps: str = Field(default="", description="기관순매수", max_length=20)
    ind_netprps: str = Field(default="", description="개인순매수", max_length=20)
    crd_remn_rt: str = Field(default="", description="신용잔고율", max_length=20)
    frgn: str = Field(default="", description="외국계", max_length=20)
    prm: str = Field(default="", description="프로그램", max_length=20)


class DomesticMarketConditionStockQuoteByDate(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="주식일자별호가요청")

    stk_ddwkmm: list[DomesticMarketConditionStockQuoteByDateItem] = Field(
        default_factory=list, description="주식일주월시분"
    )


class DomesticMarketConditionStockPrice(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="주식시세요청")

    date: str = Field(default="", description="날짜", max_length=20)
    open_pric: str = Field(default="", description="시가", max_length=20)
    high_pric: str = Field(default="", description="고가", max_length=20)
    low_pric: str = Field(default="", description="저가", max_length=20)
    close_pric: str = Field(default="", description="종가", max_length=20)
    pre: str = Field(default="", description="대비", max_length=20)
    flu_rt: str = Field(default="", description="등락률", max_length=20)
    trde_qty: str = Field(default="", description="거래량", max_length=20)
    trde_prica: str = Field(default="", description="거래대금", max_length=20)
    cntr_str: str = Field(default="", description="체결강도", max_length=20)


class DomesticMarketConditionMarketSentimentInfo(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="시세표정보요청")

    stk_nm: str = Field(default="", description="종목명", max_length=40)
    stk_cd: str = Field(default="", description="종목코드", max_length=6)
    date: str = Field(default="", description="날짜", max_length=20)
    tm: str = Field(default="", description="시간", max_length=20)
    pred_close_pric: str = Field(default="", description="전일종가", max_length=20)
    pred_trde_qty: str = Field(default="", description="전일거래량", max_length=20)
    upl_pric: str = Field(default="", description="상한가", max_length=20)
    lst_pric: str = Field(default="", description="하한가", max_length=20)
    pred_trde_prica: str = Field(default="", description="전일거래대금", max_length=20)
    flo_stkcnt: str = Field(default="", description="상장주식수", max_length=20)
    cur_prc: str = Field(default="", description="현재가", max_length=20)
    smbol: str = Field(default="", description="부호", max_length=20)
    flu_rt: str = Field(default="", description="등락률", max_length=20)
    pred_rt: str = Field(default="", description="전일비", max_length=20)
    open_pric: str = Field(default="", description="시가", max_length=20)
    high_pric: str = Field(default="", description="고가", max_length=20)
    low_pric: str = Field(default="", description="저가", max_length=20)
    cntr_qty: str = Field(default="", description="체결량", max_length=20)
    trde_qty: str = Field(default="", description="거래량", max_length=20)
    trde_prica: str = Field(default="", description="거래대금", max_length=20)
    exp_cntr_pric: str = Field(default="", description="예상체결가", max_length=20)
    exp_cntr_qty: str = Field(default="", description="예상체결량", max_length=20)
    exp_sel_pri_bid: str = Field(default="", description="예상매도우선호가", max_length=20)
    exp_buy_pri_bid: str = Field(default="", description="예상매수우선호가", max_length=20)
    trde_strt_dt: str = Field(default="", description="거래시작일", max_length=20)
    exec_pric: str = Field(default="", description="행사가격", max_length=20)
    hgst_pric: str = Field(default="", description="최고가", max_length=20)
    lwst_pric: str = Field(default="", description="최저가", max_length=20)
    hgst_pric_dt: str = Field(default="", description="최고가일", max_length=20)
    lwst_pric_dt: str = Field(default="", description="최저가일", max_length=20)
    sel_1bid: str = Field(default="", description="매도1호가", max_length=20)
    sel_2bid: str = Field(default="", description="매도2호가", max_length=20)
    sel_3bid: str = Field(default="", description="매도3호가", max_length=20)
    sel_4bid: str = Field(default="", description="매도4호가", max_length=20)
    sel_5bid: str = Field(default="", description="매도5호가", max_length=20)
    sel_6bid: str = Field(default="", description="매도6호가", max_length=20)
    sel_7bid: str = Field(default="", description="매도7호가", max_length=20)
    sel_8bid: str = Field(default="", description="매도8호가", max_length=20)
    sel_9bid: str = Field(default="", description="매도9호가", max_length=20)
    sel_10bid: str = Field(default="", description="매도10호가", max_length=20)
    buy_1bid: str = Field(default="", description="매수1호가", max_length=20)
    buy_2bid: str = Field(default="", description="매수2호가", max_length=20)
    buy_3bid: str = Field(default="", description="매수3호가", max_length=20)
    buy_4bid: str = Field(default="", description="매수4호가", max_length=20)
    buy_5bid: str = Field(default="", description="매수5호가", max_length=20)
    buy_6bid: str = Field(default="", description="매수6호가", max_length=20)
    buy_7bid: str = Field(default="", description="매수7호가", max_length=20)
    buy_8bid: str = Field(default="", description="매수8호가", max_length=20)
    buy_9bid: str = Field(default="", description="매수9호가", max_length=20)
    buy_10bid: str = Field(default="", description="매수10호가", max_length=20)
    sel_1bid_req: str = Field(default="", description="매도1호가잔량", max_length=20)
    sel_2bid_req: str = Field(default="", description="매도2호가잔량", max_length=20)
    sel_3bid_req: str = Field(default="", description="매도3호가잔량", max_length=20)
    sel_4bid_req: str = Field(default="", description="매도4호가잔량", max_length=20)
    sel_5bid_req: str = Field(default="", description="매도5호가잔량", max_length=20)
    sel_6bid_req: str = Field(default="", description="매도6호가잔량", max_length=20)
    sel_7bid_req: str = Field(default="", description="매도7호가잔량", max_length=20)
    sel_8bid_req: str = Field(default="", description="매도8호가잔량", max_length=20)
    sel_9bid_req: str = Field(default="", description="매도9호가잔량", max_length=20)
    sel_10bid_req: str = Field(default="", description="매도10호가잔량", max_length=20)
    buy_1bid_req: str = Field(default="", description="매수1호가잔량", max_length=20)
    buy_2bid_req: str = Field(default="", description="매수2호가잔량", max_length=20)
    buy_3bid_req: str = Field(default="", description="매수3호가잔량", max_length=20)
    buy_4bid_req: str = Field(default="", description="매수4호가잔량", max_length=20)
    buy_5bid_req: str = Field(default="", description="매수5호가잔량", max_length=20)
    buy_6bid_req: str = Field(default="", description="매수6호가잔량", max_length=20)
    buy_7bid_req: str = Field(default="", description="매수7호가잔량", max_length=20)
    buy_8bid_req: str = Field(default="", description="매수8호가잔량", max_length=20)
    buy_9bid_req: str = Field(default="", description="매수9호가잔량", max_length=20)
    buy_10bid_req: str = Field(default="", description="매수10호가잔량", max_length=20)
    sel_1bid_jub_pre: str = Field(default="", description="매도1호가직전대비", max_length=20)
    sel_2bid_jub_pre: str = Field(default="", description="매도2호가직전대비", max_length=20)
    sel_3bid_jub_pre: str = Field(default="", description="매도3호가직전대비", max_length=20)
    sel_4bid_jub_pre: str = Field(default="", description="매도4호가직전대비", max_length=20)
    sel_5bid_jub_pre: str = Field(default="", description="매도5호가직전대비", max_length=20)
    sel_6bid_jub_pre: str = Field(default="", description="매도6호가직전대비", max_length=20)
    sel_7bid_jub_pre: str = Field(default="", description="매도7호가직전대비", max_length=20)
    sel_8bid_jub_pre: str = Field(default="", description="매도8호가직전대비", max_length=20)
    sel_9bid_jub_pre: str = Field(default="", description="매도9호가직전대비", max_length=20)
    sel_10bid_jub_pre: str = Field(default="", description="매도10호가직전대비", max_length=20)
    buy_1bid_jub_pre: str = Field(default="", description="매수1호가직전대비", max_length=20)
    buy_2bid_jub_pre: str = Field(default="", description="매수2호가직전대비", max_length=20)
    buy_3bid_jub_pre: str = Field(default="", description="매수3호가직전대비", max_length=20)
    buy_4bid_jub_pre: str = Field(default="", description="매수4호가직전대비", max_length=20)
    buy_5bid_jub_pre: str = Field(default="", description="매수5호가직전대비", max_length=20)
    buy_6bid_jub_pre: str = Field(default="", description="매수6호가직전대비", max_length=20)
    buy_7bid_jub_pre: str = Field(default="", description="매수7호가직전대비", max_length=20)
    buy_8bid_jub_pre: str = Field(default="", description="매수8호가직전대비", max_length=20)
    buy_9bid_jub_pre: str = Field(default="", description="매수9호가직전대비", max_length=20)
    buy_10bid_jub_pre: str = Field(default="", description="매수10호가직전대비", max_length=20)
    sel_1bid_cnt: str = Field(default="", description="매도1호가건수", max_length=20)
    sel_2bid_cnt: str = Field(default="", description="매도2호가건수", max_length=20)
    sel_3bid_cnt: str = Field(default="", description="매도3호가건수", max_length=20)
    sel_4bid_cnt: str = Field(default="", description="매도4호가건수", max_length=20)
    sel_5bid_cnt: str = Field(default="", description="매도5호가건수", max_length=20)
    buy_1bid_cnt: str = Field(default="", description="매수1호가건수", max_length=20)
    buy_2bid_cnt: str = Field(default="", description="매수2호가건수", max_length=20)
    buy_3bid_cnt: str = Field(default="", description="매수3호가건수", max_length=20)
    buy_4bid_cnt: str = Field(default="", description="매수4호가건수", max_length=20)
    buy_5bid_cnt: str = Field(default="", description="매수5호가건수", max_length=20)
    lpsel_1bid_req: str = Field(default="", description="LP매도1호가잔량", max_length=20)
    lpsel_2bid_req: str = Field(default="", description="LP매도2호가잔량", max_length=20)
    lpsel_3bid_req: str = Field(default="", description="LP매도3호가잔량", max_length=20)
    lpsel_4bid_req: str = Field(default="", description="LP매도4호가잔량", max_length=20)
    lpsel_5bid_req: str = Field(default="", description="LP매도5호가잔량", max_length=20)
    lpsel_6bid_req: str = Field(default="", description="LP매도6호가잔량", max_length=20)
    lpsel_7bid_req: str = Field(default="", description="LP매도7호가잔량", max_length=20)
    lpsel_8bid_req: str = Field(default="", description="LP매도8호가잔량", max_length=20)
    lpsel_9bid_req: str = Field(default="", description="LP매도9호가잔량", max_length=20)
    lpsel_10bid_req: str = Field(default="", description="LP매도10호가잔량", max_length=20)
    lpbuy_1bid_req: str = Field(default="", description="LP매수1호가잔량", max_length=20)
    lpbuy_2bid_req: str = Field(default="", description="LP매수2호가잔량", max_length=20)
    lpbuy_3bid_req: str = Field(default="", description="LP매수3호가잔량", max_length=20)
    lpbuy_4bid_req: str = Field(default="", description="LP매수4호가잔량", max_length=20)
    lpbuy_5bid_req: str = Field(default="", description="LP매수5호가잔량", max_length=20)
    lpbuy_6bid_req: str = Field(default="", description="LP매수6호가잔량", max_length=20)
    lpbuy_7bid_req: str = Field(default="", description="LP매수7호가잔량", max_length=20)
    lpbuy_8bid_req: str = Field(default="", description="LP매수8호가잔량", max_length=20)
    lpbuy_9bid_req: str = Field(default="", description="LP매수9호가잔량", max_length=20)
    lpbuy_10bid_req: str = Field(default="", description="LP매수10호가잔량", max_length=20)
    tot_buy_req: str = Field(default="", description="총매수잔량", max_length=20)
    tot_sel_req: str = Field(default="", description="총매도잔량", max_length=20)
    tot_buy_cnt: str = Field(default="", description="총매수건수", max_length=20)
    tot_sel_cnt: str = Field(default="", description="총매도건수", max_length=20)


class DomesticMarketConditionNewStockWarrantPriceItem(BaseModel):
    stk_cd: str = Field(default="", description="종목코드", max_length=20)
    stk_nm: str = Field(default="", description="종목명", max_length=40)
    cur_prc: str = Field(default="", description="현재가", max_length=20)
    pred_pre_sig: str = Field(default="", description="전일대비기호", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    flu_rt: str = Field(default="", description="등락율", max_length=20)
    fpr_sel_bid: str = Field(default="", description="최우선매도호가", max_length=20)
    fpr_buy_bid: str = Field(default="", description="최우선매수호가", max_length=20)
    acc_trde_qty: str = Field(default="", description="누적거래량", max_length=20)
    open_pric: str = Field(default="", description="시가", max_length=20)
    high_pric: str = Field(default="", description="고가", max_length=20)
    low_pric: str = Field(default="", description="저가", max_length=20)


class DomesticMarketConditionNewStockWarrantPrice(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="신주인수권시세요청")

    newstk_recvrht_mrpr: list[DomesticMarketConditionNewStockWarrantPriceItem] = Field(
        default_factory=list, description="신주인수권시세"
    )


class DomesticMarketConditionDailyInstitutionalTradingItem(BaseModel):
    stk_cd: str = Field(default="", description="종목코드", max_length=20)
    stk_nm: str = Field(default="", description="종목명", max_length=40)
    netprps_qty: str = Field(default="", description="순매수수량", max_length=20)
    netprps_amt: str = Field(default="", description="순매수금액", max_length=20)


class DomesticMarketConditionDailyInstitutionalTrading(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="기관일자별매매요청")

    daly_orgn_trde_stk: list[DomesticMarketConditionDailyInstitutionalTradingItem] = Field(
        default_factory=list, description="일별기관매매종목"
    )


class DomesticMarketConditionInstitutionalTradingTrendByStockItem(BaseModel):
    dt: str = Field(default="", description="일자", max_length=20)
    close_pric: str = Field(default="", description="종가", max_length=20)
    pre_sig: str = Field(default="", description="대비기호", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    flu_rt: str = Field(default="", description="등락율", max_length=20)
    trde_qty: str = Field(default="", description="거래량", max_length=20)
    orgn_dt_acc: str = Field(default="", description="기관기간누적", max_length=20)
    orgn_daly_nettrde_qty: str = Field(default="", description="기관일별순매매수량", max_length=20)
    for_dt_acc: str = Field(default="", description="외인기간누적", max_length=20)
    for_daly_nettrde_qty: str = Field(default="", description="외인일별순매매수량", max_length=20)
    limit_exh_rt: str = Field(default="", description="한도소진율", max_length=20)


class DomesticMarketConditionInstitutionalTradingTrendByStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="종목별기관매매추세요청")

    orgn_prsm_avg_pric: str = Field(default="", description="기관추정평균가", max_length=20)
    for_prsm_avg_pric: str = Field(default="", description="외인추정평균가", max_length=20)
    stk_orgn_trde_trnsn: list[DomesticMarketConditionInstitutionalTradingTrendByStockItem] = Field(
        default_factory=list, description="종목별기관매매추이"
    )


class DomesticMarketConditionExecutionIntensityTrendByTimeItem(BaseModel):
    cntr_tm: str = Field(default="", description="체결시간", max_length=20)
    cur_prc: str = Field(default="", description="현재가", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    pred_pre_sig: str = Field(default="", description="전일대비기호", max_length=20)
    flu_rt: str = Field(default="", description="등락율", max_length=20)
    trde_qty: str = Field(default="", description="거래량", max_length=20)
    acc_trde_prica: str = Field(default="", description="누적거래대금", max_length=20)
    acc_trde_qty: str = Field(default="", description="누적거래량", max_length=20)
    cntr_str: str = Field(default="", description="체결강도", max_length=20)
    cntr_str_5min: str = Field(default="", description="체결강도5분", max_length=20)
    cntr_str_20min: str = Field(default="", description="체결강도20분", max_length=20)
    cntr_str_60min: str = Field(default="", description="체결강도60분", max_length=20)
    stex_tp: str = Field(default="", description="거래소구분", max_length=20)


class DomesticMarketConditionExecutionIntensityTrendByTime(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="체결강도추이시간별요청")

    cntr_str_tm: list[DomesticMarketConditionExecutionIntensityTrendByTimeItem] = Field(
        default_factory=list, description="체결강도시간별"
    )


class DomesticMarketConditionExecutionIntensityTrendByDateItem(BaseModel):
    dt: str = Field(default="", description="일자", max_length=20)
    cur_prc: str = Field(default="", description="현재가", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    pred_pre_sig: str = Field(default="", description="전일대비기호", max_length=20)
    flu_rt: str = Field(default="", description="등락율", max_length=20)
    trde_qty: str = Field(default="", description="거래량", max_length=20)
    acc_trde_prica: str = Field(default="", description="누적거래대금", max_length=20)
    acc_trde_qty: str = Field(default="", description="누적거래량", max_length=20)
    cntr_str: str = Field(default="", description="체결강도", max_length=20)
    cntr_str_5min: str = Field(default="", description="체결강도5분", max_length=20)
    cntr_str_20min: str = Field(default="", description="체결강도20분", max_length=20)
    cntr_str_60min: str = Field(default="", description="체결강도60분", max_length=20)


class DomesticMarketConditionExecutionIntensityTrendByDate(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="체결강도추이일별요청")

    cntr_str_daly: list[DomesticMarketConditionExecutionIntensityTrendByDateItem] = Field(
        default_factory=list, description="체결강도일별"
    )


class DomesticMarketConditionIntradayTradingByInvestorItem(BaseModel):
    stk_cd: str = Field(default="", description="종목코드", max_length=20)
    stk_nm: str = Field(default="", description="종목명", max_length=40)
    cur_prc: str = Field(default="", description="현재가", max_length=20)
    pre_sig: str = Field(default="", description="대비기호", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    flu_rt: str = Field(default="", description="등락율", max_length=20)
    acc_trde_qty: str = Field(default="", description="누적거래량", max_length=20)
    netprps_qty: str = Field(default="", description="순매수수량", max_length=20)
    prev_pot_netprps_qty: str = Field(default="", description="이전시점순매수수량", max_length=20)
    netprps_irds: str = Field(default="", description="순매수증감", max_length=20)
    buy_qty: str = Field(default="", description="매수수량", max_length=20)
    buy_qty_irds: str = Field(default="", description="매수수량증감", max_length=20)
    sell_qty: str = Field(default="", description="매도수량", max_length=20)
    sell_qty_irds: str = Field(default="", description="매도수량증감", max_length=20)


class DomesticMarketConditionIntradayTradingByInvestor(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="장중투자자별매매요청")

    opmr_invsr_trde: list[DomesticMarketConditionIntradayTradingByInvestorItem] = Field(
        default_factory=list, description="장중투자자별매매"
    )


class DomesticMarketConditionAfterMarketTradingByInvestorItem(BaseModel):
    stk_cd: str = Field(default="", description="종목코드", max_length=20)
    stk_nm: str = Field(default="", description="종목명", max_length=40)
    cur_prc: str = Field(default="", description="현재가", max_length=20)
    pre_sig: str = Field(default="", description="대비기호", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    flu_rt: str = Field(default="", description="등락율", max_length=20)
    trde_qty: str = Field(default="", description="거래량", max_length=20)
    ind_invsr: str = Field(default="", description="개인투자자", max_length=20)
    frgnr_invsr: str = Field(default="", description="외국인투자자", max_length=20)
    orgn: str = Field(default="", description="기관계", max_length=20)
    fnnc_invt: str = Field(default="", description="금융투자", max_length=20)
    insrnc: str = Field(default="", description="보험", max_length=20)
    invtrt: str = Field(default="", description="투신", max_length=20)
    etc_fnnc: str = Field(default="", description="기타금융", max_length=20)
    bank: str = Field(default="", description="은행", max_length=20)
    penfnd_etc: str = Field(default="", description="연기금등", max_length=20)
    samo_fund: str = Field(default="", description="사모펀드", max_length=20)
    natn: str = Field(default="", description="국가", max_length=20)
    etc_corp: str = Field(default="", description="기타법인", max_length=20)


class DomesticMarketConditionAfterMarketTradingByInvestor(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="장마감후투자자별매매요청")

    opaf_invsr_trde: list[DomesticMarketConditionAfterMarketTradingByInvestorItem] = Field(
        default_factory=list, description="장마감후투자자별매매"
    )


class DomesticMarketConditionSecuritiesFirmTradingTrendByStockItem(BaseModel):
    dt: str = Field(default="", description="일자", max_length=20)
    cur_prc: str = Field(default="", description="현재가", max_length=20)
    pre_sig: str = Field(default="", description="대비기호", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    flu_rt: str = Field(default="", description="등락율", max_length=20)
    acc_trde_qty: str = Field(default="", description="누적거래량", max_length=20)
    netprps_qty: str = Field(default="", description="순매수수량", max_length=20)
    buy_qty: str = Field(default="", description="매수수량", max_length=20)
    sell_qty: str = Field(default="", description="매도수량", max_length=20)


class DomesticMarketConditionSecuritiesFirmTradingTrendByStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="증권사별종목매매향요청")

    sec_stk_trde_trend: list[DomesticMarketConditionSecuritiesFirmTradingTrendByStockItem] = Field(
        default_factory=list, description="증권사별종목매매향"
    )


class DomesticMarketConditionDailyStockPriceItem(BaseModel):
    date: str = Field(default="", description="날짜", max_length=20)
    open_pric: str = Field(default="", description="시가", max_length=20)
    high_pric: str = Field(default="", description="고가", max_length=20)
    low_pric: str = Field(default="", description="저가", max_length=20)
    close_pric: str = Field(default="", description="종가", max_length=20)
    pred_rt: str = Field(default="", description="전일비", max_length=20)
    flu_rt: str = Field(default="", description="등락률", max_length=20)
    trde_qty: str = Field(default="", description="거래량", max_length=20)
    amt_mn: str = Field(default="", description="금액(백만)", max_length=20)
    crd_rt: str = Field(default="", description="신용비율", max_length=20)
    ind: str = Field(default="", description="개인순매수", max_length=20)
    orgn: str = Field(default="", description="기관순매수", max_length=20)
    for_qty: str = Field(default="", description="외인수량", max_length=20)
    frgn: str = Field(default="", description="외국계순매수", max_length=20)
    prm: str = Field(default="", description="프로그램순매수", max_length=20)
    for_rt: str = Field(default="", description="외인비율", max_length=20)
    for_poss: str = Field(default="", description="외인보유주식수", max_length=20)
    for_wght: str = Field(default="", description="외인비중", max_length=20)
    for_netprps: str = Field(default="", description="외인순매수금액", max_length=20)
    orgn_netprps: str = Field(default="", description="기관순매수금액", max_length=20)
    ind_netprps: str = Field(default="", description="개인순매수금액", max_length=20)
    crd_remn_rt: str = Field(default="", description="신용잔고율", max_length=20)


class DomesticMarketConditionDailyStockPrice(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="일별주가요청")

    daly_stkpc: list[DomesticMarketConditionDailyStockPriceItem] = Field(default_factory=list, description="일별주가")


class DomesticMarketConditionAfterHoursSinglePrice(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="시간외단일가요청")

    ovt_sigpric_sel_bid_jub_pre_5: str = Field(default="", description="시간외단일가_매도호가직전대비5", max_length=20)
    ovt_sigpric_sel_bid_jub_pre_4: str = Field(default="", description="시간외단일가_매도호가직전대비4", max_length=20)
    ovt_sigpric_sel_bid_jub_pre_3: str = Field(default="", description="시간외단일가_매도호가직전대비3", max_length=20)
    ovt_sigpric_sel_bid_jub_pre_2: str = Field(default="", description="시간외단일가_매도호가직전대비2", max_length=20)
    ovt_sigpric_sel_bid_jub_pre_1: str = Field(default="", description="시간외단일가_매도호가직전대비1", max_length=20)
    ovt_sigpric_sel_bid_qty_5: str = Field(default="", description="시간외단일가_매도호가수량5", max_length=20)
    ovt_sigpric_sel_bid_qty_4: str = Field(default="", description="시간외단일가_매도호가수량4", max_length=20)
    ovt_sigpric_sel_bid_qty_3: str = Field(default="", description="시간외단일가_매도호가수량3", max_length=20)
    ovt_sigpric_sel_bid_qty_2: str = Field(default="", description="시간외단일가_매도호가수량2", max_length=20)
    ovt_sigpric_sel_bid_qty_1: str = Field(default="", description="시간외단일가_매도호가수량1", max_length=20)
    ovt_sigpric_sel_bid_5: str = Field(default="", description="시간외단일가_매도호가5", max_length=20)
    ovt_sigpric_sel_bid_4: str = Field(default="", description="시간외단일가_매도호가4", max_length=20)
    ovt_sigpric_sel_bid_3: str = Field(default="", description="시간외단일가_매도호가3", max_length=20)
    ovt_sigpric_sel_bid_2: str = Field(default="", description="시간외단일가_매도호가2", max_length=20)
    ovt_sigpric_sel_bid_1: str = Field(default="", description="시간외단일가_매도호가1", max_length=20)
    ovt_sigpric_buy_bid_1: str = Field(default="", description="시간외단일가_매수호가1", max_length=20)
    ovt_sigpric_buy_bid_2: str = Field(default="", description="시간외단일가_매수호가2", max_length=20)
    ovt_sigpric_buy_bid_3: str = Field(default="", description="시간외단일가_매수호가3", max_length=20)
    ovt_sigpric_buy_bid_4: str = Field(default="", description="시간외단일가_매수호가4", max_length=20)
    ovt_sigpric_buy_bid_5: str = Field(default="", description="시간외단일가_매수호가5", max_length=20)
    ovt_sigpric_buy_bid_qty_1: str = Field(default="", description="시간외단일가_매수호가수량1", max_length=20)
    ovt_sigpric_buy_bid_qty_2: str = Field(default="", description="시간외단일가_매수호가수량2", max_length=20)
    ovt_sigpric_buy_bid_qty_3: str = Field(default="", description="시간외단일가_매수호가수량3", max_length=20)
    ovt_sigpric_buy_bid_qty_4: str = Field(default="", description="시간외단일가_매수호가수량4", max_length=20)
    ovt_sigpric_buy_bid_qty_5: str = Field(default="", description="시간외단일가_매수호가수량5", max_length=20)
    ovt_sigpric_buy_bid_jub_pre_1: str = Field(default="", description="시간외단일가_매수호가직전대비1", max_length=20)
    ovt_sigpric_buy_bid_jub_pre_2: str = Field(default="", description="시간외단일가_매수호가직전대비2", max_length=20)
    ovt_sigpric_buy_bid_jub_pre_3: str = Field(default="", description="시간외단일가_매수호가직전대비3", max_length=20)
    ovt_sigpric_buy_bid_jub_pre_4: str = Field(default="", description="시간외단일가_매수호가직전대비4", max_length=20)
    ovt_sigpric_buy_bid_jub_pre_5: str = Field(default="", description="시간외단일가_매수호가직전대비5", max_length=20)
    ovt_sigpric_sel_bid_tot_req: str = Field(default="", description="시간외단일가_매도호가총잔량", max_length=20)
    ovt_sigpric_buy_bid_tot_req: str = Field(default="", description="시간외단일가_매수호가총잔량", max_length=20)
    sel_bid_tot_req_jub_pre: str = Field(default="", description="매도호가총잔량직전대비", max_length=20)
    sel_bid_tot_req: str = Field(default="", description="매도호가총잔량", max_length=20)
    buy_bid_tot_req: str = Field(default="", description="매수호가총잔량", max_length=20)
    buy_bid_tot_req_jub_pre: str = Field(default="", description="매수호가총잔량직전대비", max_length=20)
    ovt_sel_bid_tot_req_jub_pre: str = Field(default="", description="시간외매도호가총잔량직전대비", max_length=20)
    ovt_sel_bid_tot_req: str = Field(default="", description="시간외매도호가총잔량", max_length=20)
    ovt_buy_bid_tot_req: str = Field(default="", description="시간외매수호가총잔량", max_length=20)
    ovt_buy_bid_tot_req_jub_pre: str = Field(default="", description="시간외매수호가총잔량직전대비", max_length=20)
    ovt_sigpric_cur_prc: str = Field(default="", description="시간외단일가_현재가", max_length=20)
    ovt_sigpric_pred_pre_sig: str = Field(default="", description="시간외단일가_전일대비기호", max_length=20)
    ovt_sigpric_pred_pre: str = Field(default="", description="시간외단일가_전일대비", max_length=20)
    ovt_sigpric_flu_rt: str = Field(default="", description="시간외단일가_등락률", max_length=20)
    ovt_sigpric_acc_trde_qty: str = Field(default="", description="시간외단일가_누적거래량", max_length=20)
    bid_req_base_tm: str = Field(default="", description="호가잔량기준시간", max_length=20)


class DomesticMarketConditionProgramTradingTrendByTimeItem(BaseModel):
    cntr_tm: str = Field(default="", description="체결시간", max_length=20)
    dfrt_trde_sel: str = Field(default="", description="차익거래매도", max_length=20)
    dfrt_trde_buy: str = Field(default="", description="차익거래매수", max_length=20)
    dfrt_trde_netprps: str = Field(default="", description="차익거래순매수", max_length=20)
    ndiffpro_trde_sel: str = Field(default="", description="비차익거래매도", max_length=20)
    ndiffpro_trde_buy: str = Field(default="", description="비차익거래매수", max_length=20)
    ndiffpro_trde_netprps: str = Field(default="", description="비차익거래순매수", max_length=20)
    dfrt_trde_sell_qty: str = Field(default="", description="차익거래매도수량", max_length=20)
    dfrt_trde_buy_qty: str = Field(default="", description="차익거래매수수량", max_length=20)
    dfrt_trde_netprps_qty: str = Field(default="", description="차익거래순매수수량", max_length=20)
    ndiffpro_trde_sell_qty: str = Field(default="", description="비차익거래매도수량", max_length=20)
    ndiffpro_trde_buy_qty: str = Field(default="", description="비차익거래매수수량", max_length=20)
    ndiffpro_trde_netprps_qty: str = Field(default="", description="비차익거래순매수수량", max_length=20)
    all_sel: str = Field(default="", description="전체매도", max_length=20)
    all_buy: str = Field(default="", description="전체매수", max_length=20)
    all_netprps: str = Field(default="", description="전체순매수", max_length=20)
    kospi200: str = Field(default="", description="KOSPI200", max_length=20)
    basis: str = Field(default="", description="BASIS", max_length=20)


class DomesticMarketConditionProgramTradingTrendByTime(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="프로그램매매추이시간별요청")

    prm_trde_trnsn: list[DomesticMarketConditionProgramTradingTrendByTimeItem] = Field(
        default_factory=list, description="프로그램매매추이시간별"
    )


class DomesticMarketConditionProgramTradingArbitrageBalanceTrendItem(BaseModel):
    dt: str = Field(default="", description="일자", max_length=20)
    buy_dfrt_trde_qty: str = Field(default="", description="매수차익거래수량", max_length=20)
    buy_dfrt_trde_amt: str = Field(default="", description="매수차익거래금액", max_length=20)
    buy_dfrt_trde_irds_amt: str = Field(default="", description="매수차익거래증감액", max_length=20)
    sel_dfrt_trde_qty: str = Field(default="", description="매도차익거래수량", max_length=20)
    sel_dfrt_trde_amt: str = Field(default="", description="매도차익거래금액", max_length=20)
    sel_dfrt_trde_irds_amt: str = Field(default="", description="매도차익거래증감액", max_length=20)


class DomesticMarketConditionProgramTradingArbitrageBalanceTrend(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="프로그램매매차익잔고추이요청")

    prm_trde_dfrt_remn_trnsn: list[DomesticMarketConditionProgramTradingArbitrageBalanceTrendItem] = Field(
        default_factory=list, description="프로그램매매차익잔고추이"
    )


class DomesticMarketConditionProgramTradingCumulativeTrendItem(BaseModel):
    dt: str = Field(default="", description="일자", max_length=20)
    kospi200: str = Field(default="", description="KOSPI200", max_length=20)
    basis: str = Field(default="", description="BASIS", max_length=20)
    dfrt_trde_tdy: str = Field(default="", description="차익거래당일", max_length=20)
    dfrt_trde_acc: str = Field(default="", description="차익거래누적", max_length=20)
    ndiffpro_trde_tdy: str = Field(default="", description="비차익거래당일", max_length=20)
    ndiffpro_trde_acc: str = Field(default="", description="비차익거래누적", max_length=20)
    all_tdy: str = Field(default="", description="전체당일", max_length=20)
    all_acc: str = Field(default="", description="전체누적", max_length=20)


class DomesticMarketConditionProgramTradingCumulativeTrend(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="프로그램매매누적추이요청")

    prm_trde_acc_trnsn: list[DomesticMarketConditionProgramTradingCumulativeTrendItem] = Field(
        default_factory=list, description="프로그램매매누적추이"
    )


class DomesticMarketConditionProgramTradingTrendByStockAndTimeItem(BaseModel):
    tm: str = Field(default="", description="시간", max_length=20)
    cur_prc: str = Field(default="", description="현재가", max_length=20)
    pre_sig: str = Field(default="", description="대비기호", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    flu_rt: str = Field(default="", description="등락율", max_length=20)
    trde_qty: str = Field(default="", description="거래량", max_length=20)
    prm_sell_amt: str = Field(default="", description="프로그램매도금액", max_length=20)
    prm_buy_amt: str = Field(default="", description="프로그램매수금액", max_length=20)
    prm_netprps_amt: str = Field(default="", description="프로그램순매수금액", max_length=20)
    prm_netprps_amt_irds: str = Field(default="", description="프로그램순매수금액증감", max_length=20)
    prm_sell_qty: str = Field(default="", description="프로그램매도수량", max_length=20)
    prm_buy_qty: str = Field(default="", description="프로그램매수수량", max_length=20)
    prm_netprps_qty: str = Field(default="", description="프로그램순매수수량", max_length=20)
    prm_netprps_qty_irds: str = Field(default="", description="프로그램순매수수량증감", max_length=20)
    base_pric_tm: str = Field(default="", description="기준가시간", max_length=20)
    dbrt_trde_rpy_sum: str = Field(default="", description="대차거래상환주수합", max_length=20)
    remn_rcvord_sum: str = Field(default="", description="잔고수주합", max_length=20)
    stex_tp: str = Field(default="", description="거래소구분, KRX , NXT , 통합", max_length=20)  # KRX, NXT, 통합


class DomesticMarketConditionProgramTradingTrendByStockAndTime(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="종목시간별프로그램매매추이요청")

    stk_tm_prm_trde_trnsn: list[DomesticMarketConditionProgramTradingTrendByStockAndTimeItem] = Field(
        default_factory=list, description="종목시간별프로그램매매추이"
    )


class DomesticMarketConditionProgramTradingTrendByDateItem(BaseModel):
    cntr_tm: str = Field(default="", description="체결시간", max_length=20)
    dfrt_trde_sel: str = Field(default="", description="차익거래매도", max_length=20)
    dfrt_trde_buy: str = Field(default="", description="차익거래매수", max_length=20)
    dfrt_trde_netprps: str = Field(default="", description="차익거래순매수", max_length=20)
    ndiffpro_trde_sel: str = Field(default="", description="비차익거래매도", max_length=20)
    ndiffpro_trde_buy: str = Field(default="", description="비차익거래매수", max_length=20)
    ndiffpro_trde_netprps: str = Field(default="", description="비차익거래순매수", max_length=20)
    dfrt_trde_sell_qty: str = Field(default="", description="차익거래매도수량", max_length=20)
    dfrt_trde_buy_qty: str = Field(default="", description="차익거래매수수량", max_length=20)
    dfrt_trde_netprps_qty: str = Field(default="", description="차익거래순매수수량", max_length=20)
    ndiffpro_trde_sell_qty: str = Field(default="", description="비차익거래매도수량", max_length=20)
    ndiffpro_trde_buy_qty: str = Field(default="", description="비차익거래매수수량", max_length=20)
    ndiffpro_trde_netprps_qty: str = Field(default="", description="비차익거래순매수수량", max_length=20)
    all_sel: str = Field(default="", description="전체매도", max_length=20)
    all_buy: str = Field(default="", description="전체매수", max_length=20)
    all_netprps: str = Field(default="", description="전체순매수", max_length=20)
    kospi200: str = Field(default="", description="KOSPI200", max_length=20)
    basis: str = Field(default="", description="BASIS", max_length=20)


class DomesticMarketConditionProgramTradingTrendByDate(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="프로그램매매추이일별요청일자별요청")

    prm_trde_trnsn: list[DomesticMarketConditionProgramTradingTrendByDateItem] = Field(
        default_factory=list, description="프로그램매매추이일별"
    )


class DomesticMarketConditionProgramTradingTrendByStockAndDateItem(BaseModel):
    dt: str = Field(default="", description="일자", max_length=20)
    cur_prc: str = Field(default="", description="현재가", max_length=20)
    pre_sig: str = Field(default="", description="대비기호", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    flu_rt: str = Field(default="", description="등락율", max_length=20)
    trde_qty: str = Field(default="", description="거래량", max_length=20)
    prm_sell_amt: str = Field(default="", description="프로그램매도금액", max_length=20)
    prm_buy_amt: str = Field(default="", description="프로그램매수금액", max_length=20)
    prm_netprps_amt: str = Field(default="", description="프로그램순매수금액", max_length=20)
    prm_netprps_amt_irds: str = Field(default="", description="프로그램순매수금액증감", max_length=20)
    prm_sell_qty: str = Field(default="", description="프로그램매도수량", max_length=20)
    prm_buy_qty: str = Field(default="", description="프로그램매수수량", max_length=20)
    prm_netprps_qty: str = Field(default="", description="프로그램순매수수량", max_length=20)
    prm_netprps_qty_irds: str = Field(default="", description="프로그램순매수수량증감", max_length=20)
    base_pric_tm: str = Field(default="", description="기준가시간", max_length=20)
    dbrt_trde_rpy_sum: str = Field(default="", description="대차거래상환주수합", max_length=20)
    remn_rcvord_sum: str = Field(default="", description="잔고수주합", max_length=20)
    stex_tp: str = Field(default="", description="거래소구분, KRX , NXT , 통합", max_length=20)


class DomesticMarketConditionProgramTradingTrendByStockAndDate(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="종목일별프로그램매매추이요청")

    stk_daly_prm_trde_trnsn: list[DomesticMarketConditionProgramTradingTrendByStockAndDateItem] = Field(
        default_factory=list, description="종목일별프로그램매매추이"
    )
