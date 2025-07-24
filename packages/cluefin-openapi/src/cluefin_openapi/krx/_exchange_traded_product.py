class ExchangeTradedProduct:
    def __init__(self, client):
        self.client = client
        self.path = "/svc/apis/etp/{}"

    def get_data(self, endpoint: str, params: dict = None):
        """상장지수상품 관련 데이터를 조회합니다."""
        path = self.path.format(endpoint)
        return self.client._get(path, params)
