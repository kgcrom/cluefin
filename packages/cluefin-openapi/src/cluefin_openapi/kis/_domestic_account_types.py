from __future__ import annotations

from typing import Dict, Mapping, Optional, Sequence

from pydantic import BaseModel, Field

from cluefin_openapi.kis._model import KisHttpBody


class StockQuoteCurrentItem(BaseModel):
    krx_fwdg_ord_orgno: str = Field(alias="KRX_FWDG_ORD_ORGNO", description="거래소코드", max_length=5)
    odno: str = Field(alias="ODNO", description="주문번호", max_length=10)
    ord_tmd: str = Field(alias="ORD_TMD", description="주문시간", max_length=6)


class StockQuoteCurrent(BaseModel, KisHttpBody):
    """주식주문(현금) 응답"""

    output: Sequence[StockQuoteCurrentItem] = Field(default_factory=list)


class StockQuoteCreditItem(BaseModel):
    krx_fwdg_ord_orgno: str = Field(alias="KRX_FWDG_ORD_ORGNO", description="거래소코드", max_length=5)
    odno: str = Field(alias="ODNO", description="주문번호", max_length=10)
    ord_tmd: str = Field(alias="ORD_TMD", description="주문시간", max_length=6)


class StockQuoteCredit(BaseModel, KisHttpBody):
    """주식주문(신용) 응답"""

    output: Sequence[StockQuoteCreditItem] = Field(default_factory=list)


class StockQuoteCorrectionItem(BaseModel):
    krx_fwdg_ord_orgno: str = Field(alias="KRX_FWDG_ORD_ORGNO", description="거래소코드", max_length=5)
    odno: str = Field(alias="ODNO", description="주문번호", max_length=10)
    ord_tmd: str = Field(alias="ORD_TMD", description="주문시간", max_length=6)


class StockQuoteCorrection(BaseModel, KisHttpBody):
    """주식정정/취소 응답"""

    output: Sequence[StockQuoteCorrectionItem] = Field(default_factory=list)


class StockQuoteCorrectionCancellableQtyItem(BaseModel):
    ord_gno_brno: str = Field(
        title="주문채번지점번호", description="주문시 한국투자증권 시스템에서 지정된 영업점코드", max_length=5
    )
    odno: str = Field(title="주문번호", description="주문시 한국투자증권 시스템에서 채번된 주문번호", max_length=10)
    orgn_odno: str = Field(title="원주문번호", description="정정/취소주문 인경우 원주문번호", max_length=6)
    ord_dvsn_name: str = Field(title="주문구분명", max_length=5)
    pdno: str = Field(title="상품번호", description="종목번호(뒤 6자리만 해당)", max_length=10)
    prdt_name: str = Field(title="상품명", description="종목명", max_length=6)
    rvse_cncl_dvsn_name: str = Field(title="정정취소구분명", description="정정 또는 취소 여부 표시", max_length=5)
    ord_qty: str = Field(title="주문수량", max_length=10)
    ord_unpr: str = Field(title="주문단가", description="1주당 주문가격", max_length=6)
    ord_tmd: str = Field(title="주문시각", description="주문시각(시분초HHMMSS)", max_length=5)
    tot_ccld_qty: str = Field(title="총체결수량", description="주문 수량 중 체결된 수량", max_length=10)
    tot_ccld_amt: str = Field(title="총체결금액", description="주문금액 중 체결금액", max_length=6)
    psbl_qty: str = Field(title="가능수량", description="정정/취소 주문 가능 수량", max_length=5)
    sll_buy_dvsn_cd: str = Field(title="매도매수구분코드", description="01 : 매도 / 02 : 매수", max_length=10)
    ord_dvsn_cd: str = Field(title="주문구분코드", max_length=6)
    mgco_aptm_odno: str = Field(title="운용사지정주문번호", max_length=5)
    excg_dvsn_cd: str = Field(title="거래소구분코드", max_length=2)
    excg_id_dvsn_cd: str = Field(title="거래소ID구분코드", max_length=3)
    excg_id_dvsn_name: str = Field(title="거래소ID구분명", max_length=100)
    stpm_cndt_pric: str = Field(title="스톱지정가조건가격", max_length=9)
    stpm_efct_occr_yn: str = Field(title="스톱지정가효력발생여부", description="Y 또는 N", max_length=1)


class StockQuoteCorrectionCancellableQty(BaseModel, KisHttpBody):
    """주식정정/취소 가능수량 조회 응답"""

    output: Sequence[StockQuoteCorrectionCancellableQtyItem] = Field(default_factory=list)


class StockDailySeparateConclusionItem1(BaseModel):
    ord_dt: str = Field(title="주문일자", description="주문일자(YYYYMMDD)", max_length=8)
    ord_gno_brno: str = Field(
        title="주문채번지점번호", description="주문시 한국투자증권 시스템에서 지정된 영업점코드", max_length=5
    )
    odno: str = Field(title="주문번호", description="주문시 한국투자증권 시스템에서 채번된 주문번호", max_length=10)
    orgn_odno: str = Field(title="원주문번호", description="정정/취소주문 인경우 원주문번호", max_length=10)
    ord_dvsn_name: str = Field(title="주문구분명", max_length=60)
    sll_buy_dvsn_cd: str = Field(title="매도매수구분코드", description="01 : 매도 / 02 : 매수", max_length=2)
    sll_buy_dvsn_cd_name: str = Field(title="매도매수구분코드명", max_length=60)
    pdno: str = Field(title="상품번호", description="종목번호(뒤 6자리만 해당)", max_length=12)
    prdt_name: str = Field(title="상품명", description="종목명", max_length=60)
    ord_qty: str = Field(title="주문수량", max_length=10)
    ord_unpr: str = Field(title="주문단가", description="1주당 주문가격", max_length=19)
    ord_tmd: str = Field(title="주문시각", description="주문시각(시분초HHMMSS)", max_length=6)
    tot_ccld_qty: str = Field(title="총체결수량", description="주문 수량 중 체결된 수량", max_length=10)
    avg_prvs: str = Field(title="평균가", description="체결된 가격의 평균가", max_length=19)
    cncl_yn: str = Field(title="취소여부", description="Y 또는 N", max_length=1)
    tot_ccld_amt: str = Field(title="총체결금액", description="주문금액 중 체결금액", max_length=19)
    loan_dt: str = Field(title="대출일자", description="신용주문인 경우 대출일자(YYYYMMDD)", max_length=8)
    ordr_empno: str = Field(title="주문자사번", description="주문한 직원의 사번", max_length=60)
    ord_dvsn_cd: str = Field(title="주문구분코드", max_length=2)
    cnc_cfrm_qty: str = Field(title="취소확인수량", description="취소주문시 취소가 확인된 수량", max_length=10)
    rmn_qty: str = Field(title="잔여수량", description="주문수량 중 체결 및 취소되지 않은 잔여수량", max_length=10)
    rjct_qty: str = Field(title="거부수량", description="주문수량 중 거부된 수량", max_length=10)
    ccld_cndt_name: str = Field(title="체결조건명", description="지정가, 시장가 등 체결조건명", max_length=10)
    inqr_ip_addr: str = Field(title="조회IP주소", description="주문을 요청한 PC의 IP주소", max_length=15)
    cpbc_ordp_ord_rcit_dvsn_cd: str = Field(title="전산주문표주문접수구분코드", max_length=2)
    cpbc_ordp_infm_mthd_dvsn_cd: str = Field(title="전산주문표통보방법구분코드", max_length=2)
    infm_tmd: str = Field(title="통보시각", description="주문접수 통보시각(시분초HHMMSS)", max_length=6)
    ctac_tlno: str = Field(title="연락전화번호", description="주문시 연락가능한 전화번호", max_length=20)
    prdt_type_cd: str = Field(title="상품유형코드", description="상품유형코드", max_length=3)
    excg_dvsn_cd: str = Field(title="거래소구분코드", max_length=2)
    cpbc_ordp_mtrl_dvsn_cd: str = Field(title="전산주문표자료구분코드", max_length=2)
    ord_orgno: str = Field(title="주문조직번호", max_length=5)
    rsvn_ord_end_dt: str = Field(
        title="예약주문종료일자", description="예약주문인 경우 예약종료일자(YYYYMMDD)", max_length=8
    )
    excg_id_dvsn_cd: str = Field(title="거래소ID구분코드", max_length=3)
    stpm_cndt_pric: str = Field(title="스톱지정가조건가격", max_length=9)
    stpm_efct_occr_dtmd: str = Field(
        title="스톱지정가효력발생상세시각", description="스톱지정가효력발생상세시각(시분초HHMMSS)", max_length=6
    )


class StockDailySeparateConclusionItem2(BaseModel):
    tot_ord_qty: str = Field(title="총주문수량", description="조회기간내 총 주문수량", max_length=10)
    tot_ccld_qty: str = Field(title="총체결수량", description="조회기간내 총 체결수량", max_length=10)
    tot_ccld_amt: str = Field(title="총체결금액", description="조회기간내 총 체결금액", max_length=19)
    pchs_avg_pric: str = Field(title="매입평균가격", description="조회기간내 매입평균가격", max_length=19)
    prsm_tlex_smtl: str = Field(title="추정제비용합계", description="조회기간내 추정제비용합계", max_length=184)


class StockDailySeparateConclusion(BaseModel, KisHttpBody):
    """주식일별주문체결조회 응답"""

    output1: Sequence[StockDailySeparateConclusionItem1] = Field(default_factory=list)
    output2: StockDailySeparateConclusionItem2


class StockBalanceItem1(BaseModel):
    pdno: str = Field(title="상품번호", description="종목번호(뒤 6자리만 해당)", max_length=12)
    prdt_name: str = Field(title="상품명", description="종목명", max_length=60)
    trad_dvsn_name: str = Field(title="매매구분명", description="매수매도구분", max_length=60)
    bfdy_buy_qty: str = Field(title="전일매수수량", max_length=10)
    bfdy_sll_qty: str = Field(title="전일매도수량", max_length=10)
    thdt_buyqty: str = Field(title="금일매수수량", max_length=10)
    thdt_sll_qty: str = Field(title="금일매도수량", max_length=10)
    hldg_qty: str = Field(title="보유수량", max_length=19)
    ord_psbl_qty: str = Field(title="주문가능수량", max_length=10)
    pchs_avg_pric: str = Field(title="매입평균가격", description="매입금액 / 보유수량", max_length=22)
    pchs_amt: str = Field(title="매입금액", max_length=19)
    prpr: str = Field(title="현재가", max_length=19)
    evlu_amt: str = Field(title="평가금액", max_length=19)
    evlu_pfls_amt: str = Field(title="평가손익금액", description="평가금액 - 매입금액", max_length=19)
    evlu_pfls_rt: str = Field(title="평가손익율", max_length=9)
    evlu_erng_rt: str = Field(title="평가수익율", description="미사용항목(0으로 출력)", max_length=31)
    loan_dt: str = Field(
        title="대출일자", description="INQR_DVSN(조회구분)을 01(대출일별)로 설정해야 값이 나옴", max_length=8
    )
    loan_amt: str = Field(title="대출금액", max_length=19)
    stln_slng_chgs: str = Field(title="대주매각대금", max_length=19)
    expd_dt: str = Field(title="만기일자", max_length=8)
    fltt_rt: str = Field(title="등락율", max_length=31)
    bfdy_cprs_icdc: str = Field(title="전일대비증감", max_length=19)
    item_mgna_rt_name: str = Field(title="종목증거금율명", max_length=20)
    grta_rt_name: str = Field(title="보증금율명", max_length=20)
    sbst_pric: str = Field(
        title="대용가격", description="증권매매의 위탁보증금으로서 현금 대신에 사용되는 유가증권 가격", max_length=19
    )
    stck_loan_unpr: str = Field(title="주식대출단가", max_length=22)


class StockBalanceItem2(BaseModel):
    dnca_tot_amt: str = Field(title="예수금총금액", description="예수금", max_length=19)
    nxdy_excc_amt: str = Field(title="익일정산금액", description="D+1 예수금", max_length=19)
    prvs_rcdl_excc_amt: str = Field(title="가수도정산금액", description="D+2 예수금", max_length=19)
    cma_evlu_amt: str = Field(title="CMA평가금액", max_length=19)
    bfdy_buy_amt: str = Field(title="전일매수금액", max_length=19)
    thdt_buy_amt: str = Field(title="금일매수금액", max_length=19)
    nxdy_auto_rdpt_amt: str = Field(title="익일자동상환금액", max_length=19)
    bfdy_sll_amt: str = Field(title="전일매도금액", max_length=19)
    thdt_sll_amt: str = Field(title="금일매도금액", max_length=19)
    d2_auto_rdpt_amt: str = Field(title="D+2자동상환금액", max_length=19)
    bfdy_tlex_amt: str = Field(title="전일제비용금액", max_length=19)
    thdt_tlex_amt: str = Field(title="금일제비용금액", max_length=19)
    tot_loan_amt: str = Field(title="총대출금액", max_length=19)
    scts_evlu_amt: str = Field(title="유가평가금액", max_length=19)
    tot_evlu_amt: str = Field(title="총평가금액", description="유가증권 평가금액 합계금액 + D+2 예수금", max_length=19)
    nass_amt: str = Field(title="순자산금액", max_length=19)
    fncg_gld_auto_rdpt_yn: str = Field(
        title="융자금자동상환여부",
        description="보유현금에 대한 융자금만 차감여부 신용융자 매수체결 시점에서는 융자비율을 매매대금 100%로 계산 하였다가 수도결제일에 보증금에 해당하는 금액을 고객의 현금으로 충당하여 융자금을 감소시키는 업무",
        max_length=1,
    )
    pchs_amt_smtl_amt: str = Field(title="매입금액합계금액", max_length=19)
    evlu_amt_smtl_amt: str = Field(title="평가금액합계금액", description="유가증권 평가금액 합계금액", max_length=19)
    evlu_pfls_smtl_amt: str = Field(title="평가손익합계금액", max_length=19)
    tot_stln_slng_chgs: str = Field(title="총대주매각대금", max_length=19)
    bfdy_tot_asst_evlu_amt: str = Field(title="전일총자산평가금액", max_length=19)
    asst_icdc_amt: str = Field(title="자산증감액", max_length=19)
    asst_icdc_erng_rt: str = Field(title="자산증감수익율", description="데이터 미제공", max_length=31)


class StockBalance(BaseModel, KisHttpBody):
    """주식잔고조회 응답"""

    ctx_area_fk100: str = Field(
        title="연속조회검색조건100",
        description="공란 : 최초 조회시는 이전 조회 Output CTX_AREA_FK100 값 : 다음페이지 조회시(2번째부터)",
        max_length=100,
    )
    ctx_area_nk100: str = Field(
        title="연속조회키100",
        description="공란 : 최초 조회시 이전 조회 Output CTX_AREA_NK100 값 : 다음페이지 조회시(2번째부터)",
        max_length=100,
    )

    output1: Sequence[StockBalanceItem1] = Field(default_factory=list)
    output2: Sequence[StockBalanceItem2] = Field(default_factory=list)


class BuyTradableInquiryItem1(BaseModel):
    pdno: str = Field(title="상품번호", description="종목번호(뒤 6자리만 해당)", max_length=12)
    prdt_name: str = Field(title="상품명", description="종목명", max_length=60)
    trad_dvsn_name: str = Field(title="매매구분명", description="매수매도구분", max_length=60)
    bfdy_buy_qty: str = Field(title="전일매수수량", max_length=10)
    bfdy_sll_qty: str = Field(title="전일매도수량", max_length=10)
    thdt_buyqty: str = Field(title="금일매수수량", max_length=10)
    thdt_sll_qty: str = Field(title="금일매도수량", max_length=10)
    hldg_qty: str = Field(title="보유수량", max_length=19)
    ord_psbl_qty: str = Field(title="주문가능수량", max_length=10)
    pchs_avg_pric: str = Field(title="매입평균가격", description="매입금액 / 보유수량", max_length=22)
    pchs_amt: str = Field(title="매입금액", max_length=19)
    prpr: str = Field(title="현재가", max_length=19)
    evlu_amt: str = Field(title="평가금액", max_length=19)
    evlu_pfls_amt: str = Field(title="평가손익금액", description="평가금액 - 매입금액", max_length=19)
    evlu_pfls_rt: str = Field(title="평가손익율", max_length=9)
    evlu_erng_rt: str = Field(title="평가수익율", description="미사용항목(0으로 출력)", max_length=31)
    loan_dt: str = Field(
        title="대출일자", description="INQR_DVSN(조회구분)을 01(대출일별)로 설정해야 값이 나옴", max_length=8
    )
    loan_amt: str = Field(title="대출금액", max_length=19)
    stln_slng_chgs: str = Field(title="대주매각대금", max_length=19)
    expd_dt: str = Field(title="만기일자", max_length=8)
    fltt_rt: str = Field(title="등락율", max_length=31)
    bfdy_cprs_icdc: str = Field(title="전일대비증감", max_length=19)
    item_mgna_rt_name: str = Field(title="종목증거금율명", max_length=20)
    grta_rt_name: str = Field(title="보증금율명", max_length=20)
    sbst_pric: str = Field(
        title="대용가격", description="증권매매의 위탁보증금으로서 현금 대신에 사용되는 유가증권 가격", max_length=19
    )
    stck_loan_unpr: str = Field(title="주식대출단가", max_length=22)


class BuyTradableInquiryItem2(BaseModel):
    dnca_tot_amt: str = Field(title="예수금총금액", description="예수금", max_length=19)
    nxdy_excc_amt: str = Field(title="익일정산금액", description="D+1 예수금", max_length=19)
    prvs_rcdl_excc_amt: str = Field(title="가수도정산금액", description="D+2 예수금", max_length=19)
    cma_evlu_amt: str = Field(title="CMA평가금액", max_length=19)
    bfdy_buy_amt: str = Field(title="전일매수금액", max_length=19)
    thdt_buy_amt: str = Field(title="금일매수금액", max_length=19)
    nxdy_auto_rdpt_amt: str = Field(title="익일자동상환금액", max_length=19)
    bfdy_sll_amt: str = Field(title="전일매도금액", max_length=19)
    thdt_sll_amt: str = Field(title="금일매도금액", max_length=19)
    d2_auto_rdpt_amt: str = Field(title="D+2자동상환금액", max_length=19)
    bfdy_tlex_amt: str = Field(title="전일제비용금액", max_length=19)
    thdt_tlex_amt: str = Field(title="금일제비용금액", max_length=19)
    tot_loan_amt: str = Field(title="총대출금액", max_length=19)
    scts_evlu_amt: str = Field(title="유가평가금액", max_length=19)
    tot_evlu_amt: str = Field(title="총평가금액", description="유가증권 평가금액 합계금액 + D+2 예수금", max_length=19)
    nass_amt: str = Field(title="순자산금액", max_length=19)
    fncg_gld_auto_rdpt_yn: str = Field(
        title="융자금자동상환여부",
        description="보유현금에 대한 융자금만 차감여부 신용융자 매수체결 시점에서는 융자비율을 매매대금 100%로 계산 하였다가 수도결제일에 보증금에 해당하는 금액을 고객의 현금으로 충당하여 융자금을 감소시키는 업무",
        max_length=1,
    )
    pchs_amt_smtl_amt: str = Field(title="매입금액합계금액", max_length=19)
    evlu_amt_smtl_amt: str = Field(title="평가금액합계금액", description="유가증권 평가금액 합계금액", max_length=19)
    evlu_pfls_smtl_amt: str = Field(title="평가손익합계금액", max_length=19)
    tot_stln_slng_chgs: str = Field(title="총대주매각대금", max_length=19)
    bfdy_tot_asst_evlu_amt: str = Field(title="전일총자산평가금액", max_length=19)
    asst_icdc_amt: str = Field(title="자산증감액", max_length=19)
    asst_icdc_erng_rt: str = Field(title="자산증감수익율", description="데이터 미제공", max_length=31)


class BuyTradableInquiry(BaseModel, KisHttpBody):
    """매수가능조회 응답"""

    ctx_area_fk100: str = Field(
        title="연속조회검색조건100",
        description="공란 : 최초 조회시는 이전 조회 Output CTX_AREA_FK100 값 : 다음페이지 조회시(2번째부터)",
        max_length=100,
    )
    ctx_area_nk100: str = Field(
        title="연속조회키100",
        description="공란 : 최초 조회시 이전 조회 Output CTX_AREA_NK100 값 : 다음페이지 조회시(2번째부터)",
        max_length=100,
    )

    output1: Sequence[BuyTradableInquiryItem1] = Field(default_factory=list)
    output2: Sequence[BuyTradableInquiryItem2] = Field(default_factory=list)


class SellTradableInquiryItem(BaseModel):
    pdno: str = Field(title="상품번호", description="종목번호(뒤 6자리만 해당)", max_length=12)
    prdt_name: str = Field(title="상품명", description="종목명", max_length=60)
    buy_qty: str = Field(title="매수수량", max_length=10)
    sll_qty: str = Field(title="매도수량", max_length=10)
    cblc_qty: str = Field(title="잔고수량", max_length=19)
    nsvg_qty: str = Field(title="비저축수량", max_length=19)
    ord_psbl_qty: str = Field(title="주문가능수량", max_length=10)
    pchs_avg_pric: str = Field(title="매입평균가격", description="매입금액 / 보유수량", max_length=184)
    pchs_amt: str = Field(title="매입금액", max_length=19)
    now_pric: str = Field(title="현재가", max_length=8)
    evlu_amt: str = Field(title="평가금액", max_length=19)
    evlu_pfls_amt: str = Field(title="평가손익금액", description="평가금액 - 매입금액", max_length=19)
    evlu_pfls_rt: str = Field(title="평가손익율", max_length=72)

class SellTradableInquiry(BaseModel, KisHttpBody):
    """매도가능수량조회 응답"""

    output1: Sequence[SellTradableInquiryItem] = Field(default_factory=list)

class CreditTradableInquiryItem(BaseModel):
    ord_psbl_cash: str = Field(title="주문가능현금", max_length=19)
    ord_psbl_sbst: str = Field(title="주문가능대용", max_length=19)
    ruse_psbl_amt: str = Field(title="재사용가능금액", max_length=19)
    fund_rpch_chgs: str = Field(title="펀드환매대금", max_length=19)
    psbl_qty_calc_unpr: str = Field(title="가능수량계산단가", max_length=19)
    nrcvb_buy_amt: str = Field(title="미수없는매수금액", max_length=19)
    nrcvb_buy_qty: str = Field(title="미수없는매수수량", max_length=10)
    max_buy_amt: str = Field(title="최대매수금액", max_length=19)
    max_buy_qty: str = Field(title="최대매수수량", max_length=10)
    cma_evlu_amt: str = Field(title="CMA평가금액", max_length=19)
    ovrs_re_use_amt_wcrc: str = Field(title="해외재사용금액원화", max_length=19)
    ord_psbl_frcr_amt_wcrc: str = Field(title="주문가능외화금액원화", max_length=19)

class CreditTradableInquiry(BaseModel, KisHttpBody):
    """신용매수가능조회 응답"""

    output1: Sequence[CreditTradableInquiryItem] = Field(default_factory=list)

class StockReserveQuoteItem(BaseModel):
    rsvn_ord_seq: Optional[str] = Field(title="예약주문순번", max_length=10)

class StockReserveQuote(BaseModel, KisHttpBody):
    """주식예약주문 응답"""

    output: Sequence[StockReserveQuoteItem] = Field(default_factory=list)


class StockReserveQuoteCorrectionItem(BaseModel):
    nrml_prcs_yn: str = Field(title="정상처리여부", max_length=1)

class StockReserveQuoteCorrection(BaseModel, KisHttpBody):
    """주식예약주문정정/취소 응답"""

    output: Sequence[StockReserveQuoteCorrectionItem] = Field(default_factory=list)

class StockReserveQuoteInquiryItem(BaseModel):
    rsvn_ord_seq: str = Field(title="예약주문 순번", max_length=10)
    rsvn_ord_ord_dt: str = Field(title="예약주문주문일자", max_length=8)
    rsvn_ord_rcit_dt: str = Field(title="예약주문접수일자", max_length=8)
    pdno: str = Field(title="상품번호", max_length=12)
    ord_dvsn_cd: str = Field(title="주문구분코드", max_length=2)
    ord_rsvn_qty: str = Field(title="주문예약수량", max_length=10)
    tot_ccld_qty: str = Field(title="총체결수량", max_length=10)
    cncl_ord_dt: str = Field(title="취소주문일자", max_length=8)
    ord_tmd: str = Field(title="주문시각", max_length=6)
    ctac_tlno: str = Field(title="연락전화번호", max_length=20)
    rjct_rson2: str = Field(title="거부사유2", max_length=200)
    odno: str = Field(title="주문번호", max_length=10)
    rsvn_ord_rcit_tmd: str = Field(title="예약주문접수시각", max_length=6)
    kor_item_shtn_name: str = Field(title="한글종목단축명", max_length=60)
    sll_buy_dvsn_cd: str = Field(title="매도매수구분코드", max_length=2)
    ord_rsvn_unpr: str = Field(title="주문예약단가", max_length=19)
    tot_ccld_amt: str = Field(title="총체결금액", max_length=19)
    loan_dt: str = Field(title="대출일자", max_length=8)
    cncl_rcit_tmd: str = Field(title="취소접수시각", max_length=6)
    prcs_rslt: str = Field(title="처리결과", max_length=60)
    ord_dvsn_name: str = Field(title="주문구분명", max_length=60)
    tmnl_mdia_kind_cd: str = Field(title="단말매체종류코드", max_length=2)
    rsvn_end_dt: str = Field(title="예약종료일자", max_length=8)

class StockReserveQuoteInquiry(BaseModel, KisHttpBody):
    """주식예약주문조회 응답"""

    output: Sequence[StockReserveQuoteInquiryItem] = Field(default_factory=list)


class PensionExecutedBalanceItem1(BaseModel):
    cblc_dvsn: str = Field(title="잔고구분", max_length=2)
    cblc_dvsn_name: str = Field(title="잔고구분명", max_length=60)
    pdno: str = Field(title="상품번호", max_length=12)
    prdt_name: str = Field(title="상품명", max_length=60)
    hldg_qty: str = Field(title="보유수량", max_length=19)
    slpsb_qty: str = Field(title="매도가능수량", max_length=10)
    pchs_avg_pric: str = Field(title="매입평균가격", max_length=184)
    evlu_pfls_amt: str = Field(title="평가손익금액", max_length=19)
    evlu_pfls_rt: str = Field(title="평가손익율", max_length=72)
    prpr: str = Field(title="현재가", max_length=19)
    evlu_amt: str = Field(title="평가금액", max_length=19)
    pchs_amt: str = Field(title="매입금액", max_length=19)
    cblc_weit: str = Field(title="잔고비중", max_length=238)


class PensionExecutedBalanceItem2(BaseModel):
    pchs_amt_smtl_amt: str = Field(title="매입금액합계금액", max_length=19)
    evlu_amt_smtl_amt: str = Field(title="평가금액합계금액", max_length=19)
    evlu_pfls_smtl_amt: str = Field(title="평가손익합계금액", max_length=19)
    trad_pfls_smtl: str = Field(title="매매손익합계", max_length=19)
    thdt_tot_pfls_amt: str = Field(title="당일총손익금액", max_length=19)
    pftrt: str = Field(title="수익률", max_length=238)

class PensionExecutedBalance(BaseModel, KisHttpBody):
    """퇴직연금체결기준잔고 응답"""

    output1: Sequence[PensionExecutedBalanceItem1] = Field(default_factory=list)
    output2: Sequence[PensionExecutedBalanceItem2] = Field(default_factory=list)

class PensionUnexecutedHistoryItem(BaseModel):
    ord_gno_brno: str = Field(alias="ord_gno_brno", title="주문채번지점번호", max_length=5)
    sll_buy_dvsn_cd: str = Field(alias="sll_buy_dvsn_cd", title="매도매수구분코드", max_length=2)
    trad_dvsn_name: str = Field(alias="trad_dvsn_name", title="매매구분명", max_length=60)
    odno: str = Field(alias="odno", title="주문번호", max_length=10)
    pdno: str = Field(alias="pdno", title="상품번호", max_length=12)
    prdt_name: str = Field(alias="prdt_name", title="상품명", max_length=60)
    ord_unpr: str = Field(alias="ord_unpr", title="주문단가", max_length=19)
    ord_qty: str = Field(alias="ord_qty", title="주문수량", max_length=10)
    tot_ccld_qty: str = Field(alias="tot_ccld_qty", title="총체결수량", max_length=10)
    nccs_qty: str = Field(alias="nccs_qty", title="미체결수량", max_length=10)
    ord_dvsn_cd: str = Field(alias="ord_dvsn_cd", title="주문구분코드", max_length=2)
    ord_dvsn_name: str = Field(alias="ord_dvsn_name", title="주문구분명", max_length=60)
    orgn_odno: str = Field(alias="orgn_odno", title="원주문번호", max_length=10)
    ord_tmd: str = Field(alias="ord_tmd", title="주문시각", max_length=6)
    objt_cust_dvsn_name: str = Field(alias="objt_cust_dvsn_name", title="대상고객구분명", max_length=10)
    pchs_avg_pric: str = Field(alias="pchs_avg_pric", title="매입평균가격", max_length=184)
    stpm_cndt_pric: str = Field(alias="stpm_cndt_pric", title="스톱지정가조건가격", max_length=9)
    stpm_efct_occr_dtmd: str = Field(alias="stpm_efct_occr_dtmd", title="스톱지정가효력발생상세시각", max_length=9)
    stpm_efct_occr_yn: str = Field(alias="stpm_efct_occr_yn", title="스톱지정가효력발생여부", max_length=1)
    excg_id_dvsn_cd: str = Field(alias="excg_id_dvsn_cd", title="거래소ID구분코드", max_length=3)

class PensionUnexecutedHistory(BaseModel, KisHttpBody):
    """퇴직연금미체결내역 응답"""

    output: Sequence[PensionUnexecutedHistoryItem] = Field(default_factory=list)

class PensionBuyTradableInquiryItem(BaseModel):
    ord_psbl_cash: str = Field(alias="ord_psbl_cash", title="주문가능현금", max_length=19)
    ruse_psbl_amt: str = Field(alias="ruse_psbl_amt", title="재사용가능금액", max_length=19)
    psbl_qty_calc_unpr: str = Field(alias="psbl_qty_calc_unpr", title="가능수량계산단가", max_length=19)
    max_buy_amt: str = Field(alias="max_buy_amt", title="최대매수금액", max_length=19)
    max_buy_qty: str = Field(alias="max_buy_qty", title="최대매수수량", max_length=10)

class PensionBuyTradableInquiry(BaseModel, KisHttpBody):
    """퇴직연금 매수가능조회 응답"""

    output: Sequence[PensionBuyTradableInquiryItem] = Field(default_factory=list)

class PensionReserveDepositInquiryItem(BaseModel):
    dnca_tota: str = Field(alias="dnca_tota", title="예수금총액", max_length=19)
    nxdy_excc_amt: str = Field(alias="nxdy_excc_amt", title="익일정산액", max_length=19)
    nxdy_sttl_amt: str = Field(alias="nxdy_sttl_amt", title="익일결제금액", max_length=19)
    nx2_day_sttl_amt: str = Field(alias="nx2_day_sttl_amt", title="익일결제금액", max_length=19)

class PensionReserveDepositInquiry(BaseModel, KisHttpBody):
    """퇴직연금 예수금조회 응답"""

    output: Sequence[PensionReserveDepositInquiryItem] = Field(default_factory=list)


class PensionBalanceInquiryItem1(BaseModel):
    cblc_dvsn_name: str = Field(alias="cblc_dvsn_name", title="잔고구분명", max_length=60)
    prdt_name: str = Field(alias="prdt_name", title="상품명", max_length=60)
    pdno: str = Field(alias="pdno", title="상품번호", max_length=12)
    item_dvsn_name: str = Field(alias="item_dvsn_name", title="종목구분명", max_length=60)
    thdt_buyqty: str = Field(alias="thdt_buyqty", title="금일매수수량", max_length=10)
    thdt_sll_qty: str = Field(alias="thdt_sll_qty", title="금일매도수량", max_length=10)
    hldg_qty: str = Field(alias="hldg_qty", title="보유수량", max_length=19)
    ord_psbl_qty: str = Field(alias="ord_psbl_qty", title="주문가능수량", max_length=10)
    pchs_avg_pric: str = Field(alias="pchs_avg_pric", title="매입평균가격", max_length=184)
    pchs_amt: str = Field(alias="pchs_amt", title="매입금액", max_length=19)
    prpr: str = Field(alias="prpr", title="현재가", max_length=19)
    evlu_amt: str = Field(alias="evlu_amt", title="평가금액", max_length=19)
    evlu_pfls_amt: str = Field(alias="evlu_pfls_amt", title="평가손익금액", max_length=19)
    evlu_erng_rt: str = Field(alias="evlu_erng_rt", title="평가수익율", max_length=238)

class PensionBalanceInquiryItem2(BaseModel):
    dnca_tot_amt: str = Field(alias="dnca_tot_amt", title="예수금총금액", max_length=19)
    nxdy_excc_amt: str = Field(alias="nxdy_excc_amt", title="익일정산금액", max_length=19)
    prvs_rcdl_excc_amt: str = Field(alias="prvs_rcdl_excc_amt", title="가수도정산금액", max_length=19)
    thdt_buy_amt: str = Field(alias="thdt_buy_amt", title="금일매수금액", max_length=19)
    thdt_sll_amt: str = Field(alias="thdt_sll_amt", title="금일매도금액", max_length=19)
    thdt_tlex_amt: str = Field(alias="thdt_tlex_amt", title="금일제비용금액", max_length=19)
    scts_evlu_amt: str = Field(alias="scts_evlu_amt", title="유가평가금액", max_length=19)
    tot_evlu_amt: str = Field(alias="tot_evlu_amt", title="총평가금액", max_length=19)

class PensionBalanceInquiry(BaseModel, KisHttpBody):
    """퇴직연금 잔고조회 응답"""

    output1: Sequence[PensionBalanceInquiryItem1] = Field(default_factory=list)
    output2: Sequence[PensionBalanceInquiryItem2] = Field(default_factory=list)

class StockBalanceLossProfitItem1(BaseModel):
    pdno: str = Field(alias="pdno", title="상품번호", max_length=12)
    prdt_name: str = Field(alias="prdt_name", title="상품명", max_length=60)
    trad_dvsn_name: str = Field(alias="trad_dvsn_name", title="매매구분명", max_length=60)
    bfdy_buy_qty: str = Field(alias="bfdy_buy_qty", title="전일매수수량", max_length=10)
    bfdy_sll_qty: str = Field(alias="bfdy_sll_qty", title="전일매도수량", max_length=10)
    thdt_buyqty: str = Field(alias="thdt_buyqty", title="금일매수수량", max_length=10)
    thdt_sll_qty: str = Field(alias="thdt_sll_qty", title="금일매도수량", max_length=10)
    hldg_qty: str = Field(alias="hldg_qty", title="보유수량", max_length=19)
    ord_psbl_qty: str = Field(alias="ord_psbl_qty", title="주문가능수량", max_length=10)
    pchs_avg_pric: str = Field(alias="pchs_avg_pric", title="매입평균가격", max_length=23)
    pchs_amt: str = Field(alias="pchs_amt", title="매입금액", max_length=19)
    prpr: str = Field(alias="prpr", title="현재가", max_length=19)
    evlu_amt: str = Field(alias="evlu_amt", title="평가금액", max_length=19)
    evlu_pfls_amt: str = Field(alias="evlu_pfls_amt", title="평가손익금액", max_length=19)
    evlu_pfls_rt: str = Field(alias="evlu_pfls_rt", title="평가손익율", max_length=10)
    evlu_erng_rt: str = Field(alias="evlu_erng_rt", title="평가수익율", max_length=32)
    loan_dt: str = Field(alias="loan_dt", title="대출일자", max_length=8)
    loan_amt: str = Field(alias="loan_amt", title="대출금액", max_length=19)
    stln_slng_chgs: str = Field(alias="stln_slng_chgs", title="대주매각대금", max_length=19)
    expd_dt: str = Field(alias="expd_dt", title="만기일자", max_length=8)
    stck_loan_unpr: str = Field(alias="stck_loan_unpr", title="주식대출단가", max_length=23)
    bfdy_cprs_icdc: str = Field(alias="bfdy_cprs_icdc", title="전일대비증감", max_length=19)
    fltt_rt: str = Field(alias="fltt_rt", title="등락율", max_length=32)

class StockBalanceLossProfitItem2(BaseModel):
    dnca_tot_amt: str = Field(alias="dnca_tot_amt", title="예수금총금액", max_length=19)
    nxdy_excc_amt: str = Field(alias="nxdy_excc_amt", title="익일정산금액", max_length=19)
    prvs_rcdl_excc_amt: str = Field(alias="prvs_rcdl_excc_amt", title="가수도정산금액", max_length=19)
    cma_evlu_amt: str = Field(alias="cma_evlu_amt", title="CMA평가금액", max_length=19)
    bfdy_buy_amt: str = Field(alias="bfdy_buy_amt", title="전일매수금액", max_length=19)
    thdt_buy_amt: str = Field(alias="thdt_buy_amt", title="금일매수금액", max_length=19)
    nxdy_auto_rdpt_amt: str = Field(alias="nxdy_auto_rdpt_amt", title="익일자동상환금액", max_length=19)
    bfdy_sll_amt: str = Field(alias="bfdy_sll_amt", title="전일매도금액", max_length=19)
    thdt_sll_amt: str = Field(alias="thdt_sll_amt", title="금일매도금액", max_length=19)
    d2_auto_rdpt_amt: str = Field(alias="d2_auto_rdpt_amt", title="D+2자동상환금액", max_length=19)
    bfdy_tlex_amt: str = Field(alias="bfdy_tlex_amt", title="전일제비용금액", max_length=19)
    thdt_tlex_amt: str = Field(alias="thdt_tlex_amt", title="금일제비용금액", max_length=19)
    tot_loan_amt: str = Field(alias="tot_loan_amt", title="총대출금액", max_length=19)
    scts_evlu_amt: str = Field(alias="scts_evlu_amt", title="유가평가금액", max_length=19)
    tot_evlu_amt: str = Field(alias="tot_evlu_amt", title="총평가금액", max_length=19)
    nass_amt: str = Field(alias="nass_amt", title="순자산금액", max_length=19)
    fncg_gld_auto_rdpt_yn: str = Field(alias="fncg_gld_auto_rdpt_yn", title="융자금자동상환여부", max_length=1)
    pchs_amt_smtl_amt: str = Field(alias="pchs_amt_smtl_amt", title="매입금액합계금액", max_length=19)
    evlu_amt_smtl_amt: str = Field(alias="evlu_amt_smtl_amt", title="평가금액합계금액", max_length=19)
    evlu_pfls_smtl_amt: str = Field(alias="evlu_pfls_smtl_amt", title="평가손익합계금액", max_length=19)
    tot_stln_slng_chgs: str = Field(alias="tot_stln_slng_chgs", title="총대주매각대금", max_length=19)
    bfdy_tot_asst_evlu_amt: str = Field(alias="bfdy_tot_asst_evlu_amt", title="전일총자산평가금액", max_length=19)
    asst_icdc_amt: str = Field(alias="asst_icdc_amt", title="자산증감액", max_length=19)
    asst_icdc_erng_rt: str = Field(alias="asst_icdc_erng_rt", title="자산증감수익율", max_length=32)
    rlzt_pfls: str = Field(alias="rlzt_pfls", title="실현손익", max_length=19)
    rlzt_erng_rt: str = Field(alias="rlzt_erng_rt", title="실현수익율", max_length=32)
    real_evlu_pfls: str = Field(alias="real_evlu_pfls", title="실평가손익", max_length=19)
    real_evlu_pfls_erng_rt: str = Field(alias="real_evlu_pfls_erng_rt", title="실평가손익수익율", max_length=32)

class StockBalanceLossProfit(BaseModel, KisHttpBody):
    """주식잔고조회 실현손익 응답"""

    output1: Sequence[StockBalanceLossProfitItem1] = Field(default_factory=list)
    output2: Sequence[StockBalanceLossProfitItem2] = Field(default_factory=list)

class InvestmentAccountCurrentStatusItem1(BaseModel):
    pchs_amt: str = Field(description="매입금액")
    evlu_amt: str = Field(description="평가금액")
    evlu_pfls_amt: str = Field(description="평가손익금액")
    crdt_lnd_amt: str = Field(description="신용대출금액")
    real_nass_amt: str = Field(description="실제순자산금액")
    whol_weit_rt: str = Field(description="전체비중율")

class InvestmentAccountCurrentStatusItem2(BaseModel):
    pchs_amt_smtl: str = Field(description="매입금액합계")
    nass_tot_amt: str = Field(description="순자산총금액")
    loan_amt_smtl: str = Field(description="대출금액합계")
    evlu_pfls_amt_smtl: str = Field(description="평가손익금액합계")
    evlu_amt_smtl: str = Field(description="평가금액합계")
    tot_asst_amt: str = Field(description="총자산금액")
    tot_lnda_tot_ulst_lnda: str = Field(description="총대출금액총융자대출금액")
    cma_auto_loan_amt: str = Field(description="CMA자동대출금액")
    tot_mgln_amt: str = Field(description="총당보대출금액")
    stln_evlu_amt: str = Field(description="대주평가금액")
    crdt_fncg_amt: str = Field(description="신용융자금액")
    ocl_apl_loan_amt: str = Field(description="OCL_APL대출금액")
    pldg_stup_amt: str = Field(description="질권설정금액")
    frcr_evlu_tota: str = Field(description="외화평가총액")
    tot_dncl_amt: str = Field(description="총예수금액")
    cma_evlu_amt: str = Field(description="CMA평가금액")
    dncl_amt: str = Field(description="예수금액")
    tot_sbst_amt: str = Field(description="총대용금액")
    thdt_rcvb_amt: str = Field(description="당일미수금액")
    ovrs_stck_evlu_amt1: str = Field(description="해외주식평가금액1")
    ovrs_bond_evlu_amt: str = Field(description="해외채권평가금액")
    mmf_cma_mgge_loan_amt: str = Field(description="MMFCMA담보대출금액")
    sbsc_dncl_amt: str = Field(description="청약예수금액")
    pbst_sbsc_fnds_loan_use_amt: str = Field(description="공모주청약자금대출사용금액")
    etpr_crdt_grnt_loan_amt: str = Field(description="기업신용공여대출금액")

class InvestmentAccountCurrentStatus(BaseModel, KisHttpBody):
    """투자계좌자산현황조회 응답"""

    output1: Sequence[InvestmentAccountCurrentStatusItem1] = Field(default_factory=list)
    output2: Sequence[InvestmentAccountCurrentStatusItem2] = Field(default_factory=list)

class PeriodProfitSummaryItem1(BaseModel):
    trad_dt: str = Field(description="매매일자")
    buy_amt: str = Field(description="매수금액")
    sll_amt: str = Field(description="매도금액")
    rlzt_pfls: str = Field(description="실현손익")
    fee: str = Field(description="수수료")
    loan_int: str = Field(description="대출이자")
    tl_tax: str = Field(description="제세금")
    pfls_rt: str = Field(description="손익률")
    sll_qty1: str = Field(description="매도수량1")
    buy_qty1: str = Field(description="매수수량1")

class PeriodProfitSummaryItem2(BaseModel):
    sll_qty_smtl: str = Field(description="매도수량합계")
    sll_tr_amt_smtl: str = Field(description="매도거래금액합계")
    sll_fee_smtl: str = Field(description="매도수수료합계")
    sll_tltx_smtl: str = Field(description="매도제세금합계")
    sll_excc_amt_smtl: str = Field(description="매도정산금액합계")
    buy_qty_smtl: str = Field(description="매수수량합계")
    buy_tr_amt_smtl: str = Field(description="매수거래금액합계")
    buy_fee_smtl: str = Field(description="매수수수료합계")
    buy_tax_smtl: str = Field(description="매수제세금합계")
    buy_excc_amt_smtl: str = Field(description="매수정산금액합계")
    tot_qty: str = Field(description="총수량")
    tot_tr_amt: str = Field(description="총거래금액")
    tot_fee: str = Field(description="총수수료")
    tot_tltx: str = Field(description="총제세금")
    tot_excc_amt: str = Field(description="총정산금액")
    tot_rlzt_pfls: str = Field(description="총실현손익")
    loan_int: str = Field(description="대출이자")

class PeriodProfitSummary(BaseModel, KisHttpBody):
    """기간별순익별합산조회 응답"""

    output1: Sequence[PeriodProfitSummaryItem1] = Field(default_factory=list)
    output2: Sequence[PeriodProfitSummaryItem2] = Field(default_factory=list)

class PeriodTradingProfitStatusItem1(BaseModel):
    """기간별 매매손익현황 개별 항목"""

    trad_dt: str = Field(alias="trad_dt", description="매매일자")
    pdno: str = Field(alias="pdno", description="상품번호 (종목번호 뒤 6자리만 해당)")
    prdt_name: str = Field(alias="prdt_name", description="상품명")
    trad_dvsn_name: str = Field(alias="trad_dvsn_name", description="매매구분명")
    loan_dt: str = Field(alias="loan_dt", description="대출일자")
    hldg_qty: str = Field(alias="hldg_qty", description="보유수량")
    pchs_unpr: str = Field(alias="pchs_unpr", description="매입단가")
    buy_qty: str = Field(alias="buy_qty", description="매수수량")
    buy_amt: str = Field(alias="buy_amt", description="매수금액")
    sll_pric: str = Field(alias="sll_pric", description="매도가격")
    sll_qty: str = Field(alias="sll_qty", description="매도수량")
    sll_amt: str = Field(alias="sll_amt", description="매도금액")
    rlzt_pfls: str = Field(alias="rlzt_pfls", description="실현손익")
    pfls_rt: str = Field(alias="pfls_rt", description="손익률")
    fee: str = Field(alias="fee", description="수수료")
    tl_tax: str = Field(alias="tl_tax", description="제세금")
    loan_int: str = Field(alias="loan_int", description="대출이자")


class PeriodTradingProfitStatusItem2(BaseModel):
    """기간별 매매손익현황 합계 항목"""

    sll_qty_smtl: str = Field(alias="sll_qty_smtl", description="매도수량합계")
    sll_tr_amt_smtl: str = Field(alias="sll_tr_amt_smtl", description="매도거래금액합계")
    sll_fee_smtl: str = Field(alias="sll_fee_smtl", description="매도수수료합계")
    sll_tltx_smtl: str = Field(alias="sll_tltx_smtl", description="매도제세금합계")
    sll_excc_amt_smtl: str = Field(alias="sll_excc_amt_smtl", description="매도정산금액합계")
    buyqty_smtl: str = Field(alias="buyqty_smtl", description="매수수량합계")
    buy_tr_amt_smtl: str = Field(alias="buy_tr_amt_smtl", description="매수거래금액합계")
    buy_fee_smtl: str = Field(alias="buy_fee_smtl", description="매수수수료합계")
    buy_tax_smtl: str = Field(alias="buy_tax_smtl", description="매수제세금합계")
    buy_excc_amt_smtl: str = Field(alias="buy_excc_amt_smtl", description="매수정산금액합계")
    tot_qty: str = Field(alias="tot_qty", description="총수량")
    tot_tr_amt: str = Field(alias="tot_tr_amt", description="총거래금액")
    tot_fee: str = Field(alias="tot_fee", description="총수수료")
    tot_tltx: str = Field(alias="tot_tltx", description="총제세금")
    tot_excc_amt: str = Field(alias="tot_excc_amt", description="총정산금액")
    tot_rlzt_pfls: str = Field(alias="tot_rlzt_pfls", description="총실현손익")
    loan_int: str = Field(alias="loan_int", description="대출이자")
    tot_pftrt: str = Field(alias="tot_pftrt", description="총수익률")


class PeriodTradingProfitStatus(BaseModel, KisHttpBody):
    """기간별매매순익현황조회 응답"""

    output1: Sequence[PeriodTradingProfitStatusItem1] = Field(default_factory=list)
    output2: Sequence[PeriodTradingProfitStatusItem2] = Field(default_factory=list)

class StockIntegratedDepositBalanceItem(BaseModel):
    """주식통합증거금 현황조회 항목"""

    acmga_rt: str = Field(alias="acmga_rt", description="계좌증거금율")
    acmga_pct100_aptm_rson: str = Field(alias="acmga_pct100_aptm_rson", description="계좌증거금100퍼센트지정사유")
    stck_cash_objt_amt: str = Field(alias="stck_cash_objt_amt", description="주식현금대상금액")
    stck_sbst_objt_amt: str = Field(alias="stck_sbst_objt_amt", description="주식대용대상금액")
    stck_evlu_objt_amt: str = Field(alias="stck_evlu_objt_amt", description="주식평가대상금액")
    stck_ruse_psbl_objt_amt: str = Field(alias="stck_ruse_psbl_objt_amt", description="주식재사용가능대상금액")
    stck_fund_rpch_chgs_objt_amt: str = Field(alias="stck_fund_rpch_chgs_objt_amt", description="주식펀드환매대금대상금액")
    stck_fncg_rdpt_objt_atm: str = Field(alias="stck_fncg_rdpt_objt_atm", description="주식융자상환금대상금액")
    bond_ruse_psbl_objt_amt: str = Field(alias="bond_ruse_psbl_objt_amt", description="채권재사용가능대상금액")
    stck_cash_use_amt: str = Field(alias="stck_cash_use_amt", description="주식현금사용금액")
    stck_sbst_use_amt: str = Field(alias="stck_sbst_use_amt", description="주식대용사용금액")
    stck_evlu_use_amt: str = Field(alias="stck_evlu_use_amt", description="주식평가사용금액")
    stck_ruse_psbl_amt_use_amt: str = Field(alias="stck_ruse_psbl_amt_use_amt", description="주식재사용가능금사용금액")
    stck_fund_rpch_chgs_use_amt: str = Field(alias="stck_fund_rpch_chgs_use_amt", description="주식펀드환매대금사용금액")
    stck_fncg_rdpt_amt_use_amt: str = Field(alias="stck_fncg_rdpt_amt_use_amt", description="주식융자상환금사용금액")
    bond_ruse_psbl_amt_use_amt: str = Field(alias="bond_ruse_psbl_amt_use_amt", description="채권재사용가능금사용금액")
    stck_cash_ord_psbl_amt: str = Field(alias="stck_cash_ord_psbl_amt", description="주식현금주문가능금액")
    stck_sbst_ord_psbl_amt: str = Field(alias="stck_sbst_ord_psbl_amt", description="주식대용주문가능금액")
    stck_evlu_ord_psbl_amt: str = Field(alias="stck_evlu_ord_psbl_amt", description="주식평가주문가능금액")
    stck_ruse_psbl_ord_psbl_amt: str = Field(alias="stck_ruse_psbl_ord_psbl_amt", description="주식재사용가능주문가능금액")
    stck_fund_rpch_ord_psbl_amt: str = Field(alias="stck_fund_rpch_ord_psbl_amt", description="주식펀드환매주문가능금액")
    bond_ruse_psbl_ord_psbl_amt: str = Field(alias="bond_ruse_psbl_ord_psbl_amt", description="채권재사용가능주문가능금액")
    rcvb_amt: str = Field(alias="rcvb_amt", description="미수금액")
    stck_loan_grta_ruse_psbl_amt: str = Field(alias="stck_loan_grta_ruse_psbl_amt", description="주식대출보증금재사용가능금액")
    stck_cash20_max_ord_psbl_amt: str = Field(alias="stck_cash20_max_ord_psbl_amt", description="주식현금20최대주문가능금액")
    stck_cash30_max_ord_psbl_amt: str = Field(alias="stck_cash30_max_ord_psbl_amt", description="주식현금30최대주문가능금액")
    stck_cash40_max_ord_psbl_amt: str = Field(alias="stck_cash40_max_ord_psbl_amt", description="주식현금40최대주문가능금액")
    stck_cash50_max_ord_psbl_amt: str = Field(alias="stck_cash50_max_ord_psbl_amt", description="주식현금50최대주문가능금액")
    stck_cash60_max_ord_psbl_amt: str = Field(alias="stck_cash60_max_ord_psbl_amt", description="주식현금60최대주문가능금액")
    stck_cash100_max_ord_psbl_amt: str = Field(alias="stck_cash100_max_ord_psbl_amt", description="주식현금100최대주문가능금액")
    stck_rsip100_max_ord_psbl_amt: str = Field(alias="stck_rsip100_max_ord_psbl_amt", description="주식재사용불가100최대주문가능")
    bond_max_ord_psbl_amt: str = Field(alias="bond_max_ord_psbl_amt", description="채권최대주문가능금액")
    stck_fncg45_max_ord_psbl_amt: str = Field(alias="stck_fncg45_max_ord_psbl_amt", description="주식융자45최대주문가능금액")
    stck_fncg50_max_ord_psbl_amt: str = Field(alias="stck_fncg50_max_ord_psbl_amt", description="주식융자50최대주문가능금액")
    stck_fncg60_max_ord_psbl_amt: str = Field(alias="stck_fncg60_max_ord_psbl_amt", description="주식융자60최대주문가능금액")
    stck_fncg70_max_ord_psbl_amt: str = Field(alias="stck_fncg70_max_ord_psbl_amt", description="주식융자70최대주문가능금액")
    stck_stln_max_ord_psbl_amt: str = Field(alias="stck_stln_max_ord_psbl_amt", description="주식대주최대주문가능금액")
    lmt_amt: str = Field(alias="lmt_amt", description="한도금액")
    ovrs_stck_itgr_mgna_dvsn_name: str = Field(alias="ovrs_stck_itgr_mgna_dvsn_name", description="해외주식통합증거금구분명")
    usd_objt_amt: str = Field(alias="usd_objt_amt", description="미화대상금액")
    usd_use_amt: str = Field(alias="usd_use_amt", description="미화사용금액")
    usd_ord_psbl_amt: str = Field(alias="usd_ord_psbl_amt", description="미화주문가능금액")
    hkd_objt_amt: str = Field(alias="hkd_objt_amt", description="홍콩달러대상금액")
    hkd_use_amt: str = Field(alias="hkd_use_amt", description="홍콩달러사용금액")
    hkd_ord_psbl_amt: str = Field(alias="hkd_ord_psbl_amt", description="홍콩달러주문가능금액")
    jpy_objt_amt: str = Field(alias="jpy_objt_amt", description="엔화대상금액")
    jpy_use_amt: str = Field(alias="jpy_use_amt", description="엔화사용금액")
    jpy_ord_psbl_amt: str = Field(alias="jpy_ord_psbl_amt", description="엔화주문가능금액")
    cny_objt_amt: str = Field(alias="cny_objt_amt", description="위안화대상금액")
    cny_use_amt: str = Field(alias="cny_use_amt", description="위안화사용금액")
    cny_ord_psbl_amt: str = Field(alias="cny_ord_psbl_amt", description="위안화주문가능금액")
    usd_ruse_objt_amt: str = Field(alias="usd_ruse_objt_amt", description="미화재사용대상금액")
    usd_ruse_amt: str = Field(alias="usd_ruse_amt", description="미화재사용금액")
    usd_ruse_ord_psbl_amt: str = Field(alias="usd_ruse_ord_psbl_amt", description="미화재사용주문가능금액")
    hkd_ruse_objt_amt: str = Field(alias="hkd_ruse_objt_amt", description="홍콩달러재사용대상금액")
    hkd_ruse_amt: str = Field(alias="hkd_ruse_amt", description="홍콩달러재사용금액")
    hkd_ruse_ord_psbl_amt: str = Field(alias="hkd_ruse_ord_psbl_amt", description="홍콩달러재사용주문가능금액")
    jpy_ruse_objt_amt: str = Field(alias="jpy_ruse_objt_amt", description="엔화재사용대상금액")
    jpy_ruse_amt: str = Field(alias="jpy_ruse_amt", description="엔화재사용금액")
    jpy_ruse_ord_psbl_amt: str = Field(alias="jpy_ruse_ord_psbl_amt", description="엔화재사용주문가능금액")
    cny_ruse_objt_amt: str = Field(alias="cny_ruse_objt_amt", description="위안화재사용대상금액")
    cny_ruse_amt: str = Field(alias="cny_ruse_amt", description="위안화재사용금액")
    cny_ruse_ord_psbl_amt: str = Field(alias="cny_ruse_ord_psbl_amt", description="위안화재사용주문가능금액")
    usd_gnrl_ord_psbl_amt: str = Field(alias="usd_gnrl_ord_psbl_amt", description="미화일반주문가능금액")
    usd_itgr_ord_psbl_amt: str = Field(alias="usd_itgr_ord_psbl_amt", description="미화통합주문가능금액")
    hkd_gnrl_ord_psbl_amt: str = Field(alias="hkd_gnrl_ord_psbl_amt", description="홍콩달러일반주문가능금액")
    hkd_itgr_ord_psbl_amt: str = Field(alias="hkd_itgr_ord_psbl_amt", description="홍콩달러통합주문가능금액")
    jpy_gnrl_ord_psbl_amt: str = Field(alias="jpy_gnrl_ord_psbl_amt", description="엔화일반주문가능금액")
    jpy_itgr_ord_psbl_amt: str = Field(alias="jpy_itgr_ord_psbl_amt", description="엔화통합주문가능금액")
    cny_gnrl_ord_psbl_amt: str = Field(alias="cny_gnrl_ord_psbl_amt", description="위안화일반주문가능금액")
    cny_itgr_ord_psbl_amt: str = Field(alias="cny_itgr_ord_psbl_amt", description="위안화통합주문가능금액")
    stck_itgr_cash20_ord_psbl_amt: str = Field(alias="stck_itgr_cash20_ord_psbl_amt", description="주식통합현금20주문가능금액")
    stck_itgr_cash30_ord_psbl_amt: str = Field(alias="stck_itgr_cash30_ord_psbl_amt", description="주식통합현금30주문가능금액")
    stck_itgr_cash40_ord_psbl_amt: str = Field(alias="stck_itgr_cash40_ord_psbl_amt", description="주식통합현금40주문가능금액")
    stck_itgr_cash50_ord_psbl_amt: str = Field(alias="stck_itgr_cash50_ord_psbl_amt", description="주식통합현금50주문가능금액")
    stck_itgr_cash60_ord_psbl_amt: str = Field(alias="stck_itgr_cash60_ord_psbl_amt", description="주식통합현금60주문가능금액")
    stck_itgr_cash100_ord_psbl_amt: str = Field(alias="stck_itgr_cash100_ord_psbl_amt", description="주식통합현금100주문가능금액")
    stck_itgr_100_ord_psbl_amt: str = Field(alias="stck_itgr_100_ord_psbl_amt", description="주식통합100주문가능금액")
    stck_itgr_fncg45_ord_psbl_amt: str = Field(alias="stck_itgr_fncg45_ord_psbl_amt", description="주식통합융자45주문가능금액")
    stck_itgr_fncg50_ord_psbl_amt: str = Field(alias="stck_itgr_fncg50_ord_psbl_amt", description="주식통합융자50주문가능금액")
    stck_itgr_fncg60_ord_psbl_amt: str = Field(alias="stck_itgr_fncg60_ord_psbl_amt", description="주식통합융자60주문가능금액")
    stck_itgr_fncg70_ord_psbl_amt: str = Field(alias="stck_itgr_fncg70_ord_psbl_amt", description="주식통합융자70주문가능금액")
    stck_itgr_stln_ord_psbl_amt: str = Field(alias="stck_itgr_stln_ord_psbl_amt", description="주식통합대주주문가능금액")
    bond_itgr_ord_psbl_amt: str = Field(alias="bond_itgr_ord_psbl_amt", description="채권통합주문가능금액")
    stck_cash_ovrs_use_amt: str = Field(alias="stck_cash_ovrs_use_amt", description="주식현금해외사용금액")
    stck_sbst_ovrs_use_amt: str = Field(alias="stck_sbst_ovrs_use_amt", description="주식대용해외사용금액")
    stck_evlu_ovrs_use_amt: str = Field(alias="stck_evlu_ovrs_use_amt", description="주식평가해외사용금액")
    stck_re_use_amt_ovrs_use_amt: str = Field(alias="stck_re_use_amt_ovrs_use_amt", description="주식재사용금액해외사용금액")
    stck_fund_rpch_ovrs_use_amt: str = Field(alias="stck_fund_rpch_ovrs_use_amt", description="주식펀드환매해외사용금액")
    stck_fncg_rdpt_ovrs_use_amt: str = Field(alias="stck_fncg_rdpt_ovrs_use_amt", description="주식융자상환해외사용금액")
    bond_re_use_ovrs_use_amt: str = Field(alias="bond_re_use_ovrs_use_amt", description="채권재사용해외사용금액")
    usd_oth_mket_use_amt: str = Field(alias="usd_oth_mket_use_amt", description="미화타시장사용금액")
    jpy_oth_mket_use_amt: str = Field(alias="jpy_oth_mket_use_amt", description="엔화타시장사용금액")
    cny_oth_mket_use_amt: str = Field(alias="cny_oth_mket_use_amt", description="위안화타시장사용금액")
    hkd_oth_mket_use_amt: str = Field(alias="hkd_oth_mket_use_amt", description="홍콩달러타시장사용금액")
    usd_re_use_oth_mket_use_amt: str = Field(alias="usd_re_use_oth_mket_use_amt", description="미화재사용타시장사용금액")
    jpy_re_use_oth_mket_use_amt: str = Field(alias="jpy_re_use_oth_mket_use_amt", description="엔화재사용타시장사용금액")
    cny_re_use_oth_mket_use_amt: str = Field(alias="cny_re_use_oth_mket_use_amt", description="위안화재사용타시장사용금액")
    hkd_re_use_oth_mket_use_amt: str = Field(alias="hkd_re_use_oth_mket_use_amt", description="홍콩달러재사용타시장사용금액")
    hgkg_cny_re_use_amt: str = Field(alias="hgkg_cny_re_use_amt", description="홍콩위안화재사용금액")
    usd_frst_bltn_exrt: str = Field(alias="usd_frst_bltn_exrt", description="미국달러최초고시환율")
    hkd_frst_bltn_exrt: str = Field(alias="hkd_frst_bltn_exrt", description="홍콩달러최초고시환율")
    jpy_frst_bltn_exrt: str = Field(alias="jpy_frst_bltn_exrt", description="일본엔화최초고시환율")
    cny_frst_bltn_exrt: str = Field(alias="cny_frst_bltn_exrt", description="중국위안화최초고시환율")


class StockIntegratedDepositBalance(BaseModel, KisHttpBody):
    """주식통합증거금 현황조회 응답"""

    output: Sequence[StockIntegratedDepositBalanceItem] = Field(default_factory=list)

class PeriodAccountingCurrentStatusItem(BaseModel):
    """기간별계좌권리현황 항목"""

    acno10: str = Field(alias="acno10")  # 계좌번호10
    rght_type_cd: str = Field(alias="rght_type_cd")  # 권리유형코드
    bass_dt: str = Field(alias="bass_dt")  # 기준일자
    rght_cblc_type_cd: str = Field(alias="rght_cblc_type_cd")  # 권리잔고유형코드
    rptt_pdno: str = Field(alias="rptt_pdno")  # 대표상품번호
    pdno: str = Field(alias="pdno")  # 상품번호
    prdt_type_cd: str = Field(alias="prdt_type_cd")  # 상품유형코드
    shtn_pdno: str = Field(alias="shtn_pdno")  # 단축상품번호
    prdt_name: str = Field(alias="prdt_name")  # 상품명
    cblc_qty: str = Field(alias="cblc_qty")  # 잔고수량
    last_alct_qty: str = Field(alias="last_alct_qty")  # 최종배정수량
    excs_alct_qty: str = Field(alias="excs_alct_qty")  # 초과배정수량
    tot_alct_qty: str = Field(alias="tot_alct_qty")  # 총배정수량
    last_ftsk_qty: str = Field(alias="last_ftsk_qty")  # 최종단수주수량
    last_alct_amt: str = Field(alias="last_alct_amt")  # 최종배정금액
    last_ftsk_chgs: str = Field(alias="last_ftsk_chgs")  # 최종단수주대금
    rdpt_prca: str = Field(alias="rdpt_prca")  # 상환원금
    dlay_int_amt: str = Field(alias="dlay_int_amt")  # 지연이자금액
    lstg_dt: str = Field(alias="lstg_dt")  # 상장일자
    sbsc_end_dt: str = Field(alias="sbsc_end_dt")  # 청약종료일자
    cash_dfrm_dt: str = Field(alias="cash_dfrm_dt")  # 현금지급일자
    rqst_qty: str = Field(alias="rqst_qty")  # 신청수량
    rqst_amt: str = Field(alias="rqst_amt")  # 신청금액
    rqst_dt: str = Field(alias="rqst_dt")  # 신청일자
    rfnd_dt: str = Field(alias="rfnd_dt")  # 환불일자
    rfnd_amt: str = Field(alias="rfnd_amt")  # 환불금액
    lstg_stqt: str = Field(alias="lstg_stqt")  # 상장주수
    tax_amt: str = Field(alias="tax_amt")  # 세금금액
    sbsc_unpr: str = Field(alias="sbsc_unpr")  # 청약단가

class PeriodAccountingCurrentStatus(BaseModel, KisHttpBody):
    """기간별계좌권리현황조회 응답"""

    output1: Sequence[PeriodAccountingCurrentStatusItem] = Field(default_factory=list)