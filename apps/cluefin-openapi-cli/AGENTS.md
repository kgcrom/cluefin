# AGENTS.md — cluefin-openapi-cli

Non-obvious constraints only; see the root AGENTS.md for repo-wide rules and `apps/AGENTS.md` for the cwd `.env` rule.
첫 절은 이 CLI 로 데이터를 조회하는 에이전트의 흐름이고, 그 아래는 broker·명령별 실측 함정과 CLI 를 고칠 때의 제약이다.
명령·옵션·공식은 `--help`·`schema`·`recipe`·모듈 docstring 이 말해 주므로 여기 적지 않는다.

## 에이전트가 데이터를 조회할 때

모든 명령은 **저장소 루트에서** `uv run cluefin-openapi-cli …` 로 부르고 출력은 JSON 이다. 조회 전용이지만 루트 `.env` 의
**실계좌** 자격증명으로 토큰이 발급된다(`apps/AGENTS.md`). 자격증명 값은 어디에도 찍지 않는다 — 확인은 `brokers --json` 의
`credentials.configured` 로 끝낸다.

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

- **출처 역할.** KIS 가 1순위(primary), 키움은 보조(auxiliary) — `kis_alternatives` 가 `[]` 인 명령이나 KIS 가 빈 데이터를
  줬을 때만, DART·SEC·ECOS 는 참고(reference)다. 질문별 출처는 `.claude/agents/company-review.md` 와 `recipe` 가 갖고 있다.
- **실적은 DART, 주당지표만 KIS.** KIS 종목분석(재무제표·재무비율) API 는 2026-11-11 서비스 종료로 없앴다. 리포트용 숫자는
  `dart financial-summary --corp-code <8자리>` 한 번으로 받고 다시 계산하지 않는다(억원). 한 보고서만 볼 때는
  `recipe latest-earnings`. 분기 금액 필드와 정정본 함정은 아래 `dart financial-*` 절에 있다.
- **계산 명령이 있으면 원자료를 받아 직접 계산하지 않는다.** `dart financial-summary`·`dilution-watch`, `kis stock valuation`·
  `valuation-band`·`investor-metrics`·`flow-summary`·`opinion-summary`, `kis chart technical`·`trend-setup`, `ecos macro-snapshot`,
  `cache perf` 가 그런 명령이다. 전부 라벨·판정 없이 값과 구성요소만 주므로 판단의 근거로만 쓴다. 읽을 때 걸리는 곳:
  - `kis stock estimated-earnings` 는 한국투자증권 한 곳의 추정이라 컨센서스라 부르지 않는다.
  - `flow-summary` 의 외국인 지분율은 입력 어디에도 없어 항상 null 이다(`kis stock current-price` 몫).
  - `technical` 의 `signal.trend` 와 `signal.mean_reversion` 은 별개 계열이라 하나의 점수로 합치지 않는다. 값은 `cluefin-desk`
    화면과 다르다(EMA 워밍업 차이) — 이 CLI 가 기준이다.
  - `trend-setup` 의 `atr14_pct` 는 단순 평균이라 `technical` 의 ATR(Wilder)과 다르다 — 두 값을 섞지 않는다. `action` 은 매수
    추천이 아니다(`caveats`). 장 마감(15:40) 전에는 어제 기준이다.
  - `valuation-band` 는 실시간 KIS 호출 없이 로컬 캐시를 읽는다 — `cache load` 가 먼저 돌아 있어야 한다.
- **숫자가 말해 주지 않는 것은 원문에 있다.** 부문별 매출·수주·차입금 만기·우발부채는 `recipe filing-text`(정기보고서·감사보고서만
  읽힌다), 미국 고객사·경쟁사 공시는 `recipe us-peer-filings`(20-F/6-K 제출사는 못 읽는다).
- **매크로는 `ecos`.** 통계표·항목코드를 추측하지 않는다(`table-search` → `items` → `series`). 월·분기 통계는 기간이 끝나고 몇 주
  뒤 올라온다 — 값마다 `time` 이 기준일이다. 매크로를 웹 검색으로 대신하지 않는다 — 기준일이 섞인다.
- **전종목·과거 일봉은 로컬 캐시.** 여러 종목의 일봉, 특정 날짜의 상장 종목(폐지 포함)은 `cache ohlcv`·`cache company --as-of`
  로 읽는다(네트워크 없음). 캐시는 원주가다 — 신호는 `--adjusted true`, 백테스트 체결가는 원주가. 파일이 없으면 exit 2
  `CacheMissing`; `cache load` 는 오래 걸리므로(README) 사용자가 요청할 때만 돌린다. 벤치마크 `U1001` 은 KOSPI200 이 아니라
  코스닥이다(KOSPI200 은 `U2001`) — 캐시에 지수 이름이 없다.
- **명령 하나에 Bash 호출 하나.** `for`·`while`·`$(...)`·`eval`·`bash -c` 로 여러 명령을 묶지 않는다. 호출마다 결과와 exit
  code 가 따로 남아야 분기할 수 있다(worktree 세션에서 막히는 형태는 루트 `AGENTS.md`). 서로 독립인 호출은 같은 턴에 병렬로
  보내되 KIS 는 동시 2개까지로 잡는다. 실측한 한도가 아니라 2026-10 부터 쓰는 보수적인 값이다 — `review collect` 는 자기 풀에서
  KIS 3개로 돌리고 34호출 동안 KIS 실패가 없었다(2026-11-08).
- **응답은 작게.** `--fields`·`--limit`·`--compact`. 잘리면 `_truncated` 에 실제 `total` 이 온다. `list --json` 을 필터 없이
  부르지 않는다(약 130KB, 2026-11-15).
- **exit code 로 분기한다.** 표는 README "오류와 exit code". 2 는 `error.data.issues[]` 를 읽고 고친 뒤 재시도, 3 은 키 누락·무효
  모두이니 중단하고 보고, 4 는 `error.retryable` 이 true 일 때만 1회, 5 는 `data.retry_after` 만큼 대기(DART `status` 020 은
  일일 한도라 재시도 금지).

## Env & safety

- Credential loading is hardcoded to `Path.cwd() / ".env"` (via `cluefin_openapi.client_factory`) — there is no
  `.env.test` or `--env-file` support. What that means for where you run it is in `apps/AGENTS.md`.
- Every registered command is `side_effect="read"` (asserted by a test), but any kis/kiwoom command still generates
  and caches a real auth token. `--dry-run` is the only execution path that never touches auth.
- `--dry-run` is honoured by broker commands and by `review checklist`/`review due` only. `cache *`, `audit *` and
  `review collect|record|track` ignore it even though their `--help` lists it as a global option:
  `review collect --dry-run` really collects.
- `brokers --json` and `--dry-run` report `credentials.configured` as a boolean derived from
  `BrokerClientConfig.from_env()`; never add the values themselves to any payload.
- `main()` sets stdlib logging to WARNING on stderr (`_configure_logging`) so agents get clean stderr. Set
  `CLUEFIN_OPENAPI_DEBUG=1` to lower the `cluefin_openapi` logger to DEBUG; the per-call DEBUG lines also need
  the client's own `debug=True`.

## Broker roles are data, not code paths

- KIS = primary, Kiwoom = auxiliary, DART, SEC and ECOS = reference — defined once in `metadata.BROKER_ROLES`.
  Ordering everywhere (`list`, `brokers`, `iter_brokers`) comes from `broker_rank`, not from alphabetical sorting.
- `metadata.COMMAND_TAXONOMY` is the authoritative domain/tag source, keyed by qualified name and **hand-authored for
  every command**. `_CATEGORY_DEFAULTS` (with its `market`/`ranking` fallback for an unknown category) survives only
  as an unreachable fallback — `test_every_command_has_hand_authored_taxonomy` fails in both directions, so a new
  command or a rename breaks CI rather than silently inheriting a category default. Do not reintroduce
  keyword-derived tags: matching is additive with no removal rule, so tags only ever get noisier.
- `metadata.KIWOOM_KIS_ALTERNATIVES` is a hand-maintained map; a Kiwoom command missing from it is *declared*
  Kiwoom-only and shows up in `brokers --json` → `kiwoom_only_commands`. When adding a Kiwoom handler that overlaps
  KIS, add the entry or agents will treat it as the intended Kiwoom use. `test_agent_surface_unit.py` fails if any key
  or target is not a real command path.

## Exit codes and error envelope

- Exit codes are a contract with agents (`errors.EXIT_CODES`; the table lives in the README and a test compares the
  two). Do not raise `CliError` with a bare exit 1 for a classifiable failure — route it through
  `classify_exception`.
- A bad key is exit 3 too, not only a missing one: KIS token issuance 403 and DART body status 010/011/012/901 are
  raised by the client as `*AuthenticationError` (cluefin-openapi AGENTS). The DART hint names `DART_AUTH_KEY` by
  exception class, not `broker`, because `kis stock valuation` reaches DART under broker `kis`.
- The KIS token endpoint allows one issuance a minute. `EGW00133` is the same HTTP 403 as a bad key but the client
  raises `KISRateLimitError`, so it is exit 5, not exit 3.
- Broker exceptions are classified by **class-name suffix** (`*RateLimitError`, `*AuthenticationError`, …) because
  kis/kiwoom/dart exception hierarchies are parallel copies. A pydantic `ValidationError` from response parsing is
  deliberately separated from broker `*ValidationError` (request rejected) — the former is `ResponseParseError`.
- DART "request limit exceeded" (status `020`, daily quota) never arrives as `DartRateLimitError` (that is only the
  local token-bucket timeout). It is a `status` in an HTTP 200 body: the XML paths raise a generic `DartAPIError`,
  and the JSON paths parse it into a normal model without raising. `classify_exception` maps a `*APIError` whose
  `response_data.status == "020"` to exit 5 (with a daily-quota hint), and `handlers/dart.py` `_checked()` raises
  `errors.DartQuotaExceededAPIError` for the JSON models. Other non-`000` statuses (e.g. `013` no data) are
  deliberately left as they were.
- Validation (`validation.py`) runs *before* any client is created: enum, pattern, bounds, unknown fields, and string
  hardening (control chars, `..`, `%`, `?`, `#`) on every nested string. If a broker ever needs a literal `%`/`?`/`#`
  in a parameter, the hardening list must be made per-field, not removed.

## Commands are hand-written, not generated

- Nothing introspects `cluefin-openapi`. A new client method needs: an `@rpc_method` handler, an entry in that
  module's `_ALL_HANDLERS`, wiring in the broker aggregator (`get_kis_handlers()` / `get_kiwoom_handlers()` /
  `DART_HANDLERS` / `SEC_HANDLERS` / `ECOS_HANDLERS`), a `COMMAND_TAXONOMY` row, and the command-count bump in
  `test_rpc_registry_unit.py`.
- The `name=` passed to `@rpc_method` controls the CLI path via dot-splitting (`category.leaf` for kis/kiwoom;
  brokers in `metadata.FLAT_BROKERS` — dart, sec, ecos — have no category segment) — wrong dot placement lands the
  command in the wrong path.
- A schema boolean given bare means true (`--listed-only`); it takes the next token only when that is a boolean word
  (`--include-today false`). Meta commands (`cache`, `review`, `audit`) parse their own options and need a value:
  `--history true`, and a bare `--history` is exit 2.

## Computing commands (every other command passes through)

- A handler that calls the client more than once, crosses brokers or parses a download does not fit
  `_handler_fakes.assert_calls_client_once`. Exclude it in that broker's handler test and cover it in its own file
  with one fake session. `test_handler_client_contract_unit.py` swallows `CliError` for the same reason — its probe
  returns `None` for every output field, which a computing handler correctly treats as an empty response.
- The math lives in pure modules with no I/O (`statements.py`, `quality.py`, `investor_metrics.py`, `band.py`,
  `implied.py`, `flows.py`, `dilution.py`, `macro.py`, `industry.py`); formulas, sources and measured vendor quirks
  are in their docstrings, not here. Three decisions hold across all of them: no labels or verdicts, values and
  formula components only (2026-11-04); a missing input returns `null` plus a reason, never 0; a command reuses
  another's module instead of recomputing (`investor-metrics` takes ROIC and Altman Z'' from `quality.py`).
- **Cross-broker commands**: `kis stock valuation` and `investor-metrics` (KIS + DART), `implied-expectations` (KIS +
  DART + ECOS, plus Damodaran through `cluefin-feeds`), `valuation-band` (DART + the local cache, no live KIS call).
  `_BrokerSession` creates clients per broker on demand; each broker still runs its own credentials check, so a
  missing DART key fails with exit 3 only when the command reaches DART. Market cap uses **issued** common shares
  (KRX convention, treasury included); preferred shares are ignored.
- `kis stock valuation-band` divides every year by **one** common share count — the latest periodic report filed by
  `as_of`, divided by the `adj_factor` on that report's period end (`share_base`). Dividing each year by its own
  count halved PER for a year after a bonus issue or split (post-action price ÷ pre-action EPS; 2026-11-08). The
  statements are deliberately **not** `cache financials`, which has no 지배/비지배 split (2026-11-04), and the band
  uses one basis throughout: CFS for every year, OFS only if CFS is empty everywhere.
- `kis stock implied-expectations`: `_fetch_damodaran_korea` is its own function so unit tests can monkeypatch it and
  never touch the network. Without `--erp`, a failed fetch is exit 4 `BrokerUnavailable` (retryable, hint: pass
  `--erp`); for `--tax-rate` alone it falls back to a stated default rate instead.
- `kis stock investor-metrics`, fixed 2026-11-08 after real filings: some filers report capex as a negative number,
  so FCF and owner earnings use its absolute value (the `capex` field stays as filed); the borrowings pattern accepts
  "단기/장기차입금 및 사채" and falls back to the borrowings XBRL id; unknown borrowings or cash make EV `null` with
  `ev_reason` instead of a zero-debt EV. Cash-flow metrics read the latest annual report's own year because
  `statements.py` never builds a TTM cash flow (quarterly rows are year-to-date only), while EV/EBIT and PER use TTM.
  `shareholder_yield` is the one place a missing line counts as 0 (listed in `assumed_zero`). The two PEG growth
  sources are never averaged.
- XBRL ids checked against real filings: `proceeds_from_share_issuance` (2026-11-04) and `treasury_shares_disposed`
  (`dart_DispositionOfTreasuryShares`, 2026-11-08). Filers off the standard taxonomy still match by label only.
- `kis stock flow-summary` windows five KIS endpoints; their measured row counts, paging and units are in the
  `flows.py` docstring. What bites: units differ **within one row** (`*_ntby_tr_pbmn` 백만원 beside `acml_tr_pbmn` raw
  원) and were confirmed by `qty × close`, not from the portal docs; three endpoints give 30 rows with no continuation
  key and are paged by asking again for the day before the oldest row; the credit series' `deal_date` lags the others
  by settlement, so `as_of.credit` differs; no input carries a share denominator, so `foreign_ownership` and
  `pct_of_listed_shares` are always `null`. Before 15:40 KST today's row is dropped (`_flow_summary_now`, injected in
  tests like `domestic_basic_quote._now`).
- `dart financial-summary` calls `financial-full-statements` 8 times (two years × four report codes on one basis) and
  derives figures in `statements.py` (ported from cluefin-factory `statements.mjs`, archived 2026-10-18); the rules
  live in that module.
  - The account → XBRL id/label table is data, `accounts/common.toml` (file order = output field order); change ids
    there with a `#` reason. `latest.account_match` reports how each account matched.
  - `accounts/financial.toml` (bank/insurer/securities) is read for every filer — no industry detection — and its
    keys appear only when a `marker = true` account has a value. Markers are accounts no general filer files
    (62-filer sample, 2026-11-09); 사채·FVOCI·재보험계약자산·차입부채 are not markers because general filers (or their
    financial subsidiaries) file them too. Adding a marker needs that check again.
  - `credit_loss_expense` keeps the filed sign, and filers disagree: those that label it "환입(전입)" report a
    provision as a negative number (2026-11-10).
- `dart financial-as-filed`'s `note_figures` block reads D&A, interest and taxes paid by XBRL concept from the same
  document — the OpenAPI rows `financial-summary` uses carry them only for filers that itemize cash-flow adjustments
  (8 of 62 sample filers for depreciation, 54 in XBRL, 2026-11-10). HTML notes of pre-XBRL years or small filers are
  not read for this.
- `kis chart technical` pages `chart.period` itself (`ohlcv.fetch_kis_daily_series`) and returns readings only — the
  candle series never reaches the caller, which is the whole reason it exists.
- **`adj_price` polarity is inverted between the two KIS chart endpoints** — `chart.daily` is
  `0:unadjusted, 1:adjusted`, `chart.period` is `0:adjusted, 1:original`. Always go through
  `ohlcv.adj_price_flag(endpoint, adjusted=...)`; a raw "0"/"1" silently mixes price bases. Both handlers echo
  `adjusted: bool` at the top of the response.
- **`ohlcv` parses missing values to NaN, never 0.0** (unlike desk's `_safe_float`), and takes the magnitude of every
  Kiwoom price — Kiwoom signs some responses (`cur_prc` is `"-270406"` on down days).
- Minute bars are not daily bars with a finer stamp: KIS minute responses have **no** `stck_clpr` and no per-bar
  `acml_vol` (that field is the running day total on `output1`). `from_kis_minute` reads `stck_prpr`/`cntg_vol`.
- **Signals are reported as two families, never one score.** `macd`/`ma_stack` are trend-following and
  `rsi`/`bbands`/`stoch` are mean-reverting; averaging all five cancels out precisely when the reading is strongest
  (a sustained rise and a sustained collapse both score 0.0). Do not collapse them back into a single BUY/SELL.
- Signal aggregation stays in the CLI on purpose. `cluefin-ta`'s contract is ta-lib parity, and a BUY/SELL score has
  no ta-lib counterpart to be parity-tested against. Only new *indicators* belong in `cluefin-ta`.
- Numbers will **not** match `cluefin-desk`: desk's pandas `ewm(span=N)` has no warm-up gap, while `cluefin-ta`
  follows ta-lib's SMA-seeded EMA with `N-1` leading NaNs. `cluefin-ta` is the reference here.

## `trend-setup` 은 백테스트 정의를 옮긴 것이다 (`trend_setup.py`)

- 규칙과 근거는 README "trend-setup 규칙과 근거". 공식은 cluefin-factory(아카이브) `scripts/watchlist/*.mjs` `a5cfbcf` 의 이식이고
  임계값은 그 공식에만 의미가 있다 — ta-lib 정의(Wilder ATR, SMA 시드)로 "고치면" 근거가 사라진다. 그래서 이 모듈은 cluefin-ta 를
  import 하지 않는다. 골든 픽스처(`tests/fixtures/trend_setup/stock-*.json`)의 `expected` 는 백테스트 파이썬 산출값이다 — 테스트가
  깨지면 코드를 고치지 기대값을 고치지 않는다. 파일 이름은 종목코드 대신 중립 이름이다.
- 판정은 마지막 **260봉**으로 한다(두 명령 같음). 프랙탈 피봇은 창 안에서만 찾으므로 봉 수를 바꾸면 드물게 피봇이 달라진다.
  이력(`history`)은 그 전 60봉을 더 쓴다(kis 는 320봉, 지수 500일).
- 장중 캔들: `end_date` 없이 15:40(KST) 전에 부르면 오늘 캔들을 버리고 `dropped_intraday_candle` 에 적는다. `include_today` 로
  유지하면 caveat. 시각은 `handlers/kis/domestic_basic_quote._now()` 로 주입한다(테스트).
- 지수는 코스피 `0001`·코스닥 `1001`(KOSPI200 아님). `benchmark=auto` 는 basic-info `mket_id_cd`(STK/KSQ), 그 밖은 exit 2.
  지수에 종목 마지막 날짜가 없으면 가까운 날로 메우지 않고 exit 4 `IndexDateMismatch`.
- 판정은 상태를 저장하지 않는다. 이전 상태는 `history` 가 지난 봉으로 다시 계산한 값이다(`_judge` 를 날마다 다시 부름).
  성과와 엮는 필터·문구는 표본 외 검증을 통과한 것만 낸다(README §9) — 2026-10 검증에서 `fresh_g3`(3그룹 2~3일)만 통과,
  1그룹 이력은 실패라 필터가 없다. 새 이력 필터를 더하려면 같은 통과 기준으로 표본 외 검증부터 한다.

## `cache *` 는 로컬 DuckDB 파일이다 (`cache/`)

적재 방식은 모듈 docstring(`bars.py`·`adjust.py`·`company.py`·`rates.py`·`theme.py`·`financials.py`·`throttle.py`)에 있다. 여기는
거기 없는 결정과 실측만 적는다.

- 메타 명령이다(`main.META_COMMANDS`, registry 밖). `cache load` 만 broker 를 부르고 나머지는 파일만 읽는다. `--dry-run` 은 없다.
- **쓰는 프로세스는 하나, 쓰는 동안 읽기도 막힌다**(DuckDB). 읽기는 `read_only=True` 로 열고 잠금은 `CacheLocked`.
  `cache load` 는 병렬 호출을 하지 않는다 — 사용자 결정(2026-10-18).
- **KIS 초당 한도는 429 가 아니라 HTTP 500 `EGW00201`** 이고 클라이언트 기본 20 req/s 에서도 ~10% 가 걸린다. 클라이언트 재시도에
  맡기면 실효 ~5 req/s 라 적재는 `max_retries=0` 으로 열고 `throttle.kis_call` 이 0.1초 뒤 다시 부른다(~15 req/s).
  `EGW00300`·`EGW00316`·`OPSQ1002`(SESSION FULL, HTTP 200 rt_cd 9)도 7만 회 적재에서 몇 건씩 나왔다.
- **유니버스는 키움 ka10099 의 `거래소`·`코스닥` 종류만**(ETF·ETN·리츠 제외). 2016년 이후 폐지 주식은 DART `stock_code` 차집합에서
  보충하되 basic-info 의 `mket_id_cd`(STK/KSQ)·`scty_grp_id_cd`(ST/FS/DR)로 거른다 — 차집합에는 코넥스(상장일이 **코스닥** 필드에
  있다)·리츠·선박투자가 섞인다. 우선주는 DART 에 없어 끝자리를 0 으로 바꾼 보통주의 `corp_code` 를 쓴다. KIS `setl_mmdd` 는
  `'12'`·`'1231'` 두 형식이고 빈 종목은 DART 기업개황 `acc_mt` 로 채운다.
- **일봉은 원주가**이고 매 실행 최근 60일 종가를 다시 받아 비교한다. 마지막 저장일 종가만 다르면 그 행만 덮어쓴다(`patched`) —
  그날 봉은 적재 뒤 KIS 값이 바뀔 수 있어서다. 이 구분이 없던 2026-11-04 증분 적재는 대부분 종목의 10-23 종가만 달라 전 구간
  교체로 70분이 걸렸다. 거래정지일은 시가=종가=전일 종가·거래량 0 으로 온다. 0 가격은 NULL. 16시(KST) 전에는 전 거래일까지만 받는다.
- **`adj_factor` = KIS 수정종가 ÷ 원주가 종가(날짜별)**. 분할일의 `prtt_rate` 는 0 으로 와서(2018-05 삼성전자) 기업행위를 원주가
  응답만으로는 알 수 없다. 증분은 최근 60일이 `close × adj_factor` 와 0.5원 넘게 다르면 새 기업행위로 보고 그 종목만
  전 구간 재계산한다. 2016~ 3,187종목 중 1,662종목에 기업행위가 있다(배당락일 변화 포함 — KIS 수정주가 정의 그대로). KIS 가
  수정주가를 원 단위로 반올림해 저가주의 계수는 날마다 조금씩 흔들린다 — 그래야 KIS 값과 정확히 같다(2026-10-18 표본 20종목 전
  날짜 일치).
- **`rates`**: `sample` 키(ECOS_AUTH_KEY 없음)는 쪽당 10행이라 10년이면 계열당 ~250회 — 받지 않고 오류 한 줄로 건너뛴다.
  ECOS 는 하루 늦게 올라온다(2026-10-25 적재 시 마지막 10-23). `usdkrw` 는 연 %가 아니라 환율 수준값이라 `--risk-free` 가 받는
  `RATE_SERIES` 에는 넣지 않는다.
- `cache perf` 의 수익률은 **수정종가**다. 원주가로는 분할일이 -98% 손실로 보인다. 벤치마크와 날짜를 inner join 하므로 한쪽에
  없는 날은 빠진다. 지표 정의는 `cluefin-ta` 가 갖고 여기서 다시 계산하지 않는다. `--risk-free <계열>` 은 기간 첫날 이전의 마지막
  발표값을 쓰고, 10일 넘게 묵은 값(적재가 멈춘 캐시)은 exit 2 `RatesMissing` 이다.
- **`cache trend-setup` 에 규칙을 두지 않는다.** 종목마다 `trend_setup.analyze` 를 부르고(`kis chart trend-setup` 과 같은 함수),
  `test_cache_trend_unit.py` 가 두 결과가 같은지 본다. 유니버스는 백테스트와 같다: 그날 상장, 끝자리 0, 이름에 "스팩" 없음, 0 가격
  봉 제외. 2026-10-16 전 종목 2,487개가 research `scan.py` 와 action·status·피봇·rel 모두 같았다. `--market`·`--code` 로 행을
  좁혀도 전 종목을 판정한다(테마 주도주 순위가 전 종목 기준이라서). `cache rs`·`screen` 의 백분위도 늘 전 종목 기준이다.
- **`theme` 은 키움 테마 스냅샷**이다. 키움은 현재 값만 줘서 날마다 쌓는다. 평일 16시 전은 장중이라 건너뛰고, 이름 붙일 날짜는
  KIS 지수 일봉의 마지막 거래일이다(휴장일 이름으로 쌓지 않게). 연속조회 헤더는 `cont-yn` 만 먹는다 — 문서의 `cond-yn` 은
  무시된다. 키움 기간수익률(`dt_prft_rt`)을 쓰지 않는 이유는 README §8. `main_stk` 는 종목명 쉼표 목록이라 같은 테마 구성종목
  이름과 맞춘다.
- PIT 한계: `company` 의 이름·업종·상장주식수는 현재 값이다. DART 등록 전에 폐지된 종목은 빠질 수 있다. 그래서 `base-rate`·
  `magic-formula`·`screen` 의 과거 시총은 그날 원주가 × **현재** `list_count` 근사다.
- **`base-rate-build` 만 쓴다**(`setup_state`, 거래일 5일 간격 표본, 증분·멱등). 첫 구축 실측 9분 45초(2026-11-03, 표본일 530개·
  486,382행), 조회는 1~2초. `setup_state` 의 `adj_close`·`index_close` 열은 쓰기만 하고 읽지 않는다 — `cache load` 가 새
  기업행위로 `adj_factor` 를 전 구간 재계산하면 적재 당시 값과 섞여 초과수익이 분할 비율만큼 튀므로 조회 때마다 `ohlcv` 에서 다시
  읽는다.
- **순위 백분위는 x.5 를 올림한다**(`breadth._round_half_up`). `round()` 는 짝수로 보내 50.5+49.5 와 50.4+49.7 이 둘 다 100 이
  됐다(2026-11-08). 정렬은 반올림 전 값으로 하고, `magic-formula` 의 `combined_rank` 는 표시된 두 순위의 합과 1 차이 날 수 있다.
  `cache peers` 만 백분위가 아니라 서수 합이다.
- **`financials` 는 DART `fnlttMultiAcnt`(다중회사 주요계정)다**(결정 2026-11-04). 지배/비지배 구분도 현금흐름표도 없어서 그게
  필요한 계산은 종목별 `financial-full-statements` 를 부른다. 그래서 `screen` 의 per·pbr·roe 는 비지배지분을 포함한 연결 전체
  기준이고 지주회사·모회사는 pbr 이 0.1 아래로도 나온다(2026-11-09 pbr<0.3 이 400종목). EV·투하자본도 현금·이자부채 구분이 없어
  근사다. 회사 101개를 한 번에 물으면 상태 021 인데 JSON 경로라 예외 없이 빈 `list` 로 온다(020 과 같은 모양). 우선주는 자체
  행이 없어 보통주의 행을 주고 `financials_code` 에 적는다.
- **한 종목 오류로 배치 100개를 통째로 버리지 않는다**(2026-11-04 전종목 적재: 192배치 중 31개가 통째로 실패). 중복
  `corp_code` 가 섞인 배치는 JSON 대신 HTML 에러 페이지로 302 리다이렉트된다 — 우선주와 보통주가 같은 배치에 들면 둘 다 보통주의
  `corp_code` 라 중복이 생겼다. 그 밖의 실패는 `_narrow` 가 배치를 반씩 쪼개 한 회사까지 좁히고 `status='error'` 로 남겨 다음
  실행에 다시 시도한다. 020(일일 한도)만은 쪼개지 않고 멈춘다.
- **`financials` 표는 DART 계정명을 그대로 저장한다** — 실캐시(2026-11-11)에 bare "당기순이익"은 한 건도 없고 전부
  "당기순이익(손실)"이다. 읽는 쪽이 `cache.financials.account_spellings`/`fold_accounts` 로 두 철자를 같이 읽는다(그 전의
  `magic-formula` 는 "영업이익(손실)" 종목을 재무 없음으로 뺐다). 표를 읽는 새 코드도 이 둘을 거친다.
- **`screen` 의 업종 백분위(`*_sector_pct`)는 출력 행을 좁히기 전 전 종목으로 매긴다.** `--exclude-*` 도 출력만 뺀다.
  `--rank` 는 `--where`·제외 뒤 남은 행끼리 순위를 매긴다. `--compare-as-of` 의 그날 재무는 그때 제출기한이 지난 것만이지만
  시총은 현재 `list_count`, 관리종목·거래정지 여부도 현재 값이다. 이익 성장 팩터는 EPS 대신 순이익이다(과거 주식수 없음).
- **분기 보고서의 손익 `thstrm_amount` 는 그 분기 3개월이고 누적은 `thstrm_add_amount` 다**(2026-11-22 실측). 연간 표와
  같은 로더(`_fetch`)를 `reprt_code` 만 바꿔 쓴다. TTM 의 전년 같은 기간 누적은 같은 보고서의 비교값(`frmtrm_add_amount`)을
  먼저 쓴다. 12월 결산이 아닌 회사·늦은 제출은 `empty` 로 남으므로 기한 1년 안의 분기는 `empty` 도 다시 묻는다.

## `review *` 는 수집과 판단 기록을 CLI 가 맡는다 (`review/`)

- 검토 데이터 수집을 LLM 이 아니라 여기서 펼친다(결정 2026-11-08): 서브에이전트는 서브에이전트를 못 띄우고, 수집은
  결정적이며, 응답 JSON 이 agent 맥락에 쌓이는 게 문제였다. 명령 목록은 company-review 감사 블록과 맞춘다 — 블록을
  고치면 `collect.py` 의 stage 함수도 같이 고친다.
- `collect` 는 gate → 1단계 → 2단계로 돈다. gate 는 `kis stock current-price` 를 먼저 혼자 불러 디스크의 KIS 토큰 캐시를
  채우고(뒤의 프로세스들이 공유한다) corp code 와 캐시 상태를 본다. 1단계는 종목코드·corp code 만 있으면 되는 것, 2단계는
  1단계 답(업종코드·접수번호·보고서 연도·비교 기업 corp code)이 필요한 것이다. 2026-11-08 실측: 본 종목 + 비교 1곳 34호출
  17.6초, 실패 하나는 `ecos industry-outlook` exit 2 였다 — 비제조업 종목이면 정상이다.
- 명령마다 spawn 한 새 프로세스에서 `run_cli` 를 부른다(`process_runner`: spawn `ProcessPoolExecutor(max_tasks_per_child=1)`).
  stdout·exit code 가 수동 호출과 같아야 감사가 근거로 쓴다. `subprocess.run` 은 Codacy 가 정적 문자열이 아닌 인자를 critical 로
  잡아서, 스레드는 `run_cli` 가 전역 stdout 을 바꿔서 쓰지 않는다.
- 동시성 상한은 `BROKER_LIMITS`(kis 3, dart 3, ecos 2, cache 1 — DuckDB 파일 잠금). `retryable` 인 exit 4·5 만 두 번 더
  시도한다. kis·dart exit 3 이면 그 단계 뒤로 멈춘다.
- 폴더는 지우거나 덮지 않는다. 같은 날 다시 돌리면 `-2`, `-3` 을 붙인다. 기본 자리 `/private/tmp/cluefin-review`
  (`$CLUEFIN_REVIEW_DIR` 로 바꾼다).
- `record` 가 읽는 판단 파일은 `verdict.json` 이다. YAML 로 쓰던 때는 파서가 없었고 `030000` 이 숫자로 읽혔다 —
  `stock_code` 는 6자리 **문자열**이어야 한다. `blocked` 는 추적할 가격이 없어 받지 않는다(판단은 buy·hold·sell·watch 뿐).
  watch 와 hold 는 `trigger.entry_above`·`exit_below` 중 하나, buy·sell 은 `target`·`stop` 이 있어야 한다. 문제는 한 번에
  전부 알려 준다(exit 2).
- `research/verdicts.jsonl` 은 덧붙이기만 한다. 손으로 고친 줄이 깨져 있으면 `record`·`track` 이 줄 번호와 함께 exit 2 로
  멈춘다. `research/` 는 worktree 에서 돌려도 메인 체크아웃의 것이다(`review/paths.py` 가 `.git` 의 `commondir` 를 따라간다,
  `$CLUEFIN_RESEARCH_DIR` 로 바꿈) — worktree 를 지울 때 기록이 같이 사라지지 않게 했다.
- `checklist` 의 metric 은 다른 명령이 이미 계산한 필드를 raw 파일에서 읽을 뿐 다시 계산하지 않는다. 수급 metric 은
  `kis stock flow-summary` 가 생기기 전(2026-11-11 이전)에 만든 수집 폴더에서는 `unknown` 이다. `--init` 은 파일이 있으면
  exit 2 다 — 사용자의 기존 기준표를 덮지 않는다.
- `due --events true` 는 KIS `schedule.*` 명령을 `stock_code` 없이 기간으로 한 번씩 부르고 `sht_cd` 로 거른다. 이 CLI 의
  schedule 핸들러는 `cts` 를 응답에 echo 하지 않아(요청 파라미터로만 받는다) 100행에서 조용히 잘린다(실호출 2026-11-11, 2년 창).
  `listing` 은 짧은 응답도 빈 행으로 100행을 채워 보내므로(14일 창: 실제 23종목 + 빈 행) `sht_cd` 가 빈 행은 버리고 센다.
  실제 행이 100이면 그 명령만 종목마다 `--stock-code` 로 다시 부르고 `refetched_per_stock` 에 적는다. 실패한 호출은 `failed` 에
  exit code 와 함께 남긴다 — "일정 없음" 으로 읽지 않게.
- `due` 의 공시 조회에서 DART status 013 + `list: null` 은 실패가 아니라 그 기간 공시 0건이다(2026-11-11 열린 판단 8종목 중
  5종목). 다음 정기보고서 마감일은 `company.settle_month` 로 계산만 한다(분기·반기 +45일, 사업보고서 +90일, 주말이면 월요일) —
  공휴일과 제출 여부는 모른다.

## `audit *` 는 Claude Code 트랜스크립트를 읽는다 (`audit/`)

- broker 도 캐시 쓰기도 없다. 판단 적중(수익률)은 보지 않는다 — 수집 누락·중복·실패 처리만 결정적으로 본다(결정 2026-11-05).
  받은 데이터를 리포트가 놓쳤는지는 `.claude/agents/agent-audit.md` 가 `audit trace` 를 읽고 판단한다.
- 규칙의 출처는 각 `.claude/agents/<name>.md` 끝의 `audit` 펜스 블록 하나다(`subjects`·`required`·`main`·`each`·
  `stop-on-exit3`·`report-has`·`report-lacks`). 코드에 명령 목록을 두지 않는다 — agent 데이터 절을 고치면 그 블록만 같이 고친다.
- 트랜스크립트는 `$CLAUDE_CONFIG_DIR/projects`(기본 `~/.claude/projects`)에서 저장소 경로의 slug 로 시작하는 폴더 전부에서
  찾는다(worktree 포함). 스트리밍 턴은 같은 `tool_use` 를 여러 행에 반복하므로 id 로 한 번만 센다. exit code 는 성공이 0,
  권한 거부처럼 결과가 없는 호출은 null 이다.
- 셸 파싱: `2>&1`·`> file` 은 토큰화 전에 지운다(안 지우면 `--json 2` 로 읽힌다). 인자에 `$` 가 있으면 루프·`$(...)` 로 보고
  중복 대신 `shell_expansion` 으로 센다. 탐색 명령(`search`·`schema`·`recipe` 등)은 중복으로 세지 않는다.
- 블록과 무관하게 늘 보는 것: 출력을 파일로 보낸 호출(`output_to_file` — 응답에 데이터가 없어 근거를 대조할 수 없다,
  `2>&1`·`>/dev/null` 은 제외), CLI 밖 경로(`off_cli_secret`: `.env` 읽기·키 변수, `off_cli_direct_api`: curl·
  `cluefin_openapi` 직접 import, `off_cli_order`: 그 안의 주문 흔적). CLI 명령은 전부 `side_effect: read` 라 주문·키 노출은
  CLI 밖에서만 생긴다. `duplicate` 의 `same_output: false` 는 같은 인자에 다른 응답(페이지·불안정)이다.
- `review collect` 호출은 출력의 `out` 폴더 `manifest.jsonl` 을 읽어 그 뒤에 호출로 펼친다(`CliCall.via` = 폴더, 출력 =
  raw 파일). 폴더가 지워졌으면 `collect_manifest_missing` 이다. 펼친 호출은 별도 프로세스라 `output_to_file` 이 아니다.
  그 폴더의 `report.md`(agent 가 쓴 리포트)는 마지막 답변 앞에 붙여 `report-has` 검사에 쓴다.
- 대상 종목: `subjects: prompt`/`report` 는 그 텍스트의 6자리 숫자 중 캐시 `company` 에 있는 코드만(캐시가 없으면 전부).
  `--session --code` 는 대화에 다른 작업이 섞여 있어 텍스트를 쓰지 않고 `each` 명령에 넘긴 코드만 본다. corp-code 로 부른
  명령은 출력 어디든 `stock_code`·`corp_code` 가 함께 있는 객체로 매핑한다.
- `agent_commit` 은 실행 시작 전 agent 파일의 마지막 커밋이다. `--follow` 는 `--before` 와 같이 쓰면 아무것도 못 찾아서
  옛 이름(`check.ALIASES`)을 경로로 나열한다. 검사는 **현재** 파일 기준이라 그 뒤에 추가된 명령은 누락으로 나온다(`notes`).

## `dart corp-code-lookup` 은 전체 색인을 받아 클라이언트에서 거른다

- DART 의 corpCode.xml 에는 검색 파라미터가 없다. 어떤 필터를 줘도 **매번 전체 색인(2026-09-17 실측 119,313행)을 내려받아**
  핸들러가 메모리에서 거른다. 필터는 호출량을 줄이지 않으므로 반복 조회는 호출부에서 캐시할 일이다(desk 의 `_get_corp_code` 가
  화면당 한 번으로 메모이즈하는 이유).
- 상한 파라미터가 `max_rows` 인 것은 `--limit` 이 전역 CLI 옵션이라 핸들러 params 까지 전달되지 않기 때문이다.
- `stock_code` 는 비상장사에서 공백 문자열로 채워져 오므로 비교 전에 `_clean()` 으로 strip 한다. `listed_only` 도 "값이 있다"가
  아니라 "strip 후 비어 있지 않다"로 판정한다.
- **`listed_only` 는 "현재 상장" 필터가 아니다.** DART 는 폐지 회사의 `stock_code` 를 지우지 않는다(2026-10-18 실측: 한진해운
  117930, 2017-03 폐지, `corp_cls` 만 null). 전종목 유니버스는 키움 ka10099 로 만든다. 폐지 여부는 KIS `basic-info` 의
  `scts_mket_lstg_abol_dt`/`kosdaq_mket_lstg_abol_dt`; `kis stock current-price` 는 폐지 종목에서 필드가 빠진 몸체를 받으면
  `basic-info` 를 한 번 더 불러 exit 4 `Delisted` 로 바꾼다.

## `dart financial-*` 가 실적의 유일한 경로다

- DART 주요계정의 손익 행은 **분기 보고서에서 `thstrm_amount` 가 해당 분기 단독, `thstrm_add_amount` 가 연초 누적**이다
  (1분기는 둘이 같은 값, 사업보고서와 재무상태표 행은 누적이 `None`). 반기 실적을 전년과 비교할 때 `thstrm_amount` 를 쓰면
  성장률이 절반 가까이 틀어진다. `frmtrm_add_amount` 가 전년 동기 누적이다.
- 주요계정 응답에는 `fs_div` 파라미터가 없고 회사가 제출한 기준(연결·개별)이 그대로 온다. 연결재무제표가 없는 회사는 OFS 행만
  온다. 전체 재무제표만 `fs_div` 를 받는다.
- JSON API(`financial-major-accounts`·`financial-full-statements`)는 **최신 정정본 값만** 준다. 노드메이슨(01328170) FY2024
  연결 영업이익은 원본 20250318001317 이 28,915,427, 정정 20250828000839 가 -190,143,795 인데 JSON 은 후자만 준다. 접수 당시
  값은 `financial-as-filed`(접수번호별 fnlttXbrl.xml)로만 얻는다. 전기 열은 나중 보고서에서 재작성된 값이므로 당기 열만
  as-filed 다. 그래서 `financial-summary` 의 `as_of` 도 **접수일**(`rcept_no` 앞 8자리)로만 거르고, 통과한 보고서의 숫자는 정정 후
  값일 수 있다.
- `financial-summary` 는 연초(사업보고서 제출 전)에는 두 해 창에 사업보고서가 없어 전전년 사업보고서를 한 번 더 부른다(`calls` 9).
- `dart share-count` 의 수치는 `"5,969,782,550"` 같은 콤마 문자열이고 결측은 `"-"` 로 온다. 패스스루라 변환하지 않는다.
  각 행의 `rcept_no` 는 원본이 아닌 최신 정정 보고서다(2026-09-30 실측: 노드메이슨 2024 사업보고서 4행 모두 정정
  `20250828000839`). 원본 시점 주식수는 이 API로 얻을 수 없다.
- 복수회사 조회는 일부러 뺐다 — 배열 입력이 "read 패스스루" 계약과 맞지 않는다. XBRL 원문 파일도 내지 않는다(임시 디렉터리에
  받아 파싱하고 지운다). 파싱된 행만 `financial-as-filed` 로 나간다.
- 엉뚱한 `rcept_no` 는 오류 없이 **다른 회사의 유효한 ZIP** 을 돌려주고, `reprt_code` 는 서버가 무시한다. 그래서 `corp_code` 가
  필수이고 파싱된 `entity_id` 와 다르면 exit 4 다.
- Arelle 은 콜드 캐시(`~/Library/Caches/Arelle`)에서 택소노미를 네트워크로 받아 첫 파싱이 최대 ~76초 걸린다. 오프라인+콜드면
  택소노미를 못 읽어 cluefin-xbrl 이 `XbrlParseError` 를 내고 exit 4 가 된다(예전엔 예외 없이 facts 가 빈 문서가 왔다 — facts 0·
  기간 없음 검사는 안전망으로 남겨 둠). 단위 테스트는 파서를 monkeypatch 해 네트워크를 타지 않는다.
- Arelle 은 `[info] loaded …` 를 **stdout** 에 찍는다. 파싱 호출을 `redirect_stdout(sys.stderr)` 로 감싸지 않으면 JSON 출력이
  깨진다 — 파서를 monkeypatch 하는 단위 테스트·핸들러를 직접 부르는 통합 테스트로는 안 보인다.
- 회사에 따라 IS 키가 없고 손익이 CIS 에만 있다(노드메이슨), 연결재무제표가 없는 회사도 있다(티씨머티리얼즈). IS 를 CIS 로
  합성하지 않고, 요청했지만 없는 것은 응답 `missing`(`"IS/consolidated"` 형식)에 적는다.

## `dart document-*` · `dart financial-notes` 는 공시 원문을 받아 파싱한다

- `disclosure_document_files` 로 임시 디렉터리에 받고 cluefin-dart-notes 로 파싱한다(디스크에 남기지 않음). 세 명령이 같은
  `rcept_no` 를 각자 다시 받는다 — 캐시는 없다. 2026-10-12 실측: 대형주 반기보고서 6.8MB, 다운로드+파싱 ~1초.
- `corp_code` 는 필수이고 **첨부 감사보고서까지 모든 파일**의 `AREGCIK` 가 같아야 한다(다르면 exit 4). 2019·2025·2026
  정기보고서와 감사보고서 단독 공시 모두 본문·감사보고서에 8자리 고유번호가 있었다.
- 2017년 이전 접수번호(앞 4자리)는 클라이언트를 만들기 전에 exit 2. 파서 지원 범위 밖이다.
- 핸들러는 `disclosure_document_files` 의 반환값이 아니라 **임시 디렉터리를 다시 훑는다**. `test_handler_client_contract_unit.py`
  의 프로브가 경로 목록을 주지 않기 때문이고, XML 0개는 exit 4 다.
- `index` 는 파일 경계를 넘어 매긴다(본문 먼저, 나머지 파일 이름순 — `_xml_entries` 와 같은 순서). outline 의 `chars` 는 하위
  섹션과 그 제목을 포함하고, `document-section --index` 의 `total_chars` 와 같다.
- `document-section` 의 선택자(`section`·`assoc_code`·`title`·`index`)는 정확히 하나여야 한다. 계약 테스트는 모든 파라미터에
  샘플을 채우므로 `_EXCLUSIVE_SELECTORS` 로 선택자 하나만 남긴다 — 선택자가 있는 명령을 추가하면 거기에도 넣을 것.
  `assoc_code` glob 은 `*` 만 된다(`?` 는 문자열 검증이 막는다).
- `max_chars`(기본 20000)는 블록 경계에서 자르고 첫 블록은 넘어도 돌려준다. 실측 크기: 대형주 "II. 사업의 내용" 36–61k자, 하위
  섹션 ≤18k자, 주석 섹션 75–130k자, 가장 큰 노트 43k자, 노트 중앙값 ~1k자. JSON 은 글자 수의 ~1.5배.
- `financial-notes` 는 정기보고서가 있으면 그 주석만 읽는다. 정기보고서 ZIP 의 첨부 감사보고서 주석은 같은 내용을 반복하고
  (2019 실측: 별도 주석의 글자 수가 같았다) 노트 제목 없이 연번 분할로만 나뉜다. 감사보고서만 든 공시일 때만 감사보고서
  주석(00760 별도, 00761 연결)을 쓴다.
- 분할 경고(`warnings`)는 모든 모드에서 출처별로 그대로 내보낸다. 구형 공시에서 흔하다(2019 대형주 별도 주석: 4·18번 없음).
  노트를 하나도 못 나누면 본문이 전부 preamble 이라 이 명령으로는 못 읽는다 — hint 가 `document-section --index` 로 보낸다.

## `dart major-event` · `report-item` · `dilution-watch` 는 람다 표로 디스패치한다

- 주요사항보고서와 정기보고서 주요정보를 명령 둘로 연다. 엔드포인트마다 명령을 두면 `disclosure` 태그가 50개 상한
  (`test_taxonomy_filters_are_selective`)을 넘고, 인자가 종류별로 완전히 같다.
- **라이브러리 메서드·클래스 이름은 2026-11-04 부터 엔드포인트와 일치한다** — `default_occurrence` 는 dfOcr(부도발생),
  `business_suspension` 은 bsnSp(영업정지), `exchangeable_bond_issuance_decision` 은 exbdIsDecsn(교환사채), 클래스는
  `MajorMattersReport`(주요사항보고서, DS005). 옛 이름(`real_estate_development`, `business_letter`,
  `corporate_bond_issuance_decision`, `MajorShareholderDisclosure` 등)은 `DeprecationWarning` 을 내는 별칭으로만 남아 있으니 새로
  쓰지 않는다. `handlers/dart.py` 의 `_MAJOR_EVENTS`·`_REPORT_ITEMS`(slug → 엔드포인트·한국어 이름·람다)가 그래도 진실의
  원천이다. `getattr(client, 이름)` 으로 바꾸지 않는다 — 이름이 오해를 부르고 Codacy 가 동적 호출로 잡는다.
  `test_dart_event_handlers_unit.py` 가 표의 모든 항목을 실제 client 의 `_get` 경로와 대조한다.
- 실데이터 검증(2026-10-17, 최근 12개월 주요사항보고 공시에서 종류별 표본, CLI 경유): 주요사항 33종은 행으로 확인.
  `split-merger` 는 표본 4건이 모두 013(자회사 공시로 보임), `overseas-delisting-decision`·`overseas-delisting` 은 표본이 없어
  **미검증**. 표본은 `[기재정정]` 을 빼고 고른다 — 정정 공시의 접수일로 조회하면 013 이 온다. report-item 26종은 대형주·소형주
  각 1곳의 2025 사업보고서로 확인. 10년 범위(2016–2026) 조회도 된다. 이 과정에서 라이브러리 모델 8종(유상·무상·유무상증자·
  감자·부도·영업정지·해산·자산양수도)의 숫자 필드와 감사의견 3필드를 실서버에 맞춰 고쳤다
  (`packages/cluefin-openapi/VENDOR_DOC_ERRATA.md` DART 절).
- `major-event` 의 `bgn_de`·`end_de` 는 필수다. 기본값이 있으면 "없음(013)" 과 "기간이 틀림" 을 구분할 수 없다. 달력 날짜·
  순서·20150101 이후를 클라이언트 생성 전에 검사해 exit 2. 계약 테스트가 이 검사에 걸려 클라이언트 대조를 건너뛰지 않도록
  `metadata._NAME_SAMPLES` 에 `_de` 접미사 샘플(`20250101`)이 있다.
- 출력은 다른 DART 명령처럼 패스스루에 `event`/`item`·`endpoint` 두 키만 얹는다. 013 은 오류가 아니다.
- 최대주주 현황(hyslrSttus)·주식의 총수(stockTotqySttus)는 `report-item` 에 넣지 않았다 — `dart major-shareholder`·
  `share-count` 가 연다.
- `dilution-watch` 는 `major-event` 를 종류별로 한 번씩 불러 `dilution.normalize_row` 로 공통 필드에 맞춘다(범위 결정
  2026-11-04). **자사주 소각**은 주요사항보고서가 아니라 정기보고서 `report-item treasury-stock` 이라 범위 밖이고 응답
  `not_covered` 에 적는다 — 조용히 빠뜨리지 않는다. 교환사채 모델에는 리픽싱 필드 자체가 없어 `refixing_floor` 는 CB·BW 만
  있다. `pct_of_shares` 분모는 `end_de` 이전에 접수된 가장 가까운 정기보고서의 보통주 발행주식총수이고, 못 찾으면(신규 상장 등)
  비율이 `null` 이다. `major-event` 와 달리 기간을 생략하면 최근 3년이다 — 한 번에 여러 번 부르는 명령이라 매번 날짜를 쓰게 하지
  않는다. 여러 번 부르는 핸들러라 `test_dart_handlers_unit.py` 의 `_PARSING_HANDLERS` 로 한 번 호출 검사에서 뺐다.

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
  곱하지 않는다(`dart financial-notes` 와 같은 계약). 주석 번호는 해마다 바뀐다(2026-11-04 실측: 같은 회사 Income Taxes 가
  13번 → 7번 → 6번) — 여러 해는 `note-series`.
- `financial-summary` 는 companyfacts 하나로 연간 표준 계정을 낸다(`sec_summary.py`, 표는 `accounts/us_gaap.toml`·
  `us_gaap_financial.toml`). DART 표와 달리 행 순서가 없어 **ids 순서가 우선순위**다 — 같은 계정을 회사마다 다른 개념으로
  내기 때문이다(표본 37개사 최근 10-K 에서 매출이 `Revenues` 15곳, `RevenueFromContract…` 13곳, 2026-11-10). 같은 기간은 가장
  늦게 제출된 값(재작성 반영). 금융 표는 marker 개념(은행·보험·증권만 내는 것)에 값이 있을 때만 붙는다 —
  `InterestIncomeExpenseNet` 은 일반 회사도 순이자비용으로 내서 marker 가 아니다(2026-11-10, 유통 1곳). 티커가 10-Q 만 낸 새
  지주회사 CIK 로 바뀐 회사는 10-K 연도가 없어 NotFound(힌트: 이전 CIK).
- `note-series` 는 최근 10-K(정정 제외) N편을 받아 `note_series.py` 로 잇는다. 해 잇기 규칙은 모듈 docstring 에 있고,
  여기는 고르게 된 이유만 적는다(2026-11-04 실측, 이커머스 1개사 10-K 5편):
  - 회계연도는 `dei:DocumentFiscalYearFocus` → 문서 기간말 → `report_date` 순. 같은 해가 두 편이면 최근 것만 쓰고
    `problems` 에 남긴다.
  - 값은 당해 열만. 당해 열은 머리 연도가 **기간말의 연도**인 열, 없으면 회계연도인 열이다. 1월에 회계연도가 끝나는 회사는
    머리가 "February 1, 2025"(기간말)이기도 "Fiscal 2024"(회계연도)이기도 해서 둘 다 보되, 기간말을 먼저 본다 —
    "February 1, 2025 | February 3, 2024" 표에서 회계연도(2024)는 전년 열에 맞기 때문이다.
  - 머리에 연도가 없는 표는 값 열 전부를 당해로 본다(만기표·가정표). 당해 열이 없는 표(옛 서식이 전년 값만 남은 경우)는
    `skipped_tables`. 대시는 0, 빈 칸은 값 없음.
  - 한 표가 셋으로 갈라진 경우(세그먼트 표)는 하나만 이어진다. 구역 머리("Current taxes")가 같은 이름의 행을 가르고, 구역
    머리가 새로 붙어도("Differences resulting from:") 구역을 뺀 이름이 표 안에 하나뿐이면 잇는다.
  - `restated` 는 차이가 거친 단위의 한 단위 미만이면 달지 않는다. 반 단위로 두면 천 달러 → 백만 달러 반올림(28,513 →
    28, 합계를 맞추려 내림)이 재작성으로 잡혀 5편에서 오탐 5건이 났다. 남은 4건은 세율 조정표 "Other"·"Other
    nondeductible expense" 재분류였다.
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
- `industry-outlook` 도 계산 명령이다(`industry.py`, `macro.py` 의 함수를 재사용). 제조업 중분류(KSIC C10~C33) 표가 진실의
  원천이고 2026-11-03 실서버로 확인했다 — 통계표마다 그룹 순서가 반대이고 업종 코드 글자가 KSIC 순서를 따르지 않는 것은 모듈
  docstring 에 있다. 코드를 더할 때 글자 순서를 가정하지 않고, 품목코드가 없는 업종은 비슷한 품목으로 대신 채우지 않는다
  (`missing`). 재고순환은 부호와 차이값만 내고 국면 이름(회복/확장/하강/수축)은 주지 않는다(macro-snapshot 과 같은 결정).
  `induty_code` 는 DART 기업개황 값 그대로 받고 앞 두 자리만 쓴다 — 제조업이 아니면(10~33 밖) exit 2 다.
- **ECOS 레이트리밋은 3분 300회**(`ERROR-602`, 2026-11-03 실측: 24개 업종 전수 조회 중 ~190여 회 만에 걸림)고 30분 뒤 풀린다
  (실측). `macro-snapshot`(~15회) 하나, `industry-outlook`(~8회) 하나는 문제없지만, 여러 업종·여러 종목에 `industry-outlook`
  을 반복 호출하거나(`test_ecos_integration.py` 의 `slow` 전수 테스트가 그 경우) 다른 ECOS 호출과 짧은 시간에 합쳐지면
  걸릴 수 있다. 걸리면 `EcosRateLimitError`(exit 5, retryable) 로 그대로 올라오고 — 재시도 전 30분을 기다린다.

## Tests that break on unrelated-looking changes

- `test_rpc_registry_unit.py` hardcodes the total command count — bump it when adding or removing any handler. It is
  the only place; `test_agent_surface_unit.py` reads the registry length.
- A domain/tag used in `COMMAND_TAXONOMY` must also exist in `_DOMAIN_TAXONOMY`/`_TAG_TAXONOMY` or the
  taxonomy-coverage test fails.
- `test_taxonomy_filters_are_selective` puts a floor under filter precision (≥110 distinct `(domains, tags)`
  signatures, no tag on more than 50 commands). Retagging that collapses commands back into one bucket fails it.
- Recipe → command references are validated only by a test, not at runtime; renaming a command path silently breaks
  recipes until tests run.
- `test_cli_contract_unit.py` runs every `uv run cluefin-openapi-cli` line inside a fenced block of README.md and
  this file: discovery meta commands as written, broker commands with `--dry-run` appended. `cache`, `audit` and
  `review` lines are only checked for a real subcommand (`LOCAL_STATE`) because they read local files, call brokers
  themselves or ignore `--dry-run`. An example outside a fenced block fails the test. The README exit-code table is
  compared with `errors.EXIT_CODES`.
- A new meta command must go into that file's `META` (runs offline as written) or `LOCAL_STATE`;
  `test_every_meta_command_is_classified` fails otherwise. Until 2026-11-15 the block parser lost its place after the
  first non-`bash` fence and checked one README command out of 86 — keep `_doc_commands` line-based.
- `test_readme_smoke_unit.py` requires both docs to keep explaining `primary`/`auxiliary`/`kis_alternatives`,
  `--dry-run`, `--fields`, `brokers --json` and `retryable`, and to stay free of two retired names (the old skill
  file and the CLI that desk absorbed — the test spells them). It pins words, not sentences.
- `list` is **brief** by default (`_command_brief`); tests and agents that need parameters must use `--full` or
  `schema`. An **unfiltered** `list --full` is capped at 25 rows (`_UNFILTERED_FULL_LIMIT`) and reports
  `count`/`returned`/`truncated`; `--limit 0` restores every row. It truncates rather than refuses because the
  discovery smoke test requires it to exit 0.

## search is a ranker, `list --query` is a filter

- These are deliberately separate primitives. `test_agent_surface_unit.py` asserts that
  `list --full --query "theme group"` returns **only** matching names — redirecting `--query` into the scorer breaks
  that by construction.
- The corpus is 100% English, so Hangul never enters the index. Korean reaches it only through
  `metadata.QUERY_ALIASES` expansion, and alias values are run through the same `tokenize()` as documents — the
  stemmer turns `-ies` into `-y`, so a raw `securities` would otherwise never match the indexed `security`.
  `test_search_unit.py` fails on any alias expansion that reaches nothing.
- The BM25F index is cached on the **registry object identity**; `set_registry_provider` swaps registries between
  tests and an unkeyed cache would serve a stale index.
