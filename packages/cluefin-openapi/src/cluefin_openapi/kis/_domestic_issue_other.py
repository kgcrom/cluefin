from cluefin_openapi.kis._client import Client


class DomesticIssueOther:
    """국내주식 업종/기타"""

    def __init__(self, client: Client):
        self.client = client

    def get_domestic_sector_current_index(self):
        """국내업종 현재지수"""
        pass

    def get_domestic_sector_daily_index(self):
        """국내업종 일자별지수"""
        pass

    def get_domestic_sector_time_index_stock(self):
        """국내업종 시간별지수(초)"""
        pass

    def get_domestic_sector_time_index_minute(self):
        """국내업종 시간별지수(분)"""
        pass

    def get_sector_analysis_inquiry(self):
        """업종 분봉조회"""
        pass

    def get_domestic_stock_sector_period_quote(self):
        """국내주식업종기간별시세(일/주/월/년)"""
        pass

    def get_domestic_sector_minute_separate_recent_list(self):
        """국내업종 구분별전체시세"""
        pass

    def get_domestic_stock_expected_conclusion_index_follow(self):
        """국내주식 예상체결지수 추이"""
        pass

    def get_domestic_stock_expected_conclusion_recent_index(self):
        """국내주식 예상체결 전체지수"""
        pass

    def get_volatility_completeness_status_vi_current(self):
        """변동성완화장치(VI) 현황"""
        pass

    def get_interest_aggregate_domestic_stock_interest(self):
        """금리 종합(국내채권/금리)"""
        pass

    def get_aggregate_market_announcement_schedule(self):
        """종합 시황/공시(제목)"""
        pass

    def get_domestic_rest_day_inquiry(self):
        """국내휴장일조회"""
        pass

    def get_domestic_option_business_day_inquiry(self):
        """국내선물 영업일조회"""
        pass
