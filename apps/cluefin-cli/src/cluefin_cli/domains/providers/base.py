"""Common provider adapter helpers."""

from __future__ import annotations

from typing import Any, Literal

from cluefin_openapi import BrokerClientFactory

BrokerName = Literal["dart", "kis", "kiwoom"]


class BrokerProvider:
    """Lazy broker client holder backed by BrokerClientFactory."""

    broker: BrokerName

    def __init__(self, client_factory: BrokerClientFactory | None = None) -> None:
        self._client_factory = client_factory or BrokerClientFactory()
        self._client: Any | None = None

    @property
    def client(self) -> Any:
        if self._client is None:
            self._client = self._client_factory.create(self.broker)
        return self._client
