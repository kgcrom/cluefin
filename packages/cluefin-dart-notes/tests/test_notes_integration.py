"""실제 원문 디렉터리로 주석 분할을 확인한다. `CLUEFIN_DART_NOTES_TEST_DIR`가 없으면 건너뛴다."""

from collections import Counter

import pytest

from cluefin_dart_notes import notes_sections, split_notes

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def splits(corpus_documents):
    results = []
    for document in corpus_documents:
        sections = notes_sections(document)
        assert sections, document.rcept_no
        results.extend((document.rcept_no, split_notes(section, basis)) for section, basis in sections)
    return results


def test_every_notes_section_splits_from_note_one(splits):
    methods: Counter[str] = Counter()
    for name, result in splits:
        methods[result.method] += 1
        assert len(result.notes) >= 15, (name, result.section.title, len(result.notes))
        assert result.notes[0].number == "1", (name, result.notes[0].heading)
        assert all(note.title for note in result.notes), name
    print(f"\n{len(splits)} notes sections, {dict(methods)}, {sum(len(r.notes) for _, r in splits)} notes")


def test_sequence_split_never_suspects_a_missed_note(splits):
    """번호 1개 건너뜀은 원문에 실제로 없는 번호였다. "놓쳤을 수 있음" 경고가 나오면 새 제목 형태가 생긴 것이다."""
    for name, result in splits:
        assert not [w for w in result.warnings if "놓쳤을 수" in w], (name, result.warnings)


def test_sequence_numbers_increase(splits):
    for name, result in (item for item in splits if item[1].method == "sequence"):
        numbers = [int(note.number) for note in result.notes]
        assert numbers == sorted(set(numbers)), name
        assert all(b - a <= 2 for a, b in zip(numbers, numbers[1:], strict=False)), name
