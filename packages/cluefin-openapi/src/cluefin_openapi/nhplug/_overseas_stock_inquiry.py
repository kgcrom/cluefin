from typing import Any, Dict, Literal, Optional

from cluefin_openapi.nhplug._exceptions import NHPlugAPIError
from cluefin_openapi.nhplug._http_client import HttpClient
from cluefin_openapi.nhplug._model import SUCCESS_RSP_CODES, NHPlugHttpHeader, NHPlugHttpResponse
from cluefin_openapi.nhplug._overseas_stock_inquiry_types import (
    OverseasStockInquiryBalance,
    OverseasStockInquiryBuyableAmount,
    OverseasStockInquiryDailyTransaction,
    OverseasStockInquiryMargin,
    OverseasStockInquiryPeriodPnl,
    OverseasStockInquiryPeriodPnlDetail,
    OverseasStockInquiryReservedInquiry,
    OverseasStockInquiryUnexecuted,
)

# 외화증권거래국가코드 (fc_sec_trd_nat_cd)
ForeignTradeNationCode = Literal[
    "200",  # 미국
    "070",  # 일본
    "120",  # 홍콩
    "160",  # 상해
    "170",  # 심천
]

# 전체(000)를 허용하는 국가코드 — periodPnl 의 fc_sec_trd_nat_cd, reservedInquiry 의 fc_mkt_dit_cd.
ForeignTradeNationCodeWithAll = Literal["000", "200", "070", "120", "160", "170"]

# 거래통화코드 (trd_cur_cd) / 통화코드 (cur_cd) — balance 에서 KRW 는 "전체"를 뜻한다.
TradeCurrencyCode = Literal["KRW", "USD", "CNY", "HKD", "JPY"]

# 현물호가유형코드 (ahi_nmn_pr_tp_cd) — 주문 API 와 코드 집합이 같다.
SpotQuoteTypeCode = Literal[
    "00",  # 지정가
    "03",  # 시장가
    "11",  # LOO(장개시 지정가)
    "12",  # LOC(장마감 지정가)
    "13",  # MOO(장개시 시장가)
    "14",  # MOC(장마감 시장가)
    "15",  # STOP(시장가)
    "16",  # STOP LIMIT(지정가)
    "61",  # 프리마켓(지정가)
    "62",  # 애프터마켓(지정가)
    "63",  # 주간거래(지정가)
    "TW",  # TWAP(시장가)
    "VW",  # VWAP(시장가)
    "TL",  # TWAP(지정가)
    "VL",  # VWAP(지정가)
]

# 신용대출코드 (cfd_lon_cd)
CreditLoanCode = Literal[
    "00",  # 현금
    "19",  # 해외주식담보대출
]


class OverseasStockInquiry:
    """해외주식 조회 (gbstock inquiry).

    스펙 정본: https://www.nhplug.com/openapi-docs/gbstock/openapi.json
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

    def buyable_amount(
        self,
        act_no: str,
        pcs_dit: Literal["1", "2", "3", "4", "5"],
        fc_sec_trd_nat_cd: ForeignTradeNationCode,
        iem_cd: str,
        wtm_cur_knd_cd: Literal["1", "2", "3", "4"],
        oss_orr_knd_cd: Literal["1", "2", "3"],
        ahi_nmn_pr_tp_cd: SpotQuoteTypeCode,
        fc_orr_uit_pr: Optional[float] = None,
        cfd_lon_cd: Optional[CreditLoanCode] = None,
        lon_dt: Optional[str] = None,
        cts: Optional[str] = None,
    ) -> NHPlugHttpResponse[OverseasStockInquiryBuyableAmount]:
        """해외주식 매수가능금액·수량 조회 (`POST /gbstock/inquiry/v1/buyableAmount`).

        처리구분(`pcs_dit`)으로 매수·매도를 모두 조회한다. 국내주식은
        buyableQuantity/sellableQuantity 로 API 가 분리되어 있으나, 해외주식은
        이 API 하나로 통합되어 있다.

        Args:
            act_no: 계좌번호 (길이 11). `/n2/acctinfo` 의 acct_no 사용
                (운영은 acct_type=01·02, 모의투자는 03 계좌만 유효).
            pcs_dit: 처리구분 (1.매수가능금액조회 2.매수가능수량조회 3.매도가능수량조회
                4.예약매수금액/수량 5.예약매도수량)
            fc_sec_trd_nat_cd: 외화증권거래국가코드 (200.미국 070.일본 120.홍콩 160.상해 170.심천)
            iem_cd: 종목코드 (예: 미국주식 APPLE인 경우 AAPL)
            wtm_cur_knd_cd: 증거금통화종류코드 (1.거래국가통화 2.원화 3.기타통화
                4.거래국가통화(통합금거금가능금미포함))
            oss_orr_knd_cd: 해외증권주문종류코드 (1.GTS(미국시장주문) 2.기타자동 3.기타수동)
            ahi_nmn_pr_tp_cd: 현물호가유형코드 (00.지정가 03.시장가 61.프리마켓(지정가)
                62.애프터마켓(지정가) 63.주간거래(지정가) 11.LOO(장개시 지정가) 12.LOC(장마감 지정가)
                13.MOO(장개시 시장가) 14.MOC(장마감 시장가) 15.STOP(시장가) 16.STOP LIMIT(지정가)
                TW.TWAP(시장가) VW.VWAP(시장가) TL.TWAP(지정가) VL.VWAP(지정가))
            fc_orr_uit_pr: 외화주문단가 (소수점 6자리)
            cfd_lon_cd: 신용대출코드 (00.현금 19.해외주식담보대출)
            lon_dt: 대출일자 (YYYYMMDD)
            cts: 연속거래키. 이전 응답 헤더의 `cts` 값을 그대로 전달하면 다음 페이지를 받는다.

        Returns:
            NHPlugHttpResponse[OverseasStockInquiryBuyableAmount]: 매수가능금액·수량(`orr_pbl_amt`,
                `byn_pbl_qty` 등) 및 매도가능수량(`sll_pbl_qty` 등) 조회 결과
        """
        body = self._drop_none(
            {
                "act_no": act_no,
                "pcs_dit": pcs_dit,
                "fc_sec_trd_nat_cd": fc_sec_trd_nat_cd,
                "iem_cd": iem_cd,
                "wtm_cur_knd_cd": wtm_cur_knd_cd,
                "oss_orr_knd_cd": oss_orr_knd_cd,
                "ahi_nmn_pr_tp_cd": ahi_nmn_pr_tp_cd,
                "fc_orr_uit_pr": fc_orr_uit_pr,
                "cfd_lon_cd": cfd_lon_cd,
                "lon_dt": lon_dt,
            }
        )

        response = self.client.post("/gbstock/inquiry/v1/buyableAmount", body=body, cts=cts)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=OverseasStockInquiryBuyableAmount.model_validate(data))

    def unexecuted(
        self,
        orr_dt: str,
        act_no: str,
        oss_sby_dit_cd: Literal["0", "1", "2"],
        sot_dit: Literal["0", "1"],
        ost_cns_dit: Literal["0", "1", "2"],
        iem_cd: Optional[str] = None,
        orr_no: Optional[int] = None,
        cts: Optional[str] = None,
    ) -> NHPlugHttpResponse[OverseasStockInquiryUnexecuted]:
        """해외주식 주문체결내역 (`POST /gbstock/inquiry/v1/unexecuted`).

        주문별 체결수량·체결가격·미체결주문수량을 포함한 주문·체결 내역 조회
        API 이다. URI 의 `unexecuted` 는 서버 경로일 뿐이며, 실제로는 체결·
        미체결 내역을 모두 반환한다 (주문 접수 API 아님, 조회 전용).

        Args:
            orr_dt: 주문일자 (길이 8)
            act_no: 계좌번호 (길이 11). `/n2/acctinfo` 의 acct_no 사용
                (운영은 acct_type=01·02, 모의투자는 03 계좌만 유효).
            oss_sby_dit_cd: 해외증권매매구분코드 (길이 1) (0.전체 1.매도 2.매수)
            sot_dit: 정렬구분 (길이 1) (0.주문번호순 1.주문번호역순)
            ost_cns_dit: 체결구분 (길이 1) (0.전체 1.체결 2.미체결)
            iem_cd: 티커종목코드 (길이 12). 예: 미국주식 APPLE인 경우 AAPL
            orr_no: 주문번호 (길이 10)
            cts: 연속거래키. 이전 응답 헤더의 `cts` 값을 그대로 전달하면 다음 페이지를 받는다.

        Returns:
            NHPlugHttpResponse[OverseasStockInquiryUnexecuted]: 주문·체결 내역 목록(`Output_0`)
        """
        body = self._drop_none(
            {
                "orr_dt": orr_dt,
                "act_no": act_no,
                "oss_sby_dit_cd": oss_sby_dit_cd,
                "sot_dit": sot_dit,
                "ost_cns_dit": ost_cns_dit,
                "iem_cd": iem_cd,
                "orr_no": orr_no,
            }
        )

        response = self.client.post("/gbstock/inquiry/v1/unexecuted", body=body, cts=cts)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=OverseasStockInquiryUnexecuted.model_validate(data))

    def balance(
        self,
        act_no: str,
        qut_iqr_dit_cd: Literal["1", "9"],
        fc_sec_trd_nat_cd: ForeignTradeNationCode,
        cur_cd: TradeCurrencyCode,
        xns_dit_cd: Optional[Literal["0", "1"]] = None,
        cts: Optional[str] = None,
    ) -> NHPlugHttpResponse[OverseasStockInquiryBalance]:
        """해외주식 잔고 (`POST /gbstock/inquiry/v1/balance`).

        계좌의 해외주식 잔고 요약(`Output_0`)과 종목별 잔고 목록(`Output_1`)을
        조회하는 API 이다. 응답 블록은 데이터가 있을 때만 내려온다.

        Args:
            act_no: 계좌번호 (길이 11). `/n2/acctinfo` 의 acct_no 사용
                (운영은 acct_type=01·02, 모의투자는 03 계좌만 유효).
            qut_iqr_dit_cd: 시세조회구분코드 (길이 1) (1.정규장 9.전체)
            fc_sec_trd_nat_cd: 외화증권거래국가코드 (길이 3) (200.미국 070.일본 120.홍콩
                160.상해 170.심천)
            cur_cd: 통화코드 (길이 3) (KRW.전체 USD.USD CNY.CNY HKD.HKD JPY.JPY)
            xns_dit_cd: 비용구분코드 (길이 1) (0.미포함 1.포함)
            cts: 연속거래키. 이전 응답 헤더의 `cts` 값을 그대로 전달하면 다음 페이지를 받는다.

        Returns:
            NHPlugHttpResponse[OverseasStockInquiryBalance]: 잔고 요약(`Output_0`) 및
                종목별 잔고 목록(`Output_1`) 조회 결과
        """
        body = self._drop_none(
            {
                "act_no": act_no,
                "qut_iqr_dit_cd": qut_iqr_dit_cd,
                "fc_sec_trd_nat_cd": fc_sec_trd_nat_cd,
                "cur_cd": cur_cd,
                "xns_dit_cd": xns_dit_cd,
            }
        )

        response = self.client.post("/gbstock/inquiry/v1/balance", body=body, cts=cts)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=OverseasStockInquiryBalance.model_validate(data))

    def reserved_inquiry(
        self,
        fc_mkt_dit_cd: ForeignTradeNationCodeWithAll,
        bkg_orr_dt: str,
        act_no: str,
        sby_dit_cd: Literal["0", "1", "2"],
        bkg_orr_can_yn: Literal["0", "1", "2", "3", "4", "5", "6", "7"],
        oss_orr_knd_cd: Literal["0", "1", "2", "3"],
        bkg_orr_tp_cd: Literal["0", "1", "2", "3", "4"],
        wtm_cur_knd_cd: Literal["0", "1", "2"],
        iem_cd: Optional[str] = None,
        cts: Optional[str] = None,
    ) -> NHPlugHttpResponse[OverseasStockInquiryReservedInquiry]:
        """해외주식 예약주문조회 (`POST /gbstock/inquiry/v1/reservedInquiry`).

        해외주식 예약주문내역을 조회하는 API 이다. 응답 블록은 데이터가 있을
        때만 내려온다.

        Args:
            fc_mkt_dit_cd: 외화시장구분코드 (길이 3) (000.전체 200.미국 070.일본 120.홍콩
                160.상해 170.심천)
            bkg_orr_dt: 예약주문일자 (길이 8) (YYYYMMDD)
            act_no: 계좌번호 (길이 11). `/n2/acctinfo` 의 acct_no 사용
                (운영은 acct_type=01·02, 모의투자는 03 계좌만 유효).
            sby_dit_cd: 매매구분코드 (길이 1) (0.전체 1.매도 2.매수)
            bkg_orr_can_yn: 예약주문취소여부 (길이 1) (0.전체 1.접수 2.취소 3.주문전송
                4.주문확인 5.실행거부 6.실행거부(현지) 7.완료)
            oss_orr_knd_cd: 해외증권주문종류코드 (길이 1) (0.전체 1.GTS(미국시장주문)
                2.기타자동 3.기타수동)
            bkg_orr_tp_cd: 예약주문유형코드 (길이 1) (0.전체 1.일반예약 2.기간잔량
                3.기간지정 4.증거금징수)
            wtm_cur_knd_cd: 증거금통화종류코드 (길이 1) (0.전체 1.거래국가통화 2.원화)
            iem_cd: 티커종목코드 (길이 12). 예: 미국주식 APPLE인 경우 AAPL
            cts: 연속거래키. 이전 응답 헤더의 `cts` 값을 그대로 전달하면 다음 페이지를 받는다.

        Returns:
            NHPlugHttpResponse[OverseasStockInquiryReservedInquiry]: 예약주문내역
                목록(`Output_0`) 조회 결과
        """
        body = self._drop_none(
            {
                "fc_mkt_dit_cd": fc_mkt_dit_cd,
                "bkg_orr_dt": bkg_orr_dt,
                "act_no": act_no,
                "sby_dit_cd": sby_dit_cd,
                "bkg_orr_can_yn": bkg_orr_can_yn,
                "oss_orr_knd_cd": oss_orr_knd_cd,
                "bkg_orr_tp_cd": bkg_orr_tp_cd,
                "wtm_cur_knd_cd": wtm_cur_knd_cd,
                "iem_cd": iem_cd,
            }
        )

        response = self.client.post("/gbstock/inquiry/v1/reservedInquiry", body=body, cts=cts)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=OverseasStockInquiryReservedInquiry.model_validate(data))

    def daily_transaction(
        self,
        act_no: str,
        iqr_sta_dt: str,
        iqr_end_dt: str,
        act_trd_cfc_cd: Literal["00", "01", "02", "03", "04", "05", "06"],
        iem_mlf_cd: Literal["00001", "00002", "00003", "00004", "00005"],
        iem_cd: Optional[str] = None,
        cts: Optional[str] = None,
    ) -> NHPlugHttpResponse[OverseasStockInquiryDailyTransaction]:
        """해외주식 일별거래내역 (`POST /gbstock/inquiry/v1/dailyTransaction`).

        조회기간 내 계좌의 해외주식 거래내역 목록(`Output_0`)과 거래내역
        요약(`Output_1`)을 조회하는 API 이다. 응답 블록은 데이터가 있을
        때만 내려온다.

        Args:
            act_no: 계좌번호 (길이 11). `/n2/acctinfo` 의 acct_no 사용
                (운영은 acct_type=01·02, 모의투자는 03 계좌만 유효).
            iqr_sta_dt: 조회시작일자 (길이 8) (YYYYMMDD)
            iqr_end_dt: 조회종료일자 (길이 8) (YYYYMMDD)
            act_trd_cfc_cd: 계좌거래분류코드 (길이 2) (00.전체 01.입금 02.출금 03.입고
                04.출고 05.매수 06.매도)
            iem_mlf_cd: 종목중분류코드 (길이 5) (00001.외화주식 00002.외화채권
                00003.외화Warrant 00004.외화수익증권 00005.해외수익증권)
            iem_cd: 종목코드 (길이 12). 예: 미국주식 APPLE인 경우 AAPL
            cts: 연속거래키. 이전 응답 헤더의 `cts` 값을 그대로 전달하면 다음 페이지를 받는다.

        Returns:
            NHPlugHttpResponse[OverseasStockInquiryDailyTransaction]: 일별거래내역
                목록(`Output_0`) 및 요약(`Output_1`) 조회 결과
        """
        body = self._drop_none(
            {
                "act_no": act_no,
                "iqr_sta_dt": iqr_sta_dt,
                "iqr_end_dt": iqr_end_dt,
                "act_trd_cfc_cd": act_trd_cfc_cd,
                "iem_mlf_cd": iem_mlf_cd,
                "iem_cd": iem_cd,
            }
        )

        response = self.client.post("/gbstock/inquiry/v1/dailyTransaction", body=body, cts=cts)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=OverseasStockInquiryDailyTransaction.model_validate(data))

    def period_pnl(
        self,
        act_no: str,
        iqr_dit: Literal["1", "2"],
        sta_orr_dt: str,
        end_orr_dt: str,
        iem_cd: Optional[str] = None,
        trd_cur_cd: Optional[TradeCurrencyCode] = None,
        fc_sec_trd_nat_cd: Optional[ForeignTradeNationCodeWithAll] = None,
        cts: Optional[str] = None,
    ) -> NHPlugHttpResponse[OverseasStockInquiryPeriodPnl]:
        """해외주식 기간손익 (`POST /gbstock/inquiry/v1/periodPnl`).

        조회기간 내 계좌의 해외주식 기간별 손익 요약(`Output_0`)과 주문일자별
        손익 목록(`Output_1`)을 조회하는 API 이다. 응답 블록은 데이터가 있을
        때만 내려온다.

        Args:
            act_no: 계좌번호 (길이 11). `/n2/acctinfo` 의 acct_no 사용
                (운영은 acct_type=01·02, 모의투자는 03 계좌만 유효).
            iqr_dit: 조회구분 (길이 1) (1.거래통화기준 2.원화기준)
            sta_orr_dt: 시작주문일자 (길이 8) (YYYYMMDD)
            end_orr_dt: 종료주문일자 (길이 8) (YYYYMMDD)
            iem_cd: 티커종목코드 (길이 12). 예: 미국주식 APPLE인 경우 AAPL
            trd_cur_cd: 거래통화코드 (길이 3) (KRW.KRW USD.USD CNY.CNY HKD.HKD JPY.JPY)
            fc_sec_trd_nat_cd: 외화증권거래국가코드 (길이 3) (000.전체 200.미국 070.일본
                120.홍콩 160.상해 170.심천)
            cts: 연속거래키. 이전 응답 헤더의 `cts` 값을 그대로 전달하면 다음 페이지를 받는다.

        Returns:
            NHPlugHttpResponse[OverseasStockInquiryPeriodPnl]: 기간손익 요약(`Output_0`) 및
                주문일자별 손익 목록(`Output_1`) 조회 결과
        """
        body = self._drop_none(
            {
                "act_no": act_no,
                "iqr_dit": iqr_dit,
                "sta_orr_dt": sta_orr_dt,
                "end_orr_dt": end_orr_dt,
                "iem_cd": iem_cd,
                "trd_cur_cd": trd_cur_cd,
                "fc_sec_trd_nat_cd": fc_sec_trd_nat_cd,
            }
        )

        response = self.client.post("/gbstock/inquiry/v1/periodPnl", body=body, cts=cts)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=OverseasStockInquiryPeriodPnl.model_validate(data))

    def period_pnl_detail(
        self,
        act_no: str,
        iqr_dit: Literal["1", "2"],
        orr_dt: str,
        fc_sec_trd_nat_cd: ForeignTradeNationCode,
        trd_cur_cd: TradeCurrencyCode,
        iem_cd: Optional[str] = None,
        cts: Optional[str] = None,
    ) -> NHPlugHttpResponse[OverseasStockInquiryPeriodPnlDetail]:
        """해외주식 기간손익 상세 (`POST /gbstock/inquiry/v1/periodPnlDetail`).

        지정한 주문일자의 종목별 해외주식 손익 상세 목록(`Output_0`)을 조회하는
        API 이다. 응답 블록은 데이터가 있을 때만 내려온다.

        Args:
            act_no: 계좌번호 (길이 11). `/n2/acctinfo` 의 acct_no 사용
                (운영은 acct_type=01·02, 모의투자는 03 계좌만 유효).
            iqr_dit: 조회구분 (길이 1) (1.거래통화기준 2.원화기준)
            orr_dt: 주문일자 (길이 8) (YYYYMMDD)
            fc_sec_trd_nat_cd: 외화증권거래국가코드 (길이 3) (200.미국 070.일본 120.홍콩
                160.상해 170.심천)
            trd_cur_cd: 거래통화코드 (길이 3) (KRW.KRW USD.USD CNY.CNY HKD.HKD JPY.JPY)
            iem_cd: 티커종목코드 (길이 12). 예: 미국주식 APPLE인 경우 AAPL
            cts: 연속거래키. 이전 응답 헤더의 `cts` 값을 그대로 전달하면 다음 페이지를 받는다.

        Returns:
            NHPlugHttpResponse[OverseasStockInquiryPeriodPnlDetail]: 기간손익 상세
                목록(`Output_0`) 조회 결과
        """
        body = self._drop_none(
            {
                "act_no": act_no,
                "iqr_dit": iqr_dit,
                "orr_dt": orr_dt,
                "fc_sec_trd_nat_cd": fc_sec_trd_nat_cd,
                "trd_cur_cd": trd_cur_cd,
                "iem_cd": iem_cd,
            }
        )

        response = self.client.post("/gbstock/inquiry/v1/periodPnlDetail", body=body, cts=cts)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=OverseasStockInquiryPeriodPnlDetail.model_validate(data))

    def margin(
        self,
        act_no: str,
        cts: Optional[str] = None,
    ) -> NHPlugHttpResponse[OverseasStockInquiryMargin]:
        """해외증거금 통화별조회 (`POST /gbstock/inquiry/v1/margin`).

        계좌의 통화별 해외주식 증거금 목록(`Output_0`)을 조회하는 API 이다.
        응답 블록은 데이터가 있을 때만 내려온다.

        Args:
            act_no: 계좌번호 (길이 11). `/n2/acctinfo` 의 acct_no 사용
                (운영은 acct_type=01·02, 모의투자는 03 계좌만 유효).
            cts: 연속거래키. 이전 응답 헤더의 `cts` 값을 그대로 전달하면 다음 페이지를 받는다.

        Returns:
            NHPlugHttpResponse[OverseasStockInquiryMargin]: 통화별 증거금 목록(`Output_0`) 조회 결과
        """
        body = self._drop_none({"act_no": act_no})

        response = self.client.post("/gbstock/inquiry/v1/margin", body=body, cts=cts)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=OverseasStockInquiryMargin.model_validate(data))
