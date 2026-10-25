"""Live check of `dart document-*` / `dart financial-notes` against DART (DART_AUTH_KEY from .env.test).

The filing is not named here (cluefin-dart-notes AGENTS.md: no company in the repo). Set
CLUEFIN_DART_DOCUMENT_RCEPT_NO to a periodic report (사업·반기·분기보고서) filed 2017 or later and
CLUEFIN_DART_DOCUMENT_CORP_CODE to its company; the test is skipped otherwise. Three downloads.
"""

from __future__ import annotations

import os
from pathlib import Path

import dotenv
import pytest
from cluefin_openapi import BrokerClientConfig, BrokerClientFactory

from cluefin_openapi_cli.handlers.dart import handle_document_outline, handle_document_section, handle_financial_notes


class _Session:
    def __init__(self, dart) -> None:
        self._dart = dart

    def get_dart(self):
        return self._dart


@pytest.fixture(scope="module")
def filing() -> tuple[_Session, dict]:
    rcept_no = os.getenv("CLUEFIN_DART_DOCUMENT_RCEPT_NO")
    corp_code = os.getenv("CLUEFIN_DART_DOCUMENT_CORP_CODE")
    if not rcept_no or not corp_code:
        pytest.skip("CLUEFIN_DART_DOCUMENT_RCEPT_NO / CLUEFIN_DART_DOCUMENT_CORP_CODE are not set")
    dotenv.load_dotenv(dotenv_path=Path(__file__).resolve().parents[3] / ".env.test")
    auth_key = os.getenv("DART_AUTH_KEY")
    if not auth_key:
        pytest.skip("DART_AUTH_KEY is not configured")
    # Not BrokerClientConfig.from_env(): it merges the cwd's .env (production) into the config.
    session = _Session(BrokerClientFactory(BrokerClientConfig(dart_auth_key=auth_key)).create("dart"))
    return session, {"rcept_no": rcept_no, "corp_code": corp_code}


@pytest.mark.integration
def test_outline_section_and_notes_agree_on_one_filing(filing) -> None:
    session, base = filing

    outline = handle_document_outline(base, session)
    main = outline["documents"][0]
    assert main["is_periodic_report"]
    assert main["file"] == f"{base['rcept_no']}.xml"
    # The repair rules cover every defect seen so far; the positional fallback means a new one.
    assert not any(document["repair"]["used_fallback"] for document in outline["documents"])
    business = next(s for s in main["sections"] if s["assoc_code"] == "D-0-2-0-0")

    section = handle_document_section({**base, "index": business["index"], "max_chars": 0}, session)
    assert section["total_chars"] == section["returned_chars"] == business["chars"] > 0

    toc = handle_financial_notes(base, session)
    assert toc["sources"]
    assert all(source["file"] == main["file"] for source in toc["sources"])
    first = next(source for source in toc["sources"] if source["notes"])
    number = first["notes"][0]["number"]
    notes = handle_financial_notes({**base, "basis": first["basis"], "notes": number, "max_chars": 0}, session)
    (read,) = notes["sources"][0]["notes"]
    assert read["number"] == number
    assert read["blocks"]
