from cluefin_openapi.kis._client import Client


class DomesticBasicQuote:
    """국내주식 기본시세"""

    def __init__(self, client: Client):
        self.client = client

    def get_stock_current_price(self):
        """주식현재가 시세"""
        pass

    def get_stock_current_price_2(self):
        """주식현재가 시세2"""
        pass

    def get_stock_current_price_detail(self):
        """주식현재가 체결"""
        pass

    def get_stock_current_price_daily(self):
        """주식현재가 일자별"""
        pass

    def get_stock_current_price_hoga_expected_conclusion(self):
        """주식현재가 호가/예상체결"""
        pass

    def get_stock_current_price_investor(self):
        """주식현재가 투자자"""
        pass

    def get_stock_current_price_member(self):
        """주식현재가 회원사"""
        pass

    def get_domestic_stock_period_quote(self):
        """국내주식기간별시세(일/주/월/년)"""
        pass

    def get_stock_daily_analysis_inquiry(self):
        """주식당일분봉조회"""
        pass

    def get_stock_daily_analysis_inquiry_by_date(self):
        """주식일별분봉조회"""
        pass

    def get_stock_current_price_daily_time_summary(self):
        """주식현재가 당일시간대별체결"""
        pass

    def get_stock_current_price_time_daily_price_by_date(self):
        """주식현재가 시간외일자별주가"""
        pass

    def get_stock_current_price_time_daily_conclusion(self):
        """주식현재가 시간외시간별체결"""
        pass

    def get_domestic_stock_time_current_price(self):
        """국내주식 시간외현재가"""
        pass

    def get_domestic_stock_time_hoga(self):
        """국내주식 시간외호가"""
        pass

    def get_domestic_stock_market_cap_expected_conclusion(self):
        """국내주식 장마감 예상체결가"""
        pass

    def get_etf_etn_current_price(self):
        """ETF/ETN 현재가"""
        pass

    def get_etf_component_stock_list(self):
        """ETF 구성종목시세"""
        pass

    def get_nav_comparison_stock(self):
        """NAV 비교추이(종목)"""
        pass

    def get_nav_comparison_daily(self):
        """NAV 비교추이(일)"""
        pass

    def get_nav_comparison_minute(self):
        """NAV 비교추이(분)"""
        pass
