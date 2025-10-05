from cluefin_openapi.kis._client import Client


class DomesticMarketAnalysis:
    """국내주식 시세분석"""

    def __init__(self, client: Client):
        self.client = client

    def get_stock_condition_search_target_list_inquiry(self):
        """종목조건검색 목록조회"""
        pass

    def get_stock_condition_search_inquiry(self):
        """종목조건검색조회"""
        pass

    def get_interest_stock_group_inquiry(self):
        """관심종목 그룹조회"""
        pass

    def get_interest_stock_multi_stock_quote_inquiry(self):
        """관심종목(멀티종목) 시세조회"""
        pass

    def get_interest_stock_group_separate_stock_inquiry(self):
        """관심종목 그룹별 종목조회"""
        pass

    def get_domestic_period_foreign_trading_stock_price_limit(self):
        """국내기관_외국인 매매종목가집계"""
        pass

    def get_foreign_trading_stock_price_limit(self):
        """외국계 매매종목 가집계"""
        pass

    def get_stock_separate_investor_trading_trend_daily(self):
        """종목별 투자자매매동향(일별)"""
        pass

    def get_market_separate_investor_trading_trend_time(self):
        """시장별 투자자매매동향(시세)"""
        pass

    def get_market_separate_investor_trading_trend_daily(self):
        """시장별 투자자매매동향(일별)"""
        pass

    def get_stock_separate_foreign_net_buy_follow(self):
        """종목별 외국계 순매수추이"""
        pass

    def get_member_realtime_trading_trend_tick(self):
        """회원사 실시간 매매동향(틱)"""
        pass

    def get_stock_current_price_member_stock_trading_trend(self):
        """주식현재가 회원사 종목매매동향"""
        pass

    def get_stock_separate_program_trading_follow_detail(self):
        """종목별 프로그램매매추이(체결)"""
        pass

    def get_stock_separate_program_trading_follow_daily(self):
        """종목별 프로그램매매추이(일별)"""
        pass

    def get_stock_separate_foreign_period_estimation_limit(self):
        """종목별 외인기관 추정기전계"""
        pass

    def get_stock_separate_daily_buy_sell_conclusion_power(self):
        """종목별일별매수매도체결량"""
        pass

    def get_program_trading_buy_sell_aggregate_current_time(self):
        """프로그램매매 종합현황(시간)"""
        pass

    def get_program_trading_buy_sell_aggregate_current_daily(self):
        """프로그램매매 종합현황(일별)"""
        pass

    def get_program_trading_buy_sell_investor_trading_trend_same(self):
        """프로그램매매 투자자매매동향(당일)"""
        pass

    def get_domestic_stock_new_credit_daily_follow(self):
        """국내주식 신용잔고 일별추이"""
        pass

    def get_domestic_stock_expected_conclusion_price_follow(self):
        """국내주식 예상체결가 추이"""
        pass

    def get_domestic_stock_public_sale_daily_follow(self):
        """국내주식 공매도 일별추이"""
        pass

    def get_domestic_stock_time_expected_conclusion_trend(self):
        """국내주식 시간외예상체결등락율"""
        pass

    def get_domestic_stock_settlement_amount_separate_trading_ratio(self):
        """국내주식 체결금액별 매매비중"""
        pass

    def get_domestic_medium_capital_aggregate(self):
        """국내 증시자금 종합"""
        pass

    def get_stock_separate_daily_major_data_follow(self):
        """종목별 일별 대차거래추이"""
        pass

    def get_domestic_stock_top_price_target(self):
        """국내주식 상하한가 표착"""
        pass

    def get_domestic_stock_sale_amount_coverage_ratio(self):
        """국내주식 매물대/거래비중"""
        pass
