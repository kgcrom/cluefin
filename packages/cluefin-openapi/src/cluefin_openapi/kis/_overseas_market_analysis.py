from cluefin_openapi.kis._client import Client


class OverseasMarketAnalysis:
    """해외주식 시세분석"""

    def __init__(self, client: Client):
        self.client = client

url: /uapi/overseas-stock/v1/ranking/price-fluctuation
tr_id: 실전[HHDFS76260000]
    def get_stock_price_rise_fall(self):
        """해외주식 가격급등락"""
        pass

url: /uapi/overseas-stock/v1/ranking/volume-surge
tr_id: 실전[HHDFS76270000]
    def get_stock_volume_surge(self):
        """해외주식 거래량급증"""
        pass

url: /uapi/overseas-stock/v1/ranking/volume-power
tr_id: 실전[HHDFS76280000]
    def get_stock_buy_execution_strength_top(self):
        """해외주식 매수체결강도상위"""
        pass

url: /uapi/overseas-stock/v1/ranking/updown-rate
tr_id: 실전[HHDFS76290000]
    def get_stock_rise_decline_rate(self):
        """해외주식 상승률/하락율"""
        pass

url: /uapi/overseas-stock/v1/ranking/new-highlow
tr_id: 실전[HHDFS76300000]
    def get_stock_new_high_low_price(self):
        """해외주식 신고/신저가"""
        pass

url: /uapi/overseas-stock/v1/ranking/trade-vol
tr_id: 실전[HHDFS76310010]
    def get_stock_trading_volume_rank(self):
        """해외주식 거래량순위"""
        pass

url: /uapi/overseas-stock/v1/ranking/trade-pbmn
tr_id: 실전[HHDFS76320010]
    def get_stock_trading_amount_rank(self):
        """해외주식 거래대금순위"""
        pass

url: /uapi/overseas-stock/v1/ranking/trade-growth
tr_id: 실전[HHDFS76330000]
    def get_stock_trading_increase_rate_rank(self):
        """해외주식 거래증가율순위"""
        pass

url: /uapi/overseas-stock/v1/ranking/trade-turnover
tr_id: 실전[HHDFS76340000]
    def get_stock_trading_turnover_rate_rank(self):
        """해외주식 거래회전율순위"""
        pass

url: /uapi/overseas-stock/v1/ranking/market-cap
tr_id: 실전[HHDFS76350100]
    def get_stock_market_cap_rank(self):
        """해외주식 시가총액순위"""
        pass

url: /uapi/overseas-price/v1/quotations/period-rights
tr_id: 실전[CTRGT011R]
    def get_stock_period_rights_inquiry(self):
        """해외주식 기간별권리조회"""
        pass

url: /uapi/overseas-price/v1/quotations/news-title
tr_id: 실전[HHPSTH60100C1]
    def get_news_aggregate_title(self):
        """해외뉴스종합(제목)"""
        pass

url: /uapi/overseas-price/v1/quotations/rights-by-ice
tr_id: 실전[HHDFS78330900]
    def get_stock_rights_aggregate(self):
        """해외주식 권리종합"""
        pass

url: /uapi/overseas-price/v1/quotations/colable-by-company
tr_id: 실전[CTLN4050R]
    def get_stock_collateral_loan_eligible(self):
        """당사 해외주식담보대출 가능 종목"""
        pass

url: /uapi/overseas-price/v1/quotations/brknews-title
tr_id: 실전[FHKST01011801]
    def get_breaking_news_title(self):
        """해외속보(제목)"""
        pass
