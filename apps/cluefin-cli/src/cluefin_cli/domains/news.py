"""News domain service."""

from __future__ import annotations

from cluefin_cli.domains.models import DisclosureHeadline, NewsHeadline
from cluefin_cli.domains.providers import DartProvider, KisProvider


class NewsService:
    def __init__(self, dart_provider: DartProvider | None = None, kis_provider: KisProvider | None = None) -> None:
        self.dart_provider = dart_provider or DartProvider()
        self.kis_provider = kis_provider or KisProvider()

    def fetch(
        self,
        *,
        stock_code: str | None = None,
        source: str = "auto",
        days: int = 7,
        query: str | None = None,
    ) -> dict[str, list[NewsHeadline] | list[DisclosureHeadline]]:
        include_kis = source in {"auto", "kis", "all"}
        include_dart = source in {"dart", "all"}
        return {
            "news": self.kis_provider.fetch_news(stock_code=stock_code, days=days, query=query) if include_kis else [],
            "disclosures": self.dart_provider.fetch_disclosures(stock_code=stock_code, days=days, query=query)
            if include_dart
            else [],
        }
