from cluefin_openapi.kis._client import Client


class DomesticRankingAnalysis:
    """국내주식 순위분석"""

    def __init__(self, client: Client):
        self.client = client

    def get_trading_volume_rank(self):
        """거래량순위"""
        pass

    def get_stock_fluctuation_rank(self):
        """국내주식 등락률 순위"""
        pass

    def get_stock_hoga_quantity_rank(self):
        """국내주식 호가잔량 순위"""
        pass

    def get_stock_profitability_indicator_rank(self):
        """국내주식 수익자산지표 순위"""
        pass

    def get_stock_market_cap_top(self):
        """국내주식 시가총액 상위"""
        pass

    def get_stock_finance_ratio_rank(self):
        """국내주식 재무비율 순위"""
        pass

    def get_stock_time_hoga_rank(self):
        """국내주식 시간외잔량 순위"""
        pass

    def get_stock_preferred_stock_ratio_top(self):
        """국내주식 우선주/리리율 상위"""
        pass

    def get_stock_disparity_index_rank(self):
        """국내주식 이격도 순위"""
        pass

    def get_stock_market_price_rank(self):
        """국내주식 시장가치 순위"""
        pass

    def get_stock_execution_strength_top(self):
        """국내주식 체결강도 상위"""
        pass

    def get_stock_watchlist_registration_top(self):
        """국내주식 관심종목등록 상위"""
        pass

    def get_stock_expected_execution_rise_decline_top(self):
        """국내주식 예상체결 상승/하락상위"""
        pass

    def get_stock_proprietary_trading_top(self):
        """국내주식 당사매매종목 상위"""
        pass

    def get_stock_new_high_low_approaching_top(self):
        """국내주식 신고/신저근접종목 상위"""
        pass

    def get_stock_dividend_yield_top(self):
        """국내주식 배당률 상위"""
        pass

    def get_stock_large_execution_count_top(self):
        """국내주식 대량체결건수 상위"""
        pass

    def get_stock_credit_balance_top(self):
        """국내주식 신용잔고 상위"""
        pass

    def get_stock_short_selling_top(self):
        """국내주식 공매도 상위종목"""
        pass

    def get_stock_after_hours_fluctuation_rank(self):
        """국내주식 시간외등락율순위"""
        pass

    def get_stock_after_hours_volume_rank(self):
        """국내주식 시간외거래량순위"""
        pass

    def get_hts_inquiry_top_20(self):
        """HTS조회상위20종목"""
        pass
