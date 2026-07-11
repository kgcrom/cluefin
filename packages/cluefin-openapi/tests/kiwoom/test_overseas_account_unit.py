import inspect
import re

import pytest

from cluefin_openapi.kiwoom import _overseas_account as overseas_account_module
from cluefin_openapi.kiwoom._overseas_account import OverseasAccount

from ._helpers import EndpointCase, run_post_case

CALL_KWARGS = {
    "get_daily_account_profit_rate": {"from_dt": "20240102", "to": "20240131"},
    "get_monthly_account_profit_rate": {"from_dt": "202401", "to": "202406"},
    "get_yearly_account_profit_rate": {"from_dt": "2023", "to": "2024"},
    "get_daily_stock_profit_rate": {
        "from_dt": "20240102",
        "to": "20240131",
        "stk_cd": "AAPL",
        "stex_tp": "ND",
    },
    "get_monthly_stock_profit_rate": {
        "from_dt": "202401",
        "to": "202406",
        "stk_cd": "AAPL",
        "stex_tp": "ND",
    },
    "get_yearly_stock_profit_rate": {
        "from_dt": "2023",
        "to": "2024",
        "stk_cd": "AAPL",
        "stex_tp": "ND",
    },
    "get_ledger_unfilled_orders": {
        "ord_dt": "20240102",
        "slby_tp": "0",
        "stex_tp": "ND",
        "stk_cd": "AAPL",
    },
    "get_ledger_balance": {"stex_tp": "ND", "stk_cd": "AAPL"},
    "get_transaction_history": {
        "strt_dt": "20240102",
        "end_dt": "20240131",
        "tp": "0",
        "stex_tp": "ND",
        "stk_cd": "AAPL",
        "krw_repl_skip_yn": "N",
    },
    "get_deposit": {},
    "get_krw_withdrawable_amount": {},
    "get_deposit_and_securities_valuation_by_currency": {"cmsn_incl_tp": "0", "exrt_tp": "0"},
    "get_ledger_valuation_amount": {"cmsn_incl_tp": "0", "exrt_tp": "0"},
    "get_valuation_amount_by_date": {"base_dt": "20240102"},
    "get_deposit_and_securities_valuation_by_currency_on_date": {"base_dt": "20240102"},
    "get_daily_order_execution_history": {
        "query_tp": "1",
        "slby_tp": "0",
        "ord_dt": "20240102",
        "stex_tp": "ND",
        "stk_cd": "AAPL",
        "oppo_trde_tp": "0",
        "fr_ord_no": "0001",
    },
    "get_deposit_detail": {},
    "get_today_realized_profit_loss_by_stock": {"fc_krw_tp": "0"},
    "get_order_history_by_period": {
        "strt_dt": "20240102",
        "end_dt": "20240131",
        "slby_tp": "0",
        "stex_tp": "ND",
        "stk_cd": "AAPL",
        "oppo_trde_tp": "0",
    },
    "get_today_order_execution": {"slby_tp": "0", "stex_tp": "ND", "stk_cd": "AAPL"},
    "get_realized_profit_loss": {"strt_dt": "20240102", "end_dt": "20240131", "fc_krw_tp": "0"},
    "get_today_trading": {"qry_tp": "0", "fc_krw_tp": "0", "base_dt": "20240102"},
    "get_today_trading_summary": {"fc_krw_tp": "0", "stex_tp": "ND", "stk_cd": "AAPL"},
    "get_today_realized_profit_loss": {"fc_krw_tp": "0", "stex_tp": "ND", "stk_cd": "AAPL"},
    "get_daily_realized_profit_loss_by_stock": {
        "cntr_dt": "20240102",
        "fc_krw_tp": "0",
        "stex_tp": "ND",
        "stk_cd": "AAPL",
    },
    "get_profit_rate_by_period": {"fr_dt": "20240102", "to_dt": "20240131"},
    "get_daily_realized_profit_loss": {"strt_dt": "20240102", "end_dt": "20240131"},
    "get_monthly_realized_profit_loss": {"strt_dt": "202401", "end_dt": "202406"},
}

# Methods where the request body differs from the call kwargs because the
# ``from_dt`` argument is serialized under the body key ``"from"``.
EXPECTED_BODY = {
    "get_daily_account_profit_rate": {"from": "20240102", "to": "20240131"},
    "get_monthly_account_profit_rate": {"from": "202401", "to": "202406"},
    "get_yearly_account_profit_rate": {"from": "2023", "to": "2024"},
    "get_daily_stock_profit_rate": {
        "from": "20240102",
        "to": "20240131",
        "stex_tp": "ND",
        "stk_cd": "AAPL",
    },
    "get_monthly_stock_profit_rate": {
        "from": "202401",
        "to": "202406",
        "stex_tp": "ND",
        "stk_cd": "AAPL",
    },
    "get_yearly_stock_profit_rate": {
        "from": "2023",
        "to": "2024",
        "stex_tp": "ND",
        "stk_cd": "AAPL",
    },
}


def payload(name: str):
    return {"return_code": 0, "return_msg": "OK", "endpoint": name}


def method_metadata(method_name: str) -> tuple[str, str]:
    method = getattr(OverseasAccount, method_name)
    source = inspect.getsource(method)
    api_id = re.search(r'"api-id":\s*"([^"]+)"', source).group(1)
    model_attr = re.search(r"= (OverseasAccount\w+)\.model_validate", source).group(1)
    return api_id, model_attr


ACCOUNT_CASES = []
for method_name, kwargs in CALL_KWARGS.items():
    api_id, model_attr = method_metadata(method_name)
    case_name = method_name.removeprefix("get_")
    ACCOUNT_CASES.append(
        EndpointCase(
            name=case_name,
            method_name=method_name,
            response_model_attr=model_attr,
            api_id=api_id,
            call_kwargs=dict(kwargs),
            expected_body=dict(EXPECTED_BODY.get(method_name, kwargs)),
            response_payload=payload(case_name),
        )
    )


@pytest.mark.parametrize("case", ACCOUNT_CASES, ids=lambda case: case.name)
def test_overseas_account_requests(monkeypatch, case: EndpointCase):
    run_post_case(
        monkeypatch,
        overseas_account_module,
        OverseasAccount,
        case,
        base_headers={
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
        },
    )
