from typing import Literal, Optional

from cluefin_openapi.kis._client import Client
from cluefin_openapi.kis._domestic_account_types import (
    BuyTradableInquiry,
    CreditTradableInquiry,
    InvestmentAccountCurrentStatus,
    PensionBalanceInquiry,
    PensionBuyTradableInquiry,
    PensionConclusionBalance,
    PensionNotConclusionHistory,
    PensionReserveDepositInquiry,
    PeriodAccountingCurrentStatus,
    PeriodProfitSummary,
    PeriodTradingProfitStatus,
    SellTradableInquiry,
    StockBalance,
    StockBalanceLossProfit,
    StockDailySeparateConclusion,
    StockIntegratedDepositBalance,
    StockQuoteCorrection,
    StockQuoteCorrectionCancellableQty,
    StockQuoteCredit,
    StockQuoteCurrent,
    StockReserveQuote,
    StockReserveQuoteCorrection,
    StockReserveQuoteInquiry,
)
from cluefin_openapi.kis._model import KisHttpBody, KisHttpHeader, KisHttpResponse


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
    ) -> KisHttpResponse[StockQuoteCurrent]:
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
        if response.status_code != 200:
            raise Exception(f"Error fetching stock quote current: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockQuoteCurrent.model_validate(response.json())

        return KisHttpResponse(header=header, body=body)

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
    ) -> KisHttpResponse[StockQuoteCredit]:
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
            KisHttpResponse[StockQuoteCredit]: 주식주문(신용) 응답 객체
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
        if response.status_code != 200:
            raise Exception(f"Error fetching stock quote credit: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockQuoteCredit.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

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
    ) -> KisHttpResponse[StockQuoteCorrection]:
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
            KisHttpResponse[StockQuoteCorrection]: 주식정정/취소 응답 객체
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
        if response.status_code != 200:
            raise Exception(f"Error fetching stock quote correction: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockQuoteCorrection.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

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
    ) -> KisHttpResponse[StockQuoteCorrectionCancellableQty]:
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
            KisHttpResponse[StockQuoteCorrectionCancellableQty]: 주식정정취소가능주문조회 응답 객체
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
        if response.status_code != 200:
            raise Exception(f"Error fetching stock correction cancellable qty: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockQuoteCorrectionCancellableQty.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

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
    ) -> KisHttpResponse[StockDailySeparateConclusion]:
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
            KisHttpResponse[StockDailySeparateConclusion]: 주식일별주문체결조회 응답 객체
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
        if response.status_code != 200:
            raise Exception(f"Error fetching stock daily separate conclusion: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockDailySeparateConclusion.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

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
    ) -> KisHttpResponse[StockBalance]:
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
            KisHttpResponse[StockBalance]: 주식잔고조회 응답 객체
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
        if response.status_code != 200:
            raise Exception(f"Error fetching stock balance: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockBalance.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

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
    ) -> KisHttpResponse[BuyTradableInquiry]:
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
            KisHttpResponse[BuyTradableInquiry]: 매수가능조회 응답 객체
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
        if response.status_code != 200:
            raise Exception(f"Error fetching buy tradable inquiry: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = BuyTradableInquiry.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_sell_tradable_inquiry(
        self,
        cano: str,
        acnt_prdt_cd: str,
        pdno: str,
    ) -> KisHttpResponse[SellTradableInquiry]:
        """
        매도가능수량조회

        Args:
            cano: 종합계좌번호
            acnt_prdt_cd: 계좌상품코드
            pdno: 종목코드(6자리) , ETN의 경우 7자리 입력

        Returns:
            KisHttpResponse[SellTradableInquiry]: 매도가능수량조회 응답 객체
        """
        headers = {
            "tr_id": "TTTC8408R",
        }
        params = {
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "PDNO": pdno,
        }
        response = self.client._get("/uapi/domestic-stock/v1/trading/inquire-psbl-sell", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching sell tradable inquiry: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = SellTradableInquiry.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_credit_tradable_inquiry(
        self,
        cano: str,
        acnt_prdt_cd: str,
        pdno: str,
        ord_unpr: str,
        ord_dvsn: Literal[
            "00",
            "01",
            "02",
            "03",
            "04",
            "05",
            "06",
            "07",
        ],
        crdt_type: Literal["21", "22", "23", "24", "25", "26", "27", "28"],
        cma_evlu_amt_icld_yn: Literal["Y", "N"],
        ovrs_icld_yn: Literal["Y", "N"],
    ) -> KisHttpResponse[CreditTradableInquiry]:
        """
        신용매수가능조회

        Args:
            cano: 종합계좌번호
            acnt_prdt_cd: 계좌상품코드
            pdno: 종목코드(6자리) , ETN의 경우 7자리 입력
            ord_unpr: 주문단가, 주문단가 시장가 주문시, "0"으로 입력
            ord_dvsn: 주문구분 (00 : 지정가, 01 : 시장가, 02 : 조건부지정가, 03 : 최유리지정가, 04 : 최우선지정가, 05 : 장전 시간외, 06 : 장후 시간외, 07 : 시간외 단일가 등)
            crdt_type: 신용유형 (21 : 자기융자신규, 23 : 유통융자신규, 26 : 유통대주상환, 28 : 자기대주상환, 25 : 자기융자상환, 27 : 유통융자상환, 22 : 유통대주신규, 24 : 자기대주신규)
            cma_evlu_amt_icld_yn: CMA평가금액포함여부 (Y/N)
            ovrs_icld_yn: 해외포함여부 (Y/N)

        Returns:
            KisHttpResponse[CreditTradableInquiry]: 신용매수가능조회 응답 객체
        """
        headers = {
            "tr_id": "TTTC8909R",
        }
        params = {
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "PDNO": pdno,
            "ORD_UNPR": ord_unpr,
            "ORD_DVSN": ord_dvsn,
            "CRDT_TYPE": crdt_type,
            "CMA_EVLU_AMT_ICLD_YN": cma_evlu_amt_icld_yn,
            "OVRS_ICLD_YN": ovrs_icld_yn,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/trading/inquire-credit-psamount", headers=headers, params=params
        )
        if response.status_code != 200:
            raise Exception(f"Error fetching credit tradable inquiry: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = CreditTradableInquiry.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def request_stock_reserve_quote(
        self,
        cano: str,
        acnt_prdt_cd: str,
        pdno: str,
        ord_qty: int,
        ord_unpr: int,
        sll_buy_dvsn_cd: Literal["01", "02"],
        ord_dvsn_cd: Literal["00", "01", "02", "05"],
        ord_objt_cblc_dvsn_cd: Literal["10", "12", "14", "21", "22", "23", "24", "25", "26", "27", "28"],
        loan_dt: Optional[str] = None,
        rsvn_ord_end_dt: Optional[str] = None,
        ldng_dt: Optional[str] = None,
    ) -> KisHttpResponse[StockReserveQuote]:
        """
        주식예약주문

        Args:
            cano: 종합계좌번호
            acnt_prdt_cd: 계좌상품코드
            pdno: 종목코드(6자리) , ETN의 경우 7자리 입력
            ord_qty: 주문수량
            ord_unpr: 주문단가, 주문단가 시장가 주문시, "0"으로 입력
            sll_buy_dvsn_cd: 매도매수구분코드 (01 : 매도, 02 : 매수)
            ord_dvsn_cd: 주문구분코드 (00 : 지정가, 01 : 시장가, 02 : 조건부지정가, 05 : 장전 시간외)
            ord_objt_cblc_dvsn_cd: 주문대상잔고구분코드
            loan_dt: 대출일자
            rsvn_ord_end_dt: 예약주문종료일자 (YYYYMMDD) 현재 일자보다 이후로 설정해야 함
            ldng_dt: 대여일자

        Returns:
            KisHttpResponse[StockReserveQuote]: 주식예약주문 응답 객체
        """
        headers = {
            "tr_id": "CTSC0008U",
        }
        body = {
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "PDNO": pdno,
            "ORD_QTY": ord_qty,
            "ORD_UNPR": ord_unpr,
            "SLL_BUY_DVSN_CD": sll_buy_dvsn_cd,
            "ORD_DVSN_CD": ord_dvsn_cd,
            "ORD_OBJT_CBLC_DVSN_CD": ord_objt_cblc_dvsn_cd,
            "LOAN_DT": loan_dt,
            "RSVN_ORD_END_DT": rsvn_ord_end_dt,
            "LDNG_DT": ldng_dt,
        }
        response = self.client._post("/uapi/domestic-stock/v1/trading/order-resv", headers=headers, body=body)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock reserve quote: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockReserveQuote.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def request_stock_reserve_quote_correction(
        self,
        tr_id: Literal["CTSC0009U", "CTSC0013U"],
        cano: str,
        acnt_prdt_cd: str,
        rsvn_ord_seq: str,
        ord_qty: str,
        ord_unpr: str,
        sll_buy_dvsn_cd: Literal["01", "02"],
        ord_dvsn_cd: Literal["00", "01", "02", "05"],
        ord_objt_cblc_dvsn_cd: Literal["10", "12", "14", "21", "22", "23", "24", "25", "26", "27", "28"],
        ctal_tlno: str,
        loan_dt: Optional[str] = None,
        rsvn_ord_end_dt: Optional[str] = None,
        rsvn_ord_orgno: Optional[str] = None,
        rsvn_ord_ord_dt: Optional[str] = None,
    ) -> KisHttpResponse[StockReserveQuoteCorrection]:
        """
        주식예약주문정정취소

        Args:
            tr_id: TR ID (예약취소): CTSC0009U, (예약정정): CTSC0013U
            cano: 종합계좌번호
            acnt_prdt_cd: 계좌상품코드
            rsvn_ord_seq: 예약주문순번
            ord_qty: 주문수량
            ord_unpr: 주문단가, 주문단가 시장가 주문시, "0"으로 입력
            sll_buy_dvsn_cd: 매도매수구분코드 (01 : 매도, 02 : 매수)
            ord_dvsn_cd: 주문구분코드 (00 : 지정가, 01 : 시장가, 02 : 조건부지정가, 05 : 장전 시간외)
            ord_objt_cblc_dvsn_cd: 주문대상잔고구분코드, (10 : 현금, 12 : 주식담보대출, 14 : 대여상환, 21 : 자기융자신규, 22 : 유통대주신규, 23 : 유통융자신규, 24 : 자기대주신규, 25 : 자기융자상환, 26 : 유통대주상환, 27 : 유통융자상환, 28 : 자기대주상환)
            ctal_tlno: 연락전화번호
            loan_dt: 대출일자
            rsvn_ord_end_dt: 예약주문종료일자 (YYYYMMDD) 현재 일자보다 이후로 설정해야 함
            rsvn_ord_orgno: 예약주문조직번호
            rsvn_ord_ord_dt: 예약주문주문일자 (YYYYMMDD)

        Returns:
            KisHttpResponse[StockReserveQuoteCorrection]: 주식예약주문정정취소 응답 객체
        """
        headers = {
            "tr_id": tr_id,
        }
        body = {
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "RSVN_ORD_SEQ": rsvn_ord_seq,
            "ORD_QTY": ord_qty,
            "ORD_UNPR": ord_unpr,
            "SLL_BUY_DVSN_CD": sll_buy_dvsn_cd,
            "ORD_DVSN_CD": ord_dvsn_cd,
            "ORD_OBJT_CBLC_DVSN_CD": ord_objt_cblc_dvsn_cd,
            "CTAL_TLNO": ctal_tlno,
            "LOAN_DT": loan_dt,
            "RSVN_ORD_END_DT": rsvn_ord_end_dt,
            "RSVN_ORD_ORGNO": rsvn_ord_orgno,
            "RSVN_ORD_ORD_DT": rsvn_ord_ord_dt,
        }
        response = self.client._post("/uapi/domestic-stock/v1/trading/order-resv-rvsecncl", headers=headers, body=body)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock reserve quote correction: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockReserveQuoteCorrection.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_stock_reserve_quote_inquiry(
        self,
        tr_cont: Literal["", "N"],
        rsvn_ord_ord_dt: str,
        rsvn_ord_end_dt: str,
        rsvn_ord_seq: str,
        cano: str,
        acnt_prdt_cd: str,
        prcs_dvsn_cd: Literal["0", "1", "2"],
        cncl_yn: Literal["Y", "N"],
        pdno: str,
        sll_buy_dvsn_cd: Literal["00", "01", "02"],
        ctx_area_fk200: str = "",
        ctx_area_nk200: str = "",
    ) -> KisHttpResponse[StockReserveQuoteInquiry]:
        """
        주식예약주문조회

        Args:
            tr_cont: 연속 거래 여부, (공백 : 초기 조회, N : 다음 데이터 조회 (output header의 tr_cont가 M일 경우)
            rsvn_ord_ord_dt: 예약주문시작일자, YYYYMMDD
            rsvn_ord_end_dt: 예약주문종료일자, YYYYMMDD
            rsvn_ord_seq: 예약주문순번
            cano: 종합계좌번호
            acnt_prdt_cd: 계좌상품코드
            prcs_dvsn_cd: 처리구분코드 (0: 전체 1: 처리내역 2: 미처리내역)
            cncl_yn: 취소여부 (Y: 유효한 주문만 조회)
            pdno: 상품번호, 종목번호(6자리), 공백 입력시 전체조회
            sll_buy_dvsn_cd: 매도매수구분코드 (00 : 전체, 01 : 매도, 02 : 매수)
            ctx_area_fk200: 연속조회검색조건200, '공란 : 최초 조회시는 이전 조회 Output CTX_AREA_FK200 값 : 다음페이지 조회시(2번째부터)'
            ctx_area_nk200: 연속조회키200, '공란 : 최초 조회시 이전 조회 Output CTX_AREA_NK200 값 : 다음페이지 조회시(2번째부터)

        Returns:
            KisHttpResponse[StockReserveQuoteInquiry]: 주식예약주문조회 응답 객체
        """
        headers = {
            "tr_id": "CTSC0004R",
            "tr_cont": tr_cont,
        }
        params = {
            "RSVN_ORD_ORD_DT": rsvn_ord_ord_dt,
            "RSVN_ORD_END_DT": rsvn_ord_end_dt,
            "RSVN_ORD_SEQ": rsvn_ord_seq,
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "PRCS_DVSN_CD": prcs_dvsn_cd,
            "CNCL_YN": cncl_yn,
            "PDNO": pdno,
            "SLL_BUY_DVSN_CD": sll_buy_dvsn_cd,
            "CTX_AREA_FK200": ctx_area_fk200,
            "CTX_AREA_NK200": ctx_area_nk200,
        }
        response = self.client._get("/uapi/domestic-stock/v1/trading/order-resv-ccnl", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock reserve quote inquiry: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockReserveQuoteInquiry.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_pension_conclusion_balance(
        self,
        cano: str,
        ctx_area_fk100: str,
        ctx_area_nk100: str,
        acnt_prdt_cd: str = "29",
        user_dvsn_cd: str = "00",
    ) -> KisHttpResponse[PensionConclusionBalance]:
        """
        퇴직연금 체결기준잔고

        Args:
            cano: 종합계좌번호
            ctx_area_fk100: 연속조회검색조건100, '공란 : 최초 조회시는 이전 조회 Output CTX_AREA_FK100 값 : 다음페이지 조회시(2번째부터)'
            ctx_area_nk100: 연속조회키100, '공란 : 최초 조회시 이전 조회 Output CTX_AREA_NK100 값 : 다음페이지 조회시(2번째부터)'
            acnt_prdt_cd: 계좌상품코드, 기본값 "29"
            user_dvsn_cd: 사용자구분코드, 기본값 "00"

        Returns:
            KisHttpResponse[PensionConclusionBalance]: 퇴직연금 체결기준잔고 응답 객체
        """
        headers = {
            "tr_id": "TTTC2202R",
        }
        params = {
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "USER_DVSN_CD": user_dvsn_cd,
            "CTX_AREA_FK100": ctx_area_fk100,
            "CTX_AREA_NK100": ctx_area_nk100,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/trading/pension/inquire-present-balance", headers=headers, params=params
        )
        if response.status_code != 200:
            raise Exception(f"Error fetching pension conclusion balance: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = PensionConclusionBalance.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_pension_not_conclusion_history(
        self,
        cano: str,
        sll_buy_dvsn_cd: Literal["00", "01", "02"],
        ccld_nccs_dvsn: Literal["%%", "01", "02"],
        ctx_area_fk100: str,
        ctx_area_nk100: str,
        acnt_prdt_cd: str = "29",
        inqr_dvsn_3: Literal["00"] = "00",
        user_dvsn_cd: str = "00",
    ) -> KisHttpResponse[PensionNotConclusionHistory]:
        """
        퇴직연금 미체결내역

        Args:
            cano: 종합계좌번호
            sll_buy_dvsn_cd: 매도매수구분코드 (00 : 전체, 01 : 매도, 02 : 매수)
            ccld_n  ccs_dvsn: 체결미체결구분 (%% : 전체, 01 : 체결, 02 : 미체결)
            ctx_area_fk100: 연속조회검색조건100, '공란 : 최초 조회시는 이전 조회 Output CTX_AREA_FK100 값 : 다음페이지 조회시(2번째부터)'
            ctx_area_nk100: 연속조회키100, '공란 : 최초 조회시 이전 조회 Output CTX_AREA_NK100 값 : 다음페이지 조회시(2번째부터)'
            acnt_prdt_cd: 계좌상품코드, 기본값 "29"
            inqr_dvsn_3: 조회구분3, 기본값 "00"
            user_dvsn_cd: 사용자구분코드, 기본값 "00"

        Returns:
            KisHttpResponse[PensionNotConclusionHistory]: 퇴직연금 미체결내역 응답 객체
        """
        headers = {
            "tr_id": "TTTC2210R",
        }
        params = {
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "USER_DVSN_CD": user_dvsn_cd,
            "SLL_BUY_DVSN_CD": sll_buy_dvsn_cd,
            "CCLD_NCCS_DVSN": ccld_nccs_dvsn,
            "INQR_DVSN_3": inqr_dvsn_3,
            "CTX_AREA_FK100": ctx_area_fk100,
            "CTX_AREA_NK100": ctx_area_nk100,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/trading/pension/inquire-daily-ccld", headers=headers, params=params
        )
        if response.status_code != 200:
            raise Exception(f"Error fetching pension not conclusion history: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = PensionNotConclusionHistory.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_pension_buy_tradable_inquiry(
        self,
        cano: str,
        pdno: str,
        cma_evlu_amt_icld_yn: Literal["Y", "N"],
        ord_dvsn: Literal["00", "01"],
        ord_unpr: str,
        acnt_prdt_cd: str = "29",
        acca_dvsn_cd: Literal["00"] = "00",
    ) -> KisHttpResponse[PensionBuyTradableInquiry]:
        """
        퇴직연금 매수가능조회

        Args:
            cano: 종합계좌번호
            pdno: 상품번호, 종목번호(6자리), 공백 입력시 전체조회
            cma_evlu_amt_icld_yn: CMA평가금액포함여부 (Y/N)
            ord_dvsn: 주문구분 (00 : 지정가, 01 : 시장가)
            ord_unpr: 주문단가
            acnt_prdt_cd: 계좌상품코드, 기본값 "29"
            acca_dvsn_cd: 적립금구분코드, 기본값 "00"

        Returns:
            KisHttpResponse[PensionBuyTradableInquiry]: 퇴직연금 매수가능조회 응답 객체
        """
        headers = {
            "tr_id": "TTTC0503R",
        }
        params = {
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "PDNO": pdno,
            "ACCA_DVSN_CD": acca_dvsn_cd,
            "CMA_EVLU_AMT_ICLD_YN": cma_evlu_amt_icld_yn,
            "ORD_DVSN": ord_dvsn,
            "ORD_UNPR": ord_unpr,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/trading/pension/inquire-psbl-order", headers=headers, params=params
        )
        if response.status_code != 200:
            raise Exception(f"Error fetching pension buy tradable inquiry: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = PensionBuyTradableInquiry.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_pension_reserve_deposit_inquiry(
        self,
        cano: str,
        acnt_prdt_cd: str = "29",
        user_dvsn_cd: str = "00",
    ) -> KisHttpResponse[PensionReserveDepositInquiry]:
        """
        퇴직연금 예수금조회

        Args:
            cano: 종합계좌번호
            acnt_prdt_cd: 계좌상품코드, 기본값 "29"
            user_dvsn_cd: 사용자구분코드, 기본값 "00"

        Returns:
            KisHttpResponse[PensionReserveDepositInquiry]: 퇴직연금 예수금조회 응답 객체
        """
        headers = {
            "tr_id": "TTTC0506R",
        }
        params = {
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "USER_DVSN_CD": user_dvsn_cd,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/trading/pension/inquire-deposit", headers=headers, params=params
        )
        if response.status_code != 200:
            raise Exception(f"Error fetching pension reserve deposit inquiry: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = PensionReserveDepositInquiry.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_pension_balance_inquiry(
        self,
        cano: str,
        ctx_area_fk100: str,
        ctx_area_nk100: str,
        acnt_prdt_cd: str = "29",
        user_dvsn_cd: str = "00",
        inqr_dvsn: Literal["00"] = "00",
    ) -> KisHttpResponse[PensionBalanceInquiry]:
        """
        퇴직연금 잔고조회

        Args:
            cano: 종합계좌번호
            ctx_area_fk100: 연속조회검색조건100, '공란 : 최초 조회시는 이전 조회 Output CTX_AREA_FK100 값 : 다음페이지 조회시(2번째부터)'
            ctx_area_nk100: 연속조회키100, '공란 : 최초 조회시 이전 조회 Output CTX_AREA_NK100 값 : 다음페이지 조회시(2번째부터)'
            acnt_prdt_cd: 계좌상품코드, 기본값 "29"
            user_dvsn_cd: 사용자구분코드, 기본값 "00"
            inqr_dvsn: 조회구분, 기본값 "00"

        Returns:
            KisHttpResponse[PensionBalanceInquiry]: 퇴직연금 잔고조회 응답 객체
        """
        headers = {
            "tr_id": "TTTC2208R",
        }
        params = {
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "USER_DVSN_CD": user_dvsn_cd,
            "INQR_DVSN": inqr_dvsn,
            "CTX_AREA_FK100": ctx_area_fk100,
            "CTX_AREA_NK100": ctx_area_nk100,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/trading/pension/inquire-balance", headers=headers, params=params
        )
        if response.status_code != 200:
            raise Exception(f"Error fetching pension balance inquiry: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = PensionBalanceInquiry.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_stock_balance_loss_profit(
        self,
        tr_cont: Literal["F", "M", "D", "E"],
        cano: str,
        acnt_prdt_cd: str,
        ctx_area_fk100: str,
        ctx_area_nk100: str,
        afhr_flpr_yn: Literal["N", "Y"],
        cost_icld_yn: Literal["N", "Y"],
        ofl_yn: Literal["", "Y"] = "",
        inqr_dvsn: Literal["00", "01", "02"] = "00",
        unpr_dvsn: Literal["01"] = "01",
        fund_sttl_icld_yn: Literal["N", "Y"] = "N",
        fncg_amt_auto_rdpt_yn: Literal["N", "Y"] = "N",
        prcs_dvsn: Literal["00", "01"] = "00",
    ) -> KisHttpResponse[StockBalanceLossProfit]:
        """
        주식잔고조회 실현손익

        Args:
            tr_cont: 연속 거래 여부, (F or M : 다음 데이터 있음, D or E : 마지막 데이터)
            cano: 종합계좌번호
            acnt_prdt_cd: 계좌상품코드
            ctx_area_fk100: 연속조회검색조건100, '공란 : 최초 조회시는 이전 조회 Output CTX_AREA_FK100 값 : 다음페이지 조회시(2번째부터)'
            ctx_area_nk100: 연속조회키100, '공란 : 최초 조회시 이전 조회 Output CTX_AREA_NK100 값 : 다음페이지 조회시(2번째부터)'
            afhr_flpr_yn: 시간외단일가, 거래소여부
            cost_icld_yn: 비용포함여부
            ofl_yn: 오프라인여부
            inqr_dvsn: 조회구분
            unpr_dvsn: 단가구분
            fund_sttl_icld_yn: 펀드결제분포함여부
            fncg_amt_auto_rdpt_yn: 융자금액자동상환여부
            prcs_dvsn: 처리구분 (00 : 전일매매포함, 01 : 전일매매미포함)

        Returns:
            KisHttpResponse[StockBalanceLossProfit]: 주식잔고조회 실현손익 응답 객체
        """
        headers = {
            "tr_id": "TTTC8494R",
            "tr_cont": tr_cont,
        }
        params = {
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "AFHR_FLPR_YN": afhr_flpr_yn,
            "OFL_YN": ofl_yn,
            "INQR_DVSN": inqr_dvsn,
            "UNPR_DVSN": unpr_dvsn,
            "FUND_STTL_ICLD_YN": fund_sttl_icld_yn,
            "FNCG_AMT_AUTO_RDPT_YN": fncg_amt_auto_rdpt_yn,
            "PRCS_DVSN": prcs_dvsn,
            "COST_ICLD_YN": cost_icld_yn,
            "CTX_AREA_FK100": ctx_area_fk100,
            "CTX_AREA_NK100": ctx_area_nk100,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/trading/inquire-balance-rlz-pl", headers=headers, params=params
        )
        if response.status_code != 200:
            raise Exception(f"Error fetching stock balance loss profit: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockBalanceLossProfit.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_investment_account_current_status(
        self,
        tr_cont: Literal["", "N"],
        cano: str,
        acnt_prdt_cd: str,
        inqr_dvsn_1: Literal["", "N", "Y"] = "",
        bspr_bf_dt_aply_yn: Literal["", "N", "Y"] = "",
    ) -> KisHttpResponse[InvestmentAccountCurrentStatus]:
        """
        투자계좌자산현황조회

        Args:
            tr_cont: 연속 거래 여부, (공백 : 초기 조회, N : 다음 데이터 조회 (output header의 tr_cont가 M일 경우)
            cano: 종합계좌번호
            acnt_prdt_cd: 계좌상품코드
            inqr_dvsn_1: 조회구분1, 기본값 ""
            bspr_bf_dt_aply_yn: 기준가이전일자적용여부, 기본값 ""

        Returns:
            KisHttpResponse[InvestmentAccountCurrentStatus]: 투자계좌자산현황조회 응답 객체
        """
        headers = {
            "tr_id": "CTRP6548R",
            "tr_cont": tr_cont,
        }
        params = {
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "INQR_DVSN_1": inqr_dvsn_1,
            "BSPR_BF_DT_APLY_YN": bspr_bf_dt_aply_yn,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/trading/inquire-account-balance", headers=headers, params=params
        )
        if response.status_code != 200:
            raise Exception(f"Error fetching investment account current status: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = InvestmentAccountCurrentStatus.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_period_profit_summary(
        self,
        tr_cont: Literal["", "N"],
        acnt_prdt_cd: str,
        cano: str,
        inqr_strt_dt: str,
        inqr_end_dt: str,
        pdno: str,
        ctx_area_nk100: str,
        ctx_area_fk100: str,
        sort_dvsn: Literal["00", "01", "02"],
        inqr_dvsn: Literal["00"] = "00",
        cblc_dvsn: Literal["00"] = "00",
    ) -> KisHttpResponse[PeriodProfitSummary]:
        """
        기간별순익별합산조회

        Args:
            tr_cont: 연속 거래 여부, (공백 : 초기 조회, N : 다음 데이터 조회 (output header의 tr_cont가 M일 경우)
            acnt_prdt_cd: 계좌상품코드
            cano: 종합계좌번호
            inqr_strt_dt: 조회시작일자, YYYYMMDD
            inqr_end_dt: 조회종료일자, YYYYMMDD
            pdno: 상품번호, 종목번호(6자리), 공백 입력시 전체조회
            ctx_area_nk100: 연속조회키100, '공란 : 최초 조회시 이전 조회 Output CTX_AREA_NK100 값 : 다음페이지 조회시(2번째부터)'
            ctx_area_fk100: 연속조회검색조건100, '공란 : 최초 조회시는 이전 조회 Output CTX_AREA_FK100 값 : 다음페이지 조회시(2번째부터)'
            sort_dvsn: 정렬구분 (00: 최근 순, 01: 과거 순, 02: 최근 순)

        Returns:
            KisHttpResponse[PeriodProfitSummary]: 기간별순익별합산조회 응답 객체
        """
        headers = {
            "tr_id": "TTTC8708R",
            "tr_cont": tr_cont,
        }
        params = {
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "CANO": cano,
            "INQR_STRT_DT": inqr_strt_dt,
            "INQR_END_DT": inqr_end_dt,
            "PDNO": pdno,
            "CTX_AREA_NK100": ctx_area_nk100,
            "CTX_AREA_FK100": ctx_area_fk100,
            "SORT_DVSN": sort_dvsn,
            "INQR_DVSN": inqr_dvsn,
            "CBLC_DVSN": cblc_dvsn,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/trading/inquire-period-profit", headers=headers, params=params
        )
        if response.status_code != 200:
            raise Exception(f"Error fetching period profit summary: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = PeriodProfitSummary.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_period_trading_profit_status(
        self,
        tr_cont: Literal["", "N"],
        cano: str,
        sort_dsvn: Literal["00", "01", "02"],
        acnt_prdt_cd: str,
        pdno: str,
        inqr_strt_dt: str,
        inqr_end_dt: str,
        ctx_area_nk100: str,
        ctx_area_fk100: str,
        cblc_dvsn: Literal["00", "01", "02"] = "00",
    ) -> KisHttpResponse[PeriodTradingProfitStatus]:
        """
        기간별매매순익현황조회

        Args:
            tr_cont: 연속 거래 여부, (공백 : 초기 조회, N : 다음 데이터 조회 (output header의 tr_cont가 M일 경우)
            cano: 종합계좌번호
            sort_dsvn: 정렬구분 (00: 최근 순, 01: 과거 순, 02: 최근 순)
            acnt_prdt_cd: 계좌  상품코드
            pdno: 상품번호, 종목번호(6자리), 공백 입력시 전체조회
            inqr_strt_dt: 조회시작일자, YYYYMMDD
            inqr_end_dt: 조회종료일자, YYYYMMDD
            ctx_area_nk100: 연속조회키100, '공란 : 최초 조회시 이전 조회 Output CTX_AREA_NK100 값 : 다음페이지 조회시(2번째부터)'
            ctx_area_fk100: 연속조회검색조건100, '공란 : 최초 조회시는 이전 조회 Output CTX_AREA_FK100 값 : 다음페이지 조회시(2번째부터)'
            cblc_dvsn: 잔고구분 (00: 전체, 01: 잔고, 02: 대기)

        Returns:
            KisHttpResponse[PeriodTradingProfitStatus]: 기간별매매순익현황조회 응답 객체
        """
        headers = {
            "tr_id": "TTTC8715R",
            "tr_cont": tr_cont,
        }
        params = {
            "CANO": cano,
            "SORT_DVSN": sort_dsvn,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "PDNO": pdno,
            "INQR_STRT_DT": inqr_strt_dt,
            "INQR_END_DT": inqr_end_dt,
            "CTX_AREA_NK100": ctx_area_nk100,
            "CTX_AREA_FK100": ctx_area_fk100,
            "CBLC_DVSN": cblc_dvsn,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/trading/inquire-period-trade-profit", headers=headers, params=params
        )
        if response.status_code != 200:
            raise Exception(f"Error fetching period trading profit status: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = PeriodTradingProfitStatus.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_stock_integrated_deposit_balance(
        self,
        cano: str,
        acnt_prdt_cd: str,
        wcrc_frcr_dvsn_cd: Literal["01", "02"],
        fwex_ctrt_frcr_dvsn_cd: Literal["01", "02"],
        cma_evlu_amt_icld_yn: Literal["N", "Y"] = "N",
    ) -> KisHttpResponse[StockIntegratedDepositBalance]:
        """
        주식통합증거금 현황
        Args:
            cano: 종합계좌번호
            acnt_prdt_cd: 계좌상품코드
            wcrc_frcr_dvsn_cd: 원화외화구분코드 (01(외화기준),02(원화기준))
            fwex_ctrt_frcr_dvsn_cd: 선도환계약외화구분코드 (01(외화기준),02(원화기준))
            cma_evlu_amt_icld_yn: CMA평가금액포함여부 (N/Y), 기본값 "N"

        Returns:
            KisHttpResponse[StockIntegratedDepositBalance]: 주식통합증거금 현황 응답 객체
        """
        headers = {
            "tr_id": "TTTC0869R",
        }
        params = {
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "WCRC_FRCR_DVSN_CD": wcrc_frcr_dvsn_cd,
            "FWEX_CTRT_FRCR_DVSN_CD": fwex_ctrt_frcr_dvsn_cd,
            "CMA_EVLU_AMT_ICLD_YN": cma_evlu_amt_icld_yn,
        }
        response = self.client._get("/uapi/domestic-stock/v1/trading/intgr-margin", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock integrated deposit balance: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockIntegratedDepositBalance.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_period_accounting_current_status(
        self,
        tr_cont: Literal["", "N"],
        cano: str,
        acnt_prdt_cd: str,
        inqr_strt_dt: str,
        inqr_end_dt: str,
        ctx_area_nk100: str,
        ctx_area_fk100: str,
        inqr_dvsn: Literal["03"] = "03",
        cust_rncno25: str = "",
        hmid: str = "",
        rght_type_cd: str = "",
        pdno: str = "",
        prdt_type_cd: str = "",
    ) -> KisHttpResponse[PeriodAccountingCurrentStatus]:
        """
        기간별계좌권리현황조회

        Args:
            tr_cont: 연속 거래 여부, (공백 : 초기 조회, N : 다음 데이터 조회 (output header의 tr_cont가 M일 경우)
            cano: 종합계좌번호
            acnt_prdt_cd: 계좌상품코드
            inqr_strt_dt: 조회시작일자, YYYYMMDD
            inqr_end_dt: 조회종료일자, YYYYMMDD
            ctx_area_nk100: 연속조회키100, '공란 : 최초 조회시 이전 조회 Output CTX_AREA_NK100 값 : 다음페이지 조회시(2번째부터)'
            ctx_area_fk100: 연속조회검색조건100, '공란 : 최초 조회시는 이전 조회 Output CTX_AREA_FK100 값 : 다음페이지 조회시(2번째부터)'
            inqr_dvsn: 조회구분, 기본값 "03"
            cust_rncno25: 고객실명확인번호25, 기본값 ""
            hmid: 홈넷ID, 기본값 ""
            rght_type_cd: 권리유형코드, 기본값 ""
            pdno: 상품번호, 종목번호(6자리), 공백 입력시 전체조회, 기본값 ""
            prdt_type_cd: 상품유형코드, 기본값 ""

        Returns:
            KisHttpResponse[PeriodAccountingCurrentStatus]: 기간별계좌권리현황조회 응답 객체
        """
        headers = {
            "tr_id": "CTRGA011R",
            "tr_cont": tr_cont,
        }
        params = {
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "INQR_STRT_DT": inqr_strt_dt,
            "INQR_END_DT": inqr_end_dt,
            "CTX_AREA_NK100": ctx_area_nk100,
            "CTX_AREA_FK100": ctx_area_fk100,
            "INQR_DVSN": inqr_dvsn,
            "CUST_RNCNO25": cust_rncno25,
            "HMID": hmid,
            "RGHT_TYPE_CD": rght_type_cd,
            "PDNO": pdno,
            "PRDT_TYPE_CD": prdt_type_cd,
        }
        response = self.client._get("/uapi/domestic-stock/v1/trading/period-rights", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching period accounting current status: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = PeriodAccountingCurrentStatus.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)
