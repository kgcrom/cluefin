"""공시정보 (Public Disclosure Information) API client."""

from ._client import Client


class PublicDisclosure:
    def __init__(self, client: Client):
        self.client = client

    def sample(self) -> str:
        """Sample method that outputs hello world."""
        return "hello world"
