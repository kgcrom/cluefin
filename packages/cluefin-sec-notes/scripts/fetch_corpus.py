"""manifest의 주 문서를 코퍼스 폴더로 받는다. 이미 있는 파일은 건너뛴다.

uv run python packages/cluefin-sec-notes/scripts/fetch_corpus.py docs/plans/sec-notes-corpus/golden.json ~/.cache/cluefin-sec-notes-corpus
"""

from __future__ import annotations

import argparse
from pathlib import Path

from _corpus import filing_path, read_manifest, sec_client


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("manifests", nargs="+", type=Path)
    parser.add_argument("--dest", type=Path, required=True)
    args = parser.parse_args()

    client = sec_client()
    entries = [entry for manifest in args.manifests for entry in read_manifest(manifest)]
    fetched = 0
    for entry in entries:
        path = filing_path(args.dest.expanduser(), entry)
        if path.exists():
            continue
        client.archives.download_filing_document(
            entry["cik"], entry["accession"], entry["file"], destination=path.parent
        )
        fetched += 1
    print(f"{len(entries)}건 중 {fetched}건 받음 → {args.dest}")


if __name__ == "__main__":
    main()
