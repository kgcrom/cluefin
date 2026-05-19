"""Domain service for market scanner data."""

from __future__ import annotations

from typing import Literal

from cluefin_cli.domains.models import MarketRankItem
from cluefin_cli.domains.providers.kis import KisProvider
from cluefin_cli.domains.providers.kiwoom import KiwoomProvider

MarketCategory = Literal["volume", "ranking", "theme", "sector"]


class MarketService:
    def __init__(self, *, kiwoom_provider: KiwoomProvider | None = None, kis_provider: KisProvider | None = None):
        self.kiwoom_provider = kiwoom_provider or KiwoomProvider()
        self.kis_provider = kis_provider or KisProvider()

    def fetch(self, *, category: MarketCategory, source: str = "auto", limit: int = 20) -> list[MarketRankItem]:
        if source == "auto":
            return self._fetch_default(category=category, limit=limit)
        if source == "all":
            return self._fetch_all(category=category, limit=limit)
        return self._fetch_provider(provider=source, category=category, limit=limit)

    def _fetch_default(self, *, category: MarketCategory, limit: int) -> list[MarketRankItem]:
        if category == "theme":
            return self.kiwoom_provider.fetch_market_theme(limit=limit)
        if category == "sector":
            return self.kis_provider.fetch_market_sector(limit=limit)
        if category == "ranking":
            return self.kis_provider.fetch_market_ranking(limit=limit)
        return self.kis_provider.fetch_market_volume(limit=limit)

    def _fetch_all(self, *, category: MarketCategory, limit: int) -> list[MarketRankItem]:
        if category == "theme":
            return self.kiwoom_provider.fetch_market_theme(limit=limit)

        items: list[MarketRankItem] = []
        for provider in ["kis", "kiwoom"]:
            try:
                items.extend(self._fetch_provider(provider=provider, category=category, limit=limit))
            except NotImplementedError:
                continue
        return items

    def _fetch_provider(self, *, provider: str, category: MarketCategory, limit: int) -> list[MarketRankItem]:
        if provider == "kis":
            if category == "volume":
                return self.kis_provider.fetch_market_volume(limit=limit)
            if category == "ranking":
                return self.kis_provider.fetch_market_ranking(limit=limit)
            if category == "sector":
                return self.kis_provider.fetch_market_sector(limit=limit)

        if provider == "kiwoom":
            if category == "volume":
                return self.kiwoom_provider.fetch_market_volume(limit=limit)
            if category == "ranking":
                return self.kiwoom_provider.fetch_market_ranking(limit=limit)
            if category == "theme":
                return self.kiwoom_provider.fetch_market_theme(limit=limit)
            if category == "sector":
                return self.kiwoom_provider.fetch_market_sector(limit=limit)

        raise NotImplementedError(f"{provider} does not support market {category}")
