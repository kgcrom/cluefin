from typing import Literal

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._domestic_foreign_types import (
    DomesticForeignConsecutiveNetBuySellStatusByInstitutionForeigner,
    DomesticForeignInvestorTradingTrendByStock,
    DomesticForeignStockInstitution,
)
from cluefin_openapi.kiwoom._model import (
    KiwoomHttpHeader,
    KiwoomHttpResponse,
)


class DomesticForeign:
    def __init__(self, client: Client):
        self.client = client
        self.path = "/api/dostk/frgnistt"

    def get_foreign_investor_trading_trend_by_stock(
        self, stk_cd: str, cont_yn: Literal["Y", "N"] = "N", next_key: str = ""
    ) -> KiwoomHttpResponse[DomesticForeignInvestorTradingTrendByStock]:
        """주식외국인종목별매매동향 요청

        Args:
            stk_cd (str): 종목코드 (예: KRX:039490)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticForeignInvestorTradingTrendByStock]: 외국인 종목별 매매 동향 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10008",
        }
        body = {"stk_cd": stk_cd}

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching foreign investor trading trend: {response.text}")

        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticForeignInvestorTradingTrendByStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_stock_institution(
        self, stk_cd: str, cont_yn: Literal["Y", "N"] = "N", next_key: str = ""
    ) -> KiwoomHttpResponse[DomesticForeignStockInstitution]:
        """주식기관요청

        Args:
            stk_cd (str): 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticForeignStockInstitution]: 주식기관 요청 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10009",
        }
        body = {"stk_cd": stk_cd}

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock institution data: {response.text}")

        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticForeignStockInstitution.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_consecutive_net_buy_sell_status_by_institution_foreigner(
        self,
        dt: Literal["1", "3", "5", "10", "20", "120", "0"],
        mrkt_tp: Literal["001", "101"],
        stk_inds_tp: Literal["0", "1"],
        amt_qty_tp: Literal["0", "1"],
        stex_tp: Literal["1", "2", "3"],
        netslmt_tp: Literal["2"] = "2",
        strt_dt: str = "",
        end_dt: str = "",
    ) -> KiwoomHttpResponse[DomesticForeignConsecutiveNetBuySellStatusByInstitutionForeigner]:
        """기관외국인연속순매매현황요청

        Args:
            dt (Literal["1", "3", "5", "10", "20", "120", "0"]): 기간
            mrkt_tp (Literal["001", "101"]): 장구분 (코스피:001, 코스닥:101)
            stk_inds_tp (Literal["0", "1"]): 종목업종구분 (0:종목(주식), 1:업종)
            amt_qty_tp (Literal["0", "1"]): 금액수량구분 (0:금액, 1:수량)
            stex_tp (Literal["1", "2", "3"]): 거래소구분 (1:KRX, 2:NXT, 3:통합)
            netslmt_tp (Literal["2"], optional): 순매도수구분. Defaults to "2".
            strt_dt (str, optional): 시작일자 (YYYYMMDD). Defaults to "".
            end_dt (str, optional): 종료일자 (YYYYMMDD). Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticForeignConsecutiveNetBuySellStatusByInstitutionForeigner]: 기관 외국인 연속 순매매 현황 데이터
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "api-id": "ka10131",
        }
        body = {
            "dt": dt,
            "strt_dt": strt_dt,
            "end_dt": end_dt,
            "mrkt_tp": mrkt_tp,
            "stk_inds_tp": stk_inds_tp,
            "amt_qty_tp": amt_qty_tp,
            "stex_tp": stex_tp,
            "netslmt_tp": netslmt_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching consecutive net buy sell status: {response.text}")

        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticForeignConsecutiveNetBuySellStatusByInstitutionForeigner.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)
