"""골든 기대값 초안과 경계 검토 자료를 만든다.

현재 추출 결과로 Item마다 시작·끝 근처 텍스트를 보여 준다. 사람이 경계를 확인한 뒤 `--write`로 manifest에
기대값(`items`·`present`)을 쓴다. 이미 있는 `known_bad`는 건드리지 않는다.

    uv run python packages/cluefin-sec-notes/scripts/draft_expectations.py docs/plans/sec-notes-corpus/golden.json \
        --corpus ~/.cache/cluefin-sec-notes-corpus --only <접수번호>

known_bad가 고쳐졌으면(`fixed`) 경계를 확인한 뒤 `--accept`로 지금 결과를 그 Item의 기대값으로 쓰고 known_bad에서 뺀다.

    … draft_expectations.py docs/plans/sec-notes-corpus/golden.json --corpus … --accept <접수번호> 7 8
"""

from __future__ import annotations

import argparse
from pathlib import Path

from _corpus import filing_path, read_manifest, write_manifest

from cluefin_sec_notes import block_text, catalog_for, extract_items, load_filing
from cluefin_sec_notes._expectations import accept_items, expectation_key

# 사람이 경계를 확인해 시작 문장·길이를 적는 Item(기대값 키). 나머지는 있는지만 본다. 없는 서식은 전부 핵심이다(8-K).
CORE_ITEMS = {
    "10-K": ("1", "1A", "1C", "7", "7A", "8", "9A"),
    "10-Q": ("I:1", "I:2", "I:3", "I:4", "II:1A"),
}
_CONTEXT = 160


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--only", nargs="*", default=None, help="접수번호(일부)")
    parser.add_argument("--write", action="store_true", help="초안을 manifest에 쓴다")
    parser.add_argument("--core", action="store_true", help="핵심 Item만 보여 준다")
    parser.add_argument(
        "--accept", nargs="+", metavar=("ACCESSION", "ITEM"), help="지금 결과를 이 공시 Item들의 기대값으로 쓴다"
    )
    args = parser.parse_args()

    entries = read_manifest(args.manifest)
    if args.accept:
        _accept(args, entries)
        return
    for entry in entries:
        if args.only is not None and not any(token in entry["accession"] for token in args.only):
            continue
        document = load_filing(filing_path(args.corpus.expanduser(), entry), form=entry["form"])
        extraction = extract_items(document)
        print(f"\n=== {entry['accession']} {entry['form']} {document.period_end} blocks={len(document.blocks)}")
        for finding in extraction.findings:
            print(f"  [{finding.severity}] {finding.code}: {finding.message}")
        items, present = {}, []
        catalog = catalog_for(extraction.catalog)
        part_scoped = bool(catalog and catalog.part_scoped)
        core = CORE_ITEMS.get(extraction.catalog)
        for item in extraction:
            key = expectation_key(item, part_scoped=part_scoped)
            is_core = core is None or key in core
            before_end = document.text(max(item.start, item.end - 2), item.end)
            after_end = block_text(document.blocks[item.end]) if item.end < len(document.blocks) else "<문서 끝>"
            if args.core and not is_core:
                present.append(key)
                continue
            print(f"\n  --- {item.key} [{item.method}] 블록 {item.start}–{item.end} 길이 {len(item.text)}")
            print(f"  시작: {item.text[:_CONTEXT]!r}")
            print(f"  끝  : …{before_end[-_CONTEXT:]!r}")
            print(f"  다음: {after_end[:80]!r}")
            if is_core:
                items[key] = {"starts_with": item.heading[:60], "chars": len(item.text)}
            else:
                present.append(key)
        if args.write:
            entry["items"], entry["present"] = items, present
    if args.write:
        write_manifest(args.manifest, entries)


def _accept(args: argparse.Namespace, entries: list[dict]) -> None:
    accession, *keys = args.accept
    if not keys:
        raise SystemExit("--accept <접수번호> <Item…>")
    entry = next((entry for entry in entries if entry["accession"] == accession), None)
    if entry is None:
        raise SystemExit(f"manifest에 없는 접수번호: {accession}")
    document = load_filing(filing_path(args.corpus.expanduser(), entry), form=entry["form"])
    skipped = accept_items(extract_items(document), entry, keys)
    if skipped:
        raise SystemExit(f"추출 결과에 없는 Item: {', '.join(skipped)} (manifest는 그대로)")
    for key in keys:
        print(f"{accession} {key}: {entry['items'][key]}")
    write_manifest(args.manifest, entries)


if __name__ == "__main__":
    main()
