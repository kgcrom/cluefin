from typing import Any, Dict, Literal, Optional

from cluefin_openapi.nhplug._exceptions import NHPlugAPIError
from cluefin_openapi.nhplug._http_client import HttpClient
from cluefin_openapi.nhplug._krstock_inquiry_types import (
    KrStockInquiryAssetStatus,
    KrStockInquiryBalance,
    KrStockInquiryBuyableQuantity,
    KrStockInquiryDailyOrderExecution,
    KrStockInquiryDailyPnl,
    KrStockInquiryIntegratedMargin,
    KrStockInquiryRealizedPnl,
    KrStockInquiryReservedInquiry,
    KrStockInquirySellableQuantity,
    KrStockInquiryTradingPnl,
)
from cluefin_openapi.nhplug._krstock_order import CreditLoanCode, QuoteTypeCode, ReservedCreditLoanCode
from cluefin_openapi.nhplug._model import SUCCESS_RSP_CODES, NHPlugHttpHeader, NHPlugHttpResponse

# 매도가능수량조회(sellableQuantity)의 신용대출코드 — buyableQuantity/신규주문 계열과
# 코드 집합이 다르다(00.일반거래 포함, 01~04 만 유효 — 10 이상은 스펙에 없음).
SellableCreditLoanCode = Literal[
    "00",  # 일반거래
    "01",  # 유통융자
    "02",  # 자기융자
    "03",  # 유통대주
    "04",  # 자기대주
]

# 예약주문조회(reservedInquiry)의 매매구분코드 — reserved_order/reserved_cancel 의
# sby_dit_cd("1"/"2")와 달리 "0.전체"가 있다.
ReservedInquiryTradeTypeCode = Literal[
    "0",  # 전체
    "1",  # 매도
    "2",  # 매수
]

# 예약주문조회(reservedInquiry)의 예약주문유형코드 — reserved_order/reserved_cancel 의
# bkg_orr_tp_cd("1"/"2"/"3")와 달리 "0.전체"가 있다.
ReservedInquiryOrderTypeCode = Literal[
    "0",  # 전체
    "1",  # 일반예약(현금/대출예약)
    "2",  # 기간예약(잔량예약)
    "3",  # 기간예약(수량예약)
]


class KrStockInquiry:
    """국내주식 조회.

    스펙 정본: https://www.nhplug.com/openapi-docs/krstock/openapi.json
    """

    def __init__(self, client: HttpClient):
        self.client = client

    def _check_response_error(self, response_data: dict) -> None:
        """HTTP 200 이어도 body rsp_cd 가 실패일 수 있으므로 여기서 확인한다."""
        rsp_cd = response_data.get("rsp_cd")
        if rsp_cd is not None and rsp_cd not in SUCCESS_RSP_CODES:
            raise NHPlugAPIError(
                f"API error {rsp_cd}: {response_data.get('rsp_msg', '')}",
                status_code=200,
                response_data=response_data,
            )

    @staticmethod
    def _drop_none(body: Dict[str, Any]) -> Dict[str, Any]:
        """선택 파라미터는 값이 있을 때만 전송한다."""
        return {k: v for k, v in body.items() if v is not None}

    def balance(
        self,
        act_no: str,
        bnc_bse_cd: Literal["1", "5"],
        ltg_aot_dit_cd: Literal["1", "9"],
        aet_bse: Literal["1", "2"],
        qut_dit_cd: Literal["UNT", "KRX", "NXT"],
        cts: Optional[str] = None,
    ) -> NHPlugHttpResponse[KrStockInquiryBalance]:
        """주식잔고조회 (`POST /krstock/inquiry/v1/balance`).

        스펙상 5개 입력 필드가 모두 required 다. 연속조회를 지원하는 조회 API 다 —
        응답 헤더 `cts_flag` 가 "Y" 면 그 `cts` 값을 다음 호출의 `cts` 인자로 전달해
        이어받는다.

        Args:
            act_no: 계좌번호 (`/n2/acctinfo` 의 acct_no — 운영은 acct_type 01·02,
                모의투자는 03 계좌만 유효)
            bnc_bse_cd: 잔고기준코드 (1.주식관련 총 평가(체결기준) 5.주식잔고평가(현재가기준))
            ltg_aot_dit_cd: 상장폐지구분코드 (1.상장종목 9.전체)
            aet_bse: 자산기준 (1.순자산 2.총자산)
            qut_dit_cd: 시세구분코드 (UNT.통합시세 KRX.KRX시세 NXT.NXT시세)
            cts: 연속거래키. 이전 응답 헤더 `cts_flag` 가 "Y" 면 그 `cts` 값을 전달.
        """
        body = self._drop_none(
            {
                "act_no": act_no,
                "bnc_bse_cd": bnc_bse_cd,
                "ltg_aot_dit_cd": ltg_aot_dit_cd,
                "aet_bse": aet_bse,
                "qut_dit_cd": qut_dit_cd,
            }
        )
        response = self.client.post("/krstock/inquiry/v1/balance", body=body, cts=cts)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=KrStockInquiryBalance.model_validate(data))

    def daily_order_execution(
        self,
        act_no: str,
        orr_dt: str,
        ost_cns_dit: Literal["0", "1", "2"],
        itg_orr_no: Optional[int] = None,
        orr_mkt_cd: Optional[Literal["00", "01", "02", "03", "06"]] = None,
        cts: Optional[str] = None,
    ) -> NHPlugHttpResponse[KrStockInquiryDailyOrderExecution]:
        """주식일별주문체결조회 (`POST /krstock/inquiry/v1/dailyOrderExecution`).

        연속조회를 지원하는 조회 API 다 — 응답 헤더 `cts_flag` 가 "Y" 면 그 `cts` 값을
        다음 호출의 `cts` 인자로 전달해 이어받는다.

        Args:
            act_no: 계좌번호 (`/n2/acctinfo` 의 acct_no — 운영은 acct_type 01·02,
                모의투자는 03 계좌만 유효)
            orr_dt: 주문일자 (YYYYMMDD)
            ost_cns_dit: 체결구분 (0.전체 1.미체결 2.체결)
            itg_orr_no: 통합주문번호 (특정 주문만 조회할 때)
            orr_mkt_cd: 주문시장코드 (00.전체 01.거래소주식 02.코스닥 03.K-OTC 06.코넥스)
            cts: 연속거래키. 이전 응답 헤더 `cts_flag` 가 "Y" 면 그 `cts` 값을 전달.
        """
        body = self._drop_none(
            {
                "orr_dt": orr_dt,
                "act_no": act_no,
                "itg_orr_no": itg_orr_no,
                "orr_mkt_cd": orr_mkt_cd,
                "ost_cns_dit": ost_cns_dit,
            }
        )
        response = self.client.post("/krstock/inquiry/v1/dailyOrderExecution", body=body, cts=cts)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=KrStockInquiryDailyOrderExecution.model_validate(data))

    def buyable_quantity(
        self,
        act_no: str,
        iem_cd: str,
        ost_dit_cd: Literal["1", "2", "3"],
        nmn_pr_tp_cd: QuoteTypeCode,
        orr_pr: Optional[int] = None,
        cfd_lon_cd: Optional[CreditLoanCode] = None,
        lon_dt: Optional[str] = None,
        cts: Optional[str] = None,
    ) -> NHPlugHttpResponse[KrStockInquiryBuyableQuantity]:
        """매수가능수량조회 (`POST /krstock/inquiry/v1/buyableQuantity`).

        연속조회를 지원하는 조회 API 다 — 응답 헤더 `cts_flag` 가 "Y" 면 그 `cts` 값을
        다음 호출의 `cts` 인자로 전달해 이어받는다.

        Args:
            act_no: 계좌번호 (`/n2/acctinfo` 의 acct_no — 운영은 acct_type 01·02,
                모의투자는 03 계좌만 유효)
            iem_cd: 종목코드 (예: 005940)
            ost_dit_cd: 구분코드 (1.현금 2.신용(융자대주) 3.매입자금대출)
            nmn_pr_tp_cd: 호가유형코드 (01.보통가 05.시장가 16.스톱지정가 등, `cash_buy`
                와 동일한 코드 집합)
            orr_pr: 주문가격 (지정가 계열일 때)
            cfd_lon_cd: 신용대출코드 (구분코드가 "2"인 경우 01.유통융자 02.자기융자
                03.유통대주 04.자기대주)
            lon_dt: 대출일자 (구분코드가 "2"·"3"인 경우, YYYYMMDD)
            cts: 연속거래키. 이전 응답 헤더 `cts_flag` 가 "Y" 면 그 `cts` 값을 전달.
        """
        body = self._drop_none(
            {
                "ost_dit_cd": ost_dit_cd,
                "act_no": act_no,
                "iem_cd": iem_cd,
                "nmn_pr_tp_cd": nmn_pr_tp_cd,
                "orr_pr": orr_pr,
                "cfd_lon_cd": cfd_lon_cd,
                "lon_dt": lon_dt,
            }
        )
        response = self.client.post("/krstock/inquiry/v1/buyableQuantity", body=body, cts=cts)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=KrStockInquiryBuyableQuantity.model_validate(data))

    def sellable_quantity(
        self,
        act_no: str,
        iem_cd: str,
        cfd_lon_cd: SellableCreditLoanCode,
        lon_dt: Optional[str] = None,
        cts: Optional[str] = None,
    ) -> NHPlugHttpResponse[KrStockInquirySellableQuantity]:
        """매도가능수량조회 (`POST /krstock/inquiry/v1/sellableQuantity`).

        연속조회를 지원하는 조회 API 다 — 응답 헤더 `cts_flag` 가 "Y" 면 그 `cts` 값을
        다음 호출의 `cts` 인자로 전달해 이어받는다.

        Args:
            act_no: 계좌번호 (`/n2/acctinfo` 의 acct_no — 운영은 acct_type 01·02,
                모의투자는 03 계좌만 유효)
            iem_cd: 종목코드 (예: 005940)
            cfd_lon_cd: 신용대출코드 (00.일반거래 01.유통융자 02.자기융자 03.유통대주
                04.자기대주)
            lon_dt: 대출일자 (신용대출코드가 "01.유통융자"일 때, YYYYMMDD)
            cts: 연속거래키. 이전 응답 헤더 `cts_flag` 가 "Y" 면 그 `cts` 값을 전달.
        """
        body = self._drop_none(
            {
                "act_no": act_no,
                "iem_cd": iem_cd,
                "lon_dt": lon_dt,
                "cfd_lon_cd": cfd_lon_cd,
            }
        )
        response = self.client.post("/krstock/inquiry/v1/sellableQuantity", body=body, cts=cts)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=KrStockInquirySellableQuantity.model_validate(data))

    def reserved_inquiry(
        self,
        act_no: str,
        sby_dit_cd: ReservedInquiryTradeTypeCode,
        bkg_orr_tp_cd: ReservedInquiryOrderTypeCode,
        bkg_orr_rtn_dt: Optional[str] = None,
        iem_cd: Optional[str] = None,
        cfd_lon_cd: Optional[ReservedCreditLoanCode] = None,
        bkg_orr_can_dit_cd: Optional[Literal["0", "1", "2"]] = None,
        cts: Optional[str] = None,
    ) -> NHPlugHttpResponse[KrStockInquiryReservedInquiry]:
        """주식예약주문조회 (`POST /krstock/inquiry/v1/reservedInquiry`).

        연속조회를 지원하는 조회 API 다 — 응답 헤더 `cts_flag` 가 "Y" 면 그 `cts` 값을
        다음 호출의 `cts` 인자로 전달해 이어받는다. 입력의 `sby_dit_cd`(0.전체/1.매도/
        2.매수)·`bkg_orr_tp_cd`(0.전체/1.일반예약/2.기간예약(잔량)/3.기간예약(수량))는
        `reserved_order`/`reserved_cancel` 이 쓰는 코드 집합과 다르다(그쪽엔 "0.전체"가
        없다) — 이 메서드 전용 Literal 을 쓴다. `cfd_lon_cd` 는 `reserved_order` 와
        코드 집합이 같아 `ReservedCreditLoanCode` 를 재사용한다.

        Args:
            act_no: 계좌번호 (`/n2/acctinfo` 의 acct_no — 운영은 acct_type 01·02,
                모의투자는 03 계좌만 유효, 조회구분 "2"일 때 필요)
            sby_dit_cd: 매매구분코드 (0.전체 1.매도 2.매수)
            bkg_orr_tp_cd: 예약주문유형코드 (0.전체 1.일반예약(현금/대출예약)
                2.기간예약(잔량예약) 3.기간예약(수량예약))
            bkg_orr_rtn_dt: 예약주문접수일자 (YYYYMMDD)
            iem_cd: 종목코드 (예: 005940)
            cfd_lon_cd: 신용대출코드 (00.일반거래 01.유통융자 02.자기융자 03.유통대주
                04.자기대주 10.매입자금대출 11.매도담보대출 12.주식담보대출)
            bkg_orr_can_dit_cd: 예약주문취소구분코드 (0.잔존주문 1.본인취소 2.직원취소,
                생략하면 전체)
            cts: 연속거래키. 이전 응답 헤더 `cts_flag` 가 "Y" 면 그 `cts` 값을 전달.
        """
        body = self._drop_none(
            {
                "bkg_orr_rtn_dt": bkg_orr_rtn_dt,
                "act_no": act_no,
                "iem_cd": iem_cd,
                "sby_dit_cd": sby_dit_cd,
                "cfd_lon_cd": cfd_lon_cd,
                "bkg_orr_tp_cd": bkg_orr_tp_cd,
                "bkg_orr_can_dit_cd": bkg_orr_can_dit_cd,
            }
        )
        response = self.client.post("/krstock/inquiry/v1/reservedInquiry", body=body, cts=cts)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=KrStockInquiryReservedInquiry.model_validate(data))

    def realized_pnl(
        self,
        act_no: str,
        iqr_dit_cd1: Literal["0", "1", "2"],
        fee_dit_cd: Literal["1", "2"],
        qut_dit_cd: Literal["UNT", "KRX", "NXT"],
        cts: Optional[str] = None,
    ) -> NHPlugHttpResponse[KrStockInquiryRealizedPnl]:
        """주식잔고조회_실현손익 (`POST /krstock/inquiry/v1/realizedPnl`).

        스펙상 4개 입력 필드가 모두 required 다. 연속조회를 지원하는 조회 API 다 —
        응답 헤더 `cts_flag` 가 "Y" 면 그 `cts` 값을 다음 호출의 `cts` 인자로 전달해
        이어받는다.

        Args:
            act_no: 계좌번호 (`/n2/acctinfo` 의 acct_no — 운영은 acct_type 01·02,
                모의투자는 03 계좌만 유효)
            iqr_dit_cd1: 조회구분코드1 (0.전체 1.잔고종목 2.당일매매)
            fee_dit_cd: 수수료구분코드 (1.온라인 2.영업점)
            qut_dit_cd: 시세구분코드 (UNT.통합시세 KRX.KRX시세 NXT.NXT시세)
            cts: 연속거래키. 이전 응답 헤더 `cts_flag` 가 "Y" 면 그 `cts` 값을 전달.
        """
        body = self._drop_none(
            {
                "act_no": act_no,
                "iqr_dit_cd1": iqr_dit_cd1,
                "fee_dit_cd": fee_dit_cd,
                "qut_dit_cd": qut_dit_cd,
            }
        )
        response = self.client.post("/krstock/inquiry/v1/realizedPnl", body=body, cts=cts)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=KrStockInquiryRealizedPnl.model_validate(data))

    def asset_status(
        self,
        act_no: str,
        eal_aly_cd: Literal["1", "2"],
        aet_bse: Literal["1", "2"],
        qut_dit_cd: Literal["UNT", "KRX", "NXT"],
        cts: Optional[str] = None,
    ) -> NHPlugHttpResponse[KrStockInquiryAssetStatus]:
        """투자계좌자산현황조회 (`POST /krstock/inquiry/v1/assetStatus`).

        스펙상 4개 입력 필드가 모두 required 다. 연속조회를 지원하는 조회 API 다 —
        응답 헤더 `cts_flag` 가 "Y" 면 그 `cts` 값을 다음 호출의 `cts` 인자로 전달해
        이어받는다.

        Args:
            act_no: 계좌번호 (`/n2/acctinfo` 의 acct_no — 운영은 acct_type 01·02,
                모의투자는 03 계좌만 유효)
            eal_aly_cd: 평가적용코드 (1.장부가평가 2.시가평가)
            aet_bse: 자산기준 (1.순자산 2.총자산)
            qut_dit_cd: 시세구분코드 (UNT.통합시세 KRX.KRX시세 NXT.NXT시세)
            cts: 연속거래키. 이전 응답 헤더 `cts_flag` 가 "Y" 면 그 `cts` 값을 전달.
        """
        body = self._drop_none(
            {
                "act_no": act_no,
                "eal_aly_cd": eal_aly_cd,
                "aet_bse": aet_bse,
                "qut_dit_cd": qut_dit_cd,
            }
        )
        response = self.client.post("/krstock/inquiry/v1/assetStatus", body=body, cts=cts)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=KrStockInquiryAssetStatus.model_validate(data))

    def daily_pnl(
        self,
        act_no: str,
        iqr_sta_dt: str,
        iqr_end_dt: str,
        iem_cd: Optional[str] = None,
        cts: Optional[str] = None,
    ) -> NHPlugHttpResponse[KrStockInquiryDailyPnl]:
        """실현손익일별합산조회 (`POST /krstock/inquiry/v1/dailyPnl`).

        연속조회를 지원하는 조회 API 다 — 응답 헤더 `cts_flag` 가 "Y" 면 그 `cts` 값을
        다음 호출의 `cts` 인자로 전달해 이어받는다.

        Args:
            act_no: 계좌번호 (`/n2/acctinfo` 의 acct_no — 운영은 acct_type 01·02,
                모의투자는 03 계좌만 유효)
            iqr_sta_dt: 조회시작일자 (YYYYMMDD)
            iqr_end_dt: 조회종료일자 (YYYYMMDD)
            iem_cd: 종목코드 (특정 종목만 조회할 때)
            cts: 연속거래키. 이전 응답 헤더 `cts_flag` 가 "Y" 면 그 `cts` 값을 전달.
        """
        body = self._drop_none(
            {
                "act_no": act_no,
                "iem_cd": iem_cd,
                "iqr_sta_dt": iqr_sta_dt,
                "iqr_end_dt": iqr_end_dt,
            }
        )
        response = self.client.post("/krstock/inquiry/v1/dailyPnl", body=body, cts=cts)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=KrStockInquiryDailyPnl.model_validate(data))

    def trading_pnl(
        self,
        act_no: str,
        iqr_sta_dt: str,
        iqr_end_dt: str,
        cts: Optional[str] = None,
    ) -> NHPlugHttpResponse[KrStockInquiryTradingPnl]:
        """종목별실현손익현황조회 (`POST /krstock/inquiry/v1/tradingPnl`).

        스펙상 3개 입력 필드가 모두 required 다(dailyPnl 과 달리 iem_cd 입력이 없다).
        연속조회를 지원하는 조회 API 다 — 응답 헤더 `cts_flag` 가 "Y" 면 그 `cts` 값을
        다음 호출의 `cts` 인자로 전달해 이어받는다.

        Args:
            act_no: 계좌번호 (`/n2/acctinfo` 의 acct_no — 운영은 acct_type 01·02,
                모의투자는 03 계좌만 유효)
            iqr_sta_dt: 조회시작일자 (YYYYMMDD)
            iqr_end_dt: 조회종료일자 (YYYYMMDD)
            cts: 연속거래키. 이전 응답 헤더 `cts_flag` 가 "Y" 면 그 `cts` 값을 전달.
        """
        body = self._drop_none(
            {
                "act_no": act_no,
                "iqr_sta_dt": iqr_sta_dt,
                "iqr_end_dt": iqr_end_dt,
            }
        )
        response = self.client.post("/krstock/inquiry/v1/tradingPnl", body=body, cts=cts)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=KrStockInquiryTradingPnl.model_validate(data))

    def integrated_margin(
        self,
        act_no: str,
        cts: Optional[str] = None,
    ) -> NHPlugHttpResponse[KrStockInquiryIntegratedMargin]:
        """주식통합증거금 현황 (`POST /krstock/inquiry/v1/integratedMargin`).

        스펙상 입력은 `act_no` 하나뿐이다. 연속조회를 지원하는 조회 API 다 —
        응답 헤더 `cts_flag` 가 "Y" 면 그 `cts` 값을 다음 호출의 `cts` 인자로 전달해
        이어받는다.

        Args:
            act_no: 계좌번호 (`/n2/acctinfo` 의 acct_no — 운영은 acct_type 01·02,
                모의투자는 03 계좌만 유효)
            cts: 연속거래키. 이전 응답 헤더 `cts_flag` 가 "Y" 면 그 `cts` 값을 전달.
        """
        body = self._drop_none({"act_no": act_no})
        response = self.client.post("/krstock/inquiry/v1/integratedMargin", body=body, cts=cts)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=KrStockInquiryIntegratedMargin.model_validate(data))
