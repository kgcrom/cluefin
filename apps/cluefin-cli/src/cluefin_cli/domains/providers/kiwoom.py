"""Kiwoom provider adapter."""

from __future__ import annotations

from cluefin_cli.domains.providers.base import BrokerProvider


class KiwoomProvider(BrokerProvider):
    broker = "kiwoom"
