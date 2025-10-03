from cluefin_openapi.kis._client import Client


class DomesticStockInfo:
    """국내주식 종목정보"""

    def __init__(self, client: Client):
        self.client = client
