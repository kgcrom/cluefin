from cluefin_openapi.kis._client import Client


class DomesticAccount:
    """국내주식 주문/계좌"""

    def __init__(self, client: Client):
        self.client = client
