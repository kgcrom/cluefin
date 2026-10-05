# AGENTS.md — cluefin-dart-notes

Non-obvious constraints only; see the root AGENTS.md for repo-wide rules.

## Scope

- **Pure local-file parser** — it never talks to DART. Downloading lives in cluefin-openapi
  (`disclosure_document_files` saves the main document *and* attached audit reports; a ZIP can hold only
  an audit report, so never assume the first entry is the main document).
- Supported: periodic reports (11011/11012/11013/11014) filed **2017 or later** and their audit reports
  (00760/00761), listed or not. Earlier filings are out of scope by decision, not by accident.
- Parser is stdlib `xml.etree` (through `defusedxml`) after repair. **No lxml `recover=True`** — it can
  drop text silently, so results stop being deterministic.

## Why the repair layer looks the way it does

- Raw dart4 XML is rejected by every strict parser. All defects seen so far (corpus of top KOSPI/KOSDAQ
  and unlisted filings, 2017–2026):
  1. Declared `utf-8`, actually cp949 (filings 2017–2022). The declaration is never trusted.
  2. Bare `&` (`R&D`) — hundreds per large filing.
  3. DART entity `&cr;` (thousands in 2017 filings, none from 2025).
  4. Tag-shaped body text: `<한글…>`, `<English words>`, `< spaced >`, `<2024>`, `<㈜…`.
     **Hangul is a valid XML name character**, so `<기후변화>` parses as a tag and fails much later as
     "mismatched tag".
  5. Extra quote in an attribute value (`ENG="… "">`).
  Control characters and genuinely mismatched tags: zero so far.
- `KNOWN_TAGS` is **observed, not official** (no dart4.xsd available). Any `<` outside it becomes text.
  A missing real tag therefore turns into stray text silently — `CORRECTION` (the revision block at the
  top of `[기재정정]` filings) was found exactly this way. `EscapeUnknownTags` warns when an unknown name
  also appears as a closing tag; treat that warning as "add it to `KNOWN_TAGS`".
- Rules must not add or remove newlines, so sample and parser-error line numbers match the raw file.
  That is why `&cr;` becomes `&#10;`, not a literal newline.
- expat error positions don't point at the culprit (`R&D</P>` reports the `<` of `</P>`; a fake Hangul
  tag reports the next closing tag). Columns are **characters, not bytes** (measured). `PositionalRepair`
  searches backwards by error kind, skips known tags and valid references, and refuses to escape a known
  tag — that would cascade through every following closing tag.
- Check of the fallback on real data (2026-10-05): with `unknown-tags` removed, the fallback alone
  (7–95 fixes per document) produced text identical to the full rule set on every corpus document.
- With the current rules the whole corpus parses **without** the positional fallback. The integration
  test asserts that; if it starts failing, a new defect type has appeared — add a rule.

## Document structure the code relies on (observed, 2017–2026)

- Meta tags (`DOCUMENT-NAME` with `ACODE`, `FORMULA-VERSION`, `COMPANY-NAME` with `AREGCIK`) sit directly
  under the root from 2022 filings, and inside `DOCUMENT-HEADER` before that. Every corpus file had them;
  the file-name fallback (`<rcept_no>_00760.xml`) is only a safety net.
- `ENG` and `ATOCID` on `TITLE` exist only from 2024 filings. `AASSOCNOTE` exists from 2017.
- Sections hang off `BODY`, `SECTION-n`, and wrappers such as `LIBRARY` (business and financial
  statement chapters live inside `LIBRARY`). `CORRECTION` is section-shaped (`TITLE` first) and sits in
  `BODY > LIBRARY`; it is exposed as a level-1 `Section` with `is_correction=True`.
- **Section codes are not globally unique and not stable across years.** Use only the stable ones for
  lookups and scope helpers by document kind:

  | code | periodic report (11011–11014) | audit report (00760/00761) |
  |---|---|---|
  | `D-0-1-*` | children of "I. 회사의 개요" (the chapter itself has **no** code) | `D-0-1-0-0` = 주석 |
  | `D-0-2-0-0` | II. 사업의 내용 — stable in all filings | 외부감사 실시내용 |
  | `D-0-3-3-0` / `D-0-3-5-0` | 연결재무제표 주석 / 재무제표 주석 — stable | — |
  | `D-0-4-0-0` / `D-0-5-0-0` | 경영진단 / 감사의견 — **swapped** in the oldest filings | — |
  | `D-0-1-5-0`, `D-0-3-6-0`, `D-0-10-0-0` | meaning changed between ~2018 and later filings | — |
  | `L-0-2-n-L1` / `L-0-2-n-L2` | 사업의 내용 subsections; `L2` is the financial-industry template. Older filings have none | — |
  | `D-0-0-0-0` / `D-0-0-1-0` | — | (첨부)재무제표 / 독립된 감사인의 감사보고서 |

  Chapters I, VI, VIII, 【전문가의 확인】 and the 상세표 children have no code.
- 11014 (3분기) has not been seen yet; 11013 matched 11012 in structure.

## Testing

- Unit tests use **synthetic fragments only**. Don't commit real filings or name the companies used for
  review; integration tests read `CLUEFIN_DART_NOTES_TEST_DIR` (any directory of `*.xml`, searched
  recursively) and skip when it is unset.
