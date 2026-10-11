# AGENTS.md — cluefin-xbrl

Non-obvious constraints only; see the root AGENTS.md for repo-wide rules.

## Scope

- This package is a **pure local-file parser** — it never talks to DART or SEC. The download
  path lives in cluefin-openapi (`dart` ZIP fetch, `sec.archives.download_xbrl_files`). A missing
  download function here is intentional, not a gap.
- Arelle itself does go online: it fetches the taxonomies an instance imports (US-GAAP from
  xbrl.fasb.org, DEI/SRT from xbrl.sec.gov) on first use and caches them. Unlike www/data.sec.gov,
  xbrl.sec.gov answered 200 to Arelle's default agent (2026-10-11). `http_user_agent` is there to declare
  the caller per SEC policy, not because parsing fails without it.

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
  value; the integration test asserts exactly one row per value so this cannot regress silently.
- `extract_notes` is DART-only (it keys on `D8xxxxx` role codes). Labels are the concept's standard label;
  SEC presentation `preferredLabel`s ("Total net sales") are not read yet. One visible consequence: a concept
  shown twice as beginning and ending balance (`StockholdersEquity` in SCE, period-end cash in CF) gets every
  instant on both rows, because only the `periodStartLabel`/`periodEndLabel` tells them apart.

## Testing gotchas

- Fixtures in `tests/fixtures/` are hand-authored minimal synthetic XBRL (despite
  real-looking DART entity ids). There is no tooling to regenerate them from a live
  filing; realistic test data must be hand-crafted or manually trimmed from a download.
- `tests/__init__.py` was deliberately deleted to fix a pytest collision — don't re-add.
