from typing import Optional, Sequence

from pydantic import BaseModel, Field

from cluefin_openapi.kis._model import KisHttpBody


class StockQuoteCurrentItem(BaseModel):
    krx_fwdg_ord_orgno: str = Field(
        title="한국거래소전송주문조직번호", max_length=5, description="주문시 한국투자증권 시스템에서 지정된 영업점코드"
    )
    odno: str = Field(title="주문번호", max_length=10, description="주문시 한국투자증권 시스템에서 채번된 주문번호")
    ord_tmd: str = Field(title="주문시각", max_length=6, description="주문시각(시분초HHMMSS)")


class StockQuoteCurrent(BaseModel, KisHttpBody):
    """해외주식 주문"""

    output: StockQuoteCurrentItem = Field(title="응답상세")


class StockQuoteCorrectionItem(BaseModel):
    krx_fwdg_ord_orgno: str = Field(
        title="한국거래소전송주문조직번호",
        max_length=5,
        alias="KRX_FWDG_ORD_ORGNO",
        description="주문시 한국투자증권 시스템에서 지정된 영업점코드",
    )
    odno: str = Field(
        title="주문번호", max_length=10, alias="ODNO", description="주문시 한국투자증권 시스템에서 채번된 주문번호"
    )
    ord_tmd: str = Field(title="주문시각", max_length=6, alias="ORD_TMD", description="주문시각(시분초HHMMSS)")


class StockQuoteCorrection(BaseModel, KisHttpBody):
    """해외주식 정정취소주문"""

    output: StockQuoteCorrectionItem = Field(title="응답상세")


class StockReserveQuoteItem(BaseModel):
    odno: str = Field(
        title="한국거래소전송주문조직번호",
        max_length=10,
        alias="ODNO",
        description="tr_id가 TTTT3016U(미국 예약 매도 주문) / TTTT3014U(미국 예약 매수 주문)인 경우만 출력",
    )
    rsvn_ord_rcit_dt: str = Field(
        title="예약주문접수일자",
        max_length=8,
        alias="RSVN_ORD_RCIT_DT",
        description="tr_id가 TTTS3013U(중국/홍콩/일본/베트남 예약 주문)인 경우만 출력",
    )
    ovrs_rsvn_odno: str = Field(
        title="해외예약주문번호",
        max_length=10,
        alias="OVRS_RSVN_ODNO",
        description="tr_id가 TTTS3013U(중국/홍콩/일본/베트남 예약 주문)인 경우만 출력",
    )


class StockReserveQuote(BaseModel, KisHttpBody):
    """해외주식 예약주문접수"""

    output: StockReserveQuoteItem = Field(title="응답상세")


class StockReserveQuoteCorrectionItem(BaseModel):
    ovrs_rsvn_odno: str = Field(title="해외예약주문번호", max_length=10, alias="OVRS_RSVN_ODNO")


class StockReserveQuoteCorrection(BaseModel, KisHttpBody):
    """해외주식 예약주문접수취소"""

    output: StockReserveQuoteCorrectionItem = Field(title="응답상세")


class BuyTradableAmountItem(BaseModel):
    tr_crcy_cd: Optional[str] = Field(title="거래통화코드", max_length=3)
    ord_psbl_frcr_amt: Optional[str] = Field(title="주문가능외화금액", max_length=21, description="18.2")
    sll_ruse_psbl_amt: Optional[str] = Field(
        title="매도재사용가능금액", max_length=21, description="가능금액 산정 시 사용"
    )
    ovrs_ord_psbl_amt: Optional[str] = Field(
        title="해외주문가능금액",
        max_length=21,
        description='- 한국투자 앱 해외주식 주문화면내 "외화" 인경우 주문가능금액',
    )
    max_ord_psbl_qty: Optional[str] = Field(
        title="최대주문가능수량",
        max_length=19,
        description='- 한국투자 앱 해외주식 주문화면내 "외화" 인경우 주문가능수량\n- 매수 시 수량단위 절사해서 사용 \n   예 : (100주단위) 545 주 -> 500 주 / (10주단위) 545 주 -> 540 주',
    )
    echm_af_ord_psbl_amt: Optional[str] = Field(
        title="환전이후주문가능금액", max_length=21, description="사용되지 않는 사항(0으로 출력)"
    )
    echm_af_ord_psbl_qty: Optional[str] = Field(
        title="환전이후주문가능수량", max_length=19, description="사용되지 않는 사항(0으로 출력)"
    )
    ord_psbl_qty: Optional[str] = Field(title="주문가능수량", max_length=10, description="22(20.1)")
    exrt: Optional[str] = Field(title="환율", max_length=22, description="25(18.6)")
    frcr_ord_psbl_amt1: Optional[str] = Field(
        title="외화주문가능금액1",
        max_length=25,
        description='- 한국투자 앱 해외주식 주문화면내 "통합" 인경우 주문가능금액',
    )
    ovrs_max_ord_psbl_qty: Optional[str] = Field(
        title="해외최대주문가능수량",
        max_length=19,
        description='- 한국투자 앱 해외주식 주문화면내 "통합" 인경우 주문가능수량\n- 매수 시 수량단위 절사해서 사용 \n   예 : (100주단위) 545 주 -> 500 주 / (10주단위) 545 주 -> 540 주',
    )


class BuyTradableAmount(BaseModel, KisHttpBody):
    """해외주식 매수가능금액조회"""

    output: BuyTradableAmountItem = Field(title="응답상세")


class StockNotConclusionHistoryItem(BaseModel):
    ord_dt: str = Field(title="주문일자", max_length=8, description="주문접수 일자")
    ord_gno_brno: str = Field(
        title="주문채번지점번호", max_length=5, description="계좌 개설 시 관리점으로 선택한 영업점의 고유번호"
    )
    odno: str = Field(title="주문번호", max_length=10, description="접수한 주문의 일련번호")
    orgn_odno: str = Field(title="원주문번호", max_length=10, description="정정 또는 취소 대상 주문의 일련번호")
    pdno: str = Field(title="상품번호", max_length=12, description="종목코드")
    prdt_name: str = Field(title="상품명", max_length=60, description="종목명")
    sll_buy_dvsn_cd: str = Field(title="매도매수구분코드", max_length=2, description="01 : 매도, 02 : 매수")
    sll_buy_dvsn_cd_name: str = Field(title="매도매수구분코드명", max_length=60, description="매수매도구분명")
    rvse_cncl_dvsn_cd: str = Field(title="정정취소구분코드", max_length=2, description="01 : 정정, 02 : 취소")
    rvse_cncl_dvsn_cd_name: str = Field(title="정정취소구분코드명", max_length=60, description="정정취소구분명")
    rjct_rson: str = Field(title="거부사유", max_length=60, description="정상 처리되지 못하고 거부된 주문의 사유")
    rjct_rson_name: str = Field(
        title="거부사유명", max_length=60, description="정상 처리되지 못하고 거부된 주문의 사유명"
    )
    ord_tmd: str = Field(title="주문시각", max_length=6, description="주문 접수 시간")
    tr_mket_name: str = Field(title="거래시장명", max_length=60)
    tr_crcy_cd: str = Field(
        title="거래통화코드",
        max_length=3,
        description="USD : 미국달러\nHKD : 홍콩달러\nCNY : 중국위안화\nJPY : 일본엔화\nVND : 베트남동",
    )
    natn_cd: str = Field(title="국가코드", max_length=3)
    natn_kor_name: str = Field(title="국가한글명", max_length=60)
    ft_ord_qty: str = Field(title="FT주문수량", max_length=10, description="주문수량")
    ft_ccld_qty: str = Field(title="FT체결수량", max_length=10, description="체결된 수량")
    nccs_qty: str = Field(title="미체결수량", max_length=10, description="미체결수량")
    ft_ord_unpr3: str = Field(title="FT주문단가3", max_length=26, description="주문가격")
    ft_ccld_unpr3: str = Field(title="FT체결단가3", max_length=26, description="체결된 가격")
    ft_ccld_amt3: str = Field(title="FT체결금액3", max_length=23, description="체결된 금액")
    ovrs_excg_cd: str = Field(
        title="해외거래소코드",
        max_length=4,
        description="NASD : 나스닥\nNYSE : 뉴욕\nAMEX : 아멕스\nSEHK : 홍콩\nSHAA : 중국상해\nSZAA : 중국심천\nTKSE : 일본\nHASE : 베트남 하노이\nVNSE : 베트남 호치민",
    )
    prcs_stat_name: str = Field(title="처리상태명", max_length=60, description='"" 공백 입력')
    loan_type_cd: str = Field(
        title="대출유형코드",
        max_length=2,
        description="00 해당사항없음\n01 자기융자일반형\n03 자기융자투자형\n05 유통융자일반형\n06 유통융자투자형\n07 자기대주\n09 유통대주\n10 현금\n11 주식담보대출\n12 수익증권담보대출\n13 ELS담보대출\n14 채권담보대출\n15 해외주식담보대출\n16 기업신용공여\n31 소액자동담보대출\n41 매도담보대출\n42 환매자금대출\n43 매입환매자금대출\n44 대여매도담보대출\n81 대차거래\n82 법인CMA론\n91 공모주청약자금대출\n92 매입자금\n93 미수론서비스\n94 대여",
    )
    loan_dt: str = Field(title="대출일자", max_length=8, description="대출 실행일자")
    usa_amk_exts_rqst_yn: str = Field(title="미국애프터마켓연장신청여부", max_length=1, description="Y/N")
    splt_buy_attr_name: str = Field(
        title="분할매수속성명",
        max_length=60,
        description="정규장 종료 주문 시에는 '정규장 종료', 시간 입력 시에는 from ~ to 시간 표시됨",
    )


class StockNotConclusion(BaseModel, KisHttpBody):
    """해외주식 미체결내역"""

    ctx_area_fk200: str = Field(title="연속조회검색조건200", max_length=200)
    ctx_area_nk200: str = Field(title="연속조회키200", max_length=200)
    output: Sequence[StockNotConclusionHistoryItem] = Field(default_factory=list)


class StockBalanceItem1(BaseModel):
    cano: str = Field(title="종합계좌번호", max_length=8)
    acnt_prdt_cd: str = Field(title="계좌상품코드", max_length=2)
    prdt_type_cd: str = Field(title="상품유형코드", max_length=3)
    ovrs_pdno: str = Field(title="해외상품번호", max_length=12)
    ovrs_item_name: str = Field(title="해외종목명", max_length=60)
    frcr_evlu_pfls_amt: str = Field(
        title="외화평가손익금액", max_length=30, description="해당 종목의 매입금액과 평가금액의 외회기준 비교 손익"
    )
    evlu_pfls_rt: str = Field(
        title="평가손익율", max_length=10, description="해당 종목의 평가손익을 기준으로 한 수익률"
    )
    pchs_avg_pric: str = Field(title="매입평균가격", max_length=23, description="해당 종목의 매수 평균 단가")
    ovrs_cblc_qty: str = Field(title="해외잔고수량", max_length=19)
    ord_psbl_qty: str = Field(title="주문가능수량", max_length=10, description="매도 가능한 주문 수량")
    frcr_pchs_amt1: str = Field(title="외화매입금액1", max_length=23, description="해당 종목의 외화 기준 매입금액")
    ovrs_stck_evlu_amt: str = Field(
        title="해외주식평가금액", max_length=32, description="해당 종목의 외화 기준 평가금액"
    )
    now_pric2: str = Field(title="현재가격2", max_length=25, description="해당 종목의 현재가")
    tr_crcy_cd: str = Field(
        title="거래통화코드",
        max_length=3,
        description="USD : 미국달러\nHKD : 홍콩달러\nCNY : 중국위안화\nJPY : 일본엔화\nVND : 베트남동",
    )
    ovrs_excg_cd: str = Field(
        title="해외거래소코드",
        max_length=4,
        description="NASD : 나스닥\nNYSE : 뉴욕\nAMEX : 아멕스\nSEHK : 홍콩\nSHAA : 중국상해\nSZAA : 중국심천\nTKSE : 일본\nHASE : 하노이거래소\nVNSE : 호치민거래소",
    )
    loan_type_cd: str = Field(
        title="대출유형코드",
        max_length=2,
        description="00 : 해당사항없음\n01 : 자기융자일반형\n03 : 자기융자투자형\n05 : 유통융자일반형\n06 : 유통융자투자형\n07 : 자기대주\n09 : 유통대주\n10 : 현금\n11 : 주식담보대출\n12 : 수익증권담보대출\n13 : ELS담보대출\n14 : 채권담보대출\n15 : 해외주식담보대출\n16 : 기업신용공여\n31 : 소액자동담보대출\n41 : 매도담보대출\n42 : 환매자금대출\n43 : 매입환매자금대출\n44 : 대여매도담보대출\n81 : 대차거래\n82 : 법인CMA론\n91 : 공모주청약자금대출\n92 : 매입자금\n93 : 미수론서비스\n94 : 대여",
    )
    loan_dt: str = Field(title="대출일자", max_length=8, description="대출 실행일자")
    expd_dt: str = Field(title="만기일자", max_length=8, description="대출 만기일자")


class StockBalanceItem2(BaseModel):
    frcr_pchs_amt1: str = Field(title="외화매입금액1", max_length=24)
    ovrs_rlzt_pfls_amt: str = Field(title="해외실현손익금액", max_length=20)
    ovrs_tot_pfls: str = Field(title="해외총손익", max_length=24)
    rlzt_erng_rt: str = Field(title="실현수익율", max_length=32)
    tot_evlu_pfls_amt: str = Field(title="총평가손익금액", max_length=32)
    tot_pftrt: str = Field(title="총수익률", max_length=32)
    frcr_buy_amt_smtl1: str = Field(title="외화매수금액합계1", max_length=25)
    ovrs_rlzt_pfls_amt2: str = Field(title="해외실현손익금액2", max_length=24)
    frcr_buy_amt_smtl2: str = Field(title="외화매수금액합계2", max_length=25)


class StockBalance(BaseModel, KisHttpBody):
    """해외주식 잔고"""

    ctx_area_fk200: str = Field(title="연속조회검색조건200", max_length=200)
    ctx_area_nk200: str = Field(title="연속조회키200", max_length=200)
    output1: Sequence[StockBalanceItem1] = Field(default_factory=list)
    output2: StockBalanceItem2 = Field(title="응답상세2")


class StockConclusionHistoryItem(BaseModel):
    ord_dt: str = Field(title="주문일자", max_length=8, description="주문접수 일자 (현지시각 기준)")
    ord_gno_brno: str = Field(
        title="주문채번지점번호", max_length=5, description="계좌 개설 시 관리점으로 선택한 영업점의 고유번호"
    )
    odno: str = Field(
        title="주문번호",
        max_length=10,
        description="접수한 주문의 일련번호 ※ 정정취소주문 시, 해당 값 odno(주문번호) 넣어서 사용",
    )
    orgn_odno: str = Field(title="원주문번호", max_length=10, description="정정 또는 취소 대상 주문의 일련번호")
    sll_buy_dvsn_cd: str = Field(title="매도매수구분코드", max_length=2, description="01 : 매도  02 : 매수")
    sll_buy_dvsn_cd_name: str = Field(title="매도매수구분코드명", max_length=60)
    rvse_cncl_dvsn: str = Field(title="정정취소구분", max_length=2, description="01 : 정정  02 : 취소")
    rvse_cncl_dvsn_name: str = Field(title="정정취소구분명", max_length=60)
    pdno: str = Field(title="상품번호", max_length=12)
    prdt_name: str = Field(title="상품명", max_length=60)
    ft_ord_qty: str = Field(title="FT주문수량", max_length=10, description="주문수량")
    ft_ord_unpr3: str = Field(title="FT주문단가3", max_length=26, description="주문가격")
    ft_ccld_qty: str = Field(title="FT체결수량", max_length=10, description="체결된 수량")
    ft_ccld_unpr3: str = Field(title="FT체결단가3", max_length=26, description="체결된 가격")
    ft_ccld_amt3: str = Field(title="FT체결금액3", max_length=23, description="체결된 금액")
    nccs_qty: str = Field(title="미체결수량", max_length=10, description="미체결수량")
    prcs_stat_name: str = Field(title="처리상태명", max_length=60, description="완료, 거부, 전송")
    rjct_rson: str = Field(title="거부사유", max_length=60, description="정상 처리되지 못하고 거부된 주문의 사유")
    rjct_rson_name: str = Field(title="거부사유명", max_length=60)
    ord_tmd: str = Field(title="주문시각", max_length=6, description="주문 접수 시간 ")
    tr_mket_name: str = Field(title="거래시장명", max_length=60)
    tr_natn: str = Field(title="거래국가", max_length=3)
    tr_natn_name: str = Field(title="거래국가명", max_length=3)
    ovrs_excg_cd: str = Field(
        title="해외거래소코드",
        max_length=4,
        description="NASD : 나스닥\nNYSE : 뉴욕\nAMEX : 아멕스\nSEHK : 홍콩 \nSHAA : 중국상해\nSZAA : 중국심천\nTKSE : 일본\nHASE : 베트남 하노이\nVNSE : 베트남 호치민",
    )
    tr_crcy_cd: str = Field(title="거래통화코드", max_length=60)
    dmst_ord_dt: str = Field(title="국내주문일자", max_length=8)
    thco_ord_tmd: str = Field(title="당사주문시각", max_length=6)
    loan_type_cd: str = Field(
        title="대출유형코드",
        max_length=2,
        description="00 : 해당사항없음\n01 : 자기융자일반형\n03 : 자기융자투자형\n05 : 유통융자일반형\n06 : 유통융자투자형\n07 : 자기대주\n09 : 유통대주\n10 : 현금\n11 : 주식담보대출\n12 : 수익증권담보대출\n13 : ELS담보대출\n14 : 채권담보대출\n15 : 해외주식담보대출\n16 : 기업신용공여\n31 : 소액자동담보대출\n41 : 매도담보대출\n42 : 환매자금대출\n43 : 매입환매자금대출\n44 : 대여매도담보대출\n81 : 대차거래\n82 : 법인CMA론\n91 : 공모주청약자금대출\n92 : 매입자금\n93 : 미수론서비스\n94 : 대여",
    )
    loan_dt: str = Field(title="대출일자", max_length=8)
    mdia_dvsn_name: str = Field(title="매체구분명", max_length=60, description="ex) OpenAPI, 모바일")
    usa_amk_exts_rqst_yn: str = Field(title="미국애프터마켓연장신청여부", max_length=1, description="Y/N")
    splt_buy_attr_name: str = Field(
        title="분할매수/매도속성명",
        max_length=60,
        description="정규장 종료 주문 시에는 '정규장 종료', 시간 입력 시에는 from ~ to 시간 표시",
    )


class StockConclusionHistory(BaseModel, KisHttpBody):
    """해외주식 주문체결내역"""

    ctx_area_fk200: str = Field(title="연속조회검색조건200", max_length=200)
    ctx_area_nk200: str = Field(title="연속조회키200", max_length=200)
    output: Sequence[StockConclusionHistoryItem] = Field(default_factory=list)


class CurrentBalanceByConclusionItem1(BaseModel):
    prdt_name: str = Field(title="상품명", max_length=60, description="종목명")
    cblc_qty13: str = Field(title="잔고수량13", max_length=32, description="결제보유수량")
    thdt_buy_ccld_qty1: str = Field(title="당일매수체결수량1", max_length=32, description="당일 매수 체결 완료 수량")
    thdt_sll_ccld_qty1: str = Field(title="당일매도체결수량1", max_length=32, description="당일 매도 체결 완료 수량")
    ccld_qty_smtl1: str = Field(title="체결수량합계1", max_length=32, description="체결기준 현재 보유수량")
    ord_psbl_qty1: str = Field(title="주문가능수량1", max_length=32, description="주문 가능한 주문 수량")
    frcr_pchs_amt: str = Field(title="외화매입금액", max_length=29, description="해당 종목의 외화 기준 매입금액")
    frcr_evlu_amt2: str = Field(title="외화평가금액2", max_length=30, description="해당 종목의 외화 기준 평가금액")
    evlu_pfls_amt2: str = Field(
        title="평가손익금액2", max_length=31, description="해당 종목의 매입금액과 평가금액의 외회기준 비교 손익"
    )
    evlu_pfls_rt1: str = Field(
        title="평가손익율1", max_length=32, description="해당 종목의 평가손익을 기준으로 한 수익률"
    )
    pdno: str = Field(title="상품번호", max_length=12, description="종목코드")
    bass_exrt: str = Field(title="기준환율", max_length=31, description="원화 평가 시 적용 환율")
    buy_crcy_cd: str = Field(
        title="매수통화코드",
        max_length=3,
        description="USD : 미국달러\nHKD : 홍콩달러\nCNY : 중국위안화\nJPY : 일본엔화\nVND : 베트남동",
    )
    ovrs_now_pric1: str = Field(title="해외현재가격1", max_length=29, description="해당 종목의 현재가")
    avg_unpr3: str = Field(title="평균단가3", max_length=29, description="해당 종목의 매수 평균 단가")
    tr_mket_name: str = Field(title="거래시장명", max_length=60, description="해당 종목의 거래시장명")
    natn_kor_name: str = Field(title="국가한글명", max_length=60, description="거래 국가명")
    pchs_rmnd_wcrc_amt: str = Field(title="매입잔액원화금액", max_length=19)
    thdt_buy_ccld_frcr_amt: str = Field(
        title="당일매수체결외화금액", max_length=30, description="당일 매수 외화금액 (Type: Object X String O)"
    )
    thdt_sll_ccld_frcr_amt: str = Field(title="당일매도체결외화금액", max_length=30, description="당일 매도 외화금액")
    unit_amt: str = Field(title="단위금액", max_length=19)
    std_pdno: str = Field(title="표준상품번호", max_length=12)
    prdt_type_cd: str = Field(title="상품유형코드", max_length=3)
    scts_dvsn_name: str = Field(title="유가증권구분명", max_length=60)
    loan_rmnd: str = Field(title="대출잔액", max_length=19, description="대출 미상환 금액")
    loan_dt: str = Field(title="대출일자", max_length=8, description="대출 실행일자")
    loan_expd_dt: str = Field(title="대출만기일자", max_length=8, description="대출 만기일자")
    ovrs_excg_cd: str = Field(
        title="해외거래소코드",
        max_length=4,
        description="NASD : 나스닥\nNYSE : 뉴욕\nAMEX : 아멕스\nSEHK : 홍콩\nSHAA : 중국상해\nSZAA : 중국심천\nTKSE : 일본\nHASE : 하노이거래소\nVNSE : 호치민거래소",
    )
    item_lnkg_excg_cd: str = Field(title="종목연동거래소코드", max_length=4)


class CurrentBalanceByConclusionItem2(BaseModel):
    crcy_cd: str = Field(title="통화코드", max_length=3)
    crcy_cd_name: str = Field(title="통화코드명", max_length=60)
    frcr_buy_amt_smtl: str = Field(
        title="외화매수금액합계", max_length=29, description="해당 통화로 매수한 종목 전체의 매수금액"
    )
    frcr_sll_amt_smtl: str = Field(
        title="외화매도금액합계", max_length=29, description="해당 통화로 매도한 종목 전체의 매수금액"
    )
    frcr_dncl_amt_2: str = Field(title="외화예수금액2", max_length=29, description="외화로 표시된 외화사용가능금액")
    frst_bltn_exrt: str = Field(title="최초고시환율", max_length=31)
    frcr_buy_mgn_amt: str = Field(title="외화매수증거금액", max_length=31, description="매수증거금으로 사용된 외화금액")
    frcr_etc_mgna: str = Field(title="외화기타증거금", max_length=31)
    frcr_drwg_psbl_amt_1: str = Field(title="외화출금가능금액1", max_length=29, description="출금가능한 외화금액")
    frcr_evlu_amt2: str = Field(title="출금가능원화금액", max_length=29, description="출금가능한 원화금액")
    acpl_cstd_crcy_yn: str = Field(title="현지보관통화여부", max_length=1)
    nxdy_frcr_drwg_psbl_amt: str = Field(title="익일외화출금가능금액", max_length=31)
    pchs_amt_smtl: str = Field(
        title="매입금액합계", max_length=19, description="해외유가증권 매수금액의 원화 환산 금액"
    )
    evlu_amt_smtl: str = Field(
        title="평가금액합계", max_length=19, description="해외유가증권 평가금액의 원화 환산 금액"
    )
    evlu_pfls_amt_smtl: str = Field(
        title="평가손익금액합계", max_length=19, description="해외유가증권 평가손익의 원화 환산 금액"
    )
    dncl_amt: str = Field(title="예수금액", max_length=19)
    cma_evlu_amt: str = Field(title="CMA평가금액", max_length=19)
    tot_dncl_amt: str = Field(title="총예수금액", max_length=19)
    etc_mgna: str = Field(title="기타증거금", max_length=19)
    wdrw_psbl_tot_amt: str = Field(title="인출가능총금액", max_length=19)
    frcr_evlu_tota: str = Field(title="외화평가총액", max_length=19)
    evlu_erng_rt1: str = Field(title="평가수익율1", max_length=31)
    pchs_amt_smtl_amt: str = Field(title="매입금액합계금액", max_length=19)
    evlu_amt_smtl_amt: str = Field(title="평가금액합계금액", max_length=19)
    tot_evlu_pfls_amt: str = Field(title="총평가손익금액", max_length=31)
    tot_asst_amt: str = Field(title="총자산금액", max_length=19)
    buy_mgn_amt: str = Field(title="매수증거금액", max_length=19)
    mgna_tota: str = Field(title="증거금총액", max_length=19)
    frcr_use_psbl_amt: str = Field(title="외화사용가능금액", max_length=20)
    ustl_sll_amt_smtl: str = Field(title="미결제매도금액합계", max_length=19)
    ustl_buy_amt_smtl: str = Field(title="미결제매수금액합계", max_length=19)
    tot_frcr_cblc_smtl: str = Field(title="총외화잔고합계", max_length=29)
    tot_loan_amt: str = Field(title="총대출금액", max_length=19)


class CurrentBalanceByConclusion(BaseModel, KisHttpBody):
    """해외주식 체결기준현재잔고"""

    output1: Sequence[CurrentBalanceByConclusionItem1] = Field(default_factory=list)
    output2: Sequence[CurrentBalanceByConclusionItem2] = Field(default_factory=list)


class ReserveOrdersItem(BaseModel):
    cncl_yn: Optional[str] = Field(title="취소여부", max_length=1)
    rsvn_ord_rcit_dt: Optional[str] = Field(title="예약주문접수일자", max_length=8)
    ovrs_rsvn_odno: Optional[str] = Field(title="해외예약주문번호", max_length=10)
    ord_dt: Optional[str] = Field(title="주문일자", max_length=8)
    ord_gno_brno: Optional[str] = Field(title="주문채번지점번호", max_length=5)
    odno: Optional[str] = Field(title="주문번호", max_length=10)
    sll_buy_dvsn_cd: Optional[str] = Field(title="매도매수구분코드", max_length=2)
    sll_buy_dvsn_name: Optional[str] = Field(title="매도매수구분명", max_length=4)
    ovrs_rsvn_ord_stat_cd: Optional[str] = Field(title="해외예약주문상태코드", max_length=2)
    ovrs_rsvn_ord_stat_cd_name: Optional[str] = Field(title="해외예약주문상태코드명", max_length=60)
    pdno: Optional[str] = Field(title="상품번호", max_length=12)
    prdt_type_cd: Optional[str] = Field(title="상품유형코드", max_length=3)
    prdt_name: Optional[str] = Field(title="상품명", max_length=60)
    ord_rcit_tmd: Optional[str] = Field(title="주문접수시각", max_length=6)
    ord_fwdg_tmd: Optional[str] = Field(title="주문전송시각", max_length=6)
    tr_dvsn_name: Optional[str] = Field(title="거래구분명", max_length=60)
    ovrs_excg_cd: Optional[str] = Field(title="해외거래소코드", max_length=4)
    tr_mket_name: Optional[str] = Field(title="거래시장명", max_length=60)
    ord_stfno: Optional[str] = Field(title="주문직원번호", max_length=6)
    ft_ord_qty: Optional[str] = Field(title="FT주문수량", max_length=10)
    ft_ord_unpr3: Optional[str] = Field(title="FT주문단가3", max_length=27)
    ft_ccld_qty: Optional[str] = Field(title="FT체결수량", max_length=10)
    nprc_rson_text: Optional[str] = Field(title="미처리사유내용", max_length=500)
    splt_buy_attr_name: Optional[str] = Field(
        title="분할매수속성명",
        max_length=60,
        description="정규장 종료 주문 시에는 '정규장 종료', 시간 입력 시에는 from ~ to 시간 표시",
    )


class ReserveOrders(BaseModel, KisHttpBody):
    """해외주식 예약주문조회"""

    ctx_area_fk200: str = Field(title="연속조회검색조건200", max_length=200)
    ctx_area_nk200: str = Field(title="연속조회키200", max_length=200)
    output: ReserveOrdersItem = Field(title="응답상세")


class BalanceBySettlementItem1(BaseModel):
    pdno: str = Field(title="상품번호", max_length=12)
    prdt_name: str = Field(title="상품명", max_length=60)
    cblc_qty13: str = Field(title="잔고수량13", max_length=238)
    ord_psbl_qty1: str = Field(title="주문가능수량1", max_length=238)
    avg_unpr3: str = Field(title="평균단가3", max_length=244)
    ovrs_now_pric1: str = Field(title="해외현재가격1", max_length=235)
    frcr_pchs_amt: str = Field(title="외화매입금액", max_length=235)
    frcr_evlu_amt2: str = Field(title="외화평가금액2", max_length=236)
    evlu_pfls_amt2: str = Field(title="평가손익금액2", max_length=255)
    bass_exrt: str = Field(title="기준환율", max_length=238)
    oprt_dtl_dtime: str = Field(title="조작상세일시", max_length=17)
    buy_crcy_cd: str = Field(title="매수통화코드", max_length=3)
    thdt_sll_ccld_qty1: str = Field(title="당일매도체결수량1", max_length=238)
    thdt_buy_ccld_qty1: str = Field(title="당일매수체결수량1", max_length=238)
    evlu_pfls_rt1: str = Field(title="평가손익율1", max_length=238)
    tr_mket_name: str = Field(title="거래시장명", max_length=60)
    natn_kor_name: str = Field(title="국가한글명", max_length=60)
    std_pdno: str = Field(title="표준상품번호", max_length=12)
    mgge_qty: str = Field(title="담보수량", max_length=19)
    loan_rmnd: str = Field(title="대출잔액", max_length=19)
    prdt_type_cd: str = Field(title="상품유형코드", max_length=3)
    ovrs_excg_cd: str = Field(title="해외거래소코드", max_length=4)
    scts_dvsn_name: str = Field(title="유가증권구분명", max_length=60)
    ldng_cblc_qty: str = Field(title="대여잔고수량", max_length=19)


class BalanceBySettlementItem2(BaseModel):
    crcy_cd: str = Field(title="통화코드", max_length=3)
    crcy_cd_name: str = Field(title="통화코드명", max_length=60)
    frcr_dncl_amt_2: str = Field(title="외화예수금액2", max_length=236)
    frst_bltn_exrt: str = Field(title="최초고시환율", max_length=238)
    frcr_evlu_amt2: str = Field(title="외화평가금액2", max_length=236)
    pchs_amt_smtl_amt: str = Field(title="매입금액합계금액", max_length=19)
    tot_evlu_pfls_amt: str = Field(title="총평가손익금액", max_length=238)
    evlu_erng_rt1: str = Field(title="평가수익율1", max_length=201)
    tot_dncl_amt: str = Field(title="총예수금액", max_length=19)
    wcrc_evlu_amt_smtl: str = Field(title="원화평가금액합계", max_length=236)
    tot_asst_amt2: str = Field(title="총자산금액2", max_length=236)
    frcr_cblc_wcrc_evlu_amt_smtl: str = Field(title="외화잔고원화평가금액합계", max_length=236)
    tot_loan_amt: str = Field(title="총대출금액", max_length=19)
    tot_ldng_evlu_amt: str = Field(title="총대여평가금액", max_length=9)


class BalanceBySettlement(BaseModel, KisHttpBody):
    """해외주식 결제기준잔고"""

    output1: Sequence[BalanceBySettlementItem1] = Field(default_factory=list)
    output2: Sequence[BalanceBySettlementItem2] = Field(default_factory=list)


class DailyTransactionHistoryItem(BaseModel):
    trad_dt: str = Field(title="매매일자", max_length=8)
    sttl_dt: str = Field(title="결제일자", max_length=8)
    sll_buy_dvsn_cd: str = Field(title="매도매수구분코드", max_length=2)
    sll_buy_dvsn_name: str = Field(title="매도매수구분명", max_length=4)
    pdno: str = Field(title="상품번호", max_length=12)
    ovrs_item_name: str = Field(title="해외종목명", max_length=60)
    ccld_qty: str = Field(title="체결수량", max_length=10)
    amt_unit_ccld_qty: str = Field(title="금액단위체결수량", max_length=188)
    ft_ccld_unpr2: str = Field(title="FT체결단가2", max_length=238)
    ovrs_stck_ccld_unpr: str = Field(title="해외주식체결단가", max_length=238)
    tr_frcr_amt2: str = Field(title="거래외화금액2", max_length=236)
    tr_amt: str = Field(title="거래금액", max_length=19)
    frcr_excc_amt_1: str = Field(title="외화정산금액1", max_length=236)
    wcrc_excc_amt: str = Field(title="원화정산금액", max_length=19)
    dmst_frcr_fee1: str = Field(title="국내외화수수료1", max_length=235)
    frcr_fee1: str = Field(title="외화수수료1", max_length=236)
    dmst_wcrc_fee: str = Field(title="국내원화수수료", max_length=19)
    ovrs_wcrc_fee: str = Field(title="해외원화수수료", max_length=19)
    crcy_cd: str = Field(title="통화코드", max_length=3)
    std_pdno: str = Field(title="표준상품번호", max_length=12)
    erlm_exrt: str = Field(title="등록환율", max_length=238)
    loan_dvsn_cd: str = Field(title="대출구분코드", max_length=2)
    loan_dvsn_name: str = Field(title="대출구분명", max_length=60)
    output2: str = Field(title="응답상세")
    frcr_buy_amt_smtl: str = Field(title="외화매수금액합계", max_length=236)
    frcr_sll_amt_smtl: str = Field(title="외화매도금액합계", max_length=236)
    dmst_fee_smtl: str = Field(title="국내수수료합계", max_length=256)
    ovrs_fee_smtl: str = Field(title="해외수수료합계", max_length=236)


class DailyTransactionHistory(BaseModel, KisHttpBody):
    """해외주식 일별거래내역"""

    ctx_area_fk200: str = Field(title="연속조회검색조건200", max_length=200)
    ctx_area_nk200: str = Field(title="연속조회키200", max_length=200)
    output: Sequence[DailyTransactionHistoryItem] = Field(default_factory=list)


class PeriodProfitLossItem1(BaseModel):
    trad_day: str = Field(title="매매일", max_length=8)
    ovrs_pdno: str = Field(title="해외상품번호", max_length=12)
    ovrs_item_name: str = Field(title="해외종목명", max_length=60)
    slcl_qty: str = Field(title="매도청산수량", max_length=10)
    pchs_avg_pric: str = Field(title="매입평균가격", max_length=184)
    frcr_pchs_amt1: str = Field(title="외화매입금액1", max_length=185)
    avg_sll_unpr: str = Field(title="평균매도단가", max_length=238)
    frcr_sll_amt_smtl1: str = Field(title="외화매도금액합계1", max_length=186)
    stck_sll_tlex: str = Field(title="주식매도제비용", max_length=184)
    ovrs_rlzt_pfls_amt: str = Field(title="해외실현손익금액", max_length=145)
    pftrt: str = Field(title="수익률", max_length=238)
    exrt: str = Field(title="환율", max_length=201)
    ovrs_excg_cd: str = Field(title="해외거래소코드", max_length=4)
    frst_bltn_exrt: str = Field(title="최초고시환율", max_length=238)


class PeriodProfitLossItem2(BaseModel):
    stck_sll_amt_smtl: str = Field(
        title="주식매도금액합계",
        max_length=184,
        description="WCRC_FRCR_DVSN_CD(원화외화구분코드)가 01(외화)이고 OVRS_EXCG_CD(해외거래소코드)가 공란(전체)인 경우 출력값 무시",
    )
    stck_buy_amt_smtl: str = Field(
        title="주식매수금액합계",
        max_length=184,
        description="WCRC_FRCR_DVSN_CD(원화외화구분코드)가 01(외화)이고 OVRS_EXCG_CD(해외거래소코드)가 공란(전체)인 경우 출력값 무시",
    )
    smtl_fee1: str = Field(
        title="합계수수료1",
        max_length=138,
        description="WCRC_FRCR_DVSN_CD(원화외화구분코드)가 01(외화)이고 OVRS_EXCG_CD(해외거래소코드)가 공란(전체)인 경우 출력값 무시",
    )
    excc_dfrm_amt: str = Field(
        title="정산지급금액",
        max_length=205,
        description="WCRC_FRCR_DVSN_CD(원화외화구분코드)가 01(외화)이고 OVRS_EXCG_CD(해외거래소코드)가 공란(전체)인 경우 출력값 무시",
    )
    ovrs_rlzt_pfls_tot_amt: str = Field(
        title="해외실현손익총금액",
        max_length=145,
        description="WCRC_FRCR_DVSN_CD(원화외화구분코드)가 01(외화)이고 OVRS_EXCG_CD(해외거래소코드)가 공란(전체)인 경우 출력값 무시",
    )
    tot_pftrt: str = Field(title="총수익률", max_length=238)
    bass_dt: str = Field(title="기준일자", max_length=8)
    exrt: str = Field(title="환율", max_length=201)


class PeriodProfitLoss(BaseModel, KisHttpBody):
    """해외주식 기간손익"""

    output: Sequence[PeriodProfitLossItem1] = Field(default_factory=list)
    output2: PeriodProfitLossItem2 = Field(title="응답상세2")


class MarginAggregateItem(BaseModel):
    natn_name: str = Field(title="국가명", max_length=60)
    crcy_cd: str = Field(title="통화코드", max_length=3)
    frcr_dncl_amt1: str = Field(title="외화예수금액", max_length=186)
    ustl_buy_amt: str = Field(title="미결제매수금액", max_length=182)
    ustl_sll_amt: str = Field(title="미결제매도금액", max_length=182)
    frcr_rcvb_amt: str = Field(title="외화미수금액", max_length=182)
    frcr_mgn_amt: str = Field(title="외화증거금액", max_length=186)
    frcr_gnrl_ord_psbl_amt: str = Field(title="외화일반주문가능금액", max_length=182)
    frcr_ord_psbl_amt1: str = Field(title="외화주문가능금액", max_length=186, description="원화주문가능환산금액")
    itgr_ord_psbl_amt: str = Field(title="통합주문가능금액", max_length=182)
    bass_exrt: str = Field(title="기준환율", max_length=238)


class MarginAggregate(BaseModel, KisHttpBody):
    """해외증거금 통합변조회"""

    output: Sequence[MarginAggregateItem] = Field(default_factory=list)


class OrderAfterDayTimeItem(BaseModel):
    krx_fwdg_ord_orgno: str = Field(
        title="한국거래소전송주문조직번호", max_length=5, description="주문시 한국투자증권 시스템에서 지정된 영업점코드"
    )
    odno: str = Field(title="주문번호", max_length=10, description="주문시 한국투자증권 시스템에서 채번된 주문번호")
    ord_tmd: str = Field(title="주문시각", max_length=6, description="주문시각(시분초HHMMSS)")


class OrderAfterDayTime(BaseModel, KisHttpBody):
    """해외주식 미국주간주문"""

    output: OrderAfterDayTimeItem = Field(title="응답상세")


class CorrectAfterDayTimeItem(BaseModel):
    krx_fwdg_ord_orgno: str = Field(
        title="한국거래소전송주문조직번호", max_length=5, description="주문시 한국투자증권 시스템에서 지정된 영업점코드"
    )
    odno: str = Field(title="주문번호", max_length=10, description="주문시 한국투자증권 시스템에서 채번된 주문번호")
    ord_tmd: str = Field(title="주문시각", max_length=6, description="주문시각(시분초HHMMSS)")


class CorrectAfterDayTime(BaseModel, KisHttpBody):
    """해외주식 미국주간정정취소"""

    output: CorrectAfterDayTimeItem = Field(title="응답상세")


class LimitOrderNumberItem(BaseModel):
    odno: str = Field(title="주문번호", max_length=10)
    trad_dvsn_name: str = Field(title="매매구분명", max_length=60)
    pdno: str = Field(title="상품번호", max_length=12)
    item_name: str = Field(title="종목명", max_length=60)
    ft_ord_qty: str = Field(title="FT주문수량", max_length=4)
    ft_ord_unpr3: str = Field(title="FT주문단가", max_length=8)
    splt_buy_attr_name: str = Field(title="분할매수속성명", max_length=60)
    ft_ccld_qty: str = Field(title="FT체결수량", max_length=4)
    ord_gno_brno: Optional[str] = Field(title="주문채번지점번호", max_length=5)
    rt_cd: str = Field(title="성공 실패 여부", max_length=1, description="0 : 성공 0 이외의 값 : 실패")
    msg_cd: str = Field(title="응답코드", max_length=8)
    msg1: str = Field(title="응답메세지", max_length=80)
    ctx_area_fk200: str = Field(title="연속조회검색조건200", max_length=200)
    ctx_area_nk200: str = Field(title="연속조회키200", max_length=200)


class LimitOrderNumber(BaseModel, KisHttpBody):
    """해외주식 지정가주문번호조회"""

    output: Sequence[LimitOrderNumberItem] = Field(default_factory=list)


class LimitOrderConclusionHistoryItem1(BaseModel):
    ccld_seq: str = Field(title="체결순번", max_length=4)
    ccld_btwn: str = Field(title="체결시간", max_length=6, description="HHMMSS")
    pdno: str = Field(title="상품번호", max_length=12)
    item_name: str = Field(title="종목명", max_length=60)
    ft_ccld_qty: Optional[str] = Field(title="FT체결수량", max_length=4)
    ft_ccld_unpr3: str = Field(title="FT체결단가", max_length=8)
    ft_ccld_amt3: Optional[str] = Field(title="FT체결금액", max_length=8)


class LimitOrderConclusionHistoryItem2(BaseModel):
    odno: str = Field(title="주문번호", max_length=10)
    trad_dvsn_name: str = Field(title="매매구분명", max_length=60)
    pdno: str = Field(title="상품번호", max_length=12)
    item_name: str = Field(title="종목명", max_length=60)
    ft_ord_qty: str = Field(title="FT주문수량", max_length=4)
    ft_ord_unpr3: str = Field(title="FT주문단가", max_length=8)
    ord_tmd: str = Field(title="주문시각", max_length=6)
    splt_buy_attr_name: str = Field(title="분할매수속성명", max_length=60)
    ft_ccld_qty: str = Field(title="FT체결수량", max_length=4)
    tr_crcy: str = Field(title="거래통화", max_length=3)
    ft_ccld_unpr3: str = Field(title="FT체결단가", max_length=8)
    ft_ccld_amt3: str = Field(title="FT체결금액", max_length=8)
    ccld_cnt: str = Field(title="체결건수", max_length=4)


class LimitOrderExecutionHistory(BaseModel, KisHttpBody):
    """해외주식 지정가체결내역조회"""

    output1: Sequence[LimitOrderConclusionHistoryItem1] = Field(default_factory=list)
    output2: Sequence[LimitOrderConclusionHistoryItem2] = Field(alias="output3", default_factory=list)
