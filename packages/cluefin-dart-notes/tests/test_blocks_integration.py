"""실제 원문 디렉터리로 블록 추출과 단위 연결을 확인한다. `CLUEFIN_DART_NOTES_TEST_DIR`가 없으면 건너뛴다."""

from collections import Counter

import pytest

from cluefin_dart_notes import Paragraph, Table, parse_amount

pytestmark = pytest.mark.integration


def _is_numeric(table: Table) -> bool:
    body = [cell for row in table.grid[1:] for cell in row[1:] if cell and cell.text]
    return bool(body) and sum(parse_amount(cell.text) is not None for cell in body) / len(body) >= 0.5


def _has_unit(table: Table) -> bool:
    return table.unit is not None or any(cell and cell.aunit for row in table.grid for cell in row)


def test_numeric_tables_almost_always_get_a_unit(corpus_documents):
    counts: Counter[str] = Counter()
    for document in corpus_documents:
        for section in document.iter_sections():
            for block in section.blocks:
                if isinstance(block, Table) and block.bordered and _is_numeric(block):
                    counts["numeric"] += 1
                    counts["with unit"] += _has_unit(block)
    print(f"\nnumeric data tables {counts['numeric']}, with unit {counts['with unit']}")
    assert counts["with unit"] / counts["numeric"] >= 0.95


def test_text_has_no_markers(corpus_documents):
    for document in corpus_documents:
        for section in document.iter_sections():
            for block in section.blocks:
                if isinstance(block, Paragraph):
                    assert " " not in block.text and "" not in block.text, document.rcept_no
                    assert block.text == block.text.strip(), document.rcept_no
