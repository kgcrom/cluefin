import inspect
import re

import pytest

from cluefin_openapi.kiwoom import _domestic_account as account_module
from cluefin_openapi.kiwoom._domestic_account import DomesticAccount

from ._helpers import EndpointCase, run_post_case


def payload(name: str):
    return {"return_code": 0, "return_msg": "OK", "endpoint": name}


CALL_KWARGS = {
    "get_daily_stock_realized_profit_loss_by_date": {"stk_cd": "005930", "strt_dt": "20250630"},
    "get_daily_stock_realized_profit_loss_by_period": {
        "stk_cd": "005930",
        "strt_dt": "20241101",
        "end_dt": "20241130",
    },
    "get_daily_realized_profit_loss": {"strt_dt": "20250601", "end_dt": "20250630"},
    "get_unexecuted": {
        "all_stk_tp": "0",
        "trde_tp": "0",
        "stex_tp": "005930",
        "stk_cd": "0",
    },
    "get_executed": {
        "qry_tp": "005930",
        "sell_tp": "0",
        "stex_tp": "0",
        "stk_cd": "0",
        "ord_no": "0",
    },
    "get_daily_realized_profit_loss_details": {"stk_cd": "005930", "cont_yn": "20241128"},
    "get_account_profit_rate": {
        "stex_tp": "20240601",
        "cont_yn": "20240630",
        "next_key": "1",
    },
    "get_unexecuted_split_order_details": {"ord_no": "1234567890"},
    "get_current_day_trading_journal": {
        "ottks_tp": "20240601",
        "ch_crd_tp": "0",
        "base_dt": "0",
    },
    "get_deposit_balance_details": {"qry_tp": "3"},
    "get_daily_estimated_deposit_asset_balance": {
        "start_dt": "000000100000",
        "end_dt": "20241111",
        "cont_yn": "20241114",
    },
    "get_estimated_asset_balance": {"qry_tp": "1"},
    "get_account_evaluation_status": {"qry_tp": "0", "dmst_stex_tp": "KRX"},
    "get_execution_balance": {"dmst_stex_tp": "KRX"},
    "get_account_order_execution_details": {
        "ord_dt": "20240630",
        "qry_tp": "1",
        "stk_bond_tp": "0",
        "sell_tp": "0",
        "stk_cd": "005930",
        "fr_ord_no": "0",
        "dmst_stex_tp": "%",
    },
    "get_account_next_day_settlement_details": {"strt_dcd_seq": ""},
    "get_account_order_execution_status": {
        "ord_dt": "20240630",
        "stk_bond_tp": "0",
        "mrkt_tp": "0",
        "sell_tp": "0",
        "qry_tp": "0",
        "stk_cd": "005930",
        "fr_ord_no": "0",
        "dmst_stex_tp": "%",
    },
    "get_available_withdrawal_amount": {
        "io_amt": "000000000000",
        "stk_cd": "005930",
        "trde_tp": "1",
        "trde_qty": "0000000000",
        "uv": "000000124500",
        "exp_buy_unp": "000000124500",
    },
    "get_available_order_quantity_by_margin_rate": {"stk_cd": "005930", "uv": "000000124500"},
    "get_available_order_quantity_by_margin_loan_stock": {"stk_cd": "005930", "uv": "000000124500"},
    "get_margin_details": {},
    "get_consignment_comprehensive_transaction_history": {
        "strt_dt": "20240601",
        "end_dt": "20240630",
        "tp": "0",
        "gds_tp": "0",
        "dmst_stex_tp": "%",
        "stk_cd": "005930",
        "crnc_cd": "KRW",
        "frgn_stex_code": "",
    },
    "get_daily_account_profit_rate_details": {
        "fr_dt": "20240601",
        "to_dt": "20240630",
    },
    "get_account_current_day_status": {},
    "get_account_evaluation_balance_details": {"qry_tp": "1", "dmst_stex_tp": "KRX"},
}


def method_metadata(method_name: str) -> tuple[str, str]:
    method = getattr(DomesticAccount, method_name)
    source = inspect.getsource(method)
    api_id = re.search(r'"api-id":\s*"([^"]+)"', source).group(1)
    model_attr = re.search(r"= (DomesticAccount\w+)\.model_validate", source).group(1)
    return api_id, model_attr


ACCOUNT_CASES = []
for method_name in sorted(CALL_KWARGS):
    raw_kwargs = dict(CALL_KWARGS[method_name])
    cont_value = raw_kwargs.pop("cont_yn", "N")
    next_key = raw_kwargs.pop("next_key", "")
    api_id, model_attr = method_metadata(method_name)
    ACCOUNT_CASES.append(
        EndpointCase(
            name=method_name.removeprefix("get_"),
            method_name=method_name,
            response_model_attr=model_attr,
            api_id=api_id,
            call_kwargs=dict(raw_kwargs),
            expected_body=dict(raw_kwargs),
            response_payload=payload(method_name.removeprefix("get_")),
            cont_flag_key="con-yn",
            cont_flag_value=cont_value,
            next_key=next_key,
        )
    )


@pytest.mark.parametrize("case", ACCOUNT_CASES, ids=lambda case: case.name)
def test_domestic_account_requests(monkeypatch, case: EndpointCase):
    run_post_case(
        monkeypatch,
        account_module,
        DomesticAccount,
        case,
        base_headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
