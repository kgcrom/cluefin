from typing import Literal, Optional

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._domestic_order_types import (
    DomesticOrderBuy,
    DomesticOrderCancel,
    DomesticOrderModify,
    DomesticOrderSell,
)
from cluefin_openapi.kiwoom._model import (
    KiwoomHttpHeader,
    KiwoomHttpResponse,
)


class DomesticOrder:
    def __init__(self, client: Client):
        self.client = client
        self.path = "/api/dostk/ordr"

    def request_buy_order(
        self,
        dmst_stex_tp: str,
        stk_cd: str,
        ord_qty: str,
        trde_tp: str,
        ord_uv: Optional[str] = None,
        cond_uv: Optional[str] = None,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticOrderBuy]:
        """주식 매수주문

        Args:
            dmst_stex_tp (str): 국내거래소구분 (KRX, NXT, SOR)
            stk_cd (str): 종목코드
            ord_qty (str): 주문수량
            trde_tp (str): 매매구분
            ord_uv (str, optional): 주문단가. Defaults to None.
            cond_uv (str, optional): 조건단가. Defaults to None.
            cont_yn (Literal["Y", "N"], optional): 연속주문 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticOrderBuy]: 주식 매수 주문 응답
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "kt10000",
        }

        body = {
            "dmst_stex_tp": dmst_stex_tp,
            "stk_cd": stk_cd,
            "ord_qty": ord_qty,
            "trde_tp": trde_tp,
        }
        if ord_uv is not None:
            body["ord_uv"] = ord_uv
        if cond_uv is not None:
            body["cond_uv"] = cond_uv

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"request buy order failed: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticOrderBuy.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def request_sell_order(
        self,
        dmst_stex_tp: str,
        stk_cd: str,
        ord_qty: str,
        trde_tp: Literal[
            "0",
            "3",
            "5",
            "81",
            "61",
            "62",
            "6",
            "7",
            "10",
            "13",
            "16",
            "20",
            "23",
            "26",
            "28",
            "29",
            "30",
            "3128",
            "29",
            "30",
            "31",
        ],
        ord_uv: Optional[str] = None,
        cond_uv: Optional[str] = None,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticOrderSell]:
        """주식 매도주문

        Args:
            dmst_stex_tp (str): 국내거래소구분 (KRX, NXT, SOR)
            stk_cd (str): 종목코드
            ord_qty (str): 주문수량
            trde_tp (Literal["0", "3", "5", "81", "61", "62", "6", "7", "10", "13", "16", "20", "23", "26", "28", "29", "30", "31"]): 매매구분
                - "0": 보통
                - "3": 시장가
                - "5": 조건부지정가
                - "81": 장마감후시간외
                - "61": 장시작전시간외
                - "62": 시간외단일가
                - "6": 최유리지정가
                - "7": 최우선지정가
                - "10": 보통(IOC)
                - "13": 시장가(IOC)
                - "16": 최유리(IOC)
                - "20": 보통(FOK)
                - "23": 시장가(FOK)
                - "26": 최유리(FOK)
                - "28": 스톱지정가
                - "29": 중간가
                - "30": 중간가(IOC)
                - "31": 중간가(FOK)
            ord_uv (str, optional): 주문단가. Defaults to None.
            cond_uv (str, optional): 조건단가. Defaults to None.
            cont_yn (Literal["Y", "N"], optional): 연속주문 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticOrderSell]: 주식 매도 주문 응답
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "kt10001",
        }

        body = {
            "dmst_stex_tp": dmst_stex_tp,
            "stk_cd": stk_cd,
            "ord_qty": ord_qty,
            "trde_tp": trde_tp,
        }
        if ord_uv is not None:
            body["ord_uv"] = ord_uv
        if cond_uv is not None:
            body["cond_uv"] = cond_uv

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"request sell order failed: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticOrderSell.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def request_modify_order(
        self,
        dmst_stex_tp: str,
        orig_ord_no: str,
        stk_cd: str,
        mdfy_qty: str,
        mdfy_uv: str,
        mdfy_cond_uv: Optional[str] = None,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticOrderModify]:
        """주식 정정주문

        Args:
            dmst_stex_tp (str): 국내거래소구분 (KRX, NXT, SOR)
            orig_ord_no (str): 원주문번호
            stk_cd (str): 종목코드
            mdfy_qty (str): 정정수량
            mdfy_uv (str): 정정단가
            mdfy_cond_uv (Optional[str], optional): 정정조건단가. Defaults to None.
            cont_yn (Literal["Y", "N"], optional): 연속주문 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticOrderModify]: 주식 정정 주문 응답
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "kt10002",
        }

        body = {
            "dmst_stex_tp": dmst_stex_tp,
            "orig_ord_no": orig_ord_no,
            "stk_cd": stk_cd,
            "mdfy_qty": mdfy_qty,
            "mdfy_uv": mdfy_uv,
        }
        if mdfy_cond_uv is not None:
            body["mdfy_cond_uv"] = mdfy_cond_uv

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"request modify order failed: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticOrderModify.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def request_cancel_order(
        self,
        dmst_stex_tp: str,
        orig_ord_no: str,
        stk_cd: str,
        cncl_qty: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticOrderCancel]:
        """주식 취소주문

        Args:
            dmst_stex_tp (str): 국내거래소구분 (KRX, NXT, SOR)
            orig_ord_no (str): 원주문번호
            stk_cd (str): 종목코드
            cncl_qty (str): 취소수량 ('0' 입력시 잔량 전부 취소)
            cont_yn (Literal["Y", "N"], optional): 연속주문 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticOrderCancel]: 주식 취소 주문 응답
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "kt10003",
        }

        body = {
            "dmst_stex_tp": dmst_stex_tp,
            "orig_ord_no": orig_ord_no,
            "stk_cd": stk_cd,
            "cncl_qty": cncl_qty,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"request cancel order failed: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticOrderCancel.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)
