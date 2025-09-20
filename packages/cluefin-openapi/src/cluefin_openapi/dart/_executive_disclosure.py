"""증권신고서 주요정보 (Executive Disclosure Main Information) API client."""

from ._client import Client


class ExecutiveDisclosure:
    def __init__(self, client: Client):
        self.client = client

    def sample(self) -> str:
        """Sample method that outputs hello world."""
        return "hello world"
