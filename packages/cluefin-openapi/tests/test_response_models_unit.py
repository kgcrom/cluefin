"""응답 모델에는 길이 제약을 걸지 않는다 — 구조 검사 + 브로커별 동작 예시.

2026-09-02 실측: 키움 ka90001 테마명 하나가 문서 스펙(20자)을 넘자 pydantic 이
`string_too_long` 으로 **응답 전체**를 거부해 desk 테마 화면이 빈 표로 멈췄다.
문서 길이를 응답 모델에 박아 넣으면 서버가 준 정상 값을 거부하는 쪽으로만 작동한다.
그래서 kiwoom·kis·dart 타입 파일의 `max_length` 6,200여 곳을 전부 제거했고, 이 테스트는
누가 문서를 보고 다시 넣는 것을 막는다.
"""

import re
from pathlib import Path

import pytest

from cluefin_openapi.dart._periodic_report_key_information_types import DividendInformationItem
from cluefin_openapi.kis._domestic_basic_quote_types import DomesticStockCurrentPrice
from cluefin_openapi.kiwoom._domestic_theme_types import DomesticThemeGroup

SRC = Path(__file__).resolve().parents[1] / "src" / "cluefin_openapi"
BROKERS = ("kiwoom", "kis", "dart")

# Field(..., max_length=N) 만 잡는다. json_schema_extra={"max_length": N} 은 스키마 메타데이터라
# 검증에 관여하지 않으므로 허용한다.
FIELD_MAX_LENGTH = re.compile(r"\bmax_length\s*=\s*\d+")


def _response_model_files():
    files = [p for broker in BROKERS for p in (SRC / broker).glob("*_types.py")]
    files.append(SRC / "kis" / "_model.py")
    return files


@pytest.mark.parametrize("path", _response_model_files(), ids=lambda p: f"{p.parent.name}/{p.name}")
def test_response_models_declare_no_max_length(path: Path):
    offenders = [
        f"{path.name}:{lineno}"
        for lineno, line in enumerate(path.read_text().splitlines(), 1)
        if FIELD_MAX_LENGTH.search(line)
    ]
    assert not offenders, (
        "응답 모델에 max_length 가 다시 들어왔다 — 실서버가 문서보다 긴 정상 값을 주면 응답 전체가 거부된다: "
        + ", ".join(offenders)
    )


class TestLongValuesAreAccepted:
    """문서 길이(대개 20자)를 훌쩍 넘는 값이 각 브로커 모델을 통과해야 한다."""

    def test_kiwoom(self):
        long_name = "2차전지(전고체) 및 폐배터리 리사이클링 밸류체인 관련주 묶음"
        body = DomesticThemeGroup.model_validate(
            {"return_code": 0, "return_msg": "OK", "thema_grp": [{"thema_grp_cd": "319", "thema_nm": long_name}]}
        )
        assert body.thema_grp[0].thema_nm == long_name

    def test_kis(self):
        long_msg = "정상처리 되었습니다. " * 10  # 문서상 msg1 은 80자
        body = DomesticStockCurrentPrice.model_validate(
            {"rt_cd": "0", "msg_cd": "MCA00000", "msg1": long_msg, "output": None}
        )
        assert body.msg1 == long_msg

    def test_dart(self):
        long_se = "주당 현금배당금(원) — 중간배당 및 결산배당 합산, 우선주 포함 기준"
        item = DividendInformationItem.model_validate(
            {
                "rcept_no": "20260311000123",
                "corp_cls": "Y",
                "corp_code": "00126380",
                "corp_name": "삼성전자",
                "se": long_se,
                "thstrm": "361",
                "frmtrm": "361",
                "lwfr": "361",
                "stlm_dt": "2025-12-31",
            }
        )
        assert item.se == long_se
