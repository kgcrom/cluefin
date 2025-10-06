from typing import Literal, Optional

from cluefin_openapi.kis._client import Client
from cluefin_openapi.kis._domestic_account_types import (
    StockQuoteCredit,
    StockQuoteCurrent,
)


class DomesticAccount:
    """국내주식 주문/계좌"""

    def __init__(self, client: Client):
        self.client = client

    def get_stock_quote_current(
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

        response = self.client.post("/uapi/domestic-stock/v1/trading/order-cash", headers=headers, body=body)
        return StockQuoteCurrent(**response)

    def get_stock_quote_credit(
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
        response = self.client.post("/uapi/domestic-stock/v1/trading/order-credit", headers=headers, body=body)
        return StockQuoteCredit(**response)

    def get_stock_quote_correction(self):
        """주식주문(정정취소)"""
        pass

    def get_stock_correction_cancellable_qty(self):
        """주식정정취소가능주문조회"""
        pass

    def get_stock_daily_separate_conclusion(self):
        """주식일별주문체결조회"""
        pass

    def get_stock_balance(self):
        """주식잔고조회"""
        pass

    def get_buy_tradable_inquiry(self):
        """매수가능조회"""
        pass

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
