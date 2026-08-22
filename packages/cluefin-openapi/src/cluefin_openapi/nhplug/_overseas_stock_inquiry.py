from typing import Optional

from cluefin_openapi.nhplug._http_client import HttpClient
from cluefin_openapi.nhplug._model import NHPlugHttpHeader, NHPlugHttpResponse
from cluefin_openapi.nhplug._overseas_stock_inquiry_types import OverseasStockBuyableAmount
from cluefin_openapi.nhplug._response import check_response_error


class OverseasStockInquiry:
    """해외주식 조회 (gbstock inquiry).

    스펙 정본: https://www.nhplug.com/openapi-docs/gbstock/openapi.json
    """

    def __init__(self, client: HttpClient):
        self.client = client

    def _check_response_error(self, response_data: dict) -> None:
        check_response_error(response_data)

    def get_buyable_amount(
        self,
        act_no: str,
        pcs_dit: str,
        fc_sec_trd_nat_cd: str,
        iem_cd: str,
        wtm_cur_knd_cd: str,
        oss_orr_knd_cd: str,
        ahi_nmn_pr_tp_cd: str,
        fc_orr_uit_pr: Optional[float] = None,
        cfd_lon_cd: Optional[str] = None,
        lon_dt: Optional[str] = None,
        cts: Optional[str] = None,
    ) -> NHPlugHttpResponse[OverseasStockBuyableAmount]:
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
            NHPlugHttpResponse[OverseasStockBuyableAmount]: 매수가능금액·수량(`orr_pbl_amt`,
                `byn_pbl_qty` 등) 및 매도가능수량(`sll_pbl_qty` 등) 조회 결과
        """
        body: dict = {
            "act_no": act_no,
            "pcs_dit": pcs_dit,
            "fc_sec_trd_nat_cd": fc_sec_trd_nat_cd,
            "iem_cd": iem_cd,
            "wtm_cur_knd_cd": wtm_cur_knd_cd,
            "oss_orr_knd_cd": oss_orr_knd_cd,
            "ahi_nmn_pr_tp_cd": ahi_nmn_pr_tp_cd,
        }
        optional_fields = {
            "fc_orr_uit_pr": fc_orr_uit_pr,
            "cfd_lon_cd": cfd_lon_cd,
            "lon_dt": lon_dt,
        }
        body.update({k: v for k, v in optional_fields.items() if v is not None})

        response = self.client.post("/gbstock/inquiry/v1/buyableAmount", body=body, cts=cts)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=OverseasStockBuyableAmount.model_validate(data))
