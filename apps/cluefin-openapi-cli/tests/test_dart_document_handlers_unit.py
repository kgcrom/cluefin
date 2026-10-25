"""`dart document-*` / `dart financial-notes`: download -> cluefin-dart-notes -> blocks.

The documents are synthetic fragments shaped like the observed dart4 layout, not real filings
(cluefin-dart-notes AGENTS.md: no real filing or company name in the repo).
"""

from __future__ import annotations

import json
from pathlib import Path

import cluefin_dart_notes
import pytest
from cluefin_openapi.dart import DartAPIError

from cluefin_openapi_cli import registry as registry_module
from cluefin_openapi_cli.errors import CliError, classify_exception
from cluefin_openapi_cli.handlers import dart as handlers
from cluefin_openapi_cli.main import run_cli
from cluefin_openapi_cli.registry import EmptyRegistry, RpcRegistry, set_registry_provider

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


# --- document-section ------------------------------------------------------


def _section(params: dict, session: _Session | None = None) -> dict:
    return handlers.handle_document_section({"rcept_no": RCEPT, "corp_code": CORP, **params}, session or _Session())


@pytest.mark.parametrize("selectors", [{}, {"section": "business", "index": 2}, {"title": "주석", "assoc_code": "D-*"}])
def test_section_needs_exactly_one_selector_before_any_client(selectors) -> None:
    session = _Session()
    with pytest.raises(CliError) as excinfo:
        _section(selectors, session)
    assert excinfo.value.exit_code == 2 and set(excinfo.value.data["given"]) == set(selectors)
    assert session.get_dart_calls == 0


def test_business_section_includes_subsections_with_markers_and_tables() -> None:
    result = _section({"section": "business"})
    (business,) = result["sections"]
    assert (business["file"], business["index"], business["assoc_code"]) == (f"{RCEPT}.xml", 2, "D-0-2-0-0")
    assert business["blocks"] == [
        {"type": "section", "level": 2, "title": "1. 사업의 개요", "assoc_code": "L-0-2-1-L1"},
        {"type": "paragraph", "text": "R&D 중심의 부품 사업"},
        {"type": "section", "level": 2, "title": "2. 주요 제품 및 서비스", "assoc_code": "L-0-2-2-L1"},
        {"type": "paragraph", "text": "(단위 : 백만원)"},
        {"type": "table", "caption": None, "unit": "백만원", "rows": [["제품", "매출액"], ["부품", "1,234"]]},
    ]
    assert result["selector"] == {"section": "business"} and result["truncated"] is False
    assert result["total_chars"] == result["returned_chars"]
    json.dumps(result)


def test_section_sizes_match_the_outline() -> None:
    outline = {s["index"]: s["chars"] for d in _outline()["documents"] for s in d["sections"]}
    for index in outline:
        assert _section({"index": index})["total_chars"] == outline[index]


def test_named_sections() -> None:
    (overview,) = _section({"section": "business-overview"})["sections"]
    assert overview["assoc_code"] == "L-0-2-1-L1"
    (company,) = _section({"section": "company-overview"})["sections"]
    assert company["title"] == "I. 회사의 개요"


@pytest.mark.parametrize("name", ["business", "business-overview", "company-overview"])
def test_named_section_on_an_audit_report_only_filing_is_exit_2(name) -> None:
    with pytest.raises(CliError) as excinfo:
        _section({"section": name}, _Session({f"{RCEPT}_00760.xml": audit_report()}))
    assert excinfo.value.exit_code == 2 and "audit report" in excinfo.value.hint


def test_assoc_code_glob_title_and_index_selectors() -> None:
    subsections = _section({"assoc_code": "L-0-2-*"})["sections"]
    assert [s["assoc_code"] for s in subsections] == ["L-0-2-1-L1", "L-0-2-2-L1"]

    # Same code, other meaning: only the audit report has D-0-1-0-0 (주석).
    (notes,) = _section({"assoc_code": "D-0-1-0-0"})["sections"]
    assert notes["file"] == f"{RCEPT}_00760.xml" and notes["index"] == 8

    (titled,) = _section({"title": "연결재무제표 주석"})["sections"]
    assert titled["title"] == "3. 연결재무제표 주석"

    (indexed,) = _section({"index": 4})["sections"]
    assert indexed["title"] == "2. 주요 제품 및 서비스"


def test_nested_matches_are_returned_once_with_their_parent() -> None:
    # "*0-2-*" matches II. 사업의 내용, both of its subsections and the audit report's D-0-2-0-0.
    with_children = _section({"assoc_code": "*0-2-*"})["sections"]
    assert [s["index"] for s in with_children] == [2, 9]
    own_only = _section({"assoc_code": "*0-2-*", "include_children": False})["sections"]
    assert [s["index"] for s in own_only] == [2, 3, 4, 9]
    assert own_only[0]["blocks"] == []


def test_no_match_is_an_empty_result_with_a_hint() -> None:
    result = _section({"title": "없는 제목"})
    assert result["sections"] == [] and result["total_chars"] == 0
    assert "document-outline" in result["hint"]


def test_max_chars_cuts_at_a_block_boundary() -> None:
    full = _section({"section": "business", "max_chars": 0})
    cut = _section({"section": "business", "max_chars": 30})
    assert cut["total_chars"] == full["total_chars"] == full["returned_chars"]
    assert cut["truncated"] is True and "max-chars" in cut["hint"]
    # 9 (marker) + 13 (paragraph) fit in 30; the next marker (14) does not, and nothing after it is kept.
    assert cut["returned_chars"] == len("1. 사업의 개요") + len("R&D 중심의 부품 사업")
    assert [b["type"] for b in cut["sections"][0]["blocks"]] == ["section", "paragraph"]


def test_first_block_is_kept_even_over_the_cap() -> None:
    result = _section({"index": 4, "max_chars": 1})
    assert [b["type"] for b in result["sections"][0]["blocks"]] == ["paragraph"]
    assert result["truncated"] is True


def test_cap_spans_all_selected_sections() -> None:
    result = _section({"assoc_code": "L-0-2-*", "max_chars": 20})
    first, second = result["sections"]
    assert len(first["blocks"]) == 1 and second["blocks"] == []
    assert result["truncated"] is True


# --- through the CLI ---------------------------------------------------------


class _FakeFactory:
    def __init__(self, files: dict[str, bytes]) -> None:
        self.files = files

    def create(self, broker: str):
        assert broker == "dart"
        return _FakeDart(self.files)


@pytest.fixture
def cli(monkeypatch):
    def install(files: dict[str, bytes] | None = None):
        factory = _FakeFactory(periodic_filing() if files is None else files)
        monkeypatch.setattr(registry_module, "BrokerClientFactory", lambda: factory)
        set_registry_provider(lambda: RpcRegistry(client_factory=factory))

    yield install
    set_registry_provider(EmptyRegistry)


def test_cli_section_flags_and_json(cli) -> None:
    cli()
    result = run_cli(
        ["dart", "document-section", "--rcept-no", RCEPT, "--corp-code", CORP, "--section", "business", "--json"]
    )
    assert result.exit_code == 0, result.stdout
    payload = json.loads(result.stdout)
    assert payload["sections"][0]["assoc_code"] == "D-0-2-0-0"


@pytest.mark.parametrize("bad", [{"index": -1}, {"max_chars": -1}, {"section": "notes"}, {"rcept_no": "123"}])
def test_cli_rejects_bad_section_params_with_exit_2(cli, bad) -> None:
    cli()
    body = {"rcept_no": RCEPT, "corp_code": CORP, "section": "business", **bad}
    result = run_cli(["dart", "document-section", "--params-json", json.dumps(body), "--json"])
    assert result.exit_code == 2, result.stdout


def test_cli_outline_runs(cli) -> None:
    cli()
    result = run_cli(["dart", "document-outline", "--rcept-no", RCEPT, "--corp-code", CORP, "--json"])
    assert result.exit_code == 0, result.stdout
    assert len(json.loads(result.stdout)["documents"]) == 2


# --- financial-notes ---------------------------------------------------------


def notes_report(*, consolidated: str | None = None) -> bytes:
    """An annual report whose consolidated notes need sequence splitting and separate notes have headings.

    Consolidated: 3 is absent (a skip warning) and "8." inside the last note looks like a missed note.
    """
    consolidated = (
        consolidated
        or """
<P>1. 일반사항</P><P>회사는 부품을 만든다.</P>
<P>2. 차입금</P><P>(단위 : 백만원)</P>
<TABLE BORDER="1"><TBODY><TR><TH>차입처</TH><TH>금액</TH></TR><TR><TD>은행</TD><TD>(500)</TD></TR></TBODY></TABLE>
<P>4. 특수관계자 거래</P><P>특수관계자 본문</P>
<P>8. 기타 사항은 다음과 같다.</P>"""
    )
    return f"""<?xml version="1.0" encoding="utf-8"?>
<DOCUMENT>
<DOCUMENT-NAME ACODE="11011">사업보고서</DOCUMENT-NAME>
<FORMULA-VERSION ADATE="20260101">6.7</FORMULA-VERSION>
<COMPANY-NAME AREGCIK="{CORP}">가나다 주식회사</COMPANY-NAME>
<BODY>
<SECTION-1><TITLE ATOC="Y" AASSOCNOTE="D-0-3-0-0">III. 재무에 관한 사항</TITLE>
<LIBRARY>
<SECTION-2><TITLE ATOC="Y" AASSOCNOTE="D-0-3-3-0">3. 연결재무제표 주석</TITLE>{consolidated}
</SECTION-2>
<SECTION-2><TITLE ATOC="Y" AASSOCNOTE="D-0-3-5-0">5. 재무제표 주석</TITLE>
<P>별도 주석 머리말</P>
<TABLE-GROUP><TITLE ATOC="N">1. 일반사항 (별도)</TITLE><P>별도 일반사항</P></TABLE-GROUP>
<TABLE-GROUP><TITLE ATOC="N">9-1. 차입금</TITLE><P>별도 차입금 본문</P></TABLE-GROUP>
<TABLE-GROUP><TITLE ATOC="N">10. 우발부채와 약정사항</TITLE><P>소송 본문</P></TABLE-GROUP>
</SECTION-2>
</LIBRARY>
</SECTION-1>
</BODY>
</DOCUMENT>
""".encode()


def notes_filing(**kwargs) -> dict[str, bytes]:
    return {f"{RCEPT}.xml": notes_report(**kwargs), f"{RCEPT}_00760.xml": audit_report()}


def _notes(params: dict | None = None, files: dict[str, bytes] | None = None) -> dict:
    return handlers.handle_financial_notes(
        {"rcept_no": RCEPT, "corp_code": CORP, **(params or {})}, _Session(notes_filing() if files is None else files)
    )


def test_notes_toc_reads_the_periodic_report_not_its_attached_audit_report() -> None:
    result = _notes()
    assert result["mode"] == "toc" and "total_chars" not in result
    consolidated, separate = result["sources"]
    assert {consolidated["file"], separate["file"]} == {f"{RCEPT}.xml"}
    assert (consolidated["basis"], consolidated["split_method"]) == ("consolidated", "sequence")
    assert [(n["number"], n["title"]) for n in consolidated["notes"]] == [
        ("1", "일반사항"),
        ("2", "차입금"),
        ("4", "특수관계자 거래"),
    ]
    assert consolidated["notes"][1]["tables"] == 1 and "blocks" not in consolidated["notes"][1]
    assert (separate["basis"], separate["split_method"]) == ("separate", "heading")
    assert [(n["number"], n["title"]) for n in separate["notes"]] == [
        ("1", "일반사항"),
        ("9-1", "차입금"),
        ("10", "우발부채와 약정사항"),
    ]
    assert separate["preamble_chars"] == len("별도 주석 머리말")
    json.dumps(result)


def test_splitter_warnings_are_never_dropped() -> None:
    (consolidated,) = _notes({"basis": "consolidated"})["sources"]
    warnings = " ".join(consolidated["warnings"])
    assert "3번 노트가 없습니다" in warnings
    assert "놓쳤을 수 있습니다" in warnings
    # Also in notes mode, and for a source where nothing matched.
    (consolidated,) = _notes({"basis": "consolidated", "notes": "99"})["sources"]
    assert consolidated["notes"] == [] and len(consolidated["warnings"]) == 2


def test_basis_filter() -> None:
    assert [s["basis"] for s in _notes({"basis": "separate"})["sources"]] == ["separate"]


def test_notes_by_number_return_blocks() -> None:
    result = _notes({"notes": "9-1,2"})
    assert result["mode"] == "notes" and result["truncated"] is False
    consolidated, separate = result["sources"]
    (borrowings,) = consolidated["notes"]
    assert borrowings["heading"] == "2. 차입금"
    assert borrowings["blocks"] == [
        {"type": "paragraph", "text": "(단위 : 백만원)"},
        {"type": "table", "caption": None, "unit": "백만원", "rows": [["차입처", "금액"], ["은행", "(500)"]]},
    ]
    assert [n["number"] for n in separate["notes"]] == ["9-1"]
    assert result["total_chars"] == result["returned_chars"] == borrowings["chars"] + separate["notes"][0]["chars"]


def test_notes_by_title_terms_are_or_and_ignore_spaces() -> None:
    result = _notes({"title_contains": "특수 관계자, 우발"})
    consolidated, separate = result["sources"]
    assert [n["number"] for n in consolidated["notes"]] == ["4"]
    assert [n["number"] for n in separate["notes"]] == ["10"]


def test_numbers_and_title_terms_combine_as_a_union() -> None:
    (separate,) = _notes({"basis": "separate", "notes": "1", "title_contains": "우발"})["sources"]
    assert [n["number"] for n in separate["notes"]] == ["1", "10"]


@pytest.mark.parametrize(("code", "basis"), [("00760", "separate"), ("00761", "consolidated")])
def test_audit_report_only_filing_uses_its_notes(code, basis) -> None:
    files = {f"{RCEPT}_{code}.xml": audit_report(code=code)}
    (source,) = _notes(files=files)["sources"]
    assert (source["file"], source["document_code"], source["basis"]) == (f"{RCEPT}_{code}.xml", code, basis)
    assert [n["title"] for n in source["notes"]] == ["일반사항"]


def test_notes_max_chars_cut() -> None:
    result = _notes({"title_contains": "차입금", "max_chars": 15})
    assert result["truncated"] is True and "max-chars" in result["hint"]
    consolidated, separate = result["sources"]
    assert len(consolidated["notes"][0]["blocks"]) == 1 and separate["notes"][0]["blocks"] == []
    # The note itself is still listed with its full size.
    assert separate["notes"][0]["chars"] == len("별도 차입금 본문")


def test_missing_basis_is_empty_with_a_hint() -> None:
    result = handlers.handle_financial_notes(
        {"rcept_no": RCEPT, "corp_code": CORP, "basis": "separate"}, _Session(periodic_filing())
    )
    assert result["sources"] == [] and "document-outline" in result["hint"]


def test_unsplittable_notes_point_to_document_section() -> None:
    files = notes_filing(consolidated="<P>번호 없는 주석 본문</P>")
    result = _notes({"basis": "consolidated"}, files)
    (source,) = result["sources"]
    assert source["notes"] == [] and source["warnings"] == ["노트를 하나도 찾지 못했습니다."]
    assert source["preamble_chars"] == len("번호 없는 주석 본문")
    assert "document-section" in result["hint"]


@pytest.mark.parametrize("bad", [{"notes": "7,"}, {"notes": "a"}, {"basis": "all"}, {"max_chars": -5}])
def test_cli_rejects_bad_notes_params_with_exit_2(cli, bad) -> None:
    cli(notes_filing())
    body = {"rcept_no": RCEPT, "corp_code": CORP, **bad}
    result = run_cli(["dart", "financial-notes", "--params-json", json.dumps(body), "--json"])
    assert result.exit_code == 2, result.stdout


def test_cli_notes_runs(cli) -> None:
    cli(notes_filing())
    result = run_cli(
        ["dart", "financial-notes", "--rcept-no", RCEPT, "--corp-code", CORP, "--title-contains", "차입금", "--json"]
    )
    assert result.exit_code == 0, result.stdout
    assert json.loads(result.stdout)["mode"] == "notes"
