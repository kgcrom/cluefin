"""실제 공시 코퍼스로 읽기를 확인한다. `CLUEFIN_SEC_NOTES_TEST_DIR`가 없으면 건너뛴다."""

from collections import Counter

import pytest

from cluefin_sec_notes import load_filing

pytestmark = pytest.mark.integration


def test_every_filing_parses_with_its_form_and_known_markup(corpus_filings):
    fixes: Counter[str] = Counter()
    for filing in corpus_filings:
        document = load_filing(filing.path)
        assert document.form == filing.entry["form"], filing.id
        # 처음 보는 태그는 새 마크업 신호다. 확인하고 _tree의 태그 목록에 더하거나 manifest에 허용을 적는다.
        allowed = set(filing.entry.get("allowed_unknown_tags", ()))
        unknown = {tag for tag, _ in document.report.unknown_tags} - allowed
        assert not unknown, (filing.id, unknown)
        fixes.update({fix.kind: fix.count for fix in document.report.fixes})
    print("\n", len(corpus_filings), dict(fixes))
