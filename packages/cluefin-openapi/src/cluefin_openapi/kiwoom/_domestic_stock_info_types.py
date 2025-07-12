from typing import List

from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

from cluefin_openapi.kiwoom._model import KiwoomHttpBody


class DomesticStockInfoBasic(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(
        title="주식기본정보요청 응답",
    )

    stk_cd: str = Field(default="", description="종목코드", max_length=20)
    stk_nm: str = Field(default="", description="종목명", max_length=40)
    setl_mm: str = Field(default="", description="결산월", max_length=20)
    fav: str = Field(default="", description="액면가", max_length=20)
    cap: str = Field(default="", description="자본금", max_length=20)
    flo_stk: str = Field(default="", description="상장주식", max_length=20)
    crd_rt: str = Field(default="", description="신용비율", max_length=20)
    oyr_hgst: str = Field(default="", description="연중최고", max_length=20)
    oyr_lwst: str = Field(default="", description="연중최저", max_length=20)
    mac: str = Field(default="", description="시가총액", max_length=20)
    mac_wght: str = Field(default="", description="시가총액비중", max_length=20)
    for_exh_rt: str = Field(default="", description="외인소진률", max_length=20)
    repl_pric: str = Field(default="", description="대용가", max_length=20)
    per: str = Field(default="", description="PER", max_length=20)
    eps: str = Field(default="", description="EPS", max_length=20)
    roe: str = Field(default="", description="ROE", max_length=20)
    pbr: str = Field(default="", description="PBR", max_length=20)
    ev: str = Field(default="", description="EV", max_length=20)
    bps: str = Field(default="", description="BPS", max_length=20)
    sale_amt: str = Field(default="", description="매출액", max_length=20)
    bus_pro: str = Field(default="", description="영업이익", max_length=20)
    cup_nga: str = Field(default="", description="당기순이익", max_length=20)
    hgst_250: str = Field(default="", description="250최고", max_length=20, alias="250hgst")
    lwst_250: str = Field(default="", description="250최저", max_length=20, alias="250lwst")
    high_pric: str = Field(default="", description="고가", max_length=20)
    open_pric: str = Field(default="", description="시가", max_length=20)
    low_pric: str = Field(default="", description="저가", max_length=20)
    upl_pric: str = Field(default="", description="상한가", max_length=20)
    lst_pric: str = Field(default="", description="하한가", max_length=20)
    base_pric: str = Field(default="", description="기준가", max_length=20)
    exp_cntr_pric: str = Field(default="", description="예상체결가", max_length=20)
    exp_cntr_qty: str = Field(default="", description="예상체결수량", max_length=20)
    hgst_prict_250dt: str = Field(default="", description="250최고가일", max_length=20, alias="250hgst_pric_dt")
    hgst_prict_250pre_rt: str = Field(
        default="", description="250최고가대비율", max_length=20, alias="250hgst_pric_pre_rt"
    )
    lwst_prict_250dt: str = Field(default="", description="250최저가일", max_length=20, alias="250lwst_pric_dt")
    lwst_prict_250pre_rt: str = Field(
        default="", description="250최저가대비율", max_length=20, alias="250lwst_pric_pre_rt"
    )
    cur_prc: str = Field(default="", description="현재가", max_length=20)
    pre_sig: str = Field(default="", description="대비기호", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    flu_rt: str = Field(default="", description="등락율", max_length=20)
    trde_qty: str = Field(default="", description="거래량", max_length=20)
    trde_pre: str = Field(default="", description="거래대비", max_length=20)
    fav_unit: str = Field(default="", description="액면가단위", max_length=20)
    dstr_stk: str = Field(default="", description="유통주식", max_length=20)
    dstr_rt: str = Field(default="", description="유통비율", max_length=20)


class DomesticStockInfoTradingMember(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(
        title="주식거래소회원사요청 응답",
    )
    stk_cd: str = Field(default="", description="종목코드", max_length=20)
    stk_nm: str = Field(default="", description="종목명", max_length=40)
    cur_prc: str = Field(default="", description="현재가", max_length=20)
    flu_smbol: str = Field(default="", description="등락부호", max_length=20)
    base_pric: str = Field(default="", description="기준가", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    flu_rt: str = Field(default="", description="등락율", max_length=20)
    sel_trde_ori_nm_1: str = Field(default="", description="매도거래원명1", max_length=20)
    sel_trde_ori_1: str = Field(default="", description="매도거래원1", max_length=20)
    sel_trde_qty_1: str = Field(default="", description="매도거래량1", max_length=20)
    buy_trde_ori_nm_1: str = Field(default="", description="매수거래원명1", max_length=20)
    buy_trde_ori_1: str = Field(default="", description="매수거래원1", max_length=20)
    buy_trde_qty_1: str = Field(default="", description="매수거래량1", max_length=20)
    sel_trde_ori_nm_2: str = Field(default="", description="매도거래원명2", max_length=20)
    sel_trde_ori_2: str = Field(default="", description="매도거래원2", max_length=20)
    sel_trde_qty_2: str = Field(default="", description="매도거래량2", max_length=20)
    buy_trde_ori_nm_2: str = Field(default="", description="매수거래원명2", max_length=20)
    buy_trde_ori_2: str = Field(default="", description="매수거래원2", max_length=20)
    buy_trde_qty_2: str = Field(default="", description="매수거래량2", max_length=20)
    sel_trde_ori_nm_3: str = Field(default="", description="매도거래원명3", max_length=20)
    sel_trde_ori_3: str = Field(default="", description="매도거래원3", max_length=20)
    sel_trde_qty_3: str = Field(default="", description="매도거래량3", max_length=20)
    buy_trde_ori_nm_3: str = Field(default="", description="매수거래원명3", max_length=20)
    buy_trde_ori_3: str = Field(default="", description="매수거래원3", max_length=20)
    buy_trde_qty_3: str = Field(default="", description="매수거래량3", max_length=20)
    sel_trde_ori_nm_4: str = Field(default="", description="매도거래원명4", max_length=20)
    sel_trde_ori_4: str = Field(default="", description="매도거래원4", max_length=20)
    sel_trde_qty_4: str = Field(default="", description="매도거래량4", max_length=20)
    buy_trde_ori_nm_4: str = Field(default="", description="매수거래원명4", max_length=20)
    buy_trde_ori_4: str = Field(default="", description="매수거래원4", max_length=20)
    buy_trde_qty_4: str = Field(default="", description="매수거래량4", max_length=20)
    sel_trde_ori_nm_5: str = Field(default="", description="매도거래원명5", max_length=20)
    sel_trde_ori_5: str = Field(default="", description="매도거래원5", max_length=20)
    sel_trde_qty_5: str = Field(default="", description="매도거래량5", max_length=20)
    buy_trde_ori_nm_5: str = Field(default="", description="매수거래원명5", max_length=20)
    buy_trde_ori_5: str = Field(default="", description="매수거래원5", max_length=20)
    buy_trde_qty_5: str = Field(default="", description="매수거래량5", max_length=20)


class DomesticStockInfoExecutionItem(BaseModel):
    tm: str = Field(default="", description="시간", max_length=20)
    cur_prc: str = Field(default="", description="현재가", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    pre_rt: str = Field(default="", description="대비율", max_length=20)
    pri_sel_bid_unit: str = Field(default="", description="우선매도호가단위", max_length=20)
    pri_buy_bid_unit: str = Field(default="", description="우선매수호가단위", max_length=20)
    cntr_trde_qty: str = Field(default="", description="체결거래량", max_length=20)
    sign: str = Field(default="", description="기호", max_length=20)
    acc_trde_qty: str = Field(default="", description="누적거래량", max_length=20)
    acc_trde_prica: str = Field(default="", description="누적거래대금", max_length=20)
    cntr_str: str = Field(default="", description="체결강도", max_length=20)
    stex_tp: str = Field(default="", description="거래소구분", max_length=20)  # KRX, NXT, 통합


class DomesticStockInfoExecution(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(
        title="주식체결정보요청 응답",
    )
    cntr_infr: List[DomesticStockInfoExecutionItem] = Field(
        default_factory=list, description="체결정보", max_length=1000
    )


class DomesticStockInfoMarginTradingTrendItem(BaseModel):
    dt: str = Field(default="", description="일자", max_length=20)
    cur_prc: str = Field(default="", description="현재가", max_length=20)
    pred_pre_sig: str = Field(default="", description="전일대비기호", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    trde_qty: str = Field(default="", description="거래량", max_length=20)
    new: str = Field(default="", description="신규", max_length=20)
    rpya: str = Field(default="", description="상환", max_length=20)
    remn: str = Field(default="", description="잔고", max_length=20)
    amt: str = Field(default="", description="금액", max_length=20)
    pre: str = Field(default="", description="대비", max_length=20)
    shr_rt: str = Field(default="", description="공여율", max_length=20)
    remn_rt: str = Field(default="", description="잔고율", max_length=20)


class DomesticStockInfoMarginTradingTrend(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(
        title="주식신용거래추세요청 응답",
    )
    crd_trde_trend: List[DomesticStockInfoMarginTradingTrendItem] = Field(
        default_factory=list, description="신용매매동향", max_length=1000
    )


class DomesticStockInfoDailyTradingDetailsItem(BaseModel):
    dt: str = Field(default="", description="일자", max_length=20)
    close_pric: str = Field(default="", description="종가", max_length=20)
    pred_pre_sig: str = Field(default="", description="전일대비기호", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    flu_rt: str = Field(default="", description="등락율", max_length=20)
    trde_qty: str = Field(default="", description="거래량", max_length=20)
    trde_prica: str = Field(default="", description="거래대금", max_length=20)
    bf_mkrt_trde_qty: str = Field(default="", description="장전거래량", max_length=20)
    bf_mkrt_trde_wght: str = Field(default="", description="장전거래비중", max_length=20)
    opmr_trde_qty: str = Field(default="", description="장중거래량", max_length=20)
    opmr_trde_wght: str = Field(default="", description="장중거래비중", max_length=20)
    af_mkrt_trde_qty: str = Field(default="", description="장후거래량", max_length=20)
    af_mkrt_trde_wght: str = Field(default="", description="장후거래비중", max_length=20)
    tot_3: str = Field(default="", description="합계3", max_length=20)
    prid_trde_qty: str = Field(default="", description="기간중거래량", max_length=20)
    cntr_str: str = Field(default="", description="체결강도", max_length=20)
    for_poss: str = Field(default="", description="외인보유", max_length=20)
    for_wght: str = Field(default="", description="외인비중", max_length=20)
    for_netprps: str = Field(default="", description="외인순매수", max_length=20)
    orgn_netprps: str = Field(default="", description="기관순매수", max_length=20)
    ind_netprps: str = Field(default="", description="개인순매수", max_length=20)
    frgn: str = Field(default="", description="외국계", max_length=20)
    crd_remn_rt: str = Field(default="", description="신용잔고율", max_length=20)
    prm: str = Field(default="", description="프로그램", max_length=20)
    bf_mkrt_trde_qty: str = Field(default="", description="장전거래대금", max_length=20)
    bf_mkrt_trde_prica_wght: str = Field(default="", description="장전거래대금비중", max_length=20)
    opmr_trde_prica: str = Field(default="", description="장중거래대금", max_length=20)
    opmr_trde_prica_wght: str = Field(default="", description="장중거래대금비중", max_length=20)
    af_mkrt_trde_prica: str = Field(default="", description="장후거래대금", max_length=20)
    af_mkrt_trde_prica_wght: str = Field(default="", description="장후거래대금비중", max_length=20)


class DomesticStockInfoDailyTradingDetails(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="주식일별거래상세요청 응답")
    daly_trde_dtl: List[DomesticStockInfoDailyTradingDetailsItem] = Field(
        default_factory=list, description="일별거래상세", max_length=1000
    )


class DomesticStockInfoNewHighLowPriceItem(BaseModel):
    stk_cd: str = Field(default="", description="종목코드", max_length=20)
    stk_nm: str = Field(default="", description="종목명", max_length=40)
    cur_prc: str = Field(default="", description="현재가", max_length=20)
    pred_pre_sig: str = Field(default="", description="전일대비기호", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    flu_rt: str = Field(default="", description="등락률", max_length=20)
    trde_qty: str = Field(default="", description="거래량", max_length=20)
    pred_trde_qty_pre_rt: str = Field(default="", description="전일거래량대비율", max_length=20)
    sel_bid: str = Field(default="", description="매도호가", max_length=20)
    buy_bid: str = Field(default="", description="매수호가", max_length=20)
    high_pric: str = Field(default="", description="고가", max_length=20)
    low_pric: str = Field(default="", description="저가", max_length=20)


class DomesticStockInfoNewHighLowPrice(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="주식신고저가요청 응답")
    ntl_pric: List[DomesticStockInfoNewHighLowPriceItem] = Field(
        default_factory=list, description="신고저가", max_length=1000
    )


class DomesticStockInfoNewHighLowPriceItem(BaseModel):
    stk_cd: str = Field(default="", description="종목코드", max_length=20)
    stk_infr: str = Field(default="", description="종목정보", max_length=20)
    stk_nm: str = Field(default="", description="종목명", max_length=40)
    cur_prc: str = Field(default="", description="현재가", max_length=20)
    pred_pre_sig: str = Field(default="", description="전일대비기호", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    flu_rt: str = Field(default="", description="등락률", max_length=20)
    trde_qty: str = Field(default="", description="거래량", max_length=20)
    pred_trde_qty: str = Field(default="", description="전일거래량대비율", max_length=20)
    sel_req: str = Field(default="", description="매도잔량", max_length=20)
    sel_bid: str = Field(default="", description="매도호가", max_length=20)
    buy_bid: str = Field(default="", description="매수호가", max_length=20)
    buy_req: str = Field(default="", description="매수잔량", max_length=20)
    cnt: str = Field(default="", description="횟수", max_length=20)


class DomesticStockInfoUpperLowerLimitPrice(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="주식상하한가요청 응답")
    updown_pric: List[DomesticStockInfoNewHighLowPriceItem] = Field(
        default_factory=list, description="상하한가", max_length=1000
    )


class DomesticStockInfoHighLowPriceApproachItem(BaseModel):
    stk_cd: str = Field(default="", description="종목코드", max_length=20)
    stk_nm: str = Field(default="", description="종목명", max_length=40)
    cur_prc: str = Field(default="", description="현재가", max_length=20)
    pred_pre_sig: str = Field(default="", description="전일대비기호", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    flu_rt: str = Field(default="", description="등락률", max_length=20)
    trde_qty: str = Field(default="", description="거래량", max_length=20)
    sel_bid: str = Field(default="", description="매도호가", max_length=20)
    buy_bid: str = Field(default="", description="매수호가", max_length=20)
    tdy_high_pric: str = Field(default="", description="당일고가", max_length=20)
    tdy_low_pric: str = Field(default="", description="당일저가", max_length=20)


class DomesticStockInfoHighLowPriceApproach(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="고저가 근접요청 응답")

    high_low_pric_alacc: List[DomesticStockInfoHighLowPriceApproachItem] = Field(
        default_factory=list, description="고저가근접", max_length=1000
    )


class DomesticStockInfoPriceVolatilityItem(BaseModel):
    stk_cd: str = Field(default="", description="종목코드", max_length=20)
    stk_cls: str = Field(default="", description="종목분류", max_length=20)
    stk_nm: str = Field(default="", description="종목명", max_length=40)
    pred_pre_sig: str = Field(default="", description="전일대비기호", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    flu_rt: str = Field(default="", description="등락률", max_length=20)
    base_pric: str = Field(default="", description="기준가", max_length=20)
    cur_prc: str = Field(default="", description="현재가", max_length=20)
    base_pre: str = Field(default="", description="기준대비", max_length=20)
    trde_qty: str = Field(default="", description="거래량", max_length=20)
    jmp_rt: str = Field(default="", description="급등률", max_length=20)


class DomesticStockInfoPriceVolatility(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="가격급등락요청 응답")
    pric_jmpflu: List[DomesticStockInfoPriceVolatilityItem] = Field(
        default_factory=list, description="가격 급등락", max_length=1000
    )


class DomesticStockInfoTradingVolumeRenewalItem(BaseModel):
    stk_cd: str = Field(default="", description="종목코드", max_length=20)
    stk_nm: str = Field(default="", description="종목명", max_length=40)
    cur_prc: str = Field(default="", description="현재가", max_length=20)
    pred_pre_sig: str = Field(default="", description="전일대비기호", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    flu_rt: str = Field(default="", description="등락률", max_length=20)
    prev_trde_qty: str = Field(default="", description="이전거래량", max_length=20)
    now_trde_qty: str = Field(default="", description="현재거래량", max_length=20)
    sel_bid: str = Field(default="", description="매도호가", max_length=20)
    buy_bid: str = Field(default="", description="매수호가", max_length=20)


class DomesticStockInfoTradingVolumeRenewal(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="거래량갱신요청 응답")

    trde_qty_updt: List[DomesticStockInfoPriceVolatilityItem] = Field(
        default_factory=list, description="거래량 갱신", max_length=1000
    )


class DomesticStockInfoSupplyDemandConcentrationItem(BaseModel):
    stk_cd: str = Field(default="", description="종목코드", max_length=20)
    stk_nm: str = Field(default="", description="종목명", max_length=40)
    cur_prc: str = Field(default="", description="현재가", max_length=20)
    pred_pre_sig: str = Field(default="", description="전일대비기호", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    flu_rt: str = Field(default="", description="등락률", max_length=20)
    now_trde_qty: str = Field(default="", description="현재거래량", max_length=20)
    pric_strt: str = Field(default="", description="가격대시작", max_length=20)
    pric_end: str = Field(default="", description="가격대끝", max_length=20)
    prps_qty: str = Field(default="", description="매물량", max_length=20)
    prps_rt: str = Field(default="", description="매물비율", max_length=20)


class DomesticStockInfoSupplyDemandConcentration(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="매물대집중요청 응답")

    prps_cnctr: List[DomesticStockInfoSupplyDemandConcentrationItem] = Field(
        default_factory=list, description="매물대 집중", max_length=1000
    )


class DomesticStockInfoHighPerItem(BaseModel):
    stk_cd: str = Field(default="", description="종목코드", max_length=20)
    stk_nm: str = Field(default="", description="종목명", max_length=40)
    per: str = Field(default="", description="PER", max_length=20)
    cur_prc: str = Field(default="", description="현재가", max_length=20)
    pred_pre_sig: str = Field(default="", description="전일대비기호", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    flu_rt: str = Field(default="", description="등락률", max_length=20)
    now_trde_qty: str = Field(default="", description="현재거래량", max_length=20)
    sel_bid: str = Field(default="", description="매도호가", max_length=20)


class DomesticStockInfoHighPer(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="고저PER요청 응답")

    high_low_per: List[DomesticStockInfoHighPerItem] = Field(
        default_factory=list, description="고저 PER", max_length=1000
    )


class DomesticStockInfoChangeRateFromOpenItem(BaseModel):
    stk_cd: str = Field(default="", description="종목코드", max_length=20)
    stk_nm: str = Field(default="", description="종목명", max_length=40)
    cur_prc: str = Field(default="", description="현재가", max_length=20)
    pred_pre_sig: str = Field(default="", description="전일대비기호", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    flu_rt: str = Field(default="", description="등락률", max_length=20)
    open_pric: str = Field(default="", description="시가", max_length=20)
    high_pric: str = Field(default="", description="고가", max_length=20)
    low_pric: str = Field(default="", description="저가", max_length=20)
    open_pric_pre: str = Field(default="", description="시가대비", max_length=20)
    now_trde_qty: str = Field(default="", description="현재거래량", max_length=20)
    cntr_str: str = Field(default="", description="체결강도", max_length=20)


class DomesticStockInfoChangeRateFromOpen(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="시가대비등락률요청 응답")

    open_pric_pre_flu_rt: List[DomesticStockInfoHighPerItem] = Field(
        default_factory=list, description="시가대비등락률", max_length=1000
    )


class DomesticStockInfoTradingMemberSupplyDemandAnalysisItem(BaseModel):
    dt: str = Field(default="", description="일자", max_length=20)
    close_pric: str = Field(default="", description="종가", max_length=20)
    pre_sig: str = Field(default="", description="대비기호", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    sel_qty: str = Field(default="", description="매도량", max_length=20)
    buy_qty: str = Field(default="", description="매수량", max_length=20)
    netprps_qty: str = Field(default="", description="순매수수량", max_length=20)
    trde_qty_sum: str = Field(default="", description="거래량합", max_length=20)
    trde_wght: str = Field(default="", description="거래비중", max_length=20)


class DomesticStockInfoTradingMemberSupplyDemandAnalysis(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="거래원매물대분석요청 응답")

    trde_ori_prps_anly: List[DomesticStockInfoTradingMemberSupplyDemandAnalysisItem] = Field(
        default_factory=list, description="거래원 매물대 분석", max_length=1000
    )


class DomesticStockInfoTradingMemberInstantVolumeItem(BaseModel):
    tm: str = Field(default="", description="시간", max_length=20)
    stk_cd: str = Field(default="", description="종목코드", max_length=20)
    stk_nm: str = Field(default="", description="종목명", max_length=40)
    trde_ori_nm: str = Field(default="", description="거래원명", max_length=20)
    tp: str = Field(default="", description="구분", max_length=20)
    mont_trde_qty: str = Field(default="", description="순간거래량", max_length=20)
    acc_netprps: str = Field(default="", description="누적순매수", max_length=20)
    cur_prc: str = Field(default="", description="현재가", max_length=20)
    pred_pre_sig: str = Field(default="", description="전일대비기호", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    flu_rt: str = Field(default="", description="등락율", max_length=20)


class DomesticStockInfoTradingMemberInstantVolume(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="거래원순간거래량요청 응답")

    trde_ori_mont_trde_qty: List[DomesticStockInfoTradingMemberInstantVolumeItem] = Field(
        default_factory=list, description="거래원 순간 거래량", max_length=1000
    )


class DomesticStockInfoVolatilityControlEventItem(BaseModel):
    stk_cd: str = Field(default="", description="종목코드", max_length=20)
    stk_nm: str = Field(default="", description="종목명", max_length=40)
    acc_trde_qty: str = Field(default="", description="누적거래량", max_length=20)
    motn_pric: str = Field(default="", description="발동가격", max_length=20)
    dynm_dispty_rt: str = Field(default="", description="동적괴리율", max_length=20)
    trde_cntr_proc_time: str = Field(default="", description="매매체결처리시각", max_length=20)
    virelis_time: str = Field(default="", description="VI해제시각", max_length=20)
    viaplc_tp: str = Field(default="", description="VI적용구분", max_length=20)
    dynm_stdpc: str = Field(default="", description="동적기준가격", max_length=20)
    static_stdpc: str = Field(default="", description="정적기준가격", max_length=20)
    static_dispty_rt: str = Field(default="", description="정적괴리율", max_length=20)
    open_pric_pre_flu_rt: str = Field(default="", description="시가대비등락률", max_length=20)
    vimotn_cnt: str = Field(default="", description="VI발동횟수", max_length=20)
    stex_tp: str = Field(default="", description="거래소구분", max_length=20)  # KRX, NXT, 통합


class DomesticStockInfoVolatilityControlEvent(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="변동성완화장치발동요청 응답")

    motn_stk: List[DomesticStockInfoVolatilityControlEventItem] = Field(
        default_factory=list, description="변동성완화장치 발동 목록", max_length=1000
    )


class DomesticStockInfoDailyPreviousDayExecutionVolumeItem(BaseModel):
    cntr_tm: str = Field(default="", description="체결시간", max_length=20)
    cntr_pric: str = Field(default="", description="체결가", max_length=20)
    pred_pre_sig: str = Field(default="", description="전일대비기호", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    flu_rt: str = Field(default="", description="등락율", max_length=20)
    cntr_qty: str = Field(default="", description="체결량", max_length=20)
    acc_trde_qty: str = Field(default="", description="누적거래량", max_length=20)
    acc_trde_prica: str = Field(default="", description="누적거래대금", max_length=20)


class DomesticStockInfoDailyPreviousDayExecutionVolume(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="당일전일체결량요청 응답")

    tdy_pred_cntr_qty: List[DomesticStockInfoDailyPreviousDayExecutionVolumeItem] = Field(
        default_factory=list, description="당일 전일 체결량", max_length=1000
    )


class DomesticStockInfoDailyTradingItemsByInvestorItem(BaseModel):
    stk_cd: str = Field(default="", description="종목코드", max_length=20)
    stk_nm: str = Field(default="", description="종목명", max_length=40)
    netslmt_qty: str = Field(default="", description="순매도수량", max_length=20)
    netslmt_amt: str = Field(default="", description="순매도금액", max_length=20)
    prsm_avg_pric: str = Field(default="", description="추정평균가", max_length=20)
    cur_prc: str = Field(default="", description="현재가", max_length=20)
    pre_sig: str = Field(default="", description="대비기호", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    avg_pric_pre: str = Field(default="", description="평균가대비", max_length=20)
    pre_rt: str = Field(default="", description="대비율", max_length=20)
    dt_trde_qty: str = Field(default="", description="기간거래량", max_length=20)


class DomesticStockInfoDailyTradingItemsByInvestor(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="투자자별일별매매종목요청 응답")
    invsr_daly_trde_stk: List[DomesticStockInfoDailyTradingItemsByInvestorItem] = Field(
        default_factory=list, description="투자자별 일별 매매 종목", max_length=1000
    )


class DomesticStockInfoInstitutionalInvestorByStockItem(BaseModel):
    dt: str = Field(default="", description="일자", max_length=20)
    cur_prc: str = Field(default="", description="현재가", max_length=20)
    pre_sig: str = Field(default="", description="대비기호", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    flu_rt: str = Field(default="", description="등락율", max_length=20)
    acc_trde_qty: str = Field(default="", description="누적거래량", max_length=20)
    acc_trde_prica: str = Field(default="", description="누적거래대금", max_length=20)
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
    natfor: str = Field(default="", description="내외국인", max_length=20)


class DomesticStockInfoInstitutionalInvestorByStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="종목별투자자기관별요청 응답")

    stk_invsr_orgn: List[DomesticStockInfoInstitutionalInvestorByStockItem] = Field(
        default_factory=list, description="종목별 투자자 기관", max_length=1000
    )


class DomesticStockInfoTotalInstitutionalInvestorByStockItem(BaseModel):
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
    natfor: str = Field(default="", description="내외국인", max_length=20)


class DomesticStockInfoTotalInstitutionalInvestorByStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="종목별투자자기관별합계요청 응답")

    stk_invsr_orgn_tot: List[DomesticStockInfoInstitutionalInvestorByStockItem] = Field(
        default_factory=list, description="종목별 투자자 기관 합계", max_length=1000
    )


class DomesticStockInfoDailyPreviousDayConclusionItem(BaseModel):
    tm: str = Field(default="", description="시간", max_length=20)
    cur_prc: str = Field(default="", description="현재가", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    pre_rt: str = Field(default="", description="대비율", max_length=20)
    pri_sel_bid_unit: str = Field(default="", description="우선매도호가단위", max_length=20)
    pri_buy_bid_unit: str = Field(default="", description="우선매수호가단위", max_length=20)
    cntr_trde_qty: str = Field(default="", description="체결거래량", max_length=20)
    sign: str = Field(default="", description="전일대비기호", max_length=20)
    acc_trde_qty: str = Field(default="", description="누적거래량", max_length=20)
    acc_trde_prica: str = Field(default="", description="누적거래대금", max_length=20)
    cntr_str: str = Field(default="", description="체결강도", max_length=20)
    stex_tp: str = Field(default="", description="거래소구분 (KRX, NXT, 통합)", max_length=20)


class DomesticStockInfoDailyPreviousDayConclusion(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="당일전일체결요청 응답")

    tdy_pred_cntr_qty: List[DomesticStockInfoDailyPreviousDayExecutionVolumeItem] = Field(
        default_factory=list, description="당일 전일 체결", max_length=1000
    )


class DomesticStockInfoInterestStockInfoItem(BaseModel):
    stk_cd: str = Field(default="", description="종목코드", max_length=20)
    stk_nm: str = Field(default="", description="종목명", max_length=40)
    cur_prc: str = Field(default="", description="현재가", max_length=20)
    base_pric: str = Field(default="", description="기준가", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    pred_pre_sig: str = Field(default="", description="전일대비기호", max_length=20)
    flu_rt: str = Field(default="", description="등락률", max_length=20)
    trde_qty: str = Field(default="", description="거래량", max_length=20)
    trde_prica: str = Field(default="", description="거래대금", max_length=20)
    cntr_qty: str = Field(default="", description="체결량", max_length=20)
    cntr_str: str = Field(default="", description="체결강도", max_length=20)
    pred_trde_qty_pre: str = Field(default="", description="전일거래량대비율", max_length=20)
    sel_bid: str = Field(default="", description="매도호가", max_length=20)
    buy_bid: str = Field(default="", description="매수호가", max_length=20)
    sel_1th_bid: str = Field(default="", description="매도1차호가", max_length=20)
    sel_2th_bid: str = Field(default="", description="매도2차호가", max_length=20)
    sel_3th_bid: str = Field(default="", description="매도3차호가", max_length=20)
    sel_4th_bid: str = Field(default="", description="매도4차호가", max_length=20)
    sel_5th_bid: str = Field(default="", description="매도5차호가", max_length=20)
    buy_1th_bid: str = Field(default="", description="매수1차호가", max_length=20)
    buy_2th_bid: str = Field(default="", description="매수2차호가", max_length=20)
    buy_3th_bid: str = Field(default="", description="매수3차호가", max_length=20)
    buy_4th_bid: str = Field(default="", description="매수4차호가", max_length=20)
    buy_5th_bid: str = Field(default="", description="매수5차호가", max_length=20)
    upl_pric: str = Field(default="", description="상한가", max_length=20)
    lst_pric: str = Field(default="", description="하한가", max_length=20)
    open_pric: str = Field(default="", description="시가", max_length=20)
    high_pric: str = Field(default="", description="고가", max_length=20)
    low_pric: str = Field(default="", description="저가", max_length=20)
    close_pric: str = Field(default="", description="종가", max_length=20)
    cntr_tm: str = Field(default="", description="체결시간", max_length=20)
    exp_cntr_pric: str = Field(default="", description="예상체결가", max_length=20)
    exp_cntr_qty: str = Field(default="", description="예상체결량", max_length=20)
    cap: str = Field(default="", description="자본금", max_length=20)
    fav: str = Field(default="", description="액면가", max_length=20)
    mac: str = Field(default="", description="시가총액", max_length=20)
    stkcnt: str = Field(default="", description="주식수", max_length=20)
    bid_tm: str = Field(default="", description="호가시간", max_length=20)
    dt: str = Field(default="", description="일자", max_length=20)
    pri_sel_req: str = Field(default="", description="우선매도잔량", max_length=20)
    pri_buy_req: str = Field(default="", description="우선매수잔량", max_length=20)
    pri_sel_cnt: str = Field(default="", description="우선매도건수", max_length=20)
    pri_buy_cnt: str = Field(default="", description="우선매수건수", max_length=20)
    tot_sel_req: str = Field(default="", description="총매도잔량", max_length=20)
    tot_buy_req: str = Field(default="", description="총매수잔량", max_length=20)
    tot_sel_cnt: str = Field(default="", description="총매도건수", max_length=20)
    tot_buy_cnt: str = Field(default="", description="총매수건수", max_length=20)
    prty: str = Field(default="", description="패리티", max_length=20)
    gear: str = Field(default="", description="기어링", max_length=20)
    pl_qutr: str = Field(default="", description="손익분기", max_length=20)
    cap_support: str = Field(default="", description="자본지지", max_length=20)
    elwexec_pric: str = Field(default="", description="ELW행사가", max_length=20)
    cnvt_rt: str = Field(default="", description="전환비율", max_length=20)
    elwexpr_dt: str = Field(default="", description="ELW만기일", max_length=20)
    cntr_engg: str = Field(default="", description="미결제약정", max_length=20)
    cntr_pred_pre: str = Field(default="", description="미결제전일대비", max_length=20)
    theory_pric: str = Field(default="", description="이론가", max_length=20)
    innr_vltl: str = Field(default="", description="내재변동성", max_length=20)
    delta: str = Field(default="", description="델타", max_length=20)
    gam: str = Field(default="", description="감마", max_length=20)
    theta: str = Field(default="", description="쎄타", max_length=20)
    vega: str = Field(default="", description="베가", max_length=20)
    law: str = Field(default="", description="로", max_length=20)


class DomesticStockInfoInterestStockInfo(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="관심종목정보요청 응답")

    atn_stk_infr: List[DomesticStockInfoInterestStockInfoItem] = Field(
        default_factory=list, description="관심 종목 정보", max_length=1000
    )


class DomesticStockInfoSummaryItem(BaseModel):
    code: str = Field(default="", description="종목코드", max_length=20)
    name: str = Field(default="", description="종목명", max_length=40)
    listCount: str = Field(default="", description="상장주식수", max_length=20)
    auditInfo: str = Field(default="", description="감리구분", max_length=20)
    regDay: str = Field(default="", description="상장일", max_length=20)
    lastPrice: str = Field(default="", description="전일종가", max_length=20)
    state: str = Field(default="", description="종목상태", max_length=40)
    marketCode: str = Field(default="", description="시장구분코드", max_length=20)
    marketName: str = Field(default="", description="시장명", max_length=20)
    upName: str = Field(default="", description="업종명", max_length=20)
    upSizeName: str = Field(default="", description="회사크기분류", max_length=20)
    companyClassName: str = Field(default="", description="회사분류", max_length=20)  # 코스닥만 존재함
    orderWarning: str = Field(
        default="", description="투자유의종목여부", max_length=20
    )  # 0: 해당없음, 2: 정리매매, 3: 단기과열, 4: 투자위험, 5: 투자경과, 1: ETF투자주의요망(ETF인 경우만 전달
    nxtEnable: str = Field(default="", description="NXT가능여부", max_length=20)  # Y: 가능


class DomesticStockInfoSummary(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="종목정보리스트 응답")

    list: List[DomesticStockInfoSummaryItem] = Field(default_factory=list, description="종목 리스트", max_length=3000)


class DomesticStockInfoBasicV1(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="종목정보조회 응답")

    code: str = Field(default="", description="종목코드", max_length=20)
    name: str = Field(default="", description="종목명", max_length=20)
    listCount: str = Field(default="", description="상장주식수", max_length=20)
    auditInfo: str = Field(default="", description="감리구분", max_length=20)
    regDay: str = Field(default="", description="상장일", max_length=20)
    lastPrice: str = Field(default="", description="전일종가", max_length=20)
    state: str = Field(default="", description="종목상태", max_length=20)
    marketCode: str = Field(default="", description="시장구분코드", max_length=20)
    marketName: str = Field(default="", description="시장명", max_length=20)
    upName: str = Field(default="", description="업종명", max_length=20)
    upSizeName: str = Field(default="", description="회사크기분류", max_length=20)
    companyClassName: str = Field(default="", description="회사분류", max_length=20)  # 코스닥만 존재함
    orderWarning: str = Field(
        default="", description="투자유의종목여부", max_length=20
    )  # 0: 해당없음, 2: 정리매매, 3: 단기과열, 4: 투자위험, 5: 투자경과, 1: ETF투자주의요망(ETF인 경우만 전달
    nxtEnable: str = Field(default="", description="NXT가능여부", max_length=20)  # Y: 가능


class DomesticStockInfoIndustryCodeItem(BaseModel):
    code: str = Field(default="", description="업종코드", max_length=20)
    name: str = Field(default="", description="업종명", max_length=20)
    group: str = Field(default="", description="그룹", max_length=20)
    marketCode: str = Field(default="", description="시장구분코드", max_length=20)  # KOSPI, KOSDAQ, KONEX


class DomesticStockInfoIndustryCode(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="업종코드리스트 요청 응답")

    list: List[DomesticStockInfoIndustryCodeItem] = Field(
        default_factory=list, description="업종코드 리스트", max_length=1000
    )


class DomesticStockInfoMemberCompanyItem(BaseModel):
    code: str = Field(default="", description="회원사 코드", max_length=20)
    name: str = Field(default="", description="회원사명", max_length=20)
    gb: str = Field(default="", description="구분", max_length=20)  # KOSPI, KOSDAQ, KONEX


class DomesticStockInfoMemberCompany(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="회원사코드리스트 요청 응답")

    list: List[DomesticStockInfoMemberCompanyItem] = Field(
        default_factory=list, description="회원사 코드 리스트", max_length=1000
    )


class DomesticStockInfoTop50ProgramNetBuyItem(BaseModel):
    rank: str = Field(default="", description="순위", max_length=20)
    stk_cd: str = Field(default="", description="종목코드", max_length=20)
    stk_nm: str = Field(default="", description="종목명", max_length=40)
    cur_prc: str = Field(default="", description="현재가", max_length=20)
    flu_sig: str = Field(default="", description="등락기호", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    flu_rt: str = Field(default="", description="등락율", max_length=20)
    acc_trde_qty: str = Field(default="", description="누적거래량", max_length=20)
    prm_sell_amt: str = Field(default="", description="프로그램매도금액", max_length=20)
    prm_buy_amt: str = Field(default="", description="프로그램매수금액", max_length=20)
    prm_netprps_amt: str = Field(default="", description="프로그램순매수금액", max_length=20)


class DomesticStockInfoTop50ProgramNetBuy(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="프로그램순매수상위50요청 응답")

    prm_netprps_upper_50: List[DomesticStockInfoTop50ProgramNetBuyItem] = Field(
        default_factory=list, description="프로그램 순매수 상위 50", max_length=1000
    )


class DomesticStockInfoProgramTradingStatusByStockItem(BaseModel):
    stk_cd: str = Field(default="", description="종목코드", max_length=20)
    stk_nm: str = Field(default="", description="종목명", max_length=40)
    cur_prc: str = Field(default="", description="현재가", max_length=20)
    flu_sig: str = Field(default="", description="등락기호", max_length=20)
    pred_pre: str = Field(default="", description="전일대비", max_length=20)
    buy_cntr_qty: str = Field(default="", description="매수체결수량", max_length=20)
    buy_cntr_amt: str = Field(default="", description="매수체결금액", max_length=20)
    sel_cntr_qty: str = Field(default="", description="매도체결수량", max_length=20)
    sel_cntr_amt: str = Field(default="", description="매도체결금액", max_length=20)
    netprps_prica: str = Field(default="", description="순매수대금", max_length=20)
    all_trde_rt: str = Field(default="", description="전체거래비율", max_length=20)


class DomesticStockInfoProgramTradingStatusByStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="종목별프로그램매매현황요청 응답")

    stk_prm_trde_prst: List[DomesticStockInfoTop50ProgramNetBuyItem] = Field(
        default_factory=list, description="종목별 프로그램 매매 현황", max_length=1000
    )
    tot_1: str = Field(default="", description="매수체결수량합계", max_length=20)
    tot_2: str = Field(default="", description="매수체결금액합계", max_length=20)
    tot_3: str = Field(default="", description="매도체결수량합계", max_length=20)
    tot_4: str = Field(default="", description="매도체결금액합계", max_length=20)
    tot_5: str = Field(default="", description="순매수대금합계", max_length=20)
    tot_6: str = Field(default="", description="합계6", max_length=20)
