"""Integration test for consolidated/separate statement extraction against real DART XBRL.

실행하려면 실제 XBRL 압축 해제 디렉토리를 가리키는 환경변수가 필요하다:
    CLUEFIN_XBRL_TEST_DIR=/path/to/xbrl_dir uv run pytest -m integration
"""

import os
from pathlib import Path

import pytest

from cluefin_xbrl import extract_financial_statements, parse_xbrl_directory

_XBRL_DIR = os.environ.get("CLUEFIN_XBRL_TEST_DIR")


@pytest.mark.integration
@pytest.mark.skipif(not _XBRL_DIR, reason="CLUEFIN_XBRL_TEST_DIR 미설정")
def test_consolidated_and_separate_statements_from_real_xbrl():
    doc = parse_xbrl_directory(Path(_XBRL_DIR), include_taxonomy=True)
    result = extract_financial_statements(doc)

    # 연결재무제표 5종이 모두 추출된다
    assert set(result.statements.keys()) == {"BS", "IS", "CIS", "CF", "SCE"}
    assert all(s.is_consolidated for s in result.statements.values())

    # 별도재무제표도 추출된다 (이전에는 폐기되던 부분)
    assert len(result.separate_statements) > 0
    assert all(not s.is_consolidated for s in result.separate_statements.values())

    # 별도 재무상태표는 line item을 가진다
    assert "BS" in result.separate_statements
    assert len(result.separate_statements["BS"].line_items) > 0
