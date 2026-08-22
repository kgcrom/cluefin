from typing import Any, Dict, Literal, Optional

from cluefin_openapi.nhplug._exceptions import NHPlugAPIError
from cluefin_openapi.nhplug._http_client import HttpClient
from cluefin_openapi.nhplug._krstock_inquiry_types import (
    KrStockInquiryBalance,
    KrStockInquiryDailyOrderExecution,
)
from cluefin_openapi.nhplug._model import SUCCESS_RSP_CODES, NHPlugHttpHeader, NHPlugHttpResponse


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
