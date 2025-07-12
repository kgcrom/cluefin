from typing import Literal

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._domestic_theme_types import DomesticThemeGroup, DomesticThemeGroupStocks
from cluefin_openapi.kiwoom._model import (
    KiwoomHttpHeader,
    KiwoomHttpResponse,
)


class DomesticTheme:
    def __init__(self, client: Client):
        self.client = client
        self.path = "/api/dostk/thme"

    def get_theme_group(
        self,
        qry_tp: Literal[0, 1, 2],
        date_tp: str,
        thema_nm: str,
        flu_pl_amt_tp: Literal[1, 2, 3, 4],
        stex_tp: Literal[1, 2, 3],
        stk_cd: str = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticThemeGroup]:
        """테마그룹별요청

        Args:
            qry_tp: 검색구분 (0:전체검색, 1:테마검색, 2:종목검색)
            date_tp: 날짜구분 (n일전 (1일 ~ 99일 날짜입력))
            thema_nm: 테마명 (검색하려는 테마명)
            flu_pl_amt_tp: 등락수익구분 (1:상위기간수익률, 2:하위기간수익률, 3:상위등락률, 4:하위등락률)
            stex_tp: 거래소구분 (1:KRX, 2:NXT 3.통합)
            stk_cd: 종목코드 (검색하려는 종목코드)
            cont_yn: 연속조회 여부 (Y:연속조회, N:비연속조회)
            next_key: 다음키 (다음페이지 조회시 필요)

        Returns:
            KiwoomHttpResponse[DomesticThemeGroup]: 테마그룹별요청 결과
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka90001",
        }
        body = {
            "qry_tp": qry_tp,
            "date_tp": date_tp,
            "thema_nm": thema_nm,
            "flu_pl_amt_tp": flu_pl_amt_tp,
            "stex_tp": stex_tp,
            "stk_cd": stk_cd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock basic info: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticThemeGroup.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_theme_group_stocks(
        self,
        thema_grp_cd: str,
        stex_tp: Literal[1, 2, 3],
        date_tp: str = "",
        cond_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticThemeGroupStocks]:
        """테마구성종목요청

        Args:
            thema_grp_cd: 테마그룹코드 (검색하려는 테마그룹코드)
            stex_tp: 거래소구분 (1:KRX, 2:NXT 3.통합)
            date_tp: 날짜구분 (n일전 (1일 ~ 99일 날짜입력))
            cond_yn: 연속조회 여부 (Y:연속조회, N:비연속조회)
            next_key: 다음키 (다음페이지 조회시 필요)

        Returns:
            KiwoomHttpResponse[DomesticThemeGroupStocks]: 테마구성종목요청 결과
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cond-yn": cond_yn,
            "next-key": next_key,
            "api-id": "ka90002",
        }
        body = {"thema_grp_cd": thema_grp_cd, "stex_tp": stex_tp, "date_tp": date_tp}

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock basic info: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticThemeGroupStocks.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)
