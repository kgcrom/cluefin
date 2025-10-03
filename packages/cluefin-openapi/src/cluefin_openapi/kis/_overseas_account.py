from cluefin_openapi.kis._client import Client


class OverseasAccount:
    """해외주식 주문/계좌"""

    def __init__(self, client: Client):
        self.client = client
