from typing import Literal

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._model import (
    KiwoomHttpHeader,
    KiwoomHttpResponse,
)
from cluefin_openapi.kiwoom._overseas_order_types import (
    OverseasOrderBuy,
    OverseasOrderCancel,
    OverseasOrderModify,
    OverseasOrderOrderableQuantity,
    OverseasOrderSell,
)


class OverseasOrder:
    def __init__(self, client: Client):
        self.client = client
        self.path = "/api/us/ordr"

    def request_buy_order(
        self,
        stex_tp: Literal["NA", "ND", "NY"],
        stk_cd: str,
        ord_qty: str,
        trde_tp: Literal["00", "03", "26", "27", "30", "36", "37"],
        ord_uv: str = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasOrderBuy]:
        """미국주식 매수 주문 (ust20000)

        Args:
            stex_tp (Literal["NA", "ND", "NY"]): 거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE
            stk_cd (str): 종목코드
            ord_qty (str): 주문수량
            trde_tp (Literal["00", "03", "26", "27", "30", "36", "37"]): 해외매매구분. 00:지정가,03:시장가,26:VWAP지정가,27:TWAP지정가,30:LOC,36:VWAP시장가,37:TWAP시장가
            ord_uv (str, optional): 주문단가. trde_tp가 00(지정가),30(LOC)...인 경우 필수 입력, 그 외 시장가 거래유형 설정 시 입력 값은 빈 값 처리. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasOrderBuy]: 미국주식 매수 주문 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ust20000",
        }
        body = {
            "stex_tp": stex_tp,
            "stk_cd": stk_cd,
            "ord_qty": ord_qty,
            "ord_uv": ord_uv,
            "trde_tp": trde_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"request buy order failed: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasOrderBuy.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def request_sell_order(
        self,
        stk_cd: str,
        stex_tp: Literal["NA", "ND", "NY"],
        ord_qty: str,
        trde_tp: Literal["00", "03", "26", "27", "30", "33", "34", "35", "36", "37"],
        ord_uv: str = "",
        stop_pric: str = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasOrderSell]:
        """미국주식 매도 주문 (ust20001)

        Args:
            stk_cd (str): 종목코드
            stex_tp (Literal["NA", "ND", "NY"]): 거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE
            ord_qty (str): 주문수량
            trde_tp (Literal["00", "03", "26", "27", "30", "33", "34", "35", "36", "37"]): 매매구분. 00:지정가,03:시장가,26:VWAP지정가,27:TWAP지정가,30:LOC,33:MOC,34:STOP LIMIT,35:STOP,36:VWAP시장가,37:TWAP시장가
            ord_uv (str, optional): 주문단가. trde_tp가 00(지정가),30(LOC)...인 경우 필수 입력, 그 외 시장가 거래유형 설정 시 입력 값은 빈 값 처리. Defaults to "".
            stop_pric (str, optional): STOP가격. trde_tp가 34(STOP LIMIT) 또는 35(STOP)인 경우 필수 입력, 그 외 거래유형(지정가,시장가 등) 설정 시 입력 값은 무시되거나 빈 값처리. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasOrderSell]: 미국주식 매도 주문 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ust20001",
        }
        body = {
            "stk_cd": stk_cd,
            "stex_tp": stex_tp,
            "ord_qty": ord_qty,
            "ord_uv": ord_uv,
            "stop_pric": stop_pric,
            "trde_tp": trde_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"request sell order failed: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasOrderSell.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def request_modify_order(
        self,
        orig_ord_no: str,
        stex_tp: Literal["NA", "ND", "NY"],
        stk_cd: str,
        mdfy_uv: str = "",
        stop_pric: str = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasOrderModify]:
        """미국주식 정정 주문 (ust20002)

        Args:
            orig_ord_no (str): 원주문번호. 주문 요청 응답 결과로 받은 ord_no를 설정
            stex_tp (Literal["NA", "ND", "NY"]): 거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE
            stk_cd (str): 종목코드
            mdfy_uv (str, optional): 정정단가. Defaults to "".
            stop_pric (str, optional): STOP가격. 원주문 trde_tp가 34(STOP LIMIT) 또는 35(STOP)인 경우 필수 입력, 그 외 거래유형(지정가 등) 설정 시 입력 값은 무시되거나 빈 값처리. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasOrderModify]: 미국주식 정정 주문 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ust20002",
        }
        body = {
            "orig_ord_no": orig_ord_no,
            "stex_tp": stex_tp,
            "stk_cd": stk_cd,
            "mdfy_uv": mdfy_uv,
            "stop_pric": stop_pric,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"request modify order failed: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasOrderModify.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def request_cancel_order(
        self,
        orig_ord_no: str,
        stex_tp: Literal["NA", "ND", "NY"],
        stk_cd: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasOrderCancel]:
        """미국주식 취소 주문 (ust20003)

        Args:
            orig_ord_no (str): 원주문번호. 주문 요청 응답 결과로 받은 ord_no를 설정
            stex_tp (Literal["NA", "ND", "NY"]): 거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE
            stk_cd (str): 종목코드
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasOrderCancel]: 미국주식 취소 주문 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ust20003",
        }
        body = {
            "orig_ord_no": orig_ord_no,
            "stex_tp": stex_tp,
            "stk_cd": stk_cd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"request cancel order failed: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasOrderCancel.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_orderable_quantity(
        self,
        stk_cd: str,
        uv: str,
        stex_tp: Literal["", "NA", "ND", "NY"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasOrderOrderableQuantity]:
        """미국주식 주문가능수량(종목/증거금률별) (ust31490)

        Args:
            stk_cd (str): 종목코드
            uv (str): 매수가격
            stex_tp (Literal["", "NA", "ND", "NY"], optional): 거래소구분. NA:AMEX, ND:NASDAQ, NY:NYSE. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasOrderOrderableQuantity]: 미국주식 주문가능수량(종목/증거금률별) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ust31490",
        }
        body = {
            "stex_tp": stex_tp,
            "stk_cd": stk_cd,
            "uv": uv,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching orderable quantity: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasOrderOrderableQuantity.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)
