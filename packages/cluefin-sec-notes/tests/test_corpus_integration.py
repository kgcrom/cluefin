"""실제 공시 코퍼스로 읽기를 확인한다. `CLUEFIN_SEC_NOTES_TEST_DIR`가 없으면 건너뛴다."""

from collections import Counter

import pytest

from cluefin_sec_notes import extract_items, load_filing
from cluefin_sec_notes._expectations import FAILED, FIXED, check_expectations, invariant_violations

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


def test_golden_expectations_hold(corpus_filings):
    """기대값이 틀리면 회귀(failed), known_bad가 맞으면 개선(fixed) — 둘 다 manifest를 보고 판단하라는 신호다."""
    problems = []
    for filing in corpus_filings:
        if not filing.entry.get("items") and not filing.entry.get("present") and not filing.entry.get("known_bad"):
            continue
        extraction = extract_items(load_filing(filing.path, form=filing.entry["form"]))
        for check in check_expectations(extraction, filing.entry):
            if check.status in (FAILED, FIXED):
                problems.append(f"{filing.id} {check.key} {check.status}: {check.detail}")
    assert not problems, "\n".join(problems)


def test_smoke_baseline_holds(corpus_filings):
    """스모크 공시는 자동 불변식 위반이 baseline과 같아야 한다. 새 위반은 회귀, 사라진 위반은 개선(baseline 갱신)."""
    problems = []
    for filing in corpus_filings:
        if "baseline" not in filing.entry:
            continue
        extraction = extract_items(load_filing(filing.path, form=filing.entry["form"]))
        now = set(invariant_violations(extraction, sec_items=filing.entry.get("sec_items")))
        before = set(filing.entry["baseline"])
        if now != before:
            problems.append(f"{filing.id} 새 위반 {sorted(now - before)} 사라진 위반 {sorted(before - now)}")
    assert not problems, "\n".join(problems)
