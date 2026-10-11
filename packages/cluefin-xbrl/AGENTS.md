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
  `xbrl:schemaImportMissing` and returns the instance with most facts gone (Apple FY2023: 78 of 1,164).
  The check applies even on a warm cache, so a parse doesn't depend on the machine. The rule ("@" after
  stripping) mirrors `sec.Client`'s `_validate_user_agent`; change both together. DART needs no agent.
- An SEC instance is recognized by `xbrl.sec.gov/dei` in its first 8KB (the root element's namespace
  declarations; within 2KB in every filing checked, 2011–2025, extracted, pre-2019 and inline `.htm`).
  DART instances never declare it. The CIK context scheme can sit at the end of the file, so it's not used.

## DART/Arelle quirks baked into the code

- Arelle stores `instant`/`endDate` as *exclusive* datetimes (midnight of the next day);
  the parser subtracts one day to recover the reporting date. Any period logic must
  preserve this offset or dates shift by one day.
- Statement-type detection matches linkrole URIs against undocumented DART role codes
  (`D21xxxx`=BS, `D31`=IS, `D41`=CIS, `D52`=CF, `D61`=SCE, `D8x`=notes) — these came
  from observing real filings, not from the XBRL spec.
- "Keep first match per type" in `extract_financial_statements` assumes DART orders
  consolidated linkroles before separate ones. That's an observed ordering, not a
  guaranteed invariant.
- Arelle's session state is not thread-safe; a module-level lock serializes concurrent
  `parse_xbrl_file` calls silently — parallelizing parsing buys nothing.

## SEC filings

- Statement roles are identified by the role **definition** ("0000002 - Statement - CONSOLIDATED BALANCE
  SHEETS", EDGAR Filer Manual 6.7.12), not the URI: URIs are filer-chosen, and disclosure roles such as
  `.../BalanceSheetComponentsDetails` would match the URI patterns. Only `Statement` roles count; titles with
  "Parenthetical" are skipped. Any SEC-format definition switches that role to this path; DART roles never match.
- Arelle's role order is not the filing order, so SEC roles are sorted by sort code before "keep first
  match per type". Documents without SEC definitions keep the loader order (the DART assumption above).
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
- `extract_notes` is DART-only (it keys on `D8xxxxx` role codes). Labels are the concept's standard label;
  SEC presentation `preferredLabel`s ("Total net sales") are not read yet. One visible consequence: a concept
  shown twice as beginning and ending balance (`StockholdersEquity` in SCE, period-end cash in CF) gets every
  instant on both rows, because only the `periodStartLabel`/`periodEndLabel` tells them apart.

## Testing gotchas

- Fixtures in `tests/fixtures/` are hand-authored minimal synthetic XBRL (despite
  real-looking DART entity ids). There is no tooling to regenerate them from a live
  filing; realistic test data must be hand-crafted or manually trimmed from a download.
- `tests/__init__.py` was deliberately deleted to fix a pytest collision — don't re-add.
