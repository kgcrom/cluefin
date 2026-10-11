# AGENTS.md — cluefin-sec-notes

Non-obvious constraints only; see the root AGENTS.md for repo-wide rules (Codacy patterns included).

## Scope

- **Pure local-file parser** — downloading lives in cluefin-openapi (`sec.archives.download_filing_document`).
- HTML: stdlib `html.parser` builds the tree; lxml was rejected because libxml2 silently drops content deeper than
  256 levels without `huge_tree`, and `recover=True` doesn't say what it dropped. Tree code never recurses
  (Python's recursion limit is hit by real filings). The only dependency, `defusedxml`, is for the ownership XML.
- Item extraction is out of scope for pre-2001 `.txt` filings, 20-F and other forms, and exhibits (8-K EX-99.1 is a
  separate file).
- Form 3/4/5 live in the `ownership` subpackage (decided 2026-10-12 instead of a separate package: no shared code,
  but a new package would only add setup). Keep the two apart; 13F is planned to join `ownership`.

## Ownership (Form 3/4/5)

Measured 2026-10-12 on 477 filings (eight issuers, Forms 3/4/5 and amendments, 2004–2026, schema X0201–X0609).

- `primaryDocument` is always the XSL rendering path (`xslF345X0n/<name>.xml`); the raw XML is `<name>.xml` at
  the folder root, which `download_filing_document` accepts as is. Accessions with a filing agent's prefix are
  reachable under the issuer's CIK too.
- Parse with `defusedxml` only; element types come from the local `_xml.Element` Protocol because even a
  type-only import from stdlib `xml` is a Codacy critical (root AGENTS.md).
- Rows are filled from field tables (`_parse._Field`: name, path, converter). The transaction code's footnotes sit
  on `transactionCoding`, not on the code element, hence `notes_path` (412 such references). Every `footnoteId` in
  the 477 filings landed in some row's `footnote_ids`; keep it that way when adding fields.
- Shapes seen and handled: booleans `1`/`0`/`true`/`false` (nothing else, so anything else raises); decimals without
  a leading zero (`.20`); empty cells; price given only as a footnote (M/C/A rows); derivative amounts as
  `transactionTotalValue` instead of shares; `valueOwnedFollowingTransaction`; omitted relationship flags (= False);
  an empty `transactionCoding` on Form 5 holdings (ignored).
- The issuer is not always the company whose submissions you listed: 4 of 477 were that company reporting its
  stake in another issuer. Amendments may carry no rows (5 of 34 4/A fixed only signature or remarks); the parser
  does not merge an amendment with its original.

## Detection: rules that look arbitrary but aren't

Each rule below replaced an approach that broke real filings. Don't go back to the left-hand version.

- **Order checks only against stronger detectors.** Checking every candidate pair against catalog order
  discarded valid annual-report-style 10-Ks (Items 1B–5 sit in an "Other information" section at the end).
  A weaker candidate must lie between the catalog neighbours that a *stronger* detector fixed; same-confidence
  candidates are not order-checked, and the layout is reported as `non_sequential_layout` instead.
- **TOC title matching is exact plus page tokens**, never prefix: "Business Overview" matched Item 1. After the
  title only Part/Item numbers and page tokens may follow (some TOCs are "title | Part | Item | page").
- **Don't trust TOC links blindly.** Links pointing at another Item's heading or into a note body were real
  (3 in the smoke corpus). A link whose target isn't verified as that Item's heading drops to
  `toc_anchor_unverified` (0.5, below `pattern`). Skip empty-cell tables when verifying (Workiva page tops).
  For part-scoped forms verification also checks the Part (a Part I Item 4 link pointing at Part II "Item 4.").
- **Item 4 alias "Reserved" was removed**: it swallowed 10-K Item 6 ("[Reserved]").
- **Page furniture compares Item/Part labels literally.** Stripping digits for the repeat check (needed for page
  numbers) also erased real "Item 9." headings on filings that start a new Item on every page. Sentences ending
  in "." ("None.") are excluded from repeat detection.
- **Page headers listing that page's Items ("Item 9, 9A", "Part II, III") are trimmed only at a range's end.**
  Treating a bare item label after a Part header as furniture anywhere would also delete real "PART II" +
  "Item 5." headings. At the end it's safe: the next Item's real heading is that Item's start block. Only labels
  without a title that don't name the Item itself are trimmed (a continued page's own "Item 7" stays). In the
  corpus all 18 such labels were the last block; 16 sat in golden `ok` Items within the length tolerance.
- **`statements_not_found` looks at length, not tables or titles.** "No table" missed a reference-only Item 8 that
  kept two quarterly tables (the statements sat inside Item 15). Balance-sheet wording flagged two golden `ok` Items
  (48k/72k chars). The 5,000-char cut sits in a gap: reference-only Items 112–3,321 chars, the smallest real
  statements 6,797 (a trust 10-Q), golden `ok` minimum 13,097. Not raised when `page_reference_unresolved` or
  `empty_item` already covers the Item. It replaces the corpus invariants `no_table:8`/`no_table:I:1`.
- **Boundary spills are caught by per-Item length ranges (`ItemSpec.min_chars`/`max_chars`), nothing else.**
  A first line that is neither the Item label nor its title flagged 24 golden `ok` Items (cross-reference indexes,
  statements right after the TOC, Items opening with "Part III"). "The previous Item is short" misfires on pairs
  that are short-then-long by nature (6→7, II:1→II:1A, 7A→8). Ranges are set only where the corpus splits cleanly:
  10-K 7A > 150,000 (golden max 104,249, a bank; known-bad 272,767), 10-Q I:3 > 50,000 (max 6,705 / 103,900),
  10-Q I:4 > 30,000 (max 7,104 / 275,902; one smoke 43,935 that really ate the statements), 10-K 7 < 3,000
  (non-incorporated golden min > 9,475 / 1,214). Synthetic fixtures carry long `MDNA`/`STATEMENTS` bodies so
  these rules stay quiet in unit tests.
- **`item()` raises only for `UNCERTAIN_CODES`, and only `item()` raises.** `extract_items()` and iteration never
  raise, so results, candidates and findings stay inspectable. `toc_target_missing` (8 golden `ok` Items found by
  heading after a dead TOC link) and `non_sequential_layout` (1) sit on correct Items, so they're left out.
  `MissingItemError` keys off the `missing_item` finding, not `missing`, so amendments (no missing warnings) and
  omitted Items still return None. Corpus tooling (`_expectations.item_by_key`, scripts) calls `strict=False`.
  Adding a new boundary warning means deciding whether it joins `UNCERTAIN_CODES` (measure golden `ok` first).
- **Page references follow only the first closed range in a near-empty body.** Following every reference in a
  short body broke golden 9A ("report on page F-2"), 7A ("see … on page 75"), Item 2 (a trailing "refer to pages
  51–54") and Item 7 (second sentence "read in conjunction with … pages 165–314"). Current rule: non-statement
  Items with a body ≤ 1,000 chars follow the first in-document closed range; single pages are ignored; bodies
  naming another document (proxy, Exhibit 13, annual report to shareholders) are skipped entirely. Open references,
  "page F-1" and page-less F-pages are for the financial-statements Item only. Item 15 (`lists_documents`) never follows.
- **Item 15 loses the blocks other Items took by reference; it is not cut short.** Annual-report-style 10-Ks put
  the whole annual report after Item 15, so Item 15 ran to the signatures (1,002,763 chars) while Items 7/8 had
  already taken those pages. Truncating at the first taken block lost an exhibit index that follows the F-pages,
  so the taken ranges are subtracted and empty leftovers (page breaks) dropped. 6 of 624 exhibit Items changed.
- **Cross-reference index Items are page-granular**: the first page may start with the previous section's tail.
  Their ranges don't cut other Items and don't take part in order checks.
- **10-Q Part tracking**: headings are "Item 1." without a Part; the Part comes from the last Part heading
  (`DetectionContext.part_at`). Part headings right before a TOC-like table are ignored (text TOCs carry their
  own "PART II" that would otherwise label the body's Part I items).
- **Mandatory 10-Q Items (Part I 1/2/4)** are never `omitted`. Without this, filings whose only "Item 1" label is
  in the TOC (statements start right after the TOC, no heading — 13 of 200 smoke 10-Qs) were silently
  reported as omitted. `StatementsAfterTocDetector` now fills that case.
- **Omission vs. missing for part-scoped forms**: only "Item N" mentions inside the same Part region count, and
  mentions naming another Part ("Part I, Item 4") don't. The 10-Q Part II name "OTHER INFORMATION" equals the
  Item 5 title, so Part names are excluded from title lines.
- **"shall not be incorporated by reference"** (8-K 2.02/7.01, 10-K performance graph) is not incorporation.
- **8-K legacy numbering (before 2004-08-23)** shares the catalog with current numbering (numbers don't collide);
  `applies_to` filters by date so "Item 2." vote proposals in a 2026 Item 5.07 aren't read as legacy Item 2.
- **Footnote cells in tables**: a single numeric mark "(5)" is indistinguishable from a small negative, so only
  letter marks or multiple marks ("(2)(9)") are merged as footnotes. Bare years ("2025") don't join columns —
  a year header spanning several sub-columns (Loans | Derivatives) would merge them.

## Corpus workflow

- Real filings and manifests are **never committed** (company names, CIKs and accession numbers stay out of code,
  fixtures, commits and PRs). Manifests live in the git-ignored `docs/plans/sec-notes-corpus/`:
  `golden.json` (10-K), `golden-10q.json`, `golden-8k.json` with human-checked expectations and `known_bad`;
  `smoke-10k.json`, `smoke-10q.json`, `smoke-8k.json` (200 each, seed 1) with a `baseline` of invariant violations.
- Re-download with `scripts/fetch_corpus.py <manifest…> --dest ~/.cache/cluefin-sec-notes-corpus`
  (`SEC_USER_AGENT` in `.env.test`). Run: `CLUEFIN_SEC_NOTES_TEST_DIR=~/.cache/cluefin-sec-notes-corpus uv run pytest
  packages/cluefin-sec-notes -m integration` (~5 min for 676 filings; narrow with
  `CLUEFIN_SEC_NOTES_MANIFESTS=golden.json,smoke-10k.json`).
- A `fixed` status means a known-bad item now passes: check the boundary with `scripts/draft_expectations.py`,
  then record it with `--accept <accession> <item…>`. Rewrite smoke baselines with
  `scripts/corpus_report.py <manifest> --corpus … --write-baseline`. Smoke baselines only see invariant violations,
  so a new detector that fills Items wrongly is invisible there — list what it adopted across the corpus and read it.
- Unit tests use the synthetic HTML in `tests/conftest.py` (`synthetic` fixture; importlib mode can't import test
  helper modules) and per-form helpers in `tests/test_10q.py`/`test_8k.py`.

## Gotchas

- `uv sync` alone removes other workspace packages' dependencies; use `uv sync --all-packages`.
- Naming an exploration script `inspect.py` shadows the stdlib module and breaks imports.
- Codacy flags nested regex quantifiers as critical; label lists, page lists and footnote marks are read
  token by token in code for that reason.
