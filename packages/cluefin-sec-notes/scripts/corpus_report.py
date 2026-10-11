"""코퍼스 전체의 추출 결과 요약: 공시별 기대값 검사, Finding 코드별·층화 칸별 집계.

기대값이 없는 공시(스모크)는 자동 불변식 위반을 보여 주고, `--write-baseline`이면 지금 위반 목록을 manifest의
`baseline`에 적는다(통합 테스트가 새 위반을 회귀로 잡는다).

    uv run python packages/cluefin-sec-notes/scripts/corpus_report.py docs/plans/sec-notes-corpus/golden.json \
        --corpus ~/.cache/cluefin-sec-notes-corpus
"""

from __future__ import annotations

import argparse
import time
from collections import Counter, defaultdict
from pathlib import Path

from _corpus import filing_path, read_manifest, write_manifest

from cluefin_sec_notes import extract_items, load_filing
from cluefin_sec_notes._expectations import FAILED, FIXED, KNOWN_BAD, check_expectations, invariant_violations


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("manifests", nargs="+", type=Path)
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument(
        "--write-baseline", action="store_true", help="스모크 공시의 지금 위반 목록을 baseline으로 쓴다"
    )
    args = parser.parse_args()
    violations_total: Counter[str] = Counter()

    codes: Counter[str] = Counter()
    bad_by_stratum: dict[str, list[bool]] = defaultdict(list)
    bad_filings = 0
    total = 0
    for manifest in args.manifests:
        entries = read_manifest(manifest)
        for entry in entries:
            total += 1
            started = time.perf_counter()
            document = load_filing(filing_path(args.corpus.expanduser(), entry), form=entry["form"])
            extraction = extract_items(document)
            elapsed = time.perf_counter() - started
            checks = check_expectations(extraction, entry)
            statuses = Counter(check.status for check in checks)
            violations = invariant_violations(extraction)
            violations_total.update(violations)
            if args.write_baseline and not checks:
                entry["baseline"] = violations
            warnings = Counter(finding.code for finding in extraction.warnings)
            codes.update(warnings)
            is_bad = bool(statuses[FAILED] or statuses[KNOWN_BAD] or (not checks and violations))
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
            if not checks and violations:
                print(f"       위반: {', '.join(violations)}")
        if args.write_baseline:
            write_manifest(manifest, entries)
    print(f"\nknown-bad 포함 불량 공시: {bad_filings}/{total}")
    print("Finding 코드:", dict(codes.most_common()))
    print("불변식 위반:", dict(violations_total.most_common()))
    print("층화 칸별 불량:")
    for stratum, flags in sorted(bad_by_stratum.items()):
        print(f"  {stratum:28} {sum(flags)}/{len(flags)}")


if __name__ == "__main__":
    main()
