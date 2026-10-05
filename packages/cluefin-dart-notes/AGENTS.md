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

## Testing

- Unit tests use **synthetic fragments only**. Don't commit real filings or name the companies used for
  review; integration tests read `CLUEFIN_DART_NOTES_TEST_DIR` (any directory of `*.xml`, searched
  recursively) and skip when it is unset.
