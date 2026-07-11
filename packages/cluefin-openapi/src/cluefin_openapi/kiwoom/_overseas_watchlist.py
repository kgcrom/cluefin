from typing import Literal

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._model import (
    KiwoomHttpHeader,
    KiwoomHttpResponse,
)
from cluefin_openapi.kiwoom._overseas_watchlist_types import (
    OverseasWatchlistGroupDetail,
    OverseasWatchlistGroupList,
)


class OverseasWatchlist:
    def __init__(self, client: Client):
        self.client = client
        self.path = "/api/us/watchlist"

    def get_watchlist_group_list(
        self,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasWatchlistGroupList]:
        """미국주식 관심종목 그룹 리스트 조회 (usa20200)

        Args:
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasWatchlistGroupList]: 미국주식 관심종목 그룹 리스트 조회 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa20200",
        }
        body: dict[str, str] = {}

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching watchlist group list: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasWatchlistGroupList.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_watchlist_group_detail(
        self,
        arn_grp_id: str = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasWatchlistGroupDetail]:
        """미국주식 관심종목 그룹 상세 조회 (usa20201)

        Args:
            arn_grp_id (str, optional): 그룹SEQ. usa20200 응답 결과의 gcod값을 입력. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasWatchlistGroupDetail]: 미국주식 관심종목 그룹 상세 조회 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa20201",
        }
        body = {
            "arn_grp_id": arn_grp_id,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching watchlist group detail: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasWatchlistGroupDetail.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)
