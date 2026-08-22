from typing import Any, Dict, Literal, Optional

from cluefin_openapi.nhplug._exceptions import NHPlugAPIError
from cluefin_openapi.nhplug._http_client import HttpClient
from cluefin_openapi.nhplug._krstock_order_types import (
    KrStockOrderCashBuy,
    KrStockOrderCashSell,
    KrStockOrderCreditBuy,
    KrStockOrderCreditSell,
    KrStockOrderModify,
)
from cluefin_openapi.nhplug._model import NHPlugHttpHeader, NHPlugHttpResponse

# 호가유형코드 (nmn_pr_tp_cd)
QuoteTypeCode = Literal[
    "01",  # 보통가
    "05",  # 시장가
    "06",  # 조건부지정가
    "09",  # 자기주식
    "10",  # S-OPTION자기주식
    "11",  # 금전신탁자기주식
    "12",  # 최유리지정가
    "13",  # 최우선지정가
    "16",  # 스톱지정가
    "17",  # 중간가
    "61",  # 장전시간외
    "71",  # 장후시간외
    "81",  # 시간외단일가
    "91",  # 장전시간외경쟁대량
    "92",  # 장중경쟁대량
]

# 신용대출코드 (cfd_lon_cd)
CreditLoanCode = Literal[
    "01",  # 유통융자
    "02",  # 자기융자
    "03",  # 유통대주
    "04",  # 자기대주
    "10",  # 매입자금대출
]


class KrStockOrder:
    """국내주식 주문.

    스펙 정본: https://www.nhplug.com/openapi-docs/krstock/openapi.json
    운영(prod)은 주문이 실제 체결된다 — 테스트·검증은 모의투자(dev)로.
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

    @staticmethod
    def _drop_none(body: Dict[str, Any]) -> Dict[str, Any]:
        """선택 파라미터는 값이 있을 때만 전송한다."""
        return {k: v for k, v in body.items() if v is not None}

    def cash_buy(
        self,
        act_no: str,
        iem_cd: str,
        orr_qty: int,
        nmn_pr_tp_cd: QuoteTypeCode,
        rmt_mkt_cd: Literal["SOR", "KRX", "NXT"],
        sor_mkt_sli_yn: Literal["Y", "N"],
        orr_cnd_dit_cd: Literal["00", "01", "02"] = "00",
        ssl_nmn_pr_dit_cd: Literal["00", "01", "02", "99"] = "00",
        orr_pr: Optional[float] = None,
        orr_amt: Optional[int] = None,
        sop_cnd_pr: Optional[float] = None,
    ) -> NHPlugHttpResponse[KrStockOrderCashBuy]:
        """주식주문(현금) 매수 (`POST /krstock/order/v1/cashBuy`).

        Args:
            act_no: 계좌번호 (`/n2/acctinfo` 의 acct_no — 운영은 acct_type 01·02,
                모의투자는 03 계좌만 유효)
            iem_cd: 종목코드 (예: 005940)
            orr_qty: 주문수량
            nmn_pr_tp_cd: 호가유형코드 (01.보통가 05.시장가 16.스톱지정가 등)
            rmt_mkt_cd: 요청시장코드 (SOR/KRX/NXT)
            sor_mkt_sli_yn: SOR시장분할여부 (SOR 일 경우에만 Y/N 선택, KRX/NXT 면 N)
            orr_cnd_dit_cd: 주문조건구분코드 (00.없음 01.IOC 02.FOK)
            ssl_nmn_pr_dit_cd: 공매도호가구분코드 (00.정상 01.차입주식매도 02.기타공매도 99.권리공매도)
            orr_pr: 주문가격 (지정가 계열일 때)
            orr_amt: 주문금액
            sop_cnd_pr: 정지조건가격 (호가유형코드 16.스톱지정가일 때만 입력)
        """
        body = self._drop_none(
            {
                "act_no": act_no,
                "iem_cd": iem_cd,
                "orr_qty": orr_qty,
                "orr_pr": orr_pr,
                "orr_amt": orr_amt,
                "nmn_pr_tp_cd": nmn_pr_tp_cd,
                "orr_cnd_dit_cd": orr_cnd_dit_cd,
                "ssl_nmn_pr_dit_cd": ssl_nmn_pr_dit_cd,
                "sop_cnd_pr": sop_cnd_pr,
                "rmt_mkt_cd": rmt_mkt_cd,
                "sor_mkt_sli_yn": sor_mkt_sli_yn,
            }
        )
        response = self.client.post("/krstock/order/v1/cashBuy", body=body)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=KrStockOrderCashBuy.model_validate(data))

    def cash_sell(
        self,
        act_no: str,
        iem_cd: str,
        orr_qty: int,
        nmn_pr_tp_cd: QuoteTypeCode,
        rmt_mkt_cd: Literal["SOR", "KRX", "NXT"],
        sor_mkt_sli_yn: Literal["Y", "N"],
        orr_cnd_dit_cd: Literal["00", "01", "02"] = "00",
        ssl_nmn_pr_dit_cd: Literal["00", "01", "02", "99"] = "00",
        orr_pr: Optional[float] = None,
        orr_amt: Optional[int] = None,
        sop_cnd_pr: Optional[float] = None,
    ) -> NHPlugHttpResponse[KrStockOrderCashSell]:
        """주식주문(현금) 매도 (`POST /krstock/order/v1/cashSell`).

        Args:
            act_no: 계좌번호 (`/n2/acctinfo` 의 acct_no — 운영은 acct_type 01·02,
                모의투자는 03 계좌만 유효)
            iem_cd: 종목코드 (예: 005940)
            orr_qty: 주문수량
            nmn_pr_tp_cd: 호가유형코드 (01.보통가 05.시장가 16.스톱지정가 등)
            rmt_mkt_cd: 요청시장코드 (SOR/KRX/NXT)
            sor_mkt_sli_yn: SOR시장분할여부 (SOR 일 경우에만 Y/N 선택, KRX/NXT 면 N)
            orr_cnd_dit_cd: 주문조건구분코드 (00.없음 01.IOC 02.FOK)
            ssl_nmn_pr_dit_cd: 공매도호가구분코드 (00.정상 01.차입주식매도 02.기타공매도 99.권리공매도)
            orr_pr: 주문가격 (지정가 계열일 때)
            orr_amt: 주문금액
            sop_cnd_pr: 정지조건가격 (호가유형코드 16.스톱지정가일 때만 입력)
        """
        body = self._drop_none(
            {
                "act_no": act_no,
                "iem_cd": iem_cd,
                "orr_qty": orr_qty,
                "orr_pr": orr_pr,
                "orr_amt": orr_amt,
                "nmn_pr_tp_cd": nmn_pr_tp_cd,
                "orr_cnd_dit_cd": orr_cnd_dit_cd,
                "ssl_nmn_pr_dit_cd": ssl_nmn_pr_dit_cd,
                "sop_cnd_pr": sop_cnd_pr,
                "rmt_mkt_cd": rmt_mkt_cd,
                "sor_mkt_sli_yn": sor_mkt_sli_yn,
            }
        )
        response = self.client.post("/krstock/order/v1/cashSell", body=body)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=KrStockOrderCashSell.model_validate(data))

    def credit_buy(
        self,
        act_no: str,
        iem_cd: str,
        orr_qty: int,
        nmn_pr_tp_cd: QuoteTypeCode,
        cfd_lon_cd: CreditLoanCode,
        rmt_mkt_cd: Literal["SOR", "KRX", "NXT"],
        sor_mkt_sli_yn: Literal["Y", "N"],
        orr_cnd_dit_cd: Literal["00", "01", "02"] = "00",
        orr_pr: Optional[float] = None,
        orr_amt: Optional[int] = None,
        lon_dt: Optional[str] = None,
        sop_cnd_pr: Optional[float] = None,
    ) -> NHPlugHttpResponse[KrStockOrderCreditBuy]:
        """주식주문(신용) 매수 (`POST /krstock/order/v1/creditBuy`).

        Args:
            act_no: 계좌번호 (`/n2/acctinfo` 의 acct_no — 운영은 acct_type 01·02,
                모의투자는 03 계좌만 유효)
            iem_cd: 종목코드 (예: 005940)
            orr_qty: 주문수량
            nmn_pr_tp_cd: 호가유형코드 (01.보통가 05.시장가 16.스톱지정가 등)
            cfd_lon_cd: 신용대출코드 (01.유통융자 02.자기융자 03.유통대주 04.자기대주 10.매입자금대출)
            rmt_mkt_cd: 요청시장코드 (SOR/KRX/NXT)
            sor_mkt_sli_yn: SOR시장분할여부 (SOR 일 경우에만 Y/N 선택, KRX/NXT 면 N)
            orr_cnd_dit_cd: 주문조건구분코드 (00.없음 01.IOC 02.FOK)
            orr_pr: 주문가격 (지정가 계열일 때)
            orr_amt: 주문금액
            lon_dt: 대출일자 (신용대출코드 03.유통대주·04.자기대주일 경우 필수)
            sop_cnd_pr: 정지조건가격 (호가유형코드 16.스톱지정가일 때만 입력)
        """
        body = self._drop_none(
            {
                "act_no": act_no,
                "iem_cd": iem_cd,
                "orr_qty": orr_qty,
                "orr_pr": orr_pr,
                "orr_amt": orr_amt,
                "nmn_pr_tp_cd": nmn_pr_tp_cd,
                "orr_cnd_dit_cd": orr_cnd_dit_cd,
                "cfd_lon_cd": cfd_lon_cd,
                "lon_dt": lon_dt,
                "sop_cnd_pr": sop_cnd_pr,
                "rmt_mkt_cd": rmt_mkt_cd,
                "sor_mkt_sli_yn": sor_mkt_sli_yn,
            }
        )
        response = self.client.post("/krstock/order/v1/creditBuy", body=body)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=KrStockOrderCreditBuy.model_validate(data))

    def credit_sell(
        self,
        act_no: str,
        iem_cd: str,
        orr_qty: int,
        nmn_pr_tp_cd: QuoteTypeCode,
        cfd_lon_cd: CreditLoanCode,
        rmt_mkt_cd: Literal["SOR", "KRX", "NXT"],
        sor_mkt_sli_yn: Literal["Y", "N"],
        orr_cnd_dit_cd: Literal["00", "01", "02"] = "00",
        orr_pr: Optional[float] = None,
        orr_amt: Optional[int] = None,
        lon_dt: Optional[str] = None,
        sop_cnd_pr: Optional[float] = None,
    ) -> NHPlugHttpResponse[KrStockOrderCreditSell]:
        """주식주문(신용) 매도 (`POST /krstock/order/v1/creditSell`).

        스펙은 creditBuy 와 필드·required 구성이 동일하다(설명 문구의 미세한 차이만 있음).

        Args:
            act_no: 계좌번호 (`/n2/acctinfo` 의 acct_no — 운영은 acct_type 01·02,
                모의투자는 03 계좌만 유효)
            iem_cd: 종목코드 (예: 005940)
            orr_qty: 주문수량
            nmn_pr_tp_cd: 호가유형코드 (01.보통가 05.시장가 16.스톱지정가 등)
            cfd_lon_cd: 신용대출코드 (01.유통융자 02.자기융자 03.유통대주 04.자기대주 10.매입자금대출)
            rmt_mkt_cd: 요청시장코드 (SOR/KRX/NXT)
            sor_mkt_sli_yn: SOR시장분할여부 (SOR 일 경우에만 Y/N 선택, KRX/NXT 면 N)
            orr_cnd_dit_cd: 주문조건구분코드 (00.없음 01.IOC 02.FOK)
            orr_pr: 주문가격 (지정가 계열일 때)
            orr_amt: 주문금액
            lon_dt: 대출일자 (신용대출코드 03.유통대주·04.자기대주일 경우 필수)
            sop_cnd_pr: 정지조건가격 (호가유형코드 16.스톱지정가일 때만 입력)
        """
        body = self._drop_none(
            {
                "act_no": act_no,
                "iem_cd": iem_cd,
                "orr_qty": orr_qty,
                "orr_pr": orr_pr,
                "orr_amt": orr_amt,
                "nmn_pr_tp_cd": nmn_pr_tp_cd,
                "orr_cnd_dit_cd": orr_cnd_dit_cd,
                "cfd_lon_cd": cfd_lon_cd,
                "lon_dt": lon_dt,
                "sop_cnd_pr": sop_cnd_pr,
                "rmt_mkt_cd": rmt_mkt_cd,
                "sor_mkt_sli_yn": sor_mkt_sli_yn,
            }
        )
        response = self.client.post("/krstock/order/v1/creditSell", body=body)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=KrStockOrderCreditSell.model_validate(data))

    def modify(
        self,
        act_no: str,
        org_mkt_orr_no: int,
        all_pat_dit_cd: Literal["1", "2"],
        iem_cd: str,
        cor_qty: int,
        cor_pr: float,
        sop_cnd_pr: float,
        rmt_mkt_cd: Literal["SOR", "KRX", "NXT"],
        sor_mkt_sli_yn: Literal["Y", "N"],
    ) -> NHPlugHttpResponse[KrStockOrderModify]:
        """주식주문(정정취소) 정정 (`POST /krstock/order/v1/modify`).

        스펙상 9개 입력 필드가 모두 required 다. 원주문 식별자는 `org_mkt_orr_no`
        (원시장주문번호, 신규주문 응답의 mkt_orr_no) 하나뿐이다.

        Args:
            act_no: 계좌번호 (`/n2/acctinfo` 의 acct_no — 운영은 acct_type 01·02,
                모의투자는 03 계좌만 유효)
            org_mkt_orr_no: 원시장주문번호 (정정 대상 원주문의 mkt_orr_no)
            all_pat_dit_cd: 전체일부구분코드 (1.전체(전량) 2.일부(잔량))
            iem_cd: 종목코드 (예: 005940)
            cor_qty: 정정수량 (전체일부구분코드 "2.일부(잔량)"인 경우 셋팅)
            cor_pr: 정정가격
            sop_cnd_pr: 정지조건가격 (원주문의 호가유형코드 16.스톱지정가일 때만 의미가
                있음 — KRX 는 효력발생 전으로만 수정 가능, NXT 는 원주문의 스톱지정가 그대로 입력)
            rmt_mkt_cd: 요청시장코드 (원주문과 동일하게 입력, SOR/KRX/NXT)
            sor_mkt_sli_yn: SOR시장분할여부 (원주문과 동일하게 입력, SOR 일 경우에만
                Y/N 선택, KRX/NXT 면 N)
        """
        body = self._drop_none(
            {
                "act_no": act_no,
                "org_mkt_orr_no": org_mkt_orr_no,
                "all_pat_dit_cd": all_pat_dit_cd,
                "iem_cd": iem_cd,
                "cor_qty": cor_qty,
                "cor_pr": cor_pr,
                "sop_cnd_pr": sop_cnd_pr,
                "rmt_mkt_cd": rmt_mkt_cd,
                "sor_mkt_sli_yn": sor_mkt_sli_yn,
            }
        )
        response = self.client.post("/krstock/order/v1/modify", body=body)
        data = response.json()
        self._check_response_error(data)
        header = NHPlugHttpHeader.model_validate(dict(response.headers))
        return NHPlugHttpResponse(header=header, body=KrStockOrderModify.model_validate(data))
