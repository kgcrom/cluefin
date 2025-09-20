"""정기보고서 주요정보 (Periodic Disclosure Main Information) API client."""

from ._client import Client


class PeriodicDisclosureMain:
    def __init__(self, client: Client):
        self.client = client

    def sample(self) -> str:
        """Sample method that outputs hello world."""
        return "hello world"
