from cluefin_openapi.kis._http_client import HttpClient
from cluefin_openapi.kis._model import KisHttpHeader, KisHttpResponse
from cluefin_openapi.kis._overseas_account_types import (
    BalanceBySettlement,
    BuyTradableAmount,
    CorrectAfterDayTime,
    CurrentBalanceByConclusion,
    DailyTransactionHistory,
    LimitOrderExecutionHistory,
    LimitOrderNumber,
    MarginAggregate,
    OrderAfterDayTime,
    PeriodProfitLoss,
    ReserveOrders,
    StockBalance,
    StockConclusionHistory,
    StockNotConclusion,
    StockQuoteCorrection,
    StockQuoteCurrent,
    StockReserveQuote,
    StockReserveQuoteCorrection,
)


class OverseasAccount:
    """해외주식 주문/계좌"""

    def __init__(self, client: HttpClient):
        self.client = client

    def _check_response_error(self, response_data: dict) -> None:
        """Check if API response contains an error and raise if so."""
        rt_cd = response_data.get("rt_cd")
        if rt_cd != "0":
            msg_cd = response_data.get("msg_cd", "")
            msg1 = response_data.get("msg1", "Unknown error")
            raise ValueError(f"KIS API Error [{msg_cd}]: {msg1} (rt_cd={rt_cd})")

    def request_stock_order(
        self,
        cano: str,
        acnt_prdt_cd: str,
        ovrs_excg_cd: str,
        pdno: str,
        ord_qty: str,
        ovrs_ord_unpr: str,
        ord_dvsn: str,
        start_time: str = "",
        end_time: str = "",
        algo_ord_tmd_dvsn_cd: str = "",
    ) -> KisHttpResponse[StockQuoteCurrent]:
        """해외주식 주문

        Args:
            cano (str): 종합계좌번호 (8자리)
            acnt_prdt_cd (str): 계좌상품코드 (2자리)
            ovrs_excg_cd (str): 해외거래소코드 (NASD: 나스닥, NYSE: 뉴욕, AMEX: 아멕스, SEHK: 홍콩, SHAA: 중국상해, SZAA: 중국심천, TKSE: 일본, HASE: 베트남 하노이, VNSE: 베트남 호치민)
            pdno (str): 상품번호 (종목코드)
            ord_qty (str): 주문수량
            ovrs_ord_unpr (str): 해외주문단가
            ord_dvsn (str): 주문구분 (00: 지정가, 31: MOO, 32: LOO, 33: MOC, 34: LOC, 35: TWAP, 36: VWAP)
            start_time (str): 시작시간 (HHMMSS, TWAP/VWAP 주문유형인 경우 사용)
            end_time (str): 종료시간 (HHMMSS, TWAP/VWAP 주문유형인 경우 사용)
            algo_ord_tmd_dvsn_cd (str): 알고리즘주문시간구분코드 (00: 분할주문 시간 직접입력, 02: 정규장 종료시까지)

        Returns:
            KisHttpResponse[StockQuoteCurrent]: 해외주식 주문 응답 객체
        """
        headers = {
            "tr_id": "TTTT1002U",
        }
        body = {
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "OVRS_EXCG_CD": ovrs_excg_cd,
            "PDNO": pdno,
            "ORD_QTY": ord_qty,
            "OVRS_ORD_UNPR": ovrs_ord_unpr,
            "ORD_DVSN": ord_dvsn,
            "START_TIME": start_time,
            "END_TIME": end_time,
            "ALGO_ORD_TMD_DVSN_CD": algo_ord_tmd_dvsn_cd,
        }
        response = self.client._post("/uapi/overseas-stock/v1/trading/order", headers=headers, body=body)
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = StockQuoteCurrent.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def request_stock_quote_correction(
        self,
        cano: str,
        acnt_prdt_cd: str,
        ovrs_excg_cd: str,
        pdno: str,
        orgn_odno: str,
        rvse_cncl_dvsn_cd: str,
        ord_qty: str,
        ovrs_ord_unpr: str,
        mgco_aptm_odno: str = "",
        ord_svr_dvsn_cd: str = "0",
    ) -> KisHttpResponse[StockQuoteCorrection]:
        """해외주식 정정취소주문

        Args:
            cano (str): 종합계좌번호 (8자리)
            acnt_prdt_cd (str): 계좌상품코드 (2자리)
            ovrs_excg_cd (str): 해외거래소코드 (NASD: 나스닥, NYSE: 뉴욕, AMEX: 아멕스, SEHK: 홍콩, SHAA: 중국상해, SZAA: 중국심천, TKSE: 일본, HASE: 베트남 하노이, VNSE: 베트남 호치민)
            pdno (str): 상품번호
            orgn_odno (str): 원주문번호 (정정 또는 취소할 원주문번호)
            rvse_cncl_dvsn_cd (str): 정정취소구분코드 (01: 정정, 02: 취소)
            ord_qty (str): 주문수량
            ovrs_ord_unpr (str): 해외주문단가 (취소주문 시 "0" 입력)
            mgco_aptm_odno (str): 운용사지정주문번호
            ord_svr_dvsn_cd (str): 주문서버구분코드 (기본값 "0")

        Returns:
            StockQuoteCorrection: 해외주식 정정취소주문 응답 객체
        """
        headers = {
            "tr_id": "TTTT1004U",
        }
        body = {
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "OVRS_EXCG_CD": ovrs_excg_cd,
            "PDNO": pdno,
            "ORGN_ODNO": orgn_odno,
            "RVSE_CNCL_DVSN_CD": rvse_cncl_dvsn_cd,
            "ORD_QTY": ord_qty,
            "OVRS_ORD_UNPR": ovrs_ord_unpr,
            "MGCO_APTM_ODNO": mgco_aptm_odno,
            "ORD_SVR_DVSN_CD": ord_svr_dvsn_cd,
        }
        response = self.client._post(
            "/uapi/overseas-stock/v1/trading/order-rvsecncl",
            headers=headers,
            body=body,
        )
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = StockQuoteCorrection.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def request_stock_reserve_quote(
        self,
        cano: str,
        acnt_prdt_cd: str,
        pdno: str,
        prdt_type_cd: str,
        ovrs_excg_cd: str,
        ft_ord_qty: str,
        ft_ord_unpr3: str,
        sll_buy_dvsn_cd: str = "",
        rvse_cncl_dvsn_cd: str = "",
        ord_svr_dvsn_cd: str = "0",
        rsvn_ord_rcit_dt: str = "",
        ord_dvsn: str = "",
        ovrs_rsvn_odno: str = "",
        algo_ord_tmd_dvsn_cd: str = "",
    ) -> KisHttpResponse[StockReserveQuote]:
        """해외주식 예약주문접수

        Args:
            cano (str): 종합계좌번호 (8자리)
            acnt_prdt_cd (str): 계좌상품코드 (2자리)
            pdno (str): 상품번호
            prdt_type_cd (str): 상품유형코드 (515: 일본, 501: 홍콩, 543: 홍콩CNY, 558: 홍콩USD, 507: 베트남 하노이거래소, 508: 베트남 호치민거래소, 551: 중국 상해A, 552: 중국 심천A)
            ovrs_excg_cd (str): 해외거래소코드 (NASD: 나스닥, NYSE: 뉴욕, AMEX: 아멕스, SEHK: 홍콩, SHAA: 중국상해, SZAA: 중국심천, TKSE: 일본, HASE: 베트남 하노이, VNSE: 베트남 호치민)
            ft_ord_qty (str): FT주문수량
            ft_ord_unpr3 (str): FT주문단가3
            sll_buy_dvsn_cd (str): 매도매수구분코드 (01: 매도, 02: 매수, TTTS3013U인 경우만 사용)
            rvse_cncl_dvsn_cd (str): 정정취소구분코드 (00: 매도/매수 주문시 필수, 02: 취소, TTTS3013U인 경우만 사용)
            ord_svr_dvsn_cd (str): 주문서버구분코드 (기본값 "0")
            rsvn_ord_rcit_dt (str): 예약주문접수일자 (TTTS3013U인 경우만 사용)
            ord_dvsn (str): 주문구분 (00: 지정가, 31: MOO, 35: TWAP, 36: VWAP)
            ovrs_rsvn_odno (str): 해외예약주문번호 (TTTS3013U인 경우만 사용)
            algo_ord_tmd_dvsn_cd (str): 알고리즘주문시간구분코드 (TWAP/VWAP 주문에서만 사용, 02로 값 고정)

        Returns:
            StockReserveQuote: 해외주식 예약주문접수 응답 객체
        """
        headers = {
            "tr_id": "TTTT3014U",
        }
        body = {
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "SLL_BUY_DVSN_CD": sll_buy_dvsn_cd,
            "RVSE_CNCL_DVSN_CD": rvse_cncl_dvsn_cd,
            "PDNO": pdno,
            "PRDT_TYPE_CD": prdt_type_cd,
            "OVRS_EXCG_CD": ovrs_excg_cd,
            "FT_ORD_QTY": ft_ord_qty,
            "FT_ORD_UNPR3": ft_ord_unpr3,
            "ORD_SVR_DVSN_CD": ord_svr_dvsn_cd,
            "RSVN_ORD_RCIT_DT": rsvn_ord_rcit_dt,
            "ORD_DVSN": ord_dvsn,
            "OVRS_RSVN_ODNO": ovrs_rsvn_odno,
            "ALGO_ORD_TMD_DVSN_CD": algo_ord_tmd_dvsn_cd,
        }
        response = self.client._post("/uapi/overseas-stock/v1/trading/order-resv", headers=headers, body=body)
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = StockReserveQuote.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def request_stock_reserve_quote_correction(
        self,
        cano: str,
        acnt_prdt_cd: str,
        rsyn_ord_rcit_dt: str,
        ovrs_rsvn_odno: str,
    ) -> KisHttpResponse[StockReserveQuoteCorrection]:
        """해외주식 예약주문접수취소

        Args:
            cano (str): 종합계좌번호 (8자리)
            acnt_prdt_cd (str): 계좌상품코드 (2자리)
            rsyn_ord_rcit_dt (str): 해외주문접수일자
            ovrs_rsvn_odno (str): 해외예약주문번호 (해외주식_예약주문접수 API Output ODNO 참고)

        Returns:
            StockReserveQuoteCorrection: 해외주식 예약주문접수취소 응답 객체
        """
        headers = {
            "tr_id": "TTTT3017U",
        }
        body = {
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "RSYN_ORD_RCIT_DT": rsyn_ord_rcit_dt,
            "OVRS_RSVN_ODNO": ovrs_rsvn_odno,
        }
        response = self.client._post(
            "/uapi/overseas-stock/v1/trading/order-resv-ccnl",
            headers=headers,
            body=body,
        )
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = StockReserveQuoteCorrection.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def get_buy_tradable_amount(
        self,
        cano: str,
        acnt_prdt_cd: str,
        ovrs_excg_cd: str,
        ovrs_ord_unpr: str,
        item_cd: str,
    ) -> KisHttpResponse[BuyTradableAmount]:
        """해외주식 매수가능금액조회

        Args:
            cano (str): 종합계좌번호 (8자리)
            acnt_prdt_cd (str): 계좌상품코드 (2자리)
            ovrs_excg_cd (str): 해외거래소코드 (NASD: 나스닥, NYSE: 뉴욕, AMEX: 아멕스, SEHK: 홍콩, SHAA: 중국상해, SZAA: 중국심천, TKSE: 일본, HASE: 하노이거래소, VNSE: 호치민거래소)
            ovrs_ord_unpr (str): 해외주문단가 (23.8 정수부분 23자리, 소수부분 8자리)
            item_cd (str): 종목코드

        Returns:
            BuyTradableAmount: 해외주식 매수가능금액조회 응답 객체
        """
        headers = {
            "tr_id": "TTTS3007R",
        }
        params = {
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "OVRS_EXCG_CD": ovrs_excg_cd,
            "OVRS_ORD_UNPR": ovrs_ord_unpr,
            "ITEM_CD": item_cd,
        }
        response = self.client._get(
            "/uapi/overseas-stock/v1/trading/inquire-psamount",
            headers=headers,
            params=params,
        )
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = BuyTradableAmount.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def get_stock_not_conclusion_history(
        self,
        cano: str,
        acnt_prdt_cd: str,
        ovrs_excg_cd: str,
        sort_sqn: str,
        ctx_area_fk200: str = "",
        ctx_area_nk200: str = "",
    ) -> KisHttpResponse[StockNotConclusion]:
        """해외주식 미체결내역

        Args:
            cano (str): 종합계좌번호 (8자리)
            acnt_prdt_cd (str): 계좌상품코드 (2자리)
            ovrs_excg_cd (str): 해외거래소코드 (NASD: 나스닥, NYSE: 뉴욕, AMEX: 아멕스, SEHK: 홍콩, SHAA: 중국상해, SZAA: 중국심천, TKSE: 일본, HASE: 베트남 하노이, VNSE: 베트남 호치민)
            sort_sqn (str): 정렬순서 (DS: 정순, 그외: 역순)
            ctx_area_fk200 (str): 연속조회검색조건200 (최초 조회시 공란, 다음페이지 조회시 이전 조회 Output 값)
            ctx_area_nk200 (str): 연속조회키200 (최초 조회시 공란, 다음페이지 조회시 이전 조회 Output 값)

        Returns:
            StockNotConclusion: 해외주식 미체결내역 응답 객체
        """
        headers = {
            "tr_id": "TTTS3018R",
        }
        params = {
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "OVRS_EXCG_CD": ovrs_excg_cd,
            "SORT_SQN": sort_sqn,
            "CTX_AREA_FK200": ctx_area_fk200,
            "CTX_AREA_NK200": ctx_area_nk200,
        }
        response = self.client._get(
            "/uapi/overseas-stock/v1/trading/inquire-nccs",
            headers=headers,
            params=params,
        )
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = StockNotConclusion.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def get_stock_balance(
        self,
        cano: str,
        acnt_prdt_cd: str,
        ovrs_excg_cd: str,
        tr_crcy_cd: str,
        ctx_area_fk200: str = "",
        ctx_area_nk200: str = "",
    ) -> KisHttpResponse[StockBalance]:
        """해외주식 잔고

        Args:
            cano (str): 종합계좌번호 (8자리)
            acnt_prdt_cd (str): 계좌상품코드 (2자리)
            ovrs_excg_cd (str): 해외거래소코드 (NASD: 미국전체, NAS: 나스닥, NYSE: 뉴욕, AMEX: 아멕스, SEHK: 홍콩, SHAA: 중국상해, SZAA: 중국심천, TKSE: 일본, HASE: 베트남 하노이, VNSE: 베트남 호치민)
            tr_crcy_cd (str): 거래통화코드 (USD: 미국달러, HKD: 홍콩달러, CNY: 중국위안화, JPY: 일본엔화, VND: 베트남동)
            ctx_area_fk200 (str): 연속조회검색조건200 (최초 조회시 공란, 다음페이지 조회시 이전 조회 Output 값)
            ctx_area_nk200 (str): 연속조회키200 (최초 조회시 공란, 다음페이지 조회시 이전 조회 Output 값)

        Returns:
            StockBalance: 해외주식 잔고 응답 객체
        """
        headers = {
            "tr_id": "TTTS3012R",
        }
        params = {
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "OVRS_EXCG_CD": ovrs_excg_cd,
            "TR_CRCY_CD": tr_crcy_cd,
            "CTX_AREA_FK200": ctx_area_fk200,
            "CTX_AREA_NK200": ctx_area_nk200,
        }
        response = self.client._get(
            "/uapi/overseas-stock/v1/trading/inquire-balance",
            headers=headers,
            params=params,
        )
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = StockBalance.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def get_stock_conclusion_history(
        self,
        cano: str,
        acnt_prdt_cd: str,
        pdno: str,
        ord_strt_dt: str,
        ord_end_dt: str,
        sll_buy_dvsn: str,
        ccld_nccs_dvsn: str,
        ovrs_excg_cd: str,
        sort_sqn: str,
        ord_dt: str = "",
        ord_gno_brno: str = "",
        odno: str = "",
        ctx_area_nk200: str = "",
        ctx_area_fk200: str = "",
    ) -> KisHttpResponse[StockConclusionHistory]:
        """해외주식 주문체결내역

        Args:
            cano (str): 종합계좌번호 (8자리)
            acnt_prdt_cd (str): 계좌상품코드 (2자리)
            pdno (str): 상품번호 (전종목일 경우 "%", 모의투자계좌의 경우 ""만 가능)
            ord_strt_dt (str): 주문시작일자 (YYYYMMDD, 현지시각 기준)
            ord_end_dt (str): 주문종료일자 (YYYYMMDD, 현지시각 기준)
            sll_buy_dvsn (str): 매도매수구분 (00: 전체, 01: 매도, 02: 매수)
            ccld_nccs_dvsn (str): 체결미체결구분 (00: 전체, 01: 체결, 02: 미체결)
            ovrs_excg_cd (str): 해외거래소코드 (전종목일 경우 "%", NASD: 미국시장 전체, NYSE: 뉴욕, AMEX: 아멕스, SEHK: 홍콩, SHAA: 중국상해, SZAA: 중국심천, TKSE: 일본, HASE: 베트남 하노이, VNSE: 베트남 호치민)
            sort_sqn (str): 정렬순서 (DS: 정순, AS: 역순)
            ord_dt (str): 주문일자 (Null 값 설정)
            ord_gno_brno (str): 주문채번지점번호 (Null 값 설정)
            odno (str): 주문번호 (Null 값 설정)
            ctx_area_nk200 (str): 연속조회키200 (최초 조회시 공란, 다음페이지 조회시 이전 조회 Output 값)
            ctx_area_fk200 (str): 연속조회검색조건200 (최초 조회시 공란, 다음페이지 조회시 이전 조회 Output 값)

        Returns:
            StockConclusionHistory: 해외주식 주문체결내역 응답 객체
        """
        headers = {
            "tr_id": "TTTS3035R",
        }
        params = {
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "PDNO": pdno,
            "ORD_STRT_DT": ord_strt_dt,
            "ORD_END_DT": ord_end_dt,
            "SLL_BUY_DVSN": sll_buy_dvsn,
            "CCLD_NCCS_DVSN": ccld_nccs_dvsn,
            "OVRS_EXCG_CD": ovrs_excg_cd,
            "SORT_SQN": sort_sqn,
            "ORD_DT": ord_dt,
            "ORD_GNO_BRNO": ord_gno_brno,
            "ODNO": odno,
            "CTX_AREA_NK200": ctx_area_nk200,
            "CTX_AREA_FK200": ctx_area_fk200,
        }
        response = self.client._get(
            "/uapi/overseas-stock/v1/trading/inquire-ccnl",
            headers=headers,
            params=params,
        )
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = StockConclusionHistory.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def get_current_balance_by_conclusion(
        self,
        cano: str,
        acnt_prdt_cd: str,
        wcrc_frcr_dvsn_cd: str,
        natn_cd: str,
        tr_mket_cd: str,
        inqr_dvsn_cd: str,
    ) -> KisHttpResponse[CurrentBalanceByConclusion]:
        """해외주식 체결기준현재잔고

        Args:
            cano (str): 종합계좌번호 (8자리)
            acnt_prdt_cd (str): 계좌상품코드 (2자리)
            wcrc_frcr_dvsn_cd (str): 원화외화구분코드 (01: 원화, 02: 외화)
            natn_cd (str): 국가코드 (000: 전체, 840: 미국, 344: 홍콩, 156: 중국, 392: 일본, 704: 베트남)
            tr_mket_cd (str): 거래시장코드 (00: 전체, 01: 나스닥, 02: 뉴욕거래소, 03: PINK SHEETS, 04: OTCBB, 05: 아멕스 등)
            inqr_dvsn_cd (str): 조회구분코드 (00: 전체, 01: 일반해외주식, 02: 미니스탁)

        Returns:
            CurrentBalanceByConclusion: 해외주식 체결기준현재잔고 응답 객체
        """
        headers = {
            "tr_id": "CTRP6504R",
        }
        params = {
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "WCRC_FRCR_DVSN_CD": wcrc_frcr_dvsn_cd,
            "NATN_CD": natn_cd,
            "TR_MKET_CD": tr_mket_cd,
            "INQR_DVSN_CD": inqr_dvsn_cd,
        }
        response = self.client._get(
            "/uapi/overseas-stock/v1/trading/inquire-present-balance",
            headers=headers,
            params=params,
        )
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = CurrentBalanceByConclusion.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def get_reserve_orders(
        self,
        cano: str,
        acnt_prdt_cd: str,
        inqr_strt_dt: str,
        inqr_end_dt: str,
        inqr_dvsn_cd: str,
        prdt_type_cd: str,
        ovrs_excg_cd: str,
        ctx_area_fk200: str = "",
        ctx_area_nk200: str = "",
    ) -> KisHttpResponse[ReserveOrders]:
        """해외주식 예약주문조회

        Args:
            cano (str): 종합계좌번호 (8자리)
            acnt_prdt_cd (str): 계좌상품코드 (2자리)
            inqr_strt_dt (str): 조회시작일자 (YYYYMMDD)
            inqr_end_dt (str): 조회종료일자 (YYYYMMDD)
            inqr_dvsn_cd (str): 조회구분코드 (00: 전체, 01: 일반해외주식, 02: 미니스탁)
            prdt_type_cd (str): 상품유형코드 (512: 미국 나스닥, 513: 미국 뉴욕거래소, 529: 미국 아멕스, 515: 일본, 501: 홍콩, 543: 홍콩CNY, 558: 홍콩USD, 507: 베트남 하노이거래소, 508: 베트남 호치민거래소, 551: 중국 상해A, 552: 중국 심천A)
            ovrs_excg_cd (str): 해외거래소코드 (NASD: 나스닥, NYSE: 뉴욕, AMEX: 아멕스, SEHK: 홍콩, SHAA: 중국상해, SZAA: 중국심천, TKSE: 일본, HASE: 하노이거래소, VNSE: 호치민거래소)
            ctx_area_fk200 (str): 연속조회검색조건200 (최초 조회시 공란, 다음페이지 조회시 이전 조회 Output 값)
            ctx_area_nk200 (str): 연속조회키200 (최초 조회시 공란, 다음페이지 조회시 이전 조회 Output 값)

        Returns:
            ReserveOrders: 해외주식 예약주문조회 응답 객체
        """
        headers = {
            "tr_id": "TTTT3039R",
        }
        params = {
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "INQR_STRT_DT": inqr_strt_dt,
            "INQR_END_DT": inqr_end_dt,
            "INQR_DVSN_CD": inqr_dvsn_cd,
            "PRDT_TYPE_CD": prdt_type_cd,
            "OVRS_EXCG_CD": ovrs_excg_cd,
            "CTX_AREA_FK200": ctx_area_fk200,
            "CTX_AREA_NK200": ctx_area_nk200,
        }
        response = self.client._get(
            "/uapi/overseas-stock/v1/trading/order-resv-list",
            headers=headers,
            params=params,
        )
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = ReserveOrders.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def get_balance_by_settlement(
        self,
        cano: str,
        acnt_prdt_cd: str,
        bass_dt: str,
        wcrc_frcr_dvsn_cd: str,
        inqr_dvsn_cd: str,
    ) -> KisHttpResponse[BalanceBySettlement]:
        """해외주식 결제기준잔고

        Args:
            cano (str): 종합계좌번호 (8자리)
            acnt_prdt_cd (str): 계좌상품코드 (2자리)
            bass_dt (str): 기준일자 (YYYYMMDD)
            wcrc_frcr_dvsn_cd (str): 원화외화구분코드 (01: 원화기준, 02: 외화기준)
            inqr_dvsn_cd (str): 조회구분코드 (00: 전체, 01: 일반, 02: 미니스탁)

        Returns:
            BalanceBySettlement: 해외주식 결제기준잔고 응답 객체
        """
        headers = {
            "tr_id": "CTRP6010R",
        }
        params = {
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "BASS_DT": bass_dt,
            "WCRC_FRCR_DVSN_CD": wcrc_frcr_dvsn_cd,
            "INQR_DVSN_CD": inqr_dvsn_cd,
        }
        response = self.client._get(
            "/uapi/overseas-stock/v1/trading/inquire-paymt-stdr-balance",
            headers=headers,
            params=params,
        )
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = BalanceBySettlement.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def get_daily_transaction_history(
        self,
        cano: str,
        acnt_prdt_cd: str,
        erlm_strt_dt: str,
        erlm_end_dt: str,
        ovrs_excg_cd: str,
        pdno: str,
        sll_buy_dvsn_cd: str,
        loan_dvsn_cd: str,
        ctx_area_fk100: str = "",
        ctx_area_nk100: str = "",
    ) -> KisHttpResponse[DailyTransactionHistory]:
        """해외주식 일별거래내역

        Args:
            cano (str): 종합계좌번호 (8자리)
            acnt_prdt_cd (str): 계좌상품코드 (2자리)
            erlm_strt_dt (str): 등록시작일자 (YYYYMMDD)
            erlm_end_dt (str): 등록종료일자 (YYYYMMDD)
            ovrs_excg_cd (str): 해외거래소코드 (공백: 전체)
            pdno (str): 상품번호 (공백: 전체조회, 개별종목 조회는 상품번호입력)
            sll_buy_dvsn_cd (str): 매도매수구분코드 (00: 전체, 01: 매도, 02: 매수)
            loan_dvsn_cd (str): 대출구분코드 (공백)
            ctx_area_fk100 (str): 연속조회검색조건100 (최초 조회시 공란)
            ctx_area_nk100 (str): 연속조회키100 (최초 조회시 공란)

        Returns:
            DailyTransactionHistory: 해외주식 일별거래내역 응답 객체
        """
        headers = {
            "tr_id": "CTOS4001R",
        }
        params = {
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "ERLM_STRT_DT": erlm_strt_dt,
            "ERLM_END_DT": erlm_end_dt,
            "OVRS_EXCG_CD": ovrs_excg_cd,
            "PDNO": pdno,
            "SLL_BUY_DVSN_CD": sll_buy_dvsn_cd,
            "LOAN_DVSN_CD": loan_dvsn_cd,
            "CTX_AREA_FK100": ctx_area_fk100,
            "CTX_AREA_NK100": ctx_area_nk100,
        }
        response = self.client._get(
            "/uapi/overseas-stock/v1/trading/inquire-period-trans",
            headers=headers,
            params=params,
        )
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = DailyTransactionHistory.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def get_period_profit_loss(
        self,
        cano: str,
        acnt_prdt_cd: str,
        ovrs_excg_cd: str,
        natn_cd: str,
        crcy_cd: str,
        pdno: str,
        inqr_strt_dt: str,
        inqr_end_dt: str,
        wcrc_frcr_dvsn_cd: str,
        ctx_area_fk200: str = "",
        ctx_area_nk200: str = "",
    ) -> KisHttpResponse[PeriodProfitLoss]:
        """해외주식 기간손익

        Args:
            cano (str): 종합계좌번호 (8자리)
            acnt_prdt_cd (str): 계좌상품코드 (2자리)
            ovrs_excg_cd (str): 해외거래소코드 (공란: 전체, NASD: 미국, SEHK: 홍콩, SHAA: 중국, TKSE: 일본, HASE: 베트남)
            natn_cd (str): 국가코드 (공란)
            crcy_cd (str): 통화코드 (공란: 전체, USD: 미국달러, HKD: 홍콩달러, CNY: 중국위안화, JPY: 일본엔화, VND: 베트남동)
            pdno (str): 상품번호 (공란: 전체)
            inqr_strt_dt (str): 조회시작일자 (YYYYMMDD)
            inqr_end_dt (str): 조회종료일자 (YYYYMMDD)
            wcrc_frcr_dvsn_cd (str): 원화외화구분코드 (01: 외화, 02: 원화)
            ctx_area_fk200 (str): 연속조회검색조건200 (최초 조회시 공란)
            ctx_area_nk200 (str): 연속조회키200 (최초 조회시 공란)

        Returns:
            PeriodProfitLoss: 해외주식 기간손익 응답 객체
        """
        headers = {
            "tr_id": "TTTS3039R",
        }
        params = {
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "OVRS_EXCG_CD": ovrs_excg_cd,
            "NATN_CD": natn_cd,
            "CRCY_CD": crcy_cd,
            "PDNO": pdno,
            "INQR_STRT_DT": inqr_strt_dt,
            "INQR_END_DT": inqr_end_dt,
            "WCRC_FRCR_DVSN_CD": wcrc_frcr_dvsn_cd,
            "CTX_AREA_FK200": ctx_area_fk200,
            "CTX_AREA_NK200": ctx_area_nk200,
        }
        response = self.client._get(
            "/uapi/overseas-stock/v1/trading/inquire-period-profit",
            headers=headers,
            params=params,
        )
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = PeriodProfitLoss.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def get_margin_aggregate(
        self,
        cano: str,
        acnt_prdt_cd: str,
    ) -> KisHttpResponse[MarginAggregate]:
        """해외증거금 통합변조회

        Args:
            cano (str): 종합계좌번호 (8자리)
            acnt_prdt_cd (str): 계좌상품코드 (2자리)

        Returns:
            MarginAggregate: 해외증거금 통합변조회 응답 객체
        """
        headers = {
            "tr_id": "TTTC2101R",
        }
        params = {
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
        }
        response = self.client._get(
            "/uapi/overseas-stock/v1/trading/foreign-margin",
            headers=headers,
            params=params,
        )
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = MarginAggregate.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def request_order_after_day_time(
        self,
        cano: str,
        acnt_prdt_cd: str,
        ovrs_excg_cd: str,
        pdno: str,
        ord_qty: str,
        ovrs_ord_unpr: str,
        ord_dvsn: str,
        ctac_tlno: str = "",
        mgco_aptm_odno: str = "",
        ord_svr_dvsn_cd: str = "0",
    ) -> KisHttpResponse[OrderAfterDayTime]:
        """해외주식 미국주간주문

        Args:
            cano (str): 종합계좌번호 (8자리)
            acnt_prdt_cd (str): 계좌상품코드 (2자리)
            ovrs_excg_cd (str): 해외거래소코드 (NASD: 나스닥, NYSE: 뉴욕, AMEX: 아멕스)
            pdno (str): 상품번호 (종목코드)
            ord_qty (str): 주문수량
            ovrs_ord_unpr (str): 해외주문단가 (소수점 포함, 1주당 가격, 시장가의 경우 "0"으로 입력)
            ord_dvsn (str): 주문구분 (00: 지정가, 주간거래는 지정가만 가능)
            ctac_tlno (str): 연락전화번호 (공백)
            mgco_aptm_odno (str): 운용사지정주문번호 (공백)
            ord_svr_dvsn_cd (str): 주문서버구분코드 (기본값 "0")

        Returns:
            OrderAfterDayTime: 해외주식 미국주간주문 응답 객체
        """
        headers = {
            "tr_id": "TTTS6036U",
        }
        body = {
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "OVRS_EXCG_CD": ovrs_excg_cd,
            "PDNO": pdno,
            "ORD_QTY": ord_qty,
            "OVRS_ORD_UNPR": ovrs_ord_unpr,
            "CTAC_TLNO": ctac_tlno,
            "MGCO_APTM_ODNO": mgco_aptm_odno,
            "ORD_SVR_DVSN_CD": ord_svr_dvsn_cd,
            "ORD_DVSN": ord_dvsn,
        }
        response = self.client._post(
            "/uapi/overseas-stock/v1/trading/daytime-order",
            headers=headers,
            body=body,
        )
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = OrderAfterDayTime.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def cancel_correct_after_day_time(
        self,
        cano: str,
        acnt_prdt_cd: str,
        ovrs_excg_cd: str,
        pdno: str,
        orgn_odno: str,
        rvse_cncl_dvsn_cd: str,
        ord_qty: str,
        ovrs_ord_unpr: str,
        ctac_tlno: str = "",
        mgco_aptm_odno: str = "",
        ord_svr_dvsn_cd: str = "0",
    ) -> KisHttpResponse[CorrectAfterDayTime]:
        """해외주식 미국주간정정취소

        Args:
            cano (str): 종합계좌번호 (8자리)
            acnt_prdt_cd (str): 계좌상품코드 (2자리)
            ovrs_excg_cd (str): 해외거래소코드 (NASD: 나스닥, NYSE: 뉴욕, AMEX: 아멕스)
            pdno (str): 상품번호 (종목코드)
            orgn_odno (str): 원주문번호 (정정 또는 취소할 원주문번호)
            rvse_cncl_dvsn_cd (str): 정정취소구분코드 (01: 정정, 02: 취소)
            ord_qty (str): 주문수량
            ovrs_ord_unpr (str): 해외주문단가 (소수점 포함, 1주당 가격)
            ctac_tlno (str): 연락전화번호 (공백)
            mgco_aptm_odno (str): 운용사지정주문번호 (공백)
            ord_svr_dvsn_cd (str): 주문서버구분코드 (기본값 "0")

        Returns:
            CorrectCancelAfterDayTime: 해외주식 미국주간정정취소 응답 객체
        """
        headers = {
            "tr_id": "TTTS6038U",
        }
        body = {
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "OVRS_EXCG_CD": ovrs_excg_cd,
            "PDNO": pdno,
            "ORGN_ODNO": orgn_odno,
            "RVSE_CNCL_DVSN_CD": rvse_cncl_dvsn_cd,
            "ORD_QTY": ord_qty,
            "OVRS_ORD_UNPR": ovrs_ord_unpr,
            "CTAC_TLNO": ctac_tlno,
            "MGCO_APTM_ODNO": mgco_aptm_odno,
            "ORD_SVR_DVSN_CD": ord_svr_dvsn_cd,
        }
        response = self.client._post(
            "/uapi/overseas-stock/v1/trading/daytime-order-rvsecncl",
            headers=headers,
            body=body,
        )
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = CorrectAfterDayTime.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def get_limit_order_number(
        self,
        trad_dt: str,
        cano: str,
        acno_prdt_cd: str,
        ctx_area_nk200: str = "",
        ctx_area_fk200: str = "",
    ) -> KisHttpResponse[LimitOrderNumber]:
        """해외주식 지정가주문번호조회

        Args:
            trad_dt (str): 거래일자 (YYYYMMDD)
            cano (str): 계좌번호 (종합계좌번호 8자리)
            acno_prdt_cd (str): 계좌상품코드 (2자리, 주식계좌는 01)
            ctx_area_nk200 (str): 연속조회키200 (최초 조회시 공란)
            ctx_area_fk200 (str): 연속조회조건200 (최초 조회시 공란)

        Returns:
            LimitOrderNumber: 해외주식 지정가주문번호조회 응답 객체
        """
        headers = {
            "tr_id": "TTTS6058R",
        }
        params = {
            "TRAD_DT": trad_dt,
            "CANO": cano,
            "ACNO_PRDT_CD": acno_prdt_cd,
            "CTX_AREA_NK200": ctx_area_nk200,
            "CTX_AREA_FK200": ctx_area_fk200,
        }
        response = self.client._get("/uapi/overseas-stock/v1/trading/algo-ordno", headers=headers, params=params)
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = LimitOrderNumber.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def get_limit_order_execution_history(
        self,
        cano: str,
        acnt_prdt_cd: str,
        ord_dt: str,
        odno: str,
        ord_gno_brno: str = "",
        ttlz_icld_yn: str = "",
        ctx_area_nk200: str = "",
        ctx_area_fk200: str = "",
    ) -> KisHttpResponse[LimitOrderExecutionHistory]:
        """해외주식 지정가체결내역조회

        Args:
            cano (str): 계좌번호 (종합계좌번호 8자리)
            acnt_prdt_cd (str): 계좌상품코드 (2자리, 주식계좌: 01)
            ord_dt (str): 주문일자 (YYYYMMDD)
            odno (str): 주문번호 (지정가주문번호 TTTC6058R에서 조회된 주문번호 입력)
            ord_gno_brno (str): 주문채번지점번호 (공란)
            ttlz_icld_yn (str): 집계포함여부 (공란)
            ctx_area_nk200 (str): 연속조회키200 (연속조회 시 사용)
            ctx_area_fk200 (str): 연속조회조건200 (연속조회 시 사용)

        Returns:
            LimitOrderExecutionHistory: 해외주식 지정가체결내역조회 응답 객체
        """
        headers = {
            "tr_id": "TTTS6059R",
        }
        params = {
            "CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "ORD_DT": ord_dt,
            "ORD_GNO_BRNO": ord_gno_brno,
            "ODNO": odno,
            "TTLZ_ICLD_YN": ttlz_icld_yn,
            "CTX_AREA_NK200": ctx_area_nk200,
            "CTX_AREA_FK200": ctx_area_fk200,
        }
        response = self.client._get(
            "/uapi/overseas-stock/v1/trading/inquire-algo-ccnl",
            headers=headers,
            params=params,
        )
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = LimitOrderExecutionHistory.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)
