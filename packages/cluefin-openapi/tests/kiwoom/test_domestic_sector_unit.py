import inspect
import re

import pytest

from cluefin_openapi.kiwoom import _domestic_sector as sector_module
from cluefin_openapi.kiwoom._domestic_sector import DomesticSector

from ._helpers import EndpointCase, run_post_case

CALL_KWARGS = {
    "get_industry_program": {"stk_code": "005930"},
    "get_industry_investor_net_buy": {
        "mrkt_tp": "0",
        "amt_qty_tp": "0",
        "base_dt": "20230101",
        "stex_tp": "1",
    },
    "get_industry_current_price": {
        "mrkt_tp": "0",
        "inds_cd": "001",
    },
    "get_industry_price_by_sector": {
        "mrkt_tp": "0",
        "inds_cd": "001",
        "stex_tp": "1",
    },
    "get_all_industry_index": {
        "inds_cd": "001",
    },
    "get_daily_industry_current_price": {
        "mrkt_tp": "0",
        "inds_cd": "001",
    },
}


def payload(name: str):
    return {"return_code": 0, "return_msg": "OK", "endpoint": name}


def method_metadata(method_name: str) -> tuple[str, str]:
    method = getattr(DomesticSector, method_name)
    source = inspect.getsource(method)
    api_id = re.search(r'"api-id":\s*"([^"]+)"', source).group(1)
    model_attr = re.search(r"= (DomesticSector\w+)\.model_validate", source).group(1)
    return api_id, model_attr


SECTOR_CASES = []
for method_name, kwargs in CALL_KWARGS.items():
    api_id, model_attr = method_metadata(method_name)
    case_name = method_name.removeprefix("get_")
    SECTOR_CASES.append(
        EndpointCase(
            name=case_name,
            method_name=method_name,
            response_model_attr=model_attr,
            api_id=api_id,
            call_kwargs=dict(kwargs),
            expected_body=dict(kwargs),
            response_payload=payload(case_name),
        )
    )


@pytest.mark.parametrize("case", SECTOR_CASES, ids=lambda case: case.name)
def test_domestic_sector_requests(monkeypatch, case: EndpointCase):
    run_post_case(
        monkeypatch,
        sector_module,
        DomesticSector,
        case,
        base_headers={
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
        },
    )
