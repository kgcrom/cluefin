# cluefin-xbrl extract_notes() Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `cluefin-xbrl`에 재무제표 주석(D8 disclosure) 추출 API `extract_notes()`를 추가한다.

**Architecture:** 신규 모듈 `notes.py`가 이미 파싱된 `XbrlDocument`(facts + taxonomy)를 입력받아, presentation linkrole 중 D8 주석 role만 선별해 차원을 보존한 `NoteSection` 컬렉션으로 구조화한다. 기존 `statements.py`/`parser.py`/`taxonomy.py`는 변경하지 않는다. `extract_notes`는 Arelle를 호출하지 않으므로 단위 테스트는 합성 `XbrlDocument`를 파이썬으로 직접 구성해 검증한다(별도 XBRL 픽스처 불필요).

**Tech Stack:** Python ≥3.10, pydantic v2, pytest. (arelle-release는 파싱 단계에만 쓰이며 본 기능엔 직접 사용 없음.)

## Global Constraints

- Python 명령은 `uv run`으로 실행한다.
- pydantic `>=2.12.0,<3.0.0`, 신규 런타임 의존성 추가 금지.
- ruff: line-length 120, target py310, lint select `E,F,W,B,Q,I,ASYNC,T20` (F401·E501 ignore, tests에서 T201 허용).
- 커밋 메시지는 Conventional Commits (`type(scope): 설명`), 한국어 본문.
- 시크릿/`.env` 미포함.
- 기존 `extract_financial_statements` 동작·테스트 불변.

---

## File Structure

- Create: `packages/cluefin-xbrl/src/cluefin_xbrl/notes.py` — 주석 추출 로직.
- Modify: `packages/cluefin-xbrl/src/cluefin_xbrl/_types.py` — `NoteLineItem`, `NoteSection`, `ParsedNotes` 모델 추가.
- Modify: `packages/cluefin-xbrl/src/cluefin_xbrl/__init__.py` — 신규 심볼 export.
- Create: `packages/cluefin-xbrl/tests/test_notes.py` — 단위 테스트.
- Create: `packages/cluefin-xbrl/tests/test_notes_integration.py` — 통합 테스트(env var gated).

---

## Phase 1: 주석 모델 추가 (`_types.py`)

**Files:**
- Modify: `packages/cluefin-xbrl/src/cluefin_xbrl/_types.py` (파일 끝에 추가)
- Test: `packages/cluefin-xbrl/tests/test_notes.py`

**Interfaces:**
- Produces: `NoteLineItem`, `NoteSection`, `ParsedNotes` pydantic 모델 (필드는 아래 구현 참조).

- [ ] **Step 1: 실패하는 테스트 작성** — `tests/test_notes.py` 생성

```python
"""Tests for financial statement note extraction."""

from decimal import Decimal

import pytest

from cluefin_xbrl._types import (
    ConceptLabel,
    NoteLineItem,
    NoteSection,
    ParsedNotes,
    PeriodType,
    PresentationNode,
    TaxonomyInfo,
    XbrlDocument,
    XbrlFact,
    XbrlPeriod,
)


class TestNoteModels:
    def test_note_line_item_defaults(self):
        item = NoteLineItem(concept_local_name="A", concept_qname="ns:A")
        assert item.dimensions == {}
        assert item.is_abstract is False
        assert item.value is None

    def test_note_line_item_dimensions(self):
        item = NoteLineItem(
            concept_local_name="A",
            concept_qname="ns:A",
            value=Decimal("1000"),
            dimensions={"ns:Axis": "ns:Member"},
        )
        assert item.dimensions == {"ns:Axis": "ns:Member"}
        assert item.value == Decimal("1000")

    def test_note_section_defaults(self):
        section = NoteSection(role_code="D834480", role_uri="http://x/role-D834480")
        assert section.is_consolidated is True
        assert section.line_items == []
        assert section.title is None

    def test_parsed_notes_defaults(self):
        parsed = ParsedNotes(source_file="x.xbrl")
        assert parsed.notes == {}
        assert parsed.entity_id is None
```

- [ ] **Step 2: 테스트 실패 확인**

Run: `uv run pytest packages/cluefin-xbrl/tests/test_notes.py -v`
Expected: FAIL — `ImportError: cannot import name 'NoteLineItem'`

- [ ] **Step 3: 모델 구현** — `_types.py` 파일 끝에 추가

```python
class NoteLineItem(BaseModel):
    """A single line item in a financial statement note, with dimensional context."""

    concept_local_name: str
    concept_qname: str
    label_ko: Optional[str] = None
    label_en: Optional[str] = None
    value: Optional[Decimal] = None
    unit: Optional[str] = None
    period: Optional[XbrlPeriod] = None
    depth: int = 0
    order: float = 0.0
    is_abstract: bool = False
    dimensions: dict[str, str] = {}


class NoteSection(BaseModel):
    """A structured financial statement note (disclosure)."""

    role_code: str
    role_uri: str
    title: Optional[str] = None
    is_consolidated: bool = True
    line_items: list[NoteLineItem] = []
    periods: list[XbrlPeriod] = []


class ParsedNotes(BaseModel):
    """Collection of parsed financial statement notes."""

    source_file: str
    entity_id: Optional[str] = None
    notes: dict[str, NoteSection] = {}
```

- [ ] **Step 4: 테스트 통과 확인**

Run: `uv run pytest packages/cluefin-xbrl/tests/test_notes.py::TestNoteModels -v`
Expected: PASS (4 passed)

- [ ] **Step 5: Phase 검증** (lint + format + 단위 테스트 전체)

```bash
uv run ruff format .
uv run ruff check . --fix
uv run pytest -m "not integration"
```
Expected: format/lint 통과, 전체 단위 테스트 PASS.

- [ ] **Step 6: 커밋**

```bash
git add packages/cluefin-xbrl/src/cluefin_xbrl/_types.py packages/cluefin-xbrl/tests/test_notes.py
git commit -m "feat(xbrl): 주석 데이터 모델(NoteLineItem/NoteSection/ParsedNotes) 추가"
```

---

## Phase 2: 주석 role 분류기 `_identify_note_role` (`notes.py`)

**Files:**
- Create: `packages/cluefin-xbrl/src/cluefin_xbrl/notes.py`
- Test: `packages/cluefin-xbrl/tests/test_notes.py` (클래스 추가)

**Interfaces:**
- Produces: `_identify_note_role(linkrole: str) -> tuple[str, bool] | None` — `(role_code, is_consolidated)` 또는 `None`.

- [ ] **Step 1: 실패하는 테스트 작성** — `tests/test_notes.py`에 클래스 추가 (상단 import에 `from cluefin_xbrl.notes import _identify_note_role` 추가)

```python
class TestIdentifyNoteRole:
    def test_consolidated_note(self):
        assert _identify_note_role("http://dart.fss.or.kr/role/ifrs/ias_19_role-D834480") == ("D834480", True)

    def test_separate_note(self):
        assert _identify_note_role("http://dart.fss.or.kr/role/ifrs/ias_19_role-D834485") == ("D834485", False)

    def test_statement_role_is_not_note(self):
        assert _identify_note_role("http://dart.fss.or.kr/role/ifrs/dart_2024-06-30_role-D210000") is None

    def test_doc_role_is_not_note(self):
        assert _identify_note_role("http://dart.fss.or.kr/role/ifrs/dart-gcd_2024-06-30_role-D999001") is None

    def test_generic_role_is_not_note(self):
        assert _identify_note_role("http://example.com/role/SomeOtherRole") is None
```

- [ ] **Step 2: 테스트 실패 확인**

Run: `uv run pytest packages/cluefin-xbrl/tests/test_notes.py::TestIdentifyNoteRole -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'cluefin_xbrl.notes'`

- [ ] **Step 3: 분류기 구현** — `notes.py` 생성 (이번 단계에선 import + 정규식 + 분류기까지)

```python
"""Financial statement note (disclosure) extraction from parsed XBRL data."""

from __future__ import annotations

import re

from cluefin_xbrl._types import (
    NoteLineItem,
    NoteSection,
    ParsedNotes,
    PresentationNode,
    XbrlDocument,
    XbrlFact,
    XbrlPeriod,
)

_NOTE_ROLE_PATTERN = re.compile(r"role-(D8\d+)")


def _identify_note_role(linkrole: str) -> tuple[str, bool] | None:
    """Identify a note (disclosure) role code and consolidated flag from a linkrole URI.

    DART note linkroles carry a role code of the form ``D8xxxxx``. By DART convention a
    code ending in ``0`` is the consolidated note and one ending in ``5`` is the separate note.

    Returns:
        ``(role_code, is_consolidated)`` if the linkrole is a note role, else ``None``.
    """
    match = _NOTE_ROLE_PATTERN.search(linkrole)
    if match is None:
        return None
    role_code = match.group(1)
    is_consolidated = not role_code.endswith("5")
    return role_code, is_consolidated
```

> 참고: import에 포함된 `NoteLineItem`, `NoteSection`, `ParsedNotes`, `PresentationNode`, `XbrlDocument`, `XbrlFact`, `XbrlPeriod`는 Phase 3에서 사용된다. ruff가 F401을 ignore하므로 이 단계에서 미사용 경고는 발생하지 않는다.

- [ ] **Step 4: 테스트 통과 확인**

Run: `uv run pytest packages/cluefin-xbrl/tests/test_notes.py::TestIdentifyNoteRole -v`
Expected: PASS (5 passed)

- [ ] **Step 5: Phase 검증**

```bash
uv run ruff format .
uv run ruff check . --fix
uv run pytest -m "not integration"
```
Expected: 전부 통과.

- [ ] **Step 6: 커밋**

```bash
git add packages/cluefin-xbrl/src/cluefin_xbrl/notes.py packages/cluefin-xbrl/tests/test_notes.py
git commit -m "feat(xbrl): 주석 role 분류기 _identify_note_role 추가"
```

---

## Phase 3: `extract_notes` 추출 + export (`notes.py`, `__init__.py`)

**Files:**
- Modify: `packages/cluefin-xbrl/src/cluefin_xbrl/notes.py` (함수 추가)
- Modify: `packages/cluefin-xbrl/src/cluefin_xbrl/__init__.py`
- Test: `packages/cluefin-xbrl/tests/test_notes.py` (클래스 추가)

**Interfaces:**
- Consumes: `_identify_note_role` (Phase 2), 모델 (Phase 1), `XbrlDocument`/`XbrlFact`/`PresentationNode`/`XbrlPeriod`/`TaxonomyInfo`/`ConceptLabel`.
- Produces: `extract_notes(doc: XbrlDocument) -> ParsedNotes`.

- [ ] **Step 1: 실패하는 테스트 작성** — `tests/test_notes.py`에 클래스 추가 (상단 import에 `from cluefin_xbrl.notes import _identify_note_role, extract_notes`로 갱신)

```python
def _make_doc() -> XbrlDocument:
    """확정급여 주석 1개 + 비주석(재무상태표) role 1개를 가진 합성 문서."""
    period = XbrlPeriod(period_type=PeriodType.INSTANT, instant=None)

    # 주석 트리: 추상 컨테이너 -> 값 노드(차원 있음)
    value_node = PresentationNode(
        concept_local_name="DefinedBenefitObligationAtPresentValue",
        concept_qname="ifrs-full:DefinedBenefitObligationAtPresentValue",
        depth=1,
        order=1.0,
    )
    root_node = PresentationNode(
        concept_local_name="DisclosureOfDefinedBenefitPlansAbstract",
        concept_qname="ifrs-full:DisclosureOfDefinedBenefitPlansAbstract",
        depth=0,
        order=0.0,
        children=[value_node],
    )
    note_role = "http://dart.fss.or.kr/role/ifrs/ias_19_role-D834480"
    # 비주석 role(재무상태표)도 트리에 넣어 걸러지는지 검증
    stmt_role = "http://dart.fss.or.kr/role/ifrs/dart_2024-06-30_role-D210000"
    stmt_node = PresentationNode(
        concept_local_name="Assets",
        concept_qname="ifrs-full:Assets",
    )

    labels = {
        "DisclosureOfDefinedBenefitPlansAbstract": ConceptLabel(
            concept_local_name="DisclosureOfDefinedBenefitPlansAbstract",
            concept_qname="ifrs-full:DisclosureOfDefinedBenefitPlansAbstract",
            label_ko="종업원급여에 대한 공시",
            label_en="Disclosure of defined benefit plans",
        ),
        "DefinedBenefitObligationAtPresentValue": ConceptLabel(
            concept_local_name="DefinedBenefitObligationAtPresentValue",
            concept_qname="ifrs-full:DefinedBenefitObligationAtPresentValue",
            label_ko="확정급여채무, 현재가치",
            label_en="Defined benefit obligation, at present value",
        ),
    }
    taxonomy = TaxonomyInfo(
        labels=labels,
        presentation_trees={note_role: [root_node], stmt_role: [stmt_node]},
    )
    fact = XbrlFact(
        concept_local_name="DefinedBenefitObligationAtPresentValue",
        concept_qname="ifrs-full:DefinedBenefitObligationAtPresentValue",
        namespace="http://xbrl.ifrs.org/taxonomy/2021-03-24/ifrs-full",
        value="1000",
        numeric_value=Decimal("1000"),
        unit="iso4217:KRW",
        period=period,
        dimensions={"ifrs-full:Axis": "ifrs-full:Member"},
    )
    return XbrlDocument(
        source_file="entity_test.xbrl",
        facts=[fact],
        entity_id="00000000",
        taxonomy=taxonomy,
    )


class TestExtractNotes:
    def test_requires_taxonomy(self):
        doc = XbrlDocument(source_file="x.xbrl", facts=[])
        with pytest.raises(ValueError):
            extract_notes(doc)

    def test_extracts_only_note_roles(self):
        notes = extract_notes(_make_doc())
        # D834480 주석만, 재무상태표 D210000은 제외
        assert list(notes.notes.keys()) == ["D834480"]

    def test_note_section_metadata(self):
        section = extract_notes(_make_doc()).notes["D834480"]
        assert section.role_code == "D834480"
        assert section.is_consolidated is True
        assert section.title == "종업원급여에 대한 공시"

    def test_dimensions_preserved(self):
        section = extract_notes(_make_doc()).notes["D834480"]
        value_items = [li for li in section.line_items if not li.is_abstract]
        assert len(value_items) == 1
        assert value_items[0].dimensions == {"ifrs-full:Axis": "ifrs-full:Member"}
        assert value_items[0].value == Decimal("1000")

    def test_abstract_node_has_no_value(self):
        section = extract_notes(_make_doc()).notes["D834480"]
        abstract_items = [li for li in section.line_items if li.is_abstract]
        assert any(li.concept_local_name == "DisclosureOfDefinedBenefitPlansAbstract" for li in abstract_items)

    def test_public_api_import(self):
        from cluefin_xbrl import ParsedNotes as PN
        from cluefin_xbrl import extract_notes as en

        assert en is extract_notes
        assert PN is ParsedNotes
```

- [ ] **Step 2: 테스트 실패 확인**

Run: `uv run pytest packages/cluefin-xbrl/tests/test_notes.py::TestExtractNotes -v`
Expected: FAIL — `ImportError: cannot import name 'extract_notes'`

- [ ] **Step 3: `extract_notes` + 헬퍼 구현** — `notes.py`에 아래 함수들을 `_identify_note_role` 아래에 추가

```python
def extract_notes(doc: XbrlDocument) -> ParsedNotes:
    """Extract structured financial statement notes from a parsed XBRL document.

    Requires the document to have taxonomy information (parsed with ``include_taxonomy=True``).

    Args:
        doc: XbrlDocument with taxonomy information.

    Returns:
        ParsedNotes with note sections keyed by role code.

    Raises:
        ValueError: If taxonomy information is not available.
    """
    if doc.taxonomy is None:
        raise ValueError("Taxonomy 정보가 필요합니다. parse_xbrl_file(include_taxonomy=True)로 파싱하세요.")

    facts_by_concept: dict[str, list[XbrlFact]] = {}
    for fact in doc.facts:
        facts_by_concept.setdefault(fact.concept_local_name, []).append(fact)

    notes: dict[str, NoteSection] = {}

    for linkrole, roots in doc.taxonomy.presentation_trees.items():
        identified = _identify_note_role(linkrole)
        if identified is None:
            continue
        role_code, is_consolidated = identified

        line_items = _flatten_note_tree(roots, facts_by_concept, doc.taxonomy.labels)

        periods: list[XbrlPeriod] = []
        seen_periods: set[str] = set()
        for item in line_items:
            if item.period is not None:
                period_key = str(item.period)
                if period_key not in seen_periods:
                    seen_periods.add(period_key)
                    periods.append(item.period)

        title = None
        if roots:
            label = doc.taxonomy.labels.get(roots[0].concept_local_name)
            if label is not None:
                title = label.label_ko or label.label_en

        notes[role_code] = NoteSection(
            role_code=role_code,
            role_uri=linkrole,
            title=title,
            is_consolidated=is_consolidated,
            line_items=line_items,
            periods=periods,
        )

    return ParsedNotes(source_file=doc.source_file, entity_id=doc.entity_id, notes=notes)


def _flatten_note_tree(
    roots: list[PresentationNode],
    facts_by_concept: dict[str, list[XbrlFact]],
    labels: dict[str, object],
) -> list[NoteLineItem]:
    """Flatten a note presentation tree and match with facts to create line items."""
    items: list[NoteLineItem] = []
    for root in roots:
        _collect_note_line_items(root, facts_by_concept, labels, items)
    return items


def _collect_note_line_items(
    node: PresentationNode,
    facts_by_concept: dict[str, list[XbrlFact]],
    labels: dict[str, object],
    items: list[NoteLineItem],
) -> None:
    """Recursively collect note line items, preserving dimensions, from a presentation node."""
    concept_facts = facts_by_concept.get(node.concept_local_name, [])
    label = labels.get(node.concept_local_name)

    label_ko = label.label_ko if label is not None and hasattr(label, "label_ko") else None
    label_en = label.label_en if label is not None and hasattr(label, "label_en") else None

    if concept_facts:
        for fact in concept_facts:
            items.append(
                NoteLineItem(
                    concept_local_name=node.concept_local_name,
                    concept_qname=node.concept_qname,
                    label_ko=label_ko,
                    label_en=label_en,
                    value=fact.numeric_value,
                    unit=fact.unit,
                    period=fact.period,
                    depth=node.depth,
                    order=node.order,
                    is_abstract=False,
                    dimensions=dict(fact.dimensions),
                )
            )
    else:
        items.append(
            NoteLineItem(
                concept_local_name=node.concept_local_name,
                concept_qname=node.concept_qname,
                label_ko=label_ko,
                label_en=label_en,
                depth=node.depth,
                order=node.order,
                is_abstract=True,
            )
        )

    for child in node.children:
        _collect_note_line_items(child, facts_by_concept, labels, items)
```

- [ ] **Step 4: `__init__.py` export 추가** — import 블록과 `__all__`에 신규 심볼 추가

`_types` import 블록에 추가:
```python
    NoteLineItem,
    NoteSection,
    ParsedNotes,
```
새 import 줄 추가:
```python
from cluefin_xbrl.notes import extract_notes
```
`__all__` 리스트에 추가 (알파벳 순서 유지):
```python
    "NoteLineItem",
    "NoteSection",
    "ParsedNotes",
    "extract_notes",
```

- [ ] **Step 5: 테스트 통과 확인**

Run: `uv run pytest packages/cluefin-xbrl/tests/test_notes.py -v`
Expected: PASS (전체 클래스 통과).

- [ ] **Step 6: Phase 검증**

```bash
uv run ruff format .
uv run ruff check . --fix
uv run pytest -m "not integration"
```
Expected: 전부 통과.

- [ ] **Step 7: 커밋**

```bash
git add packages/cluefin-xbrl/src/cluefin_xbrl/notes.py packages/cluefin-xbrl/src/cluefin_xbrl/__init__.py packages/cluefin-xbrl/tests/test_notes.py
git commit -m "feat(xbrl): 재무제표 주석 추출 extract_notes() 추가 및 export"
```

---

## Phase 4: 통합 테스트 (실 XBRL, env var gated)

**Files:**
- Create: `packages/cluefin-xbrl/tests/test_notes_integration.py`

**Interfaces:**
- Consumes: `parse_xbrl_directory` (기존), `extract_notes` (Phase 3).

- [ ] **Step 1: 통합 테스트 작성** — `tests/test_notes_integration.py` 생성

```python
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
```

- [ ] **Step 2: 통합 테스트 실행 (실데이터)**

Run:
```bash
CLUEFIN_XBRL_TEST_DIR=/private/tmp/claude-501/-Volumes-kgcrom-2tb-kgcrom-workspace-cluefin/d5200a88-a7a0-4b6f-b192-68c9d5c8a829/scratchpad/samsung_xbrl \
  uv run pytest packages/cluefin-xbrl/tests/test_notes_integration.py -m integration -v
```
Expected: PASS (삼성 2025 XBRL로 57개 주석, 종업원급여 존재, 차원 보존 확인).

- [ ] **Step 3: skip 동작 확인 (env var 없이)**

Run: `uv run pytest packages/cluefin-xbrl/tests/test_notes_integration.py -m integration -v`
Expected: SKIPPED (1 skipped) — `CLUEFIN_XBRL_TEST_DIR 미설정`.

- [ ] **Step 4: Phase 검증**

```bash
uv run ruff format .
uv run ruff check . --fix
uv run pytest -m "not integration"
```
Expected: 전부 통과.

- [ ] **Step 5: 커밋**

```bash
git add packages/cluefin-xbrl/tests/test_notes_integration.py
git commit -m "test(xbrl): extract_notes 통합 테스트 추가 (env var gated)"
```

---

## Self-Review

- **Spec coverage**: 범위(D8만, Phase 2 분류기), 차원 raw 보존(Phase 3 `_collect_note_line_items` + Phase 1 모델), 연결/별도 플래그(Phase 2 `is_consolidated`), 신규 모듈·모델·미변경 statements.py(전 Phase), ValueError 가드(Phase 3 test_requires_taxonomy), 테스트 전략(단위=합성 doc, 통합=env var) — 전부 태스크에 매핑됨.
- **Placeholder scan**: TBD/TODO 없음, 모든 코드 단계에 완전한 코드 포함.
- **Type consistency**: `extract_notes(doc) -> ParsedNotes`, `_identify_note_role -> tuple[str, bool] | None`, `NoteSection.role_code/role_uri/title/is_consolidated/line_items/periods`, `NoteLineItem.dimensions` — Phase 간 일관.
- **알려진 한계(설계 문서 5절)**: concept 전역 매칭은 v1 허용, 통합 테스트 주석에 명시 불필요(설계 문서가 기록). is_consolidated 휴리스틱은 docstring에 명시됨.
