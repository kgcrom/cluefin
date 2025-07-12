from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

from cluefin_openapi.kiwoom._model import (
    KiwoomHttpBody,
)


class DomesticRankInfoTopRemainingOrderQuantityItem(BaseModel):
    stk_cd: str = Field(default="", title="종목코드", max_length=20)
    stk_nm: str = Field(default="", title="종목명", max_length=40)
    cur_prc: str = Field(default="", title="현재가", max_length=20)
    pred_pre_sig: str = Field(default="", title="전일대비기호", max_length=20)
    pred_pre: str = Field(default="", title="전일대비", max_length=20)
    trde_qty: str = Field(default="", title="거래량", max_length=20)
    tot_sel_req: str = Field(default="", title="총매도잔량", max_length=20)
    tot_buy_req: str = Field(default="", title="총매수잔량", max_length=20)
    netprps_req: str = Field(default="", title="순매수잔량", max_length=20)
    buy_rt: str = Field(default="", title="매수비율", max_length=20)


class DomesticRankInfoTopRemainingOrderQuantity(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="호가잔량상위요청 응답")

    bid_req_upper: list[DomesticRankInfoTopRemainingOrderQuantityItem] = Field(
        default_factory=list, title="호가잔량상위"
    )


class DomesticRankInfoRapidlyIncreasingRemainingOrderQuantityItem(BaseModel):
    stk_cd: str = Field(default="", title="종목코드", max_length=20)
    stk_nm: str = Field(default="", title="종목명", max_length=40)
    cur_prc: str = Field(default="", title="현재가", max_length=20)
    pred_pre_sig: str = Field(default="", title="전일대비기호", max_length=20)
    pred_pre: str = Field(default="", title="전일대비", max_length=20)
    base_rate: str = Field(default="", title="기준률", max_length=20, alias="int")
    now: str = Field(default="", title="현재", max_length=20)
    sdnin_qty: str = Field(default="", title="급증수량", max_length=20)
    sdnin_rt: str = Field(default="", title="급증률", max_length=20)
    tot_buy_qty: str = Field(default="", title="총매수량", max_length=20)


class DomesticRankInfoRapidlyIncreasingRemainingOrderQuantity(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="호가잔량급증요청 응답")

    bid_req_sdnin: list[DomesticRankInfoRapidlyIncreasingRemainingOrderQuantityItem] = Field(
        default_factory=list, title="호가잔량급증"
    )


class DomesticRankInfoRapidlyIncreasingTotalSellOrdersItem(BaseModel):
    stk_cd: str = Field(default="", title="종목코드", max_length=20)
    stk_nm: str = Field(default="", title="종목명", max_length=40)
    cur_prc: str = Field(default="", title="현재가", max_length=20)
    pred_pre_sig: str = Field(default="", title="전일대비기호", max_length=20)
    pred_pre: str = Field(default="", title="전일대비", max_length=20)
    base_rate: str = Field(default="", title="기준률", max_length=20, alias="int")
    now_rt: str = Field(default="", title="현재비율", max_length=20)
    sdnin_rt: str = Field(default="", title="급증률", max_length=20)
    tot_sel_req: str = Field(default="", title="총매도잔량", max_length=20)
    tot_buy_req: str = Field(default="", title="총매수잔량", max_length=20)


class DomesticRankInfoRapidlyIncreasingTotalSellOrders(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="잔량율급증요청 응답")

    req_rt_sdnin: list[DomesticRankInfoRapidlyIncreasingRemainingOrderQuantityItem] = Field(
        default_factory=list, title="잔량율급증요청"
    )


class DomesticRankInfoRapidlyIncreasingTradingVolumeItem(BaseModel):
    stk_cd: str = Field(default="", title="종목코드", max_length=20)
    stk_nm: str = Field(default="", title="종목명", max_length=40)
    cur_prc: str = Field(default="", title="현재가", max_length=20)
    pred_pre_sig: str = Field(default="", title="전일대비기호", max_length=20)
    pred_pre: str = Field(default="", title="전일대비", max_length=20)
    flu_rt: str = Field(default="", title="등락률", max_length=20)
    prev_trde_qty: str = Field(default="", title="이전거래량", max_length=20)
    now_trde_qty: str = Field(default="", title="현재거래량", max_length=20)
    sdnin_qty: str = Field(default="", title="급증량", max_length=20)
    sdnin_rt: str = Field(default="", title="급증률", max_length=20)


class DomesticRankInfoRapidlyIncreasingTradingVolume(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="거래량급증요청 응답")

    trde_qty_sdnin: list[DomesticRankInfoRapidlyIncreasingTradingVolumeItem] = Field(
        default_factory=list, title="거래량급증요청"
    )


class DomesticRankInfoTopPercentageChangeFromPreviousDayItem(BaseModel):
    stk_cls: str = Field(default="", title="종목분류", max_length=20)
    stk_cd: str = Field(default="", title="종목코드", max_length=20)
    stk_nm: str = Field(default="", title="종목명", max_length=40)
    cur_prc: str = Field(default="", title="현재가", max_length=20)
    pred_pre_sig: str = Field(default="", title="전일대비기호", max_length=20)
    pred_pre: str = Field(default="", title="전일대비", max_length=20)
    flu_rt: str = Field(default="", title="등락률", max_length=20)
    sel_req: str = Field(default="", title="매도잔량", max_length=20)
    buy_req: str = Field(default="", title="매수잔량", max_length=20)
    now_trde_qty: str = Field(default="", title="현재거래량", max_length=20)
    cntr_str: str = Field(default="", title="체결강도", max_length=20)
    cnt: str = Field(default="", title="횟수", max_length=20)


class DomesticRankInfoTopPercentageChangeFromPreviousDay(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="전일대비상위요청 응답")

    pred_pre_flu_rt_upper: list[DomesticRankInfoTopPercentageChangeFromPreviousDayItem] = Field(
        default_factory=list, title="전일대비상위요청"
    )


class DomesticRankInfoTopExpectedConclusionPercentageChangeItem(BaseModel):
    stk_cd: str = Field(default="", title="종목코드", max_length=20)
    stk_nm: str = Field(default="", title="종목명", max_length=40)
    exp_cntr_pric: str = Field(default="", title="예상체결가", max_length=20)
    base_pric: str = Field(default="", title="기준가", max_length=20)
    pred_pre_sig: str = Field(default="", title="전일대비기호", max_length=20)
    pred_pre: str = Field(default="", title="전일대비", max_length=20)
    flu_rt: str = Field(default="", title="등락률", max_length=20)
    exp_cntr_qty: str = Field(default="", title="예상체결량", max_length=20)
    sel_req: str = Field(default="", title="매도잔량", max_length=20)
    sel_bid: str = Field(default="", title="매도호가", max_length=20)
    buy_bid: str = Field(default="", title="매수호가", max_length=20)
    buy_req: str = Field(default="", title="매수잔량", max_length=20)


class DomesticRankInfoTopExpectedConclusionPercentageChange(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="예상체결률상위요청 응답")

    exp_cntr_flu_rt_upper: list[DomesticRankInfoTopExpectedConclusionPercentageChangeItem] = Field(
        default_factory=list, title="예상체결률상위요청"
    )


class DomesticRankInfoTopCurrentDayTradingVolumeItem(BaseModel):
    stk_cd: str = Field(default="", title="종목코드", max_length=20)
    stk_nm: str = Field(default="", title="종목명", max_length=40)
    cur_prc: str = Field(default="", title="현재가", max_length=20)
    pred_pre_sig: str = Field(default="", title="전일대비기호", max_length=20)
    pred_pre: str = Field(default="", title="전일대비", max_length=20)
    flu_rt: str = Field(default="", title="등락률", max_length=20)
    trde_qty: str = Field(default="", title="거래량", max_length=20)
    pred_rt: str = Field(default="", title="전일비", max_length=20)
    trde_tern_rt: str = Field(default="", title="거래회전율", max_length=20)
    trde_amt: str = Field(default="", title="거래금액", max_length=20)
    opmr_trde_qty: str = Field(default="", title="장중거래량", max_length=20)
    opmr_pred_rt: str = Field(default="", title="장중전일비", max_length=20)
    opmr_trde_rt: str = Field(default="", title="장중거래회전율", max_length=20)
    opmr_trde_amt: str = Field(default="", title="장중거래금액", max_length=20)
    af_mkrt_trde_qty: str = Field(default="", title="장후거래량", max_length=20)
    af_mkrt_pred_rt: str = Field(default="", title="장후전일비", max_length=20)
    af_mkrt_trde_rt: str = Field(default="", title="장후거래회전율", max_length=20)
    af_mkrt_trde_amt: str = Field(default="", title="장후거래금액", max_length=20)
    bf_mkrt_trde_qty: str = Field(default="", title="장전거래량", max_length=20)
    bf_mkrt_pred_rt: str = Field(default="", title="장전전일비", max_length=20)
    bf_mkrt_trde_rt: str = Field(default="", title="장전거래회전율", max_length=20)
    bf_mkrt_pred_rt: str = Field(default="", title="장전거래금액", max_length=20)


class DomesticRankInfoTopCurrentDayTradingVolume(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="당일거래량상위요청 응답")

    tdy_trde_qty_upper: list[DomesticRankInfoTopCurrentDayTradingVolumeItem] = Field(
        default_factory=list, title="당일거래량상위요청"
    )


class DomesticRankInfoTopPreviousDayTradingVolumeItem(BaseModel):
    stk_cd: str = Field(default="", title="종목코드", max_length=20)
    stk_nm: str = Field(default="", title="종목명", max_length=40)
    cur_prc: str = Field(default="", title="현재가", max_length=20)
    pred_pre_sig: str = Field(default="", title="전일대비기호", max_length=20)
    pred_pre: str = Field(default="", title="전일대비", max_length=20)
    trde_qty: str = Field(default="", title="거래량", max_length=20)


class DomesticRankInfoTopPreviousDayTradingVolume(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="전일거래량상위요청 응답")

    pred_trde_qty_upper: list[DomesticRankInfoTopPreviousDayTradingVolumeItem] = Field(
        default_factory=list, title="전일거래량상위요청"
    )


class DomesticRankInfoTopTransactionValueItem(BaseModel):
    stk_cd: str = Field(default="", title="종목코드", max_length=20)
    now_rank: str = Field(default="", title="현재순위", max_length=20)
    pred_rank: str = Field(default="", title="전일순위", max_length=20)
    stk_nm: str = Field(default="", title="종목명", max_length=40)
    cur_prc: str = Field(default="", title="현재가", max_length=20)
    pred_pre_sig: str = Field(default="", title="전일대비기호", max_length=20)
    pred_pre: str = Field(default="", title="전일대비", max_length=20)
    flu_rt: str = Field(default="", title="등락률", max_length=20)
    sel_bid: str = Field(default="", title="매도호가", max_length=20)
    buy_bid: str = Field(default="", title="매수호가", max_length=20)
    now_trde_qty: str = Field(default="", title="현재거래량", max_length=20)
    pred_trde_qty: str = Field(default="", title="전일거래량", max_length=20)
    trde_prica: str = Field(default="", title="거래대금", max_length=20)


class DomesticRankInfoTopTransactionValue(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="거래대금상위요청 응답")

    trde_prica_upper: list[DomesticRankInfoTopTransactionValueItem] = Field(
        default_factory=list, title="거래대금상위요청"
    )


class DomesticRankInfoTopMarginRatioItem(BaseModel):
    stk_infr: str = Field(default="", title="종목정보", max_length=20)
    stk_cd: str = Field(default="", title="종목코드", max_length=20)
    stk_nm: str = Field(default="", title="종목명", max_length=40)
    cur_prc: str = Field(default="", title="현재가", max_length=20)
    pred_pre_sig: str = Field(default="", title="전일대비기호", max_length=20)
    pred_pre: str = Field(default="", title="전일대비", max_length=20)
    flu_rt: str = Field(default="", title="등락률", max_length=20)
    crd_rt: str = Field(default="", title="신용비율", max_length=20)
    sel_req: str = Field(default="", title="매도잔량", max_length=20)
    buy_req: str = Field(default="", title="매수잔량", max_length=20)
    now_trde_qty: str = Field(default="", title="현재거래량", max_length=20)


class DomesticRankInfoTopMarginRatio(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="신용비율상위요청 응답")

    crd_rt_upper: list[DomesticRankInfoTopMarginRatioItem] = Field(default_factory=list, title="신용비율상위요청")


class DomesticRankInfoTopForeignerPeriodTradingItem(BaseModel):
    rank: str = Field(default="", title="순위", max_length=20)
    stk_cd: str = Field(default="", title="종목코드", max_length=20)
    stk_nm: str = Field(default="", title="종목명", max_length=40)
    cur_prc: str = Field(default="", title="현재가", max_length=20)
    pred_pre_sig: str = Field(default="", title="전일대비기호", max_length=20)
    pred_pre: str = Field(default="", title="전일대비", max_length=20)
    sel_bid: str = Field(default="", title="매도호가", max_length=20)
    buy_bid: str = Field(default="", title="매수호가", max_length=20)
    trde_qty: str = Field(default="", title="거래량", max_length=20)
    netprps_qty: str = Field(default="", title="순매수량", max_length=20)
    gain_pos_stkcnt: str = Field(default="", title="취득가능주식수", max_length=20)


class DomesticRankInfoTopForeignerPeriodTrading(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="외인기간별매매상위요청 응답")

    for_dt_trde_upper: list[DomesticRankInfoTopForeignerPeriodTradingItem] = Field(
        default_factory=list, title="외인기간별매매상위요청"
    )


class DomesticRankInfoTopConsecutiveNetBuySellByForeignersItem(BaseModel):
    stk_cd: str = Field(default="", title="종목코드", max_length=20)
    stk_nm: str = Field(default="", title="종목명", max_length=40)
    cur_prc: str = Field(default="", title="현재가", max_length=20)
    pred_pre_sig: str = Field(default="", title="전일대비기호", max_length=20)
    pred_pre: str = Field(default="", title="전일대비", max_length=20)
    dm1: str = Field(default="", title="D-1", max_length=20)
    dm2: str = Field(default="", title="D-2", max_length=20)
    dm3: str = Field(default="", title="D-3", max_length=20)
    tot: str = Field(default="", title="합계", max_length=20)
    limit_exh_rt: str = Field(default="", title="한도소진율", max_length=20)
    pred_pre_1: str = Field(default="", title="전일대비1", max_length=20)
    pred_pre_2: str = Field(default="", title="전일대비2", max_length=20)
    pred_pre_3: str = Field(default="", title="전일대비3", max_length=20)


class DomesticRankInfoTopConsecutiveNetBuySellByForeigners(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="외인연속순매수매도상위요청 응답")

    for_cont_nettrde_upper: list[DomesticRankInfoTopConsecutiveNetBuySellByForeignersItem] = Field(
        default_factory=list, title="외인연속순매수매도상위요청"
    )


class DomesticRankInfoTopLimitExhaustionRateForeignerItem(BaseModel):
    rank: str = Field(default="", title="순위", max_length=20)
    stk_cd: str = Field(default="", title="종목코드", max_length=20)
    stk_nm: str = Field(default="", title="종목명", max_length=40)
    cur_prc: str = Field(default="", title="현재가", max_length=20)
    pred_pre_sig: str = Field(default="", title="전일대비기호", max_length=20)
    pred_pre: str = Field(default="", title="전일대비", max_length=20)
    trde_qty: str = Field(default="", title="거래량", max_length=20)
    poss_stkcnt: str = Field(default="", title="보유주식수", max_length=20)
    gain_pos_stkcnt: str = Field(default="", title="취득가능주식수", max_length=20)
    base_limit_exh_rt: str = Field(default="", title="기준한도소진율", max_length=20)
    limit_exh_rt: str = Field(default="", title="한도소진율", max_length=20)
    exh_rt_incrs: str = Field(default="", title="소진율증가", max_length=20)


class DomesticRankInfoTopLimitExhaustionRateForeigner(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="외인한도소진율상위요청 응답")

    for_limit_exh_rt_incrs_upper: list[DomesticRankInfoTopLimitExhaustionRateForeignerItem] = Field(
        default_factory=list, title="외인한도소진율상위요청"
    )


class DomesticRankInfoTopForeignAccountGroupTradingItem(BaseModel):
    rank: str = Field(default="", title="순위", max_length=20)
    stk_cd: str = Field(default="", title="종목코드", max_length=20)
    stk_nm: str = Field(default="", title="종목명", max_length=40)
    cur_prc: str = Field(default="", title="현재가", max_length=20)
    pred_pre_sig: str = Field(default="", title="전일대비기호", max_length=20)
    pred_pre: str = Field(default="", title="전일대비", max_length=20)
    flu_rt: str = Field(default="", title="등락률", max_length=20)
    sel_trde_qty: str = Field(default="", title="매도거래량", max_length=20)
    buy_trde_qty: str = Field(default="", title="매수거래량", max_length=20)
    netprps_trde_qty: str = Field(default="", title="순매수거래량", max_length=20)
    netprps_prica: str = Field(default="", title="순매수대금", max_length=20)
    trde_qty: str = Field(default="", title="거래량", max_length=20)
    trde_prica: str = Field(default="", title="거래대금", max_length=20)


class DomesticRankInfoTopForeignAccountGroupTrading(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="외인계좌그룹별매매상위요청 응답")

    frgn_wicket_trde_upper: list[DomesticRankInfoTopForeignAccountGroupTradingItem] = Field(
        default_factory=list, title="외인계좌그룹별매매상위요청"
    )


class DomesticRankInfoStockSpecificSecuritiesFirmRankingItem(BaseModel):
    rank: str = Field(default="", title="순위", max_length=20)
    mmcm_nm: str = Field(default="", title="회원사명", max_length=20)
    buy_qty: str = Field(default="", title="매수수량", max_length=20)
    sell_qty: str = Field(default="", title="매도수량", max_length=20)
    acc_netprps_qty: str = Field(default="", title="누적순매수수량", max_length=20)


class DomesticRankInfoStockSpecificSecuritiesFirmRanking(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="종목별증권사순위요청 응답")

    rank_1: str = Field(default="", title="순위1", max_length=20)
    rank_2: str = Field(default="", title="순위2", max_length=20)
    rank_3: str = Field(default="", title="순위3", max_length=20)
    prid_trde_qty: str = Field(default="", title="기간중거래량", max_length=20)
    stk_sec_rank: list[DomesticRankInfoStockSpecificSecuritiesFirmRankingItem] = Field(
        default_factory=list, title="종목별증권사순위"
    )


class DomesticRankInfoTopSecuritiesFirmTradingItem(BaseModel):
    rank: str = Field(default="", title="순위", max_length=20)
    stk_cd: str = Field(default="", title="종목코드", max_length=20)
    stk_nm: str = Field(default="", title="종목명", max_length=40)
    prid_stkpc_flu: str = Field(default="", title="기간중주가등락", max_length=20)
    flu_rt: str = Field(default="", title="등락율", max_length=20)
    prid_trde_qty: str = Field(default="", title="기간중거래량", max_length=20)
    netprps: str = Field(default="", title="순매수", max_length=20)
    buy_trde_qty: str = Field(default="", title="매수거래량", max_length=20)
    sel_trde_qty: str = Field(default="", title="매도거래량", max_length=20)


class DomesticRankInfoTopSecuritiesFirmTrading(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="증권사별매매상위요청 응답")

    sec_trde_upper: list[DomesticRankInfoTopSecuritiesFirmTradingItem] = Field(
        default_factory=list, title="증권사별매매상위요청"
    )


class DomesticRankInfoTopCurrentDayMajorTradersItem(BaseModel):
    sel_scesn_tm: str = Field(default="", title="매도이탈시간", max_length=20)
    sell_qty: str = Field(default="", title="매도수량", max_length=20)
    sel_upper_scesn_ori: str = Field(default="", title="매도상위이탈원", max_length=20)
    buy_scesn_tm: str = Field(default="", title="매수이탈시간", max_length=20)
    buy_qty: str = Field(default="", title="매수수량", max_length=20)
    buy_upper_scesn_ori: str = Field(default="", title="매수상위이탈원", max_length=20)
    qry_dt: str = Field(default="", title="조회일자", max_length=20)
    qry_tm: str = Field(default="", title="조회시간", max_length=20)


class DomesticRankInfoTopCurrentDayMajorTraders(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="당일주요거래원요청 응답")

    sel_trde_ori_irds_1: str = Field(default="", title="매도거래원별증감1", max_length=20)
    sel_trde_ori_qty_1: str = Field(default="", title="매도거래원수량1", max_length=20)
    sel_trde_ori_1: str = Field(default="", title="매도거래원1", max_length=20)
    sel_trde_ori_cd_1: str = Field(default="", title="매도거래원코드1", max_length=20)
    buy_trde_ori_1: str = Field(default="", title="매수거래원1", max_length=20)
    buy_trde_ori_cd_1: str = Field(default="", title="매수거래원코드1", max_length=20)
    buy_trde_ori_qty_1: str = Field(default="", title="매수거래원수량1", max_length=20)
    buy_trde_ori_irds_1: str = Field(default="", title="매수거래원별증감1", max_length=20)
    sel_trde_ori_irds_2: str = Field(default="", title="매도거래원별증감2", max_length=20)
    sel_trde_ori_qty_2: str = Field(default="", title="매도거래원수량2", max_length=20)
    sel_trde_ori_2: str = Field(default="", title="매도거래원2", max_length=20)
    sel_trde_ori_cd_2: str = Field(default="", title="매도거래원코드2", max_length=20)
    buy_trde_ori_2: str = Field(default="", title="매수거래원2", max_length=20)
    buy_trde_ori_cd_2: str = Field(default="", title="매수거래원코드2", max_length=20)
    buy_trde_ori_qty_2: str = Field(default="", title="매수거래원수량2", max_length=20)
    buy_trde_ori_irds_2: str = Field(default="", title="매수거래원별증감2", max_length=20)
    sel_trde_ori_irds_3: str = Field(default="", title="매도거래원별증감3", max_length=20)
    sel_trde_ori_qty_3: str = Field(default="", title="매도거래원수량3", max_length=20)
    sel_trde_ori_3: str = Field(default="", title="매도거래원3", max_length=20)
    sel_trde_ori_cd_3: str = Field(default="", title="매도거래원코드3", max_length=20)
    buy_trde_ori_3: str = Field(default="", title="매수거래원3", max_length=20)
    buy_trde_ori_cd_3: str = Field(default="", title="매수거래원코드3", max_length=20)
    buy_trde_ori_qty_3: str = Field(default="", title="매수거래원수량3", max_length=20)
    buy_trde_ori_irds_3: str = Field(default="", title="매수거래원별증감3", max_length=20)
    sel_trde_ori_irds_4: str = Field(default="", title="매도거래원별증감4", max_length=20)
    sel_trde_ori_qty_4: str = Field(default="", title="매도거래원수량4", max_length=20)
    sel_trde_ori_4: str = Field(default="", title="매도거래원4", max_length=20)
    sel_trde_ori_cd_4: str = Field(default="", title="매도거래원코드4", max_length=20)
    buy_trde_ori_4: str = Field(default="", title="매수거래원4", max_length=20)
    buy_trde_ori_cd_4: str = Field(default="", title="매수거래원코드4", max_length=20)
    buy_trde_ori_qty_4: str = Field(default="", title="매수거래원수량4", max_length=20)
    buy_trde_ori_irds_4: str = Field(default="", title="매수거래원별증감4", max_length=20)
    sel_trde_ori_irds_5: str = Field(default="", title="매도거래원별증감5", max_length=20)
    sel_trde_ori_qty_5: str = Field(default="", title="매도거래원수량5", max_length=20)
    sel_trde_ori_5: str = Field(default="", title="매도거래원5", max_length=20)
    sel_trde_ori_cd_5: str = Field(default="", title="매도거래원코드5", max_length=20)
    buy_trde_ori_5: str = Field(default="", title="매수거래원5", max_length=20)
    buy_trde_ori_cd_5: str = Field(default="", title="매수거래원코드5", max_length=20)
    buy_trde_ori_qty_5: str = Field(default="", title="매수거래원수량5", max_length=20)
    buy_trde_ori_irds_5: str = Field(default="", title="매수거래원별증감5", max_length=20)
    frgn_sel_prsm_sum_chang: str = Field(default="", title="외국계매도추정합변동", max_length=20)
    frgn_sel_prsm_sum: str = Field(default="", title="외국계매도추정합", max_length=20)
    frgn_buy_prsm_sum: str = Field(default="", title="외국계매수추정합", max_length=20)
    frgn_buy_prsm_sum_chang: str = Field(default="", title="외국계매수추정합변동", max_length=20)
    tdy_main_trde_ori: list[DomesticRankInfoTopCurrentDayMajorTradersItem] = Field(
        default_factory=list, title="당일주요거래원"
    )


class DomesticRankInfoTopNetBuyTraderRankingItem(BaseModel):
    rank: str = Field(default="", title="순위", max_length=20)
    mmcm_cd: str = Field(default="", title="회원사코드", max_length=20)
    mmcm_nm: str = Field(default="", title="회원사명", max_length=20)


class DomesticRankInfoTopNetBuyTraderRanking(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="순매수거래원순위요청 응답")

    netprps_trde_ori_rank: list[DomesticRankInfoTopNetBuyTraderRankingItem] = Field(
        default_factory=list, title="순매수거래원순위요청"
    )


class DomesticRankInfoTopCurrentDayDeviationSourcesItem(BaseModel):
    sel_scesn_tm: str = Field(default="", title="매도이탈시간", max_length=20)
    sell_qty: str = Field(default="", title="매도수량", max_length=20)
    sel_upper_scesn_ori: str = Field(default="", title="매도상위이탈원", max_length=20)
    buy_scesn_tm: str = Field(default="", title="매수이탈시간", max_length=20)
    buy_qty: str = Field(default="", title="매수수량", max_length=20)
    buy_upper_scesn_ori: str = Field(default="", title="매수상위이탈원", max_length=20)
    qry_dt: str = Field(default="", title="조회일자", max_length=20)
    qry_tm: str = Field(default="", title="조회시간", max_length=20)


class DomesticRankInfoTopCurrentDayDeviationSources(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="당일상위이탈원천 응답")

    tdy_upper_scesn_ori: list[DomesticRankInfoTopCurrentDayDeviationSourcesItem] = Field(
        default_factory=list, title="당일상위이탈원천"
    )


class DomesticRankInfoSameNetBuySellRanking(BaseModel):
    stk_cd: str = Field(default="", title="종목코드", max_length=20)
    rank: str = Field(default="", title="순위", max_length=20)
    stk_nm: str = Field(default="", title="종목명", max_length=40)
    cur_prc: str = Field(default="", title="현재가", max_length=20)
    pred_pre_sig: str = Field(default="", title="전일대비기호", max_length=20)
    pred_pre: str = Field(default="", title="전일대비", max_length=20)
    flu_rt: str = Field(default="", title="등락률", max_length=20)
    acc_trde_qty: str = Field(default="", title="누적거래량", max_length=20)
    orgn_nettrde_qty: str = Field(default="", title="기관순매매수량", max_length=20)
    orgn_nettrde_amt: str = Field(default="", title="기관순매매금액", max_length=20)
    orgn_nettrde_avg_pric: str = Field(default="", title="기관순매매평균가", max_length=20)
    for_nettrde_qty: str = Field(default="", title="외인순매매수량", max_length=20)
    for_nettrde_amt: str = Field(default="", title="외인순매매금액", max_length=20)
    for_nettrde_avg_pric: str = Field(default="", title="외인순매매평균가", max_length=20)
    for_nettrde_qty: str = Field(default="", title="순매매수량", max_length=20)
    for_nettrde_amt: str = Field(default="", title="순매매금액", max_length=20)
    for_nettrde_avg_pric: str = Field(default="", title="순매매평균가", max_length=20)
    nettrde_qty: str = Field(default="", title="순매매수량", max_length=20)
    nettrde_amt: str = Field(default="", title="순매매금액", max_length=20)


class DomesticRankInfoSameNetBuySellRanking(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="동일순매매상위요청 응답")

    eql_nettrde_rank: list[DomesticRankInfoSameNetBuySellRanking] = Field(default_factory=list, title="동일순매매상위")


class DomesticRankInfoTopIntradayTradingByInvestorItem(BaseModel):
    stk_cd: str = Field(default="", title="종목코드", max_length=20)
    stk_nm: str = Field(default="", title="종목명", max_length=40)
    sel_qty: str = Field(default="", title="매도량", max_length=20)
    buy_qty: str = Field(default="", title="매수량", max_length=20)
    netslmt: str = Field(default="", title="순매도", max_length=20)


class DomesticRankInfoTopIntradayTradingByInvestor(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="장중투자자별매매상위요청 응답")

    opmr_invsr_trde_upper: list[DomesticRankInfoTopIntradayTradingByInvestorItem] = Field(
        default_factory=list, title="장중투자자별매매상위"
    )


class DomesticRankInfoAfterHoursSinglePriceChangeRateRankingItem(BaseModel):
    rank: str = Field(default="", title="순위", max_length=20)
    stk_cd: str = Field(default="", title="종목코드", max_length=20)
    stk_nm: str = Field(default="", title="종목명", max_length=40)
    cur_prc: str = Field(default="", title="현재가", max_length=20)
    pred_pre_sig: str = Field(default="", title="전일대비기호", max_length=20)
    pred_pre: str = Field(default="", title="전일대비", max_length=20)
    flu_rt: str = Field(default="", title="등락률", max_length=20)
    sel_tot_req: str = Field(default="", title="매도총잔량", max_length=20)
    buy_tot_req: str = Field(default="", title="매수총잔량", max_length=20)
    acc_trde_qty: str = Field(default="", title="누적거래량", max_length=20)
    acc_trde_prica: str = Field(default="", title="누적거래대금", max_length=20)
    tdy_close_pric: str = Field(default="", title="당일종가", max_length=20)
    tdy_close_pric_flu_rt: str = Field(default="", title="당일종가등락률", max_length=20)


class DomesticRankInfoAfterHoursSinglePriceChangeRateRanking(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="시간외단일가등락율순위요청 응답")

    ovt_sigpric_flu_rt_rank: list[DomesticRankInfoAfterHoursSinglePriceChangeRateRankingItem] = Field(
        default_factory=list, title="시간외단일가등락율순위"
    )


class DomesticRankInfoTopForeignerLimitExhaustionRateItem(BaseModel):
    for_netslmt_stk_cd: str = Field(default="", title="외인순매도종목코드", max_length=20)
    for_netslmt_stk_nm: str = Field(default="", title="외인순매도종목명", max_length=40)
    for_netslmt_amt: str = Field(default="", title="외인순매도금액", max_length=20)
    for_netslmt_qty: str = Field(default="", title="외인순매도수량", max_length=20)
    for_netprps_stk_cd: str = Field(default="", title="외인순매수종목코드", max_length=20)
    for_netprps_stk_nm: str = Field(default="", title="외인순매수종목명", max_length=40)
    for_netprps_amt: str = Field(default="", title="외인순매수금액", max_length=20)
    for_netprps_qty: str = Field(default="", title="외인순매수수량", max_length=20)
    orgn_netslmt_stk_cd: str = Field(default="", title="기관순매도종목코드", max_length=20)
    orgn_netslmt_stk_nm: str = Field(default="", title="기관순매도종목명", max_length=40)
    orgn_netslmt_amt: str = Field(default="", title="기관순매도금액", max_length=20)
    orgn_netslmt_qty: str = Field(default="", title="기관순매도수량", max_length=20)
    orgn_netprps_stk_cd: str = Field(default="", title="기관순매수종목코드", max_length=20)
    orgn_netprps_stk_nm: str = Field(default="", title="기관순매수종목명", max_length=40)
    orgn_netprps_amt: str = Field(default="", title="기관순매수금액", max_length=20)
    orgn_netprps_qty: str = Field(default="", title="기관순매수수량", max_length=20)


class DomesticRankInfoTopForeignerLimitExhaustionRate(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="외국인기관매매상위요청 응답")

    frgnr_orgn_trde_upper: list[DomesticRankInfoTopForeignerLimitExhaustionRateItem] = Field(
        default_factory=list, title="외국인기관매매상위"
    )
