"""스모크 코퍼스 목록을 무작위로 만든다(시드 고정이라 재현된다).

`company_tickers`에서 회사를 섞어 고르고, 그 회사의 최근 제출 이력에서 해당 서식 하나를 무작위로 고른다.
상장 중인 회사만 뽑히는 생존 편향이 있다(오래된 공시·상장폐지 회사는 골든에서 직접 채운다).

    uv run python packages/cluefin-sec-notes/scripts/sample_smoke.py --form 10-K --count 200 --seed 1 \
        --out docs/plans/sec-notes-corpus/smoke-10k.json --exclude docs/plans/sec-notes-corpus/golden.json
"""

from __future__ import annotations

import argparse
import random
from pathlib import Path

from _corpus import read_manifest, sec_client, write_manifest

_HTML_SUFFIXES = (".htm", ".html")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--form", required=True)
    parser.add_argument("--count", type=int, required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--exclude", type=Path, nargs="*", default=[])
    args = parser.parse_args()

    client = sec_client()
    rng = random.Random(args.seed)
    excluded = {entry["accession"] for path in args.exclude for entry in read_manifest(path)}
    entries = read_manifest(args.out)  # 이어 받기: 이미 뽑은 것은 유지
    seen_ciks = {entry["cik"] for entry in entries}
    ciks = sorted({ticker.cik for ticker in client.reference.company_tickers()})
    rng.shuffle(ciks)
    for cik in ciks:
        if len(entries) >= args.count:
            break
        if cik in seen_ciks:
            continue
        candidates = [
            filing
            for filing in client.submissions.filings(cik, forms=[args.form], include_amendments=False)
            if filing.primary_document
            and filing.primary_document.lower().endswith(_HTML_SUFFIXES)
            and filing.accession_number not in excluded
        ]
        if not candidates:
            continue
        filing = rng.choice(candidates)
        entry = {"cik": cik, "accession": filing.accession_number, "form": filing.form, "file": filing.primary_document}
        if filing.items:
            entry["sec_items"] = filing.items.split(",")
        entries.append(entry)
        seen_ciks.add(cik)
        write_manifest(args.out, entries)
    print(f"{len(entries)}건 → {args.out}")


if __name__ == "__main__":
    main()
