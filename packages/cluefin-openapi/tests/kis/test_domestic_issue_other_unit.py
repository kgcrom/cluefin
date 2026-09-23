import pytest

from cluefin_openapi.kis import _domestic_issue_other as domestic_issue_other_module
from cluefin_openapi.kis._domestic_issue_other import DomesticIssueOther
from cluefin_openapi.kis._domestic_issue_other_types import InterestRateSummary

from ._case_runner import CASE_FIELDS, load_cases, run_case

DOMESTIC_ISSUE_OTHER_CASES = load_cases("domestic_issue_other_cases.json", relative_to=__file__)


@pytest.mark.parametrize(CASE_FIELDS, DOMESTIC_ISSUE_OTHER_CASES)
def test_domestic_issue_other_builds_request(
    monkeypatch,
    method_name,
    response_model_attr,
    endpoint,
    method,
    call_kwargs,
    expected_headers,
    expected_body,
    response_payload,
):
    run_case(
        module=domestic_issue_other_module,
        wrapper_cls=DomesticIssueOther,
        monkeypatch=monkeypatch,
        method_name=method_name,
        response_model_attr=response_model_attr,
        endpoint=endpoint,
        method=method,
        call_kwargs=call_kwargs,
        expected_headers=expected_headers,
        expected_body=expected_body,
        response_payload=response_payload,
    )


def test_interest_rate_summary_parses_domestic_and_foreign_rows():
    """div_cls_code="2" 의 output1 에는 국내(Y01xx)와 해외(Y02xx)가 함께 온다 (2026-09-20 실측)."""
    payload = {
        "rt_cd": "0",
        "msg_cd": "MCA00000",
        "msg1": "정상처리 되었습니다.",
        "output1": [
            {
                "bcdt_code": "Y0106",
                "hts_kor_isnm": "국고채 10년",
                "bond_mnrt_prpr": "4.4660",
                "prdy_vrss_sign": "5",
                "bond_mnrt_prdy_vrss": "-0.0400",
                "prdy_ctrt": "-0.89",
                "stck_bsop_date": "20260918",
            },
            {
                "bcdt_code": "Y0202",
                "hts_kor_isnm": "미국 10년T-NOTE 수익률",
                "bond_mnrt_prpr": "5.0100",
                "prdy_vrss_sign": "2",
                "bond_mnrt_prdy_vrss": "0.0700",
                "prdy_ctrt": "1.42",
                "stck_bsop_date": "20260918",
            },
        ],
        "output2": [],
    }

    body = InterestRateSummary.model_validate(payload)

    assert [item.bcdt_code for item in body.output1] == ["Y0106", "Y0202"]
    assert body.output1[0].hts_kor_isnm == "국고채 10년"


def test_interest_rate_summary_accepts_degraded_output2_rows():
    """div_cls_code="1" 의 output2 앞부분은 KIS 가 필드를 밀어 보내고 날짜도 빠뜨린다.

    모델은 이 응답을 거부하지 않아야 한다(전체 응답이 통째로 날아가므로). 밀린 행을
    걸러내는 것은 읽는 쪽의 몫이다 — cluefin-openapi-cli 의 market.interest_rate 핸들러.
    """
    payload = {
        "rt_cd": "0",
        "msg_cd": "MCA00000",
        "msg1": "정상처리 되었습니다.",
        "output1": [],
        "output2": [
            {
                "bcdt_code": "Y0101",
                "hts_kor_isnm": "Y0109",
                "bond_mnrt_prpr": "Y0117",
                "prdy_vrss_sign": "국고채 30년",
                "bond_mnrt_prdy_vrss": "4.5730",
                "bstp_nmix_prdy_ctrt": "5",
                "stck_bsop_date": "-0.0340",
            },
            {
                "bcdt_code": "Y0110",
                "hts_kor_isnm": "Y0198",
                "bond_mnrt_prpr": "Call 지수",
                "prdy_vrss_sign": "204.2551",
                "bond_mnrt_prdy_vrss": "2",
                "bstp_nmix_prdy_ctrt": "0.0346",
            },
        ],
    }

    body = InterestRateSummary.model_validate(payload)

    assert body.output2[0].hts_kor_isnm == "Y0109"
    assert body.output2[1].stck_bsop_date == ""
