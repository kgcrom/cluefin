"""실제 원문 디렉터리로 로딩과 섹션 찾기를 확인한다. `CLUEFIN_DART_NOTES_TEST_DIR`가 없으면 건너뛴다."""

from collections import Counter

import pytest

from cluefin_dart_notes import business_description, company_overview, find_section

pytestmark = pytest.mark.integration


def test_metadata_is_complete(corpus_documents):
    for document in corpus_documents:
        assert document.document_name, document.rcept_no
        assert document.document_code, document.rcept_no
        assert document.corp_code, document.rcept_no
        assert document.is_periodic_report or document.is_audit_report, document.document_code
    print("\n", Counter(document.document_code for document in corpus_documents))


def test_periodic_reports_have_core_sections(corpus_documents):
    for document in (d for d in corpus_documents if d.is_periodic_report):
        assert company_overview(document) is not None, document.rcept_no
        assert business_description(document) is not None, document.rcept_no
        assert find_section(document, assoc_code="D-0-3-3-0") is not None, document.rcept_no
        assert find_section(document, assoc_code="D-0-3-5-0") is not None, document.rcept_no


def test_audit_reports_have_notes(corpus_documents):
    for document in (d for d in corpus_documents if d.is_audit_report):
        assert find_section(document, title="주석") is not None, document.rcept_no
