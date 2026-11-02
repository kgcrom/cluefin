"""Live check of `kis stock implied-expectations` (KIS/DART/ECOS keys from .env.test, Damodaran over the network).

Samsung Electronics (005930 / corp_code 00126380) — the same public sample pair `metadata._NAME_SAMPLES`
already uses — so no corp-name scrub is needed. Asserts structure and finite values only; the model is
assumption-sensitive, so no number is pinned.
"""

from __future__ import annotations

import math
import os
from pathlib import Path

import dotenv
import pytest
from cluefin_openapi import BrokerClientConfig, BrokerClientFactory

from cluefin_openapi_cli.handlers.kis import domestic_stock_info as handlers

STOCK_CODE = "005930"
CORP_CODE = "00126380"


class _Session:
    def __init__(self, kis, dart, ecos) -> None:
        self._kis = kis
        self._dart = dart
        self._ecos = ecos

    def get_kis(self):
        return self._kis

    def get_dart(self):
        return self._dart

    def get_ecos(self):
        return self._ecos


@pytest.fixture(scope="module")
def session() -> _Session:
    dotenv.load_dotenv(dotenv_path=Path(__file__).resolve().parents[3] / ".env.test")
    kis_app_key = os.getenv("KIS_APP_KEY")
    kis_secret_key = os.getenv("KIS_SECRET_KEY")
    dart_auth_key = os.getenv("DART_AUTH_KEY")
    ecos_auth_key = os.getenv("ECOS_AUTH_KEY")
    if not (kis_app_key and kis_secret_key and dart_auth_key and ecos_auth_key):
        pytest.skip("KIS/DART/ECOS keys are not fully configured in .env.test")
    # Not BrokerClientConfig.from_env(): it merges the cwd's .env (production) into the config.
    config = BrokerClientConfig(
        kis_app_key=kis_app_key,
        kis_secret_key=kis_secret_key,
        kis_env=os.getenv("KIS_ENV", "dev"),
        dart_auth_key=dart_auth_key,
        ecos_auth_key=ecos_auth_key,
    )
    factory = BrokerClientFactory(config)
    return _Session(factory.create("kis"), factory.create("dart"), factory.create("ecos"))


@pytest.mark.integration
def test_implied_expectations_live_run_has_finite_values(session: _Session) -> None:
    out = handlers.handle_kis_implied_expectations({"stock_code": STOCK_CODE, "corp_code": CORP_CODE}, session)

    assert out["stock_code"] == STOCK_CODE
    assert out["corp_code"] == CORP_CODE
    assert math.isfinite(out["price"]["close"])
    assert out["market_cap"] is not None
    assert math.isfinite(out["market_cap"])
    assert out["ev"] is not None
    assert math.isfinite(out["ev"])

    assumptions = out["assumptions"]
    for key in ("beta", "cost_of_equity"):
        assert math.isfinite(assumptions[key])
    assert assumptions["erp"]["value"] is not None
    assert math.isfinite(assumptions["erp"]["value"])
    assert assumptions["risk_free"]["value"] is not None
    assert math.isfinite(assumptions["risk_free"]["value"])
    assert assumptions["cost_of_debt"]["value"] is not None
    assert math.isfinite(assumptions["cost_of_debt"]["value"])
    assert assumptions["tax_rate"]["value"] is not None
    assert math.isfinite(assumptions["tax_rate"]["value"])

    # RIM/reverse-DCF may legitimately have no solution in the search range; when they do, the
    # value must be finite, and either way a reason/None is present.
    rim_roe = out["rim"]["implied_roe"]
    if rim_roe is not None:
        assert math.isfinite(rim_roe)
    dcf_growth = out["reverse_dcf"]["implied_revenue_growth"]
    if dcf_growth is not None:
        assert math.isfinite(dcf_growth)

    assert len(out["sensitivity"]["rim_implied_roe"]) == 5
    assert len(out["sensitivity"]["reverse_dcf_implied_growth"]) == 5

    comparison = out["comparison"]
    assert comparison["dart_roe_latest_fy"] is not None
    assert comparison["dart_revenue_cagr_3y"] is not None
    assert comparison["ttm_operating_margin"] is not None

    assert out["calls"] > 0
    assert out["notes"]
