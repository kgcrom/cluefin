from cluefin_openapi.kis._domestic_stock_info_types import (
    BalanceSheet,
    EstimatedEarnings,
    FinancialRatio,
    GrowthRatio,
    IncomeStatement,
    InvestmentOpinion,
    InvestmentOpinionByBrokerage,
    KsdCapitalReductionSchedule,
    KsdDepositSchedule,
    KsdDividendDecision,
    KsdForfeitedShareSchedule,
    KsdIpoSubscriptionSchedule,
    KsdListingInfoSchedule,
    KsdMergerSplitDecision,
    KsdPaidInCapitalIncreaseSchedule,
    KsdParValueChangeDecision,
    KsdShareholderMeetingSchedule,
    KsdStockDividendDecision,
    KsdStockDividendSchedule,
    MarginTradableStocks,
    OtherKeyRatio,
    ProductBasicInfo,
    ProfitabilityRatio,
    StabilityRatio,
    StockBasicInfo,
    StockLoanableList,
)
from cluefin_openapi.kis._http_client import HttpClient
from cluefin_openapi.kis._model import KisHttpHeader, KisHttpResponse


class DomesticStockInfo:
    """국내주식 종목정보"""

    def __init__(self, client: HttpClient):
        self.client = client

    def get_product_basic_info(
        self,
        pdno: str,
        prdt_type_cd: str,
    ) -> KisHttpResponse[ProductBasicInfo]:
        """
        상품기본조회

        Args:
            pdno (str): 상품번호 (예: 주식(하이닉스) : 000660 (코드 : 300), 선물(101S12) : KR4101SC0009 (코드 : 301), 미국(AAPL) : AAPL (코드 : 512))
            prdt_type_cd (str): 상품유형코드 (300: 주식, 301: 선물옵션, 302: 채권, 512: 미국 나스닥, 513: 미국 뉴욕, 529: 미국 아멕스, 515: 일본, 501: 홍콩, 543: 홍콩CNY, 558: 홍콩USD, 507: 베트남 하노이, 508: 베트남 호치민, 551: 중국 상해A, 552: 중국 심천A)

        Returns:
            KisHttpResponse[ProductBasicInfo]: 상품기본조회 응답 객체
        """
        headers = {
            "tr_id": "CTPF1604R",
        }
        params = {
            "PDNO": pdno,
            "PRDT_TYPE_CD": prdt_type_cd,
        }
        response = self.client._get("/uapi/domestic-stock/v1/quotations/search-info", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching product basic info: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = ProductBasicInfo.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_stock_basic_info(
        self,
        prdt_type_cd: str,
        pdno: str,
    ) -> KisHttpResponse[StockBasicInfo]:
        """
        주식기본조회

        Args:
            prdt_type_cd (str): 상품유형코드 (300: 주식, ETF, ETN, ELW, 301: 선물옵션, 302: 채권, 306: ELS)
            pdno (str): 상품번호 (종목번호 6자리, ETN의 경우 Q로 시작, 예: Q500001)

        Returns:
            KisHttpResponse[StockBasicInfo]: 주식기본조회 응답 객체
        """
        headers = {
            "tr_id": "CTPF1002R",
        }
        params = {
            "PRDT_TYPE_CD": prdt_type_cd,
            "PDNO": pdno,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/search-stock-info", headers=headers, params=params
        )
        if response.status_code != 200:
            raise Exception(f"Error fetching stock basic info: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockBasicInfo.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_balance_sheet(
        self,
        fid_div_cls_code: str,
        fid_cond_mrkt_div_code: str,
        fid_input_iscd: str,
    ) -> KisHttpResponse[BalanceSheet]:
        """
        국내주식 대차대조표

        Args:
            fid_div_cls_code (str): 분류 구분 코드 (0: 년, 1: 분기)
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드 (J)
            fid_input_iscd (str): 입력 종목코드 (예: 000660)

        Returns:
            KisHttpResponse[BalanceSheet]: 국내주식 대차대조표 응답 객체
        """
        headers = {
            "tr_id": "FHKST66430100",
        }
        params = {
            "FID_DIV_CLS_CODE": fid_div_cls_code,
            "fid_cond_mrkt_div_code": fid_cond_mrkt_div_code,
            "fid_input_iscd": fid_input_iscd,
        }
        response = self.client._get("/uapi/domestic-stock/v1/finance/balance-sheet", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching balance sheet: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = BalanceSheet.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_income_statement(
        self,
        fid_div_cls_code: str,
        fid_cond_mrkt_div_code: str,
        fid_input_iscd: str,
    ) -> KisHttpResponse[IncomeStatement]:
        """
        국내주식 손익계산서

        Args:
            fid_div_cls_code (str): 분류 구분 코드 (0: 년, 1: 분기, 분기데이터는 연단위 누적합산)
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드 (J)
            fid_input_iscd (str): 입력 종목코드 (예: 000660)

        Returns:
            KisHttpResponse[IncomeStatement]: 국내주식 손익계산서 응답 객체
        """
        headers = {
            "tr_id": "FHKST66430200",
        }
        params = {
            "FID_DIV_CLS_CODE": fid_div_cls_code,
            "fid_cond_mrkt_div_code": fid_cond_mrkt_div_code,
            "fid_input_iscd": fid_input_iscd,
        }
        response = self.client._get("/uapi/domestic-stock/v1/finance/income-statement", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching income statement: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = IncomeStatement.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_financial_ratio(
        self,
        fid_div_cls_code: str,
        fid_cond_mrkt_div_code: str,
        fid_input_iscd: str,
    ) -> KisHttpResponse[FinancialRatio]:
        """
        국내주식 재무비율

        Args:
            fid_div_cls_code (str): 분류 구분 코드 (0: 년, 1: 분기)
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드 (J)
            fid_input_iscd (str): 입력 종목코드 (예: 000660)

        Returns:
            KisHttpResponse[FinancialRatio]: 국내주식 재무비율 응답 객체
        """
        headers = {
            "tr_id": "FHKST66430300",
        }
        params = {
            "FID_DIV_CLS_CODE": fid_div_cls_code,
            "fid_cond_mrkt_div_code": fid_cond_mrkt_div_code,
            "fid_input_iscd": fid_input_iscd,
        }
        response = self.client._get("/uapi/domestic-stock/v1/finance/financial-ratio", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching financial ratio: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = FinancialRatio.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_profitability_ratio(
        self,
        fid_input_iscd: str,
        fid_div_cls_code: str,
        fid_cond_mrkt_div_code: str,
    ) -> KisHttpResponse[ProfitabilityRatio]:
        """
        국내주식 수익성비율

        Args:
            fid_input_iscd (str): 입력 종목코드 (예: 000660)
            fid_div_cls_code (str): 분류 구분 코드 (0: 년, 1: 분기)
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드 (J)

        Returns:
            KisHttpResponse[ProfitabilityRatio]: 국내주식 수익성비율 응답 객체
        """
        headers = {
            "tr_id": "FHKST66430400",
        }
        params = {
            "fid_input_iscd": fid_input_iscd,
            "FID_DIV_CLS_CODE": fid_div_cls_code,
            "fid_cond_mrkt_div_code": fid_cond_mrkt_div_code,
        }
        response = self.client._get("/uapi/domestic-stock/v1/finance/profit-ratio", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching profitability ratio: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = ProfitabilityRatio.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_other_key_ratio(
        self,
        fid_input_iscd: str,
        fid_div_cls_code: str,
        fid_cond_mrkt_div_code: str,
    ) -> KisHttpResponse[OtherKeyRatio]:
        """
        국내주식 기타주요비율

        Args:
            fid_input_iscd (str): 입력 종목코드 (예: 000660)
            fid_div_cls_code (str): 분류 구분 코드 (0: 년, 1: 분기)
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드 (J)

        Returns:
            KisHttpResponse[OtherKeyRatio]: 국내주식 기타주요비율 응답 객체
        """
        headers = {
            "tr_id": "FHKST66430500",
        }
        params = {
            "fid_input_iscd": fid_input_iscd,
            "fid_div_cls_code": fid_div_cls_code,
            "fid_cond_mrkt_div_code": fid_cond_mrkt_div_code,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/finance/other-major-ratios", headers=headers, params=params
        )
        if response.status_code != 200:
            raise Exception(f"Error fetching other key ratio: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = OtherKeyRatio.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_stability_ratio(
        self,
        fid_input_iscd: str,
        fid_div_cls_code: str,
        fid_cond_mrkt_div_code: str,
    ) -> KisHttpResponse[StabilityRatio]:
        """
        국내주식 안정성비율

        Args:
            fid_input_iscd (str): 입력 종목코드 (예: 000660)
            fid_div_cls_code (str): 분류 구분 코드 (0: 년, 1: 분기)
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드 (J)

        Returns:
            KisHttpResponse[StabilityRatio]: 국내주식 안정성비율 응답 객체
        """
        headers = {
            "tr_id": "FHKST66430600",
        }
        params = {
            "fid_input_iscd": fid_input_iscd,
            "fid_div_cls_code": fid_div_cls_code,
            "fid_cond_mrkt_div_code": fid_cond_mrkt_div_code,
        }
        response = self.client._get("/uapi/domestic-stock/v1/finance/stability-ratio", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching stability ratio: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StabilityRatio.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_growth_ratio(
        self,
        fid_input_iscd: str,
        fid_div_cls_code: str,
        fid_cond_mrkt_div_code: str,
    ) -> KisHttpResponse[GrowthRatio]:
        """
        국내주식 성장성비율

        Args:
            fid_input_iscd (str): 입력 종목코드 (예: 000660)
            fid_div_cls_code (str): 분류 구분 코드 (0: 년, 1: 분기)
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드 (시장구분코드, 주식 J)

        Returns:
            KisHttpResponse[GrowthRatio]: 국내주식 성장성비율 응답 객체
        """
        headers = {
            "tr_id": "FHKST66430800",
        }
        params = {
            "fid_input_iscd": fid_input_iscd,
            "fid_div_cls_code": fid_div_cls_code,
            "fid_cond_mrkt_div_code": fid_cond_mrkt_div_code,
        }
        response = self.client._get("/uapi/domestic-stock/v1/finance/growth-ratio", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching growth ratio: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = GrowthRatio.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_margin_tradable_stocks(
        self,
        fid_rank_sort_cls_code: str,
        fid_slct_yn: str,
        fid_input_iscd: str,
        fid_cond_scr_div_code: str,
        fid_cond_mrkt_div_code: str,
    ) -> KisHttpResponse[MarginTradableStocks]:
        """
        국내주식 당사 신용가능종목

        Args:
            fid_rank_sort_cls_code (str): 순위 정렬 구분 코드 (0: 코드순, 1: 이름순)
            fid_slct_yn (str): 선택 여부 (0: 신용주문가능, 1: 신용주문불가)
            fid_input_iscd (str): 입력 종목코드 (0000: 전체, 0001: 거래소, 1001: 코스닥, 2001: 코스피200, 4001: KRX100)
            fid_cond_scr_div_code (str): 조건 화면 분류 코드 (Unique key: 20477)
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드 (시장구분코드, 주식 J)

        Returns:
            KisHttpResponse[MarginTradableStocks]: 국내주식 당사 신용가능종목 응답 객체
        """
        headers = {
            "tr_id": "FHPST04770000",
        }
        params = {
            "fid_rank_sort_cls_code": fid_rank_sort_cls_code,
            "fid_slct_yn": fid_slct_yn,
            "fid_input_iscd": fid_input_iscd,
            "fid_cond_scr_div_code": fid_cond_scr_div_code,
            "fid_cond_mrkt_div_code": fid_cond_mrkt_div_code,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/credit-by-company", headers=headers, params=params
        )
        if response.status_code != 200:
            raise Exception(f"Error fetching margin tradable stocks: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = MarginTradableStocks.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_ksd_dividend_decision(
        self,
        cts: str,
        gb1: str,
        f_dt: str,
        t_dt: str,
        sht_cd: str,
        high_gb: str,
    ) -> KisHttpResponse[KsdDividendDecision]:
        """
        예탁원정보(배당결정)

        Args:
            cts (str): CTS (공백)
            gb1 (str): 조회구분 (0: 배당전체, 1: 결산배당, 2: 중간배당)
            f_dt (str): 조회일자From (일자 ~, 예: 20231201)
            t_dt (str): 조회일자To (~ 일자, 예: 20240531)
            sht_cd (str): 종목코드 (공백: 전체, 특정종목 조회시: 종목코드)
            high_gb (str): 고배당여부 (공백)

        Returns:
            KisHttpResponse[KsdDividendDecision]: 예탁원정보(배당결정) 응답 객체
        """
        headers = {
            "tr_id": "HHKDB669102C0",
        }
        params = {
            "CTS": cts,
            "GB1": gb1,
            "F_DT": f_dt,
            "T_DT": t_dt,
            "SHT_CD": sht_cd,
            "HIGH_GB": high_gb,
        }
        response = self.client._get("/uapi/domestic-stock/v1/ksdinfo/dividend", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching ksd dividend decision: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = KsdDividendDecision.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_ksd_stock_dividend_decision(
        self,
        sht_cd: str,
        t_dt: str,
        f_dt: str,
        cts: str,
    ) -> KisHttpResponse[KsdStockDividendDecision]:
        """
        예탁원정보(주식배수청구결정)

        Args:
            sht_cd (str): 종목코드 (공백: 전체, 특정종목 조회시: 종목코드)
            t_dt (str): 조회일자To (~ 일자, 예: 20240531)
            f_dt (str): 조회일자From (일자 ~, 예: 20231201)
            cts (str): CTS (공백)

        Returns:
            KisHttpResponse[KsdStockDividendDecision]: 예탁원정보(주식배수청구결정) 응답 객체
        """
        headers = {
            "tr_id": "HHKDB669103C0",
        }
        params = {
            "SHT_CD": sht_cd,
            "T_DT": t_dt,
            "F_DT": f_dt,
            "CTS": cts,
        }
        response = self.client._get("/uapi/domestic-stock/v1/ksdinfo/purreq", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching ksd stock dividend decision: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = KsdStockDividendDecision.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_ksd_merger_split_decision(
        self,
        cts: str,
        f_dt: str,
        t_dt: str,
        sht_cd: str,
    ) -> KisHttpResponse[KsdMergerSplitDecision]:
        """
        예탁원정보(합병/분할결정)

        Args:
            cts (str): CTS (공백)
            f_dt (str): 조회일자From (일자 ~, 예: 20231201)
            t_dt (str): 조회일자To (~ 일자, 예: 20240531)
            sht_cd (str): 종목코드 (공백: 전체, 특정종목 조회시: 종목코드)

        Returns:
            KisHttpResponse[KsdMergerSplitDecision]: 예탁원정보(합병/분할결정) 응답 객체
        """
        headers = {
            "tr_id": "HHKDB669104C0",
        }
        params = {
            "CTS": cts,
            "F_DT": f_dt,
            "T_DT": t_dt,
            "SHT_CD": sht_cd,
        }
        response = self.client._get("/uapi/domestic-stock/v1/ksdinfo/merger-split", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching ksd merger split decision: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = KsdMergerSplitDecision.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_ksd_par_value_change_decision(
        self,
        sht_cd: str,
        cts: str,
        f_dt: str,
        t_dt: str,
        market_gb: str,
    ) -> KisHttpResponse[KsdParValueChangeDecision]:
        """
        예탁원정보(액면교체결정)

        Args:
            sht_cd (str): 종목코드 (공백: 전체, 특정종목 조회시: 종목코드)
            cts (str): CTS (공백)
            f_dt (str): 조회일자From (일자 ~, 예: 20231201)
            t_dt (str): 조회일자To (~ 일자, 예: 20240531)
            market_gb (str): 시장구분 (0: 전체, 1: 코스피, 2: 코스닥)

        Returns:
            KisHttpResponse[KsdParValueChangeDecision]: 예탁원정보(액면교체결정) 응답 객체
        """
        headers = {
            "tr_id": "HHKDB669105C0",
        }
        params = {
            "SHT_CD": sht_cd,
            "CTS": cts,
            "F_DT": f_dt,
            "T_DT": t_dt,
            "MARKET_GB": market_gb,
        }
        response = self.client._get("/uapi/domestic-stock/v1/ksdinfo/rev-split", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching ksd par value change decision: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = KsdParValueChangeDecision.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_ksd_capital_reduction_schedule(
        self,
        cts: str,
        f_dt: str,
        t_dt: str,
        sht_cd: str,
    ) -> KisHttpResponse[KsdCapitalReductionSchedule]:
        """
        예탁원정보(자본감소일정)

        Args:
            cts (str): CTS (공백)
            f_dt (str): 조회일자From (일자 ~, 예: 20231201)
            t_dt (str): 조회일자To (~ 일자, 예: 20240531)
            sht_cd (str): 종목코드 (공백: 전체, 특정종목 조회시: 종목코드)

        Returns:
            KisHttpResponse[KsdCapitalReductionSchedule]: 예탁원정보(자본감소일정) 응답 객체
        """
        headers = {
            "tr_id": "HHKDB669106C0",
        }
        params = {
            "CTS": cts,
            "F_DT": f_dt,
            "T_DT": t_dt,
            "SHT_CD": sht_cd,
        }
        response = self.client._get("/uapi/domestic-stock/v1/ksdinfo/cap-dcrs", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching ksd capital reduction schedule: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = KsdCapitalReductionSchedule.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_ksd_listing_info_schedule(
        self,
        sht_cd: str,
        t_dt: str,
        f_dt: str,
        cts: str,
    ) -> KisHttpResponse[KsdListingInfoSchedule]:
        """
        예탁원정보(상장정보일정)

        Args:
            sht_cd (str): 종목코드 (공백: 전체, 특정종목 조회시: 종목코드)
            t_dt (str): 조회일자To (~ 일자, 예: 20240531)
            f_dt (str): 조회일자From (일자 ~, 예: 20231201)
            cts (str): CTS (공백)

        Returns:
            KisHttpResponse[KsdListingInfoSchedule]: 예탁원정보(상장정보일정) 응답 객체
        """
        headers = {
            "tr_id": "HHKDB669107C0",
        }
        params = {
            "SHT_CD": sht_cd,
            "T_DT": t_dt,
            "F_DT": f_dt,
            "CTS": cts,
        }
        response = self.client._get("/uapi/domestic-stock/v1/ksdinfo/list-info", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching ksd listing info schedule: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = KsdListingInfoSchedule.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_ksd_ipo_subscription_schedule(
        self,
        sht_cd: str,
        cts: str,
        f_dt: str,
        t_dt: str,
    ) -> KisHttpResponse[KsdIpoSubscriptionSchedule]:
        """
        예탁원정보(공모주청약일정)

        Args:
            sht_cd (str): 종목코드 (공백: 전체, 특정종목 조회시: 종목코드)
            cts (str): CTS (공백)
            f_dt (str): 조회일자From (일자 ~, 예: 20231201)
            t_dt (str): 조회일자To (~ 일자, 예: 20240531)

        Returns:
            KisHttpResponse[KsdIpoSubscriptionSchedule]: 예탁원정보(공모주청약일정) 응답 객체
        """
        headers = {
            "tr_id": "HHKDB669108C0",
        }
        params = {
            "SHT_CD": sht_cd,
            "CTS": cts,
            "F_DT": f_dt,
            "T_DT": t_dt,
        }
        response = self.client._get("/uapi/domestic-stock/v1/ksdinfo/pub-offer", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching ksd ipo subscription schedule: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = KsdIpoSubscriptionSchedule.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_ksd_forfeited_share_schedule(
        self,
        sht_cd: str,
        t_dt: str,
        f_dt: str,
        cts: str,
    ) -> KisHttpResponse[KsdForfeitedShareSchedule]:
        """
        예탁원정보(실권주일정)

        Args:
            sht_cd (str): 종목코드 (공백: 전체, 특정종목 조회시: 종목코드)
            t_dt (str): 조회일자To (~ 일자, 예: 20240531)
            f_dt (str): 조회일자From (일자 ~, 예: 20231201)
            cts (str): CTS (공백)

        Returns:
            KisHttpResponse[KsdForfeitedShareSchedule]: 예탁원정보(실권주일정) 응답 객체
        """
        headers = {
            "tr_id": "HHKDB669109C0",
        }
        params = {
            "SHT_CD": sht_cd,
            "T_DT": t_dt,
            "F_DT": f_dt,
            "CTS": cts,
        }
        response = self.client._get("/uapi/domestic-stock/v1/ksdinfo/forfeit", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching ksd forfeited share schedule: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = KsdForfeitedShareSchedule.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_ksd_deposit_schedule(
        self,
        t_dt: str,
        sht_cd: str,
        f_dt: str,
        cts: str,
    ) -> KisHttpResponse[KsdDepositSchedule]:
        """
        예탁원정보(입무예치일정)

        Args:
            t_dt (str): 조회일자To (~ 일자, 예: 20240531)
            sht_cd (str): 종목코드 (공백: 전체, 특정종목 조회시: 종목코드)
            f_dt (str): 조회일자From (일자 ~, 예: 20231201)
            cts (str): CTS (공백)

        Returns:
            KisHttpResponse[KsdDepositSchedule]: 예탁원정보(입무예치일정) 응답 객체
        """
        headers = {
            "tr_id": "HHKDB669110C0",
        }
        params = {
            "T_DT": t_dt,
            "SHT_CD": sht_cd,
            "F_DT": f_dt,
            "CTS": cts,
        }
        response = self.client._get("/uapi/domestic-stock/v1/ksdinfo/mand-deposit", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching ksd deposit schedule: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = KsdDepositSchedule.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_ksd_paid_in_capital_increase_schedule(
        self,
        cts: str,
        gb1: str,
        f_dt: str,
        t_dt: str,
        sht_cd: str,
    ) -> KisHttpResponse[KsdPaidInCapitalIncreaseSchedule]:
        """
        예탁원정보(유상증자일정)

        Args:
            cts (str): CTS (공백)
            gb1 (str): 조회구분 (1: 청약일별, 2: 기준일별)
            f_dt (str): 조회일자From (일자 ~, 예: 20231201)
            t_dt (str): 조회일자To (~ 일자, 예: 20240531)
            sht_cd (str): 종목코드 (공백: 전체, 특정종목 조회시: 종목코드)

        Returns:
            KisHttpResponse[KsdPaidInCapitalIncreaseSchedule]: 예탁원정보(유상증자일정) 응답 객체
        """
        headers = {
            "tr_id": "HHKDB669100C0",
        }
        params = {
            "CTS": cts,
            "GB1": gb1,
            "F_DT": f_dt,
            "T_DT": t_dt,
            "SHT_CD": sht_cd,
        }
        response = self.client._get("/uapi/domestic-stock/v1/ksdinfo/paidin-capin", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching ksd paid in capital increase schedule: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = KsdPaidInCapitalIncreaseSchedule.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_ksd_stock_dividend_schedule(
        self,
        cts: str,
        f_dt: str,
        t_dt: str,
        sht_cd: str,
    ) -> KisHttpResponse[KsdStockDividendSchedule]:
        """
        예탁원정보(무상증자일정)

        Args:
            cts (str): CTS (공백)
            f_dt (str): 조회일자From (일자 ~, 예: 20231201)
            t_dt (str): 조회일자To (~ 일자, 예: 20240531)
            sht_cd (str): 종목코드 (공백: 전체, 특정종목 조회시: 종목코드)

        Returns:
            KisHttpResponse[KsdStockDividendSchedule]: 예탁원정보(무상증자일정) 응답 객체
        """
        headers = {
            "tr_id": "HHKDB669101C0",
        }
        params = {
            "CTS": cts,
            "F_DT": f_dt,
            "T_DT": t_dt,
            "SHT_CD": sht_cd,
        }
        response = self.client._get("/uapi/domestic-stock/v1/ksdinfo/bonus-issue", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching ksd stock dividend schedule: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = KsdStockDividendSchedule.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_ksd_shareholder_meeting_schedule(
        self,
        cts: str,
        f_dt: str,
        t_dt: str,
        sht_cd: str,
    ) -> KisHttpResponse[KsdShareholderMeetingSchedule]:
        """
        예탁원정보(주주총회일정)

        Args:
            cts (str): CTS (공백)
            f_dt (str): 조회일자From (일자 ~, 예: 20231201)
            t_dt (str): 조회일자To (~ 일자, 예: 20240531)
            sht_cd (str): 종목코드 (공백: 전체, 특정종목 조회시: 종목코드)

        Returns:
            KisHttpResponse[KsdShareholderMeetingSchedule]: 예탁원정보(주주총회일정) 응답 객체
        """
        headers = {
            "tr_id": "HHKDB669111C0",
        }
        params = {
            "CTS": cts,
            "F_DT": f_dt,
            "T_DT": t_dt,
            "SHT_CD": sht_cd,
        }
        response = self.client._get("/uapi/domestic-stock/v1/ksdinfo/sharehld-meet", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching ksd shareholder meeting schedule: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = KsdShareholderMeetingSchedule.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_estimated_earnings(
        self,
        sht_cd: str,
    ) -> KisHttpResponse[EstimatedEarnings]:
        """
        국내주식 종목추정실적

        Args:
            sht_cd (str): 종목코드 (예: 265520)

        Returns:
            KisHttpResponse[EstimatedEarnings]: 국내주식 종목추정실적 응답 객체
        """
        headers = {
            "tr_id": "HHKST668300C0",
        }
        params = {
            "SHT_CD": sht_cd,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/estimate-perform", headers=headers, params=params
        )
        if response.status_code != 200:
            raise Exception(f"Error fetching estimated earnings: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = EstimatedEarnings.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_stock_loanable_list(
        self,
        excg_dvsn_cd: str,
        pdno: str,
        thco_stln_psbl_yn: str,
        inqr_dvsn_1: str,
        ctx_area_fk200: str,
        ctx_area_nk100: str,
    ) -> KisHttpResponse[StockLoanableList]:
        """
        당사 대주가능 종목

        Args:
            excg_dvsn_cd (str): 거래소구분코드 (00: 전체, 02: 거래소, 03: 코스닥)
            pdno (str): 상품번호 (공백: 전체조회, 종목코드 입력 시 해당종목만 조회)
            thco_stln_psbl_yn (str): 당사대주가능여부 (Y)
            inqr_dvsn_1 (str): 조회구분1 (0: 전체조회, 1: 종목코드순 정렬)
            ctx_area_fk200 (str): 연속조회검색조건200 (미입력, 다음조회 불가)
            ctx_area_nk100 (str): 연속조회키100 (미입력, 다음조회 불가)

        Returns:
            KisHttpResponse[StockLoanableList]: 당사 대주가능 종목 응답 객체
        """
        headers = {
            "tr_id": "CTSC2702R",
        }
        params = {
            "EXCG_DVSN_CD": excg_dvsn_cd,
            "PDNO": pdno,
            "THCO_STLN_PSBL_YN": thco_stln_psbl_yn,
            "INQR_DVSN_1": inqr_dvsn_1,
            "CTX_AREA_FK200": ctx_area_fk200,
            "CTX_AREA_NK100": ctx_area_nk100,
        }
        response = self.client._get(
            "/uapi/domestic-stock/v1/quotations/lendable-by-company", headers=headers, params=params
        )
        if response.status_code != 200:
            raise Exception(f"Error fetching stock loanable list: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = StockLoanableList.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_investment_opinion(
        self,
        fid_cond_mrkt_div_code: str,
        fid_cond_scr_div_code: str,
        fid_input_iscd: str,
        fid_input_date_1: str,
        fid_input_date_2: str,
    ) -> KisHttpResponse[InvestmentOpinion]:
        """
        국내주식 종목투자의견

        Args:
            fid_cond_mrkt_div_code (str): 조건시장분류코드 (J: 시장 구분 코드)
            fid_cond_scr_div_code (str): 조건화면분류코드 (16633: Primary key)
            fid_input_iscd (str): 입력종목코드 (종목코드, 예: 005930(삼성전자))
            fid_input_date_1 (str): 입력날짜1 (이후 ~, 예: 0020231113)
            fid_input_date_2 (str): 입력날짜2 (~ 이전, 예: 0020240513)

        Returns:
            KisHttpResponse[InvestmentOpinion]: 국내주식 종목투자의견 응답 객체
        """
        headers = {
            "tr_id": "FHKST663300C0",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_COND_SCR_DIV_CODE": fid_cond_scr_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_INPUT_DATE_1": fid_input_date_1,
            "FID_INPUT_DATE_2": fid_input_date_2,
        }
        response = self.client._get("/uapi/domestic-stock/v1/quotations/invest-opinion", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching investment opinion: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = InvestmentOpinion.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)

    def get_investment_opinion_by_brokerage(
        self,
        fid_cond_mrkt_div_code: str,
        fid_cond_scr_div_code: str,
        fid_input_iscd: str,
        fid_div_cls_code: str,
        fid_input_date_1: str,
        fid_input_date_2: str,
    ) -> KisHttpResponse[InvestmentOpinionByBrokerage]:
        """
        국내주식 증권사별 투자의견

        Args:
            fid_cond_mrkt_div_code (str): 조건시장분류코드 (J: 시장 구분 코드)
            fid_cond_scr_div_code (str): 조건화면분류코드 (16634: Primary key)
            fid_input_iscd (str): 입력종목코드 (회원사코드, kis developers 포탈 사이트 포럼 -> FAQ -> 종목정보 다운로드(국내) 참조)
            fid_div_cls_code (str): 분류구분코드 (전체: 0, 매수: 1, 중립: 2, 매도: 3)
            fid_input_date_1 (str): 입력날짜1 (이후 ~, 예: 0020231113)
            fid_input_date_2 (str): 입력날짜2 (~ 이전, 예: 0020240513)

        Returns:
            KisHttpResponse[InvestmentOpinionByBrokerage]: 국내주식 증권사별 투자의견 응답 객체
        """
        headers = {
            "tr_id": "FHKST663400C0",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_COND_SCR_DIV_CODE": fid_cond_scr_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
            "FID_DIV_CLS_CODE": fid_div_cls_code,
            "FID_INPUT_DATE_1": fid_input_date_1,
            "FID_INPUT_DATE_2": fid_input_date_2,
        }
        response = self.client._get("/uapi/domestic-stock/v1/quotations/invest-opbysec", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching investment opinion by brokerage: {response.text}")
        header = KisHttpHeader.model_validate(response.headers)
        body = InvestmentOpinionByBrokerage.model_validate(response.json())
        return KisHttpResponse(header=header, body=body)
