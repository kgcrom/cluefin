class Esg:
    def __init__(self, client):
        self.client = client
        self.path = "/svc/apis/esg/{}"

    def get_data(self, endpoint: str, params: dict = None):
        """ESG 관련 데이터를 조회합니다."""
        path = self.path.format(endpoint)
        return self.client._get(path, params)
