# AGENTS.md — cluefin-xbrl

Non-obvious constraints only; see the root AGENTS.md for repo-wide rules.

## Scope

- This package is a **pure local-file parser** — it never talks to DART or SEC. The download
  path lives in cluefin-openapi (`dart` ZIP fetch, `sec.archives.download_xbrl_files`). A missing
  download function here is intentional, not a gap.
- Arelle itself does go online: it fetches the taxonomies an instance imports (US-GAAP from
  xbrl.fasb.org, DEI/SRT from xbrl.sec.gov, DART's from dart.fss.or.kr) on first use and caches them
  (`~/Library/Caches/Arelle`). This is the only SEC request in the repo that bypasses `sec.Client`:
  no rate limit, and it only happens on a cold cache.
- **SEC instances need `http_user_agent` with an email; `parse_xbrl_file` raises `ValueError` before Arelle
  runs.** xbrl.sec.gov still answered Arelle's default agent on 2026-10-11, but www/data.sec.gov already
  return 403 for it, and a failed taxonomy download is not an error in Arelle: it logs `IOerror` /
  `xbrl:schemaImportMissing` and returns the instance with most facts gone (Apple FY2023: 78 of 1,164;
  the parser now raises on those codes, see below). The check applies even on a warm cache, so a parse doesn't depend on the machine. The rule ("@" after
  stripping) mirrors `sec.Client`'s `_validate_user_agent`; change both together. DART needs no agent.
- An SEC instance is recognized by `xbrl.sec.gov/dei` in its first 8KB (the root element's namespace
  declarations; within 2KB in every filing checked, 2011–2025, extracted, pre-2019 and inline `.htm`).
  DART instances never declare it. The CIK context scheme can sit at the end of the file, so it's not used.

## Arelle load errors that raise

- Arelle never raises when a referenced file (linkbase, company schema, taxonomy) can't be read; it logs and
  returns a model missing whatever that file defined. `_raise_on_unreadable_files` raises `XbrlParseError` on
  `IOerror` or `xbrl:schemaImportMissing`, naming files from `model_xbrl.urlUnloadableDocs`. Measured
  2026-10-11: neither code in 35 complete filings (SEC AAPL/MSFT/JPM 2011–2025, DART three companies
  FY2011–2024); `IOerror` in every broken case (DART ZIP extracted flat, offline with an empty cache).
- Left out on purpose: `xmlSchema:valueError` (8 in one complete DART FY2024 filing — a malformed value, not a
  missing file) and `xmlSchema:elementUnexpected` (only ever a side effect of a missing taxonomy). Add a code
  only after checking it never appears in complete filings.
- DART ZIPs for FY2022 and earlier keep their linkbases in `\`-named subfolders. Extracted flat (plain
  `extractall` on macOS/Linux) they now raise here; cluefin-openapi's `download_financial_statement_xbrl`
  extracts them correctly.

## DART/Arelle quirks baked into the code

- Arelle stores `instant`/`endDate` as *exclusive* datetimes (midnight of the next day);
  the parser subtracts one day to recover the reporting date. Any period logic must
  preserve this offset or dates shift by one day.
- Statement-type detection matches linkrole URIs against undocumented DART role codes, taken from real
  filings, not from the XBRL spec. A statement has presentation variants with their own code family: BS
  `D21`/`D22`, IS `D31`/`D32`, CIS `D41`/`D42`/`D43`, CF `D51`/`D52`, SCE `D61`; notes are `D8x`. A filer that
  presents a single 포괄손익계산서 (`D43`) has **no IS** — the profit lines are in CIS only; don't synthesize one.
- Financial filers use their own families with a letter after `D`: `DB` 은행, `DI` 보험, `DS` 증권, `DX` 기타 금융
  (금융지주). Codes `22`=BS, `32`=single 포괄손익계산서 (→ CIS, no IS), `52`=CF, `61`=SCE, `8x`=notes; `0`/`5`
  endings mean 연결/별도 as in `D`. Observed in every bank/insurer/securities/holding filing FY2023–2025 (2026-11-09).
  Without them these filings parsed to no statements at all. 지주회사 KSIC 64992 can be either `DX` or plain `D`.
  Financial filers' notes are in XBRL only from FY2025.
- 연결/별도 is decided by the role code's **last digit** (`5` = 별도, anything else = 연결), not by linkrole
  order: consolidated statements go to `statements`, separate ones to `separate_statements`. A company without
  subsidiaries has an empty `statements`. Within one basis the first role of a type still wins ("keep first
  match per type"), which matters only if a filing carries two variants of one statement.
- Arelle's session state is not thread-safe; a module-level lock serializes concurrent
  `parse_xbrl_file` calls silently — parallelizing parsing buys nothing.

## SEC filings

- Statement roles are identified by the role **definition** ("0000002 - Statement - CONSOLIDATED BALANCE
  SHEETS", EDGAR Filer Manual 6.7.12), not the URI: URIs are filer-chosen, and disclosure roles such as
  `.../BalanceSheetComponentsDetails` would match the URI patterns. Only `Statement` roles count; titles with
  "Parenthetical" are skipped. Any SEC-format definition switches that role to this path; DART roles never match.
- Arelle's role order is not the filing order, so SEC roles are sorted by sort code before "keep first
  match per type". Documents without SEC definitions (DART) keep the loader order.
- SEC statements draw their own axes in the presentation tree (Apple's income statement splits net sales by
  `ProductOrServiceAxis`; equity statements use `StatementEquityComponentsAxis`). For SEC roles, any axis present
  in the tree is intrinsic; facts on other axes (segments) are note detail and dropped. DART keeps the fixed
  `_INTRINSIC_AXES_BY_TYPE` table — the tree rule was not checked against DART filings.
- `reporting_period_end` comes from `dei:DocumentPeriodEndDate` when present. The latest instant is wrong for
  SEC: cover-page shares outstanding are dated weeks after the period end.
- Inline XBRL tags a number everywhere it appears, and the SEC-extracted instance keeps every copy (Apple
  FY2023: revenue 3×, net income 4×). `_collect_line_items` collapses facts with the same context, unit and
  value, comparing numbers as numbers — Microsoft FY2026 tags the same EPS as "18.00" and "18". The integration
  test asserts exactly one row per value so this cannot regress silently.
- Newer filings embed the linkbases in the company schema: Microsoft FY2026's folder has only
  `msft-20260630.xsd` and `msft-20260630_htm.xml`. Never require separate `_pre/_cal/_lab.xml` files.
- `extract_notes` is DART-only (it keys on role codes matching `D[BISX]?8…`). Labels are the concept's standard label; the
  preferredLabel's *text* ("Total net sales") is not read, only its role (`preferred_label` on nodes and line items).
- A balance drawn twice in one statement — beginning and ending row, told apart only by `periodStartLabel` /
  `periodEndLabel` (SEC: equity in SCE, cash in CF) — is split by `_split_period_balances`: the beginning row keeps
  the day before a duration's start date, the ending row the end date. Measured 2026-10-11 on 8 SEC filings
  (10-K and 10-Q): 18 such pairs, every one of their 254 instants landed on one row or both, none on neither.
- Only pairs are split. DART never drew one (29 filings, three companies, FY2011–2024, same date): its SCE has a single
  `periodEndLabel` equity row, and FY2011 filings put the FY2010 opening equity on that row and nowhere else, so
  filtering it would drop the value. DART's own beginning-of-period concepts (`...AtBeginningOfPeriodCf`,
  `EquityAtBeginningOfPeriod`) are tagged at the **column's end date** and need no split.
- Fact order inside one row changes between runs of the same file (Arelle); compare statements as row sets.

## Testing gotchas

- Fixtures in `tests/fixtures/` are hand-authored minimal synthetic XBRL (despite
  real-looking DART entity ids). There is no tooling to regenerate them from a live
  filing; realistic test data must be hand-crafted or manually trimmed from a download.
- Don't add `tests/__init__.py`: two top-level `tests` packages once collided (2026-02). The root config now
  runs pytest with `--import-mode=importlib`, so same-named test files across packages are fine without it.
- `CLUEFIN_XBRL_TEST_DIR` is **one extracted DART filing folder**, not a corpus. The two DART integration tests
  expect a general filer with subsidiaries: exactly BS/IS/CIS/CF/SCE consolidated, a separate BS, note codes
  starting `D8` and a 종업원급여 note. A bank, insurer, securities firm or holding company fails them (no IS,
  notes under `DB8…`), as does a single-statement (`D43`) filer or one without consolidated statements.
- `-m integration` also runs the SEC tests whenever `SEC_USER_AGENT` is in `.env.test`: they download two 10-Ks
  and, on a cold Arelle cache, the US-GAAP taxonomies.
- The first parse on a cold cache took up to ~76 s for a DART filing (2026-09-30); later ones read the cache.
- Arelle prints `[info] loaded …` to **stdout**. A caller whose stdout is data (the CLI's JSON) must wrap the
  parse in `contextlib.redirect_stdout(sys.stderr)`; tests that monkeypatch the parser don't show the problem.
