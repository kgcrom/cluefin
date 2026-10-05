"""실제 원문 디렉터리 전체를 정리·파싱한다. `CLUEFIN_DART_NOTES_TEST_DIR`(하위 폴더까지 `*.xml`)가 없으면 건너뛴다."""

from collections import Counter

import pytest

from cluefin_dart_notes import DartXmlRepairer

pytestmark = pytest.mark.integration


def test_every_document_parses_with_rules_only(corpus_paths):
    repairer = DartXmlRepairer(strict=True)
    totals: Counter[str] = Counter()
    encodings: Counter[str] = Counter()
    warnings: list[str] = []

    for path in corpus_paths:
        root, result = repairer.parse(path.read_bytes())
        assert root.tag == "DOCUMENT", path.name
        encodings[result.encoding] += 1
        warnings.extend(f"{path.name}: {warning}" for warning in result.warnings)
        for report in result.reports:
            totals[report.rule] += report.count

    print(f"\n{len(corpus_paths)} documents, encodings {dict(encodings)}, repairs {dict(totals)}")
    assert warnings == []
