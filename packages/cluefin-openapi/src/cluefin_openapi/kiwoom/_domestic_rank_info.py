from typing import Literal

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._domestic_rank_info_types import (
    DomesticRankInfoAfterHoursSinglePriceChangeRateRanking,
    DomesticRankInfoRapidlyIncreasingRemainingOrderQuantity,
    DomesticRankInfoRapidlyIncreasingTotalSellOrders,
    DomesticRankInfoRapidlyIncreasingTradingVolume,
    DomesticRankInfoSameNetBuySellRanking,
    DomesticRankInfoStockSpecificSecuritiesFirmRanking,
    DomesticRankInfoTopConsecutiveNetBuySellByForeigners,
    DomesticRankInfoTopCurrentDayDeviationSources,
    DomesticRankInfoTopCurrentDayMajorTraders,
    DomesticRankInfoTopCurrentDayTradingVolume,
    DomesticRankInfoTopExpectedConclusionPercentageChange,
    DomesticRankInfoTopForeignAccountGroupTrading,
    DomesticRankInfoTopForeignerLimitExhaustionRate,
    DomesticRankInfoTopForeignerPeriodTrading,
    DomesticRankInfoTopIntradayTradingByInvestor,
    DomesticRankInfoTopLimitExhaustionRateForeigner,
    DomesticRankInfoTopMarginRatio,
    DomesticRankInfoTopNetBuyTraderRanking,
    DomesticRankInfoTopPercentageChangeFromPreviousDay,
    DomesticRankInfoTopPreviousDayTradingVolume,
    DomesticRankInfoTopRemainingOrderQuantity,
    DomesticRankInfoTopSecuritiesFirmTrading,
    DomesticRankInfoTopTransactionValue,
)
from cluefin_openapi.kiwoom._model import (
    KiwoomHttpHeader,
    KiwoomHttpResponse,
)


class DomesticRankInfo:
    def __init__(self, client: Client):
        self.client = client
        self.post = "/api/dostk/rkinfo"

    def get_top_remaining_order_quantity(
        self,
        mrkt_tp: Literal["001", "101"],
        sort_tp: Literal["1", "2", "3", "4"],
        trde_qty_tp: Literal["0000", "0010", "0050", "00100"],
        stk_cnd: Literal["0", "1", "5", "6", "7", "8", "9"],
        crd_cnd: Literal["0", "1", "2", "3", "4", "9"],
        stex_tp: Literal["1", "2", "3"],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticRankInfoTopRemainingOrderQuantity]:
        """호가잔량상위요청

        Args:
            mrkt_tp (Literal["001", "101"]): 시장구분 (코스피: "001", 코스닥: "101")
            sort_tp (Literal["1", "2", "3", "4"]): 정렬구분
                - "1": 순매수잔량순
                - "2": 순매도잔량순
                - "3": 매수비율순
                - "4": 매도비율순
            trde_qty_tp (Literal["0000", "0010", "0050", "00100"]): 거래량구분
                - "0000": 장시작전(0주이상)
                - "0010": 만주이상
                - "0050": 5만주이상
                - "00100": 10만주이상
            stk_cnd (Literal["0", "1", "5", "6", "7", "8", "9"]): 종목조건
                - "0": 전체조회
                - "1": 관리종목제외
                - "5": 증100제외
                - "6": 증100만보기
                - "7": 증40만보기
                - "8": 증30만보기
                - "9": 증20만보기
            crd_cnd (Literal["0", "1", "2", "3", "4", "9"]): 신용조건
                - "0": 전체조회
                - "1": 신용융자A군
                - "2": 신용융자B군
                - "3": 신용융자C군
                - "4": 신용융자D군
                - "9": 신용융자전체
            stex_tp (Literal["1", "2", "3"]): 거래소구분
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to 'N'.
            next_key (str, optional): 다음 페이지 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticRankInfoTopRemainingOrderQuantity]: 호가잔량상위요청 결과
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10020",
        }
        body = {
            "mrkt_tp": mrkt_tp,
            "sort_tp": sort_tp,
            "trde_qty_tp": trde_qty_tp,
            "stk_cnd": stk_cnd,
            "crd_cnd": crd_cnd,
            "stex_tp": stex_tp,
        }

        response = self.client._post(self.post, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching top remaining order quantity: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticRankInfoTopRemainingOrderQuantity.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_rapidly_increasing_remaining_order_quantity(
        self,
        mrkt_tp: Literal["001", "101"],
        trde_tp: Literal["1", "2"],
        sort_tp: Literal["1", "2"],
        tm_tp: str,
        trde_qty_tp: Literal["1", "5", "10", "50", "100"],
        stk_cnd: Literal["0", "1", "5", "6", "7", "8", "9"],
        stex_tp: Literal["1", "2"],
        cond_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticRankInfoRapidlyIncreasingRemainingOrderQuantity]:
        """호가잔량급증요청

        Args:
            mrkt_tp (Literal["001", "101"]): 시장구분 (코스피: "001", 코스닥: "101")
            trde_tp (Literal["1", "2"]): 매매구분 (매수잔량: "1", 매도잔량: "2")
            sort_tp (Literal["1", "2"]): 정렬구분 (급증량: "1", 급증률: "2")
            tm_tp (str): 시간구분. 분 입력.
            trde_qty_tp (Literal["1", "5", "10", "50", "100"]): 거래량구분
                - "1": 천주이상
                - "5": 5천주이상
                - "10": 만주이상
                - "50": 5만주이상
                - "100": 10만주이상
            stk_cnd (Literal["0", "1", "5", "6", "7", "8", "9"]): 종목조건
                - "0": 전체조회
                - "1": 관리종목제외
                - "5": 증100제외
                - "6": 증100만보기
                - "7": 증40만보기
                - "8": 증30만보기
                - "9": 증20만보기
            stex_tp (Literal["1", "2"]): 거래소구분 (KRX: "1", NXT: "2").
            cond_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to 'N'.
            next_key (str, optional): 다음 페이지 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticRankInfoRapidlyIncreasingRemainingOrderQuantity]: 호가잔량급증요청 결과
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cond-yn": cond_yn,
            "next-key": next_key,
            "api-id": "ka10021",
        }
        body = {
            "mrkt_tp": mrkt_tp,
            "trde_tp": trde_tp,
            "sort_tp": sort_tp,
            "tm_tp": tm_tp,
            "trde_qty_tp": trde_qty_tp,
            "stk_cnd": stk_cnd,
            "stex_tp": stex_tp,
        }
        response = self.client._post(self.post, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching rapidly increasing remaining order quantity: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticRankInfoRapidlyIncreasingRemainingOrderQuantity.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_rapidly_increasing_total_sell_orders(
        self,
        mrkt_tp: Literal["001", "101"],
        rt_tp: Literal["1", "2"],
        tm_tp: Literal["1", "2"],
        trde_qty_tp: Literal["5", "10", "50", "100"],
        stk_cnd: Literal["0", "1", "5", "6", "7", "8", "9"],
        stex_tp: Literal["1", "2"],
        cond_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticRankInfoRapidlyIncreasingTotalSellOrders]:
        """전량매도급증요청

        Args:
            mrkt_tp (Literal["001", "101"]): 시장구분 (코스피: "001", 코스닥: "101")
            rt_tp (Literal["1", "2"]): 비율구분 (매수/매도비율: "1", 매도/매수비율: "2")
            tm_tp (Literal["1", "2"]): 시간구분 (분 입력: "1", 전일 입력: "2")
            trde_qty_tp (Literal["5", "10", "50", "100"]): 거래량구분
                - "5": 5천주이상
                - "10": 만주이상
                - "50": 5만주이상
                - "100": 10만주이상
            stk_cnd (Literal["0", "1", "5", "6", "7", "8", "9"]): 종목조건
                - "0": 전체조회
                - "1": 관리종목제외
                - "5": 증100제외
                - "6": 증100만보기
                - "7": 증40만보기
                - "8": 증30만보기
                - "9": 증20만보기
            stex_tp (Literal["1", "2"]): 거래소구분.
            cond_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to 'N'.
            next_key (str, optional): 다음 페이지 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticRankInfoRapidlyIncreasingTotalSellOrders]: 전량매도급증요청 결과
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cond-yn": cond_yn,
            "next-key": next_key,
            "api-id": "ka10022",
        }

        body = {
            "mrkt_tp": mrkt_tp,
            "rt_tp": rt_tp,
            "tm_tp": tm_tp,
            "trde_qty_tp": trde_qty_tp,
            "stk_cnd": stk_cnd,
            "stex_tp": stex_tp,
        }
        response = self.client._post(self.post, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching rapidly increasing total sell orders: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticRankInfoRapidlyIncreasingTotalSellOrders.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_rapidly_increasing_trading_volume(
        self,
        mrkt_tp: Literal["000", "001", "101"],
        sort_tp: Literal["1", "2", "3", "4"],
        tm_tp: Literal["1", "2"],
        trde_qty_tp: Literal["5", "10", "50", "100", "200", "300", "500", "1000"],
        stk_cnd: Literal["0", "1", "3", "4", "5", "6", "7", "8", "9", "11", "12", "13", "14", "15", "16"],
        pric_tp: Literal["0", "2", "5", "6", "8", "9"],
        stex_tp: Literal["1", "2"],
        tm: str = "",
        cond_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticRankInfoRapidlyIncreasingTradingVolume]:
        """거래량급증요청

        Args:
            mrkt_tp (Literal["000", "001", "101"]): 시장구분 (전체: '000', 코스피: '001', 코스닥: '101')
            sort_tp (Literal["1", "2", "3", "4"]): 정렬구분
                - "1": 급증량
                - "2": 급증률
                - "3": 급감량
                - "4": 급감률
            tm_tp (Literal["1", "2"]): 시간구분 (분 입력: '1', 전일 입력: '2')
            trde_qty_tp (Literal["5", "10", "50", "100", "200", "300", "500", "1000"]): 거래량구분
                - "5": 5천주이상
                - "10": 1만주이상
                - "50": 5만주이상
                - "100": 10만주이상
                - "200": 20만주이상
                - "300": 30만주이상
                - "500": 50만주이상
                - "1000": 백만주이상
            stk_cnd (Literal["0","1","3","4","5","6","7","8","9","11","12","13","14","15","16"], optional): 종목조건.
                - "0": 전체조회
                - "1": 관리종목제외
                - "3": 우선주제외
                - "4": 관리종목+우선주제외
                - "5": 증100제외
                - "6": 증100만보기
                - "7": 증40만보기
                - "8": 증30만보기
                - "9": 증20만보기
                - "11": 정리매매종목제외
                - "12": 증50만보기
                - "13": 증60만보기
                - "14": ETF제외
                - "15": 스펙제외
                - "16": ETF+ETN제외
            pric_tp (Literal["0","2","5","6","8","9"]): 가격구분.
                - "0": 전체조회
                - "2": 1천원~2천원
                - "5": 1만원이상
                - "6": 1천원이상
                - "8": 1천원이상
                - "9": 1만원미만
            stex_tp (Literal["1","2"]): 거래소구분 (1:KRX, 2:NXT 3.통합).
            tm (str, optional): 시간 입력.
            cond_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to 'N'.
            next_key (str, optional): 다음 페이지 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticRankInfoRapidlyIncreasingTradingVolume]: 거래량급증요청 결과
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cond-yn": cond_yn,
            "next-key": next_key,
            "api-id": "ka10023",
        }

        body = {
            "mrkt_tp": mrkt_tp,
            "sort_tp": sort_tp,
            "tm_tp": tm_tp,
            "trde_qty_tp": trde_qty_tp,
            "tm": tm,
            "stk_cnd": stk_cnd,
            "pric_tp": pric_tp,
            "stex_tp": stex_tp,
        }
        response = self.client._post(self.post, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching rapidly increasing trading volume: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticRankInfoRapidlyIncreasingTradingVolume.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_top_percentage_change_from_previous_day(
        self,
        mrkt_tp: Literal["000", "001", "101"],
        sort_tp: Literal["1", "2", "3", "4", "5"],
        trde_qty_cnd: Literal["0000", "0010", "0050", "0100", "0150", "0200", "0300", "0500", "1000"],
        stk_cnd: Literal["0", "1", "4", "3", "5", "6", "7", "8", "9", "11", "12", "13", "14", "15", "16"],
        crd_cnd: Literal["0", "1", "2", "3", "4", "9"],
        updown_incls: Literal["0", "1"],
        pric_cnd: Literal["0", "1", "2", "3", "4", "5", "8", "10"],
        trde_prica_cnd: Literal["0", "3", "5", "10", "30", "50", "100", "300", "500", "1000", "3000", "5000"],
        stex_tp: Literal["1", "2"],
        cond_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticRankInfoTopPercentageChangeFromPreviousDay]:
        """전일대비등락률상위요청

        Args:
            mrkt_tp (Literal["000", "001", "101"]): 시장구분 (전체: '000', 코스피: '001', 코스닥: '101')
            sort_tp (Literal["1", "2", "3", "4", "5"]): 정렬구분
                - "1": 상승률
                - "2": 상승폭
                - "3": 하락률
                - "4": 하락폭
                - "5": 보합
            trde_qty_cnd (Literal["0000", "0010", "0050", "0100", "0150", "0200", "0300", "0500", "1000"]): 거래량조건
                - "0000": 전체조회
                - "0010": 만주이상
                - "0050": 5만주이상
                - "0100": 10만주이상
                - "0150": 15만주이상
                - "0200": 20만주이상
                - "0300": 30만주이상
                - "0500": 50만주이상
                - "1000": 백만주이상
            stk_cnd (Literal["0", "1", "4", "3", "5", "6", "7", "8", "9", "11", "12", "13", "14", "15", "16"]): 종목조건
                - "0": 전체조회
                - "1": 관리종목제외
                - "4": 우선주+관리주제외
                - "3": 우선주제외
                - "5": 증100제외
                - "6": 증100만보기
                - "7": 증40만보기
                - "8": 증30만보기
                - "9": 증20만보기
                - "11": 정리매매종목제외
                - "12": 증50만보기
                - "13": 증60만보기
                - "14": ETF제외
                - "15": 스펙제외
                - "16": ETF+ETN제외
            crd_cnd (Literal["0", "1", "2", "3", "4", "9"]): 신용조건
                - "0": 전체조회
                - "1": 신용융자A군
                - "2": 신용융자B군
                - "3": 신용융자C군
                - "4": 신용융자D군
                - "9": 신용융자전체
            updown_incls (Literal["0", "1"]): 상하한포함 여부 ('0': 불 포함, '1': 포함)
            pric_cnd (Literal["0", "1", "2", "3", "4", "5", "8", "10"]): 가격조건
                - "0": 전체조회
                - "1": 1천원미만
                - "2": 1천원~2천원
                - "3": 2천원~5천원
                - "4": 5천원~1만원
                - "5": 1만원이상
                - "8": 1천원이상
                - "10": 1만원미만
            trde_prica_cnd (Literal["0","3","5","10","30","50","100","300","500","1000","3000","5000"]): 거래대금조건
                - "0": 전체조회
                - "3": 3천만원이상
                - "5": 5천만원이상
                - "10": 1억원이상
                - "30": 3억원이상
                - "50": 5억원이상
                - "100": 10억원이상
                - "300": 30억원이상
                - "500": 50억원이상
                - "1000": 100억원이상
                - "3000": 300억원이상
                - "5000": 500억원이상
            stex_tp (Literal["1","2"]): 거래소구분 ('1': KRX, '2': NXT 3.통합)
            cond_yn (Literal["Y","N"], optional): 연속조회 여부. Defaults to 'N'.
            next_key (str, optional): 다음 페이지 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticRankInfoTopPercentageChangeFromPreviousDay]: 전일대비등락률상위요청 결과
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cond-yn": cond_yn,
            "next-key": next_key,
            "api-id": "ka10027",
        }
        body = {
            "mrkt_tp": mrkt_tp,
            "sort_tp": sort_tp,
            "trde_qty_cnd": trde_qty_cnd,
            "stk_cnd": stk_cnd,
            "crd_cnd": crd_cnd,
            "updown_incls": updown_incls,
            "pric_cnd": pric_cnd,
            "trde_prica_cnd": trde_prica_cnd,
            "stex_tp": stex_tp,
        }
        response = self.client._post(self.post, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching top percentage change from previous day: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticRankInfoTopPercentageChangeFromPreviousDay.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_top_expected_conclusion_percentage_change(
        self,
        mrkt_tp: Literal["000", "001", "101"],
        sort_tp: Literal["1", "2", "3", "4", "5", "6", "7", "8"],
        trde_qty_cnd: Literal["0", "1", "3", "5", "10", "50", "100"],
        stk_cnd: Literal["0", "1", "3", "4", "5", "6", "7", "8", "9", "11", "12", "13", "14", "15", "16"],
        crd_cnd: Literal["0", "1", "2", "3", "4", "8", "9"],
        pric_cnd: Literal["0", "1", "2", "3", "4", "5", "8", "10"],
        stex_tp: Literal["1", "2"],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticRankInfoTopExpectedConclusionPercentageChange]:
        """예상체결등락률상위요청

        Args:
            mrkt_tp (Literal["000", "001", "101"]): 시장구분 (전체: '000', 코스피: '001', 코스닥: '101')
            sort_tp (Literal["1", "2", "3", "4", "5", "6", "7", "8"]): 정렬구분
                - "1": 상승률
                - "2": 상승폭
                - "3": 보합
                - "4": 하락률
                - "5": 하락폭
                - "6": 체결량
                - "7": 상한
                - "8": 하한
            trde_qty_cnd (Literal["0", "1", "3", "5", "10", "50", "100"]): 거래량조건
                - "0": 전체조회
                - "1": 천주이상
                - "3": 3천주이상
                - "5": 5천주이상
                - "10": 만주이상
                - "50": 5만주이상
                - "100": 10만주이상
            stk_cnd (Literal["0", "1", "3", "4", "5", "6", "7", "8", "9", "11", "12", "13", "14", "15", "16"]): 종목조건
                - "0": 전체조회
                - "1": 관리종목제외
                - "3": 우선주제외
                - "4": 관리종목+우선주제외
                - "5": 증100제외
                - "6": 증100만보기
                - "7": 증40만보기
                - "8": 증30만보기
                - "9": 증20만보기
                - "11": 정리매매종목제외
                - "12": 증50만보기
                - "13": 증60만보기
                - "14": ETF제외
                - "15": 스펙제외
                - "16": ETF+ETN제외
            crd_cnd (Literal["0", "1", "2", "3", "4", "8", "9"]): 신용조건
                - "0": 전체조회
                - "1": 신용융자A군
                - "2": 신용융자B군
                - "3": 신용융자C군
                - "4": 신용융자D군
                - "8": 신용대주
                - "9": 신용융자전체
            pric_cnd (Literal["0", "1", "2", "3", "4", "5", "8", "10"]): 가격조건
                - "0": 전체조회
                - "1": 1천원미만
                - "2": 1천원~2천원
                - "3": 2천원~5천원
                - "4": 5천원~1만원
                - "5": 1만원이상
                - "8": 1천원이상
                - "10": 1만원미만
            stex_tp (Literal["1", "2"]): 거래소구분 (1: KRX, 2: NXT 3.통합)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to 'N'.
            next_key (str, optional): 다음 페이지 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticRankInfoTopExpectedConclusionPercentageChange]: 예상체결등락률상위요청 결과
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10029",
        }
        body = {
            "mrkt_tp": mrkt_tp,
            "sort_tp": sort_tp,
            "trde_qty_cnd": trde_qty_cnd,
            "stk_cnd": stk_cnd,
            "crd_cnd": crd_cnd,
            "pric_cnd": pric_cnd,
            "stex_tp": stex_tp,
        }
        response = self.client._post(self.post, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching top expected conclusion percentage change: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticRankInfoTopExpectedConclusionPercentageChange.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_top_current_day_trading_volume(
        self,
        mrkt_tp: Literal["000", "001", "101"],
        sort_tp: Literal["1", "2", "3"],
        mang_stk_incls: Literal["0", "1", "3", "4", "5", "6", "7", "8", "9", "11", "12", "13", "14", "15", "16"],
        crd_tp: Literal["0", "1", "2", "3", "4", "8"],
        trde_qty_tp: Literal["0", "5", "10", "50", "100", "200", "300", "500", "1000"],
        pric_tp: Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
        trde_prica_tp: Literal["0", "1", "3", "4", "10", "30", "50", "100", "300", "500", "1000", "3000", "5000"],
        mrkt_open_tp: Literal["0", "1", "2", "3"],
        stex_tp: Literal["1", "2"] = "1",
        cond_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticRankInfoTopCurrentDayTradingVolume]:
        """당일거래량상위요청

        Args:
            mrkt_tp (Literal["000","001","101"]): 시장구분 (전체: '000', 코스피: '001', 코스닥: '101')
            sort_tp (Literal["1","2","3"]): 정렬구분
                - "1": 거래량
                - "2": 거래회전율
                - "3": 거래대금
            mang_stk_incls (Literal["0","1","3","4","5","6","7","8","9","11","12","13","14","15","16"]): 관리종목포함
                - "0": 관리종목 포함
                - "1": 관리종목 미포함
                - "3": 우선주제외
                - "4": 관리종목+우선주제외
                - "5": 증100제외
                - "6": 증100만보기
                - "7": 증40만보기
                - "8": 증30만보기
                - "9": 증20만보기
                - "11": 정리매매종목제외
                - "12": 증50만보기
                - "13": 증60만보기
                - "14": ETF제외
                - "15": 스펙제외
                - "16": ETF+ETN제외
            crd_tp (Literal["0","1","2","3","4","8"]): 신용구분
                - "0": 전체조회
                - "1": 신용융자A군
                - "2": 신용융자B군
                - "3": 신용융자C군
                - "4": 신용융자D군
                - "8": 신용대주
            trde_qty_tp (Literal["0","5","10","50","100","200","300","500","1000"]): 거래량구분
                - "0": 전체조회
                - "5": 5천주이상
                - "10": 1만주이상
                - "50": 5만주이상
                - "100": 10만주이상
                - "200": 20만주이상
                - "300": 30만주이상
                - "500": 50만주이상
                - "1000": 백만주이상
            pric_tp (Literal["0","1","2","3","4","5","6","7","8","9"]): 가격구분
                - "0": 전체조회
                - "1": 1천원미만
                - "2": 1천원이상
                - "3": 1천원~2천원
                - "4": 2천원~5천원
                - "5": 5천원이상
                - "6": 5천원~1만원
                - "7": 1만원미만
                - "8": 1만원이상
                - "9": 5만원이상
            trde_prica_tp (Literal["0","1","3","4","10","30","50","100","300","500","1000","3000","5000"]): 거래대금구분
                - "0": 전체조회
                - "1": 1천만원이상
                - "3": 3천만원이상
                - "4": 5천만원이상
                - "10": 1억원이상
                - "30": 3억원이상
                - "50": 5억원이상
                - "100": 10억원이상
                - "300": 30억원이상
                - "500": 50억원이상
                - "1000": 100억원이상
                - "3000": 300억원이상
                - "5000": 500억원이상
            mrkt_open_tp (Literal["0","1","2","3"]): 장운영구분
                - "0": 전체조회
                - "1": 장중
                - "2": 장전시간외
                - "3": 장후시간외
            stex_tp (Literal["1","2"], optional): 거래소구분. Defaults to '1' (KRX).
            cond_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to 'N'.
            next_key (str, optional): 다음 페이지 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticRankInfoTopCurrentDayTradingVolume]: 당일거래량상위요청 결과
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cond-yn": cond_yn,
            "next-key": next_key,
            "api-id": "ka10030",
        }
        body = {
            "mrkt_tp": mrkt_tp,
            "sort_tp": sort_tp,
            "mang_stk_incls": mang_stk_incls,
            "crd_tp": crd_tp,
            "trde_qty_tp": trde_qty_tp,
            "pric_tp": pric_tp,
            "trde_prica_tp": trde_prica_tp,
            "mrkt_open_tp": mrkt_open_tp,
            "stex_tp": stex_tp,
        }
        response = self.client._post(self.post, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching top current day trading volume: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticRankInfoTopCurrentDayTradingVolume.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_top_previous_day_trading_volume(
        self,
        mrkt_tp: Literal["000", "001", "101"],
        qry_tp: Literal["1", "2"],
        rank_strt: str,
        rank_end: str,
        stex_tp: Literal["1", "2"],
        cond_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticRankInfoTopPreviousDayTradingVolume]:
        """전일거래량상위요청

        Args:
            mrkt_tp (Literal["000", "001", "101"]): 시장구분 (전체: '000', 코스피: '001', 코스닥: '101')
            qry_tp (Literal["1", "2"]): 조회구분
                - "1": 전일거래량 상위100종목
                - "2": 전일거래대금 상위100종목
            rank_strt (str): 순위시작 (0 ~ 100 값 중에 조회를 원하는 순위 시작값)
            rank_end (str): 순위끝 (0 ~ 100 값 중에 조회를 원하는 순위 끝값)
            stex_tp (Literal["1", "2"]): 거래소구분 ('1': KRX, '2': NXT 3.통합)
            cond_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to 'N'.
            next_key (str, optional): 다음 페이지 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticRankInfoTopPreviousDayTradingVolume]: 전일거래량상위요청 결과
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cond-yn": cond_yn,
            "next-key": next_key,
            "api-id": "ka10031",
        }
        body = {
            "mrkt_tp": mrkt_tp,
            "qry_tp": qry_tp,
            "rank_strt": rank_strt,
            "rank_end": rank_end,
            "stex_tp": stex_tp,
        }
        response = self.client._post(self.post, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching top previous day trading volume: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticRankInfoTopPreviousDayTradingVolume.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_top_transaction_value(
        self,
        mrkt_tp: Literal["000", "001", "101"],
        mang_stk_incls: Literal["0", "1"],
        stex_tp: Literal["1", "2"],
        cond_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticRankInfoTopTransactionValue]:
        """거래대금상위요청

        Args:
            mrkt_tp (Literal["000", "001", "101"]): 시장구분 (전체: '000', 코스피: '001', 코스닥: '101')
            mang_stk_incls (Literal["0", "1"]): 관리종목포함 여부 ('0': 미포함, '1': 포함)
            stex_tp (Literal["1", "2"]): 거래소구분 ('1': KRX, '2': NXT 3.통합)
            cond_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to 'N'.
            next_key (str, optional): 다음 페이지 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticRankInfoTopTransactionValue]: 거래대금상위요청 결과
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cond-yn": cond_yn,
            "next-key": next_key,
            "api-id": "ka10032",
        }
        body = {
            "mrkt_tp": mrkt_tp,
            "mang_stk_incls": mang_stk_incls,
            "stex_tp": stex_tp,
        }
        response = self.client._post(self.post, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching top trading value: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticRankInfoTopTransactionValue.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_top_margin_ratio(
        self,
        mrkt_tp: Literal["000", "001", "101"],
        trde_qty_tp: Literal["0", "10", "50", "100", "200", "300", "500", "1000"],
        stk_cnd: Literal["0", "1", "5", "6", "7", "8", "9"],
        updown_incls: Literal["0", "1"],
        crd_cnd: Literal["0", "1", "2", "3", "4", "9"],
        stex_tp: Literal["1", "2", "3"],
        cond_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticRankInfoTopMarginRatio]:
        """신용비율상위요청

        Args:
            mrkt_tp (Literal["000","001","101"]): 시장구분 (전체: '000', 코스피: '001', 코스닥: '101')
            trde_qty_tp (Literal["0","10","50","100","200","300","500","1000"]): 거래량구분
                - "0": 전체조회
                - "10": 만주이상
                - "50": 5만주이상
                - "100": 10만주이상
                - "200": 20만주이상
                - "300": 30만주이상
                - "500": 50만주이상
                - "1000": 백만주이상
            stk_cnd (Literal["0","1","5","6","7","8","9"]): 종목조건
                - "0": 전체조회
                - "1": 관리종목제외
                - "5": 증100제외
                - "6": 증100만보기
                - "7": 증40만보기
                - "8": 증30만보기
                - "9": 증20만보기
            updown_incls (Literal["0","1"]): 상하한포함 여부 ('0': 불 포함, '1': 포함)
            crd_cnd (Literal["0","1","2","3","4","9"]): 신용조건
                - "0": 전체조회
                - "1": 신용융자A군
                - "2": 신용양자B군
                - "3": 신용융자C군
                - "4": 신용융자D군
                - "9": 신용융자전체
            stex_tp (Literal["1","2","3"]): 거래소구분. (1: KRX, 2: NXT, 3: 통합)
            cond_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to 'N'.
            next_key (str, optional): 다음 페이지 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticRankInfoTopMarginRatio]: 신용비율상위요청 결과
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cond-yn": cond_yn,
            "next-key": next_key,
            "api-id": "ka10033",
        }
        body = {
            "mrkt_tp": mrkt_tp,
            "trde_qty_tp": trde_qty_tp,
            "stk_cnd": stk_cnd,
            "updown_incls": updown_incls,
            "crd_cnd": crd_cnd,
            "stex_tp": stex_tp,
        }
        response = self.client._post(self.post, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching top margin ratio: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticRankInfoTopMarginRatio.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_top_foreigner_period_trading(
        self,
        mrkt_tp: Literal["000", "001", "101"],
        trde_tp: Literal["1", "2", "3"],
        dt: Literal["0", "1", "5", "10", "20", "60"],
        stex_tp: Literal["1", "2", "3"],
        cond_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticRankInfoTopForeignerPeriodTrading]:
        """외인기간별매매상위요청
        Args:
            mrkt_tp (Literal["000", "001", "101"]): 시장구분 (전체: '000', 코스피: '001', 코스닥: '101')
            trde_tp (Literal["1", "2", "3"]): 매매구분
                - "1": 순매도
                - "2": 순매수
                - "3": 순매매
            dt (Literal["0", "1", "5", "10", "20", "60"]): 기간
                - "0": 당일
                - "1": 전일
                - "5": 5일
                - "10": 10일
                - "20": 20일
                - "60": 60일
            stex_tp (Literal["1", "2", "3"]): 거래소구분. (1: KRX, 2: NXT, 3: 통합)
            cond_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to 'N'.
            next_key (str, optional): 다음 페이지 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticRankInfoTopForeignerPeriodTrading]: 외국인기간별매매상위요청 결과
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cond-yn": cond_yn,
            "next-key": next_key,
            "api-id": "ka10034",
        }
        body = {
            "mrkt_tp": mrkt_tp,
            "trde_tp": trde_tp,
            "dt": dt,
            "stex_tp": stex_tp,
        }

        response = self.client._post(self.post, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching top foreigner period trading: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticRankInfoTopForeignerPeriodTrading.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_top_consecutive_net_buy_sell_by_foreigners(
        self,
        mrkt_tp: Literal["000", "001", "101"],
        trde_tp: Literal["1", "2"],
        base_dt_tp: Literal["0", "1"],
        stex_tp: Literal["1", "2", "3"],
        cond_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticRankInfoTopConsecutiveNetBuySellByForeigners]:
        """외국인연속순매매상위요청

        Args:
            mrkt_tp (Literal["000", "001", "101"]): 시장구분 (전체: '000', 코스피: '001', 코스닥: '101')
            trde_tp (Literal["1", "2"]): 매매구분
                - "1": 연속순매도
                - "2": 연속순매수
            base_dt_tp (Literal["0", "1"]): 기준일구분
                - "0": 당일기준
                - "1": 전일기준
            stex_tp (Literal["1", "2", "3"]): 거래소구분. (1: KRX, 2: NXT, 3: 통합)
            cond_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to 'N'.
            next_key (str, optional): 다음 페이지 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticRankInfoTopConsecutiveNetBuySellByForeigners]: 외국인연속순매매상위요청 결과
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cond-yn": cond_yn,
            "next-key": next_key,
            "api-id": "ka10035",
        }
        body = {
            "mrkt_tp": mrkt_tp,
            "trde_tp": trde_tp,
            "base_dt_tp": base_dt_tp,
            "stex_tp": stex_tp,
        }
        response = self.client._post(self.post, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching top consecutive net buy/sell by foreigners: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticRankInfoTopConsecutiveNetBuySellByForeigners.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_top_limit_exhaustion_rate_foreigner(
        self,
        mrkt_tp: Literal["000", "001", "101"],
        dt: Literal["0", "1", "5", "10", "20", "60"],
        stex_tp: Literal["1", "2", "3"],
        cond_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticRankInfoTopLimitExhaustionRateForeigner]:
        """외인한도소진율상위요청

        Args:
            mrkt_tp (Literal["000", "001", "101"]): 시장구분 (전체: '000', 코스피: '001', 코스닥: '101')
            dt (Literal["0", "1", "5", "10", "20", "60"]): 기간
                - "0": 당일
                - "1": 전일
                - "5": 5일
                - "10": 10일
                - "20": 20일
                - "60": 60일
            stex_tp (Literal["1", "2", "3"]): 거래소구분. (1: KRX, 2: NXT, 3: 통합)
            cond_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to 'N'.
            next_key (str, optional): 다음 페이지 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticRankInfoTopLimitExhaustionRateForeigner]: 외인한도소진율상위요청 결과
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cond-yn": cond_yn,
            "next-key": next_key,
            "api-id": "ka10036",
        }
        body = {
            "mrkt_tp": mrkt_tp,
            "dt": dt,
            "stex_tp": stex_tp,
        }
        response = self.client._post(self.post, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching top foreigner limit exhaustion rate: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticRankInfoTopLimitExhaustionRateForeigner.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_top_foreign_account_group_trading(
        self,
        mrkt_tp: Literal["000", "001", "101"],
        dt: Literal["0", "1", "5", "10", "20", "60"],
        trde_tp: Literal["1", "2", "3", "4"],
        sort_tp: Literal["1", "2"],
        stex_tp: Literal["1", "2", "3"],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticRankInfoTopForeignAccountGroupTrading]:
        """외국계좌군매매상위요청

        Args:
            mrkt_tp (Literal["000", "001", "101"]): 시장구분 (전체: '000', 코스피: '001', 코스닥: '101')
            dt (Literal["0", "1", "5", "10", "20", "60"]): 기간
                - "0": 당일
                - "1": 전일
                - "5": 5일
                - "10": 10일
                - "20": 20일
                - "60": 60일
            trde_tp (Literal["1", "2", "3", "4"]): 매매구분
                - "1": 순매수
                - "2": 순매도
                - "3": 매수
                - "4": 매도
            sort_tp (Literal["1", "2"]): 정렬구분
                - "1": 금액
                - "2": 수량
            stex_tp (Literal["1", "2", "3"]): 거래소구분. (1: KRX, 2: NXT, 3: 통합)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to 'N'.
            next_key (str, optional): 다음 페이지 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticRankInfoTopForeignAccountGroupTrading]: 외국계좌군매매상위요청 결과
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10037",
        }
        body = {
            "mrkt_tp": mrkt_tp,
            "dt": dt,
            "trde_tp": trde_tp,
            "sort_tp": sort_tp,
            "stex_tp": stex_tp,
        }
        response = self.client._post(self.post, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching top foreign account group trading: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticRankInfoTopForeignAccountGroupTrading.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_stock_specific_securities_firm_ranking(
        self,
        stk_cd: str,
        strt_dt: str,
        end_dt: str,
        qry_tp: Literal["1", "2"],
        dt: Literal["1", "4", "9", "19", "39", "59", "119"] = "1",
        cond_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticRankInfoStockSpecificSecuritiesFirmRanking]:
        """종목별증권사순위요청

        Args:
            stk_cd (str): 종목코드 (거래소별 종목코드, 예: KRX:039490, NXT:039490_NX, SOR:039490_AL)
            strt_dt (str): 시작일자 (YYYYMMDD 형식)
            end_dt (str): 종료일자 (YYYYMMDD 형식)
            qry_tp (Literal["1", "2"]): 조회구분
                - "1": 순매도순위정렬
                - "2": 순매수순위정렬
            dt (Literal["1", "4", "9", "19", "39", "59", "119"], optional): 기간. Defaults to '1'.
                - "1": 전일
                - "4": 5일
                - "9": 10일
                - "19": 20일
                - "39": 40일
                - "59": 60일
                - "119": 120일
            cond_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to 'N'.
            next_key (str, optional): 다음 페이지 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticRankInfoStockSpecificSecuritiesFirmRanking]: 종목별증권사순위요청 결과
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cond-yn": cond_yn,
            "next-key": next_key,
            "api-id": "ka10038",
        }
        body = {
            "stk_cd": stk_cd,
            "strt_dt": strt_dt,
            "end_dt": end_dt,
            "qry_tp": qry_tp,
            "dt": dt,
        }
        response = self.client._post(self.post, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock specific securities firm ranking: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticRankInfoStockSpecificSecuritiesFirmRanking.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_top_securities_firm_trading(
        self,
        mmcm_cd: str,
        trde_qty_tp: Literal["0", "5", "10", "50", "100", "500", "1000"],
        trde_tp: Literal["1", "2"],
        dt: Literal["1", "5", "10", "60"],
        stex_tp: Literal["1", "2", "3"],
        cond_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticRankInfoTopSecuritiesFirmTrading]:
        """증권사별매매상위요청

        Args:
            mmcm_cd (str): 회원사코드 (3자리 회원사 코드, ka10102 조회)
            trde_qty_tp (Literal["0", "5", "10", "50", "100", "500", "1000"]): 거래량구분
                - "0": 전체조회
                - "5": 5천주이상
                - "10": 1만주이상
                - "50": 5만주이상
                - "100": 10만주이상
                - "500": 50만주이상
                - "1000": 백만주이상
            trde_tp (Literal["1", "2"]): 매매구분
                - "1": 순매수
                - "2": 순매도
            dt (Literal["1", "5", "10", "60"]): 기간
                - "1": 전일
                - "5": 5일
                - "10": 10일
                - "60": 60일
            stex_tp (Literal["1", "2", "3"]): 거래소구분. (1: KRX, 2: NXT, 3: 통합)
            cond_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to 'N'.
            next_key (str, optional): 다음 페이지 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticRankInfoTopSecuritiesFirmTrading]: 증권사별매매상위요청 결과
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cond-yn": cond_yn,
            "next-key": next_key,
            "api-id": "ka10039",
        }
        body = {
            "mmcm_cd": mmcm_cd,
            "trde_qty_tp": trde_qty_tp,
            "trde_tp": trde_tp,
            "dt": dt,
            "stex_tp": stex_tp,
        }
        response = self.client._post(self.post, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching top securities firm trading: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticRankInfoTopSecuritiesFirmTrading.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_top_current_day_major_traders(
        self,
        stk_cd: str,
        cond_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticRankInfoTopCurrentDayMajorTraders]:
        """당일주요거래원요청

        Args:
            stk_cd (str): 종목코드 (거래소별 종목코드, 예: KRX:039490, NXT:039490_NX, SOR:039490_AL)
            cond_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to 'N'.
            next_key (str, optional): 다음 페이지 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticRankInfoTopCurrentDayMajorTraders]: 당일주요거래원요청 결과
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cond-yn": cond_yn,
            "next-key": next_key,
            "api-id": "ka10040",
        }
        body = {
            "stk_cd": stk_cd,
        }
        response = self.client._post(self.post, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching top current day major traders: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticRankInfoTopCurrentDayMajorTraders.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_top_net_buy_trader_ranking(
        self,
        stk_cd: str,
        strt_dt: str,
        end_dt: str,
        qry_dt_tp: Literal["0", "1"],
        pot_tp: Literal["0", "1"],
        dt: Literal["5", "10", "20", "40", "60", "120"],
        sort_base: Literal["1", "2"],
        cond_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticRankInfoTopNetBuyTraderRanking]:
        """순매수거래원순위요청

        Args:
            stk_cd (str): 종목코드 (거래소별 종목코드, 예: KRX:039490, NXT:039490_NX, SOR:039490_AL)
            strt_dt (str): 시작일자 (YYYYMMDD 형식)
            end_dt (str): 종료일자 (YYYYMMDD 형식)
            qry_dt_tp (Literal["0", "1"]): 조회기간구분
                - "0": 기간으로 조회
                - "1": 시작일자, 종료일자로 조회
            pot_tp (Literal["0", "1"]): 시점구분
                - "0": 당일
                - "1": 전일
            dt (Literal["5", "10", "20", "40", "60", "120"]): 기간
                - "5": 5일
                - "10": 10일
                - "20": 20일
                - "40": 40일
                - "60": 60일
                - "120": 120일
            sort_base (Literal["1", "2"]): 정렬기준
                - "1": 종가순
                - "2": 날짜순
            cond_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to 'N'.
            next_key (str, optional): 다음 페이지 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticRankInfoTopNetBuyTraderRanking]: 순매수거래원순위요청 결과
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cond-yn": cond_yn,
            "next-key": next_key,
            "api-id": "ka10042",
        }
        body = {
            "stk_cd": stk_cd,
            "strt_dt": strt_dt,
            "end_dt": end_dt,
            "qry_dt_tp": qry_dt_tp,
            "pot_tp": pot_tp,
            "dt": dt,
            "sort_base": sort_base,
        }
        response = self.client._post(self.post, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching top net buy trader ranking: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticRankInfoTopNetBuyTraderRanking.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_top_current_day_deviation_sources(
        self,
        stk_cd: str,
        cond_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticRankInfoTopCurrentDayDeviationSources]:
        """당일상위이탈원요청

        Args:
            stk_cd (str): 종목코드 (거래소별 종목코드, 예: KRX:039490, NXT:039490_NX, SOR:039490_AL)
            cond_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to 'N'.
            next_key (str, optional): 다음 페이지 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticRankInfoTopCurrentDayDeviationSources]: 당일상위이탈원요청 결과
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cond-yn": cond_yn,
            "next-key": next_key,
            "api-id": "ka10053",
        }
        body = {
            "stk_cd": stk_cd,
        }
        response = self.client._post(self.post, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching top current day deviation sources: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticRankInfoTopCurrentDayDeviationSources.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_same_net_buy_sell_ranking(
        self,
        strt_dt: str,
        end_dt: str,
        mrkt_tp: Literal["000", "001", "101"],
        trde_tp: Literal["1", "2"],
        sort_cnd: Literal["1", "2"],
        unit_tp: Literal["1", "1000"],
        stex_tp: Literal["1", "2", "3"],
    ) -> KiwoomHttpResponse[DomesticRankInfoSameNetBuySellRanking]:
        """동일순매매순위요청

        Args:
            strt_dt (str): 시작일자 (YYYYMMDD 형식)
            end_dt (str): 종료일자 (YYYYMMDD 형식)
            mrkt_tp (Literal["000", "001", "101"]): 시장구분 (전체: '000', 코스피: '001', 코스닥: '101')
            trde_tp (Literal["1", "2"]): 매매구분
                - "1": 순매수
                - "2": 순매도
            sort_cnd (Literal["1", "2"]): 정렬조건
                - "1": 수량
                - "2": 금액
            unit_tp (Literal["1", "1000"]): 단위구분
                - "1": 단주
                - "1000": 천주
            stex_tp (Literal["1", "2", "3"]): 거래소구분. (1: KRX, 2: NXT, 3: 통합)

        Returns:
            KiwoomHttpResponse[DomesticRankInfoSameNetBuySellRanking]: 동일순매매순위요청 결과
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "api-id": "ka10062",
        }
        body = {
            "strt_dt": strt_dt,
            "end_dt": end_dt,
            "mrkt_tp": mrkt_tp,
            "trde_tp": trde_tp,
            "sort_cnd": sort_cnd,
            "unit_tp": unit_tp,
            "stex_tp": stex_tp,
        }
        response = self.client._post(self.post, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching same net buy/sell ranking: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticRankInfoSameNetBuySellRanking.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_top_intraday_trading_by_investor(
        self,
        trde_tp: Literal["1", "2"],
        mrkt_tp: Literal["000", "001", "101"],
        orgn_tp: Literal["9000", "9100", "1000", "3000", "5000", "4000", "2000", "6000", "7000", "7100", "9999"],
        cond_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticRankInfoTopIntradayTradingByInvestor]:
        """장중투자자별매매상위요청

        Args:
            trde_tp (Literal["1", "2"]): 매매구분
                - "1": 순매수
                - "2": 순매도
            mrkt_tp (Literal["000", "001", "101"]): 시장구분 (전체: '000', 코스피: '001', 코스닥: '101')
            orgn_tp (Literal["9000", "9100", "1000", "3000", "5000", "4000", "2000", "6000", "7000", "7100", "9999"]): 기관구분
                - "9000": 외국인
                - "9100": 외국계
                - "1000": 금융투자
                - "3000": 투신
                - "5000": 기타금융
                - "4000": 은행
                - "2000": 보험
                - "6000": 연기금
                - "7000": 국가
                - "7100": 기타법인
                - "9999": 기관계
            cond_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to 'N'.
            next_key (str, optional): 다음 페이지 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticRankInfoTopIntradayTradingByInvestor]: 장중투자자별매매상위요청 결과
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cond-yn": cond_yn,
            "next-key": next_key,
        }
        body = {
            "trde_tp": trde_tp,
            "mrkt_tp": mrkt_tp,
            "orgn_tp": orgn_tp,
        }
        response = self.client._post(self.post, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching top intraday trading by investor: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticRankInfoTopIntradayTradingByInvestor.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_after_hours_single_price_change_rate_ranking(
        self,
        mrkt_tp: Literal["000", "001", "101"],
        sort_base: Literal["1", "2", "3", "4", "5"],
        stk_cnd: Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "12", "13", "14", "15", "16", "17"],
        trde_qty_cnd: Literal["0", "10", "50", "100", "500", "1000", "5000", "10000"],
        crd_cnd: Literal["0", "9", "1", "2", "3", "4", "8", "5"],
        trde_prica: Literal["0", "5", "10", "30", "50", "100", "300", "500", "1000", "3000", "5000"],
        cond_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticRankInfoAfterHoursSinglePriceChangeRateRanking]:
        """시간외단일가등락률순위요청

        Args:
            mrkt_tp (Literal["000", "001", "101"]): 시장구분 (전체: '000', 코스피: '001', 코스닥: '101')
            sort_base (Literal["1", "2", "3", "4", "5"]): 정렬기준
                - 1: 상승률
                - 2: 상승폭
                - 3: 하락률
                - 4: 하락폭
                - 5: 보합
            stk_cnd (Literal["0","1","2","3","4","5","6","7","8","9","12","13","14","15","16","17"]): 종목조건
                - "0": 전체조회
                - "1": 관리종목제외
                - "2": 정리매매종목제외
                - "3": 우선주제외
                - "4": 관리종목우선주제외
                - "5": 증100제외
                - "6": 증100만보기
                - "7": 증40만보기
                - "8": 증30만보기
                - "9": 증20만보기
                - "12": 증50만보기
                - "13": 증60만보기
                - "14": ETF제외
                - "15": 스팩제외
                - "16": ETF+ETN제외
                - "17": ETN제외
            trde_qty_cnd (Literal["0","10","50","100","500","1000","5000","10000"]): 거래량조건
                - "0": 전체조회
                - "10": 백주이상
                - "50": 5백주이상
                - "100": 천주이상
                - "500": 5천주이상
                - "1000": 만주이상
                - "5000": 5만주이상
                - "10000": 10만주이상
            crd_cnd (Literal["0","9","1","2","3","4","8","5"]): 신용조건
                - "0": 전체조회
                - "9": 신용융자전체
                - "1": 신용융자A군
                - "2": 신용융자B군
                - "3": 신용융자C군
                - "4": 신용융자D군
                - "8": 신용대주
                - "5": 신용한도초과제외
            trde_prica (Literal["0","5","10","30","50","100","300","500","1000","3000","5000"]): 거래대금
            cond_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to 'N'.
            next_key (str, optional): 다음 페이지 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticRankInfoAfterHoursSinglePriceChangeRateRanking]: 시간외단일가등락률순위요청 결과
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cond-yn": cond_yn,
            "next-key": next_key,
            "api-id": "ka10098",
        }
        body = {
            "mrkt_tp": mrkt_tp,
            "sort_base": sort_base,
            "stk_cnd": stk_cnd,
            "trde_qty_cnd": trde_qty_cnd,
            "crd_cnd": crd_cnd,
            "trde_prica": trde_prica,
        }
        response = self.client._post(self.post, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching after hours single price change rate ranking: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticRankInfoAfterHoursSinglePriceChangeRateRanking.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_top_foreigner_limit_exhaustion_rate(
        self,
        mrkt_tp: Literal["000", "001", "101"],
        dt: Literal["0", "1", "5", "10", "20", "60"],
        stex_tp: Literal["1", "2", "3"],
        cond_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticRankInfoTopForeignerLimitExhaustionRate]:
        """외국인한도소진율상위요청

        Args:
            mrkt_tp (Literal["000", "001", "101"]): 시장구분 (전체: '000', 코스피: '001', 코스닥: '101')
            dt (Literal["0", "1", "5", "10", "20", "60"]): 기간
                - "0": 당일
                - "1": 전일
                - "5": 5일
                - "10": 10일
                - "20": 20일
                - "60": 60일
            stex_tp (Literal["1", "2", "3"]): 거래소구분. (1: KRX, 2: NXT, 3: 통합)
            cond_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to 'N'.
            next_key (str, optional): 다음 페이지 키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticRankInfoTopForeignerLimitExhaustionRate]: 외국인한도소진율상위요청 결과

        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cond-yn": cond_yn,
            "next-key": next_key,
            "api-id": "ka10036",
        }
        body = {
            "mrkt_tp": mrkt_tp,
            "dt": dt,
            "stex_tp": stex_tp,
        }
        response = self.client._post(self.post, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching top foreigner limit exhaustion rate: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticRankInfoTopForeignerLimitExhaustionRate.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)
