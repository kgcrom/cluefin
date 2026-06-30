"""Integration test for extract_notes against a real DART XBRL directory.

실행하려면 실제 XBRL 압축 해제 디렉토리를 가리키는 환경변수가 필요하다:
    CLUEFIN_XBRL_TEST_DIR=/path/to/xbrl_dir uv run pytest -m integration
"""

import os
from pathlib import Path

import pytest

from cluefin_xbrl import extract_notes, parse_xbrl_directory

_XBRL_DIR = os.environ.get("CLUEFIN_XBRL_TEST_DIR")


@pytest.mark.integration
@pytest.mark.skipif(not _XBRL_DIR, reason="CLUEFIN_XBRL_TEST_DIR 미설정")
def test_extract_notes_from_real_xbrl():
    doc = parse_xbrl_directory(Path(_XBRL_DIR), include_taxonomy=True)
    parsed = extract_notes(doc)

    # 주석이 다수 추출된다
    assert len(parsed.notes) > 0

    # 모든 role_code는 D8로 시작
    assert all(code.startswith("D8") for code in parsed.notes)

    # 주요 주석(종업원급여)이 존재하고 차원이 보존된다
    assert any(s.title and "종업원급여" in s.title for s in parsed.notes.values())
    assert any(li.dimensions for s in parsed.notes.values() for li in s.line_items)
