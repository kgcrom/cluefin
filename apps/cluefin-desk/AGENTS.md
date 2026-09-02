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

## Panel conventions

- A tab that fails must say so **in that tab**. Loaders that only `logger.error(...)`
  leave the panel on its `Loading ...` placeholder forever, which reads as a hang — the
  bug class that shipped in the cli→desk port. `financial_analysis` /  `stock_detail`
  show the pattern: a `_guarded(selector, label, fn)` wrapper per tab, `_update_panel`
  for the write, and pure `_format_*_lines(...)` staticmethods that return `list[str]`
  (that is what unit tests exercise — the loaders themselves only do I/O).
- Screen-level `load_all_data` workers are `exclusive=True` with their own `group`;
  without it, `r` mashing runs overlapping workers into the same panels.
- DART 정기보고서 조회는 `_fetch_with_year_fallback` 로 직전 사업연도부터 뒤로 물러난다
  — 사업보고서는 사업연도 종료 후 90일 안에 제출되므로 연초에는 직전 연도 것이 없다.
  데이터가 없을 때 DART 는 예외가 아니라 status 013 + `list=None` 로 200 을 준다.
- 한글은 터미널에서 두 칸을 쓴다 — 컬럼 정렬은 `f"{name:<20s}"` 대신
  `cluefin_desk.formatting.pad` 를 쓴다.

## Testing

- TUI 하네스가 7화면 전부에 있다: `tests/unit/test_<screen>.py` (market_overview ·
  screening · theme_sector · etf_analysis · investor_flow · stock_detail ·
  financial_analysis_screen). 화면을 띄우는 테스트는 `CluefinDeskApp` 대신
  그 파일들의 `HarnessApp`(App 서브클래스 + fake fetcher/screener/dart client)을 쓴다 —
  `CluefinDeskApp.__init__` 은 생성만으로 실계좌 인증을 때린다. 같은 이유로 테스트에서
  실제 `DomesticDataFetcher` 를 만들면 cwd 의 `.env` 로 라이브 인증이 나간다.
- 패널 텍스트는 `str(widget.content)` 로 읽는다 (textual 8 의 Static 에는
  `renderable` 이 없다). 워커를 기다릴 때는 `await pilot.pause()` →
  `await app.workers.wait_for_complete()` → `await pilot.pause()`.
- `pytest-asyncio` 는 strict 모드다 — async 테스트에 `@pytest.mark.asyncio` 를 붙인다.
