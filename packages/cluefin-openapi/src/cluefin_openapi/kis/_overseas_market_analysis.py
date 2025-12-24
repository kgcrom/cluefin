from cluefin_openapi.kis._http_client import HttpClient
from cluefin_openapi.kis._model import KisHttpHeader, KisHttpResponse
from cluefin_openapi.kis._overseas_market_analysis_types import (
    BreakingNewsTitle,
    NewsAggregateTitle,
    StockBuyExecutionStrengthTop,
    StockCollateralLoanEligible,
    StockMarketCapRank,
    StockNewHighLowPrice,
    StockPeriodRightsInquiry,
    StockPriceFluctuation,
    StockRightsAggregate,
    StockRiseDeclineRate,
    StockTradingAmountRank,
    StockTradingIncreaseRateRank,
    StockTradingTurnoverRateRank,
    StockTradingVolumeRank,
    StockVolumeSurge,
)


class OverseasMarketAnalysis:
    """해외주식 시세분석"""

    def __init__(self, client: HttpClient):
        self.client = client

    def get_stock_price_fluctuation(
        self,
        excd: str,
        gubn: str,
        mixn: str,
        vol_rang: str,
    ) -> KisHttpResponse[StockPriceFluctuation]:
        """
        해외주식 가격급등락

        Args:
            excd (str): 거래소코드 (NYS: 뉴욕, NAS: 나스닥, AMS: 아멕스, HKS: 홍콩, SHS: 상해, SZS: 심천, HSX: 호치민, HNX: 하노이, TSE: 도쿄)
            gubn (str): 급등/급락구분 (0: 급락, 1: 급등)
            mixn (str): N분전콤보값 (0: 1분전, 1: 2분전, 2: 3분전, 3: 5분전, 4: 10분전, 5: 15분전, 6: 20분전, 7: 30분전, 8: 60분전, 9: 120분전)
            vol_rang (str): 거래량조건 (0: 전체, 1: 1백주이상, 2: 1천주이상, 3: 1만주이상, 4: 10만주이상, 5: 100만주이상, 6: 1000만주이상)

        Returns:
            StockPriceRiseFall: 해외주식 가격급등락 응답 객체
        """
        headers = {
            "tr_id": "HHDFS76260000",
        }
        params = {
            "KEYB": "",
            "AUTH": "",
            "EXCD": excd,
            "GUBN": gubn,
            "MIXN": mixn,
            "VOL_RANG": vol_rang,
        }
        response = self.client._get("/uapi/overseas-stock/v1/ranking/price-fluctuation", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock price fluctuation: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockPriceFluctuation.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_stock_volume_surge(
        self,
        keyb: str,
        auth: str,
        excd: str,
        mixn: str,
        vol_rang: str,
    ) -> KisHttpResponse[StockVolumeSurge]:
        """
        해외주식 거래량급증

        Args:
            keyb (str): NEXT KEY BUFF (공백)
            auth (str): 사용자권한정보 (공백)
            excd (str): 거래소코드 (NYS: 뉴욕, NAS: 나스닥, AMS: 아멕스, HKS: 홍콩, SHS: 상해, SZS: 심천, HSX: 호치민, HNX: 하노이, TSE: 도쿄)
            mixn (str): N분전콤보값 (0: 1분전, 1: 2분전, 2: 3분전, 3: 5분전, 4: 10분전, 5: 15분전, 6: 20분전, 7: 30분전, 8: 60분전, 9: 120분전)
            vol_rang (str): 거래량조건 (0: 전체, 1: 1백주이상, 2: 1천주이상, 3: 1만주이상, 4: 10만주이상, 5: 100만주이상, 6: 1000만주이상)

        Returns:
            StockVolumeSurge: 해외주식 거래량급증 응답 객체
        """
        headers = {
            "tr_id": "HHDFS76270000",
        }
        params = {
            "KEYB": keyb,
            "AUTH": auth,
            "EXCD": excd,
            "MIXN": mixn,
            "VOL_RANG": vol_rang,
        }
        response = self.client._get("/uapi/overseas-stock/v1/ranking/volume-surge", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock volume surge: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockVolumeSurge.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_stock_buy_execution_strength_top(
        self,
        keyb: str,
        auth: str,
        excd: str,
        nday: str,
        vol_rang: str,
    ) -> KisHttpResponse[StockBuyExecutionStrengthTop]:
        """
        해외주식 매수체결강도상위

        Args:
            keyb (str): NEXT KEY BUFF (공백)
            auth (str): 사용자권한정보 (공백)
            excd (str): 거래소코드 (NYS: 뉴욕, NAS: 나스닥, AMS: 아멕스, HKS: 홍콩, SHS: 상해, SZS: 심천, HSX: 호치민, HNX: 하노이, TSE: 도쿄)
            nday (str): N일자값 (0: 1분전, 1: 2분전, 2: 3분전, 3: 5분전, 4: 10분전, 5: 15분전, 6: 20분전, 7: 30분전, 8: 60분전, 9: 120분전)
            vol_rang (str): 거래량조건 (0: 전체, 1: 1백주이상, 2: 1천주이상, 3: 1만주이상, 4: 10만주이상, 5: 100만주이상, 6: 1000만주이상)

        Returns:
            StockBuyExecutionStrengthTop: 해외주식 매수체결강도상위 응답 객체
        """
        headers = {
            "tr_id": "HHDFS76280000",
        }
        params = {
            "KEYB": keyb,
            "AUTH": auth,
            "EXCD": excd,
            "NDAY": nday,
            "VOL_RANG": vol_rang,
        }
        response = self.client._get("/uapi/overseas-stock/v1/ranking/volume-power", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock buy execution strength top: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockBuyExecutionStrengthTop.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_stock_rise_decline_rate(
        self,
        keyb: str,
        auth: str,
        excd: str,
        gubn: str,
        nday: str,
        vol_rang: str,
    ) -> KisHttpResponse[StockRiseDeclineRate]:
        """
        해외주식 상승률/하락율

        Args:
            keyb (str): NEXT KEY BUFF (공백)
            auth (str): 사용자권한정보 (공백)
            excd (str): 거래소코드 (NYS: 뉴욕, NAS: 나스닥, AMS: 아멕스, HKS: 홍콩, SHS: 상해, SZS: 심천, HSX: 호치민, HNX: 하노이, TSE: 도쿄)
            gubn (str): 상승율/하락율 구분 (0: 하락율, 1: 상승율)
            nday (str): N일자값 (0: 당일, 1: 2일, 2: 3일, 3: 5일, 4: 10일, 5: 20일전, 6: 30일, 7: 60일, 8: 120일, 9: 1년)
            vol_rang (str): 거래량조건 (0: 전체, 1: 1백주이상, 2: 1천주이상, 3: 1만주이상, 4: 10만주이상, 5: 100만주이상, 6: 1000만주이상)

        Returns:
            StockRiseDeclineRate: 해외주식 상승률/하락율 응답 객체
        """
        headers = {
            "tr_id": "HHDFS76290000",
        }
        params = {
            "KEYB": keyb,
            "AUTH": auth,
            "EXCD": excd,
            "GUBN": gubn,
            "NDAY": nday,
            "VOL_RANG": vol_rang,
        }
        response = self.client._get("/uapi/overseas-stock/v1/ranking/updown-rate", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock rise decline rate: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockRiseDeclineRate.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_stock_new_high_low_price(
        self,
        keyb: str,
        auth: str,
        excd: str,
        gubn: str,
        gubn2: str,
        nday: str,
        vol_rang: str,
    ) -> KisHttpResponse[StockNewHighLowPrice]:
        """
        해외주식 신고/신저가

        Args:
            keyb (str): NEXT KEY BUFF (공백)
            auth (str): 사용자권한정보 (공백)
            excd (str): 거래소코드 (NYS: 뉴욕, NAS: 나스닥, AMS: 아멕스, HKS: 홍콩, SHS: 상해, SZS: 심천, HSX: 호치민, HNX: 하노이, TSE: 도쿄)
            gubn (str): 신고/신저 구분 (1: 신고, 0: 신저)
            gubn2 (str): 일시돌파/돌파 구분 (0: 일시돌파, 1: 돌파유지)
            nday (str): N일자값 (0: 5일, 1: 10일, 2: 20일, 3: 30일, 4: 60일, 5: 120일전, 6: 52주, 7: 1년)
            vol_rang (str): 거래량조건 (0: 전체, 1: 1백주이상, 2: 1천주이상, 3: 1만주이상, 4: 10만주이상, 5: 100만주이상, 6: 1000만주이상)

        Returns:
            StockNewHighLowPrice: 해외주식 신고/신저가 응답 객체
        """
        headers = {
            "tr_id": "HHDFS76300000",
        }
        params = {
            "KEYB": keyb,
            "AUTH": auth,
            "EXCD": excd,
            "GUBN": gubn,
            "GUBN2": gubn2,
            "NDAY": nday,
            "VOL_RANG": vol_rang,
        }
        response = self.client._get("/uapi/overseas-stock/v1/ranking/new-highlow", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock new high low price: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockNewHighLowPrice.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_stock_trading_volume_rank(
        self,
        keyb: str,
        auth: str,
        excd: str,
        nday: str,
        prc1: str,
        prc2: str,
        vol_rang: str,
    ) -> KisHttpResponse[StockTradingVolumeRank]:
        """
        해외주식 거래량순위

        Args:
            keyb (str): NEXT KEY BUFF (공백)
            auth (str): 사용자권한정보 (공백)
            excd (str): 거래소코드 (NYS: 뉴욕, NAS: 나스닥, AMS: 아멕스, HKS: 홍콩, SHS: 상해, SZS: 심천, HSX: 호치민, HNX: 하노이, TSE: 도쿄)
            nday (str): N일자값 (0: 당일, 1: 2일, 2: 3일, 3: 5일, 4: 10일, 5: 20일전, 6: 30일, 7: 60일, 8: 120일, 9: 1년)
            prc1 (str): 현재가 필터범위 1 (가격 ~)
            prc2 (str): 현재가 필터범위 2 (~ 가격)
            vol_rang (str): 거래량조건 (0: 전체, 1: 1백주이상, 2: 1천주이상, 3: 1만주이상, 4: 10만주이상, 5: 100만주이상, 6: 1000만주이상)

        Returns:
            StockTradingVolumeRank: 해외주식 거래량순위 응답 객체
        """
        headers = {
            "tr_id": "HHDFS76310010",
        }
        params = {
            "KEYB": keyb,
            "AUTH": auth,
            "EXCD": excd,
            "NDAY": nday,
            "PRC1": prc1,
            "PRC2": prc2,
            "VOL_RANG": vol_rang,
        }
        response = self.client._get("/uapi/overseas-stock/v1/ranking/trade-vol", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock trading volume rank: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockTradingVolumeRank.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_stock_trading_amount_rank(
        self,
        keyb: str,
        auth: str,
        excd: str,
        nday: str,
        vol_rang: str,
        prc1: str,
        prc2: str,
    ) -> KisHttpResponse[StockTradingAmountRank]:
        """
        해외주식 거래대금순위

        Args:
            keyb (str): NEXT KEY BUFF (공백)
            auth (str): 사용자권한정보 (공백)
            excd (str): 거래소코드 (NYS: 뉴욕, NAS: 나스닥, AMS: 아멕스, HKS: 홍콩, SHS: 상해, SZS: 심천, HSX: 호치민, HNX: 하노이, TSE: 도쿄)
            nday (str): N일자값 (0: 당일, 1: 2일, 2: 3일, 3: 5일, 4: 10일, 5: 20일전, 6: 30일, 7: 60일, 8: 120일, 9: 1년)
            vol_rang (str): 거래량조건 (0: 전체, 1: 1백주이상, 2: 1천주이상, 3: 1만주이상, 4: 10만주이상, 5: 100만주이상, 6: 1000만주이상)
            prc1 (str): 현재가 필터범위 1 (가격 ~)
            prc2 (str): 현재가 필터범위 2 (~ 가격)

        Returns:
            StockTradingAmountRank: 해외주식 거래대금순위 응답 객체
        """
        headers = {
            "tr_id": "HHDFS76320010",
        }
        params = {
            "KEYB": keyb,
            "AUTH": auth,
            "EXCD": excd,
            "NDAY": nday,
            "VOL_RANG": vol_rang,
            "PRC1": prc1,
            "PRC2": prc2,
        }
        response = self.client._get("/uapi/overseas-stock/v1/ranking/trade-pbmn", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock trading amount rank: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockTradingAmountRank.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_stock_trading_increase_rate_rank(
        self,
        keyb: str,
        auth: str,
        excd: str,
        nday: str,
        vol_rang: str,
    ) -> KisHttpResponse[StockTradingIncreaseRateRank]:
        """
        해외주식 거래증가율순위

        Args:
            keyb (str): NEXT KEY BUFF (공백)
            auth (str): 사용자권한정보 (공백)
            excd (str): 거래소코드 (NYS: 뉴욕, NAS: 나스닥, AMS: 아멕스, HKS: 홍콩, SHS: 상해, SZS: 심천, HSX: 호치민, HNX: 하노이, TSE: 도쿄)
            nday (str): N일자값 (0: 당일, 1: 2일, 2: 3일, 3: 5일, 4: 10일, 5: 20일전, 6: 30일, 7: 60일, 8: 120일, 9: 1년)
            vol_rang (str): 거래량조건 (0: 전체, 1: 1백주이상, 2: 1천주이상, 3: 1만주이상, 4: 10만주이상, 5: 100만주이상, 6: 1000만주이상)

        Returns:
            StockTradingIncreaseRateRank: 해외주식 거래증가율순위 응답 객체
        """
        headers = {
            "tr_id": "HHDFS76330000",
        }
        params = {
            "KEYB": keyb,
            "AUTH": auth,
            "EXCD": excd,
            "NDAY": nday,
            "VOL_RANG": vol_rang,
        }
        response = self.client._get("/uapi/overseas-stock/v1/ranking/trade-growth", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock trading increase rate rank: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockTradingIncreaseRateRank.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_stock_trading_turnover_rate_rank(
        self,
        keyb: str,
        auth: str,
        excd: str,
        nday: str,
        vol_rang: str,
    ) -> KisHttpResponse[StockTradingTurnoverRateRank]:
        """
        해외주식 거래회전율순위

        Args:
            keyb (str): NEXT KEY BUFF (공백)
            auth (str): 사용자권한정보 (공백)
            excd (str): 거래소코드 (NYS: 뉴욕, NAS: 나스닥, AMS: 아멕스, HKS: 홍콩, SHS: 상해, SZS: 심천, HSX: 호치민, HNX: 하노이, TSE: 도쿄)
            nday (str): N일자값 (0: 당일, 1: 2일, 2: 3일, 3: 5일, 4: 10일, 5: 20일전, 6: 30일, 7: 60일, 8: 120일, 9: 1년)
            vol_rang (str): 거래량조건 (0: 전체, 1: 1백주이상, 2: 1천주이상, 3: 1만주이상, 4: 10만주이상, 5: 100만주이상, 6: 1000만주이상)

        Returns:
            StockTradingTurnoverRateRank: 해외주식 거래회전율순위 응답 객체
        """
        headers = {
            "tr_id": "HHDFS76340000",
        }
        params = {
            "KEYB": keyb,
            "AUTH": auth,
            "EXCD": excd,
            "NDAY": nday,
            "VOL_RANG": vol_rang,
        }
        response = self.client._get("/uapi/overseas-stock/v1/ranking/trade-turnover", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock trading turnover rate rank: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockTradingTurnoverRateRank.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_stock_market_cap_rank(
        self,
        keyb: str,
        auth: str,
        excd: str,
        vol_rang: str,
    ) -> KisHttpResponse[StockMarketCapRank]:
        """
        해외주식 시가총액순위

        Args:
            keyb (str): NEXT KEY BUFF (공백)
            auth (str): 사용자권한정보 (공백)
            excd (str): 거래소코드 (NYS: 뉴욕, NAS: 나스닥, AMS: 아멕스, HKS: 홍콩, SHS: 상해, SZS: 심천, HSX: 호치민, HNX: 하노이, TSE: 도쿄)
            vol_rang (str): 거래량조건 (0: 전체, 1: 1백주이상, 2: 1천주이상, 3: 1만주이상, 4: 10만주이상, 5: 100만주이상, 6: 1000만주이상)

        Returns:
            StockMarketCapRank: 해외주식 시가총액순위 응답 객체
        """
        headers = {
            "tr_id": "HHDFS76350100",
        }
        params = {
            "KEYB": keyb,
            "AUTH": auth,
            "EXCD": excd,
            "VOL_RANG": vol_rang,
        }
        response = self.client._get("/uapi/overseas-stock/v1/ranking/market-cap", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock market cap rank: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockMarketCapRank.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_stock_period_rights_inquiry(
        self,
        rght_type_cd: str,
        inqr_dvsn_cd: str,
        inqr_strt_dt: str,
        inqr_end_dt: str,
        pdno: str,
        prdt_type_cd: str,
        ctx_area_nk50: str,
        ctx_area_fk50: str,
    ) -> KisHttpResponse[StockPeriodRightsInquiry]:
        """
        해외주식 기간별권리조회

        Args:
            rght_type_cd (str): 권리유형코드 (%%: 전체, 01: 유상, 02: 무상, 03: 배당, 11: 합병, 14: 액면분할, 15: 액면병합, 17: 감자, 54: WR청구, 61: 원리금상환, 71: WR소멸, 74: 배당옵션, 75: 특별배당, 76: ISINCODE변경, 77: 실권주청약)
            inqr_dvsn_cd (str): 조회구분코드 (02: 현지기준일, 03: 청약시작일, 04: 청약종료일)
            inqr_strt_dt (str): 조회시작일자 (YYYYMMDD)
            inqr_end_dt (str): 조회종료일자 (YYYYMMDD)
            pdno (str): 상품번호 (공백)
            prdt_type_cd (str): 상품유형코드 (공백)
            ctx_area_nk50 (str): 연속조회키50 (공백)
            ctx_area_fk50 (str): 연속조회검색조건50 (공백)

        Returns:
            StockPeriodRightsInquiry: 해외주식 기간별권리조회 응답 객체
        """
        headers = {
            "tr_id": "CTRGT011R",
        }
        params = {
            "RGHT_TYPE_CD": rght_type_cd,
            "INQR_DVSN_CD": inqr_dvsn_cd,
            "INQR_STRT_DT": inqr_strt_dt,
            "INQR_END_DT": inqr_end_dt,
            "PDNO": pdno,
            "PRDT_TYPE_CD": prdt_type_cd,
            "CTX_AREA_NK50": ctx_area_nk50,
            "CTX_AREA_FK50": ctx_area_fk50,
        }
        response = self.client._get("/uapi/overseas-price/v1/quotations/period-rights", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock period rights inquiry: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockPeriodRightsInquiry.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_news_aggregate_title(
        self,
        info_gb: str,
        class_cd: str,
        nation_cd: str,
        exchange_cd: str,
        symb: str,
        data_dt: str,
        data_tm: str,
        cts: str,
    ) -> KisHttpResponse[NewsAggregateTitle]:
        """
        해외뉴스종합(제목)

        Args:
            info_gb (str): 뉴스구분 (전체: 공백)
            class_cd (str): 중분류 (전체: 공백)
            nation_cd (str): 국가코드 (전체: 공백, CN: 중국, HK: 홍콩, US: 미국)
            exchange_cd (str): 거래소코드 (전체: 공백)
            symb (str): 종목코드 (전체: 공백)
            data_dt (str): 조회일자 (전체: 공백, 특정일자 YYYYMMDD ex. 20240502)
            data_tm (str): 조회시간 (전체: 공백, 특정시간 HHMMSS ex. 093500)
            cts (str): 다음키 (공백 입력)

        Returns:
            NewsAggregateTitle: 해외뉴스종합(제목) 응답 객체
        """
        headers = {
            "tr_id": "HHPSTH60100C1",
        }
        params = {
            "INFO_GB": info_gb,
            "CLASS_CD": class_cd,
            "NATION_CD": nation_cd,
            "EXCHANGE_CD": exchange_cd,
            "SYMB": symb,
            "DATA_DT": data_dt,
            "DATA_TM": data_tm,
            "CTS": cts,
        }
        response = self.client._get("/uapi/overseas-price/v1/quotations/news-title", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching news aggregate title: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = NewsAggregateTitle.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_stock_rights_aggregate(
        self,
        ncod: str,
        symb: str,
        st_ymd: str,
        ed_ymd: str,
    ) -> KisHttpResponse[StockRightsAggregate]:
        """
        해외주식 권리종합

        Args:
            ncod (str): 국가코드 (CN: 중국, HK: 홍콩, US: 미국, JP: 일본, VN: 베트남)
            symb (str): 심볼 (종목코드)
            st_ymd (str): 일자 시작일 (미입력 시 오늘-3개월, 기간지정 시 종료일 입력 ex. 20240514)
            ed_ymd (str): 일자 종료일 (미입력 시 오늘+3개월, 기간지정 시 종료일 입력 ex. 20240514)

        Returns:
            StockRightsAggregate: 해외주식 권리종합 응답 객체
        """
        headers = {
            "tr_id": "HHDFS78330900",
        }
        params = {
            "NCOD": ncod,
            "SYMB": symb,
            "ST_YMD": st_ymd,
            "ED_YMD": ed_ymd,
        }
        response = self.client._get("/uapi/overseas-price/v1/quotations/rights-by-ice", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock rights aggregate: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockRightsAggregate.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_stock_collateral_loan_eligible(
        self,
        pdno: str,
        prdt_type_cd: str,
        inqr_strt_dt: str,
        inqr_end_dt: str,
        inqr_dvsn: str,
        natn_cd: str,
        inqr_sqn_dvsn: str,
        rt_dvsn_cd: str,
        rt: str,
        loan_psbl_yn: str,
        ctx_area_fk100: str,
        ctx_area_nk100: str,
    ) -> KisHttpResponse[StockCollateralLoanEligible]:
        """
        당사 해외주식담보대출 가능 종목

        Args:
            pdno (str): 상품번호 (ex. AMD)
            prdt_type_cd (str): 상품유형코드 (공백)
            inqr_strt_dt (str): 조회시작일자 (공백)
            inqr_end_dt (str): 조회종료일자 (공백)
            inqr_dvsn (str): 조회구분 (공백)
            natn_cd (str): 국가코드 (840: 미국, 344: 홍콩, 156: 중국)
            inqr_sqn_dvsn (str): 조회순서구분 (01: 이름순, 02: 코드순)
            rt_dvsn_cd (str): 비율구분코드 (공백)
            rt (str): 비율 (공백)
            loan_psbl_yn (str): 대출가능여부 (공백)
            ctx_area_fk100 (str): 연속조회검색조건100 (공백)
            ctx_area_nk100 (str): 연속조회키100 (공백)

        Returns:
            StockCollateralLoanEligible: 당사 해외주식담보대출 가능 종목 응답 객체
        """
        headers = {
            "tr_id": "CTLN4050R",
        }
        params = {
            "PDNO": pdno,
            "PRDT_TYPE_CD": prdt_type_cd,
            "INQR_STRT_DT": inqr_strt_dt,
            "INQR_END_DT": inqr_end_dt,
            "INQR_DVSN": inqr_dvsn,
            "NATN_CD": natn_cd,
            "INQR_SQN_DVSN": inqr_sqn_dvsn,
            "RT_DVSN_CD": rt_dvsn_cd,
            "RT": rt,
            "LOAN_PSBL_YN": loan_psbl_yn,
            "CTX_AREA_FK100": ctx_area_fk100,
            "CTX_AREA_NK100": ctx_area_nk100,
        }
        response = self.client._get(
            "/uapi/overseas-price/v1/quotations/colable-by-company", headers=headers, params=params
        )
        if response.status_code != 200:
            raise Exception(f"Error fetching stock collateral loan eligible: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockCollateralLoanEligible.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_breaking_news_title(
        self,
        fid_news_ofer_entp_code: str,
        fid_cond_mrkt_cls_code: str,
        fid_input_iscd: str,
        fid_titl_cntt: str,
        fid_input_date_1: str,
        fid_input_hour_1: str,
        fid_rank_sort_cls_code: str,
        fid_input_srno: str,
        fid_cond_scr_div_code: str,
    ) -> KisHttpResponse[BreakingNewsTitle]:
        """
        해외속보(제목)

        Args:
            fid_news_ofer_entp_code (str): 뉴스제공업체코드 (0: 전체조회)
            fid_cond_mrkt_cls_code (str): 조건시장구분코드 (공백)
            fid_input_iscd (str): 입력종목코드 (공백)
            fid_titl_cntt (str): 제목내용 (공백)
            fid_input_date_1 (str): 입력날짜1 (공백)
            fid_input_hour_1 (str): 입력시간1 (공백)
            fid_rank_sort_cls_code (str): 순위정렬구분코드 (공백)
            fid_input_srno (str): 입력일련번호 (공백)
            fid_cond_scr_div_code (str): 조건화면분류코드 (화면번호: 11801)

        Returns:
            BreakingNewsTitle: 해외속보(제목) 응답 객체
        """
        headers = {
            "tr_id": "FHKST01011801",
        }
        params = {
            "FID_NEWS_OFER_ENTP_CODE": fid_news_ofer_entp_code,
            "FID_COND_MRKT_CLS_CODE": fid_cond_mrkt_cls_code,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_TITL_CNTT": fid_titl_cntt,
            "FID_INPUT_DATE_1": fid_input_date_1,
            "FID_INPUT_HOUR_1": fid_input_hour_1,
            "FID_RANK_SORT_CLS_CODE": fid_rank_sort_cls_code,
            "FID_INPUT_SRNO": fid_input_srno,
            "FID_COND_SCR_DIV_CODE": fid_cond_scr_div_code,
        }
        response = self.client._get("/uapi/overseas-price/v1/quotations/brknews-title", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching breaking news title: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = BreakingNewsTitle.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)
