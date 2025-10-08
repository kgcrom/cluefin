from cluefin_openapi.kis._client import Client


class DomesticMarketAnalysis:
    """국내주식 시세분석"""

    def __init__(self, client: Client):
        self.client = client

    def get_condition_search_list(self):
        """종목조건검색 목록조회"""
        pass

    def get_condition_search_result(self):
        """종목조건검색조회"""
        pass

    def get_watchlist_groups(self):
        """관심종목 그룹조회"""
        pass

    def get_watchlist_multi_quote(self):
        """관심종목(멀티종목) 시세조회"""
        pass

    def get_watchlist_stocks_by_group(self):
        """관심종목 그룹별 종목조회"""
        pass

    def get_institutional_foreign_trading_aggregate(self):
        """국내기관_외국인 매매종목가집계"""
        pass

    def get_foreign_brokerage_trading_aggregate(self):
        """외국계 매매종목 가집계"""
        pass

    def get_investor_trading_trend_by_stock_daily(self):
        """종목별 투자자매매동향(일별)"""
        pass

    def get_investor_trading_trend_by_market_intraday(self):
        """시장별 투자자매매동향(시세)"""
        pass

    def get_investor_trading_trend_by_market_daily(self):
        """시장별 투자자매매동향(일별)"""
        pass

    def get_foreign_net_buy_trend_by_stock(self):
        """종목별 외국계 순매수추이"""
        pass

    def get_member_trading_trend_tick(self):
        """회원사 실시간 매매동향(틱)"""
        pass

    def get_member_trading_trend_by_stock(self):
        """주식현재가 회원사 종목매매동향"""
        pass

    def get_program_trading_trend_by_stock_intraday(self):
        """종목별 프로그램매매추이(체결)"""
        pass

    def get_program_trading_trend_by_stock_daily(self):
        """종목별 프로그램매매추이(일별)"""
        pass

    def get_foreign_institutional_estimate_by_stock(self):
        """종목별 외인기관 추정기전계"""
        pass

    def get_buy_sell_volume_by_stock_daily(self):
        """종목별일별매수매도체결량"""
        pass

    def get_program_trading_summary_intraday(self):
        """프로그램매매 종합현황(시간)"""
        pass

    def get_program_trading_summary_daily(self):
        """프로그램매매 종합현황(일별)"""
        pass

    def get_program_trading_investor_trend_today(self):
        """프로그램매매 투자자매매동향(당일)"""
        pass

    def get_credit_balance_trend_daily(self):
        """국내주식 신용잔고 일별추이"""
        pass

    def get_expected_price_trend(self):
        """국내주식 예상체결가 추이"""
        pass

    def get_short_selling_trend_daily(self):
        """국내주식 공매도 일별추이"""
        pass

    def get_after_hours_expected_fluctuation(self):
        """국내주식 시간외예상체결등락율"""
        pass

    def get_trading_weight_by_amount(self):
        """국내주식 체결금액별 매매비중"""
        pass

    def get_market_fund_summary(self):
        """국내 증시자금 종합"""
        pass

    def get_stock_loan_trend_daily(self):
        """종목별 일별 대차거래추이"""
        pass

    def get_limit_price_stocks(self):
        """국내주식 상하한가 표착"""
        pass

    def get_resistance_level_trading_weight(self):
        """국내주식 매물대/거래비중"""
        pass
