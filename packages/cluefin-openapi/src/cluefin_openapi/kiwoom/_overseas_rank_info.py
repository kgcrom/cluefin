from typing import Literal

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._model import (
    KiwoomHttpHeader,
    KiwoomHttpResponse,
)
from cluefin_openapi.kiwoom._overseas_rank_info_types import (
    OverseasRankInfoConsecutiveRiseFallRankEtf,
    OverseasRankInfoConsecutiveRiseFallRankStock,
    OverseasRankInfoConsecutiveRiseFallRankWatchlist,
    OverseasRankInfoCumulativeFluctuationTopEtf,
    OverseasRankInfoCumulativeFluctuationTopStock,
    OverseasRankInfoDaytimeTradingDisparityTopEtf,
    OverseasRankInfoDaytimeTradingDisparityTopStock,
    OverseasRankInfoHighLowPriceRiseFallEtf,
    OverseasRankInfoHighLowPriceRiseFallStock,
    OverseasRankInfoKiwoomTradingTopEtf,
    OverseasRankInfoKiwoomTradingTopStock,
    OverseasRankInfoMarketCapTopEtf,
    OverseasRankInfoMarketCapTopStock,
    OverseasRankInfoOpenPriceFluctuationRankEtf,
    OverseasRankInfoOpenPriceFluctuationRankStock,
    OverseasRankInfoOpenPriceFluctuationRankWatchlist,
    OverseasRankInfoPeriodFluctuationRankEtf,
    OverseasRankInfoPeriodFluctuationRankStock,
    OverseasRankInfoPeriodFluctuationRankWatchlist,
    OverseasRankInfoPreviousDayFluctuationRankEtf,
    OverseasRankInfoPreviousDayFluctuationRankStock,
    OverseasRankInfoPreviousDayTradingTopEtf,
    OverseasRankInfoPreviousDayTradingTopStock,
    OverseasRankInfoQuoteRemainingVolumeTopEtf,
    OverseasRankInfoQuoteRemainingVolumeTopStock,
    OverseasRankInfoRealtimeSymbolQueryRank,
    OverseasRankInfoSpecificDateRiseFallEtf,
    OverseasRankInfoSpecificDateRiseFallStock,
    OverseasRankInfoTodayTradingValueTopEtf,
    OverseasRankInfoTodayTradingValueTopStock,
    OverseasRankInfoTodayTradingVolumeTopEtf,
    OverseasRankInfoTodayTradingVolumeTopStock,
    OverseasRankInfoTurnoverRateTopEtf,
    OverseasRankInfoTurnoverRateTopStock,
    OverseasRankInfoWatchlistRegistrationTop,
)


class OverseasRankInfo:
    def __init__(self, client: Client):
        self.client = client
        self.path = "/api/us/rkinfo"

    def get_realtime_symbol_query_rank(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoRealtimeSymbolQueryRank]:
        """미국주식 실시간 종목 조회 순위 (usa01980)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasRankInfoRealtimeSymbolQueryRank]: 미국주식 실시간 종목 조회 순위 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa01980",
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching realtime symbol query rank: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoRealtimeSymbolQueryRank.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_watchlist_registration_top(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoWatchlistRegistrationTop]:
        """미국주식 관심종목 등록 상위 (usa01990)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasRankInfoWatchlistRegistrationTop]: 미국주식 관심종목 등록 상위 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa01990",
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching watchlist registration top: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoWatchlistRegistrationTop.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_period_fluctuation_rank_stock(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoPeriodFluctuationRankStock]:
        """미국주식 기간별 등락률상위(주식/업종) (usa20510)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasRankInfoPeriodFluctuationRankStock]: 미국주식 기간별 등락률상위(주식/업종) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa20510",
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching period fluctuation rank stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoPeriodFluctuationRankStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_period_fluctuation_rank_etf(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoPeriodFluctuationRankEtf]:
        """미국주식 기간별 등락률상위(ETF) (usa20511)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasRankInfoPeriodFluctuationRankEtf]: 미국주식 기간별 등락률상위(ETF) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa20511",
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching period fluctuation rank etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoPeriodFluctuationRankEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_period_fluctuation_rank_watchlist(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoPeriodFluctuationRankWatchlist]:
        """미국주식 기간별 등락률상위(관심종목) (usa20512)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasRankInfoPeriodFluctuationRankWatchlist]: 미국주식 기간별 등락률상위(관심종목) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa20512",
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching period fluctuation rank watchlist: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoPeriodFluctuationRankWatchlist.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_today_trading_volume_top_stock(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoTodayTradingVolumeTopStock]:
        """미국주식 당일 거래량 상위(주식/업종) (usa20530)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasRankInfoTodayTradingVolumeTopStock]: 미국주식 당일 거래량 상위(주식/업종) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa20530",
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching today trading volume top stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoTodayTradingVolumeTopStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_today_trading_volume_top_etf(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoTodayTradingVolumeTopEtf]:
        """미국주식 당일 거래량 상위(ETF) (usa20531)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasRankInfoTodayTradingVolumeTopEtf]: 미국주식 당일 거래량 상위(ETF) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa20531",
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching today trading volume top etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoTodayTradingVolumeTopEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_today_trading_value_top_stock(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoTodayTradingValueTopStock]:
        """미국주식 당일 거래대금 상위(주식/업종) (usa20540)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasRankInfoTodayTradingValueTopStock]: 미국주식 당일 거래대금 상위(주식/업종) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa20540",
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching today trading value top stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoTodayTradingValueTopStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_today_trading_value_top_etf(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoTodayTradingValueTopEtf]:
        """미국주식 당일 거래대금 상위(ETF) (usa20541)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasRankInfoTodayTradingValueTopEtf]: 미국주식 당일 거래대금 상위(ETF) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa20541",
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching today trading value top etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoTodayTradingValueTopEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_market_cap_top_stock(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoMarketCapTopStock]:
        """미국주식 시가총액상위(주식/업종) (usa20550)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasRankInfoMarketCapTopStock]: 미국주식 시가총액상위(주식/업종) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa20550",
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching market cap top stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoMarketCapTopStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_market_cap_top_etf(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoMarketCapTopEtf]:
        """미국주식 시가총액상위(ETF) (usa20551)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasRankInfoMarketCapTopEtf]: 미국주식 시가총액상위(ETF) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa20551",
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching market cap top etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoMarketCapTopEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_kiwoom_trading_top_stock(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoKiwoomTradingTopStock]:
        """키움 거래 상위 종목(미국주식) (usa20880)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasRankInfoKiwoomTradingTopStock]: 키움 거래 상위 종목(미국주식) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa20880",
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching kiwoom trading top stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoKiwoomTradingTopStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_kiwoom_trading_top_etf(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoKiwoomTradingTopEtf]:
        """키움 거래 상위 종목(미국 ETF) (usa20881)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasRankInfoKiwoomTradingTopEtf]: 키움 거래 상위 종목(미국 ETF) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa20881",
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching kiwoom trading top etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoKiwoomTradingTopEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_previous_day_fluctuation_rank_stock(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoPreviousDayFluctuationRankStock]:
        """미국주식 전일대비 등락률상위(주식/업종) (usa20910)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasRankInfoPreviousDayFluctuationRankStock]: 미국주식 전일대비 등락률상위(주식/업종) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa20910",
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching previous day fluctuation rank stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoPreviousDayFluctuationRankStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_previous_day_fluctuation_rank_etf(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoPreviousDayFluctuationRankEtf]:
        """미국주식 전일대비 등락률상위(ETF) (usa20911)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasRankInfoPreviousDayFluctuationRankEtf]: 미국주식 전일대비 등락률상위(ETF) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa20911",
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching previous day fluctuation rank etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoPreviousDayFluctuationRankEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_open_price_fluctuation_rank_stock(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoOpenPriceFluctuationRankStock]:
        """미국주식 시가대비 등락률상위(주식/업종) (usa20920)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasRankInfoOpenPriceFluctuationRankStock]: 미국주식 시가대비 등락률상위(주식/업종) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa20920",
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching open price fluctuation rank stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoOpenPriceFluctuationRankStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_open_price_fluctuation_rank_etf(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoOpenPriceFluctuationRankEtf]:
        """미국주식 시가대비 등락률상위(ETF) (usa20921)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasRankInfoOpenPriceFluctuationRankEtf]: 미국주식 시가대비 등락률상위(ETF) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa20921",
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching open price fluctuation rank etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoOpenPriceFluctuationRankEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_open_price_fluctuation_rank_watchlist(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoOpenPriceFluctuationRankWatchlist]:
        """미국주식 시가대비 등락률상위(관심종목) (usa20922)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasRankInfoOpenPriceFluctuationRankWatchlist]: 미국주식 시가대비 등락률상위(관심종목) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa20922",
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching open price fluctuation rank watchlist: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoOpenPriceFluctuationRankWatchlist.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_cumulative_fluctuation_top_stock(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoCumulativeFluctuationTopStock]:
        """미국주식 누적 등락률 상위(주식/업종) (usa20940)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasRankInfoCumulativeFluctuationTopStock]: 미국주식 누적 등락률 상위(주식/업종) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa20940",
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching cumulative fluctuation top stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoCumulativeFluctuationTopStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_cumulative_fluctuation_top_etf(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoCumulativeFluctuationTopEtf]:
        """미국주식 누적 등락률 상위(ETF) (usa20941)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasRankInfoCumulativeFluctuationTopEtf]: 미국주식 누적 등락률 상위(ETF) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa20941",
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching cumulative fluctuation top etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoCumulativeFluctuationTopEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_previous_day_trading_top_stock(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoPreviousDayTradingTopStock]:
        """미국주식 전일 거래상위(주식/업종) (usa20960)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasRankInfoPreviousDayTradingTopStock]: 미국주식 전일 거래상위(주식/업종) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa20960",
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching previous day trading top stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoPreviousDayTradingTopStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_previous_day_trading_top_etf(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoPreviousDayTradingTopEtf]:
        """미국주식 전일 거래상위(ETF) (usa20961)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasRankInfoPreviousDayTradingTopEtf]: 미국주식 전일 거래상위(ETF) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa20961",
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching previous day trading top etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoPreviousDayTradingTopEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_high_low_price_rise_fall_stock(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoHighLowPriceRiseFallStock]:
        """미국주식 최고최저가대비 상승하락(주식/업종) (usa24110)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasRankInfoHighLowPriceRiseFallStock]: 미국주식 최고최저가대비 상승하락(주식/업종) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa24110",
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching high low price rise fall stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoHighLowPriceRiseFallStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_high_low_price_rise_fall_etf(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoHighLowPriceRiseFallEtf]:
        """미국주식 최고최저가대비 상승하락(ETF) (usa24111)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasRankInfoHighLowPriceRiseFallEtf]: 미국주식 최고최저가대비 상승하락(ETF) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa24111",
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching high low price rise fall etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoHighLowPriceRiseFallEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_specific_date_rise_fall_stock(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoSpecificDateRiseFallStock]:
        """미국주식 특정일자 상승/하락(주식/업종) (usa24120)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasRankInfoSpecificDateRiseFallStock]: 미국주식 특정일자 상승/하락(주식/업종) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa24120",
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching specific date rise fall stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoSpecificDateRiseFallStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_specific_date_rise_fall_etf(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoSpecificDateRiseFallEtf]:
        """미국주식 특정일자 상승/하락(ETF) (usa24121)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasRankInfoSpecificDateRiseFallEtf]: 미국주식 특정일자 상승/하락(ETF) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa24121",
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching specific date rise fall etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoSpecificDateRiseFallEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_turnover_rate_top_stock(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoTurnoverRateTopStock]:
        """미국주식 회전율 상위(주식/업종) (usa24150)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasRankInfoTurnoverRateTopStock]: 미국주식 회전율 상위(주식/업종) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa24150",
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching turnover rate top stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoTurnoverRateTopStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_turnover_rate_top_etf(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoTurnoverRateTopEtf]:
        """미국주식 회전율 상위(ETF) (usa24151)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasRankInfoTurnoverRateTopEtf]: 미국주식 회전율 상위(ETF) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa24151",
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching turnover rate top etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoTurnoverRateTopEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_consecutive_rise_fall_rank_stock(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoConsecutiveRiseFallRankStock]:
        """미국주식 연속상승/하락 순위(주식/업종) (usa24160)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasRankInfoConsecutiveRiseFallRankStock]: 미국주식 연속상승/하락 순위(주식/업종) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa24160",
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching consecutive rise fall rank stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoConsecutiveRiseFallRankStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_consecutive_rise_fall_rank_etf(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoConsecutiveRiseFallRankEtf]:
        """미국주식 연속상승/하락 순위(ETF) (usa24161)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasRankInfoConsecutiveRiseFallRankEtf]: 미국주식 연속상승/하락 순위(ETF) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa24161",
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching consecutive rise fall rank etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoConsecutiveRiseFallRankEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_consecutive_rise_fall_rank_watchlist(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoConsecutiveRiseFallRankWatchlist]:
        """미국주식 연속상승/하락 순위(관심종목) (usa24162)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasRankInfoConsecutiveRiseFallRankWatchlist]: 미국주식 연속상승/하락 순위(관심종목) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa24162",
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching consecutive rise fall rank watchlist: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoConsecutiveRiseFallRankWatchlist.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_quote_remaining_volume_top_stock(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoQuoteRemainingVolumeTopStock]:
        """미국주식 호가잔량상위(주식/업종) (usa24200)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasRankInfoQuoteRemainingVolumeTopStock]: 미국주식 호가잔량상위(주식/업종) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa24200",
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching quote remaining volume top stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoQuoteRemainingVolumeTopStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_quote_remaining_volume_top_etf(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoQuoteRemainingVolumeTopEtf]:
        """미국주식 호가잔량상위(ETF) (usa24201)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasRankInfoQuoteRemainingVolumeTopEtf]: 미국주식 호가잔량상위(ETF) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa24201",
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching quote remaining volume top etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoQuoteRemainingVolumeTopEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_daytime_trading_disparity_top_stock(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoDaytimeTradingDisparityTopStock]:
        """미국주식 주간거래 괴리율 상위(주식/업종) (usa24290)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasRankInfoDaytimeTradingDisparityTopStock]: 미국주식 주간거래 괴리율 상위(주식/업종) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa24290",
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching daytime trading disparity top stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoDaytimeTradingDisparityTopStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_daytime_trading_disparity_top_etf(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoDaytimeTradingDisparityTopEtf]:
        """미국주식 주간거래 괴리율 상위(ETF) (usa24291)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasRankInfoDaytimeTradingDisparityTopEtf]: 미국주식 주간거래 괴리율 상위(ETF) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa24291",
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching daytime trading disparity top etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoDaytimeTradingDisparityTopEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)
