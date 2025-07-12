import os
import time

import dotenv
import pytest

from cluefin_openapi.kiwoom._auth import Auth
from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._domestic_foreign_types import (
    DomesticForeignConsecutiveNetBuySellStatusByInstitutionForeigner,
    DomesticForeignInvestorTradingTrendByStock,
    DomesticForeignStockInstitution,
)


@pytest.fixture
def auth() -> Auth:
    dotenv.load_dotenv(dotenv_path=".env.test")
    return Auth(
        app_key=os.getenv("APP_KEY"),
        secret_key=os.getenv("SECRET_KEY"),
        env="dev",
    )


@pytest.fixture
def client(auth: Auth) -> Client:
    """Create a Client instance for testing.

    Args:
        auth (Auth): The authenticated Auth instance.

    Returns:
        Client: A configured Client instance.
    """
    token = auth.generate_token()
    return Client(token=token.token, env="dev")


def test_get_foreign_investor_trading_trend_by_stock(client: Client):
    time.sleep(1)

    response = client.foreign.get_foreign_investor_trading_trend_by_stock("005930")

    assert response is not None
    assert isinstance(response.body, DomesticForeignInvestorTradingTrendByStock)
    assert response.body.stk_frgnr is not None


def test_get_stock_institution(client: Client):
    time.sleep(1)

    response = client.foreign.get_stock_institution("005930")

    assert response is not None
    assert isinstance(response.body, DomesticForeignStockInstitution)
    assert response.body.pre is not None


def test_get_consecutive_net_buy_sell_status_by_institution_foreigner(client: Client):
    time.sleep(1)

    response = client.foreign.get_consecutive_net_buy_sell_status_by_institution_foreigner("1", "001", "0", "0", "1")

    assert response is not None
    assert isinstance(response.body, DomesticForeignConsecutiveNetBuySellStatusByInstitutionForeigner)
    assert len(response.body.orgn_frgnr_cont_trde_prst) > 0
