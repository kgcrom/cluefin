# AGENTS.md — cluefin-feeds

Non-obvious constraints only; repo-wide rules are in the root AGENTS.md and `packages/AGENTS.md` (pydantic models
are constructed by alias, XML is parsed with defusedxml). What a caller trips on — the two tax-rate units, "Korea"
vs "South Korea", the trailing Total Market rows, `krx_code` — is in the README and not repeated here.

## Scope

- Public data feeds and files that are not broker/disclosure OpenAPIs (those live in cluefin-openapi, ECOS
  included). One submodule per source. The HTTP helper (`_http.HttpClient`) is local on purpose — feeds must not
  import cluefin-openapi's private `_http_base`.
- Fetch and parse only. No caching or "once a day" policy here; callers store what they need.
- The only consumer inside the repo is the Damodaran country-risk-premium table: the CLI's
  `kis stock implied-expectations` reads Korea's ERP and tax rate from it (see `apps/cluefin-openapi-cli/AGENTS.md`).
  Treasury, BLS and the Damodaran xls tables are reached only by this package's tests, so a vendor change there
  shows up in the integration tests or nowhere.

## Server behavior the code can't show (measured 2026-10-19)

- **Treasury**: an empty month (start of month, future) or a bad period is HTTP 200 with an empty feed, not an
  error. Tenors that did not exist yet (1.5/2/4-month) are absent elements → `None`. The row model is
  `extra="allow"` so a new tenor does not break parsing, and the integration test asserts `model_extra` is empty —
  when it fails, declare the new field; do not relax the assert.
- **BLS**: errors are HTTP 200 with a non-`REQUEST_SUCCEEDED` body `status`. An unknown series is
  `REQUEST_SUCCEEDED` + a `message` and empty data. A range over the per-request year limit is **cut to its first
  10 years** (v1) with only a warning message, so `timeseries` splits ranges itself — don't remove that. The 20-year
  v2 limit is from the BLS FAQ; its cut was not measured. Missing values are `"-"` with a footnote (2025-10
  shutdown). `REQUEST_NOT_PROCESSED` (daily limit) is from the docs, not measured.
- **BLS key**: the registration key travels in the POST body, so an exception must never carry the body
  (`test_key_is_not_in_error`). Integration tests send `BLS_REGISTRATION_KEY` from `.env.test` when it is set (v2);
  without it they run on v1's 25 requests/day, so keep them few.
- **Damodaran**: no API, files change shape over the years. Columns are found by header name (the CRP page has
  typos: "Sovereignn CDS", "ERP based on sovereign CDSS"), never by position. `ctryprem.html` is latin-1 and its
  table has an empty spacer row. xls files need the `damodaran` extra (`xlrd`); the newer quarterly
  `ctryprem*.xlsx` would need openpyxl and is out of scope. `indname.xls` is ~22MB; industry names there match the
  β tables' `Industry Name` exactly (every Korean industry matched the emerging table on 2026-01 data, and an
  integration test asserts it).
- Catch `xlrd.biffh.XLRDError`, not `xlrd.XLRDError`: the latter is missing from xlrd's type stubs and fails
  pyright. It is what a non-xls body (an HTML "moved" page) raises, turned into `FeedParseError`.
