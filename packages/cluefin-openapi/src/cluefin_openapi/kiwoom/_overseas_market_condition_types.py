from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

from cluefin_openapi.kiwoom._model import KiwoomHttpBody


class OverseasMarketConditionCurrentPriceStockInfo(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 현재가 종목정보 응답")

    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    week52_hgst_pric: str = Field(
        default="",
        description="52주 최고가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자",
        alias="52wk_hgst_pric",
    )
    week52_hgst_pric_pre_rt: str = Field(
        default="",
        description="52주 최고가 대비율. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율",
        alias="52wk_hgst_pric_pre_rt",
    )
    week52_hgst_pric_dt: str = Field(
        default="",
        description="52주 최고가일. YYYYMMDD",
        alias="52wk_hgst_pric_dt",
    )
    week52_lwst_pric: str = Field(
        default="",
        description="52주 최저가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자",
        alias="52wk_lwst_pric",
    )
    week52_lwst_pric_pre_rt: str = Field(
        default="",
        description="52주 최저가 대비율. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율",
        alias="52wk_lwst_pric_pre_rt",
    )
    week52_lwst_pric_dt: str = Field(
        default="",
        description="52주 최저가일. YYYYMMDD",
        alias="52wk_lwst_pric_dt",
    )
    stk_cnt: str = Field(default="", description="주식수. 단위: 1주")
    mac: str = Field(default="", description="시가총액. 단위: 천USD")
    setl_mm: str = Field(default="", description="결산월")
    lg_inds_cd: str = Field(default="", description="대업종구분")
    sm_inds_cd: str = Field(default="", description="소업종구분")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    acc_trde_qty: str = Field(default="", description="누적거래량. 단위: 1주")
    oyr_hgst: str = Field(default="", description="연중최고가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    oyr_hgst_dt: str = Field(default="", description="연중최고가일. YYYYMMDD")
    oyr_hgst_pre_rt: str = Field(
        default="", description="연중최고가 대비율. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율"
    )
    oyr_lwst: str = Field(default="", description="연중최저가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    oyr_lwst_dt: str = Field(default="", description="연중최저가일. YYYYMMDD")
    oyr_lwst_pre_rt: str = Field(
        default="", description="연중최저가 대비율. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율"
    )
    pre_open_pric: str = Field(default="", description="전일시가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    pre_high_pric: str = Field(default="", description="전일고가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    pre_low_pric: str = Field(default="", description="전일저가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    base_close_pric: str = Field(default="", description="전일종가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    upl_pric: str = Field(default="", description="상한가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    lst_pric: str = Field(default="", description="하한가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    trde_qty_unit: str = Field(default="", description="매매수량단위")
    uncert_lv: str = Field(default="", description="불확실성")
    comp_adv_tp: str = Field(default="", description="경쟁우위")
    curr_unit: str = Field(default="", description="통화단위")
    open_pric: str = Field(default="", description="시가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    high_pric: str = Field(default="", description="고가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    low_pric: str = Field(default="", description="저가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    trd_susp_tp: str = Field(default="", description="거래정지여부")
    base_exrt: str = Field(default="", description="환율. 소수점 둘째 자리까지 포맷된 숫자")


class OverseasMarketConditionCurrentPriceTenQuotes(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 현재가 10호가 응답")

    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    trde_qty: str = Field(default="", description="거래량. 단위: 1주")
    trde_prica: str = Field(default="", description="거래대금. 단위: 천USD")
    open_pric: str = Field(default="", description="시가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    high_pric: str = Field(default="", description="고가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    low_pric: str = Field(default="", description="저가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    bid_tm: str = Field(default="", description="호가시간. HH:mm")
    dt: str = Field(default="", description="일자. YYYYMMDD")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    fpr_sel_bid: str = Field(
        default="", description="최우선매도호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자"
    )
    fpr_buy_bid: str = Field(
        default="", description="최우선매수호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자"
    )
    pre_trde_rt: str = Field(
        default="", description="전일거래대비. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율"
    )
    trde_tern_rt: str = Field(
        default="", description="거래회전율. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율"
    )
    sel_1bid: str = Field(default="", description="매도1호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    sel_2bid: str = Field(default="", description="매도2호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    sel_3bid: str = Field(default="", description="매도3호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    sel_4bid: str = Field(default="", description="매도4호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    sel_5bid: str = Field(default="", description="매도5호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    sel_6bid: str = Field(default="", description="매도6호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    sel_7bid: str = Field(default="", description="매도7호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    sel_8bid: str = Field(default="", description="매도8호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    sel_9bid: str = Field(default="", description="매도9호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    sel_10bid: str = Field(default="", description="매도10호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    buy_1bid: str = Field(default="", description="매수1호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    buy_2bid: str = Field(default="", description="매수2호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    buy_3bid: str = Field(default="", description="매수3호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    buy_4bid: str = Field(default="", description="매수4호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    buy_5bid: str = Field(default="", description="매수5호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    buy_6bid: str = Field(default="", description="매수6호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    buy_7bid: str = Field(default="", description="매수7호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    buy_8bid: str = Field(default="", description="매수8호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    buy_9bid: str = Field(default="", description="매수9호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    buy_10bid: str = Field(default="", description="매수10호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    sel_1bid_req: str = Field(default="", description="매도1호가잔량. 단위: 1주")
    sel_2bid_req: str = Field(default="", description="매도2호가잔량. 단위: 1주")
    sel_3bid_req: str = Field(default="", description="매도3호가잔량. 단위: 1주")
    sel_4bid_req: str = Field(default="", description="매도4호가잔량. 단위: 1주")
    sel_5bid_req: str = Field(default="", description="매도5호가잔량. 단위: 1주")
    sel_6bid_req: str = Field(default="", description="매도6호가잔량. 단위: 1주")
    sel_7bid_req: str = Field(default="", description="매도7호가잔량. 단위: 1주")
    sel_8bid_req: str = Field(default="", description="매도8호가잔량. 단위: 1주")
    sel_9bid_req: str = Field(default="", description="매도9호가잔량. 단위: 1주")
    sel_10bid_req: str = Field(default="", description="매도10호가잔량. 단위: 1주")
    buy_1bid_req: str = Field(default="", description="매수1호가잔량. 단위: 1주")
    buy_2bid_req: str = Field(default="", description="매수2호가잔량. 단위: 1주")
    buy_3bid_req: str = Field(default="", description="매수3호가잔량. 단위: 1주")
    buy_4bid_req: str = Field(default="", description="매수4호가잔량. 단위: 1주")
    buy_5bid_req: str = Field(default="", description="매수5호가잔량. 단위: 1주")
    buy_6bid_req: str = Field(default="", description="매수6호가잔량. 단위: 1주")
    buy_7bid_req: str = Field(default="", description="매수7호가잔량. 단위: 1주")
    buy_8bid_req: str = Field(default="", description="매수8호가잔량. 단위: 1주")
    buy_9bid_req: str = Field(default="", description="매수9호가잔량. 단위: 1주")
    buy_10bid_req: str = Field(default="", description="매수10호가잔량. 단위: 1주")
    sel_1bid_jub_pre: str = Field(default="", description="매도1호가직전대비")
    sel_2bid_jub_pre: str = Field(default="", description="매도2호가직전대비")
    sel_3bid_jub_pre: str = Field(default="", description="매도3호가직전대비")
    sel_4bid_jub_pre: str = Field(default="", description="매도4호가직전대비")
    sel_5bid_jub_pre: str = Field(default="", description="매도5호가직전대비")
    sel_6bid_jub_pre: str = Field(default="", description="매도6호가직전대비")
    sel_7bid_jub_pre: str = Field(default="", description="매도7호가직전대비")
    sel_8bid_jub_pre: str = Field(default="", description="매도8호가직전대비")
    sel_9bid_jub_pre: str = Field(default="", description="매도9호가직전대비")
    sel_10bid_jub_pre: str = Field(default="", description="매도10호가직전대비")
    buy_1th_pre_req_pre: str = Field(default="", description="매수1차선잔량대비")
    buy_1bid_jub_pre: str = Field(default="", description="매수1호가직전대비")
    buy_2bid_jub_pre: str = Field(default="", description="매수2호가직전대비")
    buy_3bid_jub_pre: str = Field(default="", description="매수3호가직전대비")
    buy_4bid_jub_pre: str = Field(default="", description="매수4호가직전대비")
    buy_5bid_jub_pre: str = Field(default="", description="매수5호가직전대비")
    buy_6bid_jub_pre: str = Field(default="", description="매수6호가직전대비")
    buy_7bid_jub_pre: str = Field(default="", description="매수7호가직전대비")
    buy_8bid_jub_pre: str = Field(default="", description="매수8호가직전대비")
    buy_9bid_jub_pre: str = Field(default="", description="매수9호가직전대비")
    buy_10bid_jub_pre: str = Field(default="", description="매수10호가직전대비")
    tot_sel_req: str = Field(default="", description="총매도잔량. 단위: 1주")
    sel_bid_tot_req_jub_pre: str = Field(default="", description="매도호가총잔량직전대비")
    tot_buy_req: str = Field(default="", description="총매수잔량. 단위: 1주")
    buy_bid_tot_req_jub_pre: str = Field(default="", description="매수호가총잔량직전대비")
    netprps_req: str = Field(default="", description="순매수잔량. 단위: 1주")
    netslmt_req: str = Field(default="", description="순매도잔량. 단위: 1주")
    upl_pric: str = Field(default="", description="상한가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    base_pric: str = Field(default="", description="기준가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")


class OverseasMarketConditionDetailedExecutionHistoryItem(BaseModel):
    cur_prc: str = Field(default="", description="현재가, 종가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    trde_qty: str = Field(default="", description="거래량. 단위: 1주, 부호가 포함된 숫자")
    cntr_tm: str = Field(default="", description="체결시간. HHmmss")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")


class OverseasMarketConditionDetailedExecutionHistory(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 상세 체결내역 응답")

    result_list: list[OverseasMarketConditionDetailedExecutionHistoryItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasMarketConditionDailyExecutionHistoryItem(BaseModel):
    dt: str = Field(default="", description="일자. YYYYMMDD")
    cur_prc: str = Field(default="", description="현재가, 종가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    acc_trde_qty: str = Field(default="", description="누적거래량. 단위: 1주")


class OverseasMarketConditionDailyExecutionHistory(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 일별 체결내역 응답")

    result_list: list[OverseasMarketConditionDailyExecutionHistoryItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasMarketConditionDailyStockPriceItem(BaseModel):
    dt: str = Field(default="", description="일자. YYYYMMDD")
    cur_prc: str = Field(default="", description="현재가(종가). 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    acc_trde_qty: str = Field(default="", description="누적거래량. 단위: 1주")
    trde_prica: str = Field(default="", description="누적금액. 단위: 천USD")
    open_pric: str = Field(default="", description="시가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    high_pric: str = Field(default="", description="고가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    low_pric: str = Field(default="", description="저가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    base_pric: str = Field(default="", description="기준가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    base_open_flu_rt: str = Field(
        default="", description="기준가대비 시가등락율. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율"
    )
    base_high_flu_rt: str = Field(
        default="", description="기준가대비 고가등락율. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율"
    )
    base_low_flu_rt: str = Field(
        default="", description="기준가대비 저가등락율. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율"
    )


class OverseasMarketConditionDailyStockPrice(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 일별주가 응답")

    result_list: list[OverseasMarketConditionDailyStockPriceItem] = Field(
        default_factory=list, description="결과리스트"
    )
