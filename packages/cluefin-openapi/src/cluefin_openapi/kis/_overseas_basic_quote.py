from cluefin_openapi.kis._client import Client


class BasicQuote:
    """해외주식 기본시세"""

    def __init__(self, client: Client):
        self.client = client

url: /uapi/overseas-price/v1/quotations/price-detail
tr_id: 실전[HHDFS76200200], 모의[모의투자 미지원]
    def get_stock_current_price_detail(self):
        """해외주식 현재가상세"""
        pass

url: /uapi/overseas-price/v1/quotations/inquire-asking-price
tr_id: 실전[해외주식-033], 모의[모의투자 미지원]
    def get_current_price_first_quote(self):
        """해외주식 현재가 1호가"""
        pass

url: /uapi/overseas-price/v1/quotations/price
tr_id: 실전[HHDFS00000300], 모의[HHDFS00000300]
    def get_stock_current_price_conclusion(self):
        """해외주식 현재체결가"""
        pass

url: /uapi/overseas-price/v1/quotations/inquire-ccnl
tr_id: 실전[해외주식-037], 모의[모의투자 미지원]
    def get_conclusion_trend(self):
        """해외주식 체결추이"""
        pass

url: /uapi/overseas-price/v1/quotations/inquire-time-itemchartprice
tr_id: 실전[HHDFS76950200], 모의[모의투자 미지원]
    def get_stock_minute_chart(self):
        """해외주식분봉조회"""
        pass

url: /uapi/overseas-price/v1/quotations/inquire-time-indexchartprice
tr_id: 실전[FHKST03030200], 모의[모의투자 미지원]
    def get_index_minute_chart(self):
        """해외지수분봉조회"""
        pass

url: /uapi/overseas-price/v1/quotations/dailyprice
tr_id: 실전[HHDFS76240000], 모의[HHDFS76240000]
    def get_stock_period_quote(self):
        """해외주식 기간별시세"""
        pass

url: /uapi/overseas-price/v1/quotations/inquire-daily-chartprice
tr_id: 실전[FHKST03030100], 모의[FHKST03030100]
    def get_item_index_exchange_period_price(self):
        """해외주식 종목/지수/환율기간별시세(일/주/월/년)"""
        pass

url: /uapi/overseas-price/v1/quotations/inquire-search
tr_id: 실전[HHDFS76410000], 모의[HHDFS76410000]
    def search_by_condition(self):
        """해외주식조건검색"""
        pass

url: /uapi/overseas-stock/v1/quotations/countries-holiday
tr_id: 실전[해외주식-017], 모의[모의투자 미지원]
    def get_settlement_date(self):
        """해외결제일자조회"""
        pass

url: /uapi/overseas-price/v1/quotations/search-info
tr_id: 실전[CTPF1702R], 모의[모의투자 미지원]
    def get_product_base_info(self):
        """해외주식 상품기본정보"""
        pass

url: /uapi/overseas-price/v1/quotations/industry-theme
tr_id: 실전[해외주식-048], 모의[모의투자 미지원]
    def get_sector_price(self):
        """해외주식 업종별시세"""
        pass

url: /uapi/overseas-price/v1/quotations/industry-price
tr_id: 실전[해외주식-049], 모의[모의투자 미지원]
    def get_sector_codes(self):
        """해외주식 업종별코드조회"""
        pass
