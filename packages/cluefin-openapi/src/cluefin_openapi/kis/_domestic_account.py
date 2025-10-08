from typing import Literal, Optional

from cluefin_openapi.kis._client import Client
from cluefin_openapi.kis._domestic_account_types import (
    BuyTradableInquiry,
    StockBalance,
    StockDailySeparateConclusion,
    StockQuoteCorrection,
    StockQuoteCorrectionCancellableQty,
    StockQuoteCredit,
    StockQuoteCurrent,
)


class DomesticAccount:
    """국내주식 주문/계좌"""

    def __init__(self, client: Client):
        self.client = client

    def request_stock_quote_current(
        self,
        tr_id: Literal["TTTC0011U", "VTTC0011U", "TTTC0012U", "VTTC0012U"],
        cano: str,
        acnt_prdt_cd: str,
        pdno: str,
        ord_dvsn: Literal[
            "00",
            "01",
            "02",
            "03",
            "04",
            "05",
            "06",
            "07",
            "11",
            "12",
            "13",
            "14",
            "15",
            "16",
            "21",
            "22",
            "23",
            "24",
        ],
        ord_qty: int,
        ord_unpr: int,
        sll_type: Literal["01", "02", "05"] = "01",
        cndt_pric: Optional[int] = None,
        excg_id_dvsn_cd: Optional[Literal["KRX", "NXT", "SOR"]] = None,
    ) -> StockQuoteCurrent:
        """
        주식주문(현금)

        Args:
            tr_id: TR ID
            cano: 종합계좌번호
            acnt_prdt_cd: 계좌상품코드
            pdno: 종목코드(6자리) , ETN의 경우 7자리 입력
            ord_dvsn: 주문구분
            ord_qty: 주문수량
            ord_unpr: 주문단가, 주문단가 시장가 주문시, "0"으로 입력
            sll_type: 매도유형 (매도주문 시)
            cndt_pric: 조건가격, 스탑지정가호가 주문 (ORD_DVSN이 22) 사용 시에만 필수
            excg_id_dvsn_cd: 거래소ID구분코드

        Returns:
            StockQuoteCurrent: 주식주문(현금) 응답 객체
        """
        headers = {
            "tr_id": tr_id,
        }
        body = {
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "PDNO": pdno,
            "SLL_TYPE": sll_type,
            "ORD_DVSN": ord_dvsn,
            "ORD_QTY": ord_qty,
            "ORD_UNPR": ord_unpr,
            "CNDT_PRIC": cndt_pric,
            "EXCG_ID_DVSN_CD": excg_id_dvsn_cd,
        }

        response = self.client._post("/uapi/domestic-stock/v1/trading/order-cash", headers=headers, body=body)
        return StockQuoteCurrent.model_validate(response.json())

    def request_stock_quote_credit(
        self,
        tr_id: Literal["TTTC0051U", "TTTC0052U"],
        cano: str,
        acnt_prdt_cd: str,
        pdno: str,
        crdt_type: Literal["21", "22", "23", "24", "25", "26", "27", "28"],
        loan_dt: str,
        ord_dvsn: Literal[
            "00",
            "01",
            "02",
            "03",
            "04",
            "05",
            "06",
            "07",
            "11",
            "12",
            "13",
            "14",
            "15",
            "16",
            "21",
            "22",
            "23",
            "24",
        ],
        ord_qty: str,
        ord_unpr: str,
        rsvn_ord_yn: Optional[Literal["Y", "N"]] = None,
        emgc_ord_yn: Optional[Literal["Y", "N"]] = None,
        pgtr_dvsn: Optional[str] = None,
        lqty_tr_ngtn_dtl_no: Optional[str] = None,
        lqty_tr_agmt_no: Optional[str] = None,
        lqty_tr_ngtn_id: Optional[str] = None,
        lp_ord_yn: Optional[Literal["Y", "N"]] = None,
        mdia_odno: Optional[str] = None,
        ord_svr_dvsn_cd: Optional[str] = None,
        pgm_nmpr_stmt_dvsn_cd: Optional[str] = None,
        cvrg_slct_rson_cd: Optional[str] = None,
        cvrg_seq: Optional[str] = None,
        excg_id_dvsn_cd: Optional[Literal["KRX", "NXT", "SOR"]] = None,
        cndt_pric: Optional[str] = None,
    ) -> StockQuoteCredit:
        """
        주식주문(신용)

        Args:
            tr_id: TR ID
            cano: 종합계좌번호
            acnt_prdt_cd: 계좌상품코드
            pdno: 종목코드(6자리) , ETN의 경우 7자리 입력
            crdt_type: 신용유형
            loan_dt: 대출일자
            ord_dvsn: 주문구분
            ord_qty: 주문수량
            ord_unpr: 주문단가, 주문단가 시장가 주문시, "0"으로 입력
            rsvn_ord_yn: 예약주문여부
            emgc_ord_yn: 비상주문여부
            pgtr_dvsn: 프로그램매매구분
            lqty_tr_ngtn_dtl_no: 대량거래협상상세번호
            lqty_tr_agmt_no: 대량거래협정번호
            lqty_tr_ngtn_id: 대량거래협상자Id
            lp_ord_yn: LP주문여부
            mdia_odno: 매체주문번호
            ord_svr_dvsn_cd: 주문서버구분코드
            pgm_nmpr_stmt_dvsn_cd: 프로그램호가신고구분코드
            cvrg_slct_rson_cd: 반대매매선정사유코드
            cvrg_seq: 반대매매순번
            excg_id_dvsn_cd: 거래소ID구분코드
            cndt_pric: 조건가격, 스탑지정가호가 주문

        Returns:
            StockQuoteCredit: 주식주문(신용) 응답 객체
        """
        headers = {
            "tr_id": tr_id,
        }
        body = {
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "PDNO": pdno,
            "SLL_TYPE": "",
            "CRDT_TYPE": crdt_type,
            "LOAN_DT": loan_dt,
            "ORD_DVSN": ord_dvsn,
            "ORD_QTY": ord_qty,
            "ORD_UNPR": ord_unpr,
            "RSVN_ORD_YN": rsvn_ord_yn,
            "EMGC_ORD_YN": emgc_ord_yn,
            "PGTR_DVSN": pgtr_dvsn,
            "LQTY_TR_NGTN_DTL_NO": lqty_tr_ngtn_dtl_no,
            "LQTY_TR_AGMT_NO": lqty_tr_agmt_no,
            "LQTY_TR_NGTN_ID": lqty_tr_ngtn_id,
            "LP_ORD_YN": lp_ord_yn,
            "MDIA_ODNO": mdia_odno,
            "ORD_SVR_DVSN_CD": ord_svr_dvsn_cd,
            "PGM_NMPR_STMT_DVSN_CD": pgm_nmpr_stmt_dvsn_cd,
            "CVRG_SLCT_RSON_CD": cvrg_slct_rson_cd,
            "CVRG_SEQ": cvrg_seq,
            "EXCG_ID_DVSN_CD": excg_id_dvsn_cd,
            "CNDT_PRIC": cndt_pric,
        }
        response = self.client._post("/uapi/domestic-stock/v1/trading/order-credit", headers=headers, body=body)
        return StockQuoteCredit.model_validate(response.json())

    def request_stock_quote_correction(
        self,
        tr_id: Literal["TTTC0013U", "VTTC0013U"],
        cano: str,
        acnt_prdt_cd: str,
        krx_fwdg_ord_orgno: str,
        orgn_odno: str,
        ord_dvsn: Literal[
            "00",
            "03",
            "04",
            "05",
            "06",
            "07",
            "11",
            "12",
            "13",
            "14",
            "15",
            "16",
            "21",
            "22",
            "23",
            "24",
        ],
        rvse_cncl_dvsn_cd: Literal["01", "02"],
        ord_qty: str,
        ord_unpr: str,
        qty_all_ord_yn: Literal["Y", "N"],
        excg_id_dvsn_cd: Optional[Literal["KRX", "NXT", "SOR"]] = None,
    ) -> StockQuoteCorrection:
        """
        주식주문(정정취소)

        Args:
            tr_id: TR ID
            cano: 종합계좌번호
            acnt_prdt_cd: 계좌상품코드
            krx_fwdg_ord_orgno: 한국거래소전송주문조직번호
            orgn_odno: 원주문번호
            ord_dvsn: 주문구분
            rvse_cncl_dvsn_cd: 정정취소구분코드
            ord_qty: 주문수량
            ord_unpr: 주문단가
            qty_all_ord_yn: 잔량전부주문여부
            excg_id_dvsn_cd: 거래소ID구분코드

        Returns:
            StockQuoteCorrection: 주식정정/취소 응답 객체
        """
        headers = {
            "tr_id": tr_id,
        }
        body = {
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "KRX_FWDG_ORD_ORGNO": krx_fwdg_ord_orgno,
            "ORGN_ODNO": orgn_odno,
            "ORD_DVSN": ord_dvsn,
            "RVSE_CNCL_DVSN_CD": rvse_cncl_dvsn_cd,
            "ORD_QTY": ord_qty,
            "ORD_UNPR": ord_unpr,
            "QTY_ALL_ORD_YN": qty_all_ord_yn,
            "EXCG_ID_DVSN_CD": excg_id_dvsn_cd,
        }
        response = self.client._post("/uapi/domestic-stock/v1/trading/order-rvsecncl", headers=headers, body=body)
        return StockQuoteCorrection.model_validate(response.json())

    def get_stock_correction_cancellable_qty(
        self,
        tr_id: Literal["TTTC0084R"],
        tr_cont: str,
        cano: str,
        acnt_prdt_cd: str,
        ctx_area_fk100: str,
        ctx_area_nk100: str,
        inqr_dvsn_1: Literal["0", "1"],
        inqr_dvsn_2: Literal["0", "1", "2"],
    ) -> StockQuoteCorrectionCancellableQty:
        """
        주식정정취소가능주문조회

        Args:
            tr_id: TR ID
            tr_cont: 연속 거래 여부, (공백 : 초기 조회, N : 다음 데이터 조회 (output header의 tr_cont가 M일 경우)
            cano: 종합계좌번호
            acnt_prdt_cd: 계좌상품코드
            ctx_area_fk100: 연속조회검색조건100, '공란 : 최초 조회시는 이전 조회 Output CTX_AREA_FK100 값 : 다음페이지 조회시(2번째부터)'
            ctx_area_nk100: 연속조회키100, '공란 : 최초 조회시 이전 조회 Output CTX_AREA_NK100 값 : 다음페이지 조회시(2번째부터)'
            inqr_dvsn_1: 조회구분1, '0 주문 1 종목'
            inqr_dvsn_2: 조회구분2, '0 전체 1 매도 2 매수'

        Returns:
            StockQuoteCorrectionCancellableQty: 주식정정취소가능주문조회 응답 객체
        """
        headers = {
            "tr_id": tr_id,
            "tr_cont": tr_cont,
        }

        params = {
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "CTX_AREA_FK100": ctx_area_fk100,
            "CTX_AREA_NK100": ctx_area_nk100,
            "INQR_DVSN_1": inqr_dvsn_1,
            "INQR_DVSN_2": inqr_dvsn_2,
        }

        response = self.client._get(
            "/uapi/domestic-stock/v1/trading/inquire-psbl-rvsecncl", headers=headers, params=params
        )
        return StockQuoteCorrectionCancellableQty.model_validate(response.json())

    def get_stock_daily_separate_conclusion(
        self,
        tr_id: Literal["TTTC0081R", "CTSC9215R", "VTTC0081R", "VTSC9215R"],
        tr_cont: Literal["", "N"],
        cano: str,
        acnt_prdt_cd: str,
        inqr_strt_dt: str,
        inqr_end_dt: str,
        sll_buy_dvsn_cd: Literal["00", "01", "02"],
        ccld_dvsn: Literal["00", "01", "02"],
        inqr_dvsn: Literal["00", "01"],
        inqr_dvsn_1: Literal["", "1", "2"],
        inqr_dvsn_3: Literal["00", "01", "02", "03", "04", "05", "06", "07"],
        excg_id_dvsn_cd: Literal["KRX", "NXT", "SOR", "ALL"],
        ctx_area_fk100: str,
        ctx_area_nk100: str,
        ord_gno_brno: str = "",
        pdno: Optional[str] = None,
        odno: Optional[str] = None,
    ) -> StockDailySeparateConclusion:
        """
        주식일별주문체결조회

        Args:
            tr_id: TR ID
            tr_cont: 연속 거래 여부, (공백 : 초기 조회, N : 다음 데이터 조회 (output header의 tr_cont가 M일 경우)
            cano: 종합계좌번호
            acnt_prdt_cd: 계좌상품코드
            inqr_strt_dt: 조회시작일자, YYYYMMDD
            inqr_end_dt: 조회종료일자, YYYYMMDD
            sll_buy_dvsn_cd: 매도매수구분코드, 00 : 전체 / 01 : 매도 / 02 : 매수
            ccld_dvsn: 체결구분, '00 전체 01 체결 02 미체결'
            inqr_dvsn: 조회구분, '00 역순 01 정순'
            inqr_dvsn_1: 조회구분1, '없음: 전체 1: ELW 2: 프리보드'
            inqr_dvsn_3: 조회구분3, '00 전체 01 현금 02 신용 03 담보 04 대주 05 대여 06 자기융자신규/상환 07 유통융자신규/상환'
            excg_id_dvsn_cd: 거래소ID구분코드, 한국거래소 : KRX 대체거래소 (NXT) : NXT SOR (Smart Order Routing) : SOR ALL : 전체 ※ 모의투자는 KRX만 제공
            ctx_area_fk100: 연속조회검색조건100, '공란 : 최초 조회시는 이전 조회 Output CTX_AREA_FK100 값 : 다음페이지 조회시(2번째부터)'
            ctx_area_nk100: 연속조회키100, '공란 : 최초 조회시 이전 조회 Output CTX_AREA_NK100 값 : 다음페이지 조회시(2번째부터)'
            ord_gno_brno: str = "",
            pdno: 상품번호, 종목번호(6자리)
            odno: 주문번호, 주문시 한국투자증권 시스템에서 채번된 주문번호

        Returns:
            StockDailySeparateConclusion: 주식일별주문체결조회 응답 객체
        """
        headers = {
            "tr_id": tr_id,
            "tr_cont": tr_cont,
        }
        params = {
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "INQR_STRT_DT": inqr_strt_dt,
            "INQR_END_DT": inqr_end_dt,
            "SLL_BUY_DVSN_CD": sll_buy_dvsn_cd,
            "ORD_GNO_BRNO": ord_gno_brno,
            "CCLD_DVSN": ccld_dvsn,
            "INQR_DVSN": inqr_dvsn,
            "INQR_DVSN_1": inqr_dvsn_1,
            "INQR_DVSN_3": inqr_dvsn_3,
            "EXCG_ID_DVSN_CD": excg_id_dvsn_cd,
            "CTX_AREA_FK100": ctx_area_fk100,
            "CTX_AREA_NK100": ctx_area_nk100,
            "PDNO": pdno,
            "ODNO": odno,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/trading/inquire-daily-ccld", headers=headers, params=params
        )
        return StockDailySeparateConclusion.model_validate(response.json())

    def get_stock_balance(
        self,
        tr_id: Literal["TTTC8434R", "VTTC8434R"],
        tr_cont: Literal["", "N"],
        cano: str,
        acnt_prdt_cd: str,
        inqr_dvsn: Literal["01", "02"],
        fund_sttl_icld_yn: Literal["N", "Y"],
        prcs_dvsn: Literal["00", "01"],
        afhr_flpr_yn: Literal["N", "Y", "X"] = "N",
        ctx_area_fk100: str = "",
        ctx_area_nk100: str = "",
    ) -> StockBalance:
        """
        주식잔고조회

        Args:
            tr_id: TR ID
            tr_cont: 연속 거래 여부, (공백 : 초기 조회, N : 다음 데이터 조회 (output header의 tr_cont가 M일 경우)
            cano: 종합계좌번호
            acnt_prdt_cd: 계좌상품코드
            afhr_flpr_yn: 시간외단일가, 거래소여부
            inqr_dvsn: 조회구분
            fund_sttl_icld_yn: 펀드결제분포함여부
            prcs_dvsn: 처리구분
            ctx_area_fk100: 연속조회검색조건100, '공란 : 최초 조회시는 이전 조회 Output CTX_AREA_FK100 값 : 다음페이지 조회시(2번째부터)'
            ctx_area_nk100: 연속조회키100, '공란 : 최초 조회시 이전 조회 Output CTX_AREA_NK100 값 : 다음페이지 조회시(2번째부터

        Returns:
            StockBalance: 주식잔고조회 응답 객체
        """
        headers = {
            "tr_id": tr_id,
            "tr_cont": tr_cont,
        }
        params = {
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "AFHR_FLPR_YN": afhr_flpr_yn,
            "OFL_YN": "",
            "INQR_DVSN": inqr_dvsn,
            "UNPR_DVSN": "01",
            "FUND_STTL_ICLD_YN": fund_sttl_icld_yn,
            "FNCG_AMT_AUTO_RDPT_YN": "N",
            "PRCS_DVSN": prcs_dvsn,
            "CTX_AREA_FK100": ctx_area_fk100,
            "CTX_AREA_NK100": ctx_area_nk100,
        }

        response = self.client._get("/uapi/domestic-stock/v1/trading/inquire-balance", headers=headers, params=params)
        return StockBalance.model_validate(response.json())

    def get_buy_tradable_inquiry(
        self,
        tr_id: Literal["TTTC0802R", "VTTC0802R"],
        tr_cont: Literal["", "N"],
        cano: str,
        acnt_prdt_cd: str,
        afhr_flpr_yn: Literal["N", "Y", "X"],
        inqr_dvsn: Literal["01", "02"],
        fund_sttl_icld_yn: Literal["N", "Y"],
        prcs_dvsn: Literal["00", "01"],
        ctx_area_fk100: str = "",
        ctx_area_nk100: str = "",
    ) -> BuyTradableInquiry:
        """
        매수가능조회

        Args:
            tr_id: TR ID
            tr_cont: 연속 거래 여부, (공백 : 초기 조회, N : 다음 데이터 조회 (output header의 tr_cont가 M일 경우)
            cano: 종합계좌번호
            acnt_prdt_cd: 계좌상품코드
            afhr_flpr_yn: 시간외단일가, 거래소여부
            inqr_dvsn: 조회구분
            fund_sttl_icld_yn: 펀드결제분포함여부
            prcs_dvsn: 처리구분
            ctx_area_fk100: 연속조회검색조건100, '공란 : 최초 조회시는 이전 조회 Output CTX_AREA_FK100 값 : 다음페이지 조회시(2번째부터)'
            ctx_area_nk100: 연속조회키100, '공란 : 최초 조회시 이전 조회 Output CTX_AREA_NK100 값 : 다음페이지 조회시(2번째부터)'

        Returns:
            BuyTradableInquiry: 매수가능조회 응답 객체
        """
        headers = {
            "tr_id": tr_id,
            "tr_cont": tr_cont,
        }
        params = {
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "AFHR_FLPR_YN": afhr_flpr_yn,
            "OFL_YN": "",
            "INQR_DVSN": inqr_dvsn,
            "UNPR_DVSN": "01",
            "FUND_STTL_ICLD_YN": fund_sttl_icld_yn,
            "FNCG_AMT_AUTO_RDPT_YN": "N",
            "PRCS_DVSN": prcs_dvsn,
            "CTX_AREA_FK100": ctx_area_fk100,
            "CTX_AREA_NK100": ctx_area_nk100,
        }

        response = self.client._get(
            "/uapi/domestic-stock/v1/trading/inquire-psbl-order", headers=headers, params=params
        )
        return BuyTradableInquiry.model_validate(response.json())

    def get_sell_tradable_inquiry(self):
        """매도가능수량조회"""
        pass

    def get_new_subscription_tradable_inquiry(self):
        """신용매수가능조회"""
        pass

    def get_stock_reserve_quote(self):
        """주식예약주문"""
        pass

    def get_stock_reserve_quote_correction(self):
        """주식예약주문정정취소"""
        pass

    def get_stock_reserve_quote_inquiry(self):
        """주식예약주문조회"""
        pass

    def get_pension_fund_establishment_standard(self):
        """퇴직연금 체결기준잔고"""
        pass

    def get_pension_fund_unexecuted_history(self):
        """퇴직연금 미체결내역"""
        pass

    def get_pension_fund_buy_tradable_inquiry(self):
        """퇴직연금 매수가능조회"""
        pass

    def get_pension_fund_reserve_deposit_inquiry(self):
        """퇴직연금 예수금조회"""
        pass

    def get_pension_fund_balance(self):
        """퇴직연금 잔고조회"""
        pass

    def get_stock_balance_loss_profit(self):
        """주식잔고조회_실현손익"""
        pass

    def get_investment_account_current_status(self):
        """투자계좌자산현황조회"""
        pass

    def get_institution_separated_disclosure(self):
        """기관별순의별합산조회"""
        pass

    def get_institution_separated_sale_current_status(self):
        """기관별매매순의현황조회"""
        pass

    def get_stock_integrated_deposit_balance(self):
        """주식통합증거금 현황"""
        pass

    def get_institution_separated_accounting_current_status(self):
        """기관별계좌권리현황조회"""
        pass
