from cluefin_openapi.kis._http_client import HttpClient


class OverseasRealtimeQuote:
    """해외주식 실시간시세"""

    def __init__(self, client: HttpClient):
        self.client = client
