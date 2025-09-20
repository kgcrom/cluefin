"""정기보고서 재무정보 (Periodic Disclosure Detail Information) API client."""

from ._client import Client


class PeriodicDisclosureDetail:
    def __init__(self, client: Client):
        self.client = client

    def sample(self) -> str:
        """Sample method that outputs hello world."""
        return "hello world"
