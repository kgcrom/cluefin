import pytest

from cluefin_dart_notes import (
    business_description,
    business_overviews,
    company_overview,
    find_section,
    find_sections,
    parse_document,
)
from cluefin_dart_notes._find import title_key


@pytest.fixture
def recent(periodic_recent_bytes):
    return parse_document(periodic_recent_bytes)


def test_find_by_assoc_code(recent):
    assert find_section(recent, assoc_code="D-0-3-3-0").title == "3. 연결재무제표 주석"
    assert find_section(recent, assoc_code="D-9-9-9-9") is None


def test_find_by_glob_pattern(recent):
    assert [s.assoc_code for s in find_sections(recent, assoc_code="D-0-1-*")] == ["D-0-1-1-0", "D-0-1-2-0"]
    assert [s.assoc_code for s in find_sections(recent, assoc_code="L-0-2-*")] == ["L-0-2-1-L1", "L-0-2-2-L1"]


def test_find_by_title_ignores_number_and_spaces(recent):
    assert find_section(recent, title="연결재무제표 주석").assoc_code == "D-0-3-3-0"
    assert find_section(recent, title="회사의연혁").assoc_code == "D-0-1-2-0"
    assert find_section(recent, title="증권의 발행을 통한 자금조달 실적").level == 3
    # 같은 제목이면 장(I.)과 절(1.)이 모두 맞는다.
    assert [s.level for s in find_sections(recent, title="회사의 개요")] == [1, 2]


def test_find_with_both_conditions(recent):
    assert [s.level for s in find_sections(recent, title="회사의 개요", assoc_code="D-0-1-1-0")] == [2]


def test_find_requires_a_condition(recent):
    with pytest.raises(ValueError):
        find_sections(recent)


@pytest.mark.parametrize(
    ("title", "key"),
    [
        ("III. 재무에 관한 사항", "재무에관한사항"),
        ("7-1. 실적", "실적"),
        ("(첨부)연 결 재 무 제 표", "(첨부)연결재무제표"),
    ],
)
def test_title_key(title, key):
    assert title_key(title) == key


def test_company_overview_finds_chapter_without_code(recent, periodic_legacy_bytes):
    assert company_overview(recent).title == "I. 회사의 개요"
    assert company_overview(parse_document(periodic_legacy_bytes)).title == "I. 회사의 개요"


def test_business_description(recent, periodic_legacy_bytes):
    assert business_description(recent).title == "II. 사업의 내용"
    legacy = business_description(parse_document(periodic_legacy_bytes))
    assert legacy.children == ()


def test_helpers_skip_audit_reports_where_codes_mean_something_else(audit_report_bytes):
    audit = parse_document(audit_report_bytes)

    assert find_section(audit, assoc_code="D-0-2-0-0").title == "외부감사 실시내용"
    assert business_description(audit) is None
    assert company_overview(audit) is None
    assert find_section(audit, title="주석").assoc_code == "D-0-1-0-0"


MULTI_INDUSTRY = """<DOCUMENT><DOCUMENT-NAME ACODE="11012">반기보고서</DOCUMENT-NAME><BODY>
<SECTION-1><TITLE AASSOCNOTE="D-0-2-0-0">II. 사업의 내용</TITLE><LIBRARY>
<SECTION-2><TITLE AASSOCNOTE="L-0-2-1-L1">1. (제조서비스업)사업의 개요</TITLE><P>플랫폼 사업</P></SECTION-2>
<SECTION-2><TITLE AASSOCNOTE="L-0-2-2-L1">2. (제조서비스업)주요 제품 및 서비스</TITLE></SECTION-2>
<SECTION-2><TITLE AASSOCNOTE="L-0-2-1-L2">1. (금융업)사업의 개요</TITLE><P>금융 사업</P></SECTION-2>
<SECTION-2><TITLE AASSOCNOTE="L-0-2-2-L2">2. (금융업)영업의 현황</TITLE></SECTION-2>
</LIBRARY></SECTION-1></BODY></DOCUMENT>""".encode()


def test_business_overviews_returns_every_industry_template():
    document = parse_document(MULTI_INDUSTRY)

    overviews = business_overviews(document)

    assert [s.title for s in overviews] == ["1. (제조서비스업)사업의 개요", "1. (금융업)사업의 개요"]
    assert [s.blocks[0].text for s in overviews] == ["플랫폼 사업", "금융 사업"]
    # find_section 은 첫 번째만 돌려준다 — 이 함수가 필요한 이유
    assert find_section(document, assoc_code="L-0-2-1-*") is overviews[0]


def test_business_overviews_single_template_and_legacy(recent, periodic_legacy_bytes):
    assert [s.assoc_code for s in business_overviews(recent)] == ["L-0-2-1-L1"]
    legacy = parse_document(periodic_legacy_bytes)
    assert business_overviews(legacy) == [business_description(legacy)]


def test_business_overviews_is_empty_for_audit_reports_and_unknown_layouts(audit_report_bytes):
    assert business_overviews(parse_document(audit_report_bytes)) == []
    other = MULTI_INDUSTRY.replace(b"L-0-2-1-L1", b"X-1").replace(b"L-0-2-1-L2", b"X-2")
    assert business_overviews(parse_document(other)) == []
