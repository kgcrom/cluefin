from unittest.mock import MagicMock, patch

import pytest

from cluefin_desk.data.fetcher import DomesticDataFetcher


def _make_fetcher(monkeypatch, **settings_overrides):
    """Build a fetcher with Kiwoom auth mocked out (no network)."""
    from cluefin_desk.config.settings import settings

    monkeypatch.setattr(settings, "kiwoom_app_key", "kiwoom-key")
    monkeypatch.setattr(settings, "kiwoom_secret_key", "kiwoom-secret")
    for name, value in settings_overrides.items():
        monkeypatch.setattr(settings, name, value)

    with (
        patch("cluefin_desk.data.fetcher.KiwoomAuth") as kiwoom_auth,
        patch("cluefin_desk.data.fetcher.KiwoomClient"),
    ):
        kiwoom_auth.return_value.generate_token.return_value.get_token.return_value = "kiwoom-token"
        return DomesticDataFetcher()


class TestKisClientLazy:
    def test_missing_kis_keys_raises_on_access_not_on_init(self, monkeypatch):
        fetcher = _make_fetcher(monkeypatch, kis_app_key=None, kis_secret_key=None)
        assert fetcher.has_kis is False
        with pytest.raises(ValueError, match="KIS_APP_KEY"):
            _ = fetcher.kis_client

    def test_missing_kis_secret_raises(self, monkeypatch):
        fetcher = _make_fetcher(monkeypatch, kis_app_key="kis-key", kis_secret_key=None)
        assert fetcher.has_kis is False
        with pytest.raises(ValueError, match="KIS_SECRET_KEY"):
            _ = fetcher.kis_client

    def test_no_kis_auth_at_construction(self, monkeypatch):
        with patch("cluefin_desk.data.fetcher.KisAuth") as kis_auth:
            _make_fetcher(monkeypatch, kis_app_key="kis-key", kis_secret_key="kis-secret")
            kis_auth.assert_not_called()

    def test_builds_once_and_caches(self, monkeypatch):
        fetcher = _make_fetcher(monkeypatch, kis_app_key="kis-key", kis_secret_key="kis-secret", kis_env="prod")
        assert fetcher.has_kis is True

        with (
            patch("cluefin_desk.data.fetcher.KisAuth") as kis_auth,
            patch("cluefin_desk.data.fetcher.KisClient") as kis_client_cls,
        ):
            kis_auth.return_value.generate.return_value.get_token.return_value = "kis-token"
            kis_client_cls.return_value = MagicMock()

            first = fetcher.kis_client
            second = fetcher.kis_client

        assert first is second
        kis_auth.assert_called_once()
        kis_auth.return_value.generate.assert_called_once()
        kis_client_cls.assert_called_once()
        assert kis_client_cls.call_args.kwargs["token"] == "kis-token"
        assert kis_client_cls.call_args.kwargs["env"] == "prod"
