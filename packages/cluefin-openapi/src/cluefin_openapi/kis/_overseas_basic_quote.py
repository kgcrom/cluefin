from cluefin_openapi.kis._client import Client


class OverseasBasicQuote:
    """해외주식 기본시세"""

    def __init__(self, client: Client):
        self.client = client

    def get_overseas_stock_current_price_detail(self):
        """해외주식 현재가상세"""
        pass

    def get_overseas_stock_current_price_first_hoga(self):
        """해외주식 현재가 1호가"""
        pass

    def get_overseas_stock_current_conclusion_price(self):
        """해외주식 현재체결가"""
        pass

    def get_overseas_stock_settlement_follow(self):
        """해외주식 체결추이"""
        pass

    def get_overseas_stock_analysis_inquiry(self):
        """해외주식분봉조회"""
        pass

    def get_overseas_index_analysis_inquiry(self):
        """해외지수분봉조회"""
        pass

    def get_overseas_stock_period_quote(self):
        """해외주식 기간별시세"""
        pass

    def get_overseas_stock_item_index_exchange_period_quote(self):
        """해외주식 종목/지수/환율기간별시세(일/주/월/년)"""
        pass

    def get_overseas_stock_condition_search(self):
        """해외주식조건검색"""
        pass

    def get_overseas_settlement_date_inquiry(self):
        """해외결제일자조회"""
        pass

    def get_overseas_stock_product_base_info(self):
        """해외주식 상품기본정보"""
        pass

    def get_overseas_stock_sector_separate_quote(self):
        """해외주식 업종별시세"""
        pass

    def get_overseas_stock_sector_separate_code_inquiry(self):
        """해외주식 업종별코드조회"""
        pass
