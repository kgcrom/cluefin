# AGENTS.md — cluefin-openapi-cli

Non-obvious constraints only; see the root AGENTS.md for repo-wide rules. 첫 절은 이 CLI 로
데이터를 조회하는 에이전트용이고, 그 아래는 CLI 를 고치는 사람용이다.

## 에이전트가 데이터를 조회할 때

모든 명령은 저장소 루트에서 `uv run cluefin-openapi-cli …` 로 부르고 출력은 JSON 이다. 조회 전용이지만
루트 `.env` 의 **실계좌** 자격증명으로 토큰이 발급된다. 자격증명 값은 어디에도 찍지 않는다 —
확인은 `brokers --json` 의 `credentials.configured` 로 끝낸다.

흐름은 `search` → `schema` → `--dry-run` → 실행이다. 명령·파라미터·코드값은 추측하지 말고 CLI 가 말해 주는
것을 쓴다(`search` 는 빈 결과 대신 `fallback` 을 주고, `schema` 는 바로 실행 가능한 `invoke.*` 를 준다).
여러 단계가 필요한 일은 `recipes --json` → `recipe <name> --json` 에 순서와 `agent_notes` 가 있다.

```bash
uv run cluefin-openapi-cli search 외국인 순매수 상위 --json
uv run cluefin-openapi-cli schema kis stock current-price --json
uv run cluefin-openapi-cli kis stock current-price --stock-code 005930 --dry-run --json
uv run cluefin-openapi-cli kis stock current-price --stock-code 005930 --fields current_price,per,pbr --compact
uv run cluefin-openapi-cli kis chart technical --stock-code 005930 --count 250 --json
uv run cluefin-openapi-cli recipe stock-research --json
```

CLI 가 말해 주지 않는 것만 적는다.

- **출처 역할.** KIS 가 1순위(primary), 키움은 보조(auxiliary) — `kis_alternatives` 가 `[]` 인 명령이나
  KIS 가 빈 데이터를 줬을 때만, DART·SEC 는 참고(reference) 다.
- **실적은 DART, 주당지표만 KIS.** KIS 종목분석(재무제표·재무비율) API 는 2026-11-11 서비스 종료로 없앴다.
  리포트용 숫자(최근 8분기 단독값·YoY, 3개년 손익·재무상태·현금흐름·비율, 최신 누적, TTM, 차입금)는
  **`dart financial-summary --corp-code <8자리>` 한 번**으로 받고 다시 계산하지 않는다(DART 8회, 억원). 한 보고서만
  볼 때는 `dart financial-major-accounts`(`recipe latest-earnings`), 비율·성장률의 공식 값은
  `dart financial-major-indicators`, EPS·BPS 만 KIS 다. 분기 보고서의 `thstrm_amount` 는 해당 분기 단독,
  `thstrm_add_amount` 는 연초 누적이다. 정정 전 원본 값은 `dart financial-as-filed` 뿐이다.
- **숫자가 말해 주지 않는 것은 원문에 있다.** 부문별 매출·수주·차입금 만기·우발부채는 `recipe filing-text`
  (정기보고서·감사보고서만 읽힌다), 주요사항보고서의 금액·상대방은 `dart major-event`, 배당·자사주·임원 등
  정기보고서 항목은 `dart report-item`. 미국 고객사·경쟁사 공시는 `recipe us-peer-filings`(20-F/6-K 제출사는
  못 읽는다).
- **희석·환원 이력은 `dart dilution-watch` 한 번.** CB·BW·EB·유상증자·무상증자·유무상증자·감자·자기주식
  취득/처분(신탁 포함)을 종류별로 `major-event` 를 11번 부르고 필드를 손으로 맞추는 대신, 금액·전환가·리픽싱
  최저가·신주수(부호로 증감 표시)·발행주식 대비 비율로 한 번에 받는다(기본 범위 최근 3년). 자사주 소각은 범위
  밖이라 `not_covered` 에 적힌다 — `dart report-item treasury-stock` 으로 따로 본다.
- **증권사 의견과 밸류에이션도 계산 명령이 있다.** 여러 증권사의 최근 목표가·의견은 `kis stock opinion-summary
  --stock-code`(기본 90일, 평균·중앙값·최고·최저), 시총·TTM PER·PBR·추정 연도별 PER 은
  `kis stock valuation --stock-code --corp-code`(KIS 종가 + DART 주식수 + DART 재무, 약 11회). 5년 PER·PBR 밴드와
  현재 분위는 `kis stock valuation-band --stock-code --corp-code`(로컬 `cache` 일봉 × 연도별 DART 전체
  재무제표·주식수, 실시간 KIS 호출 없음 — `cache load` 가 먼저 돌아 있어야 한다). `kis stock
  estimated-earnings` 는 한국투자증권 한 곳의 추정이라 컨센서스라 부르지 않는다(`table` 로 라벨됨). 가치투자자형
  지표(FCF 수익률, 오너 어닝스, EV/EBIT·이익수익률, PEG, 주주수익률, Altman Z 시총 원형)는 `kis stock
  investor-metrics --stock-code --corp-code`(약 12회) — ROIC·DuPont·F-Score·Z''(장부가)는 `dart
  financial-summary` 의 `quality` 블록이다.
- **매크로는 `ecos`(한국은행).** 국면을 볼 때는 **`ecos macro-snapshot` 한 번** — 기준금리·국고채 3/10년·회사채 AA-/BBB-·원/달러·
  CPI·선행/동행지수 순환변동치·ESI·BSI·CCSI·뉴스심리·GDP·수출 15계열과 장단기 금리차·신용스프레드마다 최근값·1m/3m/1y 변화·10년
  백분위(약 15회, 실키 필요). 국면 라벨은 주지 않는다 — 어느 수치에 판단을 기대는지 직접 적는다. 그 밖의 계열은 `ecos table-search` →
  `ecos items` → `ecos series` 로 찾아 받는다(통계표·항목코드를 추측하지 않는다). 지표마다 최근값 하나면 `ecos key-stats`.
  월·분기 통계는 기간이 끝나고 몇 주 뒤 올라온다 — 값마다 `time` 이 기준일이다. 장중 금리 요약은 `kis market interest-rate`.
  매크로를 웹 검색으로 대신하지 않는다 — 기준일이 섞인다.
- **기술적 지표는 `kis chart technical`.** 캔들을 받아 직접 계산하지 않는다. `signal.trend` 와
  `signal.mean_reversion` 은 별개 계열이라 하나의 점수로 합치지 않는다. 값은 `cluefin-desk` 화면과 다르다(EMA
  워밍업 차이) — 이 CLI 가 기준이다. `stop_sizing` 은 horizon(`--horizon-days 20,40,60`)별 손절폭 하한
  `1.5 × ATR14 × √(h/30)` 과 buy/sell 손절가(틱 맞춤), 20% 초과 시 `verdict_cap: watch` 다 — 손절폭을 직접 계산하지 않는다.
- **"이 종목이 돌파 대기냐"는 `kis chart trend-setup`.** 트렌드 템플릿·52주 고점갭·프랙탈 피봇과 수축·지수 대비 강도로 관심종목
  1·2·3그룹과 `alert`/`watch`/`exclude`, 피봇 기준 알림·손절가를 준다(약 12회 호출). 백테스트 정의라 `atr14_pct` 는 단순 평균이고
  technical 의 ATR(Wilder)과 다르다 — 두 값을 섞지 않는다. `action` 은 매수 추천이 아니다(`caveats`). 장 마감(15:40) 전에는 어제 기준이다.
- **전종목·과거 일봉은 로컬 캐시.** 여러 종목의 일봉, 특정 날짜의 상장 종목(폐지 포함)은 `cache ohlcv`·`cache company --as-of`
  로 읽는다(네트워크 없음). 캐시는 원주가다 — 신호는 `--adjusted true`, 백테스트 체결가는 원주가. 파일이 없으면 exit 2
  `CacheMissing`; `cache load`(첫 실행 ~2시간 20분, 이후 하루 ~7분)는 사용자가 요청할 때만 돌린다.
  지수 대비 성과(CAGR·MDD·샤프·베타·알파)는 `cache perf --code --bench U0001` — 일봉을 받아 직접 계산하지 않는다.
  그날 1·2·3그룹 종목 찾기는 `cache trend-setup`(전 종목 약 1초), 한 종목의 오늘 값은 `kis chart trend-setup`.
- **명령 하나에 Bash 호출 하나.** `for`·`while`·`$(...)`·`eval`·`bash -c` 로 여러 명령을 묶지 않는다. 호출마다 결과와
  exit code 가 따로 남아야 아래 exit code 분기를 할 수 있다. 서로 독립인 호출은 같은 턴에 병렬로 보낸다(KIS 는 동시 2개까지).
  worktree 세션에서는 `$(...)` 로 만든 값을 넘기면 CLI 도 실행 전에 거부된다(2026-11-03 실측, 리터럴 인자의 루프는 통과)
  — 루트 `AGENTS.md` 의 worktree 절.
- **응답은 작게.** `--fields`·`--limit`·`--compact`. 잘리면 `_truncated` 에 실제 `total` 이 온다. `list --json`
  을 필터 없이 부르지 않는다(61KB).
- **exit code 로 분기한다.** 0 정상 · 1 내부 오류 · 2 인자 오류(`error.data.issues[]` 읽고 고친 뒤 재시도) ·
  3 자격증명 — 키 누락·무효 모두(중단하고 보고) · 4 브로커/네트워크(`error.retryable` 이 true 일 때만 1회 재시도) ·
  5 레이트리밋(`data.retry_after` 만큼 대기, DART `status` 020 은 일일 한도라 재시도 금지). KIS 는 동시 2개까지.

## Env & safety

- Credential loading is hardcoded to `Path.cwd() / ".env"` (via
  `cluefin_openapi.client_factory`) — there is no `.env.test` or `--env-file` support,
  so running from the repo root always uses production credentials.
- Every registered command is `side_effect="read"` (asserted by a test): the CLI cannot
  place orders today. Running any kis/kiwoom command still generates and caches a real
  auth token, though. `--dry-run` is the only execution path that never touches auth.
- `brokers --json` and `--dry-run` report `credentials.configured` as a boolean derived
  from `BrokerClientConfig.from_env()`; never add the values themselves to any payload.
- `main()` sets stdlib logging to WARNING on stderr (`_configure_logging`) so agents get clean stderr. Set
  `CLUEFIN_OPENAPI_DEBUG=1` to lower the `cluefin_openapi` logger to DEBUG; the per-call DEBUG lines also need
  the client's own `debug=True`.

## Broker roles are data, not code paths

- KIS = primary, Kiwoom = auxiliary, DART, SEC and ECOS = reference — defined once in
  `metadata.BROKER_ROLES`. Ordering everywhere (`list`, `brokers`, `iter_brokers`) comes
  from `broker_rank`, not from alphabetical sorting.
- `metadata.COMMAND_TAXONOMY` is the authoritative domain/tag source, keyed by qualified
  name and **hand-authored for every command**. `_CATEGORY_DEFAULTS` survives only as
  an unreachable fallback — `test_every_command_has_hand_authored_taxonomy` fails in both
  directions, so a new command or a rename breaks CI rather than silently inheriting a
  category default. Do not reintroduce keyword-derived tags: matching is additive with no
  removal rule, so tags only ever get noisier.
- `metadata.CATEGORY_INFO` supplies the per-category prose for `<broker> --help`; the
  `domains`/`tags` shown there are a union over the real commands, not the seed values.
- `metadata.KIWOOM_KIS_ALTERNATIVES` is a hand-maintained map; a Kiwoom command missing
  from it is *declared* Kiwoom-only and shows up in `brokers --json` →
  `kiwoom_only_commands`. When adding a Kiwoom handler that overlaps KIS, add the entry
  or agents will treat it as the intended Kiwoom use. `test_agent_surface_unit.py` fails if
  any key or target is not a real command path.

## Exit codes and error envelope

- Exit codes are a contract with agents (`errors.EXIT_CODES`; mirrored in README and
  the agent section above): 2 usage/validation, 3 credentials/auth, 4 broker/network/response-parse,
  5 rate limit, 1 everything else. Do not raise `CliError` with a bare exit 1 for a
  classifiable failure — route it through `classify_exception`.
- A bad key is exit 3 too, not only a missing one: KIS token issuance 403 and DART body status 010/011/012/901 are
  raised by the client as `*AuthenticationError` (cluefin-openapi AGENTS). The DART hint names `DART_AUTH_KEY` by
  exception class, not `broker`, because `kis stock valuation` reaches DART under broker `kis`.
- Broker exceptions are classified by **class-name suffix** (`*RateLimitError`,
  `*AuthenticationError`, …) because kis/kiwoom/dart exception hierarchies are parallel
  copies. A pydantic `ValidationError` from response parsing is deliberately separated
  from broker `*ValidationError` (request rejected) — the former is `ResponseParseError`.
- DART "request limit exceeded" (status `020`, daily quota) never arrives as `DartRateLimitError`
  (that is only the local token-bucket timeout). It is a `status` in an HTTP 200 body: the XML
  paths raise a generic `DartAPIError`, and the JSON paths parse it into a normal model without
  raising. `classify_exception` maps a `*APIError` whose `response_data.status == "020"` to exit 5
  (with a daily-quota hint), and `handlers/dart.py` `_checked()` raises
  `errors.DartQuotaExceededAPIError` for the JSON models. Other non-`000` statuses (e.g. `013`
  no data) are deliberately left as they were.
- Validation (`validation.py`) runs *before* any client is created: enum, pattern,
  bounds, unknown fields, and string hardening (control chars, `..`, `%`, `?`, `#`) on
  every nested string. If a broker ever needs a literal `%`/`?`/`#` in a parameter, the
  hardening list must be made per-field, not removed.

## Commands are hand-written, not generated

- Nothing introspects `cluefin-openapi`. A new client method needs: an `@rpc_method`
  handler, an entry in that module's `_ALL_HANDLERS`, and wiring in the broker
  aggregator (`get_kis_handlers()` / `get_kiwoom_handlers()` / `DART_HANDLERS` / `SEC_HANDLERS` / `ECOS_HANDLERS`).
- The `name=` passed to `@rpc_method` controls the CLI path via dot-splitting
  (`category.leaf` for kis/kiwoom; brokers in `metadata.FLAT_BROKERS` — dart, sec, ecos — have no
  category segment) — wrong dot placement lands the command in the wrong path.
- A `category` missing from `_CATEGORY_DEFAULTS` in `metadata.py` silently falls back to
  domain `market` / tag `ranking` instead of erroring — add an entry for new categories.

## `kis chart technical`/`trend-setup`, `kis stock opinion-summary`/`valuation`/`valuation-band`/`implied-expectations`/`investor-metrics`, `dart financial-as-filed`/`financial-summary`, `ecos macro-snapshot` and the dart/sec filing-text commands compute; every other command passes through

- `dart financial-as-filed` is the second non-pass-through command: it parses a downloaded XBRL
  (see the `dart financial-*` section) and is excluded from the generic client-call tests the same way.
- `kis stock valuation` is the only **cross-broker** command: KIS close (`ohlcv.fetch_kis_daily_series`,
  unadjusted) × DART common share count (`dart share-count` of the latest periodic report) over
  `dart_handlers.collect_reports` statements, plus the KIS estimate EPS. `_BrokerSession` therefore creates
  clients per broker on demand (it used to refuse another broker's client); each broker still runs its own
  credentials check, so a missing DART key fails with exit 3 only when the command reaches DART.
  `test_kis_stock_info_handlers_unit.py` excludes it from the calls-once check; `test_kis_opinion_valuation_unit.py`
  covers it with one fake session answering both brokers. Market cap uses **issued** common shares (KRX
  convention, treasury included), preferred shares are ignored — stated in the response `notes`.
- `kis stock valuation-band` is a 5-year PER/PBR band: each cached daily close (local `cache`
  DuckDB, `cache.read.read_ohlcv`, unadjusted — **no live KIS call**, so `cache load` must already
  have run) over the EPS/BPS of the latest fiscal year already due on that day
  (`band.trailing_fiscal_year`: prior year from April 1, two back before it) — the same trailing basis
  as `current`, so the percentile compares like with like and the history never uses a report that was
  not public yet. `--years` is the price window back from `as_of`. EPS/BPS come from DART's per-stock full statements
  (`get_single_company_full_statements`, 11011 only) and common share count, fetched one fiscal
  year at a time — deliberately **not** `cache financials`/`fnlttMultiAcnt`, which has no
  지배/비지배 split (decision 2026-11-04, `docs/plans/today-bundles-plan.md` B-7, same reasoning as
  the `cache financials` bullet below). `_fetch_band_annual_reports` tries CFS across every
  requested year first and only falls back to OFS for the whole window if CFS is empty everywhere
  — one basis for the whole band, never mixed. A year whose annual report is not yet filed by
  `as_of`, or whose share count is missing, drops out of that year (never zero-filled); `current`
  uses the *latest computable* fiscal year's EPS/BPS against the most recent cached close, which
  need not be the same calendar year — stated in `current.eps_bps_year`. The multiple-series
  arithmetic (quantiles, percentile-of-current) is a pure module, `band.py`, hand-checkable in
  `test_band_unit.py`; `test_kis_stock_info_handlers_unit.py` excludes the handler from the
  calls-once check like valuation and implied-expectations; `test_kis_valuation_band_unit.py`
  covers it with a fake DART session and a real in-memory `cache` DuckDB
  (`cache.store.open_store(":memory:")`, `cache_store.open_store` monkeypatched to return it).
- `kis stock implied-expectations` reverse-engineers what today's price assumes: the steady ROE that makes
  RIM(잔여이익모델) match today's market cap, and the explicit-horizon revenue growth that makes a reverse DCF
  match today's EV — numbers and stated assumptions only, no label. It is **three-broker** (KIS price/estimate,
  DART statements/shares, ECOS 국고채 10년·회사채 AA- 3년) plus an optional Damodaran Korea ERP/tax-rate fetch
  (`cluefin_feeds.damodaran`, only when `--erp`/`--tax-rate` are not both given). The math (bisection, RIM,
  reverse DCF) is a pure module, `implied.py` — no I/O, hand-checkable against closed-form cases for small
  horizons. `_fetch_damodaran_korea` is its own function so unit tests can monkeypatch it and never touch the
  network; if it is not given `--erp` and that fetch fails, the command exits 3 with a hint to pass `--erp`
  (a missing/failing Damodaran fetch for `--tax-rate` alone instead falls back to a stated default rate — not a
  hard failure, since the plan only requires the ERP path to error). `test_kis_stock_info_handlers_unit.py`
  excludes it from the calls-once check like valuation; `test_kis_implied_expectations_unit.py` covers it with
  one fake session answering all three brokers. Depends on `cluefin-feeds` (workspace dependency, not a broker
  client — there is no `session.get_damodaran()`).
- `kis stock investor-metrics` gives value-investor metrics at a reference close: FCF yield, owner earnings (and
  its yield), EV/EBIT and earnings yield (Greenblatt magic-formula style, EBIT = 영업이익), PEG from two growth
  sources side by side, shareholder yield, and Altman Z (market-cap original). The math is a pure module,
  `investor_metrics.py` — no I/O, every metric returns `null` + `reason` instead of substituting 0 for a missing
  input (same discipline as `quality.py`). It does not recompute ROIC or Altman Z'' — those stay in `quality.py`
  (`dart financial-summary`'s `quality` block); this command only adds `quality.altman_z`, the market-cap variant
  that reuses Z'''s x1-x3 (운전자본·이익잉여금·EBIT 비율) and adds x4(시가총액/부채)·x5(매출/자산).
  `fcf_yield`/`owner_earnings`/`shareholder_yield` read the **latest annual report's own fiscal year**
  (`statements.annual()`'s last entry) because `statements.py` never builds a TTM cash-flow figure (quarterly
  cash-flow rows are year-to-date only, see the `statements.py` section) — `ev_ebit`/`earnings_yield`/`per_ttm`
  instead use TTM operating income/net income (`statements.trailing`), the same convention as `valuation`/
  `implied-expectations`. The DART EPS CAGR divides the latest and oldest of the 3 DART fiscal years' 지배주주
  순이익 by **that fiscal year's own** common-share count — the oldest year needs one extra DART
  `periodic_report_key_information.get_total_number_of_shares` call (`bsns_year` = that year, `reprt_code`
  `11011`) beyond the one `valuation`/`implied-expectations` already make for the latest year. The KIS-sourced
  growth instead reads `eps_growth_yoy` straight off `stock estimated-earnings`' table (nearest `E` period) — the
  two PEG growth sources are never averaged or made to agree. Of the two unverified `statements.py` XBRL ids,
  `proceeds_from_share_issuance` was confirmed against a real filing (2026-11-04, a stock with a large rights
  offering); `treasury_shares_disposed` is still unverified. When the cash-flow statement was read
  (`operating_cash_flow` present), `shareholder_yield` treats a missing item as no activity (0) and lists it in
  `assumed_zero` — companies don't file lines for things they didn't do; without a cash-flow statement it is null.
  `test_investor_metrics_unit.py` covers the pure functions, `test_quality_unit.py` covers `altman_z`,
  `test_kis_investor_metrics_unit.py` covers the handler with one fake session answering KIS and DART (excluded
  from the calls-once check like valuation/implied-expectations).
- `kis stock opinion-summary` is one `investment-opinion` call plus `opinions.summarize` (factory
  `opinions()`): each broker's latest row in the window, positive targets only.
- `dart financial-summary` calls `financial-full-statements` 8 times (two years × four report codes on one
  basis) and returns derived figures from `statements.py` (ported from cluefin-factory `statements.mjs`,
  archived 2026-10-18). Rules live in that module, not in docs: Q2–Q4 are year-to-date differences, a year's
  own report beats the next year's comparative column, borrowings are summed by label with a
  financial-liabilities fallback (`borrowings_basis` says which), ROE/ROA use average equity/assets.
  `test_dart_handlers_unit.py` lists it with the parsing handlers; `test_dart_financial_summary_unit.py` covers it
  with a fake keyed by (year, reprt_code, fs_div).
- The `quality` block (ROIC, DuPont, accrual ratio, Piotroski F-Score, Altman Z'') is a separate pure module,
  `quality.py` — no DART calls, takes the `annual` three-year list `statements.annual()` already returned (post
  `to_eok`, since every quality ratio is scale-invariant). Formulas and sources are in the module docstring and
  README "재무 품질 지표"; no labels or verdicts, values and formula components only (2026-11-04 decision).
  F-Score needs two consecutive years, so the oldest of the three gets `incomplete: true`. A classified balance
  sheet (유동/비유동) is not required for banks/insurers/securities firms under K-IFRS, so `current_assets`/
  `current_liabilities`/`revenue` are already `None` from `statements.py` for them — `quality.py` never
  substitutes 0, it returns `null` for the affected metric and names the missing field in
  `altman_z_double_prime.missing`. `test_quality_unit.py` covers the pure functions with synthetic figures.
- `dart document-outline` / `document-section` / `financial-notes` parse the downloaded original XML with
  cluefin-dart-notes (see the `dart document-*` section) and are excluded from those tests too.
- `sec filing-items` / `filing-notes` / `filing-exhibit` / `note-series` parse downloaded documents with cluefin-sec-notes (see the `sec *`
  section); `test_sec_filing_handlers_unit.py` covers them with synthetic HTML.
- `kis chart trend-setup` also computes from paged series (stock via `ohlcv.fetch_kis_daily_series`, index via
  `cache.bars.fetch_index_bars` — 50 rows a call) plus `basic-info` for the benchmark; the rules live in `trend_setup.py`
  (see its section below). Excluded from the calls-once check like technical; `test_kis_trend_setup_handler_unit.py` covers it.
- `kis chart technical` computes from a paged series the same way. It pages
  `chart.period` itself (`ohlcv.fetch_kis_daily_series`), computes via `indicators.py`, and
  returns readings only — the candle series never reaches the caller, which is the whole
  reason it exists. `_handler_fakes.assert_calls_client_once` therefore does not describe
  it: `test_kis_basic_quote_handlers_unit.py` excludes it and `test_kis_technical_handler_unit.py`
  covers it instead. `test_handler_client_contract_unit.py` swallows `CliError` for the same
  reason — its probe returns `None` for every output field, which this handler correctly
  treats as an empty response.
- **`adj_price` polarity is inverted between the two KIS chart endpoints** —
  `chart.daily` is `0:unadjusted, 1:adjusted`, `chart.period` is `0:adjusted, 1:original`.
  Always go through `ohlcv.adj_price_flag(endpoint, adjusted=...)`; a raw "0"/"1" silently
  mixes price bases. Since 2026-11-04 both handlers also echo `adjusted: bool` at the top of
  their response (via `ohlcv.is_adjusted(endpoint, flag)`, the inverse lookup) so the agent
  doesn't have to remember the polarity; the input `adj_price` parameter is unchanged.
  `is_adjusted` raises on a literal that isn't either polarity value for that endpoint — it
  does not guess.
- **`ohlcv` parses missing values to NaN, never 0.0** (unlike desk's `_safe_float`), and
  takes the magnitude of every Kiwoom price — Kiwoom signs some responses (`cur_prc` is
  `"-270406"` on down days) and prices cannot be negative, so this is correct either way
  and needs no live call to settle.
- Minute bars are not daily bars with a finer stamp: KIS minute responses have **no**
  `stck_clpr` and no per-bar `acml_vol` (that field is the running day total on `output1`).
  `from_kis_minute` reads `stck_prpr`/`cntg_vol`.
- **Signals are reported as two families, never one score.** `macd`/`ma_stack` are
  trend-following and `rsi`/`bbands`/`stoch` are mean-reverting; averaging all five
  cancels out precisely when the reading is strongest (a sustained rise and a sustained
  collapse both score 0.0). Do not collapse them back into a single BUY/SELL.
- Signal aggregation stays in the CLI on purpose. `cluefin-ta`'s contract is ta-lib
  parity, and a BUY/SELL score has no ta-lib counterpart to be parity-tested against —
  moving it there breaks that package's only invariant. Only new *indicators* belong in
  `cluefin-ta`.
- Numbers will **not** match `cluefin-desk`: desk's pandas `ewm(span=N)` has no warm-up
  gap, while `cluefin-ta` follows ta-lib's SMA-seeded EMA with `N-1` leading NaNs.
  `cluefin-ta` is the reference here.

## `trend-setup` 은 백테스트 정의를 옮긴 것이다 (`trend_setup.py`)

- 규칙과 근거는 README "trend-setup 규칙과 근거". 공식은 cluefin-factory(아카이브) `scripts/watchlist/*.mjs` `a5cfbcf` 의 이식이고
  임계값은 그 공식에만 의미가 있다 — ta-lib 정의(Wilder ATR, SMA 시드)로 "고치면" 근거가 사라진다. 그래서 이 모듈은 cluefin-ta 를
  import 하지 않는다. 골든 픽스처(`tests/fixtures/trend_setup/stock-*.json`)의 `expected` 는 백테스트 파이썬 산출값이다 — 테스트가
  깨지면 코드를 고치지 기대값을 고치지 않는다. 파일 이름은 종목코드 대신 중립 이름이다.
- 판정은 마지막 **260봉**으로 한다(두 명령 같음). 프랙탈 피봇은 창 안에서만 찾으므로 봉 수를 바꾸면 드물게 피봇이 달라진다.
  이력(`history`)은 그 전 60봉을 더 쓴다(kis 는 320봉, 지수 500일).
- 장중 캔들: `end_date` 없이 15:40(KST) 전에 부르면 오늘 캔들을 버리고 `dropped_intraday_candle` 에 적는다. `include_today` 로 유지하면
  caveat. 시각은 `handlers/kis/domestic_basic_quote._now()` 로 주입한다(테스트).
- 지수는 코스피 `0001`·코스닥 `1001`(KOSPI200 아님). `benchmark=auto` 는 basic-info `mket_id_cd`(STK/KSQ), 그 밖은 exit 2.
  지수에 종목 마지막 날짜가 없으면 가까운 날로 메우지 않고 exit 4 `IndexDateMismatch`.
- 판정은 상태를 저장하지 않는다. 이전 상태는 `history` 가 지난 봉으로 다시 계산한 값이다(`_judge` 를 날마다 다시 부름).
  성과와 엮는 필터·문구는 표본 외 검증을 통과한 것만 낸다(README §9) — 2026-10 검증에서 `fresh_g3`(3그룹 2~3일)만 통과,
  1그룹 이력은 실패라 필터가 없다. 새 이력 필터를 더하려면 `docs/plans/watchlist-rules-backtest/validate_history.py` 로 먼저 검증한다.

## `cache *` 는 로컬 DuckDB 파일이다 (`cache/`)

- 메타 명령이다(`main.META_COMMANDS`, registry 밖). `cache load` 만 broker 를 부르고 나머지는 파일만 읽는다.
  `test_cli_contract_unit.py` 는 문서의 `cache` 줄을 실행하지 않고 하위 명령 이름만 확인한다 — `load` 는 실호출이고 읽기는
  로컬 파일에 따라 결과가 달라서다. `--dry-run` 은 없다.
- **쓰는 프로세스는 하나, 쓰는 동안 읽기도 막힌다**(DuckDB). 읽기는 `read_only=True` 로 열고 잠금은 `CacheLocked`.
  `cache load` 는 병렬 호출을 하지 않는다 — 사용자 결정(2026-10-18), KIS 는 동시 2개 제한도 있다.
- **KIS 초당 한도는 HTTP 500 `EGW00201`** 이고 클라이언트 기본 20 req/s 에서도 ~10% 가 걸린다. 클라이언트 재시도(1초부터)로는
  실효 ~5 req/s 라 `Sources` 가 KIS 클라이언트를 `max_retries=0` 으로 바꾸고 `throttle.kis_call` 이 0.1초 쉬고 다시 부른다
  (실효 ~15 req/s). 같은 곳에서 `EGW00300`(게이트웨이)·`EGW00316`(재조회 요청)·`OPSQ1002`(SESSION FULL, HTTP 200
  rt_cd 9)는 1초씩 5회 — 7만 회 적재에서 각각 몇 건씩 나왔다.
- **유니버스는 키움 ka10099 의 `거래소`·`코스닥` 종류만**(ETF·ETN·리츠 제외). 목록에서 사라진 코드는 지우지 않고 basic-info
  `lstg_abol_dt` 로 `delisted_on` 을 채운다. 2016년 이후 폐지 주식은 DART `stock_code` 차집합에서 보충하되 basic-info 의
  `mket_id_cd`(STK/KSQ)·`scty_grp_id_cd`(ST/FS/DR)로 거른다 — 차집합에는 코넥스(상장일이 **코스닥** 필드에 있다)·리츠·선박투자가
  섞인다. 확인한 코드는 `probe_log` 에 남겨 다시 부르지 않는다. 우선주는 DART 에 없어 끝자리를 0 으로 바꾼 보통주의
  `corp_code`, KIS `setl_mmdd` 는 `'12'`·`'1231'` 두 형식이고 빈 종목은 DART 기업개황 `acc_mt`.
- **`listed_on` 으로 일봉 시작을 자르지 않는다.** 코스닥→코스피 이전 종목은 basic-info 에 코스피 상장일만 남는다(035720:
  2017-07-10) 그런데 KIS 일봉은 그 코드로 이전 시절까지 준다. 일봉은 항상 `--since` 부터다.
- **일봉은 원주가**(`chart.period` 의 `"1"`). 과거가 안 바뀌므로 덧붙이기만 하고, 매 실행 최근 60일 종가를 다시 받아 비교한다.
  마지막 저장일 종가만 다르면 그 행만 덮어쓰고(`patched`, `adj_log.checked_through` 를 그 전날로 되돌린다), 그보다 앞선 날이
  다르면 그 종목만 전 구간 교체(`replaced`, `adj_log` 도 지워 수정계수를 다시 계산). 마지막 날은 적재 뒤 KIS 값이 바뀔 수 있다 —
  2026-11-04 증분 적재에서 대부분 종목의 10-23 종가(가끔 고가)만 달라 전 구간 교체로 70분이 걸렸다.
  KIS 는 10년 구간을 줘도 **최근 100행**(지수 50행)을 주므로 매번 남은 구간 전체를 요청하고 가장 오래된 행 전날로 줄여
  가다 빈 응답에서 멈춘다 — 거래정지 공백·상장 전 기간에 호출을 쓰지 않는다.
  `bar_log.fetched_from` 이 종목별 시작이고, `--since` 가 앞당겨지면 앞부분만 받아 채운다. 거래정지일은 시가=종가=전일 종가·
  거래량 0 으로 온다. 0 가격은 NULL. 16시(KST) 전에는 전 거래일까지만 받는다.
- **`adj_factor` = KIS 수정종가 ÷ 원주가 종가(날짜별)**. 분할일의 `prtt_rate` 는 0 으로 와서(2018-05 삼성전자) 기업행위를
  원주가 응답만으로는 알 수 없다. 첫 구간 수정주가가 원주가와 모두 같으면 계수 1(호출 1회), 다르면 전 구간. 증분은 최근 60일을
  받아 `close × adj_factor` 와 0.5원 넘게 다르면 새 기업행위로 보고 전 구간 재계산. 2016~ 3,187종목 중 1,662종목이 기업행위
  있음(배당락일 변화도 있다 — KIS 수정주가 정의 그대로). KIS 가 수정주가를 원 단위로 반올림해 저가주의 계수는 날마다 조금씩
  흔들린다 — 그래야 KIS 값과 정확히 같다(2026-10-18 표본 20종목 원주가·수정주가 전 날짜 일치).
- **`rates` 는 ECOS 시장금리(817Y002) 4계열 + 원/달러(731Y001) `usdkrw`**, 계열당 호출 1번(실키는 행 상한이 없다 —
  cluefin-openapi AGENTS). 매번 저장된 마지막 날 7일 전부터 다시 받아 덮어쓴다. `sample` 키(ECOS_AUTH_KEY 없음)는 쪽당 10행이라
  10년이면 계열당 ~250회 — 받지 않고 오류 한 줄로 건너뛴다. ECOS 는 하루 늦게 올라온다(2026-10-25 적재 시 마지막 10-23).
  `usdkrw` 는 다른 네 계열과 달리 연 %가 아니라 환율 수준값이다 — 적재 목록은 `ECOS_SERIES`, `--risk-free` 가 받는
  `RATE_SERIES` 에는 넣지 않는다.
- **`cache macro-beta` 는 `cache/macro_beta.py`**, 쓰기 없음(`rates`·`ohlcv` 만 읽는다). 종목·KOSPI(`U0001`)·`usdkrw`·
  `ktb3y`·`ktb10y` 각각 ISO 주(월요일 기준 `date_trunc('week', ...)`) 마지막 관측치만 남기고, 종목·KOSPI 는 전주 대비 변화율,
  금리 둘은 %p 차이 × 100(bp)로 바꾼 뒤 다섯 계열 모두 값이 있는 주의 교집합에서만 절편 포함 OLS 한 번(`numpy.linalg.lstsq`,
  `(X'X)^-1` 로 표준오차)을 돌린다. 30주(`_MIN_WEEKS`, 5개 계수 + 여유) 미만이면 `regression` 이 `null`이고 `hint` 가 이유를
  적는다(캐시 부족 또는 `cache load --only rates` 필요). 계열이 공선(금리가 구간 내내 그대로 등)이면 계수를 식별할 수 없어
  `beta`·`t` 가 모두 `null` 이고 `hint` 가 붙는다. t값·R² 는 전체 구간 적합도이지 예측이 아니다.
- `cache perf` 의 수익률은 **수정종가**다(`read_ohlcv(adjusted=True)` 와 같은 계수, 0·NULL 계수는 1). 원주가로는 분할일이
  -98% 손실로 보인다. 벤치마크와 날짜를 inner join 하므로 한쪽에 없는 날은 빠진다. 지표 정의는 `cluefin-ta` 가 갖고 여기서
  다시 계산하지 않는다 — NaN(변동 없음 등)은 `null`. `--risk-free <계열>` 은 `rates` 를 ASOF join 해 기간 첫날 이전의 마지막 발표값을
  쓰고, 10일 넘게 묵은 값(적재가 멈춘 캐시)은 exit 2 `RatesMissing` 이다.
- **`cache trend-setup` 에 규칙을 두지 않는다.** 종목마다 `trend_setup.analyze` 를 부르고(`kis chart trend-setup` 과 같은 함수),
  `test_cache_trend_unit.py` 가 두 결과가 같은지 본다. 유니버스는 백테스트와 같다: 그날 상장(`read_company(as_of)`), 끝자리 0, 이름에
  "스팩" 없음, 0 가격 봉 제외. 2026-10-16 전 종목 2,487개가 research `scan.py` 와 action·status·피봇·rel 모두 같았다.
  `--market`·`--code` 로 행을 좁혀도 전 종목을 판정한다(테마 주도주 순위가 전 종목 기준이라서). `--history true` 는 보이는 행만.
- **`theme` 은 키움 테마 스냅샷**이다. 키움은 현재 값만 주고 KIS 에는 국내 테마 API 가 없어 날마다 쌓는다. 평일 16시 전은 장중이라
  건너뛰고, 이름 붙일 날짜는 KIS 지수 일봉의 마지막 거래일이다(휴장일 이름으로 쌓지 않게). 2026-10-25 실측 142테마·897구성종목,
  ka90002 연속조회가 필요한 테마는 없었다(2026-11-08 최대 21종목). 연속조회 헤더는 `cont-yn` 만 먹는다 — 문서의 `cond-yn` 은 무시된다. **키움 기간수익률(`dt_prft_rt`)은 원주가 기준이고 테마 값은 구성종목
  단순 평균**이라 감자 종목 하나(+905%)가 테마를 1위로 만든다 — 관심 테마는 캐시 수정주가 중앙값으로 계산한다. `main_stk` 는 종목명
  쉼표 목록이라 같은 테마 구성종목 이름과 맞춘다.
- PIT 한계: `company` 의 이름·업종·상장주식수는 현재 값이다. DART 등록 전에 폐지된 종목은 빠질 수 있다.
- **`cache base-rate`/`base-rate-build` 는 기저율(outside view)이다**(`cache/baserate.py`). 칸은 trend-setup 그룹(g1/g2/g3/none,
  `trend_setup.analyze`의 action/status 를 `_STATUS_TO_STATE` 로 되짚은 것 — 규칙을 다시 derive 하지 않는다. illiquid 는 버린다)
  × 그날 횡단면 시총 3분위다. PBR 축은 B-1b(과거 재무) 전까지 없다. 시총은 그날 원주가 × **현재** `company.list_count` 근사다(캐시에
  과거 상장주식수가 없다). `base-rate-build` 만 쓰고(거래일 5일 간격 표본, `setup_state`), 증분(표의 현재 max `sample_date` 이후만
  계산)·멱등(`ON CONFLICT DO NOTHING`)이다 — 전 종목 하루치 판정이 `cache trend-setup` 과 같은 비용(~0.5~1초)이라 매번 전부 다시
  돌리지 않는다. `base-rate` 쿼리는 그 표만 읽는다: 대상 종목 하나의 오늘 판정(`analyze` 1회)과 오늘 유니버스의 시총 3분위(유동성
  필터 전, 과거 칸보다 약간 넓은 모집단 — 속도 때문에 의도적인 근사, `notes` 에 적는다)만 새로 계산한다. 칸 표본이 30개 미만이면
  그룹×시총 → 그룹 → 전체로 올려 합치고(`_resolve_cell`), horizon 별 초과수익(수정종가, `cache perf` 와 같은 관례)은 forward
  거래일 매핑 후 계산하므로 칸 표본 수와 horizon 별 n 이 다를 수 있다(최근 표본은 긴 horizon 의 미래 데이터가 아직 없다).
  `--target-pct`/`--stop-pct` 선도달률의 동일 날 양쪽 도달은 손절로 센다.
- **`cache rs`/`cache breadth` 는 쓰기가 없다**(`cache/breadth.py`, 새 표 없음 — `ohlcv`/`company`만 읽는다). 유니버스는
  `cache trend-setup`과 같은 `cache.trend._universe`(그날 상장 보통주, 스팩 제외, KOSPI/KOSDAQ). 가격은 trend.py 와 같이
  **수정주가**(`close * adj_factor`)다 — `cache ohlcv` 기본값(원주가)과 다르다.
  - **RS(1M)** = 21거래일 수정주가 수익률의 횡단면 백분위(0~99, 평균순위로 동점 처리) — memory
    `stockeasy-metric-definitions`(2026-10-07, 46종목 역산, 상관 0.998) 그대로다. 같은 memory 가 적은 IBD식 분기 가중 장기
    RS 는 "정확한 공식 미확인"이라 내지 않는다 — RS(1M) 하나뿐이다. SQL 한 번(`_RETURN_SQL`)으로 전 종목의 `rn=1`(당일)·
    `rn=22`(21거래일 전) 종가만 뽑는다(duckdb `row_number` 창함수) — `cache trend-setup`처럼 종목마다 `analyze` 를 돌리지
    않아 빠르다(전 종목 1초 미만).
  - **업종 RS** = 그룹(기본 `company.sector`, 26개 — `--by industry` 로 `industry`, 155개) 중앙값 21거래일 수익률을 그룹
    간에 같은 백분위 함수로 다시 매긴 값. 표본 3종목(`_MIN_SECTOR_STOCKS`) 미만 그룹은 통째로 드롭(`null`) — 그 종목
    자신의 RS(1M)은 영향받지 않는다.
  - `scipy.stats.rankdata`를 쓰지 않는다(이 패키지는 scipy 의존성이 없다) — `_percentile_rank` 가 평균순위 타이 처리를 numpy
    `argsort`+누적합으로 직접 구현한다.
  - **시장 폭**(`breadth()`): 52주 신고가·신저가는 당일 제외 직전 250거래일 수정 고가·저가 범위를 당일 고가·저가가
    갱신했는지(memory 의 52주 고점갭 정의와 같은 창, `>=`/`<=`로 동률도 신고가·신저가로 센다). 50일선 비율은 50일 데이터가
    다 찬 종목만 분모로 쓴다(상장 50일 미만 종목은 분자·분모 모두 제외). 상승·하락·보합은 전일 대비 수정종가.
  - **distribution day**·**follow-through day**는 지수(U0001·U1001·U2001) 각각에 대해 IBD(윌리엄 오닐) 방법론의 근사다 —
    IBD 는 두 개념을 정확한 공식으로 공개하지 않아 문턱값·창 크기는 통용되는 값을 썼고, 근거는 `cache/breadth.py` 모듈
    docstring 에 코드와 함께 둔다(여기서 또 적지 않는다 — 바뀌면 두 곳을 같이 고친다). distribution day 는 최근 25거래일
    롤링, "5% 반등으로 지워지는" IBD 의 비공식 규칙은 적용하지 않는다(그래서 급반등 뒤 수치가 재량적 카운트보다 약간 높을
    수 있다). follow-through day 는 최근 60거래일(`_DAY1_SEARCH_DAYS`) 안에서 "직전 50거래일 최저 종가 다음 상승일"을
    1일차로 잡고 4~10일차(IBD 원래 규칙은 4~7일, 이후 확장)에 1.25%(2015년 이전 1%) 이상 상승 + 전일 대비 거래량 증가를
    찾는다 — 매수·매도 신호가 아니라 날짜·등락률·거래량 비교 사실만 낸다.
- **`cache load --only financials`/`cache financials` 는 DART `fnlttMultiAcnt`(다중회사 주요계정)다**(`cache/financials.py`,
  결정 2026-11-04 `docs/plans/today-bundles-plan.md` B-1b). 한 번에 최대 100개 `corp_code`(콤마로 묶어 한 파라미터), 101개면
  상태 021(`COMPANY_LIMIT_EXCEEDED`) — JSON 경로라 예외 없이 빈 `list` 로 온다(020 처리와 같은 모양). `BATCH_SIZE=100` 이
  이미 한도 안이라 021 은 정상 경로에서 거의 안 뜬다. 연간(`reprt_code` 11011)만 쓰고, 사업연도는 `default_years`(오늘
  기준 최근 5개, 당해 연도는 아직 사업보고서가 안 나왔을 수 있어 제외)다. 이 엔드포인트가 주는 계정은 고정된 표준
  12개뿐이다 — 유동자산·비유동자산·자산총계·유동부채·비유동부채·부채총계·자본금·이익잉여금(결손금)·자본총계·매출액·
  영업이익·당기순이익(`ACCOUNT_NAMES`). **지배/비지배 구분이 없고 현금흐름표 항목도 없다** — 둘 다 필요하면 종목별
  `financial-full-statements`(`kis stock valuation-band` 가 하는 방식)를 직접 부른다. 연결(CFS)이 있으면 그걸, 없으면
  별도(OFS)만 쓴다(`_best_rows`, 한 회사가 둘 다 내면 CFS 우선) — 행의 `basis` 에 어느 쪽인지 남는다. 금액은 DART 가
  주는 그대로 **원**이다(`statements.won` 재사용) — `financial-summary` 의 억원과 다르다. `financials_fetch_log`(code,
  year)가 이미 물어본 쌍을 기억해 재실행은 새 종목(`company.corp_code IS NOT NULL`)·새 연도·그리고 `error` 로 남은 쌍만
  부른다(`ok`/`empty` 는 다시 안 묻는다). 그 배치 응답에 없던 회사는 "그 해 공시 없음"으로 보고 `status='empty'` 로 남긴다.
  일일 한도(상태 020)에 걸리면 즉시 멈추고(`quota_exhausted`) 남은 연도·배치를 건너뛴다 — 계속 불러 봐야 전부 같은
  이유로 실패한다.
- **한 종목 오류로 배치 100개를 통째로 버리지 않는다**(`_fetch`/`_narrow`, 2026-11-04 전종목 적재 실측: 192배치 중 31개가
  통째로 실패). 두 원인이 있었다: ① **중복 `corp_code` 가 섞인 배치는 JSON 대신 HTML 에러 페이지로 302 리다이렉트된다**
  (`JSONDecodeError`) — 우선주와 보통주가 같은 100개 배치에 들어가면 `company.corp_code_for` 가 둘 다 보통주의
  `corp_code` 로 돌려줘 중복이 생긴다. `_fetch` 가 호출 직전 `corp_code` 리스트를 중복 제거해서 막는다(배치 자체도
  `_process_batch` 에서 `codes_by_corp` 딕셔너리 키로 모아 호출하므로 이중으로 막힘). ② 그래도 한 회사의 응답이 pydantic
  검증을 못 넘기거나(모델이 필수로 선언한 필드가 그 회사만 빠짐) 호출 자체가 실패하면, `_narrow` 가 배치를 반으로 계속
  쪼개 문제의 `corp_code` 하나(또는 드물게 그 이하)까지 좁힌다 — 020(일일 한도)만은 쪼개지 않고 바로 멈춘다(어차피 전부
  같은 이유로 실패해 호출만 낭비). 끝까지 좁혀도 실패하는 (code, year) 는 `financials_fetch_log` 에 `status='error'` 로
  남고(다음 실행에 재시도 대상, `ok`/`empty` 와 달리 스킵 안 함) `cache load` 결과의 `failed_codes`/`errors` 에 찍힌다 —
  그 회사만 빠지고 같은 배치의 나머지는 정상 적재된다.

- **`cache magic-formula` 는 Greenblatt 마법공식 횡단면 스크린이다**(`cache/magic.py`, 쓰기 없음, 결정 2026-11-04
  B-22). 유니버스는 `cache.trend._universe` 에서 금융·증권·보험·전기/가스(`company.sector`, Kiwoom 26개 그룹 중 넷)·
  관리종목(`is_admin`)·거래정지(`is_halted`)를 빼고, 남은 종목의 시총(그날 원주가 × 현재 `list_count`, `baserate.py`와
  같은 근사) 하위 20% 를 더 뺀다. 재무는 `cache financials`(`fnlttMultiAcnt`)의 종목별 최신 사업연도 1개년뿐이라
  **EV·투하자본이 둘 다 근사다** — 그 표에 현금·이자부채 구분이 없어 EV = 시총 + 부채총계(현금 미차감), 투하자본 =
  자산총계 − 유동부채(유동자산+비유동자산=자산총계인 대수적 항등식, 순운전자본+순고정자산의 근사)로 뗀다. 두 지표의
  순위는 `cache.breadth._percentile_rank` 를 그대로 불러 쓴 값(0~99, 평균순위 동점 처리)의 합이다 — Greenblatt 원래의
  오름차순 서수 합이 아니라 내림차순 백분위 합(높을수록 좋음, 0~198)이라고 모듈 docstring과 응답 `notes`에 적는다.
  EBIT(영업이익)·투하자본·EV 중 하나라도 0 이하면 정의가 안 돼 `excluded` 로 세고 뺀다. `--top`(기본 30)은 출력 행수만
  자르고 순위 모집단은 그대로다.

## `audit *` 는 Claude Code 트랜스크립트를 읽는다 (`audit/`)

- broker 도 캐시 쓰기도 없다. 판단 적중(수익률)은 보지 않는다 — 수집 누락·중복·실패 처리만 결정적으로 본다(결정 2026-11-05).
  받은 데이터를 리포트가 놓쳤는지는 `.claude/agents/agent-audit.md` 가 `audit trace` 를 읽고 판단한다.
- 규칙의 출처는 각 `.claude/agents/<name>.md` 끝의 ```` ```audit ```` 블록 하나다(`subjects`·`required`·`main`·`each`·
  `stop-on-exit3`·`report-has`(리포트에 있어야 할 문자열)·`report-lacks`(있으면 안 되는 정규식)). 코드에 명령 목록을 두지 않는다 — agent 데이터 절을 고치면 그 블록만 같이 고친다.
- 트랜스크립트 자리: `$CLAUDE_CONFIG_DIR/projects`(기본 `~/.claude/projects`)에서 저장소 경로의 slug(영숫자 외 `-`)로
  시작하는 폴더 전부(worktree 포함). 서브에이전트는 `<session>/subagents/agent-<id>.jsonl` + `.meta.json`(`agentType`).
  스트리밍 턴은 같은 `tool_use` 를 여러 행에 반복하므로 id 로 한 번만 센다. exit code 는 `tool_result.is_error` 와
  `Exit code N` 첫 줄에서 읽는다(성공은 0, 권한 거부 등은 null).
- 셸 파싱: `2>&1`·`> file` 은 토큰화 전에 지운다(안 지우면 `--json 2` 로 읽힌다). 인자에 `$` 가 있으면 루프·`$(...)` 로 보고
  중복 대신 `shell_expansion` 으로 센다. 탐색 명령(`search`·`schema`·`recipe` 등)은 중복으로 세지 않는다.
- 블록과 무관하게 늘 보는 것: 출력을 파일로 보낸 호출(`output_to_file` — 응답에 데이터가 없어 근거를 대조할 수 없다,
  `2>&1`·`>/dev/null` 은 제외), CLI 밖 경로(`off_cli_secret`: `.env` 읽기·키 변수, `off_cli_direct_api`: curl·
  `cluefin_openapi` 직접 import, `off_cli_order`: 그 안의 주문 흔적). CLI 명령은 전부 `side_effect: read` 라 주문·키 노출은
  CLI 밖에서만 생긴다. `duplicate` 의 `same_output: false` 는 같은 인자에 다른 응답(페이지·불안정)이다.
- 대상 종목: `subjects: prompt`/`report` 는 그 텍스트의 6자리 숫자 중 캐시 `company` 에 있는 코드만(캐시가 없으면 전부).
  `--session --code` 는 대화에 다른 작업이 섞여 있어 텍스트를 쓰지 않고 `each` 명령에 넘긴 코드만 본다. corp-code 로 부른
  명령은 출력 어디든 `stock_code`·`corp_code` 가 함께 있는 객체로 매핑한다.
- `agent_commit` 은 실행 시작 전 agent 파일의 마지막 커밋이다. `--follow` 는 `--before` 와 같이 쓰면 아무것도 못 찾아서
  옛 이름(`check.ALIASES`)을 경로로 나열한다. 검사는 **현재** 파일 기준이라 그 뒤에 추가된 명령은 누락으로 나온다(`notes`).

## `dart corp-code-lookup` 은 전체 색인을 받아 클라이언트에서 거른다

- DART 의 corpCode.xml 에는 검색 파라미터가 없다. 어떤 필터를 줘도 **매번 전체 색인
  (2026-09-17 실측 119,313행) 을 내려받아** 핸들러가 메모리에서 거른다. 필터는 호출량을
  줄이지 않으므로 반복 조회는 호출부에서 캐시할 일이다 (desk 의 `_get_corp_code` 가
  화면당 한 번으로 메모이즈하는 이유).
- 상한 파라미터가 `max_rows` 인 것은 `--limit` 이 전역 CLI 옵션이라 핸들러 params 까지
  전달되지 않기 때문이다. 기본 100행, `--max-rows 0` 이면 전량. 응답의
  `total`/`returned`/`truncated` 는 `list --full` 의 절단 규약과 같은 모양이다.
- `stock_code` 는 비상장사에서 공백 문자열로 채워져 오므로 비교 전에 `_clean()` 으로
  strip 한다. `listed_only` 도 "값이 있다"가 아니라 "strip 후 비어 있지 않다"로 판정한다.
- **`listed_only` 는 "현재 상장" 필터가 아니다.** DART 는 폐지 회사의 `stock_code` 를 지우지 않는다(2026-10-18 실측: 한진해운
  117930, 2017-03 폐지, `corp_cls` 만 null). 전종목 유니버스는 키움 ka10099 로 만든다(`docs/plans/ohlcv-cache-plan.md`).
  폐지 여부는 KIS `basic-info` 의 `scts_mket_lstg_abol_dt`/`kosdaq_mket_lstg_abol_dt`; `kis stock current-price` 는
  폐지 종목에서 필드가 빠진 몸체를 받으면 `basic-info` 를 한 번 더 불러 exit 4 `Delisted` 로 바꾼다.
- 불리언 파라미터는 값을 받아야 한다 — `--listed-only true`. 플래그처럼 값 없이 주면
  exit 2 (`Option --listed-only requires a value.`).

## `dart financial-*` 가 실적의 유일한 경로다

- DART 주요계정의 손익 행은 **분기 보고서에서 `thstrm_amount` 가 해당 분기 단독,
  `thstrm_add_amount` 가 연초 누적**이다 (1분기는 둘이 같은 값, 사업보고서와
  재무상태표 행은 누적이 `None`). 반기 실적을 전년과 비교할 때 `thstrm_amount` 를
  쓰면 성장률이 절반 가까이 틀어진다. `frmtrm_add_amount` 가 전년 동기 누적이다.
- 주요계정 응답에는 `fs_div` 파라미터가 없고 회사가 제출한 기준(연결·개별)이 그대로
  온다. 연결재무제표가 없는 회사는 OFS 행만 온다. 전체 재무제표만 `fs_div` 를 받는다.
- `financial-summary` 의 `as_of` 는 **접수일**(`rcept_no` 앞 8자리)로만 거른다. JSON API 가 최신 정정본 값만 주므로
  시점 필터를 통과한 보고서의 숫자도 정정 후 값일 수 있다 — 응답 `notes` 에 적혀 있고, 접수 당시 값은 `financial-as-filed`.
  연초(사업보고서 제출 전)에는 두 해 창에 사업보고서가 없어 전전년 사업보고서를 한 번 더 부른다(`calls` 9).
- `dart share-count` 의 수치는 `"5,969,782,550"` 같은 콤마 문자열이고 결측은 `"-"` 로 온다. 패스스루라
  변환하지 않는다. 각 행의 `rcept_no` 는 원본이 아닌 최신 정정 보고서다 (2026-09-30 실측:
  노드메이슨 2024 사업보고서 4행 모두 정정 `20250828000839`). 원본 시점 주식수는 이 API로 얻을 수 없다.
- 복수회사 조회는 일부러 뺐다 — 배열 입력이 "read 패스스루" 계약과 맞지 않는다. XBRL 원문 파일도
  여전히 내지 않는다(임시 디렉터리에 받아 파싱하고 지운다). 파싱된 행만 `financial-as-filed` 로 나간다.
- JSON API(`financial-major-accounts`·`financial-full-statements`)는 **최신 정정본 값만** 준다.
  노드메이슨(01328170) FY2024 연결 영업이익은 원본 20250318001317 이 28,915,427,
  정정 20250828000839 가 -190,143,795 인데 JSON 은 후자만 준다. 접수 당시 값은
  `financial-as-filed` (접수번호별 fnlttXbrl.xml) 로만 얻는다. 전기 열은 나중 보고서에서 재작성된
  값이므로 당기 열만 as-filed 다.
- 엉뚱한 `rcept_no` 는 오류 없이 **다른 회사의 유효한 ZIP** 을 돌려주고, `reprt_code` 는 서버가
  무시한다. 그래서 `corp_code` 가 필수이고 파싱된 `entity_id` 와 다르면 exit 4 다.
- Arelle 은 콜드 캐시(`~/Library/Caches/Arelle`)에서 택소노미를 네트워크로 받아 첫 파싱이 최대 ~76초
  걸린다. 오프라인+콜드면 택소노미를 못 읽어 cluefin-xbrl 이 `XbrlParseError` 를 내고 exit 4 가 된다
  (예전엔 예외 없이 facts 가 빈 문서가 왔다 — facts 0·기간 없음 검사는 안전망으로 남겨 둠). 단위 테스트는
  파서를 monkeypatch 해 네트워크를 타지 않는다.
- Arelle 은 `[info] loaded …` 를 **stdout** 에 찍는다. 파싱 호출을 `redirect_stdout(sys.stderr)` 로 감싸지 않으면
  JSON 출력이 깨진다 — 파서를 monkeypatch 하는 단위 테스트·핸들러를 직접 부르는 통합 테스트로는 안 보인다.
- 회사에 따라 IS 키가 없고 손익이 CIS 에만 있다(노드메이슨), 연결재무제표가 없는 회사도 있다(티씨머티리얼즈).
  IS 를 CIS 로 합성하지 않고, 요청했지만 없는 것은 응답 `missing`(`"IS/consolidated"` 형식)에 적는다.

## `dart document-*` · `dart financial-notes` 는 공시 원문을 받아 파싱한다

- `disclosure_document_files` 로 임시 디렉터리에 받고 cluefin-dart-notes 로 파싱한다(디스크에 남기지 않음).
  세 명령이 같은 `rcept_no` 를 각자 다시 받는다 — 캐시는 없다. 2026-10-12 실측: 대형주 반기보고서 6.8MB,
  다운로드+파싱 ~1초.
- `corp_code` 는 필수이고 **첨부 감사보고서까지 모든 파일**의 `AREGCIK` 가 같아야 한다(다르면 exit 4).
  2019·2025·2026 정기보고서와 감사보고서 단독 공시 모두 본문·감사보고서에 8자리 고유번호가 있었다.
- 2017년 이전 접수번호(앞 4자리)는 클라이언트를 만들기 전에 exit 2. 파서 지원 범위 밖이다.
- 핸들러는 `disclosure_document_files` 의 반환값이 아니라 **임시 디렉터리를 다시 훑는다**.
  `test_handler_client_contract_unit.py` 의 프로브가 경로 목록을 주지 않기 때문이고, XML 0개는 exit 4 다.
- `index` 는 파일 경계를 넘어 매긴다(본문 먼저, 나머지 파일 이름순 — `_xml_entries` 와 같은 순서).
  outline 의 `chars` 는 하위 섹션과 그 제목을 포함하고, `document-section --index` 의 `total_chars` 와 같다.
- `document-section` 의 선택자(`section`·`assoc_code`·`title`·`index`)는 정확히 하나여야 한다. 계약 테스트는
  모든 파라미터에 샘플을 채우므로 `_EXCLUSIVE_SELECTORS` 로 선택자 하나만 남긴다 — 선택자가 있는 명령을
  추가하면 거기에도 넣을 것. `assoc_code` glob 은 `*` 만 된다(`?` 는 문자열 검증이 막는다).
- `max_chars`(기본 20000)는 블록 경계에서 자르고 첫 블록은 넘어도 돌려준다. 실측 크기: 대형주 "II. 사업의
  내용" 36–61k자, 하위 섹션 ≤18k자, 주석 섹션 75–130k자, 가장 큰 노트 43k자, 노트 중앙값 ~1k자.
  JSON 은 글자 수의 ~1.5배.
- `financial-notes` 는 정기보고서가 있으면 그 주석만 읽는다. 정기보고서 ZIP 의 첨부 감사보고서 주석은 같은
  내용을 반복하고(2019 실측: 별도 주석의 글자 수가 같았다) 노트 제목 없이 연번 분할로만 나뉜다.
  감사보고서만 든 공시일 때만 감사보고서 주석(00760 별도, 00761 연결)을 쓴다.
- 분할 경고(`warnings`)는 모든 모드에서 출처별로 그대로 내보낸다. 구형 공시에서 흔하다(2019 대형주 별도
  주석: 4·18번 없음). 노트를 하나도 못 나누면 본문이 전부 preamble 이라 이 명령으로는 못 읽는다 —
  hint 가 `document-section --index` 로 보낸다.

## `dart major-event` · `dart report-item` 은 람다 표로 디스패치한다

- 주요사항보고서 36종·정기보고서 주요정보 26종을 명령 둘로 연다. 엔드포인트마다 명령을 두면 `disclosure` 태그가
  50개 상한(`test_taxonomy_filters_are_selective`)을 넘고, 인자가 종류별로 완전히 같다.
- **라이브러리 메서드·클래스 이름은 2026-11-04(B-13)부터 엔드포인트와 일치한다** — `default_occurrence` 는
  dfOcr(부도발생), `business_suspension` 은 bsnSp(영업정지), `exchangeable_bond_issuance_decision` 은
  exbdIsDecsn(교환사채). 클래스 이름도 `MajorMattersReport`(주요사항보고서, DS005)로 바뀌었다. 옛 이름(`real_estate_development`,
  `business_letter`, `corporate_bond_issuance_decision`, `MajorShareholderDisclosure` 등)은 `DeprecationWarning`
  을 내는 별칭으로만 남아 있으니 새로 쓰지 않는다. `handlers/dart.py` 의 `_MAJOR_EVENTS`·`_REPORT_ITEMS`
  (slug → 엔드포인트·한국어 이름·람다)가 그래도 진실의 원천이다. `getattr(client, 이름)` 으로 바꾸지 않는다 — 이름이 오해를
  부르고 Codacy 가 동적 호출로 잡는다. `test_dart_event_handlers_unit.py` 가 62종 전부 실제 client 의 `_get` 경로를 표와 대조한다.
- 실데이터 검증(2026-10-17, 최근 12개월 주요사항보고 공시에서 종류별 표본, CLI 경유): 주요사항 33종은 행으로 확인.
  `split-merger` 는 표본 4건이 모두 013(자회사 공시로 보임), `overseas-delisting-decision`·`overseas-delisting` 은 표본이 없어
  **미검증**. 표본은 `[기재정정]` 을 빼고 고른다 — 정정 공시의 접수일로 조회하면 013 이 온다. report-item 26종은 대형주·소형주
  각 1곳의 2025 사업보고서로 확인. 10년 범위(2016–2026) 조회도 된다.
  이 과정에서 라이브러리 모델 8종(유상·무상·유무상증자·감자·부도·영업정지·해산·자산양수도)의 숫자 필드와 감사의견 3필드를
  실서버에 맞춰 고쳤다(`packages/cluefin-openapi/VENDOR_DOC_ERRATA.md` DART 절).
- `major-event` 의 `bgn_de`·`end_de` 는 필수다. 기본값이 있으면 "없음(013)" 과 "기간이 틀림" 을 구분할 수 없다. 달력 날짜·
  순서·20150101 이후를 클라이언트 생성 전에 검사해 exit 2. 계약 테스트가 이 검사에 걸려 클라이언트 대조를 건너뛰지 않도록
  `metadata._NAME_SAMPLES` 에 `_de` 접미사 샘플(`20250101`)이 있다.
- 출력은 다른 DART 명령처럼 패스스루에 `event`/`item`·`endpoint` 두 키만 얹는다. 013 은 오류가 아니고, 020 은 `_checked` 가 exit 5 로 바꾼다.
- 최대주주 현황(hyslrSttus)·주식의 총수(stockTotqySttus)는 `report-item` 에 넣지 않았다 — `dart major-shareholder`·`share-count` 가 연다.

## `dart dilution-watch` 는 `major-event` 11종을 한 번에 모아 정규화한다 (`dilution.py`)

- 범위는 2026-11-04 결정(`docs/plans/bundle1-plan.md` B-11): CB·BW·EB·유상증자·무상증자·유무상증자·감자·자기주식
  취득/처분(신탁 체결·해지 포함). **자사주 소각**은 주요사항보고서가 아니라 정기보고서 `report-item treasury-stock`
  이라 범위 밖이고, 응답 `not_covered` 에 그 사실을 적는다 — 조용히 빠뜨리지 않는다.
  `dilution.DILUTION_KINDS` 가 그 11종의 슬러그 목록이고 `_MAJOR_EVENTS` 와 이름을 공유한다.
- 엔드포인트마다 필드 이름이 다른 것(위 절)을 `dilution.normalize_row(kind, row)` 가 공통 필드로 맞춘다:
  `rcept_dt`·`kind`·`corp_name`·`amount_won`·`conversion_price`·`refixing_floor`(CB/BW 만 있다 — 교환사채 모델에는
  리픽싱 필드 자체가 없다)·`new_shares`. `new_shares` 는 부호로 방향을 표현한다 — 유통주식이 느는 쪽(CB/BW/EB 전환,
  유상·무상·유무상증자, 자사주 처분)은 양수, 주는 쪽(감자, 자사주 취득)은 음수다. `normalize_row` 는 순수 함수라
  DART 호출이 없다 — 행은 호출부(`handle_dilution_watch`)가 넘긴다.
- **`pct_of_shares` 분모는 기간 끝(`end_de`)에 가장 가까운 사업보고서의 발행주식총수**(`dart share-count` 의
  `se=보통주` 행 `istc_totqy`, 기존 `_common_shares`·`kis stock valuation` 과 같은 관례 — 우선주 제외)다.
  `_latest_share_count` 가 `(end_de 연도, 전년) × (11011·11014·11012·11013)` 순으로 조회해 `end_de` 이전에
  접수된 첫 보고서에서 멈춘다 — `fetch_reports`(재무제표용)와 같은 창이지만 주식수는 보고서별 스냅샷이라 기준·연결
  구분이 없다. 모든 reprt_code 가 013 이면(신규 상장 등) `total_common_shares`·`report` 모두 `null`, 그 행들의
  `pct_of_shares` 도 `null` (`dilution.with_pct_of_shares` 는 분자·분모 중 하나라도 없으면 그대로 둔다).
- **`bgn_de`·`end_de` 를 생략하면 최근 3년**(`_default_bgn_de`, `end_de` 기준 -3년, 하한 20150101)이다. `major-event`
  자체는 그 둘이 필수지만(013 vs 기간 오류 구분), `dilution-watch` 는 한 번에 11번 부르는 명령이라 매번 날짜를
  쓰게 하지 않는다 — 범위는 응답 `bgn_de`/`end_de` 에 그대로 찍힌다.
- 호출 수(`calls`)는 11(종류별 1회씩) + share-count 시도 횟수(보통 1~2, 최악 8)다. 013 인 종류는 `rows` 에 보태지
  않고 `empty_kinds` 에 슬러그만 남는다 — `major-event` 와 같은 "013 은 오류 아님" 원칙.
- `handle_dilution_watch` 는 financial-summary 처럼 클라이언트를 여러 번 부르고 계산하므로
  `test_dart_handlers_unit.py` 의 "handler 가 client 를 한 번만 부르는지" 공용 검사에서 뺐다(`_PARSING_HANDLERS`).
  `test_dart_event_handlers_unit.py` 가 종류별 호출·정규화·pct 계산·기본 기간·013/020 처리를 덮는다.

## `sec *` 는 SEC EDGAR 를 읽는다 (미국 고객사·경쟁사 공시)

- `SEC_USER_AGENT`("이름 이메일")는 루트 `.env` 에 있어야 한다 — `.env.test` 에만 있으면 CLI 는 못 쓴다. 없거나 `@` 가
  없으면 exit 3 `CredentialsMissing`(클라이언트의 ValueError 문구로 분류). SEC 403 은 User-Agent 문제와 과속 차단
  (약 10분)을 구별할 수 없어 exit 3 + 그 둘을 말하는 hint, `*NotFoundError`(404)는 exit 4 `NotFound`.
- **SEC 폴더는 다른 회사 CIK 경로로도 200 을 준다**(2026-10-12 실측). 그래서 `filing-items`·`filing-notes`·`filing-exhibit` 은
  `archives.filing_detail()`(공시 상세 `-index.html`)의 `parties` 에 `cik` 가 없으면 다운로드 전에 exit 4. 주 문서는
  상세 페이지의 순번 1 문서라 `primary_document` 파라미터가 없고, exhibit 은 문서 종류(EX-99.1)로 고른다(파일명은
  공시마다 제각각). `-index-headers.html`(SGML)은 2015년 이전 공시에서 404 라 쓰지 않는다.
- 20-F·40-F·6-K 등 sec-notes 카탈로그에 없는 서식과 `.txt` 주 문서(2001년 이전)는 다운로드 전에 exit 2.
- 경고는 버리지 않는다. `extract_items` 결과를 그대로 싣고, `UNCERTAIN_CODES` 경고가 있으면 `uncertain: true`.
  `item()`(예외를 냄)은 쓰지 않는다 — 생략·누락·없는 Item 은 `status`(`omitted`/`missing`/`not_in_filing`/
  `not_in_catalog`)와 `text: null` 로 돌려준다.
- `max_chars` 기본 40000: 영문은 글자당 토큰이 적어 DART 20000 과 비슷한 토큰량이다. 2026-10-12 실측(대형 반도체·장비·
  은행 10-K, 10-Q, 8-K): 10-K 1A 68–118k자, 7 18–40k자(은행 393k), 1 16–62k자, 8 62–535k자, 10-Q I:2 34–38k자,
  II:1A 64–109k자, EX-99.1 2–30k자. 다운로드+파싱 0.3–1초(은행 10-K 13MB 2.7초). 자르는 곳은 빈 줄, 없으면 줄 끝
  (표는 한 행이 한 줄). `next_offset` 은 구분 줄바꿈을 건너뛴 위치. `offset_chars` 는 Item 하나일 때만.
- `include_tables` 는 반환 구간 안에서 **시작하는** 표만 `grid()` 로 준다. 오프셋은 `SecDocument.text` 처럼 빈 블록을
  빼고 빈 줄로 이은 위치로 센다(`_table_grids`) — sec-notes 의 텍스트 조립을 바꾸면 같이 바꿀 것.
- `filing-notes` 는 재무제표 Item(10-K 8, 10-Q I:1)을 `split_notes` 로 나눈다. 표는 `{unit, grid}` 로 주고 단위는
  곱하지 않는다(`dart financial-notes` 와 같은 계약). `notes` 의 숫자(또는 한 글자)는 주석 번호, 나머지는 제목 부분 일치다.
  주석 번호는 해마다 바뀐다(2026-11-04 실측: 같은 회사 Income Taxes 가 13번 → 7번 → 6번) — 여러 해는 `note-series`.
- `note-series` 는 최근 10-K(정정 제외) N편을 받아 `note_series.py` 로 잇는다. 해 잇기 규칙은 모듈 docstring 에 있고,
  여기는 고르게 된 이유만 적는다(2026-11-04 실측, 이커머스 1개사 10-K 5편):
  - 회계연도는 `dei:DocumentFiscalYearFocus` → 문서 기간말 → `report_date` 순. 같은 해가 두 편이면 최근 것만 쓰고
    `problems` 에 남긴다.
  - 값은 당해 열만. 머리에 연도가 없는 표는 값 열 전부를 당해로 본다(만기표·가정표). 당해 열이 없는 표(옛 서식이
    전년 값만 남은 경우)는 `skipped_tables`.
  - 표 짝은 행 이름 Jaccard 0.5 로는 행이 갈라진 표("Foreign" ↔ "Foreign - Korea"/"Foreign - Other")를 못 잇는다. 그래서
    표 전체 낱말 Jaccard 0.7 을 두 번째 기준으로 둔다. 한 표가 셋으로 갈라진 경우(세그먼트 표)는 하나만 이어진다.
  - 구역 머리("Current taxes")가 같은 이름의 행을 가른다. 구역 머리가 새로 붙어도("Differences resulting from:")
    구역을 뺀 이름이 표 안에 하나뿐이면 잇는다.
  - 대시는 0, 빈 칸은 값 없음.
  - `restated` 는 차이가 거친 단위의 한 단위 미만이면 달지 않는다. 반 단위로 두면 천 달러 → 백만 달러 반올림(28,513 →
    28, 합계를 맞추려 내림)이 재작성으로 잡혀 5편에서 오탐 5건이 났다. 남은 4건은 세율 조정표 "Other"·"Other
    nondeductible expense" 재분류였다. Net Revenues 구분은 재작성이 없었다(5,580 은 FY2024 당해 값, 2023 비교 열은 2,576 그대로).
  - `xbrl` 은 `notes` 를 줬을 때만 companyfacts 를 한 번 더 받는다(목록 모드는 안 받는다). 같은 실측에서 Net Revenues·
    Income Taxes·Leases 금액 행 97개 중 57개에 개념이 붙었다. 구분 행(Net retail sales 등)은 차원 값이라 companyfacts 에
    없어 붙지 않는다 — 그건 정상이다. companyfacts 404 는 `xbrl.error` 로 두고 명령은 성공한다.
- `company-lookup` 은 매번 전체 목록(~1만 행)을 받아 거른다. `filings` 는 SEC 의 recent 목록(1년 이상 또는 1,000건)만 본다.
- 테스트 픽스처는 합성 회사·CIK·접수번호만 쓴다(cluefin-sec-notes AGENTS.md). 스키마 예시의 `cik`/`accession_number`
  샘플은 cluefin-openapi README 와 같은 AAPL 값이다.
- 클라이언트 계약 테스트는 SEC 메서드가 모델을 그대로 돌려주므로 프로브 자체를 응답으로 준다(`bare=True`, 리스트를
  돌려주는 메서드는 `[]`). 핸들러는 모델 **필드**만 읽어야 한다 — `FilingDetail.ciks` 같은 property 를 읽으면 그 테스트가
  실패하므로 `parties` 를 읽는다.

## `ecos *` 는 한국은행 경제통계다

- `ECOS_AUTH_KEY` 는 선택이다. 없으면 클라이언트가 공개 `sample` 키로 쪽당 10행씩 받는다(`table-search` 는 전체 목록 ~840행이라
  ~85회). 키 오류(INFO-100)는 exit 3, 그 밖의 결과 코드는 클라이언트의 `hint` 를 그대로 싣는다(`errors._classify_ecos`).
  ERROR-400(60초 초과)은 이름이 `*TimeoutError` 지만 같은 범위를 다시 보내도 같으니 `QueryTooLarge`, retryable false.
- `series` 의 기간 형식은 주기를 따른다(`handlers/ecos.py` `_PERIOD_PATTERNS`). 클라이언트를 만들기 전에 exit 2 로 걸러 ERROR-101
  왕복을 줄인다. 파라미터가 `start_date`/`end_date` 인 것은 계약 테스트 샘플(`date` → `20250101`)이 주기 D 에 맞아서다 — 주기
  enum 의 첫 값도 그래서 `D` 다. `stat_code` 샘플은 `metadata._NAME_SAMPLES` 의 `817Y002`.
- ECOS 서비스는 `EcosPage` 를 바로 돌려준다 — 계약 테스트는 SEC 처럼 `bare=True` 프로브를 쓰고, 핸들러는 `page.rows or []` 로
  읽는다(프로브의 필드는 None). 행의 `value` property 는 프로브가 모델 필드가 아니라고 막으므로 `to_number(row.data_value)` 를 쓴다.
- `DATA_VALUE` 는 문자열이고 빈 값(휴일·미집계)이 있다. 숫자로 바꾸되 빈 값은 `null`, 0 으로 채우지 않는다.
- `key-stats` 는 서버 행 순서가 호출마다 달라 `(class_name, name)` 으로 정렬해 낸다.
- `macro-snapshot` 은 계산 명령이다(`macro.py`). 계열 표 `SERIES` 의 코드는 2026-11-01 실서버로 확인했고, 통합 테스트
  (`test_ecos_integration.py`)가 계열마다 값이 오는지 본다. 항목 그룹이 둘인 표(BSI 512Y014, CCSI 511Y002)는 두 코드를 다 준다 —
  하나만 주면 성별·연령별 행이 같은 시점에 섞여 온다. 한 시점에 행이 둘 이상이면 평균내지 않고 `missing` 에 적는다.
  - 국면 라벨을 넣지 않는 것은 사용자 결정(2026-11-01)이다. trend-setup 처럼 표본 외 검증을 통과한 규칙만 낸다.
  - 기준일을 맞추지 않는다. 계열마다 `as_of` 가 다르고(월·분기 발표 지연), 파생 스프레드는 두 계열에 모두 있는 날만 뺀다.
  - 백분위는 창 안 관측치 중 최근값 이하의 비율이다. 값은 오늘 받은 개정 후 값이라 과거 시점 재현(eval)에는 그대로 못 쓴다.
  - sample 키면 클라이언트를 부르기 전에 exit 3. 계열 하나의 실패(`EcosAPIError`)는 `missing` 에 적고 계속하지만, 키 오류와 레이트
    리밋은 그대로 올린다(exit 3·5). 계약 테스트의 프록시는 `is_sample` 이 bool 이 아니어서 `is True` 로 비교한다.
- `industry-outlook` 도 계산 명령이다(`industry.py`, `macro.py` 의 `MacroSeries`·`summarize`·`year_over_year`·`align`·`fetch_window` 를
  재사용). 제조업 중분류 24개(KSIC C10~C33) 표가 진실의 원천이고, 2026-11-03 실서버로 확인했다 — `901Y032`(생산·출하·재고)는
  Group1 이 업종(`I11ACx`)·Group2 가 지표(1~6)로 `macro-snapshot` 의 BSI 표(Group1 지표·Group2 업종)와 그룹 순서가 반대고,
  `I11ACx` 글자가 `I11ACR`(27) 다음부터는 KSIC 순서를 따르지 않는다(`I11ACV`=31 이 `I11ACS/T/U`=28/29/30 보다 먼저 온다) — 글자
  순서를 가정하지 않고 이름으로 맞췄다. 품목코드(수출물가 402Y014·생산자물가 404Y014·수출금액지수 403Y001)가 없는 업종(인쇄 18,
  조선 등 기타운송장비 31 의 수출 쪽)은 비슷한 품목으로 대신 채우지 않고 `missing` 에 적는다. 재고순환은 부호(`shipments_up`/
  `inventory_up`)와 차이값만 내고 국면 이름(회복/확장/하강/수축)은 주지 않는다(macro-snapshot 과 같은 결정). `induty_code` 는
  DART 기업개황 값 그대로 받고 앞 두 자리만 쓴다 — 제조업이 아니면(10~33 밖) exit 2. 담배(12)·기타 제품(33)은 BSI 업종코드
  `C3300`("기타제품, 담배")를 공유한다 — 두 업종 모두 `industry.bsi_shared_with` 에 서로를 적어 이 BSI 가 담배만의 값이
  아님을 agent 가 바로 안다.
- **ECOS 레이트리밋은 3분 300회**(`ERROR-602`, 2026-11-03 실측: 24개 업종 전수 조회 중 ~190여 회 만에 걸림)고 30분 뒤 풀린다
  (실측). `macro-snapshot`(~15회) 하나, `industry-outlook`(~8회) 하나는 문제없지만, 여러 업종·여러 종목에 `industry-outlook`
  을 반복 호출하거나(`test_ecos_integration.py` 의 `slow` 전수 테스트가 그 경우) 다른 ECOS 호출과 짧은 시간에 합쳐지면
  걸릴 수 있다. 걸리면 `EcosRateLimitError`(exit 5, retryable) 로 그대로 올라오고 — 재시도 전 30분을 기다린다.

## Tests that break on unrelated-looking changes

- `test_rpc_registry_unit.py` hardcodes the total command count — bump it when adding or
  removing any handler. It is the only place; `test_agent_surface_unit.py` reads the registry length.
- A domain/tag used in `COMMAND_TAXONOMY` must also exist in `_DOMAIN_TAXONOMY`/
  `_TAG_TAXONOMY` or the taxonomy-coverage test fails.
- `test_taxonomy_filters_are_selective` puts a floor under filter precision (≥110 distinct
  `(domains, tags)` signatures, no tag on more than 50 commands). Retagging that collapses
  commands back into one bucket fails it.
- Recipe → command references are validated only by a test, not at runtime; renaming a
  command path silently breaks recipes until tests run.
- `test_readme_smoke_unit.py` does literal substring assertions against `README.md` and
  this file's agent section — keep the example/taxonomy strings in sync with `metadata.py` text.
  `test_cli_contract_unit.py` also runs every `uv run cluefin-openapi-cli` line inside a code block of
  both files (offline, or `--dry-run`), so an example here must be a valid command.
- `list` is **brief** by default (`_command_brief`); `--full` restores the old
  per-command `parameters`. Tests and agents that need parameters must use `--full` or
  `schema`. An **unfiltered** `list --full` is capped at 25 rows (`_UNFILTERED_FULL_LIMIT`)
  and reports `count`/`returned`/`truncated`; `--limit 0` restores every row. It truncates
  rather than refuses because README/AGENTS assertions require it to exit 0.
- `test_readme_smoke_unit.py` also pins the `command_count` printed in the README's taxonomy
  example against the live `domains --json`, so retagging commands can fail it.

## search is a ranker, `list --query` is a filter

- These are deliberately separate primitives. `test_agent_surface_unit.py` asserts that
  `list --full --query "theme group"` returns **only** matching names — redirecting
  `--query` into the scorer breaks that by construction.
- The corpus is 100% English, so Hangul never enters the index. Korean reaches it only
  through `metadata.QUERY_ALIASES` expansion, and alias values are run through the same
  `tokenize()` as documents — a raw plural like `securities` would otherwise never match
  the indexed stem `securitie`. `test_search_unit.py` fails on any alias expansion that
  reaches nothing.
- The BM25F index is cached on the **registry object identity**; `set_registry_provider`
  swaps registries between tests and an unkeyed cache would serve a stale index.
- `tests/test_cli_contract_unit.py` has a `META` set — a new meta command must be added there
  or its documented examples get re-run as network commands and silently stop being
  verified offline.
