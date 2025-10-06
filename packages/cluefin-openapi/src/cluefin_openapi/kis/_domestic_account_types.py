from __future__ import annotations

from typing import Dict, Mapping, Sequence

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
    output2: StockDailySeparateConclusionItem2 = Field(default_factory=StockDailySeparateConclusionItem2)


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
