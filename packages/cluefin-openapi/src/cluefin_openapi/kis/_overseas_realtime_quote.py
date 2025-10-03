from cluefin_openapi.kis._client import Client


class OverseasRealtimeQuote:
    """해외주식 실시간시세"""

    def __init__(self, client: Client):
        self.client = client
