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
- **최신 실적은 DART, 주당지표만 KIS.** `kis financial *` 은 소형주에서 연간 행만 오고 최신 공시보다 한 해 늦을
  수 있다. 리포트용 숫자(최근 8분기 단독값·YoY, 3개년 손익·재무상태·현금흐름·비율, 최신 누적, TTM, 차입금)는
  **`dart financial-summary --corp-code <8자리>` 한 번**으로 받고 다시 계산하지 않는다(DART 8회, 억원). 한 보고서만
  볼 때는 `dart financial-major-accounts`(`recipe latest-earnings`), 비율·성장률의 공식 값은
  `dart financial-major-indicators`, EPS·BPS 만 KIS 다. 분기 보고서의 `thstrm_amount` 는 해당 분기 단독,
  `thstrm_add_amount` 는 연초 누적이다. 정정 전 원본 값은 `dart financial-as-filed` 뿐이다.
- **숫자가 말해 주지 않는 것은 원문에 있다.** 부문별 매출·수주·차입금 만기·우발부채는 `recipe filing-text`
  (정기보고서·감사보고서만 읽힌다), 주요사항보고서의 금액·상대방은 `dart major-event`, 배당·자사주·임원 등
  정기보고서 항목은 `dart report-item`. 미국 고객사·경쟁사 공시는 `recipe us-peer-filings`(20-F/6-K 제출사는
  못 읽는다).
- **증권사 의견과 밸류에이션도 계산 명령이 있다.** 여러 증권사의 최근 목표가·의견은 `kis stock opinion-summary
  --stock-code`(기본 90일, 평균·중앙값·최고·최저), 시총·TTM PER·PBR·추정 연도별 PER 은
  `kis stock valuation --stock-code --corp-code`(KIS 종가 + DART 주식수 + DART 재무, 약 11회). `kis stock
  estimated-earnings` 는 한국투자증권 한 곳의 추정이라 컨센서스라 부르지 않는다(`table` 로 라벨됨).
- **환율 명령은 없다.** 금리는 `kis market interest-rate`. 매크로를 웹 검색으로 대신하지 않는다 — 기준일이 섞인다.
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
- **응답은 작게.** `--fields`·`--limit`·`--compact`. 잘리면 `_truncated` 에 실제 `total` 이 온다. `list --json`
  을 필터 없이 부르지 않는다(61KB).
- **exit code 로 분기한다.** 0 정상 · 1 내부 오류 · 2 인자 오류(`error.data.issues[]` 읽고 고친 뒤 재시도) ·
  3 자격증명(중단하고 보고) · 4 브로커/네트워크(`error.retryable` 이 true 일 때만 1회 재시도) ·
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

- KIS = primary, Kiwoom = auxiliary, DART and SEC = reference — defined once in
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
  aggregator (`get_kis_handlers()` / `get_kiwoom_handlers()` / `DART_HANDLERS` / `SEC_HANDLERS`).
- The `name=` passed to `@rpc_method` controls the CLI path via dot-splitting
  (`category.leaf` for kis/kiwoom; brokers in `metadata.FLAT_BROKERS` — dart, sec — have no
  category segment) — wrong dot placement lands the command in the wrong path.
- A `category` missing from `_CATEGORY_DEFAULTS` in `metadata.py` silently falls back to
  domain `market` / tag `ranking` instead of erroring — add an entry for new categories.

## `kis chart technical`/`trend-setup`, `kis stock opinion-summary`/`valuation`, `dart financial-as-filed`/`financial-summary` and the dart/sec filing-text commands compute; every other command passes through

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
- `kis stock opinion-summary` is one `investment-opinion` call plus `opinions.summarize` (factory
  `opinions()`): each broker's latest row in the window, positive targets only.
- `dart financial-summary` calls `financial-full-statements` 8 times (two years × four report codes on one
  basis) and returns derived figures from `statements.py` (ported from cluefin-factory `statements.mjs`,
  archived 2026-10-18). Rules live in that module, not in docs: Q2–Q4 are year-to-date differences, a year's
  own report beats the next year's comparative column, borrowings are summed by label with a
  financial-liabilities fallback (`borrowings_basis` says which), ROE/ROA use average equity/assets.
  `test_dart_handlers_unit.py` lists it with the parsing handlers; `test_dart_financial_summary_unit.py` covers it
  with a fake keyed by (year, reprt_code, fs_div).
- `dart document-outline` / `document-section` / `financial-notes` parse the downloaded original XML with
  cluefin-dart-notes (see the `dart document-*` section) and are excluded from those tests too.
- `sec filing-items` / `filing-exhibit` parse a downloaded document with cluefin-sec-notes (see the `sec *`
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
  mixes price bases.
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
- **일봉은 원주가**(`chart.period` 의 `"1"`). 과거가 안 바뀌므로 덧붙이기만 하고, 매 실행 최근 60일 종가가 다르면 그 종목만
  전 구간 교체(`adj_log` 도 지워 수정계수를 다시 계산). KIS 는 10년 구간을 줘도 **최근 100행**(지수 50행)을 주므로 매번 남은
  구간 전체를 요청하고 가장 오래된 행 전날로 줄여 가다 빈 응답에서 멈춘다 — 거래정지 공백·상장 전 기간에 호출을 쓰지 않는다.
  `bar_log.fetched_from` 이 종목별 시작이고, `--since` 가 앞당겨지면 앞부분만 받아 채운다. 거래정지일은 시가=종가=전일 종가·
  거래량 0 으로 온다. 0 가격은 NULL. 16시(KST) 전에는 전 거래일까지만 받는다.
- **`adj_factor` = KIS 수정종가 ÷ 원주가 종가(날짜별)**. 분할일의 `prtt_rate` 는 0 으로 와서(2018-05 삼성전자) 기업행위를
  원주가 응답만으로는 알 수 없다. 첫 구간 수정주가가 원주가와 모두 같으면 계수 1(호출 1회), 다르면 전 구간. 증분은 최근 60일을
  받아 `close × adj_factor` 와 0.5원 넘게 다르면 새 기업행위로 보고 전 구간 재계산. 2016~ 3,187종목 중 1,662종목이 기업행위
  있음(배당락일 변화도 있다 — KIS 수정주가 정의 그대로). KIS 가 수정주가를 원 단위로 반올림해 저가주의 계수는 날마다 조금씩
  흔들린다 — 그래야 KIS 값과 정확히 같다(2026-10-18 표본 20종목 원주가·수정주가 전 날짜 일치).
- **`rates` 는 ECOS 시장금리(817Y002) 4계열**, 계열당 호출 1번(실키는 행 상한이 없다 — cluefin-openapi AGENTS). 매번 저장된 마지막
  날 7일 전부터 다시 받아 덮어쓴다. `sample` 키(ECOS_AUTH_KEY 없음)는 쪽당 10행이라 10년이면 계열당 ~250회 — 받지 않고 오류 한 줄로
  건너뛴다. ECOS 는 하루 늦게 올라온다(2026-10-25 적재 시 마지막 10-23).
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
  ka90002 연속조회(`cond-yn` 헤더)가 필요한 테마는 없었다. **키움 기간수익률(`dt_prft_rt`)은 원주가 기준이고 테마 값은 구성종목
  단순 평균**이라 감자 종목 하나(+905%)가 테마를 1위로 만든다 — 관심 테마는 캐시 수정주가 중앙값으로 계산한다. `main_stk` 는 종목명
  쉼표 목록이라 같은 테마 구성종목 이름과 맞춘다.
- PIT 한계: `company` 의 이름·업종·상장주식수는 현재 값이다. DART 등록 전에 폐지된 종목은 빠질 수 있다.

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

## `dart financial-*` 가 최신 실적의 기본 경로다

- `kis financial *` 의 `--div-cls-code 1` 은 파라미터가 정상 전달되지만 **종목에 따라
  연간 행만 온다** (2026-09-20 실측: 삼성전자는 202606·202603 분기 행이 오고,
  티씨머티리얼즈 125020 은 FY2024 연간까지만 온다 — DART 에는 FY2025 사업보고서와
  2026 반기보고서가 이미 있는데도). 코드 버그가 아니라 KIS 의 소형주 커버리지다.
  스키마 설명이 이 사실을 안내하므로 문구를 줄이지 말 것.
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
- **라이브러리 메서드 이름이 엔드포인트와 자주 다르다** — `real_estate_development` 는 dfOcr(부도발생),
  `business_letter` 는 bsnSp(영업정지), `corporate_bond_issuance_decision` 은 exbdIsDecsn(교환사채). 클래스 이름
  `MajorShareholderDisclosure` 도 실제로는 주요사항보고서(DS005)다. `handlers/dart.py` 의 `_MAJOR_EVENTS`·`_REPORT_ITEMS`
  (slug → 엔드포인트·한국어 이름·람다)가 진실의 원천이다. `getattr(client, 이름)` 으로 바꾸지 않는다 — 이름이 오해를
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

## `sec *` 는 SEC EDGAR 를 읽는다 (미국 고객사·경쟁사 공시)

- `SEC_USER_AGENT`("이름 이메일")는 루트 `.env` 에 있어야 한다 — `.env.test` 에만 있으면 CLI 는 못 쓴다. 없거나 `@` 가
  없으면 exit 3 `CredentialsMissing`(클라이언트의 ValueError 문구로 분류). SEC 403 은 User-Agent 문제와 과속 차단
  (약 10분)을 구별할 수 없어 exit 3 + 그 둘을 말하는 hint, `*NotFoundError`(404)는 exit 4 `NotFound`.
- **SEC 폴더는 다른 회사 CIK 경로로도 200 을 준다**(2026-10-12 실측). 그래서 `filing-items`·`filing-exhibit` 은
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
- `company-lookup` 은 매번 전체 목록(~1만 행)을 받아 거른다. `filings` 는 SEC 의 recent 목록(1년 이상 또는 1,000건)만 본다.
- 테스트 픽스처는 합성 회사·CIK·접수번호만 쓴다(cluefin-sec-notes AGENTS.md). 스키마 예시의 `cik`/`accession_number`
  샘플은 cluefin-openapi README 와 같은 AAPL 값이다.
- 클라이언트 계약 테스트는 SEC 메서드가 모델을 그대로 돌려주므로 프로브 자체를 응답으로 준다(`bare=True`, 리스트를
  돌려주는 메서드는 `[]`). 핸들러는 모델 **필드**만 읽어야 한다 — `FilingDetail.ciks` 같은 property 를 읽으면 그 테스트가
  실패하므로 `parties` 를 읽는다.

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
