"""`dart document-*` / `dart financial-notes`: download -> cluefin-dart-notes -> blocks.

The documents are synthetic fragments shaped like the observed dart4 layout, not real filings
(cluefin-dart-notes AGENTS.md: no real filing or company name in the repo).
"""

from __future__ import annotations

import json
from pathlib import Path

import cluefin_dart_notes
import pytest
from cluefin_openapi.dart._exceptions import DartAPIError

from cluefin_openapi_cli.errors import CliError, classify_exception
from cluefin_openapi_cli.handlers import dart as handlers

CORP = "00000001"
OTHER_CORP = "00000002"
RCEPT = "20260814000001"


def periodic_report(corp: str = CORP) -> bytes:
    return f"""<?xml version="1.0" encoding="utf-8"?>
<DOCUMENT>
<DOCUMENT-NAME ACODE="11012">반기보고서</DOCUMENT-NAME>
<FORMULA-VERSION ADATE="20260101">6.7</FORMULA-VERSION>
<COMPANY-NAME AREGCIK="{corp}">가나다 주식회사</COMPANY-NAME>
<SUMMARY><EXTRACTION ACODE="IFRS_YN">Y</EXTRACTION></SUMMARY>
<BODY>
<SECTION-1><TITLE ATOC="Y">I. 회사의 개요</TITLE>
<SECTION-2><TITLE ATOC="Y" AASSOCNOTE="D-0-1-1-0">1. 회사의 개요</TITLE><P>회사 소개 본문</P></SECTION-2>
</SECTION-1>
<SECTION-1><TITLE ATOC="Y" AASSOCNOTE="D-0-2-0-0">II. 사업의 내용</TITLE>
<LIBRARY>
<SECTION-2><TITLE ATOC="Y" AASSOCNOTE="L-0-2-1-L1">1. 사업의 개요</TITLE><P>R&D 중심의 부품 사업</P></SECTION-2>
<SECTION-2><TITLE ATOC="Y" AASSOCNOTE="L-0-2-2-L1">2. 주요 제품 및 서비스</TITLE>
<P>(단위 : 백만원)</P>
<TABLE BORDER="1"><TBODY>
<TR><TH>제품</TH><TH>매출액</TH></TR>
<TR><TD>부품</TD><TD>1,234</TD></TR>
</TBODY></TABLE>
</SECTION-2>
</LIBRARY>
</SECTION-1>
<SECTION-1><TITLE ATOC="Y" AASSOCNOTE="D-0-3-0-0">III. 재무에 관한 사항</TITLE>
<LIBRARY>
<SECTION-2><TITLE ATOC="Y" AASSOCNOTE="D-0-3-3-0">3. 연결재무제표 주석</TITLE>
<P>1. 일반사항</P><P>회사는 부품을 만든다.</P>
<P>2. 차입금</P><P>단기차입금 본문</P>
</SECTION-2>
</LIBRARY>
</SECTION-1>
</BODY>
</DOCUMENT>
""".encode()


def audit_report(corp: str = CORP, code: str = "00760") -> bytes:
    name = "연결감사보고서" if code == "00761" else "감사보고서"
    return f"""<?xml version="1.0" encoding="utf-8"?>
<DOCUMENT>
<DOCUMENT-NAME ACODE="{code}">{name}</DOCUMENT-NAME>
<FORMULA-VERSION ADATE="20260101">6.0</FORMULA-VERSION>
<COMPANY-NAME AREGCIK="{corp}">가나다 주식회사</COMPANY-NAME>
<SUMMARY><EXTRACTION ACODE="AUDIT_CIK">00000009</EXTRACTION></SUMMARY>
<BODY>
<SECTION-1><TITLE ATOC="Y" AASSOCNOTE="D-0-0-0-0">(첨부)재 무 제 표</TITLE>
<SECTION-2><TITLE ATOC="Y" AASSOCNOTE="D-0-1-0-0">주석</TITLE><P>1. 일반사항</P><P>감사보고서 주석 본문</P></SECTION-2>
</SECTION-1>
<SECTION-1><TITLE ATOC="Y" AASSOCNOTE="D-0-2-0-0">외부감사 실시내용</TITLE><P>감사 일정</P></SECTION-1>
</BODY>
</DOCUMENT>
""".encode()


def periodic_filing(corp: str = CORP, audit_corp: str | None = None) -> dict[str, bytes]:
    """A periodic report ZIP: the main document plus its attached audit report (written in reverse order)."""
    return {f"{RCEPT}_00760.xml": audit_report(audit_corp or corp), f"{RCEPT}.xml": periodic_report(corp)}


class _FakePublicDisclosure:
    def __init__(self, files: dict[str, bytes], error: Exception | None = None) -> None:
        self.files = files
        self.error = error
        self.calls: list[str] = []
        self.destinations: list[Path] = []

    def disclosure_document_files(self, rcept_no, *, destination, overwrite=False):
        self.calls.append(rcept_no)
        destination = Path(destination)
        self.destinations.append(destination)
        if self.error is not None:
            raise self.error
        for name, data in self.files.items():
            (destination / name).write_bytes(data)
        return [destination / name for name in self.files]


class _FakeDart:
    def __init__(self, files: dict[str, bytes], error: Exception | None = None) -> None:
        self.public_disclosure = _FakePublicDisclosure(files, error)


class _Session:
    def __init__(self, files: dict[str, bytes] | None = None, error: Exception | None = None) -> None:
        self.dart = _FakeDart(periodic_filing() if files is None else files, error)
        self.get_dart_calls = 0

    def get_dart(self) -> _FakeDart:
        self.get_dart_calls += 1
        return self.dart


def _outline(params: dict | None = None, session: _Session | None = None) -> dict:
    return handlers.handle_document_outline(
        {"rcept_no": RCEPT, "corp_code": CORP, **(params or {})}, session or _Session()
    )


# --- shared loader ---------------------------------------------------------


def test_main_document_comes_first_whatever_order_the_zip_had() -> None:
    result = _outline()
    assert [d["file"] for d in result["documents"]] == [f"{RCEPT}.xml", f"{RCEPT}_00760.xml"]
    assert [d["document_code"] for d in result["documents"]] == ["11012", "00760"]
    assert result["rcept_no"] == RCEPT and result["corp_code"] == CORP
    json.dumps(result)


def test_audit_report_only_filing() -> None:
    result = _outline(session=_Session({f"{RCEPT}_00760.xml": audit_report()}))
    (document,) = result["documents"]
    assert document["is_audit_report"] and not document["is_periodic_report"]
    assert document["summary"] == {"AUDIT_CIK": "00000009"}


@pytest.mark.parametrize("files", [periodic_filing(OTHER_CORP), periodic_filing(audit_corp=OTHER_CORP)])
def test_another_company_in_any_file_is_exit_4(files) -> None:
    with pytest.raises(CliError) as excinfo:
        _outline(session=_Session(files))
    err = excinfo.value
    assert err.exit_code == 4 and err.error_type == "ResponseParseError"
    assert err.data["expected"] == CORP and OTHER_CORP in err.data["actual"]


def test_filing_before_2017_is_exit_2_without_touching_the_client() -> None:
    session = _Session()
    with pytest.raises(CliError) as excinfo:
        _outline({"rcept_no": "20160330000001"}, session)
    assert excinfo.value.exit_code == 2 and "2017" in (excinfo.value.hint or "")
    assert session.get_dart_calls == 0


def test_no_xml_in_the_download_is_exit_4() -> None:
    with pytest.raises(CliError) as excinfo:
        _outline(session=_Session({}))
    assert excinfo.value.exit_code == 4 and excinfo.value.error_type == "ResponseParseError"


def test_unparseable_document_is_exit_4(monkeypatch) -> None:
    def broken(path, **kwargs):
        raise cluefin_dart_notes.DartXmlRepairError("cannot repair")

    monkeypatch.setattr(cluefin_dart_notes, "load_document", broken)
    with pytest.raises(CliError) as excinfo:
        _outline()
    assert excinfo.value.exit_code == 4 and excinfo.value.data["exception"] == "DartXmlRepairError"


def test_dart_quota_status_propagates_and_classifies_as_exit_5() -> None:
    error = DartAPIError("사용한도를 초과하였습니다.", response_data={"status": "020", "message": "한도 초과"})
    with pytest.raises(DartAPIError) as excinfo:
        _outline(session=_Session(error=error))
    assert classify_exception(excinfo.value, command="dart.document-outline", broker="dart").exit_code == 5


@pytest.mark.parametrize("error", [None, RuntimeError("boom")])
def test_temp_directory_is_removed(error) -> None:
    session = _Session(error=error)
    try:
        _outline(session=session)
    except RuntimeError:
        pass
    (destination,) = session.dart.public_disclosure.destinations
    assert not destination.exists()


# --- document-outline ------------------------------------------------------


def test_outline_numbers_sections_across_the_whole_filing() -> None:
    main, audit = _outline()["documents"]
    titles = [(s["index"], s["level"], s["title"]) for s in main["sections"]]
    assert titles == [
        (0, 1, "I. 회사의 개요"),
        (1, 2, "1. 회사의 개요"),
        (2, 1, "II. 사업의 내용"),
        (3, 2, "1. 사업의 개요"),
        (4, 2, "2. 주요 제품 및 서비스"),
        (5, 1, "III. 재무에 관한 사항"),
        (6, 2, "3. 연결재무제표 주석"),
    ]
    assert [s["index"] for s in audit["sections"]] == [7, 8, 9]
    assert audit["sections"][1]["assoc_code"] == "D-0-1-0-0"


def test_outline_sizes_include_subsections_and_their_titles() -> None:
    sections = {s["title"]: s for s in _outline()["documents"][0]["sections"]}
    overview, products = sections["1. 사업의 개요"], sections["2. 주요 제품 및 서비스"]
    assert overview["chars"] == len("R&D 중심의 부품 사업")
    assert products["tables"] == 1
    assert products["chars"] == len("(단위 : 백만원)") + len("제품매출액부품1,234")
    business = sections["II. 사업의 내용"]
    assert business["tables"] == 1
    assert business["chars"] == len(overview["title"]) + overview["chars"] + len(products["title"]) + products["chars"]


def test_outline_reports_header_summary_and_repair() -> None:
    main = _outline()["documents"][0]
    assert main["document_name"] == "반기보고서" and main["company_name"] == "가나다 주식회사"
    assert main["is_periodic_report"] and not main["is_audit_report"]
    assert main["summary"] == {"IFRS_YN": "Y"}
    assert main["repair"]["used_fallback"] is False
    assert main["repair"]["rules"]["bare-ampersand"] == 1
    assert main["sections"][0]["is_correction"] is False
