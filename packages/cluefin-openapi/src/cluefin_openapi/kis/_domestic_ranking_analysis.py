from cluefin_openapi.kis._client import Client


class DomesticRankingAnalysis:
    """국내주식 순위분석"""

    def __init__(self, client: Client):
        self.client = client
