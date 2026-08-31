# AGENTS.md — cluefin-desk

Non-obvious constraints only; see the root AGENTS.md for repo-wide rules.

## Real-account behavior

- `Settings` loads `.env` **cwd-relative**, so launching from the repo root uses the
  production Kiwoom credentials, and `DomesticDataFetcher.__init__` authenticates
  (real network call) at app startup before any screen renders. The app is read-only —
  no order/account-mutation code exists — so exposure is auth/API usage, not trades.

## Conventions for new screens

- The fetcher and screener are app-lifetime singletons: use `self.app.fetcher` /
  `self.app.screener`. Constructing another `DomesticDataFetcher` re-authenticates.
  The DART client is different on purpose — a lazy property on the App, created only
  when `dart_auth_key` is set; follow that pattern for optional data sources.
- KIS is an optional enrichment source: `fetcher.kis_client` is a lazy property that
  authenticates (real network call) on first access and raises `ValueError` without
  keys. Gate KIS-backed UI on `fetcher.has_kis` — never let a missing-key error take
  down a screen that also renders Kiwoom data.
- I/O uses `@work(thread=True)` workers with `self.app.call_from_thread(...)` for UI
  updates — not `async/await`, even though some fetcher methods are declared `async`.
  Check call sites before extending those.

## Testing & dead code

- There is no TUI test harness (no Pilot/snapshot tests, no conftest); only the
  screener logic is tested, with the fetcher mocked. Instantiating a real
  `DomesticDataFetcher` in a test triggers a live auth call against whatever `.env`
  is in cwd.
- The `xbrl` optional extra in pyproject is dead — nothing in the app imports it;
  `financial_analysis` uses the DART client only.
