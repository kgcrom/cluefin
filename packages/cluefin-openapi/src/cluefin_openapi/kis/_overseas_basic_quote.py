from cluefin_openapi.kis._client import Client


class BasicQuote:
    """해외주식 기본시세"""

    def __init__(self, client: Client):
        self.client = client

    def get_current_price_detail(self):
        """해외주식 현재가상세"""
        pass

    def get_current_price_first_quote(self):
        """해외주식 현재가 1호가"""
        pass

    def get_current_execution_price(self):
        """해외주식 현재체결가"""
        pass

    def get_execution_trend(self):
        """해외주식 체결추이"""
        pass

    def get_stock_minute_data(self):
        """해외주식분봉조회"""
        pass

    def get_index_minute_data(self):
        """해외지수분봉조회"""
        pass

    def get_period_price(self):
        """해외주식 기간별시세"""
        pass

    def get_item_index_exchange_period_price(self):
        """해외주식 종목/지수/환율기간별시세(일/주/월/년)"""
        pass

    def search_by_condition(self):
        """해외주식조건검색"""
        pass

    def get_settlement_date(self):
        """해외결제일자조회"""
        pass

    def get_product_base_info(self):
        """해외주식 상품기본정보"""
        pass

    def get_sector_price(self):
        """해외주식 업종별시세"""
        pass

    def get_sector_codes(self):
        """해외주식 업종별코드조회"""
        pass
