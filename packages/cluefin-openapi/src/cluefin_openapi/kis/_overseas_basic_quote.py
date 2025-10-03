from cluefin_openapi.kis._client import Client


class OverseasBasicQuote:
    """해외주식 기본시세"""

    def __init__(self, client: Client):
        self.client = client
