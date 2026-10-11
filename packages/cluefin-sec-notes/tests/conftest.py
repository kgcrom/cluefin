"""통합 테스트용 코퍼스. 원문과 manifest는 커밋하지 않는다(기업명 비공개).

- `CLUEFIN_SEC_NOTES_TEST_DIR`: 원문 폴더(`<form>/<accession>/<file>`). 없으면 통합 테스트를 건너뛴다.
- `CLUEFIN_SEC_NOTES_MANIFEST_DIR`: `golden.json`, `smoke-*.json`이 있는 폴더. 기본값 `docs/plans/sec-notes-corpus`.
  받는 법은 `scripts/fetch_corpus.py`.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

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
    for manifest in sorted(manifest_dir.glob("*.json")):
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
