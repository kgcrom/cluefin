class GeneralProduct:
    def __init__(self, client):
        self.client = client
        self.path = "/svc/apis/gen/{}"

    def get_data(self, endpoint: str, params: dict = None):
        """일반상품 관련 데이터를 조회합니다."""
        path = self.path.format(endpoint)
        return self.client._get(path, params)
