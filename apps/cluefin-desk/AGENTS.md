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
- KIS 랭킹 조회의 `fid_cond_scr_div_code` 등 화면코드는 KIS 포털이 요구하는 고정 키다
  (`data/fetcher.py`). 통합테스트 값과 다르게 바꾸면 오류 없이 빈 응답이 온다.
- KIS 재무 시계열은 문서와 달리 진행연도 누적 행이 맨 앞에 온다(실측).
  `_split_annual_and_ytd` 를 우회해 첫 행을 연간으로 쓰면 ROE·성장률이 부풀려진다.

## 지표 → ML 피처 경로

- `TechnicalAnalyzer.calculate_all` 은 호출자가 `screens/stock_detail.py` 하나뿐이고
  **이를 실행하는 테스트가 없다.** 산출 DataFrame 은 `predictor.prepare_data`/`predict` 의
  `indicators` 인자로 그대로 흘러간다 — 선언은 `Dict` 인데 DataFrame 을 넘기며
  `DataFrame.items()` 가 `(컬럼, Series)` 를 내주는 덕에 동작한다.
- `ml/feature_engineering.create_talib_features` 가 그중 14개 컬럼을 자기 talib 버전으로
  덮어쓴다. 실제 모델 피처로 살아남는 것은 `sma_50`·`sma_120`·`sma_240`·`rsi`·
  `macd_histogram`·`adx`·`resistance`·`support` 8개뿐이다. **컬럼 이름을 바꾸면 테스트는
  하나도 안 깨지고 모델 피처 벡터만 조용히 바뀐다.**
- `resistance`/`support` 는 행이 20개 이상일 때만 붙는다 — 행 수에 따라 출력 스키마가 달라진다.

## Panel conventions

- A tab that fails must say so **in that tab**. Loaders that only `logger.error(...)`
  leave the panel on its `Loading ...` placeholder forever, which reads as a hang.
  `financial_analysis` / `stock_detail` show the pattern: a `_guarded(selector, label, fn)`
  wrapper per tab, `_update_panel` for the write, and pure `_format_*_lines(...)`
  staticmethods that return `list[str]` (that is what unit tests exercise — the loaders
  themselves only do I/O).
- Screen-level `load_all_data` workers are `exclusive=True` with their own `group`;
  without it, `r` mashing runs overlapping workers into the same panels.
- Worker-side UI helpers live in `screens/_guard.py`: wrap each loader in
  `guarded(self, selector, label, fn, *args)` (logs + shows `… 로딩 실패` in the panel) and
  update a `Static` with `set_text(self, selector, text)`. Any hand-written
  `except Exception as e:` in a worker must start with `if screen_gone(self, e): return`.
  Switching screens mid-load detaches the old screen, and its worker then raises
  `NoActiveAppError` — an *empty-message* exception — on `self.app`; without the guard
  that cancellation is logged as `Failed to load …: ` with no reason.
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
