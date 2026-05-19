"""KIS provider adapter."""

from __future__ import annotations

from cluefin_cli.domains.providers.base import BrokerProvider


class KisProvider(BrokerProvider):
    broker = "kis"
