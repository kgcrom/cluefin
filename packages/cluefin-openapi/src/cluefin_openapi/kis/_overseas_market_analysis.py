from cluefin_openapi.kis._client import Client


class OverseasMarketAnalysis:
    """해외주식 시세분석"""

    def __init__(self, client: Client):
        self.client = client
