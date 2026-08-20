# AGENTS.md — cluefin-xbrl

Non-obvious constraints only; see the root AGENTS.md for repo-wide rules.

## Scope

- This package is a **pure local-file parser** — it never talks to DART. The download
  path (ZIP fetch + unzip) lives in cluefin-cli / cluefin-openapi's dart module. A
  missing download function here is intentional, not a gap.

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

## Testing gotchas

- Fixtures in `tests/fixtures/` are hand-authored minimal synthetic XBRL (despite
  real-looking DART entity ids). There is no tooling to regenerate them from a live
  filing; realistic test data must be hand-crafted or manually trimmed from a download.
- `tests/__init__.py` was deliberately deleted to fix a pytest collision — don't re-add.
- Notes-extraction / consolidated-vs-separate filtering work already exists on the
  unmerged branch `feat/xbrl-extract-notes-design`; check it before building either.
