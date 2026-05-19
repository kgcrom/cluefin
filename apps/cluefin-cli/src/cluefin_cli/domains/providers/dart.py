"""DART provider adapter."""

from __future__ import annotations

from cluefin_cli.domains.providers.base import BrokerProvider


class DartProvider(BrokerProvider):
    broker = "dart"
