from cluefin_cli.domains.providers import DartProvider, KisProvider, KiwoomProvider


class FakeFactory:
    def __init__(self) -> None:
        self.calls: list[str] = []

    def create(self, broker: str):
        self.calls.append(broker)
        return {"broker": broker}


def test_providers_create_clients_through_injected_factory() -> None:
    factory = FakeFactory()

    assert DartProvider(factory).client == {"broker": "dart"}
    assert KisProvider(factory).client == {"broker": "kis"}
    assert KiwoomProvider(factory).client == {"broker": "kiwoom"}
    assert factory.calls == ["dart", "kis", "kiwoom"]


def test_provider_client_is_cached() -> None:
    factory = FakeFactory()
    provider = KisProvider(factory)

    assert provider.client is provider.client
    assert factory.calls == ["kis"]
