from cluefin_openapi.kis._client import Client
from cluefin_openapi.kis._domestic_ranking_analysis_types import (
    HtsInquiryTop20,
    StockAfterHoursFluctuationRank,
    StockAfterHoursVolumeRank,
    StockCreditBalanceTop,
    StockDisparityIndexRank,
    StockDividendYieldTop,
    StockExecutionStrengthTop,
    StockExpectedExecutionRiseDeclineTop,
    StockFinanceRatioRank,
    StockFluctuationRank,
    StockHogaQuantityRank,
    StockLargeExecutionCountTop,
    StockMarketCapTop,
    StockMarketPriceRank,
    StockNewHighLowApproachingTop,
    StockPreferredStockRatioTop,
    StockProfitabilityIndicatorRank,
    StockProprietaryTradingTop,
    StockShortSellingTop,
    StockTimeHogaRank,
    StockWatchlistRegistrationTop,
    TradingVolumeRank,
)
from cluefin_openapi.kis._model import KisHttpHeader, KisHttpResponse


class DomesticRankingAnalysis:
    """국내주식 순위분석"""

    def __init__(self, client: Client):
        self.client = client

    def get_trading_volume_rank(
        self,
        fid_cond_mrkt_div_code: str,
        fid_cond_scr_div_code: str,
        fid_input_iscd: str,
        fid_div_cls_code: str,
        fid_blng_cls_code: str,
        fid_trgt_cls_code: str,
        fid_trgt_exls_cls_code: str,
        fid_input_price_1: str,
        fid_input_price_2: str,
        fid_vol_cnt: str,
        fid_input_date_1: str,
    ) -> KisHttpResponse[TradingVolumeRank]:
        """
        거래량순위

        Args:
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드 (J:KRX, NX:NXT)
            fid_cond_scr_div_code (str): 조건 화면 분류 코드 (20171)
            fid_input_iscd (str): 입력 종목코드 (0000:전체, 기타:업종코드)
            fid_div_cls_code (str): 분류 구분 코드 (0:전체, 1:보통주, 2:우선주)
            fid_blng_cls_code (str): 소속 구분 코드 (0:평균거래량, 1:거래증가율, 2:평균거래회전율, 3:거래금액순, 4:평균거래금액회전율)
            fid_trgt_cls_code (str): 대상 구분 코드 (1 or 0 9자리, 예: "111111111")
            fid_trgt_exls_cls_code (str): 대상 제외 구분 코드 (1 or 0 10자리, 예: "0000000000")
            fid_input_price_1 (str): 입력 가격1 (가격~, 전체 조회시 공란)
            fid_input_price_2 (str): 입력 가격2 (~가격, 전체 조회시 공란)
            fid_vol_cnt (str): 거래량 수 (거래량~, 전체 조회시 공란)
            fid_input_date_1 (str): 입력 날짜1 (공란 입력)

        Returns:
            TradingVolumeRank: 거래량순위 응답 객체
        """
        headers = {
            "tr_id": "FHPST01710000",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_COND_SCR_DIV_CODE": fid_cond_scr_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_DIV_CLS_CODE": fid_div_cls_code,
            "FID_BLNG_CLS_CODE": fid_blng_cls_code,
            "FID_TRGT_CLS_CODE": fid_trgt_cls_code,
            "FID_TRGT_EXLS_CLS_CODE": fid_trgt_exls_cls_code,
            "FID_INPUT_PRICE_1": fid_input_price_1,
            "FID_INPUT_PRICE_2": fid_input_price_2,
            "FID_VOL_CNT": fid_vol_cnt,
            "FID_INPUT_DATE_1": fid_input_date_1,
        }
        response = self.client._get("/uapi/domestic-stock/v1/quotations/volume-rank", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching trading volume rank: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = TradingVolumeRank.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_stock_fluctuation_rank(
        self,
        fid_rsfl_rate2: str,
        fid_cond_mrkt_div_code: str,
        fid_cond_scr_div_code: str,
        fid_input_iscd: str,
        fid_rank_sort_cls_code: str,
        fid_input_cnt_1: str,
        fid_prc_cls_code: str,
        fid_input_price_1: str,
        fid_input_price_2: str,
        fid_vol_cnt: str,
        fid_trgt_cls_code: str,
        fid_trgt_exls_cls_code: str,
        fid_div_cls_code: str,
        fid_rsfl_rate1: str,
    ) -> KisHttpResponse[StockFluctuationRank]:
        """
        국내주식 등락률 순위

        Args:
            fid_rsfl_rate2 (str): 등락 비율2 (공백 입력시 전체, ~비율)
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드 (J:KRX, NX:NXT)
            fid_cond_scr_div_code (str): 조건 화면 분류 코드 (20170)
            fid_input_iscd (str): 입력 종목코드 (0000:전체, 0001:코스피, 1001:코스닥, 2001:코스피200)
            fid_rank_sort_cls_code (str): 순위 정렬 구분 코드 (0:상승율순, 1:하락율순, 2:시가대비상승율, 3:시가대비하락율, 4:변동율)
            fid_input_cnt_1 (str): 입력 수1 (0:전체, 누적일수 입력)
            fid_prc_cls_code (str): 가격 구분 코드 (상승율순: 0:저가대비/1:종가대비, 하락율순: 0:고가대비/1:종가대비, 기타: 0:전체)
            fid_input_price_1 (str): 입력 가격1 (공백 입력시 전체, 가격~)
            fid_input_price_2 (str): 입력 가격2 (공백 입력시 전체, ~가격)
            fid_vol_cnt (str): 거래량 수 (공백 입력시 전체, 거래량~)
            fid_trgt_cls_code (str): 대상 구분 코드 (0:전체)
            fid_trgt_exls_cls_code (str): 대상 제외 구분 코드 (0:전체)
            fid_div_cls_code (str): 분류 구분 코드 (0:전체)
            fid_rsfl_rate1 (str): 등락 비율1 (공백 입력시 전체, 비율~)

        Returns:
            StockFluctuationRank: 국내주식 등락률 순위 응답 객체
        """
        headers = {
            "tr_id": "FHPST01700000",
        }
        params = {
            "fid_rsfl_rate2": fid_rsfl_rate2,
            "fid_cond_mrkt_div_code": fid_cond_mrkt_div_code,
            "fid_cond_scr_div_code": fid_cond_scr_div_code,
            "fid_input_iscd": fid_input_iscd,
            "fid_rank_sort_cls_code": fid_rank_sort_cls_code,
            "fid_input_cnt_1": fid_input_cnt_1,
            "fid_prc_cls_code": fid_prc_cls_code,
            "fid_input_price_1": fid_input_price_1,
            "fid_input_price_2": fid_input_price_2,
            "fid_vol_cnt": fid_vol_cnt,
            "fid_trgt_cls_code": fid_trgt_cls_code,
            "fid_trgt_exls_cls_code": fid_trgt_exls_cls_code,
            "fid_div_cls_code": fid_div_cls_code,
            "fid_rsfl_rate1": fid_rsfl_rate1,
        }
        response = self.client._get("/uapi/domestic-stock/v1/ranking/fluctuation", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock fluctuation rank: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockFluctuationRank.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_stock_hoga_quantity_rank(
        self,
        fid_vol_cnt: str,
        fid_cond_mrkt_div_code: str,
        fid_cond_scr_div_code: str,
        fid_input_iscd: str,
        fid_rank_sort_cls_code: str,
        fid_div_cls_code: str,
        fid_trgt_cls_code: str,
        fid_trgt_exls_cls_code: str,
        fid_input_price_1: str,
        fid_input_price_2: str,
    ) -> KisHttpResponse[StockHogaQuantityRank]:
        """
        국내주식 호가잔량 순위

        Args:
            fid_vol_cnt (str): 거래량 수 (입력값 없을때 전체, 거래량~)
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드 (J:KRX, NX:NXT)
            fid_cond_scr_div_code (str): 조건 화면 분류 코드 (20172)
            fid_input_iscd (str): 입력 종목코드 (0000:전체, 0001:코스피, 1001:코스닥, 2001:코스피200)
            fid_rank_sort_cls_code (str): 순위 정렬 구분 코드 (0:순매수잔량순, 1:순매도잔량순, 2:매수비율순, 3:매도비율순)
            fid_div_cls_code (str): 분류 구분 코드 (0:전체)
            fid_trgt_cls_code (str): 대상 구분 코드 (0:전체)
            fid_trgt_exls_cls_code (str): 대상 제외 구분 코드 (0:전체)
            fid_input_price_1 (str): 입력 가격1 (입력값 없을때 전체, 가격~)
            fid_input_price_2 (str): 입력 가격2 (입력값 없을때 전체, ~가격)

        Returns:
            StockHogaQuantityRank: 국내주식 호가잔량 순위 응답 객체
        """
        headers = {
            "tr_id": "FHPST01720000",
        }
        params = {
            "fid_vol_cnt": fid_vol_cnt,
            "fid_cond_mrkt_div_code": fid_cond_mrkt_div_code,
            "fid_cond_scr_div_code": fid_cond_scr_div_code,
            "fid_input_iscd": fid_input_iscd,
            "fid_rank_sort_cls_code": fid_rank_sort_cls_code,
            "fid_div_cls_code": fid_div_cls_code,
            "fid_trgt_cls_code": fid_trgt_cls_code,
            "fid_trgt_exls_cls_code": fid_trgt_exls_cls_code,
            "fid_input_price_1": fid_input_price_1,
            "fid_input_price_2": fid_input_price_2,
        }
        response = self.client._get("/uapi/domestic-stock/v1/ranking/quote-balance", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock hoga quantity rank: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockHogaQuantityRank.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_stock_profitability_indicator_rank(
        self,
        fid_cond_mrkt_div_code: str,
        fid_trgt_cls_code: str,
        fid_cond_scr_div_code: str,
        fid_input_iscd: str,
        fid_div_cls_code: str,
        fid_input_price_1: str,
        fid_input_price_2: str,
        fid_vol_cnt: str,
        fid_input_option_1: str,
        fid_input_option_2: str,
        fid_rank_sort_cls_code: str,
        fid_blng_cls_code: str,
        fid_trgt_exls_cls_code: str,
    ) -> KisHttpResponse[StockProfitabilityIndicatorRank]:
        """
        국내주식 수익자산지표 순위

        Args:
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드 (J:KRX, NX:NXT)
            fid_trgt_cls_code (str): 대상 구분 코드 (0:전체)
            fid_cond_scr_div_code (str): 조건 화면 분류 코드 (20173)
            fid_input_iscd (str): 입력 종목코드 (0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200)
            fid_div_cls_code (str): 분류 구분 코드 (0:전체)
            fid_input_price_1 (str): 입력 가격1 (입력값 없을때 전체, 가격~)
            fid_input_price_2 (str): 입력 가격2 (입력값 없을때 전체, ~가격)
            fid_vol_cnt (str): 거래량 수 (입력값 없을때 전체, 거래량~)
            fid_input_option_1 (str): 입력 옵션1 (회계연도, 예: 2023)
            fid_input_option_2 (str): 입력 옵션2 (0:1/4분기, 1:반기, 2:3/4분기, 3:결산)
            fid_rank_sort_cls_code (str): 순위 정렬 구분 코드 (0:매출이익, 1:영업이익, 2:경상이익, 3:당기순이익, 4:자산총계, 5:부채총계, 6:자본총계)
            fid_blng_cls_code (str): 소속 구분 코드 (0:전체)
            fid_trgt_exls_cls_code (str): 대상 제외 구분 코드 (0:전체)

        Returns:
            StockProfitabilityIndicatorRank: 국내주식 수익자산지표 순위 응답 객체
        """
        headers = {
            "tr_id": "FHPST01730000",
        }
        params = {
            "fid_cond_mrkt_div_code": fid_cond_mrkt_div_code,
            "fid_trgt_cls_code": fid_trgt_cls_code,
            "fid_cond_scr_div_code": fid_cond_scr_div_code,
            "fid_input_iscd": fid_input_iscd,
            "fid_div_cls_code": fid_div_cls_code,
            "fid_input_price_1": fid_input_price_1,
            "fid_input_price_2": fid_input_price_2,
            "fid_vol_cnt": fid_vol_cnt,
            "fid_input_option_1": fid_input_option_1,
            "fid_input_option_2": fid_input_option_2,
            "fid_rank_sort_cls_code": fid_rank_sort_cls_code,
            "fid_blng_cls_code": fid_blng_cls_code,
            "fid_trgt_exls_cls_code": fid_trgt_exls_cls_code,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/ranking/profit-asset-index", headers=headers, params=params
        )
        if response.status_code != 200:
            raise Exception(f"Error fetching stock profitability indicator rank: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockProfitabilityIndicatorRank.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_stock_market_cap_top(
        self,
        fid_input_price_2: str,
        fid_cond_mrkt_div_code: str,
        fid_cond_scr_div_code: str,
        fid_div_cls_code: str,
        fid_input_iscd: str,
        fid_trgt_cls_code: str,
        fid_trgt_exls_cls_code: str,
        fid_input_price_1: str,
        fid_vol_cnt: str,
    ) -> KisHttpResponse[StockMarketCapTop]:
        """
        국내주식 시가총액 상위

        Args:
            fid_input_price_2 (str): 입력 가격2 (입력값 없을때 전체, ~가격)
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드 (J:KRX, NX:NXT)
            fid_cond_scr_div_code (str): 조건 화면 분류 코드 (20174)
            fid_div_cls_code (str): 분류 구분 코드 (0:전체, 1:보통주, 2:우선주)
            fid_input_iscd (str): 입력 종목코드 (0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200)
            fid_trgt_cls_code (str): 대상 구분 코드 (0:전체)
            fid_trgt_exls_cls_code (str): 대상 제외 구분 코드 (0:전체)
            fid_input_price_1 (str): 입력 가격1 (입력값 없을때 전체, 가격~)
            fid_vol_cnt (str): 거래량 수 (입력값 없을때 전체, 거래량~)

        Returns:
            StockMarketCapTop: 국내주식 시가총액 상위 응답 객체
        """
        headers = {
            "tr_id": "FHPST01740000",
        }
        params = {
            "fid_input_price_2": fid_input_price_2,
            "fid_cond_mrkt_div_code": fid_cond_mrkt_div_code,
            "fid_cond_scr_div_code": fid_cond_scr_div_code,
            "fid_div_cls_code": fid_div_cls_code,
            "fid_input_iscd": fid_input_iscd,
            "fid_trgt_cls_code": fid_trgt_cls_code,
            "fid_trgt_exls_cls_code": fid_trgt_exls_cls_code,
            "fid_input_price_1": fid_input_price_1,
            "fid_vol_cnt": fid_vol_cnt,
        }
        response = self.client._get("/uapi/domestic-stock/v1/ranking/market-cap", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock market cap top: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockMarketCapTop.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_stock_finance_ratio_rank(
        self,
        fid_trgt_cls_code: str,
        fid_cond_mrkt_div_code: str,
        fid_cond_scr_div_code: str,
        fid_input_iscd: str,
        fid_div_cls_code: str,
        fid_input_price_1: str,
        fid_input_price_2: str,
        fid_vol_cnt: str,
        fid_input_option_1: str,
        fid_input_option_2: str,
        fid_rank_sort_cls_code: str,
        fid_blng_cls_code: str,
        fid_trgt_exls_cls_code: str,
    ) -> KisHttpResponse[StockFinanceRatioRank]:
        """
        국내주식 재무비율 순위

        Args:
            fid_trgt_cls_code (str): 대상 구분 코드 (0:전체)
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드 (J:KRX, NX:NXT)
            fid_cond_scr_div_code (str): 조건 화면 분류 코드 (20175)
            fid_input_iscd (str): 입력 종목코드 (0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200)
            fid_div_cls_code (str): 분류 구분 코드 (0:전체)
            fid_input_price_1 (str): 입력 가격1 (입력값 없을때 전체, 가격~)
            fid_input_price_2 (str): 입력 가격2 (입력값 없을때 전체, ~가격)
            fid_vol_cnt (str): 거래량 수 (입력값 없을때 전체, 거래량~)
            fid_input_option_1 (str): 입력 옵션1 (회계년도, 예: 2023)
            fid_input_option_2 (str): 입력 옵션2 (0:1/4분기, 1:반기, 2:3/4분기, 3:결산)
            fid_rank_sort_cls_code (str): 순위 정렬 구분 코드 (7:수익성분석, 11:안정성분석, 15:성장성분석, 20:활동성분석)
            fid_blng_cls_code (str): 소속 구분 코드 (0)
            fid_trgt_exls_cls_code (str): 대상 제외 구분 코드 (0:전체)

        Returns:
            StockFinanceRatioRank: 국내주식 재무비율 순위 응답 객체
        """
        headers = {
            "tr_id": "FHPST01750000",
        }
        params = {
            "fid_trgt_cls_code": fid_trgt_cls_code,
            "fid_cond_mrkt_div_code": fid_cond_mrkt_div_code,
            "fid_cond_scr_div_code": fid_cond_scr_div_code,
            "fid_input_iscd": fid_input_iscd,
            "fid_div_cls_code": fid_div_cls_code,
            "fid_input_price_1": fid_input_price_1,
            "fid_input_price_2": fid_input_price_2,
            "fid_vol_cnt": fid_vol_cnt,
            "fid_input_option_1": fid_input_option_1,
            "fid_input_option_2": fid_input_option_2,
            "fid_rank_sort_cls_code": fid_rank_sort_cls_code,
            "fid_blng_cls_code": fid_blng_cls_code,
            "fid_trgt_exls_cls_code": fid_trgt_exls_cls_code,
        }
        response = self.client._get("/uapi/domestic-stock/v1/ranking/finance-ratio", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock finance ratio rank: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockFinanceRatioRank.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_stock_time_hoga_rank(
        self,
        fid_input_price_1: str,
        fid_cond_mrkt_div_code: str,
        fid_cond_scr_div_code: str,
        fid_rank_sort_cls_code: str,
        fid_div_cls_code: str,
        fid_input_iscd: str,
        fid_trgt_exls_cls_code: str,
        fid_trgt_cls_code: str,
        fid_vol_cnt: str,
        fid_input_price_2: str,
    ) -> KisHttpResponse[StockTimeHogaRank]:
        """
        국내주식 시간외잔량 순위

        Args:
            fid_input_price_1 (str): 입력 가격1 (입력값 없을때 전체, 가격~)
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드 (주식 J)
            fid_cond_scr_div_code (str): 조건 화면 분류 코드 (20176)
            fid_rank_sort_cls_code (str): 순위 정렬 구분 코드 (1:장전시간외, 2:장후시간외, 3:매도잔량, 4:매수잔량)
            fid_div_cls_code (str): 분류 구분 코드 (0:전체)
            fid_input_iscd (str): 입력 종목코드 (0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200)
            fid_trgt_exls_cls_code (str): 대상 제외 구분 코드 (0:전체)
            fid_trgt_cls_code (str): 대상 구분 코드 (0:전체)
            fid_vol_cnt (str): 거래량 수 (입력값 없을때 전체, 거래량~)
            fid_input_price_2 (str): 입력 가격2 (입력값 없을때 전체, ~가격)

        Returns:
            StockTimeHogaRank: 국내주식 시간외잔량 순위 응답 객체
        """
        headers = {
            "tr_id": "FHPST01760000",
        }
        params = {
            "fid_input_price_1": fid_input_price_1,
            "fid_cond_mrkt_div_code": fid_cond_mrkt_div_code,
            "fid_cond_scr_div_code": fid_cond_scr_div_code,
            "fid_rank_sort_cls_code": fid_rank_sort_cls_code,
            "fid_div_cls_code": fid_div_cls_code,
            "fid_input_iscd": fid_input_iscd,
            "fid_trgt_exls_cls_code": fid_trgt_exls_cls_code,
            "fid_trgt_cls_code": fid_trgt_cls_code,
            "fid_vol_cnt": fid_vol_cnt,
            "fid_input_price_2": fid_input_price_2,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/ranking/after-hour-balance", headers=headers, params=params
        )
        if response.status_code != 200:
            raise Exception(f"Error fetching stock time hoga rank: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockTimeHogaRank.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_stock_preferred_stock_ratio_top(
        self,
        fid_vol_cnt: str,
        fid_cond_mrkt_div_code: str,
        fid_cond_scr_div_code: str,
        fid_div_cls_code: str,
        fid_input_iscd: str,
        fid_trgt_cls_code: str,
        fid_trgt_exls_cls_code: str,
        fid_input_price_1: str,
        fid_input_price_2: str,
    ) -> KisHttpResponse[StockPreferredStockRatioTop]:
        """
        국내주식 우선주/괴리율 상위

        Args:
            fid_vol_cnt (str): 거래량 수 (입력값 없을때 전체, 거래량~)
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드 (J:KRX, NX:NXT)
            fid_cond_scr_div_code (str): 조건 화면 분류 코드 (20177)
            fid_div_cls_code (str): 분류 구분 코드 (0:전체)
            fid_input_iscd (str): 입력 종목코드 (0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200)
            fid_trgt_cls_code (str): 대상 구분 코드 (0:전체)
            fid_trgt_exls_cls_code (str): 대상 제외 구분 코드 (0:전체)
            fid_input_price_1 (str): 입력 가격1 (입력값 없을때 전체, 가격~)
            fid_input_price_2 (str): 입력 가격2 (입력값 없을때 전체, ~가격)

        Returns:
            StockPreferredStockRatioTop: 국내주식 우선주/리리율 상위 응답 객체
        """
        headers = {
            "tr_id": "FHPST01770000",
        }
        params = {
            "fid_vol_cnt": fid_vol_cnt,
            "fid_cond_mrkt_div_code": fid_cond_mrkt_div_code,
            "fid_cond_scr_div_code": fid_cond_scr_div_code,
            "fid_div_cls_code": fid_div_cls_code,
            "fid_input_iscd": fid_input_iscd,
            "fid_trgt_cls_code": fid_trgt_cls_code,
            "fid_trgt_exls_cls_code": fid_trgt_exls_cls_code,
            "fid_input_price_1": fid_input_price_1,
            "fid_input_price_2": fid_input_price_2,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/ranking/prefer-disparate-ratio", headers=headers, params=params
        )
        if response.status_code != 200:
            raise Exception(f"Error fetching stock preferred stock ratio top: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockPreferredStockRatioTop.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_stock_disparity_index_rank(
        self,
        fid_input_price_2: str,
        fid_cond_mrkt_div_code: str,
        fid_cond_scr_div_code: str,
        fid_div_cls_code: str,
        fid_rank_sort_cls_code: str,
        fid_hour_cls_code: str,
        fid_input_iscd: str,
        fid_trgt_cls_code: str,
        fid_trgt_exls_cls_code: str,
        fid_input_price_1: str,
        fid_vol_cnt: str,
    ) -> KisHttpResponse[StockDisparityIndexRank]:
        """
        국내주식 이격도 순위

        Args:
            fid_input_price_2 (str): 입력 가격2 (입력값 없을때 전체, ~가격)
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드 (J:KRX, NX:NXT)
            fid_cond_scr_div_code (str): 조건 화면 분류 코드 (20178)
            fid_div_cls_code (str): 분류 구분 코드 (0:전체, 1:관리종목, 2:투자주의, 3:투자경고, 4:투자위험예고, 5:투자위험, 6:보통주, 7:우선주)
            fid_rank_sort_cls_code (str): 순위 정렬 구분 코드 (0:이격도상위순, 1:이격도하위순)
            fid_hour_cls_code (str): 시간 구분 코드 (5:이격도5, 10:이격도10, 20:이격도20, 60:이격도60, 120:이격도120)
            fid_input_iscd (str): 입력 종목코드 (0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200)
            fid_trgt_cls_code (str): 대상 구분 코드 (0:전체)
            fid_trgt_exls_cls_code (str): 대상 제외 구분 코드 (0:전체)
            fid_input_price_1 (str): 입력 가격1 (입력값 없을때 전체, 가격~)
            fid_vol_cnt (str): 거래량 수 (입력값 없을때 전체, 거래량~)

        Returns:
            StockDisparityIndexRank: 국내주식 이격도 순위 응답 객체
        """
        headers = {
            "tr_id": "FHPST01780000",
        }
        params = {
            "fid_input_price_2": fid_input_price_2,
            "fid_cond_mrkt_div_code": fid_cond_mrkt_div_code,
            "fid_cond_scr_div_code": fid_cond_scr_div_code,
            "fid_div_cls_code": fid_div_cls_code,
            "fid_rank_sort_cls_code": fid_rank_sort_cls_code,
            "fid_hour_cls_code": fid_hour_cls_code,
            "fid_input_iscd": fid_input_iscd,
            "fid_trgt_cls_code": fid_trgt_cls_code,
            "fid_trgt_exls_cls_code": fid_trgt_exls_cls_code,
            "fid_input_price_1": fid_input_price_1,
            "fid_vol_cnt": fid_vol_cnt,
        }
        response = self.client._get("/uapi/domestic-stock/v1/ranking/disparity", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock disparity index rank: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockDisparityIndexRank.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_stock_market_price_rank(
        self,
        fid_trgt_cls_code: str,
        fid_cond_mrkt_div_code: str,
        fid_cond_scr_div_code: str,
        fid_input_iscd: str,
        fid_div_cls_code: str,
        fid_input_price_1: str,
        fid_input_price_2: str,
        fid_vol_cnt: str,
        fid_input_option_1: str,
        fid_input_option_2: str,
        fid_rank_sort_cls_code: str,
        fid_blng_cls_code: str,
        fid_trgt_exls_cls_code: str,
    ) -> KisHttpResponse[StockMarketPriceRank]:
        """
        국내주식 시장가치 순위

        Args:
            fid_trgt_cls_code (str): 대상 구분 코드 (0:전체)
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드 (J:KRX, NX:NXT)
            fid_cond_scr_div_code (str): 조건 화면 분류 코드 (20179)
            fid_input_iscd (str): 입력 종목코드 (0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200)
            fid_div_cls_code (str): 분류 구분 코드 (0:전체, 1:관리종목, 2:투자주의, 3:투자경고, 4:투자위험예고, 5:투자위험, 6:보통주, 7:우선주)
            fid_input_price_1 (str): 입력 가격1 (입력값 없을때 전체, 가격~)
            fid_input_price_2 (str): 입력 가격2 (입력값 없을때 전체, ~가격)
            fid_vol_cnt (str): 거래량 수 (입력값 없을때 전체, 거래량~)
            fid_input_option_1 (str): 입력 옵션1 (회계연도, 예: 2023)
            fid_input_option_2 (str): 입력 옵션2 (0:1/4분기, 1:반기, 2:3/4분기, 3:결산)
            fid_rank_sort_cls_code (str): 순위 정렬 구분 코드 (가치분석: 23:PER, 24:PBR, 25:PCR, 26:PSR, 27:EPS, 28:EVA, 29:EBITDA, 30:EV/EBITDA, 31:EBITDA/금융비율)
            fid_blng_cls_code (str): 소속 구분 코드 (0:전체)
            fid_trgt_exls_cls_code (str): 대상 제외 구분 코드 (0:전체)

        Returns:
            StockMarketPriceRank: 국내주식 시장가치 순위 응답 객체
        """
        headers = {
            "tr_id": "FHPST01790000",
        }
        params = {
            "fid_trgt_cls_code": fid_trgt_cls_code,
            "fid_cond_mrkt_div_code": fid_cond_mrkt_div_code,
            "fid_cond_scr_div_code": fid_cond_scr_div_code,
            "fid_input_iscd": fid_input_iscd,
            "fid_div_cls_code": fid_div_cls_code,
            "fid_input_price_1": fid_input_price_1,
            "fid_input_price_2": fid_input_price_2,
            "fid_vol_cnt": fid_vol_cnt,
            "fid_input_option_1": fid_input_option_1,
            "fid_input_option_2": fid_input_option_2,
            "fid_rank_sort_cls_code": fid_rank_sort_cls_code,
            "fid_blng_cls_code": fid_blng_cls_code,
            "fid_trgt_exls_cls_code": fid_trgt_exls_cls_code,
        }
        response = self.client._get("/uapi/domestic-stock/v1/ranking/market-value", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock market price rank: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockMarketPriceRank.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_stock_execution_strength_top(
        self,
        fid_trgt_exls_cls_code: str,
        fid_cond_mrkt_div_code: str,
        fid_cond_scr_div_code: str,
        fid_input_iscd: str,
        fid_div_cls_code: str,
        fid_input_price_1: str,
        fid_input_price_2: str,
        fid_vol_cnt: str,
        fid_trgt_cls_code: str,
    ) -> KisHttpResponse[StockExecutionStrengthTop]:
        """
        국내주식 체결강도 상위

        Args:
            fid_trgt_exls_cls_code (str): 대상 제외 구분 코드 (0:전체)
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드 (J:KRX, NX:NXT)
            fid_cond_scr_div_code (str): 조건 화면 분류 코드 (20168)
            fid_input_iscd (str): 입력 종목코드 (0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200)
            fid_div_cls_code (str): 분류 구분 코드 (0:전체, 1:보통주, 2:우선주)
            fid_input_price_1 (str): 입력 가격1 (입력값 없을때 전체, 가격~)
            fid_input_price_2 (str): 입력 가격2 (입력값 없을때 전체, ~가격)
            fid_vol_cnt (str): 거래량 수 (입력값 없을때 전체, 거래량~)
            fid_trgt_cls_code (str): 대상 구분 코드 (0:전체)

        Returns:
            StockExecutionStrengthTop: 국내주식 체결강도 상위 응답 객체
        """
        headers = {
            "tr_id": "FHPST01680000",
        }
        params = {
            "fid_trgt_exls_cls_code": fid_trgt_exls_cls_code,
            "fid_cond_mrkt_div_code": fid_cond_mrkt_div_code,
            "fid_cond_scr_div_code": fid_cond_scr_div_code,
            "fid_input_iscd": fid_input_iscd,
            "fid_div_cls_code": fid_div_cls_code,
            "fid_input_price_1": fid_input_price_1,
            "fid_input_price_2": fid_input_price_2,
            "fid_vol_cnt": fid_vol_cnt,
            "fid_trgt_cls_code": fid_trgt_cls_code,
        }
        response = self.client._get("/uapi/domestic-stock/v1/ranking/volume-power", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock execution strength top: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockExecutionStrengthTop.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_stock_watchlist_registration_top(
        self,
        fid_input_iscd_2: str,
        fid_cond_mrkt_div_code: str,
        fid_cond_scr_div_code: str,
        fid_input_iscd: str,
        fid_trgt_cls_code: str,
        fid_trgt_exls_cls_code: str,
        fid_input_price_1: str,
        fid_input_price_2: str,
        fid_vol_cnt: str,
        fid_div_cls_code: str,
        fid_input_cnt_1: str,
    ) -> KisHttpResponse[StockWatchlistRegistrationTop]:
        """
        국내주식 관심종목등록 상위

        Args:
            fid_input_iscd_2 (str): 입력 필수값2 (000000:필수입력값)
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드 (J:KRX, NX:NXT)
            fid_cond_scr_div_code (str): 조건 화면 분류 코드 (20180)
            fid_input_iscd (str): 업종 코드 (0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200)
            fid_trgt_cls_code (str): 대상 구분 코드 (0:전체)
            fid_trgt_exls_cls_code (str): 대상 제외 구분 코드 (0:전체)
            fid_input_price_1 (str): 입력 가격1 (입력값 없을때 전체, 가격~)
            fid_input_price_2 (str): 입력 가격2 (입력값 없을때 전체, ~가격)
            fid_vol_cnt (str): 거래량 수 (입력값 없을때 전체, 거래량~)
            fid_div_cls_code (str): 분류 구분 코드 (0:전체, 1:관리종목, 2:투자주의, 3:투자경고, 4:투자위험예고, 5:투자위험, 6:보통주, 7:우선주)
            fid_input_cnt_1 (str): 순위 입력값 (순위검색 입력값, 1:1위부터, 10:10위부터)

        Returns:
            StockWatchlistRegistrationTop: 국내주식 관심종목등록 상위 응답 객체
        """
        headers = {
            "tr_id": "FHPST01800000",
        }
        params = {
            "fid_input_iscd_2": fid_input_iscd_2,
            "fid_cond_mrkt_div_code": fid_cond_mrkt_div_code,
            "fid_cond_scr_div_code": fid_cond_scr_div_code,
            "fid_input_iscd": fid_input_iscd,
            "fid_trgt_cls_code": fid_trgt_cls_code,
            "fid_trgt_exls_cls_code": fid_trgt_exls_cls_code,
            "fid_input_price_1": fid_input_price_1,
            "fid_input_price_2": fid_input_price_2,
            "fid_vol_cnt": fid_vol_cnt,
            "fid_div_cls_code": fid_div_cls_code,
            "fid_input_cnt_1": fid_input_cnt_1,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/ranking/top-interest-stock", headers=headers, params=params
        )
        if response.status_code != 200:
            raise Exception(f"Error fetching stock watchlist registration top: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockWatchlistRegistrationTop.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_stock_expected_execution_rise_decline_top(
        self,
        fid_rank_sort_cls_code: str,
        fid_cond_mrkt_div_code: str,
        fid_cond_scr_div_code: str,
        fid_input_iscd: str,
        fid_div_cls_code: str,
        fid_aply_rang_prc_1: str,
        fid_vol_cnt: str,
        fid_pbmn: str,
        fid_blng_cls_code: str,
        fid_mkop_cls_code: str,
    ) -> KisHttpResponse[StockExpectedExecutionRiseDeclineTop]:
        """
        국내주식 예상체결 상승/하락상위

        Args:
            fid_rank_sort_cls_code (str): 순위 정렬 구분 코드 (0:상승률, 1:상승폭, 2:보합, 3:하락율, 4:하락폭, 5:체결량, 6:거래대금)
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드 (주식 J)
            fid_cond_scr_div_code (str): 조건 화면 분류 코드 (20182)
            fid_input_iscd (str): 입력 종목코드 (0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200, 4001:KRX100)
            fid_div_cls_code (str): 분류 구분 코드 (0:전체, 1:보통주, 2:우선주)
            fid_aply_rang_prc_1 (str): 적용 범위 가격1 (입력값 없을때 전체, 가격~)
            fid_vol_cnt (str): 거래량 수 (입력값 없을때 전체, 거래량~)
            fid_pbmn (str): 거래대금 (입력값 없을때 전체, 거래대금~ 천원단위)
            fid_blng_cls_code (str): 소속 구분 코드 (0:전체)
            fid_mkop_cls_code (str): 장운영 구분 코드 (0:장전예상, 1:장마감예상)

        Returns:
            StockExpectedExecutionRiseDeclineTop: 국내주식 예상체결 상승/하락상위 응답 객체
        """
        headers = {
            "tr_id": "FHPST01820000",
        }
        params = {
            "fid_rank_sort_cls_code": fid_rank_sort_cls_code,
            "fid_cond_mrkt_div_code": fid_cond_mrkt_div_code,
            "fid_cond_scr_div_code": fid_cond_scr_div_code,
            "fid_input_iscd": fid_input_iscd,
            "fid_div_cls_code": fid_div_cls_code,
            "fid_aply_rang_prc_1": fid_aply_rang_prc_1,
            "fid_vol_cnt": fid_vol_cnt,
            "fid_pbmn": fid_pbmn,
            "fid_blng_cls_code": fid_blng_cls_code,
            "fid_mkop_cls_code": fid_mkop_cls_code,
        }
        response = self.client._get("/uapi/domestic-stock/v1/ranking/exp-trans-updown", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock expected execution rise decline top: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockExpectedExecutionRiseDeclineTop.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_stock_proprietary_trading_top(
        self,
        fid_trgt_exls_cls_code: str,
        fid_cond_mrkt_div_code: str,
        fid_cond_scr_div_code: str,
        fid_div_cls_code: str,
        fid_rank_sort_cls_code: str,
        fid_input_date_1: str,
        fid_input_date_2: str,
        fid_input_iscd: str,
        fid_trgt_cls_code: str,
        fid_aply_rang_vol: str,
        fid_aply_rang_prc_2: str,
        fid_aply_rang_prc_1: str,
    ) -> KisHttpResponse[StockProprietaryTradingTop]:
        """
        국내주식 당사매매종목 상위

        Args:
            fid_trgt_exls_cls_code (str): 대상 제외 구분 코드 (0:전체)
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드 (J:KRX, NX:NXT)
            fid_cond_scr_div_code (str): 조건 화면 분류 코드 (20186)
            fid_div_cls_code (str): 분류 구분 코드 (0:전체, 1:관리종목, 2:투자주의, 3:투자경고, 4:투자위험예고, 5:투자위험, 6:보통주, 7:우선주)
            fid_rank_sort_cls_code (str): 순위 정렬 구분 코드 (0:매도상위, 1:매수상위)
            fid_input_date_1 (str): 입력 날짜1 (기간~)
            fid_input_date_2 (str): 입력 날짜2 (~기간)
            fid_input_iscd (str): 입력 종목코드 (0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200, 4001:KRX100)
            fid_trgt_cls_code (str): 대상 구분 코드 (0:전체)
            fid_aply_rang_vol (str): 적용 범위 거래량 (0:전체, 100:100주 이상)
            fid_aply_rang_prc_2 (str): 적용 범위 가격2 (~가격)
            fid_aply_rang_prc_1 (str): 적용 범위 가격1 (가격~)

        Returns:
            StockProprietaryTradingTop: 국내주식 당사매매종목 상위 응답 객체
        """
        headers = {
            "tr_id": "FHPST01860000",
        }
        params = {
            "fid_trgt_exls_cls_code": fid_trgt_exls_cls_code,
            "fid_cond_mrkt_div_code": fid_cond_mrkt_div_code,
            "fid_cond_scr_div_code": fid_cond_scr_div_code,
            "fid_div_cls_code": fid_div_cls_code,
            "fid_rank_sort_cls_code": fid_rank_sort_cls_code,
            "fid_input_date_1": fid_input_date_1,
            "fid_input_date_2": fid_input_date_2,
            "fid_input_iscd": fid_input_iscd,
            "fid_trgt_cls_code": fid_trgt_cls_code,
            "fid_aply_rang_vol": fid_aply_rang_vol,
            "fid_aply_rang_prc_2": fid_aply_rang_prc_2,
            "fid_aply_rang_prc_1": fid_aply_rang_prc_1,
        }
        response = self.client._get("/uapi/domestic-stock/v1/ranking/traded-by-company", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock proprietary trading top: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockProprietaryTradingTop.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_stock_new_high_low_approaching_top(
        self,
        fid_aply_rang_vol: str,
        fid_cond_mrkt_div_code: str,
        fid_cond_scr_div_code: str,
        fid_div_cls_code: str,
        fid_input_cnt_1: str,
        fid_input_cnt_2: str,
        fid_prc_cls_code: str,
        fid_input_iscd: str,
        fid_trgt_cls_code: str,
        fid_trgt_exls_cls_code: str,
        fid_aply_rang_prc_1: str,
        fid_aply_rang_prc_2: str,
    ) -> KisHttpResponse[StockNewHighLowApproachingTop]:
        """
        국내주식 신고/신저근접종목 상위

        Args:
            fid_aply_rang_vol (str): 적용 범위 거래량 (0:전체, 100:100주 이상)
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드 (주식 J)
            fid_cond_scr_div_code (str): 조건 화면 분류 코드 (20187)
            fid_div_cls_code (str): 분류 구분 코드 (0:전체, 1:관리종목, 2:투자주의, 3:투자경고)
            fid_input_cnt_1 (str): 입력 수1 (괴리율 최소)
            fid_input_cnt_2 (str): 입력 수2 (괴리율 최대)
            fid_prc_cls_code (str): 가격 구분 코드 (0:신고근접, 1:신저근접)
            fid_input_iscd (str): 입력 종목코드 (0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200, 4001:KRX100)
            fid_trgt_cls_code (str): 대상 구분 코드 (0:전체)
            fid_trgt_exls_cls_code (str): 대상 제외 구분 코드 (0:전체, 1:관리종목, 2:투자주의, 3:투자경고, 4:투자위험예고, 5:투자위험, 6:보통주, 7:우선주)
            fid_aply_rang_prc_1 (str): 적용 범위 가격1 (가격~)
            fid_aply_rang_prc_2 (str): 적용 범위 가격2 (~가격)

        Returns:
            StockNewHighLowApproachingTop: 국내주식 신고/신저근접종목 상위 응답 객체
        """
        headers = {
            "tr_id": "FHPST01870000",
        }
        params = {
            "fid_aply_rang_vol": fid_aply_rang_vol,
            "fid_cond_mrkt_div_code": fid_cond_mrkt_div_code,
            "fid_cond_scr_div_code": fid_cond_scr_div_code,
            "fid_div_cls_code": fid_div_cls_code,
            "fid_input_cnt_1": fid_input_cnt_1,
            "fid_input_cnt_2": fid_input_cnt_2,
            "fid_prc_cls_code": fid_prc_cls_code,
            "fid_input_iscd": fid_input_iscd,
            "fid_trgt_cls_code": fid_trgt_cls_code,
            "fid_trgt_exls_cls_code": fid_trgt_exls_cls_code,
            "fid_aply_rang_prc_1": fid_aply_rang_prc_1,
            "fid_aply_rang_prc_2": fid_aply_rang_prc_2,
        }
        response = self.client._get("/uapi/domestic-stock/v1/ranking/near-new-highlow", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock new high low approaching top: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockNewHighLowApproachingTop.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_stock_dividend_yield_top(
        self,
        cts_area: str,
        gb1: str,
        upjong: str,
        gb2: str,
        gb3: str,
        f_dt: str,
        t_dt: str,
        gb4: str,
    ) -> KisHttpResponse[StockDividendYieldTop]:
        """
        국내주식 배당률 상위

        Args:
            cts_area (str): CTS_AREA (공백)
            gb1 (str): KOSPI (0:전체, 1:코스피, 2:코스피200, 3:코스닥)
            upjong (str): 업종구분 (코스피: 0001:종합, 0002:대형주..0027:제조업, 코스닥: 1001:종합..1041:IT부품, 코스피200: 2001:KOSPI200, 2007:KOSPI100, 2008:KOSPI50)
            gb2 (str): 종목선택 (0:전체, 6:보통주, 7:우선주)
            gb3 (str): 배당구분 (1:주식배당, 2:현금배당)
            f_dt (str): 기준일From (YYYYMMDD)
            t_dt (str): 기준일To (YYYYMMDD)
            gb4 (str): 결산/중간배당 (0:전체, 1:결산배당, 2:중간배당)

        Returns:
            StockDividendYieldTop: 국내주식 배당률 상위 응답 객체
        """
        headers = {
            "tr_id": "HHKDB13470100",
        }
        params = {
            "CTS_AREA": cts_area,
            "GB1": gb1,
            "UPJONG": upjong,
            "GB2": gb2,
            "GB3": gb3,
            "F_DT": f_dt,
            "T_DT": t_dt,
            "GB4": gb4,
        }
        response = self.client._get("/uapi/domestic-stock/v1/ranking/dividend-rate", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock dividend yield top: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockDividendYieldTop.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_stock_large_execution_count_top(
        self,
        fid_aply_rang_prc_2: str,
        fid_cond_mrkt_div_code: str,
        fid_cond_scr_div_code: str,
        fid_input_iscd: str,
        fid_rank_sort_cls_code: str,
        fid_div_cls_code: str,
        fid_input_price_1: str,
        fid_aply_rang_prc_1: str,
        fid_input_iscd_2: str,
        fid_trgt_exls_cls_code: str,
        fid_trgt_cls_code: str,
        fid_vol_cnt: str,
    ) -> KisHttpResponse[StockLargeExecutionCountTop]:
        """
        국내주식 대량체결건수 상위

        Args:
            fid_aply_rang_prc_2 (str): 적용 범위 가격2 (~가격)
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드 (J:KRX, NX:NXT)
            fid_cond_scr_div_code (str): 조건 화면 분류 코드 (11909)
            fid_input_iscd (str): 입력 종목코드 (0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200, 4001:KRX100)
            fid_rank_sort_cls_code (str): 순위 정렬 구분 코드 (0:매수상위, 1:매도상위)
            fid_div_cls_code (str): 분류 구분 코드 (0:전체)
            fid_input_price_1 (str): 입력 가격1 (건별금액~)
            fid_aply_rang_prc_1 (str): 적용 범위 가격1 (가격~)
            fid_input_iscd_2 (str): 입력 종목코드2 (공백:전체종목, 개별종목 조회시 종목코드, 예: 000660)
            fid_trgt_exls_cls_code (str): 대상 제외 구분 코드 (0:전체)
            fid_trgt_cls_code (str): 대상 구분 코드 (0:전체)
            fid_vol_cnt (str): 거래량 수 (거래량~)

        Returns:
            StockLargeExecutionCountTop: 국내주식 대량체결건수 상위 응답 객체
        """
        headers = {
            "tr_id": "HHKST1909000C0",
        }
        params = {
            "fid_aply_rang_prc_2": fid_aply_rang_prc_2,
            "fid_cond_mrkt_div_code": fid_cond_mrkt_div_code,
            "fid_cond_scr_div_code": fid_cond_scr_div_code,
            "fid_input_iscd": fid_input_iscd,
            "fid_rank_sort_cls_code": fid_rank_sort_cls_code,
            "fid_div_cls_code": fid_div_cls_code,
            "fid_input_price_1": fid_input_price_1,
            "fid_aply_rang_prc_1": fid_aply_rang_prc_1,
            "fid_input_iscd_2": fid_input_iscd_2,
            "fid_trgt_exls_cls_code": fid_trgt_exls_cls_code,
            "fid_trgt_cls_code": fid_trgt_cls_code,
            "fid_vol_cnt": fid_vol_cnt,
        }
        response = self.client._get("/uapi/domestic-stock/v1/ranking/bulk-trans-num", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock large execution count top: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockLargeExecutionCountTop.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_stock_credit_balance_top(
        self,
        fid_cond_scr_div_code: str,
        fid_input_iscd: str,
        fid_option: str,
        fid_cond_mrkt_div_code: str,
        fid_rank_sort_cls_code: str,
    ) -> KisHttpResponse[StockCreditBalanceTop]:
        """
        국내주식 신용잔고 상위

        Args:
            fid_cond_scr_div_code (str): 조건 화면 분류 코드 (11701)
            fid_input_iscd (str): 입력 종목코드 (0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200)
            fid_option (str): 증가율기간 (2~999)
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드 (주식 J)
            fid_rank_sort_cls_code (str): 순위 정렬 구분 코드 (융자: 0:잔고비율상위, 1:잔고수량상위, 2:잔고금액상위, 3:잔고비율증가상위, 4:잔고비율감소상위, 대주: 5:잔고비율상위, 6:잔고수량상위, 7:잔고금액상위, 8:잔고비율증가상위, 9:잔고비율감소상위)

        Returns:
            StockCreditBalanceTop: 국내주식 신용잔고 상위 응답 객체
        """
        headers = {
            "tr_id": "HHKST17010000",
        }
        params = {
            "FID_COND_SCR_DIV_CODE": fid_cond_scr_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_OPTION": fid_option,
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_RANK_SORT_CLS_CODE": fid_rank_sort_cls_code,
        }
        response = self.client._get("/uapi/domestic-stock/v1/ranking/credit-balance", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock credit balance top: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockCreditBalanceTop.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_stock_short_selling_top(
        self,
        fid_aply_rang_vol: str,
        fid_cond_mrkt_div_code: str,
        fid_cond_scr_div_code: str,
        fid_input_iscd: str,
        fid_period_div_code: str,
        fid_input_cnt_1: str,
        fid_trgt_exls_cls_code: str,
        fid_trgt_cls_code: str,
        fid_aply_rang_prc_1: str,
        fid_aply_rang_prc_2: str,
    ) -> KisHttpResponse[StockShortSellingTop]:
        """
        국내주식 공매도 상위종목

        Args:
            fid_aply_rang_vol (str): FID 적용 범위 거래량 (공백)
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드 (주식 J)
            fid_cond_scr_div_code (str): 조건 화면 분류 코드 (20482)
            fid_input_iscd (str): 입력 종목코드 (0000:전체, 0001:코스피, 1001:코스닥, 2001:코스피200, 4001:KRX100, 3003:코스닥150)
            fid_period_div_code (str): 조회구분 (D:일, M:월)
            fid_input_cnt_1 (str): 조회기간(일수) (조회구분 D: 0:1일, 1:2일, 2:3일, 3:4일, 4:1주일, 9:2주일, 14:3주일, 조회구분 M: 1:1개월, 2:2개월, 3:3개월)
            fid_trgt_exls_cls_code (str): 대상 제외 구분 코드 (공백)
            fid_trgt_cls_code (str): FID 대상 구분 코드 (공백)
            fid_aply_rang_prc_1 (str): FID 적용 범위 가격1 (가격~)
            fid_aply_rang_prc_2 (str): FID 적용 범위 가격2 (~가격)

        Returns:
            StockShortSellingTop: 국내주식 공매도 상위종목 응답 객체
        """
        headers = {
            "tr_id": "FHPST04820000",
        }
        params = {
            "FID_APLY_RANG_VOL": fid_aply_rang_vol,
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_COND_SCR_DIV_CODE": fid_cond_scr_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_PERIOD_DIV_CODE": fid_period_div_code,
            "FID_INPUT_CNT_1": fid_input_cnt_1,
            "FID_TRGT_EXLS_CLS_CODE": fid_trgt_exls_cls_code,
            "FID_TRGT_CLS_CODE": fid_trgt_cls_code,
            "FID_APLY_RANG_PRC_1": fid_aply_rang_prc_1,
            "FID_APLY_RANG_PRC_2": fid_aply_rang_prc_2,
        }
        response = self.client._get("/uapi/domestic-stock/v1/ranking/short-sale", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock short selling top: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockShortSellingTop.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_stock_after_hours_fluctuation_rank(
        self,
        fid_cond_mrkt_div_code: str,
        fid_mrkt_cls_code: str,
        fid_cond_scr_div_code: str,
        fid_input_iscd: str,
        fid_div_cls_code: str,
        fid_input_price_1: str,
        fid_input_price_2: str,
        fid_vol_cnt: str,
        fid_trgt_cls_code: str,
        fid_trgt_exls_cls_code: str,
    ) -> KisHttpResponse[StockAfterHoursFluctuationRank]:
        """
        국내주식 시간외등락율순위

        Args:
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드 (J:주식)
            fid_mrkt_cls_code (str): 시장 구분 코드 (공백 입력)
            fid_cond_scr_div_code (str): 조건 화면 분류 코드 (20234)
            fid_input_iscd (str): 입력 종목코드 (0000:전체, 0001:코스피, 1001:코스닥)
            fid_div_cls_code (str): 분류 구분 코드 (1:상한가, 2:상승률, 3:보합, 4:하한가, 5:하락률)
            fid_input_price_1 (str): 입력 가격1 (입력값 없을때 전체, 가격~)
            fid_input_price_2 (str): 입력 가격2 (입력값 없을때 전체, ~가격)
            fid_vol_cnt (str): 거래량 수 (입력값 없을때 전체, 거래량~)
            fid_trgt_cls_code (str): 대상 구분 코드 (공백 입력)
            fid_trgt_exls_cls_code (str): 대상 제외 구분 코드 (공백 입력)

        Returns:
            StockAfterHoursFluctuationRank: 국내주식 시간외등락율순위 응답 객체
        """
        headers = {
            "tr_id": "FHPST02340000",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_MRKT_CLS_CODE": fid_mrkt_cls_code,
            "FID_COND_SCR_DIV_CODE": fid_cond_scr_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_DIV_CLS_CODE": fid_div_cls_code,
            "FID_INPUT_PRICE_1": fid_input_price_1,
            "FID_INPUT_PRICE_2": fid_input_price_2,
            "FID_VOL_CNT": fid_vol_cnt,
            "FID_TRGT_CLS_CODE": fid_trgt_cls_code,
            "FID_TRGT_EXLS_CLS_CODE": fid_trgt_exls_cls_code,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/ranking/overtime-fluctuation", headers=headers, params=params
        )
        if response.status_code != 200:
            raise Exception(f"Error fetching stock after hours fluctuation rank: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockAfterHoursFluctuationRank.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_stock_after_hours_volume_rank(
        self,
        fid_cond_mrkt_div_code: str,
        fid_cond_scr_div_code: str,
        fid_input_iscd: str,
        fid_rank_sort_cls_code: str,
        fid_input_price_1: str,
        fid_input_price_2: str,
        fid_vol_cnt: str,
        fid_trgt_cls_code: str,
        fid_trgt_exls_cls_code: str,
    ) -> KisHttpResponse[StockAfterHoursVolumeRank]:
        """
        국내주식 시간외거래량순위

        Args:
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드 (J:주식)
            fid_cond_scr_div_code (str): 조건 화면 분류 코드 (20235)
            fid_input_iscd (str): 입력 종목코드 (0000:전체, 0001:코스피, 1001:코스닥)
            fid_rank_sort_cls_code (str): 순위 정렬 구분 코드 (0:매수잔량, 1:매도잔량, 2:거래량)
            fid_input_price_1 (str): 입력 가격1 (가격~)
            fid_input_price_2 (str): 입력 가격2 (~가격)
            fid_vol_cnt (str): 거래량 수 (거래량~)
            fid_trgt_cls_code (str): 대상 구분 코드 (공백)
            fid_trgt_exls_cls_code (str): 대상 제외 구분 코드 (공백)

        Returns:
            StockAfterHoursVolumeRank: 국내주식 시간외거래량순위 응답 객체
        """
        headers = {
            "tr_id": "FHPST02350000",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_COND_SCR_DIV_CODE": fid_cond_scr_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_RANK_SORT_CLS_CODE": fid_rank_sort_cls_code,
            "FID_INPUT_PRICE_1": fid_input_price_1,
            "FID_INPUT_PRICE_2": fid_input_price_2,
            "FID_VOL_CNT": fid_vol_cnt,
            "FID_TRGT_CLS_CODE": fid_trgt_cls_code,
            "FID_TRGT_EXLS_CLS_CODE": fid_trgt_exls_cls_code,
        }
        response = self.client._get("/uapi/domestic-stock/v1/ranking/overtime-volume", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock after hours volume rank: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockAfterHoursVolumeRank.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_hts_inquiry_top_20(self) -> KisHttpResponse[HtsInquiryTop20]:
        """
        HTS조회상위20종목

        Returns:
            KisHttpResponse[HtsInquiryTop20]: HTS조회상위20종목 응답 객체
        """
        headers = {
            "tr_id": "HHMCM000100C0",
        }
        params = {}
        response = self.client._get("/uapi/domestic-stock/v1/ranking/hts-top-view", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching HTS inquiry top 20: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = HtsInquiryTop20.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)
