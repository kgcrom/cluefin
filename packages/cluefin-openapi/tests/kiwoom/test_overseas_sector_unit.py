import inspect
import re

import pytest

from cluefin_openapi.kiwoom import _overseas_sector as overseas_sector_module
from cluefin_openapi.kiwoom._overseas_sector import OverseasSector

from ._helpers import EndpointCase, run_post_case

CALL_KWARGS = {
    "get_industry_period_profit_rate": {"stex_tp": "3", "inds_cd": "000"},
    "get_industry_fluctuation_rank": {"stex_tp": "3", "sort_tp": "1", "inds_cd": "000"},
}


def payload(name: str):
    return {"return_code": 0, "return_msg": "OK", "endpoint": name}


def method_metadata(method_name: str) -> tuple[str, str]:
    method = getattr(OverseasSector, method_name)
    source = inspect.getsource(method)
    api_id = re.search(r'"api-id":\s*"([^"]+)"', source).group(1)
    model_attr = re.search(r"res_body = (\w+)\.model_validate", source).group(1)
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
def test_overseas_sector_requests(monkeypatch, case: EndpointCase):
    run_post_case(
        monkeypatch,
        overseas_sector_module,
        OverseasSector,
        case,
        base_headers={
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
        },
    )
