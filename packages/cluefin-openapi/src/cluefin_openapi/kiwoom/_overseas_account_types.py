from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

from cluefin_openapi.kiwoom._model import KiwoomHttpBody


class OverseasAccountDailyProfitRateItem(BaseModel):
    base_dt: str = Field(default="", description="기준일")
    stk_evlta: str = Field(default="", description="주식평가금")
    pl_amt: str = Field(default="", description="손익금액")
    dvid_amt: str = Field(default="", description="배당금액")
    cmsn_tax: str = Field(default="", description="수수료+세금")
    acum_pl_amt: str = Field(default="", description="누적손익")
    pymn_amt: str = Field(default="", description="출금금액")
    dast: str = Field(default="", description="예탁자산")
    dly_amt: str = Field(default="", description="연체금액")
    sell_amt: str = Field(default="", description="매도금액")
    buy_amt: str = Field(default="", description="매수금액")
    prft_rt: str = Field(default="", description="수익률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    frgn_stk_outq_amt: str = Field(default="", description="출고금액")
    frgn_stk_inq_amt: str = Field(default="", description="입고금액")
    ina_amt: str = Field(default="", description="입금금액")
    exrt: str = Field(default="", description="환율")


class OverseasAccountDailyProfitRate(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 일별계좌수익률현황 응답")

    result_list: list[OverseasAccountDailyProfitRateItem] = Field(default_factory=list, description="결과리스트")


class OverseasAccountMonthlyProfitRateItem(BaseModel):
    base_dt: str = Field(default="", description="기준일")
    stk_evlta: str = Field(default="", description="주식평가금")
    pl_amt: str = Field(default="", description="손익금액")
    dvid_amt: str = Field(default="", description="배당금액")
    cmsn_tax: str = Field(default="", description="수수료+세금")
    acum_pl_amt: str = Field(default="", description="누적손익")
    pymn_amt: str = Field(default="", description="출금금액")
    dast: str = Field(default="", description="예탁자산")
    dly_amt: str = Field(default="", description="연체금액")
    sell_amt: str = Field(default="", description="매도금액")
    buy_amt: str = Field(default="", description="매수금액")
    prft_rt: str = Field(default="", description="수익률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    frgn_stk_outq_amt: str = Field(default="", description="출고금액")
    frgn_stk_inq_amt: str = Field(default="", description="입고금액")
    ina_amt: str = Field(default="", description="입금금액")
    exrt: str = Field(default="", description="환율")


class OverseasAccountMonthlyProfitRate(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 월별계좌수익률현황 응답")

    result_list: list[OverseasAccountMonthlyProfitRateItem] = Field(default_factory=list, description="결과리스트")


class OverseasAccountYearlyProfitRateItem(BaseModel):
    base_dt: str = Field(default="", description="기준일")
    stk_evlta: str = Field(default="", description="주식평가금")
    pl_amt: str = Field(default="", description="손익금액")
    dvid_amt: str = Field(default="", description="배당금액")
    cmsn_tax: str = Field(default="", description="수수료+세금")
    acum_pl_amt: str = Field(default="", description="누적손익")
    pymn_amt: str = Field(default="", description="출금금액")
    dast: str = Field(default="", description="예탁자산")
    dly_amt: str = Field(default="", description="연체금액")
    sell_amt: str = Field(default="", description="매도금액")
    buy_amt: str = Field(default="", description="매수금액")
    prft_rt: str = Field(default="", description="수익률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    frgn_stk_outq_amt: str = Field(default="", description="출고금액")
    frgn_stk_inq_amt: str = Field(default="", description="입고금액")
    ina_amt: str = Field(default="", description="입금금액")
    exrt: str = Field(default="", description="환율")


class OverseasAccountYearlyProfitRate(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 연도별계좌수익률현황 응답")

    result_list: list[OverseasAccountYearlyProfitRateItem] = Field(default_factory=list, description="결과리스트")


class OverseasAccountDailyStockProfitRateItem(BaseModel):
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    frst_base_dt: str = Field(default="", description="최초기준일")
    last_base_dt: str = Field(default="", description="최종기준일")
    pl_amt: str = Field(default="", description="매매수익")
    prft_rt: str = Field(default="", description="수익률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    frst_stk_evlta: str = Field(default="", description="최초주식평가금")
    last_stk_evlta: str = Field(default="", description="최종주식평가금")
    frst_qty: str = Field(default="", description="최초수량")
    last_qty: str = Field(default="", description="최종수량")
    buy_qty: str = Field(default="", description="매수수량. 단위: 1주")
    sell_qty: str = Field(default="", description="매도수량. 단위: 1주")
    buy_amt: str = Field(default="", description="매수금. 단위: 1주")
    sell_amt: str = Field(default="", description="매도금. 단위: 1주")
    frgn_stk_inq_amt: str = Field(default="", description="입고평가금")
    frgn_stk_outq_amt: str = Field(default="", description="출고평가금")
    cmsn_tax: str = Field(default="", description="수수료+세금")
    dvid_amt: str = Field(default="", description="배당금")
    crnc_code: str = Field(default="", description="통화코드")


class OverseasAccountDailyStockProfitRate(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 일별종목수익률현황 응답")

    result_list: list[OverseasAccountDailyStockProfitRateItem] = Field(default_factory=list, description="결과리스트")


class OverseasAccountMonthlyStockProfitRateItem(BaseModel):
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    frst_base_dt: str = Field(default="", description="최초기준일")
    last_base_dt: str = Field(default="", description="최종기준일")
    pl_amt: str = Field(default="", description="매매수익")
    prft_rt: str = Field(default="", description="수익률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    frst_stk_evlta: str = Field(default="", description="최초주식평가금")
    last_stk_evlta: str = Field(default="", description="최종주식평가금")
    frst_qty: str = Field(default="", description="최초수량")
    last_qty: str = Field(default="", description="최종수량")
    buy_qty: str = Field(default="", description="매수수량. 단위: 1주")
    sell_qty: str = Field(default="", description="매도수량. 단위: 1주")
    buy_amt: str = Field(default="", description="매수금. 단위: 1주")
    sell_amt: str = Field(default="", description="매도금. 단위: 1주")
    frgn_stk_inq_amt: str = Field(default="", description="입고평가금")
    frgn_stk_outq_amt: str = Field(default="", description="출고평가금")
    cmsn_tax: str = Field(default="", description="수수료+세금")
    dvid_amt: str = Field(default="", description="배당금")
    crnc_code: str = Field(default="", description="통화코드")


class OverseasAccountMonthlyStockProfitRate(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 월별종목수익률현황 응답")

    result_list: list[OverseasAccountMonthlyStockProfitRateItem] = Field(default_factory=list, description="결과리스트")


class OverseasAccountYearlyStockProfitRateItem(BaseModel):
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    frst_base_dt: str = Field(default="", description="최초기준일")
    last_base_dt: str = Field(default="", description="최종기준일")
    pl_amt: str = Field(default="", description="매매수익")
    prft_rt: str = Field(default="", description="수익률")
    frst_stk_evlta: str = Field(default="", description="최초주식평가금")
    last_stk_evlta: str = Field(default="", description="최종주식평가금")
    frst_qty: str = Field(default="", description="최초수량")
    last_qty: str = Field(default="", description="최종수량")
    buy_qty: str = Field(default="", description="매수수량. 단위: 1주")
    sell_qty: str = Field(default="", description="매도수량. 단위: 1주")
    buy_amt: str = Field(default="", description="매수금. 단위: 1주")
    sell_amt: str = Field(default="", description="매도금. 단위: 1주")
    frgn_stk_inq_amt: str = Field(default="", description="입고평가금")
    frgn_stk_outq_amt: str = Field(default="", description="출고평가금")
    cmsn_tax: str = Field(default="", description="수수료+세금")
    dvid_amt: str = Field(default="", description="배당금")
    crnc_code: str = Field(default="", description="통화코드")


class OverseasAccountYearlyStockProfitRate(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 연도별종목수익률현황 응답")

    result_list: list[OverseasAccountYearlyStockProfitRateItem] = Field(default_factory=list, description="결과리스트")


class OverseasAccountLedgerUnfilledOrdersItem(BaseModel):
    ord_cntr_tp: str = Field(default="", description="주문종류. 10:원주문,11:정정주문,12:취소주문")
    ord_no: str = Field(default="", description="주문번호")
    orig_ord_no: str = Field(default="", description="원주문번호. 원 주문이 없는 경우 '000000000'으로 출력")
    stex_nm: str = Field(default="", description="거래소명")
    crnc_code: str = Field(default="", description="통화코드. USD")
    stk_cd: str = Field(default="", description="종목코드")
    frgn_stk_nm: str = Field(default="", description="종목명")
    frgn_trde_tp: str = Field(
        default="",
        description="매매구분. 00:지정가,03:시장가,11:Enhanced Limit Order,12:Special Limit Order,30:Limit On Close,33:Market On Close,34:Stop Limit,35:Stop Market,36:VWAP,37:TWAP",
    )
    frgn_trde_nm: str = Field(
        default="",
        description="매매구분명. 00:지정가,03:시장가,11:Enhanced Limit Order,12:Special Limit Order,30:Limit On Close,33:Market On Close,34:Stop Limit,35:Stop Market,36:VWAP,37:TWAP",
    )
    slby_tp: str = Field(default="", description="매도매수구분. 1:매도,2:매수")
    slby_tp_nm: str = Field(default="", description="매도매수구분명. 1:매도,2:매수")
    ord_qty: str = Field(default="", description="주문수량. 단위: 1주, 좌측 0-padding 처리된 12자리 숫자")
    ord_uv: str = Field(default="", description="주문단가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    stop_pric: str = Field(default="", description="STOP가격. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    cntr_qty: str = Field(default="", description="체결수량. 단위: 1주, 좌측 0-padding 처리된 12자리 숫자")
    cntr_uv: str = Field(default="", description="체결단가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    mdfy_qty: str = Field(default="", description="정정수량. 단위: 1주, 좌측 0-padding 처리된 12자리 숫자")
    mdfy_uv: str = Field(default="", description="정정단가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    cncl_qty: str = Field(default="", description="취소수량. 단위: 1주, 좌측 0-padding 처리된 12자리 숫자")
    ord_remnq: str = Field(default="", description="주문잔량. 단위: 1주, 좌측 0-padding 처리된 12자리 숫자")
    ord_time: str = Field(default="", description="주문시간. HH:mm:ss")
    ord_resp_time: str = Field(default="", description="주문응답시간. HH:mm:ss")
    ord_stat: str = Field(default="", description="주문상태명")
    rsrv_tp: str = Field(default="", description="예약주문구분. 0:일반,1:예약")
    natn_nm: str = Field(default="", description="국가명")


class OverseasAccountLedgerUnfilledOrders(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 원장 미체결 응답")

    result_list: list[OverseasAccountLedgerUnfilledOrdersItem] = Field(default_factory=list, description="결과리스트")


class OverseasAccountLedgerBalanceItem(BaseModel):
    stex_nm: str = Field(default="", description="거래소명")
    crnc_code: str = Field(default="", description="통화코드")
    stk_cd: str = Field(default="", description="종목코드")
    frgn_stk_nm: str = Field(default="", description="종목명")
    qty: str = Field(default="", description="결제기준수량")
    poss_qty: str = Field(default="", description="보유수량")
    sell_alowq: str = Field(default="", description="매도가능수량")
    pred_cntr_sellq: str = Field(default="", description="전일매도수량")
    pred_cntr_buyq: str = Field(default="", description="전일매수수량")
    tdy_cntr_sellq: str = Field(default="", description="금일매도수량")
    tdy_cntr_buyq: str = Field(default="", description="금일매수수량")
    frgn_stk_book_uv: str = Field(default="", description="매입단가")
    now_pric: str = Field(default="", description="현재가")
    evlt_amt: str = Field(default="", description="평가금액")
    pl_amt: str = Field(default="", description="손익금액")
    pl_rt: str = Field(default="", description="손익율(%)")
    evlt_amt_krw: str = Field(default="", description="평가금액(원)")
    pl_amt_krw: str = Field(default="", description="손익금액(원)")
    natn_nm: str = Field(default="", description="국가명")
    exch_rate: str = Field(default="", description="환율")
    frgn_stk_book_uv_krw: str = Field(default="", description="매입단가(원)")
    now_pric_krw: str = Field(default="", description="현재가(원)")
    frgn_stk_book_amt: str = Field(default="", description="매입금액")
    frgn_stk_book_amt_krw: str = Field(default="", description="매입금액(원)")


class OverseasAccountLedgerBalance(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 원장잔고확인 응답")

    crnc_code: str = Field(default="", description="통화코드. USD")
    tot_evlt_amt: str = Field(default="", description="총평가금액")
    tot_prch_amt: str = Field(default="", description="총매입금액")
    tot_pl_amt: str = Field(default="", description="총손익금액")
    tot_pl_rt: str = Field(default="", description="총수익율")
    tdy_book_amt: str = Field(default="", description="당일실현손익매입금액")
    tdy_pl_amt: str = Field(default="", description="당일실현손익")
    tdy_pl_rt: str = Field(default="", description="당일실현손익율(%)")
    tot_evlt_amt_krw: str = Field(default="", description="총평가금액(원)")
    tot_prch_amt_krw: str = Field(default="", description="총매입금액(원)")
    tot_pl_amt_krw: str = Field(default="", description="총손익금액(원)")
    tdy_book_amt_krw: str = Field(default="", description="당일실현손익매입금액(원)")
    tdy_pl_amt_krw: str = Field(default="", description="당일실현손익(원)")
    result_list: list[OverseasAccountLedgerBalanceItem] = Field(default_factory=list, description="결과리스트")


class OverseasAccountTransactionHistoryItem(BaseModel):
    deal_dt: str = Field(default="", description="거래일자")
    deal_kind_nm: str = Field(default="", description="거래종류명")
    rmrk_nm: str = Field(default="", description="적요명")
    deal_amt: str = Field(default="", description="거래금액")
    tax_tot_amt: str = Field(default="", description="소득/주민세. 기존:세금합")
    exct_amt: str = Field(default="", description="정산금액")
    uncl_ocr: str = Field(default="", description="미수(원/주)")
    fc_uncl_ocr: str = Field(default="", description="미수(외)")
    entra_remn: str = Field(default="", description="예수금잔고")
    deal_no: str = Field(default="", description="거래번호")
    stk_nm: str = Field(default="", description="종목명")
    deal_qty: str = Field(default="", description="거래수량")
    fc_deal_tax: str = Field(default="", description="거래세(외)")
    frgn_pay_txam: str = Field(default="", description="외국납부세액(외)")
    rpym_sum: str = Field(default="", description="변제합")
    fc_rpym_sum: str = Field(default="", description="변제합(외)")
    fc_entra: str = Field(default="", description="외화예수금잔고")
    mdia_nm: str = Field(default="", description="메체구분명")
    orig_deal_no: str = Field(default="", description="원거래번호")
    stk_cd: str = Field(default="", description="종목코드")
    uv_exrt: str = Field(default="", description="거래단가/환율")
    fc_cmsn: str = Field(default="", description="수수료(외)")
    fc_exct_amt: str = Field(default="", description="정산금액(외)")
    dly_sum: str = Field(default="", description="연체합")
    fc_dly_sum: str = Field(default="", description="연체합(외)")
    vlbl_nowrm: str = Field(default="", description="유가금잔")
    stex_nm: str = Field(default="", description="거래소구분명")
    fc_deal_amt: str = Field(default="", description="거래금액(외)")
    proc_time: str = Field(default="", description="처리시간")
    crnc_code: str = Field(default="", description="통화코드")


class OverseasAccountTransactionHistory(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 거래내역 응답")

    acnt_print: str = Field(default="", description="계좌번호. 계좌번호 출력용")
    sell_sum: str = Field(default="", description="매도합계")
    buy_sum: str = Field(default="", description="매수합계")
    result_list: list[OverseasAccountTransactionHistoryItem] = Field(default_factory=list, description="결과리스트")


class OverseasAccountDepositItem(BaseModel):
    crnc_code: str = Field(default="", description="통화코드")
    crnc_nm: str = Field(default="", description="통화명")
    fc_entra: str = Field(default="", description="외화예수금")
    fc_pymn_alowa: str = Field(default="", description="외화출금가능금액")
    futr_repl_profa: str = Field(default="", description="선물대용증거금")
    fc_booka: str = Field(default="", description="외화장부금액")
    fc_ord_alowa: str = Field(default="", description="외화주문가능금액")
    futr_profa_booka: str = Field(default="", description="선물증거금장부금액")
    fc_ch_uncla: str = Field(default="", description="외화현금미수금")
    fc_etc_loana: str = Field(default="", description="외화기타대여금")


class OverseasAccountDeposit(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="해외주식 예수금 응답")

    krw_entra: str = Field(default="", description="원화예수금")
    ch_uncla: str = Field(default="", description="현금미수금")
    etc_loana: str = Field(default="", description="기타대여금")
    result_list: list[OverseasAccountDepositItem] = Field(default_factory=list, description="결과리스트")


class OverseasAccountKrwWithdrawableAmount(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="원화출금가능 금액 조회(원화대용 포함) 응답")

    rgst_abnd_tp: str = Field(
        default="", description="원화대용등록해지구분. 원화대용약정등록상태 1:신청,2:해지 또는 미신청"
    )
    krw_pymn_alow_amt: str = Field(default="", description="원화출금가능금액. 원화대용포함한 원화출금가능금액")
    krw_repl_abnd_amt: str = Field(default="", description="원화대용해지가능금액")


class OverseasAccountDepositAndSecuritiesValuationByCurrencyItem(BaseModel):
    crnc_code: str = Field(default="", description="통화코드")
    fx_entr: str = Field(default="", description="외화예수금. 소수점 및 소수점 이하2자리 포함")
    evlt_amt: str = Field(default="", description="해외증권평가금. 소수점 및 소수점 이하2자리 포함")
    crnc_rt: str = Field(default="", description="기준환율. 소수점 및 소수점 이하2자리 포함")
    chg_entr: str = Field(default="", description="환전예수금. 단위: 원, 좌측 0-padding 처리된 12자리 숫자")
    chg_evlt_amt: str = Field(default="", description="환전평가금. 단위: 원, 좌측 0-padding 처리된 12자리 숫자")
    evlt_amt_wght: str = Field(default="", description="평가금액비중. 소수점 둘째 자리까지 포맷된 숫자")


class OverseasAccountDepositAndSecuritiesValuationByCurrency(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="통화별 예수금 및 증권 평가금현황 응답")

    won_entr: str = Field(default="", description="예수금. 단위: 원, 좌측 0-padding 처리된 12자리 숫자")
    aset_evlt_amt: str = Field(default="", description="원화추정자산. 단위: 원, 좌측 0-padding 처리된 12자리 숫자")
    result_list: list[OverseasAccountDepositAndSecuritiesValuationByCurrencyItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasAccountLedgerValuationAmountItem(BaseModel):
    natn_nm: str = Field(default="", description="국가명")
    stex_nm: str = Field(default="", description="거래소코드명")
    crnc_code: str = Field(default="", description="통화코드")
    crnc_nm: str = Field(default="", description="통화코드명")
    evlt_amt: str = Field(default="", description="평가금액")
    chg_evlt_amt: str = Field(
        default="", description="환전평가금액. 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자"
    )
    pl_rt: str = Field(default="", description="평가수익율(%). 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    pl_amt: str = Field(default="", description="평가손익")
    chg_profit_amt: str = Field(
        default="", description="환전평가손익. 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자"
    )
    evlt_amt_wght: str = Field(default="", description="평가금액비중. 소수점 둘째 자리까지 포맷된 숫자")


class OverseasAccountLedgerValuationAmount(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="해외증권 원장 평가금액현황 응답")

    result_list: list[OverseasAccountLedgerValuationAmountItem] = Field(default_factory=list, description="결과리스트")


class OverseasAccountValuationAmountByDateItem(BaseModel):
    natn_nm: str = Field(default="", description="국가명")
    stex_nm: str = Field(default="", description="거래소코드명")
    crnc_code: str = Field(default="", description="통화코드")
    crnc_nm: str = Field(default="", description="통화코드명")
    evlt_amt: str = Field(default="", description="평가금액. 단위: USD, 소수점 둘째 자리까지 포맷된 숫자")
    chg_evlt_amt: str = Field(
        default="", description="환전평가금액. 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자"
    )
    pl_rt: str = Field(default="", description="평가수익율(%). 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    pl_amt: str = Field(default="", description="평가손익. 단위: USD, 소수점 둘째 자리까지 포맷된 숫자")
    chg_profit_amt: str = Field(
        default="", description="환전평가손익. 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자"
    )
    evlt_amt_wght: str = Field(default="", description="평가금액비중. 소수점 둘째 자리까지 포맷된 숫자")


class OverseasAccountValuationAmountByDate(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="해외증권 특정일 평가금액 응답")

    result_list: list[OverseasAccountValuationAmountByDateItem] = Field(default_factory=list, description="결과리스트")


class OverseasAccountDepositAndSecuritiesValuationByCurrencyByDateItem(BaseModel):
    crnc_code: str = Field(default="", description="통화코드")
    fx_entr: str = Field(default="", description="외화예수금. 소수점 및 소수점 이하2자리 포함")
    evlt_amt: str = Field(default="", description="해외증권평가금. 소수점 및 소수점 이하2자리 포함")
    crnc_rt: str = Field(default="", description="기준환율. 소수점 및 소수점 이하2자리 포함")
    chg_entr: str = Field(default="", description="환전예수금. 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자")
    chg_evlt_amt: str = Field(
        default="", description="환전평가금. 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자"
    )
    evlt_amt_wght: str = Field(default="", description="평가금액비중. 소수점 둘째 자리까지 포맷된 숫자")


class OverseasAccountDepositAndSecuritiesValuationByCurrencyByDate(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="특정일 통화별 예수금 및 증권 평가금 응답")

    won_entr: str = Field(default="", description="예수금. 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자")
    tot_evlt_amt: str = Field(
        default="", description="총평가금액. 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자"
    )
    book_amt: str = Field(default="", description="총매입금액. 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자")
    tot_pl: str = Field(default="", description="총손익금액. 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자")
    tot_pl_rt: str = Field(default="", description="총수익률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    aset_evlt_amt: str = Field(
        default="", description="원화추정자산. 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자"
    )
    result_list: list[OverseasAccountDepositAndSecuritiesValuationByCurrencyByDateItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasAccountDailyOrderExecutionHistoryItem(BaseModel):
    ord_no: str = Field(default="", description="주문번호")
    crnc_code: str = Field(default="", description="통화코드")
    stk_cd: str = Field(default="", description="종목코드")
    isin_code: str = Field(default="", description="국제표준코드")
    frgn_trde_tp: str = Field(default="", description="매매구분")
    ord_qty: str = Field(default="", description="주문수량. 단위: 1주, 좌측 0-padding 처리된 12자리 숫자")
    cntr_qty: str = Field(default="", description="체결수량. 단위: 1주, 좌측 0-padding 처리된 12자리 숫자")
    mdfy_qty: str = Field(default="", description="정정수량. 단위: 1주, 좌측 0-padding 처리된 12자리 숫자")
    cncl_qty: str = Field(default="", description="취소수량. 단위: 1주, 좌측 0-padding 처리된 12자리 숫자")
    frgn_msg_code: str = Field(default="", description="해외메세지코드")
    rsrv_tp: str = Field(default="", description="예약구분")
    oppo_trde_tp_nm: str = Field(default="", description="반대매매구분명")
    comm_ord_tp_nm: str = Field(default="", description="통신주문구분명")
    ord_time: str = Field(default="", description="주문시간. HH:mm:ss")
    crnc_nm: str = Field(default="", description="통화코드명")
    stex_nm: str = Field(default="", description="거래소코드명")
    frgn_stk_nm: str = Field(default="", description="종목명")
    slby_tp_nm: str = Field(default="", description="매도매수구분명")
    ord_uv: str = Field(default="", description="주문단가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    stop_pric: str = Field(default="", description="STOP가격. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    cntr_uv: str = Field(default="", description="체결단가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    mdfy_uv: str = Field(default="", description="정정단가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    ord_remnq: str = Field(default="", description="주문잔량. 단위: 1주, 좌측 0-padding 처리된 12자리 숫자")
    ord_stat_nm: str = Field(default="", description="주문상태명")
    text1: str = Field(default="", description="거부사유")
    inpt_chnl_tp: str = Field(default="", description="입력매체구분명")
    ord_resp_time: str = Field(default="", description="주문응답수신시간. HH:mm:ss")
    cntr_time: str = Field(default="", description="체결시간")


class OverseasAccountDailyOrderExecutionHistory(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 일별 주문체결내역 응답")

    result_list: list[OverseasAccountDailyOrderExecutionHistoryItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasAccountDepositDetail(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 예수금 상세 응답")

    won_entr: str = Field(default="", description="원화 예수금. 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자")
    won_dfr_amt: str = Field(default="", description="미수금. 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자")
    won_etc_loana: str = Field(
        default="", description="기타 대여금. 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자"
    )
    krw_ord_set_amt: str = Field(
        default="", description="해외원화주문설정금. 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자"
    )
    usd_exch_rate: str = Field(default="", description="매도환율(USD). 세자릿수 콤마, 소수점 둘째 자리까지 포맷된 숫자")
    d0_setl_dt: str = Field(default="", description="D0 국내결제일자. YYYYMMDD")
    d0_won_conv_alow_ch: str = Field(
        default="", description="D0 원화환산추정인출가능금. 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자"
    )
    d0_usd_fx_entr: str = Field(default="", description="D0 외화예수금(USD)")
    d1_setl_dt: str = Field(default="", description="D1 국내결제일자")
    d1_won_conv_alow_ch: str = Field(default="", description="D1 원화환산추정인출가능금")
    d1_usd_fx_entr: str = Field(default="", description="D1 외화예수금(USD)")
    d1_usd_exct_amt: str = Field(default="", description="D1 해외정산금(USD)")
    d1_usd_buy_excta: str = Field(default="", description="D1 해외매수정산금(USD)")
    d1_usd_sell_excta: str = Field(default="", description="D1 해외매도정산금(USD)")
    d2_setl_dt: str = Field(default="", description="D2 국내결제일자. YYYYMMDD")
    d2_won_conv_alow_ch: str = Field(
        default="", description="D2 원화환산추정인출가능금. 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자"
    )
    d2_usd_fx_entr: str = Field(default="", description="D2 외화예수금(USD)")
    d2_usd_exct_amt: str = Field(default="", description="D2 해외정산금(USD)")
    d2_usd_buy_excta: str = Field(default="", description="D2 해외매수정산금(USD)")
    d2_usd_sell_excta: str = Field(default="", description="D2 해외매도정산금(USD)")
    d3_setl_dt: str = Field(default="", description="D3 국내결제일자. YYYYMMDD")
    d3_won_conv_alow_ch: str = Field(
        default="", description="D3 원화환산추정인출가능금. 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자"
    )
    d3_usd_fx_entr: str = Field(default="", description="D3 외화예수금(USD)")
    d3_usd_exct_amt: str = Field(default="", description="D3 해외정산금(USD)")
    d3_usd_buy_excta: str = Field(default="", description="D3 해외매수정산금(USD)")
    d3_usd_sell_excta: str = Field(default="", description="D3 해외매도정산금(USD)")
    d4_setl_dt: str = Field(default="", description="D4 국내결제일자. YYYYMMDD")
    d4_won_conv_alow_ch: str = Field(
        default="", description="D4 원화환산추정인출가능금. 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자"
    )
    d4_usd_fx_entr: str = Field(default="", description="D4 외화예수금(USD)")
    d4_usd_exct_amt: str = Field(default="", description="D4 해외정산금(USD)")
    d4_usd_buy_excta: str = Field(default="", description="D4 해외매수정산금(USD)")
    d4_usd_sell_excta: str = Field(default="", description="D4 해외매도정산금(USD)")


class OverseasAccountTodayRealizedProfitLossByStockItem(BaseModel):
    stex_nm: str = Field(default="", description="거래소명")
    crnc_code: str = Field(default="", description="통화코드")
    stk_cd: str = Field(default="", description="종목코드")
    frgn_stk_nm: str = Field(default="", description="종목명")
    tdy_pl_amt: str = Field(default="", description="당일실현손익금액. 소수점 넷째 자리까지 포맷된 숫자")
    evlt_pl_amt: str = Field(default="", description="평가손익금액. 소수점 넷째 자리까지 포맷된 숫자")
    evlt_pl_rt: str = Field(
        default="", description="평가수익율(%). 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율"
    )
    prch_uv: str = Field(default="", description="매입단가. 소수점 넷째 자리까지 포맷된 숫자")
    poss_qty: str = Field(default="", description="보유수량. 단위: 1주, 좌측 0-padding 처리된 12자리 숫자")
    sell_alowq: str = Field(default="", description="매도가능수량. 단위: 1주, 좌측 0-padding 처리된 12자리 숫자")
    now_pric: str = Field(default="", description="현재가. 소수점 넷째 자리까지 포맷된 숫자")
    prch_amt: str = Field(default="", description="매입금액. 소수점 넷째 자리까지 포맷된 숫자")
    evlt_amt: str = Field(default="", description="평가금액. 소수점 넷째 자리까지 포맷된 숫자")
    prch_exrt: str = Field(default="", description="매입환율. 소수점 둘째 자리까지 포맷된 숫자")
    sell_exrt: str = Field(default="", description="매도환율. 소수점 둘째 자리까지 포맷된 숫자")
    krw_chg_dfrn_pl_amt: str = Field(
        default="", description="환차손익(원). 단위: 원, 좌측 0-padding 처리된 15자리 숫자"
    )
    krw_chg_pl_amt: str = Field(default="", description="환실현손익(원). 단위: 원, 좌측 0-padding 처리된 15자리 숫자")
    evlt_amt_cmsn: str = Field(default="", description="평가금액수수료. 소수점 넷째 자리까지 포맷된 숫자")
    evlt_amt_tax: str = Field(default="", description="평가금액세금. 소수점 넷째 자리까지 포맷된 숫자")
    natn_nm: str = Field(default="", description="국가명")


class OverseasAccountTodayRealizedProfitLossByStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 당일 종목별 실현손익 응답")

    crnc_code: str = Field(default="", description="통화코드. 거래소전체 KRW")
    tot_evlt_amt: str = Field(default="", description="총평가금액. 소수점 넷째 자리까지 포맷된 숫자")
    tot_prch_amt: str = Field(default="", description="총매입금액. 소수점 넷째 자리까지 포맷된 숫자")
    tot_pl_amt: str = Field(default="", description="총손익금액. 소수점 넷째 자리까지 포맷된 숫자")
    tot_pl_rt: str = Field(default="", description="총수익율. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    tdy_pl_amt: str = Field(default="", description="당일실현손익. 소수점 넷째 자리까지 포맷된 숫자")
    prsm_aseta_krw: str = Field(default="", description="추정자산(원). 단위: 원, 좌측 0-padding 처리된 15자리 숫자")
    result_list: list[OverseasAccountTodayRealizedProfitLossByStockItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasAccountOrderHistoryByPeriodItem(BaseModel):
    ord_dt: str = Field(default="", description="주문일. YYYYMMDD")
    ord_no: str = Field(default="", description="주문번호")
    crnc_code: str = Field(default="", description="해당통화코드")
    stk_cd: str = Field(default="", description="종목코드")
    trde_tp: str = Field(default="", description="매매구분")
    ord_qty: str = Field(default="", description="주문수량. 단위: 1주, 좌측 0-padding 처리된 12자리 숫자")
    cntr_qty: str = Field(default="", description="체결수량. 단위: 1주, 좌측 0-padding 처리된 12자리 숫자")
    mdfy_qty: str = Field(default="", description="정정수량. 단위: 1주, 좌측 0-padding 처리된 12자리 숫자")
    cncl_qty: str = Field(default="", description="취소수량. 단위: 1주, 좌측 0-padding 처리된 12자리 숫자")
    rsrv_tp: str = Field(default="", description="예약구분")
    oppo_trde_tp_nm: str = Field(default="", description="반대매매구분명")
    inpt_chnl_tp_nm: str = Field(default="", description="입력매체명")
    ord_time: str = Field(default="", description="주문시간. HH:mm:ss")
    crnc_nm: str = Field(default="", description="통화명")
    stex_nm: str = Field(default="", description="거래소명")
    stk_nm: str = Field(default="", description="종목명")
    slby_tp_nm: str = Field(default="", description="매도매수구분명")
    ord_uv: str = Field(default="", description="주문단가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    stop_pric: str = Field(default="", description="STOP가격. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    cntr_uv: str = Field(default="", description="체결단가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    mdfy_uv: str = Field(default="", description="정정단가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    ord_remnq: str = Field(default="", description="주문잔량. 단위: 1주, 좌측 0-padding 처리된 12자리 숫자")
    cntr_amt: str = Field(default="", description="체결금액")
    comm_ord_tp_nm: str = Field(default="", description="통신주문구분명")


class OverseasAccountOrderHistoryByPeriod(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 기간별 주문내역 응답")

    result_list: list[OverseasAccountOrderHistoryByPeriodItem] = Field(default_factory=list, description="결과리스트")


class OverseasAccountTodayOrderExecutionItem(BaseModel):
    ord_no: str = Field(default="", description="주문번호")
    orig_ord_no: str = Field(default="", description="원주문번호")
    stex_nm: str = Field(default="", description="거래소명")
    crnc_code: str = Field(default="", description="통화코드")
    stk_cd: str = Field(default="", description="종목코드")
    frgn_stk_nm: str = Field(default="", description="종목명")
    frgn_trde_tp: str = Field(
        default="",
        description="매매구분. 00:지정가,03:시장가,11:Enhanced Limit Order,12:Special Limit Order,30:Limit On Close,33:Market On Close,34:Stop Limit,35:Stop Market,36:VWAP,37:TWAP",
    )
    frgn_trde_nm: str = Field(default="", description="매매구분명")
    slby_tp: str = Field(default="", description="매도매수구분. 1:매도,2:매수")
    slby_tp_nm: str = Field(default="", description="매도매수구분명")
    ord_qty: str = Field(default="", description="주문수량. 단위: 1주, 좌측 0-padding 처리된 12자리 숫자")
    ord_uv: str = Field(default="", description="주문단가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    stop_pric: str = Field(default="", description="STOP가격. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    cntr_qty: str = Field(default="", description="체결수량. 단위: 1주, 좌측 0-padding 처리된 12자리 숫자")
    cntr_uv: str = Field(default="", description="체결단가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    cnfm_qty: str = Field(default="", description="확인수량. 단위: 1주, 좌측 0-padding 처리된 12자리 숫자")
    ord_remnq: str = Field(default="", description="주문잔량. 단위: 1주, 좌측 0-padding 처리된 12자리 숫자")
    ord_time: str = Field(default="", description="주문시간. HH:mm:ss")
    ord_resp_time: str = Field(default="", description="주문응답시간. HH:mm:ss")
    ord_stat: str = Field(default="", description="주문상태명")
    rsrv_tp: str = Field(default="", description="예약주문구분. 0:일반, 1:예약")
    natn_nm: str = Field(default="", description="국가명")
    cntr_time: str = Field(default="", description="체결시간")


class OverseasAccountTodayOrderExecution(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 당일 주문체결 확인 응답")

    result_list: list[OverseasAccountTodayOrderExecutionItem] = Field(
        default_factory=list, description="조회결과리스트"
    )


class OverseasAccountRealizedProfitLossItem(BaseModel):
    sell_dt: str = Field(default="", description="매도일자")
    stk_cd: str = Field(default="", description="종목코드")
    frgn_stk_nm: str = Field(default="", description="종목명")
    sell_qty: str = Field(default="", description="청산수량")
    avg_buy_uv: str = Field(default="", description="매입평균가")
    buy_amt: str = Field(default="", description="매입금액")
    avg_sell_uv: str = Field(default="", description="매도평균가")
    sell_amt: str = Field(default="", description="매도금액")
    cmsn_tax: str = Field(default="", description="수수료제세금")
    pl_amt: str = Field(default="", description="손익금액")
    pl_rt: str = Field(default="", description="실현수익률(%)")
    prch_exrt: str = Field(default="", description="매입환율")
    sell_exrt: str = Field(default="", description="매도환율")
    krw_chg_dfrn_pl_amt: str = Field(default="", description="환차손익(원)")
    krw_chg_pl_amt: str = Field(default="", description="환실현손익(원)")
    comm_ord_tp: str = Field(default="", description="매체구분")
    stex_nm: str = Field(default="", description="거래소명")
    natn_nm: str = Field(default="", description="국가명")


class OverseasAccountRealizedProfitLoss(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 실현손익 응답")

    tot_sell_amt: str = Field(default="", description="총매도금액")
    tot_buy_amt: str = Field(default="", description="총매수금액")
    tot_cmsn_tax: str = Field(default="", description="총수수료제세금")
    tot_exct_amt: str = Field(default="", description="총정산금액")
    tot_pl_amt: str = Field(default="", description="총손익금액")
    tot_pl_rt: str = Field(default="", description="총실현수익률(%)")
    result_list: list[OverseasAccountRealizedProfitLossItem] = Field(default_factory=list, description="결과리스트")


class OverseasAccountTodayTradingItem(BaseModel):
    stex_nm: str = Field(default="", description="거래소코드명")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    tdy_avg_buy_uv: str = Field(default="", description="금일매수평균가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    tdy_buyq: str = Field(
        default="", description="금일매수수량. 단위: 1주, 좌측 0-padding 처리된 부호 포함 15자리 숫자"
    )
    tdy_buy_amt: str = Field(default="", description="금일매입금액. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    tdy_avg_sell_uv: str = Field(default="", description="금일매도평균가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    tdy_sellq: str = Field(
        default="", description="금일매도수량. 단위: 1주, 좌측 0-padding 처리된 부호 포함 15자리 숫자"
    )
    tdy_sell_amt: str = Field(default="", description="금일매도금액. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    cmsn_altx: str = Field(default="", description="수수료제세금. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    pl_amt: str = Field(default="", description="실현손익. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    pl_rt: str = Field(default="", description="실현손익률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    bf_prch_uv: str = Field(default="", description="이전매입가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    exch_rate: str = Field(default="", description="기준환율. 소수점 둘째 자리까지 포맷된 숫자")


class OverseasAccountTodayTrading(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 당일매매 응답")

    tot_sell_amt: str = Field(default="", description="총매도금액. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    tot_buy_amt: str = Field(default="", description="총매수금액. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    tot_cmsn_altx: str = Field(default="", description="총수수료제세금. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    tot_exct_amt: str = Field(default="", description="총정산금액. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    tot_pl_amt: str = Field(default="", description="총실현손익. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    tot_pl_rt: str = Field(
        default="", description="총실현손익률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율"
    )
    exch_rate: str = Field(default="", description="기준환율. 소수점 둘째 자리까지 포맷된 숫자")
    result_list: list[OverseasAccountTodayTradingItem] = Field(default_factory=list, description="결과리스트")


class OverseasAccountTodayTradingSummaryItem(BaseModel):
    stex_nm: str = Field(default="", description="거래소코드명")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    slby_tp_nm: str = Field(default="", description="매도수구분명. 매수인경우'+',매도인경우'-'")
    crnc_code: str = Field(default="", description="통화코드")
    cntr_uv: str = Field(default="", description="체결단가")
    cntr_qty: str = Field(default="", description="체결수량")
    engg_amt: str = Field(default="", description="약정금액")
    cmsn: str = Field(default="", description="수수료")
    altx: str = Field(default="", description="제세금")
    exct_amt: str = Field(default="", description="정산금액")
    exch_rate: str = Field(default="", description="환율")
    natn_nm: str = Field(default="", description="국가명")


class OverseasAccountTodayTradingSummary(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 당일매매정리 응답")

    result_list: list[OverseasAccountTodayTradingSummaryItem] = Field(default_factory=list, description="결과리스트")


class OverseasAccountTodayRealizedProfitLossItem(BaseModel):
    stex_nm: str = Field(default="", description="거래소코드명")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    crnc_code: str = Field(default="", description="통화코드")
    cntr_sellq: str = Field(default="", description="체결매도수량")
    avg_buy_uv: str = Field(default="", description="매입평균가")
    cntr_sella: str = Field(default="", description="체결매도가")
    tdy_pl_amt: str = Field(default="", description="당일실현손익")
    pl_rt: str = Field(default="", description="실현수익률")
    cmsn: str = Field(default="", description="수수료")
    altx: str = Field(default="", description="제세금")
    exch_rate: str = Field(default="", description="환율")
    natn_nm: str = Field(default="", description="국가명")


class OverseasAccountTodayRealizedProfitLoss(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 당일 실현손익 응답")

    tot_tdy_pl_amt: str = Field(default="", description="총당일실현손익")
    tot_tdy_pl_amt_krw: str = Field(default="", description="총당일실현손익(원)")
    result_list: list[OverseasAccountTodayRealizedProfitLossItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasAccountDailyRealizedProfitLossByStockItem(BaseModel):
    stex_nm: str = Field(default="", description="거래소코드명")
    stk_nm: str = Field(default="", description="종목명")
    crnc_code: str = Field(default="", description="통화코드")
    cntr_sellq: str = Field(default="", description="체결매도수량")
    avg_buy_uv: str = Field(default="", description="매입평균가")
    cntr_sella: str = Field(default="", description="체결매도가")
    pl_amt: str = Field(default="", description="실현손익")
    pl_rt: str = Field(default="", description="실현수익률")
    stk_cd: str = Field(default="", description="종목코드")
    cmsn: str = Field(default="", description="수수료")
    altx: str = Field(default="", description="제세금")
    exch_rate: str = Field(default="", description="환율")
    natn_nm: str = Field(default="", description="국가명")


class OverseasAccountDailyRealizedProfitLossByStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 일별 종목별 실현손익 응답")

    tot_pl_amt: str = Field(default="", description="총실현손익")
    tot_pl_amt_krw: str = Field(default="", description="총실현손익(원)")
    result_list: list[OverseasAccountDailyRealizedProfitLossByStockItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasAccountProfitRateByPeriod(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 기간별 수익률 현황 응답")

    fr_entr: str = Field(default="", description="기간초예수금. 단위: 원, 좌측 0-padding 처리된 12자리 숫자")
    fr_dfr_amt: str = Field(default="", description="기간초현금미수금. 단위: 원, 좌측 0-padding 처리된 12자리 숫자")
    fr_etc_loana: str = Field(default="", description="기간초기타대여금. 단위: 원, 좌측 0-padding 처리된 12자리 숫자")
    fr_fc_entr: str = Field(default="", description="기간초외화예수금. 단위: 원, 좌측 0-padding 처리된 12자리 숫자")
    fr_fc_dfr_amt: str = Field(default="", description="기간초외화미수금. 단위: 원, 좌측 0-padding 처리된 12자리 숫자")
    fr_fc_etc_loana: str = Field(
        default="", description="기간초외화기타대여금. 단위: 원, 좌측 0-padding 처리된 12자리 숫자"
    )
    fr_frgn_stk_evltv: str = Field(
        default="", description="기간초해외증권평가금. 단위: 원, 좌측 0-padding 처리된 12자리 숫자"
    )
    fr_tot_evltv: str = Field(default="", description="기간초순자산액계. 단위: 원, 좌측 0-padding 처리된 12자리 숫자")
    to_entr: str = Field(default="", description="기간말예수금. 단위: 원, 좌측 0-padding 처리된 12자리 숫자")
    to_dfr_amt: str = Field(default="", description="기간말현금미수금. 단위: 원, 좌측 0-padding 처리된 12자리 숫자")
    to_etc_loana: str = Field(default="", description="기간말기타대여금. 단위: 원, 좌측 0-padding 처리된 12자리 숫자")
    to_fc_entr: str = Field(default="", description="기간말외화예수금. 단위: 원, 좌측 0-padding 처리된 12자리 숫자")
    to_fc_dfr_amt: str = Field(default="", description="기간말외화미수금. 단위: 원, 좌측 0-padding 처리된 12자리 숫자")
    to_fc_etc_loana: str = Field(
        default="", description="기간말외화기타대여금. 단위: 원, 좌측 0-padding 처리된 12자리 숫자"
    )
    to_frgn_stk_evltv: str = Field(
        default="", description="기간말해외증권평가금. 단위: 원, 좌측 0-padding 처리된 12자리 숫자"
    )
    to_tot_evltv: str = Field(default="", description="기간말순자산액계. 단위: 원, 좌측 0-padding 처리된 12자리 숫자")
    fc_rcpta: str = Field(default="", description="기간내총외화입금. 단위: 원, 좌측 0-padding 처리된 12자리 숫자")
    fc_payma: str = Field(default="", description="기간내총외화출금. 단위: 원, 좌측 0-padding 처리된 12자리 숫자")
    chg_rcpta: str = Field(default="", description="기간내외화매도. 단위: 원, 좌측 0-padding 처리된 12자리 숫자")
    chg_payma: str = Field(default="", description="기간내외화매수. 단위: 원, 좌측 0-padding 처리된 12자리 숫자")
    frgn_stk_inqa: str = Field(
        default="", description="기간내해외증권입고. 단위: 원, 좌측 0-padding 처리된 12자리 숫자"
    )
    frgn_stk_outqa: str = Field(
        default="", description="기간내해외증권출고. 단위: 원, 좌측 0-padding 처리된 12자리 숫자"
    )
    invt_bsamt: str = Field(default="", description="투자원금평잔. 단위: 원, 좌측 0-padding 처리된 12자리 숫자")
    evlt_profit: str = Field(default="", description="평가손익. 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자")
    profit_rate: str = Field(default="", description="수익율. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    io_bsamt: str = Field(default="", description="기간내총입출금고평잔. 단위: 원, 좌측 0-padding 처리된 12자리 숫자")
    tern_rt: str = Field(default="", description="회전율. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")


class OverseasAccountDailyRealizedProfitLossItem(BaseModel):
    trde_dt: str = Field(default="", description="매매일자")
    buy_amt: str = Field(default="", description="매수금액")
    sell_amt: str = Field(default="", description="매도금액")
    pl_amt: str = Field(default="", description="실현손익금액")
    cmsn: str = Field(default="", description="수수료")
    tax: str = Field(default="", description="세금")


class OverseasAccountDailyRealizedProfitLoss(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 일별 실현손익 응답")

    tot_buy_amt: str = Field(default="", description="총매수금액")
    tot_sell_amt: str = Field(default="", description="총매도금액")
    tot_pl_amt: str = Field(default="", description="총실현손익금액")
    tot_cmsn: str = Field(default="", description="수수료합")
    tot_tax: str = Field(default="", description="세금합")
    result_list: list[OverseasAccountDailyRealizedProfitLossItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasAccountMonthlyRealizedProfitLossItem(BaseModel):
    trde_dt: str = Field(default="", description="매매일자")
    buy_amt: str = Field(default="", description="매수금액")
    sell_amt: str = Field(default="", description="매도금액")
    pl_amt: str = Field(default="", description="실현손익금액")
    cmsn: str = Field(default="", description="수수료")
    tax: str = Field(default="", description="세금")


class OverseasAccountMonthlyRealizedProfitLoss(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 월별 실현손익 응답")

    tot_buy_amt: str = Field(default="", description="총매수금액")
    tot_sell_amt: str = Field(default="", description="총매도금액")
    tot_pl_amt: str = Field(default="", description="총실현손익금액")
    tot_cmsn: str = Field(default="", description="수수료합")
    tot_tax: str = Field(default="", description="세금합")
    result_list: list[OverseasAccountMonthlyRealizedProfitLossItem] = Field(
        default_factory=list, description="결과리스트"
    )
