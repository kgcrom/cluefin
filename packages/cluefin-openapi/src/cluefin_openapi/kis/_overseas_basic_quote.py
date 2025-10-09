from cluefin_openapi.kis._client import Client
from cluefin_openapi.kis._overseas_basic_quote_types import (
    ConclusionTrend,
    CurrentPriceFirstQuote,
    IndexMinuteChart,
    ItemIndexExchangePeriodPrice,
    ProductBaseInfo,
    SearchByCondition,
    SectorCodes,
    SectorPrice,
    SettlementDate,
    StockCurrentPriceConclusion,
    StockCurrentPriceDetail,
    StockMinuteChart,
    StockPeriodQuote,
)


class BasicQuote:
    """해외주식 기본시세"""

    def __init__(self, client: Client):
        self.client = client

    def get_stock_current_price_detail(
        self,
        auth: str,
        excd: str,
        symb: str,
    ) -> StockCurrentPriceDetail:
        """
        해외주식 현재가상세

        Args:
            auth (str): 사용자권한정보 (공백입력)
            excd (str): 거래소명 (HKS: 홍콩, NYS: 뉴욕, NAS: 나스닥, AMS: 아멕스, TSE: 도쿄, SHS: 상해, SZS: 심천, SHI: 상해지수, SZI: 심천지수, HSX: 호치민, HNX: 하노이, BAY: 뉴욕(주간), BAQ: 나스닥(주간), BAA: 아멕스(주간))
            symb (str): 종목코드

        Returns:
            StockCurrentPriceDetail: 해외주식 현재가상세 응답 객체
        """
        headers = {
            "tr_id": "HHDFS76200200",
        }
        params = {
            "AUTH": auth,
            "EXCD": excd,
            "SYMB": symb,
        }
        response = self.client._get("/uapi/overseas-price/v1/quotations/price-detail", headers=headers, params=params)
        return StockCurrentPriceDetail.model_validate(response.json())

    def get_current_price_first_quote(
        self,
        excd: str,
        symb: str,
        auth: str = "",
    ) -> CurrentPriceFirstQuote:
        """
        해외주식 현재가 1호가

        Args:
            excd (str): 거래소코드 (NYS: 뉴욕, NAS: 나스닥, AMS: 아멕스, HKS: 홍콩, SHS: 상해, SZS: 심천, HSX: 호치민, HNX: 하노이, TSE: 도쿄, BAY: 뉴욕(주간), BAQ: 나스닥(주간), BAA: 아멕스(주간))
            symb (str): 종목코드 (예: TSLA)
            auth (str): 사용자권한정보 (공백)

        Returns:
            CurrentPriceFirstQuote: 해외주식 현재가 1호가 응답 객체
        """
        headers = {
            "tr_id": "HHDFS76200100",
        }
        params = {
            "AUTH": "",
            "EXCD": excd,
            "SYMB": symb,
        }
        response = self.client._get(
            "/uapi/overseas-price/v1/quotations/inquire-asking-price", headers=headers, params=params
        )
        return CurrentPriceFirstQuote.model_validate(response.json())

    def get_stock_current_price_conclusion(
        self,
        auth: str,
        excd: str,
        symb: str,
    ) -> StockCurrentPriceConclusion:
        """
        해외주식 현재체결가

        Args:
            auth (str): 사용자권한정보 ("" Null 값 설정)
            excd (str): 거래소코드 (HKS: 홍콩, NYS: 뉴욕, NAS: 나스닥, AMS: 아멕스, TSE: 도쿄, SHS: 상해, SZS: 심천, SHI: 상해지수, SZI: 심천지수, HSX: 호치민, HNX: 하노이, BAY: 뉴욕(주간), BAQ: 나스닥(주간), BAA: 아멕스(주간))
            symb (str): 종목코드

        Returns:
            StockCurrentPriceConclusion: 해외주식 현재체결가 응답 객체
        """
        headers = {
            "tr_id": "HHDFS00000300",
        }
        params = {
            "AUTH": auth,
            "EXCD": excd,
            "SYMB": symb,
        }
        response = self.client._get("/uapi/overseas-price/v1/quotations/price", headers=headers, params=params)
        return StockCurrentPriceConclusion.model_validate(response.json())

    def get_conclusion_trend(
        self,
        excd: str,
        auth: str,
        keyb: str,
        tday: str,
        symb: str,
    ) -> ConclusionTrend:
        """
        해외주식 체결추이

        Args:
            excd (str): 거래소명 (NYS: 뉴욕, NAS: 나스닥, AMS: 아멕스, HKS: 홍콩, SHS: 상해, SZS: 심천, HSX: 호치민, HNX: 하노이, TSE: 도쿄)
            auth (str): 사용자권한정보 (공백)
            keyb (str): NEXT KEY BUFF (공백)
            tday (str): 당일전일구분 (0: 전일, 1: 당일)
            symb (str): 종목코드 (해외종목코드)

        Returns:
            ConclusionTrend: 해외주식 체결추이 응답 객체
        """
        headers = {
            "tr_id": "HHDFS76200300",
        }
        params = {
            "EXCD": excd,
            "AUTH": auth,
            "KEYB": keyb,
            "TDAY": tday,
            "SYMB": symb,
        }
        response = self.client._get("/uapi/overseas-price/v1/quotations/inquire-ccnl", headers=headers, params=params)
        return ConclusionTrend.model_validate(response.json())

    def get_stock_minute_chart(
        self,
        auth: str,
        excd: str,
        symb: str,
        nmin: str,
        pinc: str,
        next: str,
        nrec: str,
        fill: str,
        keyb: str,
    ) -> StockMinuteChart:
        """
        해외주식분봉조회

        Args:
            auth (str): 사용자권한정보 ("" 공백으로 입력)
            excd (str): 거래소코드 (NYS: 뉴욕, NAS: 나스닥, AMS: 아멕스, HKS: 홍콩, SHS: 상해, SZS: 심천, HSX: 호치민, HNX: 하노이, TSE: 도쿄, BAY: 뉴욕(주간), BAQ: 나스닥(주간), BAA: 아멕스(주간), ※ 주간거래는 최대 1일치 분봉만 조회 가능)
            symb (str): 종목코드 (예: TSLA)
            nmin (str): 분갭 (분단위, 1: 1분봉, 2: 2분봉, ...)
            pinc (str): 전일포함여부 (0: 당일, 1: 전일포함, ※ 다음조회 시 반드시 "1"로 입력)
            next (str): 다음여부 (처음조회 시 "" 공백 입력, 다음조회 시 "1" 입력)
            nrec (str): 요청갯수 (레코드요청갯수, 최대 120)
            fill (str): 미체결채움구분 ("" 공백으로 입력)
            keyb (str): NEXT KEY BUFF (처음 조회 시 "" 공백 입력, 다음 조회 시 이전 조회 결과의 마지막 분봉 데이터를 이용하여 1분 전 혹은 n분 전의 시간을 입력, 형식: YYYYMMDDHHMMSS, 예: 20241014140100)

        Returns:
            StockMinuteChart: 해외주식분봉조회 응답 객체
        """
        headers = {
            "tr_id": "HHDFS76950200",
        }
        params = {
            "AUTH": auth,
            "EXCD": excd,
            "SYMB": symb,
            "NMIN": nmin,
            "PINC": pinc,
            "NEXT": next,
            "NREC": nrec,
            "FILL": fill,
            "KEYB": keyb,
        }
        response = self.client._get(
            "/uapi/overseas-price/v1/quotations/inquire-time-itemchartprice", headers=headers, params=params
        )
        return StockMinuteChart.model_validate(response.json())

    def get_index_minute_chart(
        self,
        fid_cond_mrkt_div_code: str,
        fid_input_iscd: str,
        fid_hour_cls_code: str,
        fid_pw_data_incu_yn: str,
    ) -> IndexMinuteChart:
        """
        해외지수분봉조회

        Args:
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드 (N: 해외지수, X: 환율, KX: 원화환율)
            fid_input_iscd (str): 입력 종목코드 (종목번호, 예: TSLA)
            fid_hour_cls_code (str): 시간 구분 코드 (0: 정규장, 1: 시간외)
            fid_pw_data_incu_yn (str): 과거 데이터 포함 여부 (Y/N)

        Returns:
            IndexMinuteChart: 해외지수분봉조회 응답 객체
        """
        headers = {
            "tr_id": "FHKST03030200",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_HOUR_CLS_CODE": fid_hour_cls_code,
            "FID_PW_DATA_INCU_YN": fid_pw_data_incu_yn,
        }
        response = self.client._get(
            "/uapi/overseas-price/v1/quotations/inquire-time-indexchartprice", headers=headers, params=params
        )
        return IndexMinuteChart.model_validate(response.json())

    def get_stock_period_quote(
        self,
        auth: str,
        excd: str,
        symb: str,
        gubn: str,
        bymd: str,
        modp: str,
        keyb: str = "",
    ) -> StockPeriodQuote:
        """
        해외주식 기간별시세

        Args:
            auth (str): 사용자권한정보 ("" Null 값 설정)
            excd (str): 거래소코드 (HKS: 홍콩, NYS: 뉴욕, NAS: 나스닥, AMS: 아멕스, TSE: 도쿄, SHS: 상해, SZS: 심천, SHI: 상해지수, SZI: 심천지수, HSX: 호치민, HNX: 하노이)
            symb (str): 종목코드 (예: TSLA)
            gubn (str): 일/주/월구분 (0: 일, 1: 주, 2: 월)
            bymd (str): 조회기준일자 (YYYYMMDD, ※ 공란 설정 시 기준일 오늘 날짜로 설정)
            modp (str): 수정주가반영여부 (0: 미반영, 1: 반영)
            keyb (str): NEXT KEY BUFF (응답시 다음값이 있으면 값이 셋팅되어 있으므로 다음 조회시 응답값 그대로 셋팅)

        Returns:
            StockPeriodQuote: 해외주식 기간별시세 응답 객체
        """
        headers = {
            "tr_id": "HHDFS76240000",
        }
        params = {
            "AUTH": auth,
            "EXCD": excd,
            "SYMB": symb,
            "GUBN": gubn,
            "BYMD": bymd,
            "MODP": modp,
            "KEYB": keyb,
        }
        response = self.client._get("/uapi/overseas-price/v1/quotations/dailyprice", headers=headers, params=params)
        return StockPeriodQuote.model_validate(response.json())

    def get_item_index_exchange_period_price(
        self,
        fid_cond_mrkt_div_code: str,
        fid_input_iscd: str,
        fid_input_date_1: str,
        fid_input_date_2: str,
        fid_period_div_code: str,
    ) -> ItemIndexExchangePeriodPrice:
        """
        해외주식 종목/지수/환율기간별시세(일/주/월/년)

        Args:
            fid_cond_mrkt_div_code (str): FID 조건 시장 분류 코드 (N: 해외지수, X: 환율, I: 국채, S: 금선물)
            fid_input_iscd (str): FID 입력 종목코드 (종목코드, ※ 해외주식 마스터 코드 참조, 해당 API로 미국주식 조회 시 다우30, 나스닥100, S&P500 종목만 조회 가능)
            fid_input_date_1 (str): FID 입력 날짜1 (시작일자 YYYYMMDD)
            fid_input_date_2 (str): FID 입력 날짜2 (종료일자 YYYYMMDD)
            fid_period_div_code (str): FID 기간 분류 코드 (D: 일, W: 주, M: 월, Y: 년)

        Returns:
            ItemIndexExchangePeriodPrice: 해외주식 종목/지수/환율기간별시세(일/주/월/년) 응답 객체
        """
        headers = {
            "tr_id": "FHKST03030100",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_INPUT_DATE_1": fid_input_date_1,
            "FID_INPUT_DATE_2": fid_input_date_2,
            "FID_PERIOD_DIV_CODE": fid_period_div_code,
        }
        response = self.client._get(
            "/uapi/overseas-price/v1/quotations/inquire-daily-chartprice", headers=headers, params=params
        )
        return ItemIndexExchangePeriodPrice.model_validate(response.json())

    def search_by_condition(
        self,
        auth: str,
        excd: str,
        co_yn_pricecur: str = "",
        co_st_pricecur: str = "",
        co_en_pricecur: str = "",
        co_yn_rate: str = "",
        co_st_rate: str = "",
        co_en_rate: str = "",
        co_yn_valx: str = "",
        co_st_valx: str = "",
        co_en_valx: str = "",
        co_yn_shar: str = "",
        co_st_shar: str = "",
        co_en_shar: str = "",
        co_yn_volume: str = "",
        co_st_volume: str = "",
        co_en_volume: str = "",
        co_yn_amt: str = "",
        co_st_amt: str = "",
        co_en_amt: str = "",
        co_yn_eps: str = "",
        co_st_eps: str = "",
        co_en_eps: str = "",
        co_yn_per: str = "",
        co_st_per: str = "",
        co_en_per: str = "",
        keyb: str = "",
    ) -> SearchByCondition:
        """
        해외주식조건검색

        Args:
            auth (str): 사용자권한정보 ("" Null 값 설정)
            excd (str): 거래소코드 (NYS: 뉴욕, NAS: 나스닥, AMS: 아멕스, HKS: 홍콩, SHS: 상해, SZS: 심천, HSX: 호치민, HNX: 하노이, TSE: 도쿄)
            co_yn_pricecur (str): 현재가선택조건 (해당조건 사용시 1, 미사용시 필수항목아님)
            co_st_pricecur (str): 현재가시작범위가 (단위: 각국통화 JPY, USD, HKD, CNY, VND)
            co_en_pricecur (str): 현재가끝범위가 (단위: 각국통화 JPY, USD, HKD, CNY, VND)
            co_yn_rate (str): 등락율선택조건 (해당조건 사용시 1, 미사용시 필수항목아님)
            co_st_rate (str): 등락율시작율 (%)
            co_en_rate (str): 등락율끝율 (%)
            co_yn_valx (str): 시가총액선택조건 (해당조건 사용시 1, 미사용시 필수항목아님)
            co_st_valx (str): 시가총액시작액 (단위: 천)
            co_en_valx (str): 시가총액끝액 (단위: 천)
            co_yn_shar (str): 발행주식수선택조건 (해당조건 사용시 1, 미사용시 필수항목아님)
            co_st_shar (str): 발행주식시작수 (단위: 천)
            co_en_shar (str): 발행주식끝수 (단위: 천)
            co_yn_volume (str): 거래량선택조건 (해당조건 사용시 1, 미사용시 필수항목아님)
            co_st_volume (str): 거래량시작량 (단위: 주)
            co_en_volume (str): 거래량끝량 (단위: 주)
            co_yn_amt (str): 거래대금선택조건 (해당조건 사용시 1, 미사용시 필수항목아님)
            co_st_amt (str): 거래대금시작금 (단위: 천)
            co_en_amt (str): 거래대금끝금 (단위: 천)
            co_yn_eps (str): EPS선택조건 (해당조건 사용시 1, 미사용시 필수항목아님)
            co_st_eps (str): EPS시작
            co_en_eps (str): EPS끝
            co_yn_per (str): PER선택조건 (해당조건 사용시 1, 미사용시 필수항목아님)
            co_st_per (str): PER시작
            co_en_per (str): PER끝
            keyb (str): NEXT KEY BUFF ("" 공백 입력)

        Returns:
            SearchByCondition: 해외주식조건검색 응답 객체
        """
        headers = {
            "tr_id": "HHDFS76410000",
        }
        params = {
            "AUTH": auth,
            "EXCD": excd,
            "CO_YN_PRICECUR": co_yn_pricecur,
            "CO_ST_PRICECUR": co_st_pricecur,
            "CO_EN_PRICECUR": co_en_pricecur,
            "CO_YN_RATE": co_yn_rate,
            "CO_ST_RATE": co_st_rate,
            "CO_EN_RATE": co_en_rate,
            "CO_YN_VALX": co_yn_valx,
            "CO_ST_VALX": co_st_valx,
            "CO_EN_VALX": co_en_valx,
            "CO_YN_SHAR": co_yn_shar,
            "CO_ST_SHAR": co_st_shar,
            "CO_EN_SHAR": co_en_shar,
            "CO_YN_VOLUME": co_yn_volume,
            "CO_ST_VOLUME": co_st_volume,
            "CO_EN_VOLUME": co_en_volume,
            "CO_YN_AMT": co_yn_amt,
            "CO_ST_AMT": co_st_amt,
            "CO_EN_AMT": co_en_amt,
            "CO_YN_EPS": co_yn_eps,
            "CO_ST_EPS": co_st_eps,
            "CO_EN_EPS": co_en_eps,
            "CO_YN_PER": co_yn_per,
            "CO_ST_PER": co_st_per,
            "CO_EN_PER": co_en_per,
            "KEYB": keyb,
        }
        response = self.client._get("/uapi/overseas-price/v1/quotations/inquire-search", headers=headers, params=params)
        return SearchByCondition.model_validate(response.json())

    def get_settlement_date(
        self,
        trad_dt: str,
        ctx_area_nk: str,
        ctx_area_fk: str,
    ) -> SettlementDate:
        """
        해외결제일자조회

        Args:
            trad_dt (str): 기준일자 (YYYYMMDD)
            ctx_area_nk (str): 연속조회키 (공백으로 입력)
            ctx_area_fk (str): 연속조회검색조건 (공백으로 입력)

        Returns:
            SettlementDate: 해외결제일자조회 응답 객체
        """
        headers = {
            "tr_id": "CTOS5011R",
        }
        params = {
            "TRAD_DT": trad_dt,
            "CTX_AREA_NK": ctx_area_nk,
            "CTX_AREA_FK": ctx_area_fk,
        }
        response = self.client._get(
            "/uapi/overseas-stock/v1/quotations/countries-holiday", headers=headers, params=params
        )
        return SettlementDate.model_validate(response.json())

    def get_product_base_info(
        self,
        prdt_type_cd: str,
        pdno: str,
    ) -> ProductBaseInfo:
        """
        해외주식 상품기본정보

        Args:
            prdt_type_cd (str): 상품유형코드 (512: 미국 나스닥, 513: 미국 뉴욕, 529: 미국 아멕스, 515: 일본, 501: 홍콩, 543: 홍콩CNY, 558: 홍콩USD, 507: 베트남 하노이, 508: 베트남 호치민, 551: 중국 상해A, 552: 중국 심천A)
            pdno (str): 상품번호 (예: AAPL)

        Returns:
            ProductBaseInfo: 해외주식 상품기본정보 응답 객체
        """
        headers = {
            "tr_id": "CTPF1702R",
        }
        params = {
            "PRDT_TYPE_CD": prdt_type_cd,
            "PDNO": pdno,
        }
        response = self.client._get("/uapi/overseas-price/v1/quotations/search-info", headers=headers, params=params)
        return ProductBaseInfo.model_validate(response.json())

    def get_sector_price(
        self,
        keyb: str,
        auth: str,
        excd: str,
        icod: str,
        vol_rang: str,
    ) -> SectorPrice:
        """
        해외주식 업종별시세

        Args:
            keyb (str): NEXT KEY BUFF (공백)
            auth (str): 사용자권한정보 (공백)
            excd (str): 거래소코드 (NYS: 뉴욕, NAS: 나스닥, AMS: 아멕스, HKS: 홍콩, SHS: 상해, SZS: 심천, HSX: 호치민, HNX: 하노이, TSE: 도쿄)
            icod (str): 업종코드 (업종코드별조회 HHDFS76370100 를 통해 확인)
            vol_rang (str): 거래량조건 (0: 전체, 1: 1백주이상, 2: 1천주이상, 3: 1만주이상, 4: 10만주이상, 5: 100만주이상, 6: 1000만주이상)

        Returns:
            SectorPrice: 해외주식 업종별시세 응답 객체
        """
        headers = {
            "tr_id": "HHDFS76370000",
        }
        params = {
            "KEYB": keyb,
            "AUTH": auth,
            "EXCD": excd,
            "ICOD": icod,
            "VOL_RANG": vol_rang,
        }
        response = self.client._get("/uapi/overseas-price/v1/quotations/industry-theme", headers=headers, params=params)
        return SectorPrice.model_validate(response.json())

    def get_sector_codes(
        self,
        auth: str,
        excd: str,
    ) -> SectorCodes:
        """
        해외주식 업종별코드조회

        Args:
            auth (str): 사용자권한정보 (공백)
            excd (str): 거래소코드 (NYS: 뉴욕, NAS: 나스닥, AMS: 아멕스, HKS: 홍콩, SHS: 상해, SZS: 심천, HSX: 호치민, HNX: 하노이, TSE: 도쿄)

        Returns:
            SectorCodes: 해외주식 업종별코드조회 응답 객체
        """
        headers = {
            "tr_id": "HHDFS76370100",
        }
        params = {
            "AUTH": auth,
            "EXCD": excd,
        }
        response = self.client._get("/uapi/overseas-price/v1/quotations/industry-price", headers=headers, params=params)
        return SectorCodes.model_validate(response.json())
