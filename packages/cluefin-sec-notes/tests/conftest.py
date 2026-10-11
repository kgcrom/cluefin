"""통합 테스트용 코퍼스. 원문과 manifest는 커밋하지 않는다(기업명 비공개).

- `CLUEFIN_SEC_NOTES_TEST_DIR`: 원문 폴더(`<form>/<accession>/<file>`). 없으면 통합 테스트를 건너뛴다.
- `CLUEFIN_SEC_NOTES_MANIFEST_DIR`: `golden.json`, `smoke-*.json`이 있는 폴더. 기본값 `docs/plans/sec-notes-corpus`.
- `CLUEFIN_SEC_NOTES_MANIFESTS`: 그 폴더에서 돌릴 manifest glob(예: `golden*.json`, `*10q*.json`). 기본값 전부.
  받는 법은 `scripts/fetch_corpus.py`.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[3]


@dataclass(frozen=True)
class CorpusFiling:
    manifest: str
    entry: dict
    path: Path

    @property
    def id(self) -> str:
        return f"{self.manifest}:{self.entry['accession']}"


def _corpus_filings() -> list[CorpusFiling]:
    corpus = os.getenv("CLUEFIN_SEC_NOTES_TEST_DIR")
    if not corpus:
        return []
    manifest_dir = Path(os.getenv("CLUEFIN_SEC_NOTES_MANIFEST_DIR", _REPO_ROOT / "docs" / "plans" / "sec-notes-corpus"))
    filings = []
    for manifest in sorted(manifest_dir.glob(os.getenv("CLUEFIN_SEC_NOTES_MANIFESTS", "*.json"))):
        for entry in json.loads(manifest.read_text()):
            folder = entry["form"].upper().replace("/", "_")
            path = Path(corpus).expanduser() / folder / entry["accession"] / entry["file"]
            filings.append(CorpusFiling(manifest=manifest.stem, entry=entry, path=path))
    return filings


@pytest.fixture(scope="session")
def corpus_filings() -> list[CorpusFiling]:
    filings = _corpus_filings()
    if not filings:
        pytest.skip("CLUEFIN_SEC_NOTES_TEST_DIR 또는 manifest 없음")
    missing = [filing.id for filing in filings if not filing.path.exists()]
    assert not missing, f"원문이 없습니다. scripts/fetch_corpus.py로 받으세요: {missing[:5]}"
    return filings


# 합성 10-K 조각 ---------------------------------------------------------------------------------------------------
# 실제 공시가 아니며, 관찰한 레이아웃 유형만 흉내 낸다. 테스트는 `synthetic` fixture로 쓴다(importlib 모드라
# 테스트 폴더의 도움 모듈을 import할 수 없다).

TOC_ITEMS = (
    ("I", "1", "Business"),
    ("I", "1A", "Risk Factors"),
    ("I", "1B", "Unresolved Staff Comments"),
    ("I", "1C", "Cybersecurity"),
    ("I", "2", "Properties"),
    ("I", "3", "Legal Proceedings"),
    ("I", "4", "Mine Safety Disclosures"),
    (
        "II",
        "5",
        "Market for Registrant’s Common Equity, Related Stockholder Matters and Issuer Purchases of Equity Securities",
    ),
    ("II", "6", "[Reserved]"),
    ("II", "7", "Management’s Discussion and Analysis of Financial Condition and Results of Operations"),
    ("II", "7A", "Quantitative and Qualitative Disclosures About Market Risk"),
    ("II", "8", "Financial Statements and Supplementary Data"),
    ("II", "9", "Changes in and Disagreements with Accountants on Accounting and Financial Disclosure"),
    ("II", "9A", "Controls and Procedures"),
    ("II", "9B", "Other Information"),
    ("II", "9C", "Disclosure Regarding Foreign Jurisdictions that Prevent Inspections"),
    ("III", "10", "Directors, Executive Officers and Corporate Governance"),
    ("III", "11", "Executive Compensation"),
    ("III", "12", "Security Ownership of Certain Beneficial Owners and Management and Related Stockholder Matters"),
    ("III", "13", "Certain Relationships and Related Transactions, and Director Independence"),
    ("III", "14", "Principal Accountant Fees and Services"),
    ("IV", "15", "Exhibits and Financial Statement Schedules"),
    ("IV", "16", "Form 10-K Summary"),
)
COVER = (
    '<div style="display:none"><ix:header><ix:hidden>'
    '<ix:nonNumeric name="dei:DocumentType">10-K</ix:nonNumeric>'
    '<ix:nonNumeric name="dei:DocumentPeriodEndDate">2025-12-31</ix:nonNumeric>'
    "</ix:hidden></ix:header></div><div>FORM 10-K</div>"
)


def anchor_id(number: str) -> str:
    return "i" + number.lower()


def workiva_toc(items=TOC_ITEMS) -> str:
    """Workiva형: 표 하나, 행마다 Item 번호·제목·페이지 칸에 같은 링크."""
    rows = []
    part = None
    for item_part, number, title in items:
        if item_part != part:
            part = item_part
            rows.append(f'<tr><td colspan="3"><a href="#part{part}">Part {part}</a></td></tr>')
        href = f"#{anchor_id(number)}"
        rows.append(
            f'<tr><td><a href="{href}">Item {number}.</a></td><td><a href="{href}">{title}</a></td>'
            f'<td><a href="{href}">{len(rows)}</a></td></tr>'
        )
    return '<div id="toc"></div><table>' + "".join(rows) + "</table>"


def body(items=TOC_ITEMS, *, anchored=True, page_header=False) -> str:
    parts = []
    for _part, number, title in items:
        anchor = f'<div id="{anchor_id(number)}"></div>' if anchored else ""
        header = '<div><a href="#toc">Table of Contents</a></div>' if page_header else ""
        parts.append(
            '<hr style="page-break-after:always"/>'
            + header
            + anchor
            + f'<div style="font-weight:700">Item {number}. {title}</div>'
            + f"<div>Body of item {number}.</div>"
        )
    return "".join(parts) + '<hr style="page-break-after:always"/><div>SIGNATURES</div><div>signed</div>'


def filing(toc: str | None = None, content: str | None = None) -> str:
    return (
        "<html><body>"
        + COVER
        + (workiva_toc() if toc is None else toc)
        + (body() if content is None else content)
        + "</body></html>"
    )


@pytest.fixture
def synthetic() -> SimpleNamespace:
    return SimpleNamespace(TOC_ITEMS=TOC_ITEMS, anchor_id=anchor_id, workiva_toc=workiva_toc, body=body, filing=filing)
