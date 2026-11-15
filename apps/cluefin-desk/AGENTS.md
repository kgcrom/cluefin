# AGENTS.md — cluefin-desk

Non-obvious constraints only. Repo-wide rules are in the root AGENTS.md; the cwd `.env`, "read-only but issues real
tokens" and the KST clock rule are in `apps/AGENTS.md`.

## Real-account behavior

- `config/settings.py` runs `Settings.from_env()` **at import**, so importing `app` or `data.fetcher` already reads
  `<cwd>/.env` (real environment variables override the file). Don't monkeypatch that global: tests pass
  `Settings(brokers=BrokerClientConfig(...))` to `DomesticDataFetcher` and patch auth in
  `cluefin_openapi.client_factory`.
- `CluefinDeskApp()` builds the Kiwoom client before any screen renders. A still-valid token in the disk cache is
  reused; a token is issued (network) only when the cache is missing or expired. Without Kiwoom keys the constructor
  raises `ValueError` and nothing starts.
- Clients come from `BrokerClientFactory`, so `CLUEFIN_OPENAPI_CACHE_DIR` (token cache location) and
  `CLUEFIN_OPENAPI_DEBUG` apply to desk too. Only `KIS_HTS_USER_ID` is desk's own setting.
- Logs are readable only with Textual devtools attached. `app._configure_logging` installs `TextualHandler`, but
  Textual 8.0 runs thread workers without the app context, so every record logged inside `@work(thread=True)` —
  nearly all fetch failures — takes the handler's stderr fallback, and a running app captures stdout/stderr and
  forwards them only to the devtools console. `textual console` ships in `textual-dev`, which is not a workspace
  dependency, and `TEXTUAL_LOG=<file>` receives UI-thread records only (headless probe, 2026-11-15). So a failure
  must be written into its panel (Panel conventions); tests read logs with `caplog`.
- For the same reason never `print`, and never call `ml/predictor.py`'s `display_*` methods (they print through a
  rich `Console`) from a screen — render the returned dict/metrics into a `Static`.

## Conventions for new screens

- Optional data sources are lazy: `app.dart_client` is created only when `dart_auth_key` is set, and
  `fetcher.kis_client` gets its token on first access and raises `ValueError` without keys. Gate KIS-backed UI on
  `fetcher.has_kis` — never let a missing-key error take down a screen that also renders Kiwoom data.
- I/O uses `@work(thread=True)` workers with `self.app.call_from_thread(...)` for UI
  updates — not `async/await`, even though some fetcher methods are declared `async`.
  Check call sites before extending those.
- A `DataTable` consumes Enter before the Screen's `enter` binding sees it. Handle `DataTable.RowSelected`; the binding
  alone does nothing while the table has focus (investor-flow sector table, 2026-09-02).
- Never override `Widget._render` — it is the hook Textual calls to get the Visual, and a widget that redefines it
  draws nothing (market bar, 2026-11-04). Name such helpers something else (`_refresh_text`).
- KIS blocked its 7 종목분석 endpoints on 2026-11-11 (data licence). The "KIS 재무" tab and the company widget's
  financials block were removed and not replaced — the DART tab has the same numbers — so `roe` exists only on the
  Kiwoom path of `get_basic_data`. Don't add them back.
- The root `.gitignore` ignores `data/`, with an exception for `src/cluefin_desk/data/`. Before that exception new
  modules there silently dropped out of git and ruff (2026-10-17); a new directory named like an ignored pattern
  will do the same.
- KIS 랭킹 조회의 `fid_cond_scr_div_code` 등 화면코드는 KIS 포털이 요구하는 고정 키다
  (`data/fetcher.py`). 통합테스트 값과 다르게 바꾸면 오류 없이 빈 응답이 온다.
- `KIS_HTS_USER_ID`(관심종목 화면)는 KIS 관심종목 API 의 요청 파라미터다. 값을 화면·로그·테스트 픽스처에
  남기지 않는다 — 네트워크 오류 메시지에는 쿼리 문자열이 붙은 URL 이 실릴 수 있어서 fetcher 의 `_hts_call` 이
  가린 뒤 다시 던진다. 관심종목 호출을 추가하면 이 래퍼를 거친다.
- KIS 조건검색(`psearch-*`)은 HTS [0110] 에서 서버저장한 조건식만 읽는다. 저장된 조건식이 없으면 HTTP 200 +
  `rt_cd=1` `MCA05762` "조회가 계속 됩니다" 가 온다(2026-10-17 실측). MTS 만 쓰는 계정은 조건식을 만들 수 없어
  화면을 두지 않았다. 관심 그룹은 MTS 에서 만든 것도 바로 보인다.
- 종목코드는 숫자만이 아니다 — 신규 상장·우선주 일부가 `0001A0`·`00088K` 꼴이다.
  코드 형식을 `isdigit()`·`[0-9]{6}` 로 거르지 않는다(`data/listing.is_stock_code`).

## 키움 조회 함정

키움은 조건 코드가 틀려도 오류 없이 그럴듯한 목록을 준다. 응답이 왔다는 것으로 확인하지 말고, 상위 몇 종목이 탭
이름과 맞는지 내용으로 확인한다. 아래는 화면에서 드러난 것이고(대부분 2026-11-08), 쓰는 값은 `data/fetcher.py` 에 있다.

- ka10027(등락률 상위) `sort_tp`: 1 상승률·3 하락률, 2·4 는 상승폭·하락폭(금액)이다. 하락률 탭이 2 를 불러 상승
  종목을 보였다. 상·하한가를 빼면 +30% 종목이 상승률 순위에서 사라지므로 넣는다.
- ka10034(외인 매매 상위) `trde_tp`: 1 순매도·2 순매수. "외인 순매수" 탭과 투자자 화면이 1 을 부르고 있었다.
- ka10016(신고가): 문서 밖 값(`dt=1`, `stk_cnd=4`)을 주면 900번대 외국기업만 온다. `stk_cnd=16`(ETF·ETN 제외)은
  문서에 없지만 서버가 받는다 — 빼지 않으면 채권 ETF 가 상위를 채운다.
- 거래대금 순위는 ka10032 가 아니라 ka10030 `sort_tp=3` 으로 받는다. ka10032 에는 ETF 를 뺄 조건이 없다.
- ka10051·ka20002 의 `mrkt_tp` 는 한 자리다(코스피 0·코스닥 1). `"0001"` 을 주면 코스닥으로 읽힌다(2026-09-02).
  ka10051 의 `cur_prc`·`pred_pre`·`flu_rt` 는 소수점을 뺀 100배 정수다(`-210` = -2.10%).
- 가격·수량 문자열에 등락 부호가 붙어 온다(`-270406`, `--5516442`). 그대로 숫자로 바꾸면 하락일 가격이 음수가 되고
  (ML 입력 OHLCV 가 음수였다), 부호가 겹친 값은 변환에 실패해 0 으로 보였다. 숫자는 `DomesticDataFetcher._safe_float`,
  가격·거래량은 거기에 `abs()`, 표에 찍는 수량은 `screener._signed_int` 를 거친다.
- 연속조회에서 서버는 요청 헤더 `cont-yn` 만 읽는다. 다른 철자로 2쪽을 요청하면 1쪽이 다시 온다(ka90001). 그래서
  반복은 응답의 `cont_yn` 이 `Y` 가 아니거나 `next_key` 가 비면 끝내고, 쪽수 상한도 둔다(종목 목록 20쪽, 일봉 3쪽).
- ka10099(종목 목록) `mrkt_tp=0` 응답에 거래소 ETF·ETN·리츠가 이미 들어 있다 — 0 과 10 두 번이면 전부고, 다른 시장
  코드를 더하면 겹친다. 앱 실행당 한 번만 받고, 받지 못해도 검색 창에서 6자리 코드는 그대로 열린다.
- 뺀 랭킹 탭은 다시 넣지 않는다. KIS 배당수익률은 시가배당수익률이 아니라 액면 기준 값(주당배당금과 같은 수)이라
  순위에 의미가 없고, KIS 신용 상위는 키움 신용비율 상위와 같은 종목이다.

## 지표 → ML 피처 경로

- `TechnicalAnalyzer.calculate_all` 의 DataFrame 이 `predictor.prepare_data`/`predict` 의 `indicators` 인자로 그대로
  간다. 선언은 `dict` 인데 DataFrame 을 넘기며, `DataFrame.items()` 가 `(컬럼, Series)` 를 내주는 덕에 동작한다.
- `ml/feature_engineering.create_talib_features` 가 이름이 같은 컬럼을 자기 값으로 덮어쓴다(그 파일의 `talib` 은
  `cluefin_ta` 의 별칭이다 — C TA-Lib 이 아니다). 덮이지 않고 모델 피처로 남는 것은 `sma_50`·`sma_120`·`sma_240`·`rsi`·
  `macd_histogram`·`adx`·`resistance`·`support` 다. 컬럼 이름·순서와 이 컬럼들의 값은
  `tests/ml/test_indicators_unit.py` 가 리팩터 전 구현과 비교해 고정한다.
- `calculate_all` 에서 cluefin-ta 로 옮긴 것은 SMA·OBV·ADX·ATR 뿐이다(2026-11-04). EMA·RSI·MACD·볼린저·스토캐스틱은
  일부러 직접 계산한다 — cluefin-ta 는 정의가 달라(Wilder 평활 RSI, SMA 로 시작하는 EMA, 모표준편차 밴드) 바꾸면
  모델 피처 값이 달라진다. 그래서 피처 `rsi`·`macd_histogram` 은 차트 탭 지표 패널과 CLI `kis chart technical`
  (둘 다 cluefin-ta)의 숫자와 다르다. Wilder RSI 는 `rsi_14` 로 따로 들어간다. 한쪽에 맞춰 고치지 않는다.
- `resistance`/`support` 는 행이 20개 이상일 때만 붙는다 — 행 수에 따라 출력 스키마가 달라진다.
- 피처는 그 봉까지의 데이터로만 계산한다. 지금까지 고친 미래 누수:
  - `resistance`/`support` 가 `center=True` 창이라 다음 5봉을 미리 봤다 → 직전 10봉(2026-11-08).
  - SMOTE 가 시간순 분할 전에 전체 기간에 돌아 검증 구간 봉이 합성 행에 섞였다 → 뺐다(2026-11-08). imbalanced-learn 이
    scikit-learn 1.8 과 맞지 않아 import 부터 실패한 채 조용히 꺼져 있기도 했다. 불균형은 LightGBM
    `class_weight="balanced"` 로만 다루고, 가중치는 분할 뒤 학습 구간에서 잡는다.
  - cluefin-ta 의 `REGIME_VOLATILITY` 가 전 구간 NATR 백분위를, `REGIME_HMM` 이 전 구간 학습을 썼다 → 그 시점까지의
    expanding 계산(2026-10-12).
  - 새 피처를 넣으면 `test_resistance_support_do_not_look_ahead` 처럼 뒤 봉을 바꿔도 앞 행이 그대로인지 확인한다.
- 값이 전부 NaN 인 피처 열은 `dropna` 가 학습 행을 전부 지우게 만든다. 봉이 모자라 HMM 상태가 전부 NaN 이면 HMM
  열을 넣지 않는 이유다.
- ML 탭에 나오는 것은 LightGBM feature importance 다. SHAP explainer 는 학습 때 만들어지지만 화면은 쓰지 않는다.

## Panel conventions

- A tab that fails must say so **in that tab**. Loaders that only `logger.error(...)`
  leave the panel on its `Loading ...` placeholder forever, which reads as a hang. Wrap each loader in
  `_guard.guarded(self, selector, label, fn, *args)` and write with `set_text(self, selector, text)`.
- Any hand-written `except Exception as e:` in a worker must start with `if screen_gone(self, e): return`.
  Switching screens mid-load detaches the old screen, and its worker then raises
  `NoActiveAppError` — an *empty-message* exception — on `self.app`; without the guard
  that cancellation is logged as `Failed to load …: ` with no reason.
- Load workers are `exclusive=True` with their own `group`; without it, `r` mashing runs overlapping workers into
  the same panels.
- An empty table is not "no data". `StockScreener` swallows failures and returns `[]` (`test_screener_unit.py`
  expects it), and the KIS wrappers in `fetcher` degrade API/validation errors to `[]` with a warning log. A table
  screen can't tell the two apart, so its status line points at the log instead of claiming zero rows.
- Wrap every string that comes from outside in `rich.markup.escape` before it reaches a panel — names, news
  titles, exception text. Rich parses `[fnRASSI]` as a tag and drops it, `[/…]` raises `MarkupError` and fails the
  whole tab, and pydantic errors carry `[type=…]`.
- DART 정기보고서 조회는 `_fetch_with_year_fallback` 로 직전 사업연도부터 뒤로 물러난다
  — 사업보고서는 사업연도 종료 후 90일 안에 제출되므로 연초에는 직전 연도 것이 없다.
  데이터가 없을 때 DART 는 예외가 아니라 status 013 + `list=None` 로 200 을 준다.
- 한글은 터미널에서 두 칸을 쓴다 — 컬럼 정렬은 `f"{name:<20s}"` 대신
  `cluefin_desk.formatting.pad` 를 쓴다.

## Testing

- macOS 에서는 `brew install libomp` 가 먼저 필요하다(LightGBM, 루트 README).
- 화면을 띄우는 테스트는 `CluefinDeskApp` 대신 화면별 테스트 파일의 `HarnessApp`(App 서브클래스 + fake
  fetcher/screener/dart client)을 쓴다 — `CluefinDeskApp.__init__` 과 실제 `DomesticDataFetcher` 는 만드는 순간
  cwd 의 `.env` 키로 키움 인증을 한다.
- 앱 수준 바인딩·액션을 테스트할 때는 `test_stock_search_unit.py` 처럼 `CluefinDeskApp` 을 상속하고
  `App.__init__` 만 부른다. `on_mount` 를 덮어쓸 때는 `event.prevent_default()` 를 불러야 한다 — Textual 은
  부모 클래스의 `on_mount` 도 부르므로 막지 않으면 실제 시장 개요 화면이 떠 라이브 조회를 한다.
- 패널 텍스트는 `str(widget.content)` 로 읽는다 (textual 8 의 Static 에는
  `renderable` 이 없다). 워커를 기다릴 때는 `await pilot.pause()` →
  `await app.workers.wait_for_complete()` → `await pilot.pause()`.
- `pytest-asyncio` 는 strict 모드다 — async 테스트에 `@pytest.mark.asyncio` 를 붙인다.
