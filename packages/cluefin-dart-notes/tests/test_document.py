from pathlib import Path

import pytest

from cluefin_dart_notes import DartDocument, DartXmlRepairer, DartXmlRepairError, Section, load_document, parse_document


def test_recent_periodic_metadata(periodic_recent_bytes):
    document = parse_document(periodic_recent_bytes)

    assert document.document_name == "반기보고서"
    assert document.document_code == "11012"
    assert document.company_name == "가나다 주식회사"
    assert document.corp_code == "00000001"
    assert document.formula_version == "6.7"
    assert document.encoding == "utf-8"
    assert dict(document.summary) == {"IFRS_YN": "Y"}
    assert document.is_periodic_report and not document.is_audit_report
    assert document.rcept_no is None


def test_legacy_metadata_lives_in_document_header(periodic_legacy_bytes):
    document = parse_document(periodic_legacy_bytes)

    assert document.document_name == "사업보고서"
    assert document.document_code == "11011"
    assert document.company_name == "라마바(주)"
    assert document.formula_version == "3.2"
    assert document.encoding == "cp949"
    assert dict(document.summary) == {}
    assert document.repair is not None and document.repair.reports


def test_audit_report_summary(audit_report_bytes):
    document = parse_document(audit_report_bytes)

    assert document.is_audit_report and not document.is_periodic_report
    assert dict(document.summary) == {"AUDIT_CIK": "00000009", "TOT_ASSETS": "1,234"}


def test_section_tree_passes_through_library_and_keeps_order(periodic_recent_bytes):
    document = parse_document(periodic_recent_bytes)

    assert [(s.level, s.title) for s in document.sections] == [
        (1, "정 정 신 고 (보고)"),
        (1, "【 대표이사 등의 확인 】"),
        (1, "I. 회사의 개요"),
        (1, "II. 사업의 내용"),
        (1, "III. 재무에 관한 사항"),
    ]
    business = document.sections[3]
    assert [child.assoc_code for child in business.children] == ["L-0-2-1-L1", "L-0-2-2-L1"]
    finance = document.sections[4]
    assert [child.title for child in finance.children] == [
        "3. 연결재무제표 주석",
        "7. 증권의 발행을 통한 자금조달에 관한 사항",
    ]
    assert finance.children[1].children[0].level == 3


def test_section_attributes(periodic_recent_bytes):
    document = parse_document(periodic_recent_bytes)
    correction, _, overview, *_ = document.sections

    assert correction.is_correction
    assert correction.assoc_code == "CORRECTION"
    assert correction.title_en == "Report of Disclosure Revision"
    assert overview.assoc_code is None
    assert overview.toc_id == "3"
    assert overview.title_en == "I. Overview"
    assert overview.children[1].title == "2. 회사의 연혁"
    assert overview.element is not None and overview.element.tag == "SECTION-1"


def test_legacy_sections_have_no_english_title_or_toc_id(periodic_legacy_bytes):
    document = parse_document(periodic_legacy_bytes)

    assert all(s.title_en is None and s.toc_id is None for s in document.iter_sections())
    assert not any(s.is_correction for s in document.iter_sections())


def test_iter_sections_is_preorder(periodic_recent_bytes):
    titles = [s.title for s in parse_document(periodic_recent_bytes).iter_sections()]

    assert titles.index("I. 회사의 개요") < titles.index("1. 회사의 개요") < titles.index("II. 사업의 내용")
    assert len(titles) == 12


def test_load_document_reads_rcept_no_from_file_name(tmp_path: Path, periodic_recent_bytes):
    path = tmp_path / "20260101000001.xml"
    path.write_bytes(periodic_recent_bytes)

    document = load_document(path)

    assert isinstance(document, DartDocument)
    assert document.rcept_no == "20260101000001"


def test_document_code_falls_back_to_file_name_suffix(audit_report_bytes):
    raw = audit_report_bytes.replace(b' ACODE="00761"', b"")

    document = parse_document(raw, file_name="20260101000001_00761.xml")

    assert document.document_code == "00761"
    assert document.rcept_no == "20260101000001"


def test_custom_repairer_is_used(periodic_legacy_bytes):
    with pytest.raises(DartXmlRepairError):
        parse_document(periodic_legacy_bytes, repairer=DartXmlRepairer(rules=(), strict=True))


def test_section_without_element_has_no_blocks():
    assert Section("제목", None, None, None, 1).blocks == ()


def test_unrecognized_file_name_is_ignored(periodic_recent_bytes):
    assert parse_document(periodic_recent_bytes, file_name="document.xml").rcept_no is None
