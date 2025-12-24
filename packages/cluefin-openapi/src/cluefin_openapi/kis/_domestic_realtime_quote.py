from cluefin_openapi.kis._http_client import HttpClient


class DomesticRealtimeQuote:
    """국내주식 실시간시세"""

    def __init__(self, client: HttpClient):
        self.client = client
