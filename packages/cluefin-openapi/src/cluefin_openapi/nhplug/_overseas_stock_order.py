from typing import Optional

from cluefin_openapi.nhplug._exceptions import NHPlugAPIError
from cluefin_openapi.nhplug._http_client import HttpClient
from cluefin_openapi.nhplug._model import NHPlugHttpHeader, NHPlugHttpResponse
from cluefin_openapi.nhplug._overseas_stock_order_types import OverseasStockOrderBuy


class OverseasStockOrder:
    """해외주식 주문 (gbstock order).

    스펙 정본: https://www.nhplug.com/openapi-docs/gbstock/openapi.json
    모의투자(dev)는 acct_type=03 계좌, 운영(prod)은 01·02 계좌만 유효하다.
    """

    def __init__(self, client: HttpClient):
        self.client = client

    def _check_response_error(self, response_data: dict) -> None:
        """HTTP 200 이어도 body rsp_cd 가 실패일 수 있으므로 여기서 확인한다."""
        rsp_cd = response_data.get("rsp_cd")
        if rsp_cd is not None and rsp_cd != "00000":
            raise NHPlugAPIError(
                f"API error {rsp_cd}: {response_data.get('rsp_msg', '')}",
                status_code=200,
                response_data=response_data,
            )

    def buy(
        self,
        act_no: str,
        fc_sec_trd_nat_cd: str,
        iem_cd: str,
        orr_qty: int,
        ahi_nmn_pr_tp_cd: str,
        wtm_cur_knd_cd: str,
        fc_orr_uit_pr: Optional[float] = None,
    ) -> NHPlugHttpResponse[OverseasStockOrderBuy]:
        """해외주식 주문매수 (`POST /gbstock/order/v1/buy`).

        Args:
            act_no: 계좌번호. `/n2/acctinfo` 의 acct_no 사용.
            fc_sec_trd_nat_cd: 외화증권거래국가코드 (200.미국 070.일본 120.홍콩 160.상해 170.심천)
            iem_cd: 티커종목코드 (예: AAPL)
            orr_qty: 주문수량
            ahi_nmn_pr_tp_cd: 현물호가유형코드 (00.지정가 03.시장가 61.프리마켓 62.애프터마켓
                63.주간거래 11.LOO 12.LOC 13.MOO 14.MOC TW/VW.TWAP·VWAP(시장가) TL/VL.TWAP·VWAP(지정가))
            wtm_cur_knd_cd: 증거금통화종류코드 (1.해당통화 2.원화)
            fc_orr_uit_pr: 외화주문단가 (소수점 2자리). 호가유형 00,11,12,61,62,63 이면 필수.

        Returns:
            NHPlugHttpResponse[OverseasStockOrderBuy]: 주문번호(`orr_no`) 포함 접수 결과
        """
        body = {
            "act_no": act_no,
            "fc_sec_trd_nat_cd": fc_sec_trd_nat_cd,
            "iem_cd": iem_cd,
            "orr_qty": orr_qty,
            "ahi_nmn_pr_tp_cd": ahi_nmn_pr_tp_cd,
            "wtm_cur_knd_cd": wtm_cur_knd_cd,
        }
        if fc_orr_uit_pr is not None:
            body["fc_orr_uit_pr"] = fc_orr_uit_pr

        response = self.client.post("/gbstock/order/v1/buy", body=body)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=OverseasStockOrderBuy.model_validate(data))
