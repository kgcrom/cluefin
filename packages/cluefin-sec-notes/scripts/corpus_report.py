"""코퍼스 전체의 추출 결과 요약: 공시별 기대값 검사, Finding 코드별·층화 칸별 집계.

    uv run python packages/cluefin-sec-notes/scripts/corpus_report.py docs/plans/sec-notes-corpus/golden.json \
        --corpus ~/.cache/cluefin-sec-notes-corpus
"""

from __future__ import annotations

import argparse
import time
from collections import Counter, defaultdict
from pathlib import Path

from _corpus import filing_path, read_manifest

from cluefin_sec_notes import extract_items, load_filing
from cluefin_sec_notes._expectations import FAILED, FIXED, KNOWN_BAD, check_expectations


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("manifests", nargs="+", type=Path)
    parser.add_argument("--corpus", type=Path, required=True)
    args = parser.parse_args()

    codes: Counter[str] = Counter()
    bad_by_stratum: dict[str, list[bool]] = defaultdict(list)
    bad_filings = 0
    total = 0
    for manifest in args.manifests:
        for entry in read_manifest(manifest):
            total += 1
            started = time.perf_counter()
            document = load_filing(filing_path(args.corpus.expanduser(), entry), form=entry["form"])
            extraction = extract_items(document)
            elapsed = time.perf_counter() - started
            checks = check_expectations(extraction, entry)
            statuses = Counter(check.status for check in checks)
            warnings = Counter(finding.code for finding in extraction.warnings)
            codes.update(warnings)
            is_bad = bool(statuses[FAILED] or statuses[KNOWN_BAD] or (not checks and extraction.missing))
            bad_filings += is_bad
            strata = [*entry.get("strata", ()), f"agent:{entry['accession'][:10]}", f"manifest:{manifest.stem}"]
            for stratum in strata:
                bad_by_stratum[stratum].append(is_bad)
            print(
                f"{'BAD ' if is_bad else 'ok  '} {entry['accession']} {elapsed:4.1f}s items={len(extraction):2} "
                f"missing={len(extraction.missing):2} checks={dict(statuses)} warnings={dict(warnings)}"
            )
            for check in checks:
                if check.status in (FAILED, FIXED):
                    print(f"       {check.status} {check.key}: {check.detail}")
    print(f"\nknown-bad 포함 불량 공시: {bad_filings}/{total}")
    print("Finding 코드:", dict(codes.most_common()))
    print("층화 칸별 불량:")
    for stratum, flags in sorted(bad_by_stratum.items()):
        print(f"  {stratum:28} {sum(flags)}/{len(flags)}")


if __name__ == "__main__":
    main()
