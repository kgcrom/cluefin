from pydantic import BaseModel, ConfigDict, Field

from cluefin_openapi.kiwoom._model import (
    KiwoomHttpBody,
)


class DomesticAccountDailyStockRealizedProfitLossByDateItem(BaseModel):
    stk_nm: str = Field(default="", description="종목명", max_length=40)
    cntr_qty: str = Field(default="", description="체결량", max_length=20)
    buy_uv: str = Field(default="", description="매입단가", max_length=20)
    cntr_pric: str = Field(default="", description="체결가", max_length=20)
    tdy_sel_pl: str = Field(default="", description="당일매도손익", max_length=20)
    pl_rt: str = Field(default="", description="손익율", max_length=20)
    stk_cd: str = Field(default="", description="종목코드", max_length=20)
    tdy_trde_cmsn: str = Field(default="", description="당일매매수수료", max_length=20)
    tdy_trde_tax: str = Field(default="", description="당일매매세금", max_length=20)
    wthd_alowa: str = Field(default="", description="인출가능금액", max_length=20)
    loan_dt: str = Field(default="", description="대출일", max_length=20)
    crd_tp: str = Field(default="", description="신용구분", max_length=20)
    stk_cd_1: str = Field(default="", description="종목코드1", max_length=20)
    tdy_sel_pl_1: str = Field(default="", description="당일매도손익1", max_length=20)


class DomesticAccountDailyStockRealizedProfitLossByDate(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="일자별종목별실현속인요청 일자 응답")
    dt_stk_div_rlzt_pl: list[DomesticAccountDailyStockRealizedProfitLossByDateItem] = Field(
        default_factory=list,
        description="일자별종목별실현손익",
    )


class DomesticAccountDailyStockRealizedProfitLossByPeriodItem(BaseModel):
    dt: str = Field(default="", description="일자", max_length=20)
    tdy_htssel_cmsn: str = Field(default="", description="당일hts매도수수료", max_length=20)
    stk_nm: str = Field(default="", description="종목명", max_length=40)
    cntr_qty: str = Field(default="", description="체결량", max_length=20)
    buy_uv: str = Field(default="", description="매입단가", max_length=20)
    cntr_pric: str = Field(default="", description="체결가", max_length=20)
    tdy_sel_pl: str = Field(default="", description="당일매도손익", max_length=20)
    pl_rt: str = Field(default="", description="손익율", max_length=20)
    stk_cd: str = Field(default="", description="종목코드", max_length=20)
    tdy_trde_cmsn: str = Field(default="", description="당일매매수수료", max_length=20)
    tdy_trde_tax: str = Field(default="", description="당일매매세금", max_length=20)
    wthd_alowa: str = Field(default="", description="인출가능금액", max_length=20)
    loan_dt: str = Field(default="", description="대출일", max_length=20)
    crd_tp: str = Field(default="", description="신용구분", max_length=20)


class DomesticAccountDailyStockRealizedProfitLossByPeriod(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="일자별종목별실현손익요청 기간 응답")

    dt_stk_rlzt_pl: list[DomesticAccountDailyStockRealizedProfitLossByPeriodItem] = Field(
        default_factory=list,
        description="일자별종목별실현손익",
    )


class DomesticAccountDailyRealizedProfitLossItem(BaseModel):
    dt: str = Field(default="", description="일자", max_length=20)
    buy_amt: str = Field(default="", description="매수금액", max_length=20)
    sell_amt: str = Field(default="", description="매도금액", max_length=20)
    tdy_sel_pl: str = Field(default="", description="당일매도손익", max_length=20)
    tdy_trde_cmsn: str = Field(default="", description="당일매매수수료", max_length=20)
    tdy_trde_tax: str = Field(default="", description="당일매매세금", max_length=20)


class DomesticAccountDailyRealizedProfitLoss(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="일자별실현손익요청 응답")

    tot_buy_amt: str = Field(default="", description="총매수금액", max_length=20)
    tot_sell_amt: str = Field(default="", description="총매도금액", max_length=20)
    rlzt_pl: str = Field(default="", description="실현손익", max_length=20)
    trde_cmsn: str = Field(default="", description="매매수수료", max_length=20)
    trde_tax: str = Field(default="", description="매매세금", max_length=20)
    dt_rlzt_pl: list[DomesticAccountDailyRealizedProfitLossItem] = (
        Field(
            default_factory=list,
            description="일자별실현손익",
        ),
    )


class DomesticAccountUnexecutedItem(BaseModel):
    acnt_no: str = Field(default="", description="계좌번호", max_length=20)
    ord_no: str = Field(default="", description="주문번호", max_length=20)
    mang_empno: str = Field(default="", description="관리사번", max_length=20)
    stk_cd: str = Field(default="", description="종목코드", max_length=20)
    tsk_tp: str = Field(default="", description="업무구분", max_length=20)
    ord_stt: str = Field(default="", description="주문상태", max_length=20)
    stk_nm: str = Field(default="", description="종목명", max_length=40)
    ord_qty: str = Field(default="", description="주문수량", max_length=20)
    ord_pric: str = Field(default="", description="주문가격", max_length=20)
    oso_qty: str = Field(default="", description="미체결수량", max_length=20)
    cntr_tot_amt: str = Field(default="", description="체결누계금액", max_length=20)
    orig_ord_no: str = Field(default="", description="원주문번호", max_length=20)
    io_tp_nm: str = Field(default="", description="주문구분", max_length=20)
    trde_tp: str = Field(default="", description="매매구분", max_length=20)
    tm: str = Field(default="", description="시간", max_length=20)
    cntr_no: str = Field(default="", description="체결번호", max_length=20)
    cntr_pric: str = Field(default="", description="체결가", max_length=20)
    cntr_qty: str = Field(default="", description="체결량", max_length=20)
    cur_prc: str = Field(default="", description="현재가", max_length=20)
    sel_bid: str = Field(default="", description="매도호가", max_length=20)
    buy_bid: str = Field(default="", description="매수호가", max_length=20)
    unit_cntr_pric: str = Field(default="", description="단위체결가", max_length=20)
    unit_cntr_qty: str = Field(default="", description="단위체결량", max_length=20)
    tdy_trde_cmsn: str = Field(default="", description="당일매매수수료", max_length=20)
    tdy_trde_tax: str = Field(default="", description="당일매매세금", max_length=20)
    ind_invsr: str = Field(default="", description="개인투자자", max_length=20)
    stex_tp: str = Field(default="", description="거래소구분", max_length=20)
    stex_tp_txt: str = Field(default="", description="거래소구분텍스트", max_length=20)
    sor_yn: str = Field(default="", description="SOR 여부값", max_length=20)
    stop_pric: str = Field(default="", description="스톱가", max_length=20)


class DomesticAccountUnexecuted(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미체결요청 응답")

    oso: list[DomesticAccountUnexecutedItem] = Field(
        default_factory=list,
        description="미체결",
    )


class DomesticAccountExecutedItem(BaseModel):
    ord_no: str = Field(default="", description="주문번호", max_length=20)
    stk_nm: str = Field(default="", description="종목명", max_length=40)
    io_tp_nm: str = Field(default="", description="주문구분", max_length=20)
    ord_pric: str = Field(default="", description="주문가격", max_length=20)
    ord_qty: str = Field(default="", description="주문수량", max_length=20)
    cntr_pric: str = Field(default="", description="체결가", max_length=20)
    cntr_qty: str = Field(default="", description="체결량", max_length=20)
    oso_qty: str = Field(default="", description="미체결수량", max_length=20)
    tdy_trde_cmsn: str = Field(default="", description="당일매매수수료", max_length=20)
    tdy_trde_tax: str = Field(default="", description="당일매매세금", max_length=20)
    ord_stt: str = Field(default="", description="주문상태", max_length=20)
    trde_tp: str = Field(default="", description="매매구분", max_length=20)
    orig_ord_no: str = Field(default="", description="원주문번호", max_length=20)
    ord_tm: str = Field(default="", description="주문시간", max_length=20)
    stk_cd: str = Field(default="", description="종목코드", max_length=20)
    stex_tp: str = Field(default="", description="거래소구분", max_length=20)
    stex_tp_txt: str = Field(default="", description="거래소구분텍스트", max_length=20)
    sor_yn: str = Field(default="", description="SOR 여부값", max_length=20)
    stop_pric: str = Field(default="", description="스톱가", max_length=20)


class DomesticAccountExecuted(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="체결요청 응답")

    cntr: list[DomesticAccountExecutedItem] = Field(
        default_factory=list,
        description="체결",
    )


class DomesticAccountDailyRealizedProfitLossDetailsItem(BaseModel):
    stk_nm: str = Field(default="", description="종목명", max_length=40)
    cntr_qty: str = Field(default="", description="체결량", max_length=20)
    buy_uv: str = Field(default="", description="매입단가", max_length=20)
    cntr_pric: str = Field(default="", description="체결가", max_length=20)
    tdy_sel_pl: str = Field(default="", description="당일매도손익", max_length=20)
    pl_rt: str = Field(default="", description="손익율", max_length=20)
    tdy_trde_cmsn: str = Field(default="", description="당일매매수수료", max_length=20)
    tdy_trde_tax: str = Field(default="", description="당일매매세금", max_length=20)
    stk_cd: str = Field(default="", description="종목코드", max_length=20)


class DomesticAccountDailyRealizedProfitLossDetails(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="당일실현손익상세요청 응답")

    tdy_rlzt_pl: str = Field(default="", description="당일실현손익", max_length=20)
    tdy_rlzt_pl_dtl: list[DomesticAccountDailyRealizedProfitLossDetailsItem] = Field(
        default_factory=list,
        description="당일실현손익상세",
    )


class DomesticAccountProfitRateItem(BaseModel):
    dt: str = Field(default="", description="일자", max_length=20)
    stk_cd: str = Field(default="", description="종목코드", max_length=20)
    stk_nm: str = Field(default="", description="종목명", max_length=40)
    cur_prc: str = Field(default="", description="현재가", max_length=20)
    pur_pric: str = Field(default="", description="매입가", max_length=20)
    pur_amt: str = Field(default="", description="매입금액", max_length=20)
    rmnd_qty: str = Field(default="", description="보유수량", max_length=20)
    tdy_sel_pl: str = Field(default="", description="당일매도손익", max_length=20)
    tdy_trde_cmsn: str = Field(default="", description="당일매매수수료", max_length=20)
    tdy_trde_tax: str = Field(default="", description="당일매매세금", max_length=20)
    crd_tp: str = Field(default="", description="신용구분", max_length=20)
    loan_dt: str = Field(default="", description="대출일", max_length=20)
    setl_remn: str = Field(default="", description="결제잔고", max_length=20)
    clrn_alow_qty: str = Field(default="", description="청산가능수량", max_length=20)
    crd_amt: str = Field(default="", description="신용금액", max_length=20)
    crd_int: str = Field(default="", description="신용이자", max_length=20)
    expr_dt: str = Field(default="", description="만기일", max_length=20)


class DomesticAccountProfitRate(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="계좌수익률요청 응답")

    acnt_prft_rt: list[DomesticAccountProfitRateItem] = Field(
        default_factory=list,
        description="계좌수익률",
    )


class DomesticAccountUnexecutedSplitOrderDetailsItem(BaseModel):
    stk_cd: str = Field(default="", description="종목코드", max_length=20)
    stk_nm: str = Field(default="", description="종목명", max_length=40)
    ord_no: str = Field(default="", description="주문번호", max_length=20)
    ord_qty: str = Field(default="", description="주문수량", max_length=20)
    ord_pric: str = Field(default="", description="주문가격", max_length=20)
    osop_qty: str = Field(default="", description="미체결수량", max_length=20)
    io_tp_nm: str = Field(default="", description="주문구분", max_length=20)
    trde_tp: str = Field(default="", description="매매구분", max_length=20)
    sell_tp: str = Field(default="", description="매도/수 구분", max_length=20)
    cntr_qty: str = Field(default="", description="체결량", max_length=20)
    ord_stt: str = Field(default="", description="주문상태", max_length=20)
    cur_prc: str = Field(default="", description="현재가", max_length=20)
    stex_tp: str = Field(default="", description="거래소구분. 0 : 통합, 1 : KRX, 2 : NXT", max_length=20)
    stex_tp_txt: str = Field(default="", description="거래소구분텍스트", max_length=20)


class DomesticAccountUnexecutedSplitOrderDetails(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미체결분할주문상세 응답")

    osop: list[DomesticAccountUnexecutedSplitOrderDetailsItem] = Field(
        default_factory=list,
        description="미체결분할주문리스트",
    )


class DomesticAccountCurrentDayTradingJournalItem(BaseModel):
    stk_nm: str = Field(default="", description="종목명", max_length=40)
    buy_avg_pric: str = Field(default="", description="매수평균가", max_length=20)
    buy_qty: str = Field(default="", description="매수수량", max_length=20)
    sel_avg_pric: str = Field(default="", description="매도평균가", max_length=20)
    sell_qty: str = Field(default="", description="매도수량", max_length=20)
    cmsn_alm_tax: str = Field(default="", description="수수료_제세금", max_length=20)
    pl_amt: str = Field(default="", description="손익금액", max_length=20)
    sell_amt: str = Field(default="", description="매도금액", max_length=20)
    buy_amt: str = Field(default="", description="매수금액", max_length=20)
    prft_rt: str = Field(default="", description="수익률", max_length=20)
    stk_cd: str = Field(default="", description="종목코드", max_length=6)


class DomesticAccountCurrentDayTradingJournal(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="당일매매일지조회 응답")

    tot_sell_amt: str = Field(default="", description="총매도금액", max_length=20)
    tot_buy_amt: str = Field(default="", description="총매수금액", max_length=20)
    tot_cmsn_tax: str = Field(default="", description="총수수료_세금", max_length=20)
    tot_exct_amt: str = Field(default="", description="총정산금액", max_length=20)
    tot_pl_amt: str = Field(default="", description="총손익금액", max_length=20)
    tot_prft_rt: str = Field(default="", description="총수익률", max_length=20)
    tdy_trde_diary: list[DomesticAccountCurrentDayTradingJournalItem] = Field(
        default_factory=list,
        description="당일매매일지",
    )


class DomesticAccountDepositBalanceDetailsItem(BaseModel):
    crnc_cd: str = Field(default="", description="통화코드", max_length=3)
    fx_entr: str = Field(default="", description="외화예수금", max_length=15)
    fc_krw_repl_evlta: str = Field(default="", description="원화대용평가금", max_length=15)
    fc_trst_profa: str = Field(default="", description="해외주식증거금", max_length=15)
    pymn_alow_amt: str = Field(default="", description="출금가능금액", max_length=15)
    pymn_alow_amt_entr: str = Field(default="", description="출금가능금액(예수금)", max_length=15)
    ord_alow_amt_entr: str = Field(default="", description="주문가능금액(예수금)", max_length=15)
    fc_uncla: str = Field(default="", description="외화미수(합계)", max_length=15)
    fc_ch_uncla: str = Field(default="", description="외화현금미수금", max_length=15)
    dly_amt: str = Field(default="", description="연체료", max_length=15)
    d1_fx_entr: str = Field(default="", description="d+1외화예수금", max_length=15)
    d2_fx_entr: str = Field(default="", description="d+2외화예수금", max_length=15)
    d3_fx_entr: str = Field(default="", description="d+3외화예수금", max_length=15)
    d4_fx_entr: str = Field(default="", description="d+4외화예수금", max_length=15)


class DomesticAccountDepositBalanceDetails(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="예수금상세현황요청 응답")

    entr: str = Field(default="", description="예수금", max_length=15)
    profa_ch: str = Field(default="", description="주식증거금현금", max_length=15)
    bncr_profa_ch: str = Field(default="", description="수익증권증거금현금", max_length=15)
    nxdy_bncr_sell_exct: str = Field(default="", description="익일수익증권매도정산대금", max_length=15)
    fc_stk_krw_repl_set_amt: str = Field(default="", description="해외주식원화대용설정금", max_length=15)
    crd_grnta_ch: str = Field(default="", description="신용보증금현금", max_length=15)
    crd_grnt_ch: str = Field(default="", description="신용담보금현금", max_length=15)
    add_grnt_ch: str = Field(default="", description="추가담보금현금", max_length=15)
    etc_profa: str = Field(default="", description="기타증거금", max_length=15)
    uncl_stk_amt: str = Field(default="", description="미수확보금", max_length=15)
    shrts_prica: str = Field(default="", description="공매도대금", max_length=15)
    crd_set_grnta: str = Field(default="", description="신용설정평가금", max_length=15)
    chck_ina_amt: str = Field(default="", description="수표입금액", max_length=15)
    etc_chck_ina_amt: str = Field(default="", description="기타수표입금액", max_length=15)
    crd_grnt_ruse: str = Field(default="", description="신용담보재사용", max_length=15)
    knx_asset_evltv: str = Field(default="", description="코넥스기본예탁금", max_length=15)
    elwdpst_evlta: str = Field(default="", description="ELW예탁평가금", max_length=15)
    crd_ls_rght_frcs_amt: str = Field(default="", description="신용대주권리예정금액", max_length=15)
    lvlh_join_amt: str = Field(default="", description="생계형가입금액", max_length=15)
    lvlh_trns_alowa: str = Field(default="", description="생계형입금가능금액", max_length=15)
    repl_amt: str = Field(default="", description="대용금평가금(합계)", max_length=15)
    remn_repl_evlta: str = Field(default="", description="잔고대용평가금액", max_length=15)
    trst_remn_repl_evlta: str = Field(default="", description="위탁대용잔고평가금액", max_length=15)
    bncr_remn_repl_evlta: str = Field(default="", description="수익증권대용평가금액", max_length=15)
    profa_repl: str = Field(default="", description="위탁증거금대용", max_length=15)
    crd_grnta_repl: str = Field(default="", description="신용보증금대용", max_length=15)
    crd_grnt_repl: str = Field(default="", description="신용담보금대용", max_length=15)
    add_grnt_repl: str = Field(default="", description="추가담보금대용", max_length=15)
    rght_repl_amt: str = Field(default="", description="권리대용금", max_length=15)
    pymn_alow_amt: str = Field(default="", description="출금가능금액", max_length=15)
    wrap_pymn_alow_amt: str = Field(default="", description="랩출금가능금액", max_length=15)
    ord_alow_amt: str = Field(default="", description="주문가능금액", max_length=15)
    bncr_buy_alowa: str = Field(default="", description="수익증권매수가능금액", max_length=15)
    stk_ord_alow_amt_20: str = Field(
        default="", description="20%종목주문가능금액", max_length=15, alias="20stk_ord_alow_amt"
    )
    stk_ord_alow_amt_30: str = Field(
        default="", description="30%종목주문가능금액", max_length=15, alias="30stk_ord_alow_amt"
    )
    stk_ord_alow_amt_40: str = Field(
        default="", description="40%종목주문가능금액", max_length=15, alias="40stk_ord_alow_amt"
    )
    stk_ord_alow_amt_100: str = Field(
        default="", description="100%종목주문가능금액", max_length=15, alias="100stk_ord_alow_amt"
    )
    ch_uncla: str = Field(default="", description="현금미수금", max_length=15)
    ch_uncla_dlfe: str = Field(default="", description="현금미수연체료", max_length=15)
    ch_uncla_tot: str = Field(default="", description="현금미수금합계", max_length=15)
    crd_int_npay: str = Field(default="", description="신용이자미납", max_length=15)
    int_npay_amt_dlfe: str = Field(default="", description="신용이자미납연체료", max_length=15)
    int_npay_amt_tot: str = Field(default="", description="신용이자미납합계", max_length=15)
    etc_loana: str = Field(default="", description="기타대여금", max_length=15)
    etc_loana_dlfe: str = Field(default="", description="기타대여금연체료", max_length=15)
    etc_loan_tot: str = Field(default="", description="기타대여금합계", max_length=15)
    nrpy_loan: str = Field(default="", description="미상환융자금", max_length=15)
    loan_sum: str = Field(default="", description="융자금합계", max_length=15)
    ls_sum: str = Field(default="", description="대주금합계", max_length=15)
    crd_grnt_ch: str = Field(default="", description="신용담보비율", max_length=15, alias="crd_grnt_rt")
    mdstrm_usfe: str = Field(default="", description="중도이용료", max_length=15)
    min_ord_alow_yn: str = Field(default="", description="최소주문가능금액", max_length=15)
    loan_remn_evlt_amt: str = Field(default="", description="대출총평가금액", max_length=15)
    dpst_grntl_remn: str = Field(default="", description="예탁담보대출잔고", max_length=15)
    sell_grntl_remn: str = Field(default="", description="매도담보대출잔고", max_length=15)
    d1_entra: str = Field(default="", description="d+1추정예수금", max_length=15)
    d1_slby_exct_amt: str = Field(default="", description="d+1매도매수정산금", max_length=15)
    d1_buy_exct_amt: str = Field(default="", description="d+1매수정산금", max_length=15)
    d1_out_rep_mor: str = Field(default="", description="d+1미수변제소요금", max_length=15)
    d1_sel_exct_amt: str = Field(default="", description="d+1매도정산금", max_length=15)
    d1_pymn_alow_amt: str = Field(default="", description="d+1출금가능금액", max_length=15)
    stk_ord_allow_amt_50: str = Field(
        default="", description="50%종목주문가능금액", max_length=15, alias="50stk_ord_alow_amt"
    )
    stk_ord_allow_amt_60: str = Field(
        default="", description="60%종목주문가능금액", max_length=15, alias="60stk_ord_alow_amt"
    )
    stk_entr_prst: list[DomesticAccountDepositBalanceDetailsItem] = Field(
        default_factory=list,
        description="종목별예수금",
    )


class DomesticAccountDailyEstimatedDepositAssetBalanceItem(BaseModel):
    dt: str = Field(default="", description="일자", max_length=8)
    entr: str = Field(default="", description="예수금", max_length=12)
    grnt_use_amt: str = Field(default="", description="담보대출금", max_length=12)
    crd_loan: str = Field(default="", description="신용융자금", max_length=12)
    ls_grnt: str = Field(default="", description="대주담보금", max_length=12)
    repl_amt: str = Field(default="", description="대용금", max_length=12)
    prsm_dpst_aset_amt: str = Field(default="", description="추정예탁자산", max_length=12)
    prsm_dpst_aset_amt_bncr_skip: str = Field(default="", description="추정예탁자산수익증권제외", max_length=12)


class DomesticAccountDailyEstimatedDepositAssetBalance(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="일별추정예탁자산현황요청 응답")

    daly_prsm_dpst_aset_amt_prst: list[DomesticAccountDailyEstimatedDepositAssetBalanceItem] = Field(
        default_factory=list,
        description="일별추정예탁자산현황",
    )


class DomesticAccountEstimatedAssetBalance(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="추정자산조회요청 응답")

    prsm_dpst_aset_amt: str = Field(default="", description="추정예탁자산", max_length=12)


class DomesticAccountEvaluationStatusItem(BaseModel):
    stk_cd: str = Field(default="", description="종목코드", max_length=12)
    stk_nm: str = Field(default="", description="종목명", max_length=40)
    rmnd_qty: str = Field(default="", description="보유수량", max_length=12)
    avg_prc: str = Field(default="", description="평균단가", max_length=12)
    cur_prc: str = Field(default="", description="현재가", max_length=12)
    evlt_amt: str = Field(default="", description="평가금액", max_length=12)
    pl_amt: str = Field(default="", description="손익금액", max_length=12)
    pl_rt: str = Field(default="", description="손익율", max_length=12)
    loan_dt: str = Field(default="", description="대출일", max_length=10)
    pur_amt: str = Field(default="", description="매입금액", max_length=12)
    setl_remn: str = Field(default="", description="결제잔고", max_length=12)
    pred_buyq: str = Field(default="", description="전일매수수량", max_length=12)
    pred_sellq: str = Field(default="", description="전일매도수량", max_length=12)
    tdy_buyq: str = Field(default="", description="금일매수수량", max_length=12)
    tdy_sellq: str = Field(default="", description="금일매도수량", max_length=12)


class DomesticAccountEvaluationStatus(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="계좌평가현황요청 응답")

    acnt_nm: str = Field(default="", description="계좌명", max_length=30)
    brch_nm: str = Field(default="", description="지점명", max_length=30)
    entr: str = Field(default="", description="예수금", max_length=12)
    d2_entra: str = Field(default="", description="D+2추정예수금", max_length=12)
    tot_est_amt: str = Field(default="", description="유가잔고평가액", max_length=12)
    aset_evlt_amt: str = Field(default="", description="예탁자산평가액", max_length=12)
    tot_pur_amt: str = Field(default="", description="총매입금액", max_length=12)
    prsm_dpst_aset_amt: str = Field(default="", description="추정예탁자산", max_length=12)
    tot_grnt_sella: str = Field(default="", description="매도담보대출금", max_length=12)
    tdy_lspft_amt: str = Field(default="", description="당일투자원금", max_length=12)
    invt_bsamt: str = Field(default="", description="당월투자원금", max_length=12)
    lspft_amt: str = Field(default="", description="누적투자원금", max_length=12)
    tdy_lspft: str = Field(default="", description="당일투자손익", max_length=12)
    lspft2: str = Field(default="", description="당월투자손익", max_length=12)
    lspft: str = Field(default="", description="누적투자손익", max_length=12)
    tdy_lspft_rt: str = Field(default="", description="당일손익율", max_length=12)
    lspft_ratio: str = Field(default="", description="당월손익율", max_length=12)
    lspft_rt: str = Field(default="", description="누적손익율", max_length=12)
    stk_acnt_evlt_prst: list[DomesticAccountEvaluationStatusItem] = Field(
        default_factory=list,
        description="종목별계좌평가현황",
    )


class DomesticAccountExecutionBalanceItem(BaseModel):
    crd_tp: str = Field(default="", description="신용구분", max_length=2)
    loan_dt: str = Field(default="", description="대출일", max_length=8)
    expr_dt: str = Field(default="", description="만기일", max_length=8)
    stk_cd: str = Field(default="", description="종목번호", max_length=12)
    stk_nm: str = Field(default="", description="종목명", max_length=40)
    setl_remn: str = Field(default="", description="결제잔고", max_length=12)
    cur_qty: str = Field(default="", description="현재잔고", max_length=12)
    cur_prc: str = Field(default="", description="현재가", max_length=12)
    buy_uv: str = Field(default="", description="매입단가", max_length=12)
    pur_amt: str = Field(default="", description="매입금액", max_length=12)
    evlt_amt: str = Field(default="", description="평가금액", max_length=12)
    evltv_prft: str = Field(default="", description="평가손익", max_length=12)
    pl_rt: str = Field(default="", description="손익률", max_length=12)


class DomesticAccountExecutionBalance(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="체결잔고요청 응답")

    entr: str = Field(default="", description="예수금", max_length=12)
    entr_d1: str = Field(default="", description="예수금 D+1", max_length=12)
    entr_d2: str = Field(default="", description="예수금 D+2", max_length=12)
    pymn_alow_amt: str = Field(default="", description="출금가능금액", max_length=12)
    uncl_stk_amt: str = Field(default="", description="미수확보금", max_length=12)
    repl_amt: str = Field(default="", description="대용금", max_length=12)
    rght_repl_amt: str = Field(default="", description="권리대용금", max_length=12)
    ord_alowa: str = Field(default="", description="주문가능현금", max_length=12)
    ch_uncla: str = Field(default="", description="현금미수금", max_length=12)
    crd_int_npay_gold: str = Field(default="", description="신용이자미납금", max_length=12)
    etc_loana: str = Field(default="", description="기타대여금", max_length=12)
    nrpy_loan: str = Field(default="", description="미상환융자금", max_length=12)
    profa_ch: str = Field(default="", description="증거금현금", max_length=12)
    repl_profa: str = Field(default="", description="증거금대용", max_length=12)
    stk_buy_tot_amt: str = Field(default="", description="주식매수총액", max_length=12)
    evlt_amt_tot: str = Field(default="", description="평가금액합계", max_length=12)
    tot_pl_tot: str = Field(default="", description="총손익합계", max_length=12)
    tot_pl_rt: str = Field(default="", description="총손익률", max_length=12)
    tot_re_buy_alowa: str = Field(default="", description="총재매수가능금액", max_length=12)
    ord_alow_amt_20: str = Field(default="", description="20%주문가능금액", max_length=12, alias="20ord_alow_amt")
    ord_alow_amt_30: str = Field(default="", description="30%주문가능금액", max_length=12, alias="30ord_alow_amt")
    ord_alow_amt_40: str = Field(default="", description="40%주문가능금액", max_length=12, alias="40ord_alow_amt")
    ord_alow_amt_50: str = Field(default="", description="50%주문가능금액", max_length=12, alias="50ord_alow_amt")
    ord_alow_amt_60: str = Field(default="", description="60%주문가능금액", max_length=12, alias="60ord_alow_amt")
    ord_alow_amt_100: str = Field(default="", description="100%주문가능금액", max_length=12, alias="100ord_alow_amt")
    crd_loan_tot: str = Field(default="", description="신용융자합계", max_length=12)
    crd_loan_ls_tot: str = Field(default="", description="신용융자대주합계", max_length=12)
    crd_grnt_rt: str = Field(default="", description="신용담보비율", max_length=12, alias="crd_grnt_ch")
    dpst_grnt_use_amt_amt: str = Field(default="", description="예탁담보대출금액", max_length=12)
    grnt_loan_amt: str = Field(default="", description="매도담보대출금액", max_length=12)
    stk_cntr_remn: list[DomesticAccountExecutionBalanceItem] = Field(
        default_factory=list,
        description="종목별체결잔고",
    )


class DomesticAccountOrderExecutionDetailsItem(BaseModel):
    ord_no: str = Field(default="", description="주문번호", max_length=7)
    stk_cd: str = Field(default="", description="종목번호", max_length=12)
    trde_tp: str = Field(default="", description="매매구분", max_length=20)
    crd_tp: str = Field(default="", description="신용구분", max_length=20)
    ord_qty: str = Field(default="", description="주문수량", max_length=10)
    ord_uv: str = Field(default="", description="주문단가", max_length=10)
    cnfm_qty: str = Field(default="", description="확인수량", max_length=10)
    acpt_tp: str = Field(default="", description="접수구분", max_length=20)
    rsrv_tp: str = Field(default="", description="반대여부", max_length=20)
    ord_tm: str = Field(default="", description="주문시간", max_length=8)
    ori_ord: str = Field(default="", description="원주문", max_length=7)
    stk_nm: str = Field(default="", description="종목명", max_length=40)
    io_tp_nm: str = Field(default="", description="주문구분", max_length=20)
    loan_dt: str = Field(default="", description="대출일", max_length=8)
    cntr_qty: str = Field(default="", description="체결수량", max_length=10)
    cntr_uv: str = Field(default="", description="체결단가", max_length=10)
    ord_remnq: str = Field(default="", description="주문잔량", max_length=10)
    comm_ord_tp: str = Field(default="", description="통신구분", max_length=20)
    mdfy_cncl: str = Field(default="", description="정정취소", max_length=20)
    cnfm_tm: str = Field(default="", description="확인시간", max_length=8)
    dmst_stex_tp: str = Field(default="", description="국내거래소구분", max_length=8)
    cond_uv: str = Field(default="", description="스톱가", max_length=10)


class DomesticAccountOrderExecutionDetails(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="계좌별주문체결내역상세요청 응답")

    acnt_ord_cntr_prps_dtl: list[DomesticAccountOrderExecutionDetailsItem] = Field(
        default_factory=list,
        description="계좌별주문체결내역상세",
    )


class DomesticAccountNextDaySettlementDetailsItem(BaseModel):
    ord_no: str = Field(default="", description="주문번호", max_length=7)
    stk_cd: str = Field(default="", description="종목번호", max_length=12)
    trde_tp: str = Field(default="", description="매매구분", max_length=20)
    crd_tp: str = Field(default="", description="신용구분", max_length=20)
    ord_qty: str = Field(default="", description="주문수량", max_length=10)
    ord_uv: str = Field(default="", description="주문단가", max_length=10)
    cnfm_qty: str = Field(default="", description="확인수량", max_length=10)
    acpt_tp: str = Field(default="", description="접수구분", max_length=20)
    rsrv_tp: str = Field(default="", description="반대여부", max_length=20)
    ord_tm: str = Field(default="", description="주문시간", max_length=8)
    ori_ord: str = Field(default="", description="원주문", max_length=7)
    stk_nm: str = Field(default="", description="종목명", max_length=40)
    io_tp_nm: str = Field(default="", description="주문구분", max_length=20)
    loan_dt: str = Field(default="", description="대출일", max_length=8)
    cntr_qty: str = Field(default="", description="체결수량", max_length=10)
    cntr_uv: str = Field(default="", description="체결단가", max_length=10)
    ord_remnq: str = Field(default="", description="주문잔량", max_length=10)
    comm_ord_tp: str = Field(default="", description="통신구분", max_length=20)
    mdfy_cncl: str = Field(default="", description="정정취소", max_length=20)
    cnfm_tm: str = Field(default="", description="확인시간", max_length=8)
    dmst_stex_tp: str = Field(default="", description="국내거래소구분", max_length=8)
    cond_uv: str = Field(default="", description="스톱가", max_length=10)


class DomesticAccountNextDaySettlementDetails(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="계좌별익일결제예정내역요청 응답")

    acnt_ord_cntr_prps_dtl: list[DomesticAccountOrderExecutionDetailsItem] = Field(
        default_factory=list,
        description="계좌별주문체결내역상세",
    )


class DomesticAccountOrderExecutionStatusItem(BaseModel):
    stk_bond_tp: str = Field(default="", description="주식채권구분", max_length=1)
    ord_no: str = Field(default="", description="주문번호", max_length=7)
    stk_cd: str = Field(default="", description="종목번호", max_length=12)
    trde_tp: str = Field(default="", description="매매구분", max_length=15)
    io_tp_nm: str = Field(default="", description="주문유형구분", max_length=20)
    ord_qty: str = Field(default="", description="주문수량", max_length=10)
    ord_uv: str = Field(default="", description="주문단가", max_length=10)
    cnfm_qty: str = Field(default="", description="확인수량", max_length=10)
    rsrv_oppo: str = Field(default="", description="예약/반대", max_length=4)
    cntr_no: str = Field(default="", description="체결번호", max_length=7)
    acpt_tp: str = Field(default="", description="접수구분", max_length=8)
    orig_ord_no: str = Field(default="", description="원주문번호", max_length=7)
    stk_nm: str = Field(default="", description="종목명", max_length=40)
    setl_tp: str = Field(default="", description="결제구분", max_length=8)
    crd_deal_tp: str = Field(default="", description="신용거래구분", max_length=20)
    cntr_qty: str = Field(default="", description="체결수량", max_length=10)
    cntr_uv: str = Field(default="", description="체결단가", max_length=10)
    comm_ord_tp: str = Field(default="", description="통신구분", max_length=8)
    mdfy_cncl_tp: str = Field(default="", description="정정/취소구분", max_length=12)
    cntr_tm: str = Field(default="", description="체결시간", max_length=8)
    dmst_stex_tp: str = Field(default="", description="국내거래소구분", max_length=6)
    cond_uv: str = Field(default="", description="스톱가", max_length=10)


class DomesticAccountOrderExecutionStatus(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="계좌별주문체결현황요청 응답")

    sell_grntl_engg_amt: str = Field(default="", description="매도약정금액", max_length=12)
    buy_engg_amt: str = Field(default="", description="매수약정금액", max_length=12)
    engg_amt: str = Field(default="", description="약정금액", max_length=12)
    acnt_ord_cntr_prst: list[DomesticAccountOrderExecutionStatusItem] = Field(
        default_factory=list,
        description="계좌별주문체결현황",
    )


class DomesticAccountAvailableWithdrawalAmount(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="주문인출가능금액요청 응답")

    profa_20ord_alow_amt: str = Field(default="", description="증거금20%주문가능금액", max_length=12)
    profa_20ord_alowq: str = Field(default="", description="증거금20%주문가능수량", max_length=10)
    profa_30ord_alow_amt: str = Field(default="", description="증거금30%주문가능금액", max_length=12)
    profa_30ord_alowq: str = Field(default="", description="증거금30%주문가능수량", max_length=10)
    profa_40ord_alow_amt: str = Field(default="", description="증거금40%주문가능금액", max_length=12)
    profa_40ord_alowq: str = Field(default="", description="증거금40%주문가능수량", max_length=10)
    profa_50ord_alow_amt: str = Field(default="", description="증거금50%주문가능금액", max_length=12)
    profa_50ord_alowq: str = Field(default="", description="증거금50%주문가능수량", max_length=10)
    profa_60ord_alow_amt: str = Field(default="", description="증거금60%주문가능금액", max_length=12)
    profa_60ord_alowq: str = Field(default="", description="증거금60%주문가능수량", max_length=10)
    profa_rdex_60ord_alow_amt: str = Field(default="", description="증거금감면60%주문가능금액", max_length=12)
    profa_rdex_60ord_alowq: str = Field(default="", description="증거금감면60%주문가능수량", max_length=10)
    prfa_100ord_allow_amt: str = Field(default="", description="증거금100%주문가능금액", max_length=12)
    profa_100ord_alowq: str = Field(default="", description="증거금100%주문가능수량", max_length=10)
    pred_reu_allowa: str = Field(default="", description="전일재사용가능금액", max_length=12)
    tdy_reu_alowa: str = Field(default="", description="금일재사용가능금액", max_length=12)
    entr: str = Field(default="", description="예수금", max_length=12)
    repl_amt: str = Field(default="", description="대용금", max_length=12)
    uncla: str = Field(default="", description="미수금", max_length=12)
    ord_pos_repl: str = Field(default="", description="주문가능대용", max_length=12)
    ord_alowa: str = Field(default="", description="주문가능현금", max_length=12)
    wthd_alowa: str = Field(default="", description="인출가능금액", max_length=12)
    nxdy_wthd_alowa: str = Field(default="", description="익일인출가능금액", max_length=12)
    pur_amt: str = Field(default="", description="매입금액", max_length=12)
    cmsn: str = Field(default="", description="수수료", max_length=12)
    pur_exct_amt: str = Field(default="", description="매입정산금", max_length=12)
    d2entra: str = Field(default="", description="D+2추정예수금", max_length=12)
    profa_rdex_aplc_tp: str = Field(default="", description="증거금감면적용구분. 0:일반,1:60%감면", max_length=1)


class DomesticAccountAvailableOrderQuantityByMarginRate(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="증거금율별주문가능수량조회요청 응답")

    stk_profa_rt: str = Field(default="", description="종목증거금율", max_length=15)
    profa_rt: str = Field(default="", description="계좌증거금율", max_length=15)
    aplc_rt: str = Field(default="", description="적용증거금율", max_length=15)
    profa_20ord_alow_amt: str = Field(default="", description="증거금20%주문가능금액", max_length=12)
    profa_20ord_alowq: str = Field(default="", description="증거금20%주문가능수량", max_length=12)
    profa_20pred_reu_amt: str = Field(default="", description="증거금20%전일재사용금액", max_length=12)
    profa_20tdy_reu_amt: str = Field(default="", description="증거금20%금일재사용금액", max_length=12)
    profa_30ord_alow_amt: str = Field(default="", description="증거금30%주문가능금액", max_length=12)
    profa_30ord_alowq: str = Field(default="", description="증거금30%주문가능수량", max_length=12)
    profa_30pred_reu_amt: str = Field(default="", description="증거금30%전일재사용금액", max_length=12)
    profa_30tdy_reu_amt: str = Field(default="", description="증거금30%금일재사용금액", max_length=12)
    profa_40ord_alow_amt: str = Field(default="", description="증거금40%주문가능금액", max_length=12)
    profa_40ord_alowq: str = Field(default="", description="증거금40%주문가능수량", max_length=12)
    profa_40pred_reu_amt: str = Field(default="", description="증거금40%전일재사용금액", max_length=12)
    profa_40tdy_reu_amt: str = Field(default="", description="증거금40%금일재사용금액", max_length=12)
    profa_50ord_alow_amt: str = Field(default="", description="증거금50%주문가능금액", max_length=12)
    profa_50ord_alowq: str = Field(default="", description="증거금50%주문가능수량", max_length=12)
    profa_50pred_reu_amt: str = Field(default="", description="증거금50%전일재사용금액", max_length=12)
    profa_50tdy_reu_amt: str = Field(default="", description="증거금50%금일재사용금액", max_length=12)
    profa_60ord_alow_amt: str = Field(default="", description="증거금60%주문가능금액", max_length=12)
    profa_60ord_alowq: str = Field(default="", description="증거금60%주문가능수량", max_length=12)
    profa_60pred_reu_amt: str = Field(default="", description="증거금60%전일재사용금액", max_length=12)
    profa_60tdy_reu_amt: str = Field(default="", description="증거금60%금일재사용금액", max_length=12)
    profa_100ord_alow_amt: str = Field(default="", description="증거금100%주문가능금액", max_length=12)
    profa_100ord_alowq: str = Field(default="", description="증거금100%주문가능수량", max_length=12)
    profa_100pred_reu_amt: str = Field(default="", description="증거금100%전일재사용금액", max_length=12)
    profa_100tdy_reu_amt: str = Field(default="", description="증거금100%금일재사용금액", max_length=12)
    min_ord_allow_amt: str = Field(default="", description="미수불가주문가능금액", max_length=12)
    min_ord_allowq: str = Field(default="", description="미수불가주문가능수량", max_length=12)
    min_pred_reu_amt: str = Field(default="", description="미수불가전일재사용금액", max_length=12)
    min_tdy_reu_amt: str = Field(default="", description="미수불가금일재사용금액", max_length=12)
    entr: str = Field(default="", description="예수금", max_length=12)
    repl_amt: str = Field(default="", description="대용금", max_length=12)
    uncla: str = Field(default="", description="미수금", max_length=12)
    ord_pos_repl: str = Field(default="", description="주문가능대용", max_length=12)
    ord_alowa: str = Field(default="", description="주문가능현금", max_length=12)


class DomesticAccountAvailableOrderQuantityByMarginLoanStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="신용융자증권별주문가능수량요청 응답")

    stk_assr_rt: str = Field(default="", description="종목보증금율", max_length=1)
    stk_assr_rt_nm: str = Field(default="", description="종목보증금율명", max_length=4)
    assr_30ord_alow_amt: str = Field(default="", description="보증금30%주문가능금액", max_length=12)
    assr_30ord_alowq: str = Field(default="", description="보증금30%주문가능수량", max_length=12)
    assr_30pred_reu_amt: str = Field(default="", description="보증금30%전일재사용금액", max_length=12)
    assr_30tdy_reu_amt: str = Field(default="", description="보증금30%금일재사용금액", max_length=12)
    assr_40ord_alow_amt: str = Field(default="", description="보증금40%주문가능금액", max_length=12)
    assr_40ord_alowq: str = Field(default="", description="보증금40%주문가능수량", max_length=12)
    assr_40pred_reu_amt: str = Field(default="", description="보증금40%전일재사용금액", max_length=12)
    assr_40tdy_reu_amt: str = Field(default="", description="보증금40%금일재사용금액", max_length=12)
    assr_50ord_alow_amt: str = Field(default="", description="보증금50%주문가능금액", max_length=12)
    assr_50ord_alowq: str = Field(default="", description="보증금50%주문가능수량", max_length=12)
    assr_50pred_reu_amt: str = Field(default="", description="보증금50%전일재사용금액", max_length=12)
    assr_50tdy_reu_amt: str = Field(default="", description="보증금50%금일재사용금액", max_length=12)
    assr_60ord_alow_amt: str = Field(default="", description="보증금60%주문가능금액", max_length=12)
    assr_60ord_alowq: str = Field(default="", description="보증금60%주문가능수량", max_length=12)
    assr_60pred_reu_amt: str = Field(default="", description="보증금60%전일재사용금액", max_length=12)
    assr_60tdy_reu_amt: str = Field(default="", description="보증금60%금일재사용금액", max_length=12)
    entr: str = Field(default="", description="예수금", max_length=12)
    repl_amt: str = Field(default="", description="대용금", max_length=12)
    uncla: str = Field(default="", description="미수금", max_length=12)
    ord_pos_repl: str = Field(default="", description="주문가능대용", max_length=12)
    ord_alowa: str = Field(default="", description="주문가능현금", max_length=12)
    out_alowa: str = Field(default="", description="미수가능금액", max_length=12)
    out_pos_qty: str = Field(default="", description="미수가능수량", max_length=12)
    min_amt: str = Field(default="", description="미수불가금액", max_length=12)
    min_qty: str = Field(default="", description="미수불가수량", max_length=12)


class DomesticAccountMarginDetails(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="증거금세부내역조회요청 응답")

    tdy_reu_objt_amt: str = Field(default="", description="금일재사용대상금액", max_length=15)
    tdy_reu_use_amt: str = Field(default="", description="금일재사용사용금액", max_length=15)
    tdy_reu_alowa: str = Field(default="", description="금일재사용가능금액", max_length=15)
    tdy_reu_lmtt_amt: str = Field(default="", description="금일재사용제한금액", max_length=15)
    tdy_reu_alowa_fin: str = Field(default="", description="금일재사용가능금액최종", max_length=15)
    pred_reu_objt_amt: str = Field(default="", description="전일재사용대상금액", max_length=15)
    pred_reu_use_amt: str = Field(default="", description="전일재사용사용금액", max_length=15)
    pred_reu_alowa: str = Field(default="", description="전일재사용가능금액", max_length=15)
    pred_reu_lmtt_amt: str = Field(default="", description="전일재사용제한금액", max_length=15)
    pred_reu_alowa_fin: str = Field(default="", description="전일재사용가능금액최종", max_length=15)
    ch_amt: str = Field(default="", description="현금금액", max_length=15)
    ch_profa: str = Field(default="", description="현금증거금", max_length=15)
    use_pos_ch: str = Field(default="", description="사용가능현금", max_length=15)
    ch_use_lmtt_amt: str = Field(default="", description="현금사용제한금액", max_length=15)
    use_pos_ch_fin: str = Field(default="", description="사용가능현금최종", max_length=15)
    repl_amt_amt: str = Field(default="", description="대용금액", max_length=15)
    repl_profa: str = Field(default="", description="대용증거금", max_length=15)
    use_pos_repl: str = Field(default="", description="사용가능대용", max_length=15)
    repl_use_lmtt_amt: str = Field(default="", description="대용사용제한금액", max_length=15)
    use_pos_repl_fin: str = Field(default="", description="사용가능대용최종", max_length=15)
    crd_grnta_ch: str = Field(default="", description="신용보증금현금", max_length=15)
    crd_grnta_repl: str = Field(default="", description="신용보증금대용", max_length=15)
    crd_grnt_ch: str = Field(default="", description="신용담보금현금", max_length=15)
    crd_grnt_repl: str = Field(default="", description="신용담보금대용", max_length=15)
    uncla: str = Field(default="", description="미수금", max_length=12)
    ls_grnt_reu_gold: str = Field(default="", description="대주담보금재사용금", max_length=15)
    ord_alow_amt_20: str = Field(default="", description="20%주문가능금액", max_length=15, alias="20ord_alow_amt")
    ord_alow_amt_30: str = Field(default="", description="30%주문가능금액", max_length=15, alias="30ord_alow_amt")
    ord_alow_amt_40: str = Field(default="", description="40%주문가능금액", max_length=15, alias="40ord_alow_amt")
    ord_alow_amt_50: str = Field(default="", description="50%주문가능금액", max_length=15, alias="50ord_alow_amt")
    ord_alow_amt_60: str = Field(default="", description="60%주문가능금액", max_length=15, alias="60ord_alow_amt")
    ord_alow_amt_100: str = Field(default="", description="100%주문가능금액", max_length=15, alias="100ord_alow_amt")
    tdy_crd_rpya_loss_amt: str = Field(default="", description="금일신용상환손실금액", max_length=15)
    pred_crd_rpya_loss_amt: str = Field(default="", description="전일신용상환손실금액", max_length=15)
    tdy_ls_rpya_loss_repl_profa: str = Field(default="", description="금일대주상환손실대용증거금", max_length=15)
    pred_ls_rpya_loss_repl_profa: str = Field(default="", description="전일대주상환손실대용증거금", max_length=15)
    evlt_repl_amt_spg_use_skip: str = Field(default="", description="평가대용금(현물사용제외)", max_length=15)
    evlt_repl_rt: str = Field(default="", description="평가대용비율", max_length=15)
    crd_repl_profa: str = Field(default="", description="신용대용증거금", max_length=15)
    ch_ord_repl_profa: str = Field(default="", description="현금주문대용증거금", max_length=15)
    crd_ord_repl_profa: str = Field(default="", description="신용주문대용증거금", max_length=15)
    crd_repl_conv_gold: str = Field(default="", description="신용대용환산금", max_length=15)
    repl_alowa: str = Field(default="", description="대용가능금액(현금제한)", max_length=15)
    repl_alowa_2: str = Field(default="", description="대용가능금액2(신용제한)", max_length=15)
    ch_repl_lck_gold: str = Field(default="", description="현금대용부족금", max_length=15)
    crd_repl_lck_gold: str = Field(default="", description="신용대용부족금", max_length=15)
    ch_ord_alow_repla: str = Field(default="", description="현금주문가능대용금", max_length=15)
    crd_ord_alow_repla: str = Field(default="", description="신용주문가능대용금", max_length=15)
    d2vexct_entr: str = Field(default="", description="D2가정산예수금", max_length=15)
    d2ch_ord_alow_amt: str = Field(default="", description="D2현금주문가능금액", max_length=15)


class DomesticAccountConsignmentComprehensiveTransactionHistoryItem(BaseModel):
    trde_dt: str = Field(default="", description="거래일자", max_length=8)
    trde_no: str = Field(default="", description="거래번호", max_length=9)
    rmrk_nm: str = Field(default="", description="적요명", max_length=60)
    crd_deal_tp_nm: str = Field(default="", description="신용거래구분명", max_length=20)
    exct_amt: str = Field(default="", description="정산금액", max_length=15)
    loan_amt_rpya: str = Field(default="", description="대출금상환", max_length=15)
    fc_trde_amt: str = Field(default="", description="거래금액(외)", max_length=15)
    fc_exct_amt: str = Field(default="", description="정산금액(외)", max_length=15)
    entra_remn: str = Field(default="", description="예수금잔고", max_length=15)
    crnc_cd: str = Field(default="", description="통화코드", max_length=3)
    trde_ocr_tp: str = Field(
        default="",
        description="거래종류구분. 1:입출금, 2:펀드, 3:ELS, 4:채권, 5:해외채권, 6:외화RP, 7:외화발행어음",
        max_length=2,
    )
    trde_kind_nm: str = Field(default="", description="거래종류명", max_length=20)
    stk_nm: str = Field(default="", description="종목명", max_length=40)
    trde_amt: str = Field(default="", description="거래금액", max_length=15)
    trde_agri_tax: str = Field(default="", description="거래및농특세", max_length=15)
    rpy_diffa: str = Field(default="", description="상환차금", max_length=15)
    fc_trde_tax: str = Field(default="", description="거래세(외)", max_length=15)
    dly_sum: str = Field(default="", description="연체합", max_length=15)
    fc_entra: str = Field(default="", description="외화예수금잔고", max_length=15)
    mdia_tp_nm: str = Field(default="", description="매체구분명", max_length=20)
    io_tp: str = Field(default="", description="입출구분", max_length=1)
    io_tp_nm: str = Field(default="", description="입출구분명", max_length=10)
    orig_deal_no: str = Field(default="", description="원거래번호", max_length=9)
    stk_cd: str = Field(default="", description="종목코드", max_length=12)
    trde_qty_jwa_cnt: str = Field(default="", description="거래수량/좌수", max_length=30)
    cmsn: str = Field(default="", description="수수료", max_length=15)
    int_ls_usfe: str = Field(default="", description="이자/대주이용", max_length=15)
    fc_cmsn: str = Field(default="", description="수수료(외)", max_length=15)
    fc_dly_sum: str = Field(default="", description="연체합(외)", max_length=15)
    vlbl_nowrm: str = Field(default="", description="유가금잔", max_length=30)
    proc_tm: str = Field(default="", description="처리시간", max_length=111)
    isin_cd: str = Field(default="", description="ISIN코드", max_length=12)
    stex_cd: str = Field(default="", description="거래소코드", max_length=10)
    stex_nm: str = Field(default="", description="거래소명", max_length=20)
    trde_unit: str = Field(default="", description="거래단가/환율", max_length=20)
    incm_resi_tax: str = Field(default="", description="소득/주민세", max_length=15)
    loan_dt: str = Field(default="", description="대출일", max_length=8)
    uncl_ocr: str = Field(default="", description="미수(원/주)", max_length=30)
    rpym_sum: str = Field(default="", description="변제합", max_length=30)
    cntr_dt: str = Field(default="", description="체결일", max_length=8)
    rcpy_no: str = Field(default="", description="출납번호", max_length=20)
    prcsr: str = Field(default="", description="처리자", max_length=20)
    proc_brch: str = Field(default="", description="처리점", max_length=20)
    trde_stle: str = Field(default="", description="매매형태", max_length=40)
    txon_base_pric: str = Field(default="", description="과세기준가", max_length=15)
    tax_sum_cmsn: str = Field(default="", description="세금수수료합", max_length=15)
    frgn_pay_txam: str = Field(default="", description="외국납부세액(외)", max_length=15)
    fc_uncl_ocr: str = Field(default="", description="미수(외)", max_length=15)
    rpym_sum_fr: str = Field(default="", description="변제합(외)", max_length=30)
    rcpmnyer: str = Field(default="", description="입금자", max_length=20)
    trde_prtc_tp: str = Field(default="", description="거래내역구분", max_length=2)


class DomesticAccountConsignmentComprehensiveTransactionHistory(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="위탁종합거래내역요청 응답")

    acnt_no: str = Field(default="", description="계좌번호", max_length=40)
    trst_ovrl_trde_prps_array: list[DomesticAccountConsignmentComprehensiveTransactionHistoryItem] = Field(
        default_factory=list,
        description="위탁종합거래내역배열",
    )


class DomesticAccountDailyProfitRateDetails(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="일별계좌수익률상세현황요청 응답")

    mang_empno: str = Field(default="", description="관리사원번호", max_length=8)
    mngr_nm: str = Field(default="", description="관리자명", max_length=8)
    dept_nm: str = Field(default="", description="관리자지점", max_length=30)
    entr_fr: str = Field(default="", description="예수금_초", max_length=30)
    entr_to: str = Field(default="", description="예수금_말", max_length=12)
    scrt_evlt_amt_fr: str = Field(default="", description="유가증권평가금액_초", max_length=12)
    scrt_evlt_amt_to: str = Field(default="", description="유가증권평가금액_말", max_length=12)
    ls_grnt_fr: str = Field(default="", description="대주담보금_초", max_length=12)
    ls_grnt_to: str = Field(default="", description="대주담보금_말", max_length=12)
    crd_loan_fr: str = Field(default="", description="신용융자금_초", max_length=12)
    crd_loan_to: str = Field(default="", description="신용융자금_말", max_length=12)
    ch_uncla_fr: str = Field(default="", description="현금미수금_초", max_length=12)
    ch_uncla_to: str = Field(default="", description="현금미수금_말", max_length=12)
    krw_asgna_fr: str = Field(default="", description="원화대용금_초", max_length=12)
    krw_asgna_to: str = Field(default="", description="원화대용금_말", max_length=12)
    ls_evlta_fr: str = Field(default="", description="대주평가금_초", max_length=12)
    ls_evlta_to: str = Field(default="", description="대주평가금_말", max_length=12)
    rght_evlta_fr: str = Field(default="", description="권리평가금_초", max_length=12)
    rght_evlta_to: str = Field(default="", description="권리평가금_말", max_length=12)
    loan_amt_fr: str = Field(default="", description="대출금_초", max_length=12)
    loan_amt_to: str = Field(default="", description="대출금_말", max_length=12)
    etc_loana_fr: str = Field(default="", description="기타대여금_초", max_length=12)
    etc_loana_to: str = Field(default="", description="기타대여금_말", max_length=12)
    crd_int_npay_gold_fr: str = Field(default="", description="신용이자미납금_초", max_length=12)
    crd_int_npay_gold_to: str = Field(default="", description="신용이자미납금_말", max_length=12)
    crd_int_fr: str = Field(default="", description="신용이자_초", max_length=12)
    crd_int_to: str = Field(default="", description="신용이자_말", max_length=12)
    tot_amt_fr: str = Field(default="", description="순자산액계_초", max_length=12)
    tot_amt_to: str = Field(default="", description="순자산액계_말", max_length=12)
    invt_bsamt: str = Field(default="", description="투자원금평잔", max_length=12)
    evltv_prft: str = Field(default="", description="평가손익", max_length=12)
    prft_rt: str = Field(default="", description="수익률", max_length=12)
    tern_rt: str = Field(default="", description="회전율", max_length=12)
    termin_tot_trns: str = Field(default="", description="기간내총입금", max_length=12)
    termin_tot_pymn: str = Field(default="", description="기간내총출금", max_length=12)
    termin_tot_inq: str = Field(default="", description="기간내총입고", max_length=12)
    termin_tot_outq: str = Field(default="", description="기간내총출고", max_length=12)
    futr_repl_sella: str = Field(default="", description="선물대용매도금액", max_length=12)
    trst_repl_sella: str = Field(default="", description="위탁대용매도금액", max_length=12)


class DomesticAccountCurrentDayStatus(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="계좌별당일현황요청 응답")

    d2_entra: str = Field(default="", description="D+2추정예수금", max_length=12)
    crd_int_npay_gold: str = Field(default="", description="신용이자미납금", max_length=12)
    etc_loana: str = Field(default="", description="기타대여금", max_length=12)
    gnrl_stk_evlt_amt_d2: str = Field(default="", description="일반주식평가금액D+2", max_length=12)
    dpst_grnt_use_amt_d2: str = Field(default="", description="예탁담보대출금D+2", max_length=12)
    crd_stk_evlt_amt_d2: str = Field(default="", description="예탁담보주식평가금액D+2", max_length=12)
    crd_loan_d2: str = Field(default="", description="신용융자금D+2", max_length=12)
    crd_loan_evlta_d2: str = Field(default="", description="신용융자평가금D+2", max_length=12)
    crd_ls_grnt_d2: str = Field(default="", description="신용대주담보금D+2", max_length=12)
    crd_ls_evlta_d2: str = Field(default="", description="신용대주평가금D+2", max_length=12)
    ina_amt: str = Field(default="", description="입금금액", max_length=12)
    outa: str = Field(default="", description="출금금액", max_length=12)
    inq_amt: str = Field(default="", description="입고금액", max_length=12)
    outq_amt: str = Field(default="", description="출고금액", max_length=12)
    sell_amt: str = Field(default="", description="매도금액", max_length=12)
    buy_amt: str = Field(default="", description="매수금액", max_length=12)
    cmsn: str = Field(default="", description="수수료", max_length=12)
    tax: str = Field(default="", description="세금", max_length=12)
    stk_pur_cptal_loan_amt: str = Field(default="", description="주식매입자금대출금", max_length=12)
    rp_evlt_amt: str = Field(default="", description="RP평가금액", max_length=12)
    bd_evlt_amt: str = Field(default="", description="채권평가금액", max_length=12)
    elsevlt_amt: str = Field(default="", description="ELS평가금액", max_length=12)
    crd_int_amt: str = Field(default="", description="신용이자금액", max_length=12)
    sel_prica_grnt_loan_int_amt_amt: str = Field(default="", description="매도대금담보대출이자금액", max_length=12)
    dvida_amt: str = Field(default="", description="배당금액", max_length=12)


class DomesticAccountEvaluationBalanceDetailsItem(BaseModel):
    stk_cd: str = Field(default="", description="종목번호", max_length=12)
    stk_nm: str = Field(default="", description="종목명", max_length=40)
    evltv_prft: str = Field(default="", description="평가손익", max_length=15)
    prft_rt: str = Field(default="", description="수익률(%)", max_length=12)
    pur_pric: str = Field(default="", description="매입가", max_length=15)
    pred_close_pric: str = Field(default="", description="전일종가", max_length=12)
    rmnd_qty: str = Field(default="", description="보유수량", max_length=15)
    trde_able_qty: str = Field(default="", description="매매가능수량", max_length=15)
    cur_prc: str = Field(default="", description="현재가", max_length=12)
    pred_buyq: str = Field(default="", description="전일매수수량", max_length=15)
    pred_sellq: str = Field(default="", description="전일매도수량", max_length=15)
    tdy_buyq: str = Field(default="", description="금일매수수량", max_length=15)
    tdy_sellq: str = Field(default="", description="금일매도수량", max_length=15)
    pur_amt: str = Field(default="", description="매입금액", max_length=15)
    pur_cmsn: str = Field(default="", description="매입수수료", max_length=15)
    evlt_amt: str = Field(default="", description="평가금액", max_length=15)
    sell_cmsn: str = Field(default="", description="평가수수료", max_length=15)
    tax: str = Field(default="", description="세금", max_length=15)
    sum_cmsn: str = Field(default="", description="수수료합", max_length=15)
    poss_rt: str = Field(default="", description="보유비중(%)", max_length=12)
    crd_tp: str = Field(default="", description="신용구분", max_length=2)
    crd_tp_nm: str = Field(default="", description="신용구분명", max_length=4)
    crd_loan_dt: str = Field(default="", description="대출일", max_length=8)


class DomesticAccountEvaluationBalanceDetails(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="계좌평가잔고내역요청 응답")

    tot_pur_amt: str = Field(default="", description="총매입금액", max_length=15)
    tot_evlt_amt: str = Field(default="", description="총평가금액", max_length=15)
    tot_evlt_pl: str = Field(default="", description="총평가손익금액", max_length=15)
    tot_prft_rt: str = Field(default="", description="총수익률(%)", max_length=12)
    prsm_dpst_aset_amt: str = Field(default="", description="추정예탁자산", max_length=15)
    tot_loan_amt: str = Field(default="", description="총대출금", max_length=15)
    tot_crd_loan_amt: str = Field(default="", description="총융자금액", max_length=15)
    tot_crd_ls_amt: str = Field(default="", description="총대주금액", max_length=15)
    acnt_evlt_remn_indv_tot: list[DomesticAccountEvaluationBalanceDetailsItem] = Field(
        default_factory=list, description="계좌평가잔고개별합산"
    )
