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
        svc_type: Literal["", "B286", "B281", "B282", "B283", "B284"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoRealtimeSymbolQueryRank]:
        """미국주식 실시간 종목 조회 순위 (usa01980)

        Args:
            svc_type (Literal["", "B286", "B281", "B282", "B283", "B284"], optional): 서비스 유형. B286:30초,B281:1분,B282:10분,B283:1시간,B284:당일. Defaults to "".
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
        body = {
            "svc_type": svc_type,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching realtime symbol query rank: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoRealtimeSymbolQueryRank.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_watchlist_registration_top(
        self,
        dt_unit_tp: Literal["", "D", "W", "M"] = "",
        stk_tp: Literal["", "A", "S", "E"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoWatchlistRegistrationTop]:
        """미국주식 관심종목 등록 상위 (usa01990)

        Args:
            dt_unit_tp (Literal["", "D", "W", "M"], optional): 일,주,월단위구분. D:일,W:주,M:월. Defaults to "".
            stk_tp (Literal["", "A", "S", "E"], optional): 시장구분. A:전체,S:주식,E:ETF. Defaults to "".
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
        body = {
            "dt_unit_tp": dt_unit_tp,
            "stk_tp": stk_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching watchlist registration top: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoWatchlistRegistrationTop.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_period_fluctuation_rank_stock(
        self,
        stex_tp: Literal["", "0", "1", "2", "3"] = "",
        inds_cd: str = "",
        stk_tp: Literal["", "0", "1"] = "",
        stk_cnd: Literal["", "0", "1", "2"] = "",
        tm: Literal["", "1", "5", "10", "30"] = "",
        trde_qty_tp: Literal["", "0", "10", "15", "20", "30", "50", "100", "300", "500"] = "",
        pric_cnd: Literal["", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] = "",
        trde_prica_cnd: Literal[
            "", "0", "1", "3", "5", "10", "30", "50", "100", "300", "500", "1000", "3000", "5000"
        ] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoPeriodFluctuationRankStock]:
        """미국주식 기간별 등락률상위(주식/업종) (usa20510)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소구분. 0:전체,1:NYSE,2:NASDAQ,3:AMEX. Defaults to "".
            inds_cd (str, optional): 업종코드. 000:전체, usa10101 API 참고, stk_tp(종목구분) 1일 경우. Defaults to "".
            stk_tp (Literal["", "0", "1"], optional): 종목구분. 0:전체,1:주식. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목조건. 0:전체,1:증100%,2:증50%. Defaults to "".
            tm (Literal["", "1", "5", "10", "30"], optional): n일전 구분. 1:전일 5:5일 10:10일 30:30일,기본값:1. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            pric_cnd (Literal, optional): 가격조건. 0:전체,1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
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
        body = {
            "stex_tp": stex_tp,
            "inds_cd": inds_cd,
            "stk_tp": stk_tp,
            "stk_cnd": stk_cnd,
            "tm": tm,
            "trde_qty_tp": trde_qty_tp,
            "pric_cnd": pric_cnd,
            "trde_prica_cnd": trde_prica_cnd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching period fluctuation rank stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoPeriodFluctuationRankStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_period_fluctuation_rank_etf(
        self,
        stex_tp: Literal["", "0", "1", "2", "3"] = "",
        etf_cat1: str = "",
        etf_cat2: str = "",
        stk_cnd: Literal["", "0", "1", "2"] = "",
        tm: Literal["", "1", "5", "10", "30"] = "",
        trde_qty_tp: Literal["", "0", "10", "15", "20", "30", "50", "100", "300", "500"] = "",
        pric_cnd: Literal["", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] = "",
        trde_prica_cnd: Literal[
            "", "0", "1", "3", "5", "10", "30", "50", "100", "300", "500", "1000", "3000", "5000"
        ] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoPeriodFluctuationRankEtf]:
        """미국주식 기간별 등락률상위(ETF) (usa20511)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소구분. 0:전체,1:NYSE,2:NASDAQ,3:AMEX. Defaults to "".
            etf_cat1 (str, optional): ETF코드1. ETF 대카테고리코드, usa10105 cate1 속성 참고. Defaults to "".
            etf_cat2 (str, optional): ETF코드2. ETF 중카테고리코드, usa10105 cate2 속성 참고. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목조건. 0:전체,1:증100%,2:증50%. Defaults to "".
            tm (Literal["", "1", "5", "10", "30"], optional): n일전 구분. 1:전일 5:5일 10:10일 30:30일,기본값:1. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            pric_cnd (Literal, optional): 가격조건. 0:전체,1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
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
        body = {
            "stex_tp": stex_tp,
            "etf_cat1": etf_cat1,
            "etf_cat2": etf_cat2,
            "stk_cnd": stk_cnd,
            "tm": tm,
            "trde_qty_tp": trde_qty_tp,
            "pric_cnd": pric_cnd,
            "trde_prica_cnd": trde_prica_cnd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching period fluctuation rank etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoPeriodFluctuationRankEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_period_fluctuation_rank_watchlist(
        self,
        stex_tp: Literal["", "0", "1", "2", "3"] = "",
        stk_cd: list[dict[str, str]] | None = None,
        tm: Literal["", "1", "5", "10", "30"] = "",
        trde_qty_tp: Literal["", "0", "10", "15", "20", "30", "50", "100", "300", "500"] = "",
        stk_cnd: Literal["", "0", "1", "2"] = "",
        pric_cnd: Literal["", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] = "",
        trde_prica_cnd: Literal[
            "", "0", "1", "3", "5", "10", "30", "50", "100", "300", "500", "1000", "3000", "5000"
        ] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoPeriodFluctuationRankWatchlist]:
        """미국주식 기간별 등락률상위(관심종목) (usa20512)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소구분. 0:전체,1:NYSE,2:NASDAQ,3:AMEX. Defaults to "".
            stk_cd (list[dict[str, str]] | None, optional): 종목코드. [{'stex_tp':'거래소구분','stk_cd':'종목코드'},...]. Defaults to None.
            tm (Literal["", "1", "5", "10", "30"], optional): n일전 설정. 1:전일 5:5일 10:10일 30:30일,기본값:1. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목조건. 0:전체,1:증100%,2:증50%. Defaults to "".
            pric_cnd (Literal, optional): 가격조건. 0:전체,1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
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
        body = {
            "stex_tp": stex_tp,
            "stk_cd": stk_cd if stk_cd is not None else [],
            "tm": tm,
            "trde_qty_tp": trde_qty_tp,
            "stk_cnd": stk_cnd,
            "pric_cnd": pric_cnd,
            "trde_prica_cnd": trde_prica_cnd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching period fluctuation rank watchlist: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoPeriodFluctuationRankWatchlist.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_today_trading_volume_top_stock(
        self,
        stex_tp: Literal["", "0", "1", "2", "3"] = "",
        inds_cd: str = "",
        stk_tp: Literal["", "0", "1"] = "",
        trde_qty_tp: Literal["", "0", "10", "15", "20", "30", "50", "100", "300", "500"] = "",
        qry_tp: Literal["", "0", "1", "2"] = "",
        stk_cnd: Literal["", "0", "1", "2"] = "",
        pric_cnd: Literal["", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] = "",
        trde_prica_cnd: Literal[
            "", "0", "1", "3", "5", "10", "30", "50", "100", "300", "500", "1000", "3000", "5000"
        ] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoTodayTradingVolumeTopStock]:
        """미국주식 당일 거래량 상위(주식/업종) (usa20530)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소 구분. 0:전체,1:NYSE,2:NASDAQ,3:AMEX. Defaults to "".
            inds_cd (str, optional): 업종코드. 000:전체, usa10101 API 참고, stk_tp(종목구분) 1일 경우. Defaults to "".
            stk_tp (Literal["", "0", "1"], optional): 종목 구분. 0:전체,1:주식. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            qry_tp (Literal["", "0", "1", "2"], optional): 정렬기준 구분. 0:거래량상위,1:거래대금상위,2:거래회전율상위. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목필터 구분. 0:전체,1:증100%만보기,2:증50%만보기. Defaults to "".
            pric_cnd (Literal, optional): 검색가격대 구분. 0:전체,1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
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
        body = {
            "stex_tp": stex_tp,
            "inds_cd": inds_cd,
            "stk_tp": stk_tp,
            "trde_qty_tp": trde_qty_tp,
            "qry_tp": qry_tp,
            "stk_cnd": stk_cnd,
            "pric_cnd": pric_cnd,
            "trde_prica_cnd": trde_prica_cnd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching today trading volume top stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoTodayTradingVolumeTopStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_today_trading_volume_top_etf(
        self,
        stex_tp: Literal["", "0", "1", "2", "3"] = "",
        etf_cat1: str = "",
        etf_cat2: str = "",
        trde_qty_tp: Literal["", "0", "10", "15", "20", "30", "50", "100", "300", "500"] = "",
        qry_tp: Literal["", "0", "1", "2"] = "",
        stk_cnd: Literal["", "0", "1", "2"] = "",
        pric_cnd: Literal["", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] = "",
        trde_prica_cnd: Literal[
            "", "0", "1", "3", "5", "10", "30", "50", "100", "300", "500", "1000", "3000", "5000"
        ] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoTodayTradingVolumeTopEtf]:
        """미국주식 당일 거래량 상위(ETF) (usa20531)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소 구분. 0:전체,1:NYSE,2:NASDAQ,3:AMEX. Defaults to "".
            etf_cat1 (str, optional): ETF카테고리코드1. ETF 대카테고리코드, usa10105 cate1 속성 참고. Defaults to "".
            etf_cat2 (str, optional): ETF카테고리코드2. ETF 중카테고리코드, usa10105 cate2 속성 참고. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            qry_tp (Literal["", "0", "1", "2"], optional): 정렬기준 구분. 0:거래량상위,1:거래대금상위,2:거래회전율상위. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목필터 구분. 0:전체,1:증100%만보기,2:증50%만보기. Defaults to "".
            pric_cnd (Literal, optional): 검색가격대 구분. 0:전체,1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
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
        body = {
            "stex_tp": stex_tp,
            "etf_cat1": etf_cat1,
            "etf_cat2": etf_cat2,
            "trde_qty_tp": trde_qty_tp,
            "qry_tp": qry_tp,
            "stk_cnd": stk_cnd,
            "pric_cnd": pric_cnd,
            "trde_prica_cnd": trde_prica_cnd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching today trading volume top etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoTodayTradingVolumeTopEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_today_trading_value_top_stock(
        self,
        stex_tp: Literal["", "0", "1", "2", "3"] = "",
        inds_cd: str = "",
        stk_tp: Literal["", "0", "1"] = "",
        trde_qty_tp: Literal["", "0", "10", "15", "20", "30", "50", "100", "300", "500"] = "",
        stk_cnd: Literal["", "0", "1", "2"] = "",
        pric_cnd: Literal["", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] = "",
        trde_prica_cnd: Literal[
            "", "0", "1", "3", "5", "10", "30", "50", "100", "300", "500", "1000", "3000", "5000"
        ] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoTodayTradingValueTopStock]:
        """미국주식 당일 거래대금 상위(주식/업종) (usa20540)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소 구분. 0:전체,1:NYSE,2:NASDAQ,3:AMEX. Defaults to "".
            inds_cd (str, optional): 업종코드. 000:전체, usa10101 API 참고, stk_tp(종목구분) 1일 경우. Defaults to "".
            stk_tp (Literal["", "0", "1"], optional): 종목 구분. 0:전체,1:주식. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목필터 구분. 0:전체,1:증100%만보기,2:증50%만보기. Defaults to "".
            pric_cnd (Literal, optional): 검색가격대 구분. 0:전체,1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
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
        body = {
            "stex_tp": stex_tp,
            "inds_cd": inds_cd,
            "stk_tp": stk_tp,
            "trde_qty_tp": trde_qty_tp,
            "stk_cnd": stk_cnd,
            "pric_cnd": pric_cnd,
            "trde_prica_cnd": trde_prica_cnd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching today trading value top stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoTodayTradingValueTopStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_today_trading_value_top_etf(
        self,
        stex_tp: Literal["", "0", "1", "2", "3"] = "",
        etf_cat1: str = "",
        etf_cat2: str = "",
        trde_qty_tp: Literal["", "0", "10", "15", "20", "30", "50", "100", "300", "500"] = "",
        stk_cnd: Literal["", "0", "1", "2"] = "",
        pric_cnd: Literal["", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] = "",
        trde_prica_cnd: Literal[
            "", "0", "1", "3", "5", "10", "30", "50", "100", "300", "500", "1000", "3000", "5000"
        ] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoTodayTradingValueTopEtf]:
        """미국주식 당일 거래대금 상위(ETF) (usa20541)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소 구분. 0:전체,1:NYSE,2:NASDAQ,3:AMEX. Defaults to "".
            etf_cat1 (str, optional): ETF카테고리코드1. ETF 대카테고리코드, usa10105 cate1 속성 참고. Defaults to "".
            etf_cat2 (str, optional): ETF카테고리코드2. ETF 중카테고리코드, usa10105 cate2 속성 참고. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목필터 구분. 0:전체,1:증100%만보기,2:증50%만보기. Defaults to "".
            pric_cnd (Literal, optional): 검색가격대 구분. 0:전체,1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
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
        body = {
            "stex_tp": stex_tp,
            "etf_cat1": etf_cat1,
            "etf_cat2": etf_cat2,
            "trde_qty_tp": trde_qty_tp,
            "stk_cnd": stk_cnd,
            "pric_cnd": pric_cnd,
            "trde_prica_cnd": trde_prica_cnd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching today trading value top etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoTodayTradingValueTopEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_market_cap_top_stock(
        self,
        stex_tp: Literal["", "0", "1", "2", "3"] = "",
        inds_cd: str = "",
        stk_tp: Literal["", "0", "1"] = "",
        trde_qty_tp: Literal["", "0", "10", "15", "20", "30", "50", "100", "300", "500"] = "",
        stk_cnd: Literal["", "0", "1", "2"] = "",
        pric_cnd: Literal["", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] = "",
        trde_prica_cnd: Literal[
            "", "0", "1", "3", "5", "10", "30", "50", "100", "300", "500", "1000", "3000", "5000"
        ] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoMarketCapTopStock]:
        """미국주식 시가총액상위(주식/업종) (usa20550)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소 구분. 0:전체,1:NYSE,2:NASDAQ,3:AMEX. Defaults to "".
            inds_cd (str, optional): 업종코드. 000:전체, usa10101 API 참고, stk_tp(종목구분) 1일 경우. Defaults to "".
            stk_tp (Literal["", "0", "1"], optional): 종목 구분. 0:전체,1:주식. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목필터 구분. 0:전체,1:증100%만보기,2:증50%만보기. Defaults to "".
            pric_cnd (Literal, optional): 검색가격대 구분. 0:전체,1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
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
        body = {
            "stex_tp": stex_tp,
            "inds_cd": inds_cd,
            "stk_tp": stk_tp,
            "trde_qty_tp": trde_qty_tp,
            "stk_cnd": stk_cnd,
            "pric_cnd": pric_cnd,
            "trde_prica_cnd": trde_prica_cnd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching market cap top stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoMarketCapTopStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_market_cap_top_etf(
        self,
        stex_tp: Literal["", "0", "1", "2", "3"] = "",
        etf_cat1: str = "",
        etf_cat2: str = "",
        trde_qty_tp: Literal["", "0", "10", "15", "20", "30", "50", "100", "300", "500"] = "",
        stk_cnd: Literal["", "0", "1", "2"] = "",
        pric_cnd: Literal["", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] = "",
        trde_prica_cnd: Literal[
            "", "0", "1", "3", "5", "10", "30", "50", "100", "300", "500", "1000", "3000", "5000"
        ] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoMarketCapTopEtf]:
        """미국주식 시가총액상위(ETF) (usa20551)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소 구분. 0:전체,1:NYSE,2:NASDAQ,3:AMEX. Defaults to "".
            etf_cat1 (str, optional): ETF카테고리코드1. ETF 대카테고리코드, usa10105 cate1 속성 참고. Defaults to "".
            etf_cat2 (str, optional): ETF카테고리코드2. ETF 중카테고리코드, usa10105 cate2 속성 참고. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목필터 구분. 0:전체,1:증100%만보기,2:증50%만보기. Defaults to "".
            pric_cnd (Literal, optional): 검색가격대 구분. 0:전체,1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
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
        body = {
            "stex_tp": stex_tp,
            "etf_cat1": etf_cat1,
            "etf_cat2": etf_cat2,
            "trde_qty_tp": trde_qty_tp,
            "stk_cnd": stk_cnd,
            "pric_cnd": pric_cnd,
            "trde_prica_cnd": trde_prica_cnd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching market cap top etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoMarketCapTopEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_kiwoom_trading_top_stock(
        self,
        qry_tp: Literal["", "1", "2", "3", "4", "5", "6", "7"] = "",
        dt_unit_tp: Literal["", "1", "2", "3", "4", "5", "6", "7", "8"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoKiwoomTradingTopStock]:
        """키움 거래 상위 종목(미국주식) (usa20880)

        Args:
            qry_tp (Literal, optional): 조회구분. 1:매수상위,2:매도상위,3:순매수상위,4:보유잔고상위,5:보유고객상위,6:거래비중상위,7:거래대금상위. Defaults to "".
            dt_unit_tp (Literal, optional): 일,주,월단위구분. 1:일,2:주,3:월,4:년,5:10분,6:30분,7:60분,8:5분. Defaults to "".
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
        body = {
            "qry_tp": qry_tp,
            "dt_unit_tp": dt_unit_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching kiwoom trading top stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoKiwoomTradingTopStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_kiwoom_trading_top_etf(
        self,
        qry_tp: Literal["", "1", "2", "3", "4", "5", "6", "7"] = "",
        dt_unit_tp: Literal["", "1", "2", "3", "4", "5", "6", "7", "8"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoKiwoomTradingTopEtf]:
        """키움 거래 상위 종목(미국 ETF) (usa20881)

        Args:
            qry_tp (Literal, optional): 조회구분. 1:매수상위,2:매도상위,3:순매수상위,4:보유잔고상위,5:보유고객상위,6:거래비중상위,7:거래대금상위. Defaults to "".
            dt_unit_tp (Literal, optional): 일,주,월단위구분. 1:일,2:주,3:월,4:년,5:10분,6:30분,7:60분,8:5분. Defaults to "".
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
        body = {
            "qry_tp": qry_tp,
            "dt_unit_tp": dt_unit_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching kiwoom trading top etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoKiwoomTradingTopEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_previous_day_fluctuation_rank_stock(
        self,
        stex_tp: Literal["", "0", "1", "2", "3"] = "",
        inds_cd: str = "",
        inds_cls_tp: Literal["", "0", "1", "2", "3"] = "",
        sort_tp: Literal["", "1", "2", "3", "4", "5"] = "",
        stk_tp: Literal["", "0", "1"] = "",
        stk_cnd: Literal["", "0", "1", "2"] = "",
        pric_cnd: Literal["", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] = "",
        trde_prica_cnd: Literal[
            "", "0", "1", "3", "5", "10", "30", "50", "100", "300", "500", "1000", "3000", "5000"
        ] = "",
        trde_qty_tp: Literal["", "0", "10", "15", "20", "30", "50", "100", "300", "500"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoPreviousDayFluctuationRankStock]:
        """미국주식 전일대비 등락률상위(주식/업종) (usa20910)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소구분. 0:전체,1:NYSE,2:NASDAQ,3:AMEX. Defaults to "".
            inds_cd (str, optional): 업종코드. 000:전체, usa10101 API 참고, stk_tp(종목구분) 1일 경우. Defaults to "".
            inds_cls_tp (Literal["", "0", "1", "2", "3"], optional): 미국업종구분. stk_tp 0일경우, 0:전체,1:다우30,2:나스닥100,3:S&P500. Defaults to "".
            sort_tp (Literal["", "1", "2", "3", "4", "5"], optional): 정렬기준. 1:전일대비 상승률,2:전일대비 상승폭,3:보합,4:전일대비 하락률,5:전일대비 하락폭. Defaults to "".
            stk_tp (Literal["", "0", "1"], optional): 종목구분. 0:전체,1:주식. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목조건. 0:전체,1:증100%,2:증50%. Defaults to "".
            pric_cnd (Literal, optional): 가격조건. 0:전체,1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
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
        body = {
            "stex_tp": stex_tp,
            "inds_cd": inds_cd,
            "inds_cls_tp": inds_cls_tp,
            "sort_tp": sort_tp,
            "stk_tp": stk_tp,
            "stk_cnd": stk_cnd,
            "pric_cnd": pric_cnd,
            "trde_prica_cnd": trde_prica_cnd,
            "trde_qty_tp": trde_qty_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching previous day fluctuation rank stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoPreviousDayFluctuationRankStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_previous_day_fluctuation_rank_etf(
        self,
        stex_tp: Literal["", "0", "1", "2", "3"] = "",
        etf_cat1: str = "",
        etf_cat2: str = "",
        sort_tp: Literal["", "1", "2", "3", "4", "5"] = "",
        stk_cnd: Literal["", "0", "1", "2"] = "",
        pric_cnd: Literal["", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] = "",
        trde_prica_cnd: Literal[
            "", "0", "1", "3", "5", "10", "30", "50", "100", "300", "500", "1000", "3000", "5000"
        ] = "",
        trde_qty_tp: Literal["", "0", "10", "15", "20", "30", "50", "100", "300", "500"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoPreviousDayFluctuationRankEtf]:
        """미국주식 전일대비 등락률상위(ETF) (usa20911)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소구분. 0:전체,1:NYSE,2:NASDAQ,3:AMEX. Defaults to "".
            etf_cat1 (str, optional): ETF카테고리코드1. ETF 대카테고리코드, usa10105 cate1 속성 참고. Defaults to "".
            etf_cat2 (str, optional): ETF카테고리코드2. ETF 중카테고리코드, usa10105 cate2 속성 참고. Defaults to "".
            sort_tp (Literal["", "1", "2", "3", "4", "5"], optional): 정렬기준. 1:전일대비 상승률,2:전일대비 상승폭,3:보합,4:전일대비 하락률,5:전일대비 하락폭. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목조건. 0:전체,1:증100%,2:증50%. Defaults to "".
            pric_cnd (Literal, optional): 가격조건. 0:전체,1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
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
        body = {
            "stex_tp": stex_tp,
            "etf_cat1": etf_cat1,
            "etf_cat2": etf_cat2,
            "sort_tp": sort_tp,
            "stk_cnd": stk_cnd,
            "pric_cnd": pric_cnd,
            "trde_prica_cnd": trde_prica_cnd,
            "trde_qty_tp": trde_qty_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching previous day fluctuation rank etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoPreviousDayFluctuationRankEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_open_price_fluctuation_rank_stock(
        self,
        stex_tp: Literal["", "0", "1", "2", "3"] = "",
        inds_cd: str = "",
        trde_qty_tp: Literal["", "0", "10", "15", "20", "30", "50", "100", "300", "500"] = "",
        stk_tp: Literal["", "0", "1"] = "",
        stk_cnd: Literal["", "0", "1", "2"] = "",
        pric_cnd: Literal["", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] = "",
        trde_prica_cnd: Literal[
            "", "0", "1", "3", "5", "10", "30", "50", "100", "300", "500", "1000", "3000", "5000"
        ] = "",
        sort_tp: Literal["", "1", "2"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoOpenPriceFluctuationRankStock]:
        """미국주식 시가대비 등락률상위(주식/업종) (usa20920)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소구분. 0:전체,1:NYSE,2:NASDAQ,3:AMEX. Defaults to "".
            inds_cd (str, optional): 업종코드. 000:전체, usa10101 API 참고, stk_tp(종목구분) 1일 경우. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            stk_tp (Literal["", "0", "1"], optional): 종목구분. 0:전체,1:주식. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목조건. 0:전체,1:증100%,2:증50%. Defaults to "".
            pric_cnd (Literal, optional): 가격조건. 0:전체,1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
            sort_tp (Literal["", "1", "2"], optional): 정렬기준. 1:상승률,2:하락률. Defaults to "".
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
        body = {
            "stex_tp": stex_tp,
            "inds_cd": inds_cd,
            "trde_qty_tp": trde_qty_tp,
            "stk_tp": stk_tp,
            "stk_cnd": stk_cnd,
            "pric_cnd": pric_cnd,
            "trde_prica_cnd": trde_prica_cnd,
            "sort_tp": sort_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching open price fluctuation rank stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoOpenPriceFluctuationRankStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_open_price_fluctuation_rank_etf(
        self,
        stex_tp: Literal["", "0", "1", "2", "3"] = "",
        etf_cat1: str = "",
        etf_cat2: str = "",
        trde_qty_tp: Literal["", "0", "10", "15", "20", "30", "50", "100", "300", "500"] = "",
        stk_cnd: Literal["", "0", "1", "2"] = "",
        pric_cnd: Literal["", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] = "",
        trde_prica_cnd: Literal[
            "", "0", "1", "3", "5", "10", "30", "50", "100", "300", "500", "1000", "3000", "5000"
        ] = "",
        sort_tp: Literal["", "1", "2"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoOpenPriceFluctuationRankEtf]:
        """미국주식 시가대비 등락률상위(ETF) (usa20921)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소구분. 0:전체,1:NYSE,2:NASDAQ,3:AMEX. Defaults to "".
            etf_cat1 (str, optional): ETF카테고리코드1. ETF 대카테고리코드, usa10105 cate1 속성 참고. Defaults to "".
            etf_cat2 (str, optional): ETF카테고리코드2. ETF 중카테고리코드, usa10105 cate2 속성 참고. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목조건. 0:전체,1:증100%,2:증50%. Defaults to "".
            pric_cnd (Literal, optional): 가격조건. 0:전체,1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
            sort_tp (Literal["", "1", "2"], optional): 정렬기준. 1:상승률,2:하락률. Defaults to "".
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
        body = {
            "stex_tp": stex_tp,
            "etf_cat1": etf_cat1,
            "etf_cat2": etf_cat2,
            "trde_qty_tp": trde_qty_tp,
            "stk_cnd": stk_cnd,
            "pric_cnd": pric_cnd,
            "trde_prica_cnd": trde_prica_cnd,
            "sort_tp": sort_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching open price fluctuation rank etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoOpenPriceFluctuationRankEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_open_price_fluctuation_rank_watchlist(
        self,
        stex_tp: Literal["", "0", "1", "2", "3"] = "",
        stk_cd: list[dict[str, str]] | None = None,
        sort_tp: Literal["", "1", "2"] = "",
        stk_tp: Literal["", "0", "1", "2"] = "",
        stk_cnd: Literal["", "0", "1", "2"] = "",
        pric_cnd: Literal["", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] = "",
        trde_prica_cnd: Literal[
            "", "0", "1", "3", "5", "10", "30", "50", "100", "300", "500", "1000", "3000", "5000"
        ] = "",
        trde_qty_tp: Literal["", "0", "10", "15", "20", "30", "50", "100", "300", "500"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoOpenPriceFluctuationRankWatchlist]:
        """미국주식 시가대비 등락률상위(관심종목) (usa20922)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소구분. 0:전체,1:NYSE,2:NASDAQ,3:AMEX. Defaults to "".
            stk_cd (list[dict[str, str]] | None, optional): 관심종목코드. [{'stex_tp':'거래소구분','stk_cd':'종목코드'},...]. Defaults to None.
            sort_tp (Literal["", "1", "2"], optional): 정렬기준. 1:상승률,2:하락률. Defaults to "".
            stk_tp (Literal["", "0", "1", "2"], optional): 종목구분. 0:전체,1:주식,2:ETF. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목조건. 0:전체,1:증100%,2:증50%. Defaults to "".
            pric_cnd (Literal, optional): 가격조건. 0:전체,1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
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
        body = {
            "stex_tp": stex_tp,
            "stk_cd": stk_cd if stk_cd is not None else [],
            "sort_tp": sort_tp,
            "stk_tp": stk_tp,
            "stk_cnd": stk_cnd,
            "pric_cnd": pric_cnd,
            "trde_prica_cnd": trde_prica_cnd,
            "trde_qty_tp": trde_qty_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching open price fluctuation rank watchlist: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoOpenPriceFluctuationRankWatchlist.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_cumulative_fluctuation_top_stock(
        self,
        stex_tp: Literal["", "0", "1", "2", "3"] = "",
        inds_cd: str = "",
        stk_tp: Literal["", "0", "1"] = "",
        sort_tp: Literal["", "0", "1", "3", "4"] = "",
        pric_cnd1: str = "",
        pric_cnd2: str = "",
        base_dt: str = "",
        stk_cnd: Literal["", "0"] = "",
        trde_qty_tp: Literal["", "0", "10", "15", "20", "30", "50", "100", "300", "500"] = "",
        pric_cnd: Literal["", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] = "",
        trde_prica_cnd: Literal[
            "", "0", "1", "3", "5", "10", "30", "50", "100", "300", "500", "1000", "3000", "5000"
        ] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoCumulativeFluctuationTopStock]:
        """미국주식 누적 등락률 상위(주식/업종) (usa20940)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소 구분. 0:전체,1:NYSE,2:AMEX,3:NASDAQ. Defaults to "".
            inds_cd (str, optional): 업종코드. 000:전체, usa10101 API 참고, stk_tp(종목구분) 1일 경우. Defaults to "".
            stk_tp (Literal["", "0", "1"], optional): 종목구분. 0:전체,1:주식. Defaults to "".
            sort_tp (Literal["", "0", "1", "3", "4"], optional): 정렬기준구분. 0:상승률,1:상승폭,3:하락률,4:하락폭. Defaults to "".
            pric_cnd1 (str, optional): 가격1 구분. Defaults to "".
            pric_cnd2 (str, optional): 가격2 구분. Defaults to "".
            base_dt (str, optional): 기준일자. YYYYMMDD. Defaults to "".
            stk_cnd (Literal["", "0"], optional): 종목조건. 0:전체. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            pric_cnd (Literal, optional): 검색가격대 구분. 0:전체 1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
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
        body = {
            "stex_tp": stex_tp,
            "inds_cd": inds_cd,
            "stk_tp": stk_tp,
            "sort_tp": sort_tp,
            "pric_cnd1": pric_cnd1,
            "pric_cnd2": pric_cnd2,
            "base_dt": base_dt,
            "stk_cnd": stk_cnd,
            "trde_qty_tp": trde_qty_tp,
            "pric_cnd": pric_cnd,
            "trde_prica_cnd": trde_prica_cnd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching cumulative fluctuation top stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoCumulativeFluctuationTopStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_cumulative_fluctuation_top_etf(
        self,
        stex_tp: Literal["", "0", "1", "2", "3"] = "",
        etf_cat1: str = "",
        etf_cat2: str = "",
        sort_tp: Literal["", "0", "1", "3", "4"] = "",
        pric_cnd1: str = "",
        pric_cnd2: str = "",
        base_dt: str = "",
        stk_cnd: Literal["", "0"] = "",
        trde_qty_tp: Literal["", "0", "10", "15", "20", "30", "50", "100", "300", "500"] = "",
        pric_cnd: Literal["", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] = "",
        trde_prica_cnd: Literal[
            "", "0", "1", "3", "5", "10", "30", "50", "100", "300", "500", "1000", "3000", "5000"
        ] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoCumulativeFluctuationTopEtf]:
        """미국주식 누적 등락률 상위(ETF) (usa20941)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소 구분. 0:전체,1:NYSE,2:AMEX,3:NASDAQ. Defaults to "".
            etf_cat1 (str, optional): ETF카테고리코드1. ETF 대카테고리코드, usa10105 cate1 속성 참고. Defaults to "".
            etf_cat2 (str, optional): ETF카테고리코드2. ETF 중카테고리코드, usa10105 cate2 속성 참고. Defaults to "".
            sort_tp (Literal["", "0", "1", "3", "4"], optional): 정렬기준구분. 0:상승률,1:상승폭,3:하락률,4:하락폭. Defaults to "".
            pric_cnd1 (str, optional): 가격1 구분. Defaults to "".
            pric_cnd2 (str, optional): 가격2 구분. Defaults to "".
            base_dt (str, optional): 기준일자. YYYYMMDD. Defaults to "".
            stk_cnd (Literal["", "0"], optional): 종목조건. 0:전체. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            pric_cnd (Literal, optional): 검색가격대 구분. 0:전체 1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
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
        body = {
            "stex_tp": stex_tp,
            "etf_cat1": etf_cat1,
            "etf_cat2": etf_cat2,
            "sort_tp": sort_tp,
            "pric_cnd1": pric_cnd1,
            "pric_cnd2": pric_cnd2,
            "base_dt": base_dt,
            "stk_cnd": stk_cnd,
            "trde_qty_tp": trde_qty_tp,
            "pric_cnd": pric_cnd,
            "trde_prica_cnd": trde_prica_cnd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching cumulative fluctuation top etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoCumulativeFluctuationTopEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_previous_day_trading_top_stock(
        self,
        stex_tp: Literal["", "0", "1", "2", "3"] = "",
        inds_cd: str = "",
        stk_tp: Literal["", "0", "1"] = "",
        qry_tp: Literal["", "0", "1"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoPreviousDayTradingTopStock]:
        """미국주식 전일 거래상위(주식/업종) (usa20960)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소 구분. 0:전체,1:NYSE,2:AMEX,3:NASDAQ. Defaults to "".
            inds_cd (str, optional): 업종코드. 000:전체, usa10101 API 참고, stk_tp(종목구분) 1일 경우. Defaults to "".
            stk_tp (Literal["", "0", "1"], optional): 종목 구분. 0:전체,1:주식. Defaults to "".
            qry_tp (Literal["", "0", "1"], optional): 정렬기준구분. 0:전일거래량상위,1:전일거래대금상위. Defaults to "".
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
        body = {
            "stex_tp": stex_tp,
            "inds_cd": inds_cd,
            "stk_tp": stk_tp,
            "qry_tp": qry_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching previous day trading top stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoPreviousDayTradingTopStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_previous_day_trading_top_etf(
        self,
        stex_tp: Literal["", "0", "1", "2", "3"] = "",
        etf_cat1: str = "",
        etf_cat2: str = "",
        qry_tp: Literal["", "0", "1"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoPreviousDayTradingTopEtf]:
        """미국주식 전일 거래상위(ETF) (usa20961)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소 구분. 0:전체,1:NYSE,2:AMEX,3:NASDAQ. Defaults to "".
            etf_cat1 (str, optional): ETF카테고리코드1. ETF 대카테고리코드, usa10105 cate1 속성 참고. Defaults to "".
            etf_cat2 (str, optional): ETF카테고리코드2. ETF 중카테고리코드, usa10105 cate2 속성 참고. Defaults to "".
            qry_tp (Literal["", "0", "1"], optional): 정렬기준구분. 0:전일거래량상위,1:전일거래대금상위. Defaults to "".
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
        body = {
            "stex_tp": stex_tp,
            "etf_cat1": etf_cat1,
            "etf_cat2": etf_cat2,
            "qry_tp": qry_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching previous day trading top etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoPreviousDayTradingTopEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_high_low_price_rise_fall_stock(
        self,
        stex_tp: Literal["", "0", "1", "2", "3"] = "",
        inds_cd: str = "",
        stk_tp: Literal["", "0", "1"] = "",
        sort_tp: Literal["", "0", "1"] = "",
        dt_tp: Literal["", "0", "1"] = "",
        stk_cnd: Literal["", "0", "1", "2"] = "",
        trde_qty_tp: Literal["", "0", "10", "15", "20", "30", "50", "100", "300", "500"] = "",
        pric_cnd: Literal["", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] = "",
        trde_prica_cnd: Literal[
            "", "0", "1", "3", "5", "10", "30", "50", "100", "300", "500", "1000", "3000", "5000"
        ] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoHighLowPriceRiseFallStock]:
        """미국주식 최고최저가대비 상승하락(주식/업종) (usa24110)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소 구분. 0:전체,1:NYSE,2:AMEX,3:NASDAQ. Defaults to "".
            inds_cd (str, optional): 업종코드. 000:전체, usa10101 API 참고, stk_tp(종목구분) 1일 경우. Defaults to "".
            stk_tp (Literal["", "0", "1"], optional): 종목 구분. 0:전체,1:주식. Defaults to "".
            sort_tp (Literal["", "0", "1"], optional): 정렬기준구분. 0:저가대비상승,1:고가대비하락. Defaults to "".
            dt_tp (Literal["", "0", "1"], optional): 기간구분. 0:연중,1:52주. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목조건. 0:전체,1:증100%,2:증50%. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            pric_cnd (Literal, optional): 가격조건. 0:전체 1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
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
        body = {
            "stex_tp": stex_tp,
            "inds_cd": inds_cd,
            "stk_tp": stk_tp,
            "sort_tp": sort_tp,
            "dt_tp": dt_tp,
            "stk_cnd": stk_cnd,
            "trde_qty_tp": trde_qty_tp,
            "pric_cnd": pric_cnd,
            "trde_prica_cnd": trde_prica_cnd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching high low price rise fall stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoHighLowPriceRiseFallStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_high_low_price_rise_fall_etf(
        self,
        stex_tp: Literal["", "0", "1", "2", "3"] = "",
        etf_cat1: str = "",
        etf_cat2: str = "",
        sort_tp: Literal["", "0", "1"] = "",
        dt_tp: Literal["", "0", "1"] = "",
        stk_cnd: Literal["", "0", "1", "2"] = "",
        trde_qty_tp: Literal["", "0", "10", "15", "20", "30", "50", "100", "300", "500"] = "",
        pric_cnd: Literal["", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] = "",
        trde_prica_cnd: Literal[
            "", "0", "1", "3", "5", "10", "30", "50", "100", "300", "500", "1000", "3000", "5000"
        ] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoHighLowPriceRiseFallEtf]:
        """미국주식 최고최저가대비 상승하락(ETF) (usa24111)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소 구분. 0:전체,1:NYSE,2:AMEX,3:NASDAQ. Defaults to "".
            etf_cat1 (str, optional): ETF카테고리코드1. ETF 대카테고리코드, usa10105 cate1 속성 참고. Defaults to "".
            etf_cat2 (str, optional): ETF카테고리코드2. ETF 중카테고리코드, usa10105 cate2 속성 참고. Defaults to "".
            sort_tp (Literal["", "0", "1"], optional): 정렬기준구분. 0:저가대비상승,1:고가대비하락. Defaults to "".
            dt_tp (Literal["", "0", "1"], optional): 기간구분. 0:연중,1:52주. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목조건. 0:전체,1:증100%,2:증50%. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            pric_cnd (Literal, optional): 가격조건. 0:전체 1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
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
        body = {
            "stex_tp": stex_tp,
            "etf_cat1": etf_cat1,
            "etf_cat2": etf_cat2,
            "sort_tp": sort_tp,
            "dt_tp": dt_tp,
            "stk_cnd": stk_cnd,
            "trde_qty_tp": trde_qty_tp,
            "pric_cnd": pric_cnd,
            "trde_prica_cnd": trde_prica_cnd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching high low price rise fall etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoHighLowPriceRiseFallEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_specific_date_rise_fall_stock(
        self,
        stex_tp: Literal["", "0", "1", "2", "3"] = "",
        inds_cd: str = "",
        stk_tp: Literal["", "0", "1"] = "",
        stk_cnd: Literal["", "0", "1", "2"] = "",
        pric_cnd: Literal["", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] = "",
        trde_qty_tp: Literal["", "0", "10", "15", "20", "30", "50", "100", "300", "500"] = "",
        trde_prica_cnd: Literal[
            "", "0", "1", "3", "5", "10", "30", "50", "100", "300", "500", "1000", "3000", "5000"
        ] = "",
        base_dt: str = "",
        sort_tp: Literal["", "0", "2"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoSpecificDateRiseFallStock]:
        """미국주식 특정일자 상승/하락(주식/업종) (usa24120)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소구분. 0:전체,1:NYSE,2:AMEX,3:NASDAQ. Defaults to "".
            inds_cd (str, optional): 업종코드. 000:전체, usa10101 API 참고, stk_tp(종목구분) 1일 경우. Defaults to "".
            stk_tp (Literal["", "0", "1"], optional): 종목구분. 0:전체,1:주식. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목조건. 0:전체,1:증100%,2:증50%. Defaults to "".
            pric_cnd (Literal, optional): 가격조건. 0:전체,1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
            base_dt (str, optional): 기간. YYYYMMDD. Defaults to "".
            sort_tp (Literal["", "0", "2"], optional): 정렬기준 구분. 0:상승,2:하락. Defaults to "".
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
        body = {
            "stex_tp": stex_tp,
            "inds_cd": inds_cd,
            "stk_tp": stk_tp,
            "stk_cnd": stk_cnd,
            "pric_cnd": pric_cnd,
            "trde_qty_tp": trde_qty_tp,
            "trde_prica_cnd": trde_prica_cnd,
            "base_dt": base_dt,
            "sort_tp": sort_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching specific date rise fall stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoSpecificDateRiseFallStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_specific_date_rise_fall_etf(
        self,
        stex_tp: Literal["", "0", "1", "2", "3"] = "",
        etf_cat1: str = "",
        etf_cat2: str = "",
        stk_cnd: Literal["", "0", "1", "2"] = "",
        pric_cnd: Literal["", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] = "",
        trde_qty_tp: Literal["", "0", "10", "15", "20", "30", "50", "100", "300", "500"] = "",
        trde_prica_cnd: Literal[
            "", "0", "1", "3", "5", "10", "30", "50", "100", "300", "500", "1000", "3000", "5000"
        ] = "",
        base_dt: str = "",
        sort_tp: Literal["", "0", "2"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoSpecificDateRiseFallEtf]:
        """미국주식 특정일자 상승/하락(ETF) (usa24121)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소구분. 0:전체,1:NYSE,2:AMEX,3:NASDAQ. Defaults to "".
            etf_cat1 (str, optional): ETF카테고리코드1. ETF 대카테고리코드, usa10105 cate1 속성 참고. Defaults to "".
            etf_cat2 (str, optional): ETF카테고리코드2. ETF 중카테고리코드, usa10105 cate2 속성 참고. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목조건. 0:전체,1:증100%,2:증50%. Defaults to "".
            pric_cnd (Literal, optional): 가격조건. 0:전체,1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
            base_dt (str, optional): 기간. YYYYMMDD. Defaults to "".
            sort_tp (Literal["", "0", "2"], optional): 정렬기준 구분. 0:상승,2:하락. Defaults to "".
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
        body = {
            "stex_tp": stex_tp,
            "etf_cat1": etf_cat1,
            "etf_cat2": etf_cat2,
            "stk_cnd": stk_cnd,
            "pric_cnd": pric_cnd,
            "trde_qty_tp": trde_qty_tp,
            "trde_prica_cnd": trde_prica_cnd,
            "base_dt": base_dt,
            "sort_tp": sort_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching specific date rise fall etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoSpecificDateRiseFallEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_turnover_rate_top_stock(
        self,
        stex_tp: Literal["", "0", "1", "2", "3"] = "",
        inds_cd: str = "",
        trde_qty_tp: Literal["", "0", "10", "15", "20", "30", "50", "100", "300", "500"] = "",
        stk_tp: Literal["", "0", "1"] = "",
        stk_cnd: Literal["", "0", "1", "2"] = "",
        pric_cnd: Literal["", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] = "",
        trde_prica_cnd: Literal[
            "", "0", "1", "3", "5", "10", "30", "50", "100", "300", "500", "1000", "3000", "5000"
        ] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoTurnoverRateTopStock]:
        """미국주식 회전율 상위(주식/업종) (usa24150)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소구분. 0:전체,1:NYSE,2:NASDAQ,3:AMEX. Defaults to "".
            inds_cd (str, optional): 업종코드. 000:전체, usa10101 API 참고, stk_tp(종목구분) 1일 경우. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            stk_tp (Literal["", "0", "1"], optional): 종목구분. 0:전체,1:주식. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목조건. 0:전체,1:증100%,2:증50%. Defaults to "".
            pric_cnd (Literal, optional): 가격조건. 0:전체,1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
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
        body = {
            "stex_tp": stex_tp,
            "inds_cd": inds_cd,
            "trde_qty_tp": trde_qty_tp,
            "stk_tp": stk_tp,
            "stk_cnd": stk_cnd,
            "pric_cnd": pric_cnd,
            "trde_prica_cnd": trde_prica_cnd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching turnover rate top stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoTurnoverRateTopStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_turnover_rate_top_etf(
        self,
        stex_tp: Literal["", "0", "1", "2", "3"] = "",
        etf_cat1: str = "",
        etf_cat2: str = "",
        trde_qty_tp: Literal["", "0", "10", "15", "20", "30", "50", "100", "300", "500"] = "",
        stk_cnd: Literal["", "0", "1", "2"] = "",
        pric_cnd: Literal["", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] = "",
        trde_prica_cnd: Literal[
            "", "0", "1", "3", "5", "10", "30", "50", "100", "300", "500", "1000", "3000", "5000"
        ] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoTurnoverRateTopEtf]:
        """미국주식 회전율 상위(ETF) (usa24151)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소구분. 0:전체,1:NYSE,2:NASDAQ,3:AMEX. Defaults to "".
            etf_cat1 (str, optional): ETF카테고리코드1. ETF 대카테고리코드, usa10105 cate1 속성 참고. Defaults to "".
            etf_cat2 (str, optional): ETF카테고리코드2. ETF 중카테고리코드, usa10105 cate2 속성 참고. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목조건. 0:전체,1:증100%,2:증50%. Defaults to "".
            pric_cnd (Literal, optional): 가격조건. 0:전체,1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
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
        body = {
            "stex_tp": stex_tp,
            "etf_cat1": etf_cat1,
            "etf_cat2": etf_cat2,
            "trde_qty_tp": trde_qty_tp,
            "stk_cnd": stk_cnd,
            "pric_cnd": pric_cnd,
            "trde_prica_cnd": trde_prica_cnd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching turnover rate top etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoTurnoverRateTopEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_consecutive_rise_fall_rank_stock(
        self,
        stex_tp: Literal["", "0", "1", "2", "3"] = "",
        inds_cd: str = "",
        stk_tp: Literal["", "0", "1"] = "",
        trde_qty_tp: Literal["", "0", "10", "15", "20", "30", "50", "100", "300", "500"] = "",
        stk_cnd: Literal["", "0", "1", "2"] = "",
        pric_cnd: Literal["", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] = "",
        trde_prica_cnd: Literal[
            "", "0", "1", "3", "5", "10", "30", "50", "100", "300", "500", "1000", "3000", "5000"
        ] = "",
        sort_tp: Literal["", "0", "1", "2", "3", "4", "5"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoConsecutiveRiseFallRankStock]:
        """미국주식 연속상승/하락 순위(주식/업종) (usa24160)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소구분. 0:전체,1:NYSE,2:AMEX,3:NASDAQ. Defaults to "".
            inds_cd (str, optional): 업종코드. 000:전체, usa10101 API 참고, stk_tp(종목구분) 1일 경우. Defaults to "".
            stk_tp (Literal["", "0", "1"], optional): 종목구분. 0:전체,1:주식. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목조건. 0:전체,1:증100%,2:증50%. Defaults to "".
            pric_cnd (Literal, optional): 가격조건. 0:전체,1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
            sort_tp (Literal, optional): 정렬기준. 0:연속일수상승,1:연속일수보합,2:연속일수하락,3:기준일대비상승,4:기준일대비보합,5:기준일대비 하락. Defaults to "".
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
        body = {
            "stex_tp": stex_tp,
            "inds_cd": inds_cd,
            "stk_tp": stk_tp,
            "trde_qty_tp": trde_qty_tp,
            "stk_cnd": stk_cnd,
            "pric_cnd": pric_cnd,
            "trde_prica_cnd": trde_prica_cnd,
            "sort_tp": sort_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching consecutive rise fall rank stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoConsecutiveRiseFallRankStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_consecutive_rise_fall_rank_etf(
        self,
        stex_tp: Literal["", "0", "1", "2", "3"] = "",
        etf_cat1: str = "",
        etf_cat2: str = "",
        trde_qty_tp: Literal["", "0", "10", "15", "20", "30", "50", "100", "300", "500"] = "",
        stk_cnd: Literal["", "0", "1", "2"] = "",
        pric_cnd: Literal["", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] = "",
        trde_prica_cnd: Literal[
            "", "0", "1", "3", "5", "10", "30", "50", "100", "300", "500", "1000", "3000", "5000"
        ] = "",
        sort_tp: Literal["", "0", "1", "2", "3", "4", "5"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoConsecutiveRiseFallRankEtf]:
        """미국주식 연속상승/하락 순위(ETF) (usa24161)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소구분. 0:전체,1:NYSE,2:AMEX,3:NASDAQ. Defaults to "".
            etf_cat1 (str, optional): ETF카테고리코드1. ETF 대카테고리코드, usa10105 cate1 속성 참고. Defaults to "".
            etf_cat2 (str, optional): ETF카테고리코드2. ETF 중카테고리코드, usa10105 cate2 속성 참고. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목조건. 0:전체,1:증100%,2:증50%. Defaults to "".
            pric_cnd (Literal, optional): 가격조건. 0:전체,1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
            sort_tp (Literal, optional): 정렬기준. 0:연속일수상승,1:연속일수보합,2:연속일수하락,3:기준일대비상승,4:기준일대비보합,5:기준일대비 하락. Defaults to "".
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
        body = {
            "stex_tp": stex_tp,
            "etf_cat1": etf_cat1,
            "etf_cat2": etf_cat2,
            "trde_qty_tp": trde_qty_tp,
            "stk_cnd": stk_cnd,
            "pric_cnd": pric_cnd,
            "trde_prica_cnd": trde_prica_cnd,
            "sort_tp": sort_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching consecutive rise fall rank etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoConsecutiveRiseFallRankEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_consecutive_rise_fall_rank_watchlist(
        self,
        stex_tp: Literal["", "0", "1", "2", "3"] = "",
        stk_cd: list[dict[str, str]] | None = None,
        trde_qty_tp: Literal["", "0", "10", "15", "20", "30", "50", "100", "300", "500"] = "",
        stk_cnd: Literal["", "0", "1", "2"] = "",
        pric_cnd: Literal["", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] = "",
        trde_prica_cnd: Literal[
            "", "0", "1", "3", "5", "10", "30", "50", "100", "300", "500", "1000", "3000", "5000"
        ] = "",
        sort_tp: Literal["", "0", "1", "2", "3", "4", "5"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoConsecutiveRiseFallRankWatchlist]:
        """미국주식 연속상승/하락 순위(관심종목) (usa24162)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소구분. 0:전체,1:NYSE,2:AMEX,3:NASDAQ. Defaults to "".
            stk_cd (list[dict[str, str]] | None, optional): 관심종목. [{'stex_tp':'거래소구분','stk_cd':'종목코드'},...]. Defaults to None.
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목조건. 0:전체,1:증100%,2:증50%. Defaults to "".
            pric_cnd (Literal, optional): 가격조건. 0:전체,1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
            sort_tp (Literal, optional): 정렬기준. 0:연속일수상승,1:연속일수보합,2:연속일수하락,3:기준일대비상승,4:기준일대비보합,5:기준일대비 하락. Defaults to "".
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
        body = {
            "stex_tp": stex_tp,
            "stk_cd": stk_cd if stk_cd is not None else [],
            "trde_qty_tp": trde_qty_tp,
            "stk_cnd": stk_cnd,
            "pric_cnd": pric_cnd,
            "trde_prica_cnd": trde_prica_cnd,
            "sort_tp": sort_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching consecutive rise fall rank watchlist: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoConsecutiveRiseFallRankWatchlist.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_quote_remaining_volume_top_stock(
        self,
        stex_tp: Literal["", "0", "1", "2", "3"] = "",
        inds_cd: str = "",
        stk_tp: Literal["", "0", "1"] = "",
        sort_tp: Literal["", "1", "2", "3", "4"] = "",
        stk_cnd: Literal["", "0", "1", "2"] = "",
        trde_qty_tp: Literal["", "0", "10", "15", "20", "30", "50", "100", "300", "500"] = "",
        pric_cnd: Literal["", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] = "",
        trde_prica_cnd: Literal[
            "", "0", "1", "3", "5", "10", "30", "50", "100", "300", "500", "1000", "3000", "5000"
        ] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoQuoteRemainingVolumeTopStock]:
        """미국주식 호가잔량상위(주식/업종) (usa24200)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소구분. 0:전체,1:NYSE,2:NASDAQ,3:AMEX. Defaults to "".
            inds_cd (str, optional): 업종코드. 000:전체, usa10101 API 참고, stk_tp(종목구분) 1일 경우. Defaults to "".
            stk_tp (Literal["", "0", "1"], optional): 종목구분. 0:전체,1:주식. Defaults to "".
            sort_tp (Literal["", "1", "2", "3", "4"], optional): 정렬기준. 1:순매수잔량순,2:순매도잔량순,3:순매수비율순,4:순매도비율순. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목조건. 0:전체,1:증100%,2:증50%. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            pric_cnd (Literal, optional): 가격조건. 0:전체,1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
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
        body = {
            "stex_tp": stex_tp,
            "inds_cd": inds_cd,
            "stk_tp": stk_tp,
            "sort_tp": sort_tp,
            "stk_cnd": stk_cnd,
            "trde_qty_tp": trde_qty_tp,
            "pric_cnd": pric_cnd,
            "trde_prica_cnd": trde_prica_cnd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching quote remaining volume top stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoQuoteRemainingVolumeTopStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_quote_remaining_volume_top_etf(
        self,
        stex_tp: Literal["", "0", "1", "2", "3"] = "",
        etf_cat1: str = "",
        etf_cat2: str = "",
        sort_tp: Literal["", "1", "2", "3", "4"] = "",
        stk_cnd: Literal["", "0", "1", "2"] = "",
        trde_qty_tp: Literal["", "0", "10", "15", "20", "30", "50", "100", "300", "500"] = "",
        pric_cnd: Literal["", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] = "",
        trde_prica_cnd: Literal[
            "", "0", "1", "3", "5", "10", "30", "50", "100", "300", "500", "1000", "3000", "5000"
        ] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoQuoteRemainingVolumeTopEtf]:
        """미국주식 호가잔량상위(ETF) (usa24201)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소구분. 0:전체,1:NYSE,2:NASDAQ,3:AMEX. Defaults to "".
            etf_cat1 (str, optional): ETF카테고리코드1. ETF 대카테고리코드, usa10105 cate1 속성 참고. Defaults to "".
            etf_cat2 (str, optional): ETF카테고리코드2. ETF 중카테고리코드, usa10105 cate2 속성 참고. Defaults to "".
            sort_tp (Literal["", "1", "2", "3", "4"], optional): 정렬기준. 1:순매수잔량순,2:순매도잔량순,3:순매수비율순,4:순매도비율순. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목조건. 0:전체,1:증100%,2:증50%. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            pric_cnd (Literal, optional): 가격조건. 0:전체,1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
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
        body = {
            "stex_tp": stex_tp,
            "etf_cat1": etf_cat1,
            "etf_cat2": etf_cat2,
            "sort_tp": sort_tp,
            "stk_cnd": stk_cnd,
            "trde_qty_tp": trde_qty_tp,
            "pric_cnd": pric_cnd,
            "trde_prica_cnd": trde_prica_cnd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching quote remaining volume top etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoQuoteRemainingVolumeTopEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_daytime_trading_disparity_top_stock(
        self,
        stex_tp: Literal["", "0", "1", "2", "3"] = "",
        inds_cd: str = "",
        inds_cls_tp: Literal["", "0", "1", "2", "3"] = "",
        stk_tp: Literal["", "0", "1"] = "",
        stk_cnd: Literal["", "0", "1", "2"] = "",
        pric_cnd: Literal["", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] = "",
        trde_qty_tp: Literal["", "0", "10", "15", "20", "30", "50", "100", "300", "500"] = "",
        trde_prica_cnd: Literal[
            "", "0", "1", "3", "5", "10", "30", "50", "100", "300", "500", "1000", "3000", "5000"
        ] = "",
        sort_tp: Literal["", "0", "1", "2", "3", "4"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoDaytimeTradingDisparityTopStock]:
        """미국주식 주간거래 괴리율 상위(주식/업종) (usa24290)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소구분. 0:전체,1:NYSE,2:AMEX,3:NASDAQ. Defaults to "".
            inds_cd (str, optional): 업종코드. 000:전체, usa10101 API 참고, stk_tp(종목구분) 1일 경우. Defaults to "".
            inds_cls_tp (Literal["", "0", "1", "2", "3"], optional): 해외주식업종분류구분. stk_tp 0일 경우, 0:전체,1:다우30,2:나스닥100,3:S&P500. Defaults to "".
            stk_tp (Literal["", "0", "1"], optional): 종목구분. 0:전체,1:주식. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목조건. 0:전체,1:증100%,2:증50%. Defaults to "".
            pric_cnd (Literal, optional): 가격조건. 0:전체,1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
            sort_tp (Literal["", "0", "1", "2", "3", "4"], optional): 정렬기준 구분. 0:상승률,1:상승폭,2:보합,3:하락율,4:하락폭. Defaults to "".
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
        body = {
            "stex_tp": stex_tp,
            "inds_cd": inds_cd,
            "inds_cls_tp": inds_cls_tp,
            "stk_tp": stk_tp,
            "stk_cnd": stk_cnd,
            "pric_cnd": pric_cnd,
            "trde_qty_tp": trde_qty_tp,
            "trde_prica_cnd": trde_prica_cnd,
            "sort_tp": sort_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching daytime trading disparity top stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoDaytimeTradingDisparityTopStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_daytime_trading_disparity_top_etf(
        self,
        stex_tp: Literal["", "0", "1", "2", "3"] = "",
        etf_cat1: str = "",
        etf_cat2: str = "",
        stk_cnd: Literal["", "0", "1", "2"] = "",
        pric_cnd: Literal["", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] = "",
        trde_qty_tp: Literal["", "0", "10", "15", "20", "30", "50", "100", "300", "500"] = "",
        trde_prica_cnd: Literal[
            "", "0", "1", "3", "5", "10", "30", "50", "100", "300", "500", "1000", "3000", "5000"
        ] = "",
        sort_tp: Literal["", "0", "1", "2", "3", "4"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasRankInfoDaytimeTradingDisparityTopEtf]:
        """미국주식 주간거래 괴리율 상위(ETF) (usa24291)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소구분. 0:전체,1:NYSE,2:AMEX,3:NASDAQ. Defaults to "".
            etf_cat1 (str, optional): ETF카테고리코드1. ETF 대카테고리코드, usa10105 cate1 속성 참고. Defaults to "".
            etf_cat2 (str, optional): ETF카테고리코드2. ETF 중카테고리코드, usa10105 cate2 속성 참고. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목조건. 0:전체,1:증100%,2:증50%. Defaults to "".
            pric_cnd (Literal, optional): 가격조건. 0:전체,1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
            sort_tp (Literal["", "0", "1", "2", "3", "4"], optional): 정렬기준 구분. 0:상승률,1:상승폭,2:보합,3:하락율,4:하락폭. Defaults to "".
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
        body = {
            "stex_tp": stex_tp,
            "etf_cat1": etf_cat1,
            "etf_cat2": etf_cat2,
            "stk_cnd": stk_cnd,
            "pric_cnd": pric_cnd,
            "trde_qty_tp": trde_qty_tp,
            "trde_prica_cnd": trde_prica_cnd,
            "sort_tp": sort_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching daytime trading disparity top etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasRankInfoDaytimeTradingDisparityTopEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)
