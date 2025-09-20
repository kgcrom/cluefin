"""주요사항보고서 주요정보 (Major Shareholder Disclosure Main Information) API client."""

from ._client import Client


class MajorShareholderDisclosure:
    def __init__(self, client: Client):
        self.client = client

    def sample(self) -> str:
        """Sample method that outputs hello world."""
        return "hello world"
