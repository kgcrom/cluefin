from pydantic import BaseModel, ConfigDict, Field

from cluefin_openapi.kiwoom._model import (
    KiwoomHttpBody,
)


class DomesticAccountDailyStockRealizedProfitLossByDateItem(BaseModel):
    stk_nm: str = Field(default="", description="종목명")
    cntr_qty: str = Field(default="", description="체결량")
    buy_uv: str = Field(default="", description="매입단가")
    cntr_pric: str = Field(default="", description="체결가")
    tdy_sel_pl: str = Field(default="", description="당일매도손익")
    pl_rt: str = Field(default="", description="손익율")
    stk_cd: str = Field(default="", description="종목코드")
    tdy_trde_cmsn: str = Field(default="", description="당일매매수수료")
    tdy_trde_tax: str = Field(default="", description="당일매매세금")
    wthd_alowa: str = Field(default="", description="인출가능금액")
    loan_dt: str = Field(default="", description="대출일")
    crd_tp: str = Field(default="", description="신용구분")
    stk_cd_1: str = Field(default="", description="종목코드1")
    tdy_sel_pl_1: str = Field(default="", description="당일매도손익1")


class DomesticAccountDailyStockRealizedProfitLossByDate(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="일자별종목별실현속인요청 일자 응답")
    dt_stk_div_rlzt_pl: list[DomesticAccountDailyStockRealizedProfitLossByDateItem] = Field(
        default_factory=list,
        description="일자별종목별실현손익",
    )


class DomesticAccountDailyStockRealizedProfitLossByPeriodItem(BaseModel):
    dt: str = Field(default="", description="일자")
    tdy_htssel_cmsn: str = Field(default="", description="당일hts매도수수료")
    stk_nm: str = Field(default="", description="종목명")
    cntr_qty: str = Field(default="", description="체결량")
    buy_uv: str = Field(default="", description="매입단가")
    cntr_pric: str = Field(default="", description="체결가")
    tdy_sel_pl: str = Field(default="", description="당일매도손익")
    pl_rt: str = Field(default="", description="손익율")
    stk_cd: str = Field(default="", description="종목코드")
    tdy_trde_cmsn: str = Field(default="", description="당일매매수수료")
    tdy_trde_tax: str = Field(default="", description="당일매매세금")
    wthd_alowa: str = Field(default="", description="인출가능금액")
    loan_dt: str = Field(default="", description="대출일")
    crd_tp: str = Field(default="", description="신용구분")


class DomesticAccountDailyStockRealizedProfitLossByPeriod(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="일자별종목별실현손익요청 기간 응답")

    dt_stk_rlzt_pl: list[DomesticAccountDailyStockRealizedProfitLossByPeriodItem] = Field(
        default_factory=list,
        description="일자별종목별실현손익",
    )


class DomesticAccountDailyRealizedProfitLossItem(BaseModel):
    dt: str = Field(default="", description="일자")
    buy_amt: str = Field(default="", description="매수금액")
    sell_amt: str = Field(default="", description="매도금액")
    tdy_sel_pl: str = Field(default="", description="당일매도손익")
    tdy_trde_cmsn: str = Field(default="", description="당일매매수수료")
    tdy_trde_tax: str = Field(default="", description="당일매매세금")


class DomesticAccountDailyRealizedProfitLoss(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="일자별실현손익요청 응답")

    tot_buy_amt: str = Field(default="", description="총매수금액")
    tot_sell_amt: str = Field(default="", description="총매도금액")
    rlzt_pl: str = Field(default="", description="실현손익")
    trde_cmsn: str = Field(default="", description="매매수수료")
    trde_tax: str = Field(default="", description="매매세금")
    dt_rlzt_pl: list[DomesticAccountDailyRealizedProfitLossItem] = (
        Field(
            default_factory=list,
            description="일자별실현손익",
        ),
    )


class DomesticAccountUnexecutedItem(BaseModel):
    acnt_no: str = Field(default="", description="계좌번호")
    ord_no: str = Field(default="", description="주문번호")
    mang_empno: str = Field(default="", description="관리사번")
    stk_cd: str = Field(default="", description="종목코드")
    tsk_tp: str = Field(default="", description="업무구분")
    ord_stt: str = Field(default="", description="주문상태")
    stk_nm: str = Field(default="", description="종목명")
    ord_qty: str = Field(default="", description="주문수량")
    ord_pric: str = Field(default="", description="주문가격")
    oso_qty: str = Field(default="", description="미체결수량")
    cntr_tot_amt: str = Field(default="", description="체결누계금액")
    orig_ord_no: str = Field(default="", description="원주문번호")
    io_tp_nm: str = Field(default="", description="주문구분")
    trde_tp: str = Field(default="", description="매매구분")
    tm: str = Field(default="", description="시간")
    cntr_no: str = Field(default="", description="체결번호")
    cntr_pric: str = Field(default="", description="체결가")
    cntr_qty: str = Field(default="", description="체결량")
    cur_prc: str = Field(default="", description="현재가")
    sel_bid: str = Field(default="", description="매도호가")
    buy_bid: str = Field(default="", description="매수호가")
    unit_cntr_pric: str = Field(default="", description="단위체결가")
    unit_cntr_qty: str = Field(default="", description="단위체결량")
    tdy_trde_cmsn: str = Field(default="", description="당일매매수수료")
    tdy_trde_tax: str = Field(default="", description="당일매매세금")
    ind_invsr: str = Field(default="", description="개인투자자")
    stex_tp: str = Field(default="", description="거래소구분")
    stex_tp_txt: str = Field(default="", description="거래소구분텍스트")
    sor_yn: str = Field(default="", description="SOR 여부값")
    stop_pric: str = Field(default="", description="스톱가")


class DomesticAccountUnexecuted(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미체결요청 응답")

    oso: list[DomesticAccountUnexecutedItem] = Field(
        default_factory=list,
        description="미체결",
    )


class DomesticAccountExecutedItem(BaseModel):
    ord_no: str = Field(default="", description="주문번호")
    stk_nm: str = Field(default="", description="종목명")
    io_tp_nm: str = Field(default="", description="주문구분")
    ord_pric: str = Field(default="", description="주문가격")
    ord_qty: str = Field(default="", description="주문수량")
    cntr_pric: str = Field(default="", description="체결가")
    cntr_qty: str = Field(default="", description="체결량")
    oso_qty: str = Field(default="", description="미체결수량")
    tdy_trde_cmsn: str = Field(default="", description="당일매매수수료")
    tdy_trde_tax: str = Field(default="", description="당일매매세금")
    ord_stt: str = Field(default="", description="주문상태")
    trde_tp: str = Field(default="", description="매매구분")
    orig_ord_no: str = Field(default="", description="원주문번호")
    ord_tm: str = Field(default="", description="주문시간")
    stk_cd: str = Field(default="", description="종목코드")
    stex_tp: str = Field(default="", description="거래소구분")
    stex_tp_txt: str = Field(default="", description="거래소구분텍스트")
    sor_yn: str = Field(default="", description="SOR 여부값")
    stop_pric: str = Field(default="", description="스톱가")


class DomesticAccountExecuted(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="체결요청 응답")

    cntr: list[DomesticAccountExecutedItem] = Field(
        default_factory=list,
        description="체결",
    )


class DomesticAccountDailyRealizedProfitLossDetailsItem(BaseModel):
    stk_nm: str = Field(default="", description="종목명")
    cntr_qty: str = Field(default="", description="체결량")
    buy_uv: str = Field(default="", description="매입단가")
    cntr_pric: str = Field(default="", description="체결가")
    tdy_sel_pl: str = Field(default="", description="당일매도손익")
    pl_rt: str = Field(default="", description="손익율")
    tdy_trde_cmsn: str = Field(default="", description="당일매매수수료")
    tdy_trde_tax: str = Field(default="", description="당일매매세금")
    stk_cd: str = Field(default="", description="종목코드")


class DomesticAccountDailyRealizedProfitLossDetails(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="당일실현손익상세요청 응답")

    tdy_rlzt_pl: str = Field(default="", description="당일실현손익")
    tdy_rlzt_pl_dtl: list[DomesticAccountDailyRealizedProfitLossDetailsItem] = Field(
        default_factory=list,
        description="당일실현손익상세",
    )


class DomesticAccountProfitRateItem(BaseModel):
    dt: str = Field(default="", description="일자")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    cur_prc: str = Field(default="", description="현재가")
    pur_pric: str = Field(default="", description="매입가")
    pur_amt: str = Field(default="", description="매입금액")
    rmnd_qty: str = Field(default="", description="보유수량")
    tdy_sel_pl: str = Field(default="", description="당일매도손익")
    tdy_trde_cmsn: str = Field(default="", description="당일매매수수료")
    tdy_trde_tax: str = Field(default="", description="당일매매세금")
    crd_tp: str = Field(default="", description="신용구분")
    loan_dt: str = Field(default="", description="대출일")
    setl_remn: str = Field(default="", description="결제잔고")
    clrn_alow_qty: str = Field(default="", description="청산가능수량")
    crd_amt: str = Field(default="", description="신용금액")
    crd_int: str = Field(default="", description="신용이자")
    expr_dt: str = Field(default="", description="만기일")


class DomesticAccountProfitRate(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="계좌수익률요청 응답")

    acnt_prft_rt: list[DomesticAccountProfitRateItem] = Field(
        default_factory=list,
        description="계좌수익률",
    )


class DomesticAccountUnexecutedSplitOrderDetailsItem(BaseModel):
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    ord_no: str = Field(default="", description="주문번호")
    ord_qty: str = Field(default="", description="주문수량")
    ord_pric: str = Field(default="", description="주문가격")
    osop_qty: str = Field(default="", description="미체결수량")
    io_tp_nm: str = Field(default="", description="주문구분")
    trde_tp: str = Field(default="", description="매매구분")
    sell_tp: str = Field(default="", description="매도/수 구분")
    cntr_qty: str = Field(default="", description="체결량")
    ord_stt: str = Field(default="", description="주문상태")
    cur_prc: str = Field(default="", description="현재가")
    stex_tp: str = Field(default="", description="거래소구분. 0 : 통합, 1 : KRX, 2 : NXT")
    stex_tp_txt: str = Field(default="", description="거래소구분텍스트")


class DomesticAccountUnexecutedSplitOrderDetails(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미체결분할주문상세 응답")

    osop: list[DomesticAccountUnexecutedSplitOrderDetailsItem] = Field(
        default_factory=list,
        description="미체결분할주문리스트",
    )


class DomesticAccountCurrentDayTradingJournalItem(BaseModel):
    stk_nm: str = Field(default="", description="종목명")
    buy_avg_pric: str = Field(default="", description="매수평균가")
    buy_qty: str = Field(default="", description="매수수량")
    sel_avg_pric: str = Field(default="", description="매도평균가")
    sell_qty: str = Field(default="", description="매도수량")
    cmsn_alm_tax: str = Field(default="", description="수수료_제세금")
    pl_amt: str = Field(default="", description="손익금액")
    sell_amt: str = Field(default="", description="매도금액")
    buy_amt: str = Field(default="", description="매수금액")
    prft_rt: str = Field(default="", description="수익률")
    stk_cd: str = Field(default="", description="종목코드")


class DomesticAccountCurrentDayTradingJournal(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="당일매매일지조회 응답")

    tot_sell_amt: str = Field(default="", description="총매도금액")
    tot_buy_amt: str = Field(default="", description="총매수금액")
    tot_cmsn_tax: str = Field(default="", description="총수수료_세금")
    tot_exct_amt: str = Field(default="", description="총정산금액")
    tot_pl_amt: str = Field(default="", description="총손익금액")
    tot_prft_rt: str = Field(default="", description="총수익률")
    tdy_trde_diary: list[DomesticAccountCurrentDayTradingJournalItem] = Field(
        default_factory=list,
        description="당일매매일지",
    )


class DomesticAccountDepositBalanceDetailsItem(BaseModel):
    crnc_cd: str = Field(default="", description="통화코드")
    fx_entr: str = Field(default="", description="외화예수금")
    fc_krw_repl_evlta: str = Field(default="", description="원화대용평가금")
    fc_trst_profa: str = Field(default="", description="해외주식증거금")
    pymn_alow_amt: str = Field(default="", description="출금가능금액")
    pymn_alow_amt_entr: str = Field(default="", description="출금가능금액(예수금)")
    ord_alow_amt_entr: str = Field(default="", description="주문가능금액(예수금)")
    fc_uncla: str = Field(default="", description="외화미수(합계)")
    fc_ch_uncla: str = Field(default="", description="외화현금미수금")
    dly_amt: str = Field(default="", description="연체료")
    d1_fx_entr: str = Field(default="", description="d+1외화예수금")
    d2_fx_entr: str = Field(default="", description="d+2외화예수금")
    d3_fx_entr: str = Field(default="", description="d+3외화예수금")
    d4_fx_entr: str = Field(default="", description="d+4외화예수금")


class DomesticAccountDepositBalanceDetails(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="예수금상세현황요청 응답")

    entr: str = Field(default="", description="예수금")
    profa_ch: str = Field(default="", description="주식증거금현금")
    bncr_profa_ch: str = Field(default="", description="수익증권증거금현금")
    nxdy_bncr_sell_exct: str = Field(default="", description="익일수익증권매도정산대금")
    fc_stk_krw_repl_set_amt: str = Field(default="", description="해외주식원화대용설정금")
    crd_grnta_ch: str = Field(default="", description="신용보증금현금")
    crd_grnt_ch: str = Field(default="", description="신용담보금현금")
    add_grnt_ch: str = Field(default="", description="추가담보금현금")
    etc_profa: str = Field(default="", description="기타증거금")
    uncl_stk_amt: str = Field(default="", description="미수확보금")
    shrts_prica: str = Field(default="", description="공매도대금")
    crd_set_grnta: str = Field(default="", description="신용설정평가금")
    chck_ina_amt: str = Field(default="", description="수표입금액")
    etc_chck_ina_amt: str = Field(default="", description="기타수표입금액")
    crd_grnt_ruse: str = Field(default="", description="신용담보재사용")
    knx_asset_evltv: str = Field(default="", description="코넥스기본예탁금")
    elwdpst_evlta: str = Field(default="", description="ELW예탁평가금")
    crd_ls_rght_frcs_amt: str = Field(default="", description="신용대주권리예정금액")
    lvlh_join_amt: str = Field(default="", description="생계형가입금액")
    lvlh_trns_alowa: str = Field(default="", description="생계형입금가능금액")
    repl_amt: str = Field(default="", description="대용금평가금(합계)")
    remn_repl_evlta: str = Field(default="", description="잔고대용평가금액")
    trst_remn_repl_evlta: str = Field(default="", description="위탁대용잔고평가금액")
    bncr_remn_repl_evlta: str = Field(default="", description="수익증권대용평가금액")
    profa_repl: str = Field(default="", description="위탁증거금대용")
    crd_grnta_repl: str = Field(default="", description="신용보증금대용")
    crd_grnt_repl: str = Field(default="", description="신용담보금대용")
    add_grnt_repl: str = Field(default="", description="추가담보금대용")
    rght_repl_amt: str = Field(default="", description="권리대용금")
    pymn_alow_amt: str = Field(default="", description="출금가능금액")
    wrap_pymn_alow_amt: str = Field(default="", description="랩출금가능금액")
    ord_alow_amt: str = Field(default="", description="주문가능금액")
    bncr_buy_alowa: str = Field(default="", description="수익증권매수가능금액")
    stk_ord_alow_amt_20: str = Field(default="", description="20%종목주문가능금액", alias="20stk_ord_alow_amt")
    stk_ord_alow_amt_30: str = Field(default="", description="30%종목주문가능금액", alias="30stk_ord_alow_amt")
    stk_ord_alow_amt_40: str = Field(default="", description="40%종목주문가능금액", alias="40stk_ord_alow_amt")
    stk_ord_alow_amt_100: str = Field(default="", description="100%종목주문가능금액", alias="100stk_ord_alow_amt")
    ch_uncla: str = Field(default="", description="현금미수금")
    ch_uncla_dlfe: str = Field(default="", description="현금미수연체료")
    ch_uncla_tot: str = Field(default="", description="현금미수금합계")
    crd_int_npay: str = Field(default="", description="신용이자미납")
    int_npay_amt_dlfe: str = Field(default="", description="신용이자미납연체료")
    int_npay_amt_tot: str = Field(default="", description="신용이자미납합계")
    etc_loana: str = Field(default="", description="기타대여금")
    etc_loana_dlfe: str = Field(default="", description="기타대여금연체료")
    etc_loan_tot: str = Field(default="", description="기타대여금합계")
    nrpy_loan: str = Field(default="", description="미상환융자금")
    loan_sum: str = Field(default="", description="융자금합계")
    ls_sum: str = Field(default="", description="대주금합계")
    crd_grnt_rt: str = Field(default="", description="신용담보비율")
    mdstrm_usfe: str = Field(default="", description="중도이용료")
    min_ord_alow_yn: str = Field(default="", description="최소주문가능금액")
    loan_remn_evlt_amt: str = Field(default="", description="대출총평가금액")
    dpst_grntl_remn: str = Field(default="", description="예탁담보대출잔고")
    sell_grntl_remn: str = Field(default="", description="매도담보대출잔고")
    d1_entra: str = Field(default="", description="d+1추정예수금")
    d1_slby_exct_amt: str = Field(default="", description="d+1매도매수정산금")
    d1_buy_exct_amt: str = Field(default="", description="d+1매수정산금")
    d1_out_rep_mor: str = Field(default="", description="d+1미수변제소요금")
    d1_sel_exct_amt: str = Field(default="", description="d+1매도정산금")
    d1_pymn_alow_amt: str = Field(default="", description="d+1출금가능금액")
    d2_entra: str = Field(default="", description="d+2추정예수금")
    d2_slby_exct_amt: str = Field(default="", description="d+2매도매수정산금")
    d2_buy_exct_amt: str = Field(default="", description="d+2매수정산금")
    d2_out_rep_mor: str = Field(default="", description="d+2미수변제소요금")
    d2_sel_exct_amt: str = Field(default="", description="d+2매도정산금")
    d2_pymn_alow_amt: str = Field(default="", description="d+2출금가능금액")
    stk_ord_allow_amt_50: str = Field(default="", description="50%종목주문가능금액", alias="50stk_ord_alow_amt")
    stk_ord_allow_amt_60: str = Field(default="", description="60%종목주문가능금액", alias="60stk_ord_alow_amt")
    stk_entr_prst: list[DomesticAccountDepositBalanceDetailsItem] = Field(
        default_factory=list,
        description="종목별예수금",
    )


class DomesticAccountDailyEstimatedDepositAssetBalanceItem(BaseModel):
    dt: str = Field(default="", description="일자")
    entr: str = Field(default="", description="예수금")
    grnt_use_amt: str = Field(default="", description="담보대출금")
    crd_loan: str = Field(default="", description="신용융자금")
    ls_grnt: str = Field(default="", description="대주담보금")
    repl_amt: str = Field(default="", description="대용금")
    prsm_dpst_aset_amt: str = Field(default="", description="추정예탁자산")
    prsm_dpst_aset_amt_bncr_skip: str = Field(default="", description="추정예탁자산수익증권제외")


class DomesticAccountDailyEstimatedDepositAssetBalance(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="일별추정예탁자산현황요청 응답")

    daly_prsm_dpst_aset_amt_prst: list[DomesticAccountDailyEstimatedDepositAssetBalanceItem] = Field(
        default_factory=list,
        description="일별추정예탁자산현황",
    )


class DomesticAccountEstimatedAssetBalance(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="추정자산조회요청 응답")

    prsm_dpst_aset_amt: str = Field(default="", description="추정예탁자산")


class DomesticAccountEvaluationStatusItem(BaseModel):
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    rmnd_qty: str = Field(default="", description="보유수량")
    avg_prc: str = Field(default="", description="평균단가")
    cur_prc: str = Field(default="", description="현재가")
    evlt_amt: str = Field(default="", description="평가금액")
    pl_amt: str = Field(default="", description="손익금액")
    pl_rt: str = Field(default="", description="손익율")
    loan_dt: str = Field(default="", description="대출일")
    pur_amt: str = Field(default="", description="매입금액")
    setl_remn: str = Field(default="", description="결제잔고")
    pred_buyq: str = Field(default="", description="전일매수수량")
    pred_sellq: str = Field(default="", description="전일매도수량")
    tdy_buyq: str = Field(default="", description="금일매수수량")
    tdy_sellq: str = Field(default="", description="금일매도수량")


class DomesticAccountEvaluationStatus(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="계좌평가현황요청 응답")

    acnt_nm: str = Field(default="", description="계좌명")
    brch_nm: str = Field(default="", description="지점명")
    entr: str = Field(default="", description="예수금")
    d2_entra: str = Field(default="", description="D+2추정예수금")
    tot_est_amt: str = Field(default="", description="유가잔고평가액")
    aset_evlt_amt: str = Field(default="", description="예탁자산평가액")
    tot_pur_amt: str = Field(default="", description="총매입금액")
    prsm_dpst_aset_amt: str = Field(default="", description="추정예탁자산")
    tot_grnt_sella: str = Field(default="", description="매도담보대출금")
    tdy_lspft_amt: str = Field(default="", description="당일투자원금")
    invt_bsamt: str = Field(default="", description="당월투자원금")
    lspft_amt: str = Field(default="", description="누적투자원금")
    tdy_lspft: str = Field(default="", description="당일투자손익")
    lspft2: str = Field(default="", description="당월투자손익")
    lspft: str = Field(default="", description="누적투자손익")
    tdy_lspft_rt: str = Field(default="", description="당일손익율")
    lspft_ratio: str = Field(default="", description="당월손익율")
    lspft_rt: str = Field(default="", description="누적손익율")
    stk_acnt_evlt_prst: list[DomesticAccountEvaluationStatusItem] = Field(
        default_factory=list,
        description="종목별계좌평가현황",
    )


class DomesticAccountExecutionBalanceItem(BaseModel):
    crd_tp: str = Field(default="", description="신용구분")
    loan_dt: str = Field(default="", description="대출일")
    expr_dt: str = Field(default="", description="만기일")
    stk_cd: str = Field(default="", description="종목번호")
    stk_nm: str = Field(default="", description="종목명")
    setl_remn: str = Field(default="", description="결제잔고")
    cur_qty: str = Field(default="", description="현재잔고")
    cur_prc: str = Field(default="", description="현재가")
    buy_uv: str = Field(default="", description="매입단가")
    pur_amt: str = Field(default="", description="매입금액")
    evlt_amt: str = Field(default="", description="평가금액")
    evltv_prft: str = Field(default="", description="평가손익")
    pl_rt: str = Field(default="", description="손익률")


class DomesticAccountExecutionBalance(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="체결잔고요청 응답")

    entr: str = Field(default="", description="예수금")
    entr_d1: str = Field(default="", description="예수금 D+1")
    entr_d2: str = Field(default="", description="예수금 D+2")
    pymn_alow_amt: str = Field(default="", description="출금가능금액")
    uncl_stk_amt: str = Field(default="", description="미수확보금")
    repl_amt: str = Field(default="", description="대용금")
    rght_repl_amt: str = Field(default="", description="권리대용금")
    ord_alowa: str = Field(default="", description="주문가능현금")
    ch_uncla: str = Field(default="", description="현금미수금")
    crd_int_npay_gold: str = Field(default="", description="신용이자미납금")
    etc_loana: str = Field(default="", description="기타대여금")
    nrpy_loan: str = Field(default="", description="미상환융자금")
    profa_ch: str = Field(default="", description="증거금현금")
    repl_profa: str = Field(default="", description="증거금대용")
    stk_buy_tot_amt: str = Field(default="", description="주식매수총액")
    evlt_amt_tot: str = Field(default="", description="평가금액합계")
    tot_pl_tot: str = Field(default="", description="총손익합계")
    tot_pl_rt: str = Field(default="", description="총손익률")
    tot_re_buy_alowa: str = Field(default="", description="총재매수가능금액")
    ord_alow_amt_20: str = Field(default="", description="20%주문가능금액", alias="20ord_alow_amt")
    ord_alow_amt_30: str = Field(default="", description="30%주문가능금액", alias="30ord_alow_amt")
    ord_alow_amt_40: str = Field(default="", description="40%주문가능금액", alias="40ord_alow_amt")
    ord_alow_amt_50: str = Field(default="", description="50%주문가능금액", alias="50ord_alow_amt")
    ord_alow_amt_60: str = Field(default="", description="60%주문가능금액", alias="60ord_alow_amt")
    ord_alow_amt_100: str = Field(default="", description="100%주문가능금액", alias="100ord_alow_amt")
    crd_loan_tot: str = Field(default="", description="신용융자합계")
    crd_loan_ls_tot: str = Field(default="", description="신용융자대주합계")
    crd_grnt_rt: str = Field(default="", description="신용담보비율")
    dpst_grnt_use_amt_amt: str = Field(default="", description="예탁담보대출금액")
    grnt_loan_amt: str = Field(default="", description="매도담보대출금액")
    stk_cntr_remn: list[DomesticAccountExecutionBalanceItem] = Field(
        default_factory=list,
        description="종목별체결잔고",
    )


class DomesticAccountOrderExecutionDetailsItem(BaseModel):
    ord_no: str = Field(default="", description="주문번호")
    stk_cd: str = Field(default="", description="종목번호")
    trde_tp: str = Field(default="", description="매매구분")
    crd_tp: str = Field(default="", description="신용구분")
    ord_qty: str = Field(default="", description="주문수량")
    ord_uv: str = Field(default="", description="주문단가")
    cnfm_qty: str = Field(default="", description="확인수량")
    acpt_tp: str = Field(default="", description="접수구분")
    rsrv_tp: str = Field(default="", description="반대여부")
    ord_tm: str = Field(default="", description="주문시간")
    ori_ord: str = Field(default="", description="원주문")
    stk_nm: str = Field(default="", description="종목명")
    io_tp_nm: str = Field(default="", description="주문구분")
    loan_dt: str = Field(default="", description="대출일")
    cntr_qty: str = Field(default="", description="체결수량")
    cntr_uv: str = Field(default="", description="체결단가")
    ord_remnq: str = Field(default="", description="주문잔량")
    comm_ord_tp: str = Field(default="", description="통신구분")
    mdfy_cncl: str = Field(default="", description="정정취소")
    cnfm_tm: str = Field(default="", description="확인시간")
    dmst_stex_tp: str = Field(default="", description="국내거래소구분")
    cond_uv: str = Field(default="", description="스톱가")


class DomesticAccountOrderExecutionDetails(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="계좌별주문체결내역상세요청 응답")

    acnt_ord_cntr_prps_dtl: list[DomesticAccountOrderExecutionDetailsItem] = Field(
        default_factory=list,
        description="계좌별주문체결내역상세",
    )


class DomesticAccountNextDaySettlementDetailsItem(BaseModel):
    seq: str = Field(default="", description="일련번호")
    stk_cd: str = Field(default="", description="종목번호")
    loan_dt: str = Field(default="", description="대출일")
    qty: str = Field(default="", description="수량")
    engg_amt: str = Field(default="", description="약정금액")
    cmsn: str = Field(default="", description="수수료")
    incm_tax: str = Field(default="", description="소득세")
    rstx: str = Field(default="", description="농특세")
    stk_nm: str = Field(default="", description="종목명")
    sell_tp: str = Field(default="", description="매도수구분")
    unp: str = Field(default="", description="단가")
    exct_amt: str = Field(default="", description="정산금액")
    trde_tax: str = Field(default="", description="거래세")
    resi_tax: str = Field(default="", description="주민세")
    crd_tp: str = Field(default="", description="신용구분")


class DomesticAccountNextDaySettlementDetails(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="계좌별익일결제예정내역요청 응답")

    trde_dt: str = Field(default="", description="매매일자")
    setl_dt: str = Field(default="", description="결제일자")
    sell_amt_sum: str = Field(default="", description="매도정산합")
    buy_amt_sum: str = Field(default="", description="매수정산합")
    acnt_nxdy_setl_frcs_prps_array: list[DomesticAccountNextDaySettlementDetailsItem] = Field(
        default_factory=list,
        description="계좌별익일결제예정내역배열",
    )


class DomesticAccountOrderExecutionStatusItem(BaseModel):
    stk_bond_tp: str = Field(default="", description="주식채권구분")
    ord_no: str = Field(default="", description="주문번호")
    stk_cd: str = Field(default="", description="종목번호")
    trde_tp: str = Field(default="", description="매매구분")
    io_tp_nm: str = Field(default="", description="주문유형구분")
    ord_qty: str = Field(default="", description="주문수량")
    ord_uv: str = Field(default="", description="주문단가")
    cnfm_qty: str = Field(default="", description="확인수량")
    rsrv_oppo: str = Field(default="", description="예약/반대")
    cntr_no: str = Field(default="", description="체결번호")
    acpt_tp: str = Field(default="", description="접수구분")
    orig_ord_no: str = Field(default="", description="원주문번호")
    stk_nm: str = Field(default="", description="종목명")
    setl_tp: str = Field(default="", description="결제구분")
    crd_deal_tp: str = Field(default="", description="신용거래구분")
    cntr_qty: str = Field(default="", description="체결수량")
    cntr_uv: str = Field(default="", description="체결단가")
    comm_ord_tp: str = Field(default="", description="통신구분")
    mdfy_cncl_tp: str = Field(default="", description="정정/취소구분")
    cntr_tm: str = Field(default="", description="체결시간")
    dmst_stex_tp: str = Field(default="", description="국내거래소구분")
    cond_uv: str = Field(default="", description="스톱가")


class DomesticAccountOrderExecutionStatus(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="계좌별주문체결현황요청 응답")

    sell_grntl_engg_amt: str = Field(default="", description="매도약정금액")
    buy_engg_amt: str = Field(default="", description="매수약정금액")
    engg_amt: str = Field(default="", description="약정금액")
    acnt_ord_cntr_prst_array: list[DomesticAccountOrderExecutionStatusItem] = Field(
        default_factory=list,
        description="계좌별주문체결현황배열",
    )


class DomesticAccountAvailableWithdrawalAmount(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="주문인출가능금액요청 응답")

    profa_20ord_alow_amt: str = Field(default="", description="증거금20%주문가능금액")
    profa_20ord_alowq: str = Field(default="", description="증거금20%주문가능수량")
    profa_30ord_alow_amt: str = Field(default="", description="증거금30%주문가능금액")
    profa_30ord_alowq: str = Field(default="", description="증거금30%주문가능수량")
    profa_40ord_alow_amt: str = Field(default="", description="증거금40%주문가능금액")
    profa_40ord_alowq: str = Field(default="", description="증거금40%주문가능수량")
    profa_50ord_alow_amt: str = Field(default="", description="증거금50%주문가능금액")
    profa_50ord_alowq: str = Field(default="", description="증거금50%주문가능수량")
    profa_60ord_alow_amt: str = Field(default="", description="증거금60%주문가능금액")
    profa_60ord_alowq: str = Field(default="", description="증거금60%주문가능수량")
    profa_rdex_60ord_alow_amt: str = Field(default="", description="증거금감면60%주문가능금액")
    profa_rdex_60ord_alowq: str = Field(default="", description="증거금감면60%주문가능수량")
    profa_100ord_alow_amt: str = Field(default="", description="증거금100%주문가능금액")
    profa_100ord_alowq: str = Field(default="", description="증거금100%주문가능수량")
    pred_reu_alowa: str = Field(default="", description="전일재사용가능금액")
    tdy_reu_alowa: str = Field(default="", description="금일재사용가능금액")
    entr: str = Field(default="", description="예수금")
    repl_amt: str = Field(default="", description="대용금")
    uncla: str = Field(default="", description="미수금")
    ord_pos_repl: str = Field(default="", description="주문가능대용")
    ord_alowa: str = Field(default="", description="주문가능현금")
    wthd_alowa: str = Field(default="", description="인출가능금액")
    nxdy_wthd_alowa: str = Field(default="", description="익일인출가능금액")
    pur_amt: str = Field(default="", description="매입금액")
    cmsn: str = Field(default="", description="수수료")
    pur_exct_amt: str = Field(default="", description="매입정산금")
    d2entra: str = Field(default="", description="D+2추정예수금")
    profa_rdex_aplc_tp: str = Field(default="", description="증거금감면적용구분. 0:일반,1:60%감면")


class DomesticAccountAvailableOrderQuantityByMarginRate(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="증거금율별주문가능수량조회요청 응답")

    stk_profa_rt: str = Field(default="", description="종목증거금율")
    profa_rt: str = Field(default="", description="계좌증거금율")
    aplc_rt: str = Field(default="", description="적용증거금율")
    profa_20ord_alow_amt: str = Field(default="", description="증거금20%주문가능금액")
    profa_20ord_alowq: str = Field(default="", description="증거금20%주문가능수량")
    profa_20pred_reu_amt: str = Field(default="", description="증거금20%전일재사용금액")
    profa_20tdy_reu_amt: str = Field(default="", description="증거금20%금일재사용금액")
    profa_30ord_alow_amt: str = Field(default="", description="증거금30%주문가능금액")
    profa_30ord_alowq: str = Field(default="", description="증거금30%주문가능수량")
    profa_30pred_reu_amt: str = Field(default="", description="증거금30%전일재사용금액")
    profa_30tdy_reu_amt: str = Field(default="", description="증거금30%금일재사용금액")
    profa_40ord_alow_amt: str = Field(default="", description="증거금40%주문가능금액")
    profa_40ord_alowq: str = Field(default="", description="증거금40%주문가능수량")
    profa_40pred_reu_amt: str = Field(default="", description="증거금40%전일재사용금액")
    profa_40tdy_reu_amt: str = Field(default="", description="증거금40%금일재사용금액")
    profa_50ord_alow_amt: str = Field(default="", description="증거금50%주문가능금액")
    profa_50ord_alowq: str = Field(default="", description="증거금50%주문가능수량")
    profa_50pred_reu_amt: str = Field(default="", description="증거금50%전일재사용금액")
    profa_50tdy_reu_amt: str = Field(default="", description="증거금50%금일재사용금액")
    profa_60ord_alow_amt: str = Field(default="", description="증거금60%주문가능금액")
    profa_60ord_alowq: str = Field(default="", description="증거금60%주문가능수량")
    profa_60pred_reu_amt: str = Field(default="", description="증거금60%전일재사용금액")
    profa_60tdy_reu_amt: str = Field(default="", description="증거금60%금일재사용금액")
    profa_100ord_alow_amt: str = Field(default="", description="증거금100%주문가능금액")
    profa_100ord_alowq: str = Field(default="", description="증거금100%주문가능수량")
    profa_100pred_reu_amt: str = Field(default="", description="증거금100%전일재사용금액")
    profa_100tdy_reu_amt: str = Field(default="", description="증거금100%금일재사용금액")
    min_ord_alow_amt: str = Field(default="", description="미수불가주문가능금액")
    min_ord_alowq: str = Field(default="", description="미수불가주문가능수량")
    min_pred_reu_amt: str = Field(default="", description="미수불가전일재사용금액")
    min_tdy_reu_amt: str = Field(default="", description="미수불가금일재사용금액")
    entr: str = Field(default="", description="예수금")
    repl_amt: str = Field(default="", description="대용금")
    uncla: str = Field(default="", description="미수금")
    ord_pos_repl: str = Field(default="", description="주문가능대용")
    ord_alowa: str = Field(default="", description="주문가능현금")


class DomesticAccountAvailableOrderQuantityByMarginLoanStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="신용융자증권별주문가능수량요청 응답")

    stk_assr_rt: str = Field(default="", description="종목보증금율")
    stk_assr_rt_nm: str = Field(default="", description="종목보증금율명")
    assr_30ord_alow_amt: str = Field(default="", description="보증금30%주문가능금액")
    assr_30ord_alowq: str = Field(default="", description="보증금30%주문가능수량")
    assr_30pred_reu_amt: str = Field(default="", description="보증금30%전일재사용금액")
    assr_30tdy_reu_amt: str = Field(default="", description="보증금30%금일재사용금액")
    assr_40ord_alow_amt: str = Field(default="", description="보증금40%주문가능금액")
    assr_40ord_alowq: str = Field(default="", description="보증금40%주문가능수량")
    assr_40pred_reu_amt: str = Field(default="", description="보증금40%전일재사용금액")
    assr_40tdy_reu_amt: str = Field(default="", description="보증금40%금일재사용금액")
    assr_50ord_alow_amt: str = Field(default="", description="보증금50%주문가능금액")
    assr_50ord_alowq: str = Field(default="", description="보증금50%주문가능수량")
    assr_50pred_reu_amt: str = Field(default="", description="보증금50%전일재사용금액")
    assr_50tdy_reu_amt: str = Field(default="", description="보증금50%금일재사용금액")
    assr_60ord_alow_amt: str = Field(default="", description="보증금60%주문가능금액")
    assr_60ord_alowq: str = Field(default="", description="보증금60%주문가능수량")
    assr_60pred_reu_amt: str = Field(default="", description="보증금60%전일재사용금액")
    assr_60tdy_reu_amt: str = Field(default="", description="보증금60%금일재사용금액")
    entr: str = Field(default="", description="예수금")
    repl_amt: str = Field(default="", description="대용금")
    uncla: str = Field(default="", description="미수금")
    ord_pos_repl: str = Field(default="", description="주문가능대용")
    ord_alowa: str = Field(default="", description="주문가능현금")
    out_alowa: str = Field(default="", description="미수가능금액")
    out_pos_qty: str = Field(default="", description="미수가능수량")
    min_amt: str = Field(default="", description="미수불가금액")
    min_qty: str = Field(default="", description="미수불가수량")


class DomesticAccountMarginDetails(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="증거금세부내역조회요청 응답")

    tdy_reu_objt_amt: str = Field(default="", description="금일재사용대상금액")
    tdy_reu_use_amt: str = Field(default="", description="금일재사용사용금액")
    tdy_reu_alowa: str = Field(default="", description="금일재사용가능금액")
    tdy_reu_lmtt_amt: str = Field(default="", description="금일재사용제한금액")
    tdy_reu_alowa_fin: str = Field(default="", description="금일재사용가능금액최종")
    pred_reu_objt_amt: str = Field(default="", description="전일재사용대상금액")
    pred_reu_use_amt: str = Field(default="", description="전일재사용사용금액")
    pred_reu_alowa: str = Field(default="", description="전일재사용가능금액")
    pred_reu_lmtt_amt: str = Field(default="", description="전일재사용제한금액")
    pred_reu_alowa_fin: str = Field(default="", description="전일재사용가능금액최종")
    ch_amt: str = Field(default="", description="현금금액")
    ch_profa: str = Field(default="", description="현금증거금")
    use_pos_ch: str = Field(default="", description="사용가능현금")
    ch_use_lmtt_amt: str = Field(default="", description="현금사용제한금액")
    use_pos_ch_fin: str = Field(default="", description="사용가능현금최종")
    repl_amt_amt: str = Field(default="", description="대용금액")
    repl_profa: str = Field(default="", description="대용증거금")
    use_pos_repl: str = Field(default="", description="사용가능대용")
    repl_use_lmtt_amt: str = Field(default="", description="대용사용제한금액")
    use_pos_repl_fin: str = Field(default="", description="사용가능대용최종")
    crd_grnta_ch: str = Field(default="", description="신용보증금현금")
    crd_grnta_repl: str = Field(default="", description="신용보증금대용")
    crd_grnt_ch: str = Field(default="", description="신용담보금현금")
    crd_grnt_repl: str = Field(default="", description="신용담보금대용")
    uncla: str = Field(default="", description="미수금")
    ls_grnt_reu_gold: str = Field(default="", description="대주담보금재사용금")
    ord_alow_amt_20: str = Field(default="", description="20%주문가능금액", alias="20ord_alow_amt")
    ord_alow_amt_30: str = Field(default="", description="30%주문가능금액", alias="30ord_alow_amt")
    ord_alow_amt_40: str = Field(default="", description="40%주문가능금액", alias="40ord_alow_amt")
    ord_alow_amt_50: str = Field(default="", description="50%주문가능금액", alias="50ord_alow_amt")
    ord_alow_amt_60: str = Field(default="", description="60%주문가능금액", alias="60ord_alow_amt")
    ord_alow_amt_100: str = Field(default="", description="100%주문가능금액", alias="100ord_alow_amt")
    tdy_crd_rpya_loss_amt: str = Field(default="", description="금일신용상환손실금액")
    pred_crd_rpya_loss_amt: str = Field(default="", description="전일신용상환손실금액")
    tdy_ls_rpya_loss_repl_profa: str = Field(default="", description="금일대주상환손실대용증거금")
    pred_ls_rpya_loss_repl_profa: str = Field(default="", description="전일대주상환손실대용증거금")
    evlt_repl_amt_spg_use_skip: str = Field(default="", description="평가대용금(현물사용제외)")
    evlt_repl_rt: str = Field(default="", description="평가대용비율")
    crd_repl_profa: str = Field(default="", description="신용대용증거금")
    ch_ord_repl_profa: str = Field(default="", description="현금주문대용증거금")
    crd_ord_repl_profa: str = Field(default="", description="신용주문대용증거금")
    crd_repl_conv_gold: str = Field(default="", description="신용대용환산금")
    repl_alowa: str = Field(default="", description="대용가능금액(현금제한)")
    repl_alowa_2: str = Field(default="", description="대용가능금액2(신용제한)")
    ch_repl_lck_gold: str = Field(default="", description="현금대용부족금")
    crd_repl_lck_gold: str = Field(default="", description="신용대용부족금")
    ch_ord_alow_repla: str = Field(default="", description="현금주문가능대용금")
    crd_ord_alow_repla: str = Field(default="", description="신용주문가능대용금")
    d2vexct_entr: str = Field(default="", description="D2가정산예수금")
    d2ch_ord_alow_amt: str = Field(default="", description="D2현금주문가능금액")


class DomesticAccountConsignmentComprehensiveTransactionHistoryItem(BaseModel):
    trde_dt: str = Field(default="", description="거래일자")
    trde_no: str = Field(default="", description="거래번호")
    rmrk_nm: str = Field(default="", description="적요명")
    crd_deal_tp_nm: str = Field(default="", description="신용거래구분명")
    exct_amt: str = Field(default="", description="정산금액")
    loan_amt_rpya: str = Field(default="", description="대출금상환")
    fc_trde_amt: str = Field(default="", description="거래금액(외)")
    fc_exct_amt: str = Field(default="", description="정산금액(외)")
    entra_remn: str = Field(default="", description="예수금잔고")
    crnc_cd: str = Field(default="", description="통화코드")
    trde_ocr_tp: str = Field(
        default="",
        description="거래종류구분. 1:입출금, 2:펀드, 3:ELS, 4:채권, 5:해외채권, 6:외화RP, 7:외화발행어음",
    )
    trde_kind_nm: str = Field(default="", description="거래종류명")
    stk_nm: str = Field(default="", description="종목명")
    trde_amt: str = Field(default="", description="거래금액")
    trde_agri_tax: str = Field(default="", description="거래및농특세")
    rpy_diffa: str = Field(default="", description="상환차금")
    fc_trde_tax: str = Field(default="", description="거래세(외)")
    dly_sum: str = Field(default="", description="연체합")
    fc_entra: str = Field(default="", description="외화예수금잔고")
    mdia_tp_nm: str = Field(default="", description="매체구분명")
    io_tp: str = Field(default="", description="입출구분")
    io_tp_nm: str = Field(default="", description="입출구분명")
    orig_deal_no: str = Field(default="", description="원거래번호")
    stk_cd: str = Field(default="", description="종목코드")
    trde_qty_jwa_cnt: str = Field(default="", description="거래수량/좌수")
    cmsn: str = Field(default="", description="수수료")
    int_ls_usfe: str = Field(default="", description="이자/대주이용")
    fc_cmsn: str = Field(default="", description="수수료(외)")
    fc_dly_sum: str = Field(default="", description="연체합(외)")
    vlbl_nowrm: str = Field(default="", description="유가금잔")
    proc_tm: str = Field(default="", description="처리시간")
    isin_cd: str = Field(default="", description="ISIN코드")
    stex_cd: str = Field(default="", description="거래소코드")
    stex_nm: str = Field(default="", description="거래소명")
    trde_unit: str = Field(default="", description="거래단가/환율")
    incm_resi_tax: str = Field(default="", description="소득/주민세")
    loan_dt: str = Field(default="", description="대출일")
    uncl_ocr: str = Field(default="", description="미수(원/주)")
    rpym_sum: str = Field(default="", description="변제합")
    cntr_dt: str = Field(default="", description="체결일")
    rcpy_no: str = Field(default="", description="출납번호")
    prcsr: str = Field(default="", description="처리자")
    proc_brch: str = Field(default="", description="처리점")
    trde_stle: str = Field(default="", description="매매형태")
    txon_base_pric: str = Field(default="", description="과세기준가")
    tax_sum_cmsn: str = Field(default="", description="세금수수료합")
    frgn_pay_txam: str = Field(default="", description="외국납부세액(외)")
    fc_uncl_ocr: str = Field(default="", description="미수(외)")
    rpym_sum_fr: str = Field(default="", description="변제합(외)")
    rcpmnyer: str = Field(default="", description="입금자")
    trde_prtc_tp: str = Field(default="", description="거래내역구분")


class DomesticAccountConsignmentComprehensiveTransactionHistory(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="위탁종합거래내역요청 응답")

    acnt_no: str = Field(default="", description="계좌번호")
    trst_ovrl_trde_prps_array: list[DomesticAccountConsignmentComprehensiveTransactionHistoryItem] = Field(
        default_factory=list,
        description="위탁종합거래내역배열",
    )


class DomesticAccountDailyProfitRateDetails(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="일별계좌수익률상세현황요청 응답")

    mang_empno: str = Field(default="", description="관리사원번호")
    mngr_nm: str = Field(default="", description="관리자명")
    dept_nm: str = Field(default="", description="관리자지점")
    entr_fr: str = Field(default="", description="예수금_초")
    entr_to: str = Field(default="", description="예수금_말")
    scrt_evlt_amt_fr: str = Field(default="", description="유가증권평가금액_초")
    scrt_evlt_amt_to: str = Field(default="", description="유가증권평가금액_말")
    ls_grnt_fr: str = Field(default="", description="대주담보금_초")
    ls_grnt_to: str = Field(default="", description="대주담보금_말")
    crd_loan_fr: str = Field(default="", description="신용융자금_초")
    crd_loan_to: str = Field(default="", description="신용융자금_말")
    ch_uncla_fr: str = Field(default="", description="현금미수금_초")
    ch_uncla_to: str = Field(default="", description="현금미수금_말")
    krw_asgna_fr: str = Field(default="", description="원화대용금_초")
    krw_asgna_to: str = Field(default="", description="원화대용금_말")
    ls_evlta_fr: str = Field(default="", description="대주평가금_초")
    ls_evlta_to: str = Field(default="", description="대주평가금_말")
    rght_evlta_fr: str = Field(default="", description="권리평가금_초")
    rght_evlta_to: str = Field(default="", description="권리평가금_말")
    loan_amt_fr: str = Field(default="", description="대출금_초")
    loan_amt_to: str = Field(default="", description="대출금_말")
    etc_loana_fr: str = Field(default="", description="기타대여금_초")
    etc_loana_to: str = Field(default="", description="기타대여금_말")
    crd_int_npay_gold_fr: str = Field(default="", description="신용이자미납금_초")
    crd_int_npay_gold_to: str = Field(default="", description="신용이자미납금_말")
    crd_int_fr: str = Field(default="", description="신용이자_초")
    crd_int_to: str = Field(default="", description="신용이자_말")
    tot_amt_fr: str = Field(default="", description="순자산액계_초")
    tot_amt_to: str = Field(default="", description="순자산액계_말")
    invt_bsamt: str = Field(default="", description="투자원금평잔")
    evltv_prft: str = Field(default="", description="평가손익")
    prft_rt: str = Field(default="", description="수익률")
    tern_rt: str = Field(default="", description="회전율")
    termin_tot_trns: str = Field(default="", description="기간내총입금")
    termin_tot_pymn: str = Field(default="", description="기간내총출금")
    termin_tot_inq: str = Field(default="", description="기간내총입고")
    termin_tot_outq: str = Field(default="", description="기간내총출고")
    futr_repl_sella: str = Field(default="", description="선물대용매도금액")
    trst_repl_sella: str = Field(default="", description="위탁대용매도금액")


class DomesticAccountCurrentDayStatus(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="계좌별당일현황요청 응답")

    d2_entra: str = Field(default="", description="D+2추정예수금")
    crd_int_npay_gold: str = Field(default="", description="신용이자미납금")
    etc_loana: str = Field(default="", description="기타대여금")
    gnrl_stk_evlt_amt_d2: str = Field(default="", description="일반주식평가금액D+2")
    dpst_grnt_use_amt_d2: str = Field(default="", description="예탁담보대출금D+2")
    crd_stk_evlt_amt_d2: str = Field(default="", description="예탁담보주식평가금액D+2")
    crd_loan_d2: str = Field(default="", description="신용융자금D+2")
    crd_loan_evlta_d2: str = Field(default="", description="신용융자평가금D+2")
    crd_ls_grnt_d2: str = Field(default="", description="신용대주담보금D+2")
    crd_ls_evlta_d2: str = Field(default="", description="신용대주평가금D+2")
    ina_amt: str = Field(default="", description="입금금액")
    outa: str = Field(default="", description="출금금액")
    inq_amt: str = Field(default="", description="입고금액")
    outq_amt: str = Field(default="", description="출고금액")
    sell_amt: str = Field(default="", description="매도금액")
    buy_amt: str = Field(default="", description="매수금액")
    cmsn: str = Field(default="", description="수수료")
    tax: str = Field(default="", description="세금")
    stk_pur_cptal_loan_amt: str = Field(default="", description="주식매입자금대출금")
    rp_evlt_amt: str = Field(default="", description="RP평가금액")
    bd_evlt_amt: str = Field(default="", description="채권평가금액")
    elsevlt_amt: str = Field(default="", description="ELS평가금액")
    crd_int_amt: str = Field(default="", description="신용이자금액")
    sel_prica_grnt_loan_int_amt_amt: str = Field(default="", description="매도대금담보대출이자금액")
    dvida_amt: str = Field(default="", description="배당금액")


class DomesticAccountEvaluationBalanceDetailsItem(BaseModel):
    stk_cd: str = Field(default="", description="종목번호")
    stk_nm: str = Field(default="", description="종목명")
    evltv_prft: str = Field(default="", description="평가손익")
    prft_rt: str = Field(default="", description="수익률(%)")
    pur_pric: str = Field(default="", description="매입가")
    pred_close_pric: str = Field(default="", description="전일종가")
    rmnd_qty: str = Field(default="", description="보유수량")
    trde_able_qty: str = Field(default="", description="매매가능수량")
    cur_prc: str = Field(default="", description="현재가")
    pred_buyq: str = Field(default="", description="전일매수수량")
    pred_sellq: str = Field(default="", description="전일매도수량")
    tdy_buyq: str = Field(default="", description="금일매수수량")
    tdy_sellq: str = Field(default="", description="금일매도수량")
    pur_amt: str = Field(default="", description="매입금액")
    pur_cmsn: str = Field(default="", description="매입수수료")
    evlt_amt: str = Field(default="", description="평가금액")
    sell_cmsn: str = Field(default="", description="평가수수료")
    tax: str = Field(default="", description="세금")
    sum_cmsn: str = Field(default="", description="수수료합")
    poss_rt: str = Field(default="", description="보유비중(%)")
    crd_tp: str = Field(default="", description="신용구분")
    crd_tp_nm: str = Field(default="", description="신용구분명")
    crd_loan_dt: str = Field(default="", description="대출일")


class DomesticAccountEvaluationBalanceDetails(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="계좌평가잔고내역요청 응답")

    tot_pur_amt: str = Field(default="", description="총매입금액")
    tot_evlt_amt: str = Field(default="", description="총평가금액")
    tot_evlt_pl: str = Field(default="", description="총평가손익금액")
    tot_prft_rt: str = Field(default="", description="총수익률(%)")
    prsm_dpst_aset_amt: str = Field(default="", description="추정예탁자산")
    tot_loan_amt: str = Field(default="", description="총대출금")
    tot_crd_loan_amt: str = Field(default="", description="총융자금액")
    tot_crd_ls_amt: str = Field(default="", description="총대주금액")
    acnt_evlt_remn_indv_tot: list[DomesticAccountEvaluationBalanceDetailsItem] = Field(
        default_factory=list, description="계좌평가잔고개별합산"
    )
