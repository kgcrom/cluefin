# AGENTS.md — cluefin-feeds

Non-obvious constraints only; see the root AGENTS.md for repo-wide rules.

## Scope

- Public data feeds and files that are not broker/disclosure OpenAPIs (those live in cluefin-openapi, ECOS
  included). One submodule per source. The HTTP helper (`_http.HttpClient`) is local on purpose — feeds must not
  import cluefin-openapi's private `_http_base`.
- Fetch and parse only. No caching or "once a day" policy here; callers store what they need.

## Server behavior the code can't show (measured 2026-10-19)

- **Treasury**: an empty month (start of month, future) or a bad period is HTTP 200 with an empty feed, not an
  error. Tenors that did not exist yet (1.5/2/4-month) are absent elements → `None`.
- **BLS**: errors are HTTP 200 with a non-`REQUEST_SUCCEEDED` body `status`. An unknown series is
  `REQUEST_SUCCEEDED` + a `message` and empty data. A range over the per-request year limit is **cut to its first
  10 (v1) / 20 (v2) years** with only a warning message, so `timeseries` splits ranges itself — don't remove that.
  Missing values are `"-"` with a footnote (2025-10 shutdown). `REQUEST_NOT_PROCESSED` (daily limit) is from the
  docs, not measured. Integration tests use v1's 25 requests/day: keep them few.
- **Damodaran**: no API, files change shape over the years. Columns are found by header name (the CRP page has
  typos: "Sovereignn CDS", "ERP based on sovereign CDSS"), never by position. `ctryprem.html` is latin-1 and its
  table has an empty spacer row. xls files need the `damodaran` extra (`xlrd`); the newer quarterly
  `ctryprem*.xlsx` would need openpyxl and is out of scope. `indname.xls` is ~22MB; industry names there match the
  β tables' `Industry Name` exactly (all 88 Korean industries matched the emerging table, 2026-01 data).
