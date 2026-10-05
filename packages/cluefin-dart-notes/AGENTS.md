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
  That is why `&cr;` becomes a numeric reference, not a literal newline.
- `&cr;` maps to **U+2028**, not `\n`: raw sources put formatting newlines between runs (1 in 4 paragraphs
  in old filings — `주소 : ⏎ 경기도…` is one line), so a plain newline would be indistinguishable from a real
  `&cr;` break. Block text keeps only U+2028 (and `BR`/paragraph boundaries in cells) as `\n`. Note `&cr;` is
  sometimes a soft wrap mid-word in old filings (`선임&cr;되었습니다`); it is kept as-is.
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

## Blocks: what the heuristics are based on

- `USERMARK` is a space-separated token list (`F-10` font size, `A-L` align, `BC0X…` background,
  ` 0X…` colour). Bold is the token `B` exactly — substring matching would treat `BC0XDCDCDC` as bold.
- Tables: `BORDER="1"` = data table. Layout tables (1×1, or holding a real table in a cell — the big
  borderless wrappers of 2024+ filings) are unwrapped into their blocks. Pick a table's rows from
  `TABLE > (THEAD|TBODY) > TR` only; `iter("TR")` also returns rows of nested tables.
- Unit lookup order: caption table right before (borderless, ≤6 rows, ≤200 chars, contains "단위:"; notes
  use 1–2 rows, statement title tables 3–5), else the last line of the previous paragraph if short (old
  filings append "(단위: 주)" to an explanation paragraph), else the data table's own first row.
  On the corpus this gives a unit to 79% of data tables and to 96% of numeric ones (7,233 of 7,506); the rest are
  text tables or genuinely unitless. A caption table that no data table follows stays a block.
- `TU` cells carry `AUNIT`/`AUNITVALUE`; `TE` cells carry `ACODE` (an XBRL-like item code).

## Note splitting: why the rules are what they are

- Method is chosen by **whether the notes section has numbered `Heading` blocks**, never by year: unlisted
  filings from 2026 and every attached audit report have no per-note titles.
- Sequence search accepts only the next number N or N+1. Every N+1 jump in the corpus was a number that
  is genuinely absent from the filing (e.g. a separate-statement note numbering that skips 4 and 18), so
  the skip is allowed and only warned. Two missing in a row stops the split; the "놓쳤을 수" warning
  scans the last note for later numbers at paragraph start.
- Candidates: paragraph start `N. title` (no colon needed — requiring one empties several filings);
  mid-paragraph `N. title :` right after a sentence end (colon required — without it body text like
  "…입니다. 3. …" splits); mid-paragraph **bold run** starting with `N.` (no colon — an unlisted half-year
  report glues `…되었습니다.<SPAN USERMARK="B">16. 영업으로부터 창출된 현금</SPAN>당반기…`). Sub-numbers
  never match: `2.1` fails "a letter or `(` after `N.`", and `가.`/`(1)` have no `N.` at all.
- Title end: the bold run end when there is one, else the first line up to a colon. Some audit reports
  glue title and body with **no markup at all** (`32. 보고기간후사건회사는 …`), so the line title is cut
  before common body starts (`회사는`, `주식회사`, `당기`, `보고기간말 현재`, `(1)`, `24.1` …). Adjacent bold
  runs merge, so the same cut also separates a bold note title from a bold sub-heading. Corpus result:
  no sequence-mode title over 22 characters that isn't a real title.

## Testing

- Unit tests use **synthetic fragments only**. Don't commit real filings or name the companies used for
  review; integration tests read `CLUEFIN_DART_NOTES_TEST_DIR` (any directory of `*.xml`, searched
  recursively) and skip when it is unset.
- `examples/dart_notes_analysis.ipynb` takes the company from `DART_CORP_CODE` on purpose (no company in the
  file). Execute it with `--output-dir` outside the repo to check it, and commit it with outputs cleared.
