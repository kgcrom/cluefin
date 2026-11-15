# AGENTS.md — cluefin-openapi

Non-obvious constraints only; the root `AGENTS.md` and `packages/AGENTS.md` hold the repo-wide rules.

- **Vendor doc ≠ live server cases live in `VENDOR_DOC_ERRATA.md`** (misnamed blocks and fields, fields the server
  omits or adds, wrong lengths, undocumented server and mock behavior, each with its measured date). Code follows the
  live server: read that file before "fixing" a model back to the docs, and add a row when you measure a new one.
- The gitignored `CLAUDE.local.md` in this folder has the working procedure for scraping the KIS, Kiwoom and NH PLUG
  doc portals. Read it before re-deriving that.

## Environments and accounts

- `.env.test` is dev (mock) for **Kiwoom and NH PLUG only; its KIS side is `KIS_ENV=prod`**, a real account. The KIS
  integration suite is quotes and analysis today, with no account or order call. Check that a new KIS integration
  test is read-only before adding it; anything that places an order needs the `mutation` gate below.
- **Default `env` is not the same across classes.** Every `Auth` defaults to `dev` (NH PLUG `Auth` has no env), while
  KIS and NH PLUG `HttpClient`, both `SocketClient`s and `KiwoomWebSocketClient` default to `prod` (the Kiwoom one
  also to `market="overseas"`). Kiwoom `Client` has no default. A token from `Auth(...)` passed to `HttpClient(...)`
  without `env` is a dev token sent to prod. Pass `env` to both, as `BrokerClientFactory` does:

  ```python
  auth = Auth(app_key=key, secret_key=SecretStr(secret), env="dev")
  client = HttpClient(token=auth.generate().get_token(), app_key=key, secret_key=secret, env="dev")
  ```

- **A Kiwoom dev failure at authentication is usually the account, not the code.** Expired mock keys make token
  issuance return a 200 body without a token, which surfaces as a pydantic `ValidationError` on `TokenResponse`;
  an expired mock account answers orders with `RC4091`. Domestic and US mock accounts are applied for and expire
  separately. Codes and how to tell them apart: errata, "모의투자(dev) 서버". Ask for re-issued keys before debugging.
- NH PLUG 시세 (`/krstock/quote/*`, `/gbstock/quote/*`) and WebSocket quote channels are **live-domain only**, so their
  integration tests run only with `NHPLUG_ENV=prod` (same keys, read-only calls). moapi's refusal for gbstock is
  `IGW40019 "종목코드(iem_cd)를 확인해주세요"`, which means "not provided on mock", not a bad code.
- The account numbers in nhplug unit fixtures (`20101036881`, `50051036881`, `cust_no` `100805701`) are the example
  values published in the vendor spec, not a real account. Don't scrub them or report them as leaked secrets.

## Dangerous integration tests

- Tests that place orders or exchange currency (Kiwoom domestic/US orders, `ust31302`) are marked
  `mutation` and run **only when `-m` names `mutation`**; with `KIWOOM_ENV=prod` they also need
  `CLUEFIN_TEST_LIVE_MUTATION=1` in the shell (the gate is `pytest_collection_modifyitems` in
  `tests/kiwoom/conftest.py`, so even the order-placing fixture is skipped). Keep that flag out of
  `pyproject.toml` and `.env*` — a saved flag would let the next run trade unnoticed. Orders are
  unfillable limit orders that teardown cancels; a teardown failure is an ERROR that lists the order
  numbers left behind — cancel those by hand. `ust31302` executes a **real currency exchange** on prod.
- NH PLUG has no order integration tests (order modules are unit-tested only).
- `realtime` tests run only with `-m "integration and realtime"` and inside market hours: KRX stocks
  09:00–15:20 KST (after 15:20 is the closing auction, no trades), KIS bonds 09:00–15:30 KST, US
  09:30–16:00 New York. The gates are fixtures in `tests/conftest.py` (`krx_continuous_hours`,
  `kst_market_hours`, `us_market_hours`) applied with `pytest.mark.usefixtures`, listed **before** any
  fixture that authenticates — autouse fixtures run before `usefixtures`, so an autouse auth check
  would hit the network off-hours. During those hours a liquid stock that sends nothing within 30s is a
  failure, not a skip; thinly traded bonds skip. The gates know weekdays, not holidays: on a market holiday
  those tests fail.
- **No broker's WebSocket rejects a bad subscription**, so a subscribe/ack check proves nothing —
  **assert on received data.** KIS, Kiwoom and NH PLUG live all acknowledge an unknown code (errata, each broker's
  "서버 동작"). The KIS Python client also emits `subscribed` right after sending, not on the server reply. NH PLUG's
  mock socket is the exception that does refuse — quote channels get `WSS10006`, so NH realtime tests are live-only.
- Kiwoom packs several realtime types into one REAL frame, so `DomesticRealtime.parse`/`OverseasRealtime.parse`
  return a list with one model per type. Don't go back to picking the model from `data[0]` — the other type's
  values silently become empty strings.
- A KIS app key allows **one WebSocket session at a time**, and each `Auth.approve()` call voids the keys issued
  before it (`OPSP8996`/`OPSP0011`, errata). So KIS realtime tests fail when anything else uses the same app key at
  the same time: another pytest or TS run, desk, a script. `SocketClient` reports these replies as `error` events
  and names them in the next "not connected" error.
- **KIS `HttpClient` writes every response it receives, unredacted, to `<tempfile.gettempdir()>/cluefin-kis-debug/*.json`**
  (`$TMPDIR` on macOS, not `/tmp`) — in any process, not only in tests, and nothing deletes them.
  `KIS_DEBUG_ON_FAILURE` only gates *printing* the last one when an integration test fails.
- `_sanitize_request_context` (`_http_base.py`) is the only redaction layer for request
  context in exceptions/logs: it strips headers but keeps `params`/`body` as-is, so
  never put secrets in params/body context.
- Revoking a token forces a re-issue for every process sharing the cache, so the revoke tests run only with
  `KIS_TEST_REVOKE=1` / `NHPLUG_TEST_REVOKE=1`.

## Token cache

Python and `cluefin-openapi-ts` read and write the **same cache files**, so everything here is mirrored by hand in
TS `src/<broker>/token-cache.ts` and `core/token-file.ts`.

- The three `TokenManager` classes (kis/kiwoom/nhplug) are copy-pasted, not shared — a cache-behavior change goes
  into all three and into TS.
- File: `<tempfile.gettempdir()>/cluefin-openapi/.<broker>_token_cache_<env>_<sha256(app_key)[:8]>.json`
  (`cache_dir=` on `Auth`, `CLUEFIN_OPENAPI_CACHE_DIR` through the factory), body `{"token": {...}, "cached_at": ...}`.
  KIS and Kiwoom scope by env and app key because mixed dev/prod tokens are rejected server-side (Kiwoom `8031`,
  KIS `EGW00123`). nhplug scopes by app key only: one token serves live and mock — don't "fix" it to match.
- Lifetime: KIS and Kiwoom re-issue once the cache is older than `MAX_CACHE_AGE=6h` or within 1 h of expiry. The 6 h
  is deliberate — KIS may invalidate tokens before their stated 24 h. nhplug deliberately has no max age (no early
  invalidation, and every needless re-issue raises a security alert on the account) and computes expiry from
  `cached_at + expires_in`.
- **`cached_at` is naive local time** in both languages (`datetime.now().isoformat()`, TS `localIsoNow`). Never
  write an offset or a `Z` suffix: both sides compare it with a naive "now".
- Issuance is throttled server-side: KIS 1/min (`EGW00133` → `KISRateLimitError`, not a key error), NH PLUG 1/sec on
  the **live domain only** (there is no mock token endpoint). Always go through `Auth.generate()`; never call the raw
  endpoint in loops or retries. Retries (429, 5xx, timeout — the shared `_execute_with_retry`, order POSTs included)
  reuse the SAME token.
- Only NH PLUG `Auth.revoke()` clears the cache. KIS `revoke()` and Kiwoom `revoke_token()` leave the dead token in
  the file; call `token_manager.clear_cache()` after them.

## Response models

- **Never put `max_length` (or any length constraint) on a response model.** The portal
  docs state field lengths, but the live servers exceed them (2026-09-02: a Kiwoom ka90001
  theme name over 20 chars made pydantic reject the *whole* response with
  `string_too_long`, blanking the desk theme screen). A constraint on a response can only
  reject good data; `tests/test_response_models_unit.py` fails if one comes back.
  `json_schema_extra` metadata is fine — it doesn't validate.
- **Integration tests compare the raw response with the model exactly** (keys, and lengths against the
  `spec_lengths.json` snapshots shared with TS). A divergence already measured goes in that call's
  `ignore`/`ignore_length` — NH PLUG: `known_exceed` in the snapshot, and `mock_omits(...)` when only moapi omits the
  key, so a prod run still checks it — with a comment pointing at the errata. Don't loosen the helpers. Every nhplug
  model is `extra="allow"`, so without the check undeclared fields vanish into `model_extra` silently. An empty
  block passes vacuously and only warns (`EmptyBlockWarning`); run with `-W always::UserWarning` to see which.
- **A shape-only test passes on a wrong request**: Kiwoom answers most bad inputs with an empty result, not an
  error (errata, "문서 표기 함정"). Use the portal's request example values and assert that rows came back.
- **DART 응답 본문은 `DartHttpBody.parse()` 가 채우는 `result` 안에만 있다.** 모델
  최상위에 `list` 같은 필드를 선언해도 parse() 는 건드리지 않아 항상 기본값(빈 리스트)이
  남고, 읽는 쪽은 예외 없이 0건을 받는다. `UniqueNumber` 가 실제로 그랬다 — 실서버는
  119,313행을 돌려주는데 CLI 는 빈 목록을 내보내고 있었다. 행은 `result.list` 로 읽는다.
- **`validate_kis_response` 는 로그를 남기지 않고 `KISValidationError` 만 던진다.** 원문은
  예외의 `response_data` 에 실려 있다. 같은 내용을 `logger.error` 로도 찍으면 호출부가 예외를
  잡아 처리해도 에러 로그가 남고, 계좌 모듈로 넓히면 원문 속 계좌번호가 로그에 남는다
  (2026-09-20 결정). 다른 KIS 모듈로 넓힐 때도 로그를 다시 넣지 말 것.

## KIS and Kiwoom

- Never assume HTTP 200 == success. KIS can return 200 with a failing body `rt_cd`; every service module checks it
  with `_exceptions.raise_for_rt_cd`, which raises `KISResponseError` (a `KISAPIError` **and** a `ValueError` —
  these were plain `ValueError` before, keep the base for callers) carrying only `rt_cd`/`msg_cd`/`msg1`. Don't add
  a per-module check again. Kiwoom's `_post` wrapper resolves the body `return_code` before the HTTP status.
- A bad KIS key fails at token issuance with HTTP 403 `EGW00103` (AppKey) — `Auth` raises `KISAuthenticationError`.
- WebSocket auth differs per broker: KIS needs a separate `approval_key` from `Auth.approve()`, Kiwoom reuses the
  plain access token, NH PLUG puts the access token in each subscribe message. Don't assume symmetry.
- Kiwoom continuation reads **only the `cont-yn` request header**; `cond-yn`/`con-yn` (typos in the vendor docs)
  silently return page one again. A unit test fails if a misspelled header comes back into the source.
- **KIS 국내주식 종목분석 7 endpoints** (balance sheet, income statement, financial/profit/other/stability/growth
  ratios) were removed in 1.1.0 because KIS blocked them on 2026-11-11 (data licence). Don't add them back; the same
  figures come from DART.
- Kiwoom US-stock (overseas) support is **Python-only**; the sibling `cluefin-openapi-ts` package's `overseas-*`
  files are KIS, not Kiwoom.

## DART

- A bad key comes as HTTP 200 with body `status` 010/011/012/901 — JSON, or an error XML where a ZIP was expected.
  `Client._request` raises `DartAuthenticationError` for these so callers don't read it as "no data" or a corrupt ZIP.
- **`013` (no data) is a normal return**: `result.status == "013"` and `result.list is None`, no exception. An
  integration test that accepts `013` verifies nothing — a default query that always answered `013` hid four wrong
  models and paths until 2026-10-02. Query a real filing sample and assert `000`.
- `Client.major_matters_report` (주요사항보고서) was misnamed `major_shareholder_disclosure`. The old property, method
  and class names remain as `DeprecationWarning` aliases (2026-11-04) and the module file keeps the old name; don't
  add callers on the old names. 5% 대량보유 is `share_disclosure_comprehensive.large_holding_report`.
- `executive_major_shareholder_ownership_report` (`elestock.json`) rows carry the holding and its change only —
  **no trade date, buy/sell side or price.**
- `disclosure_document_file` extracts only the **first** XML of the ZIP. Audit reports attached to a periodic report
  need `disclosure_document_files` (main `<rcept_no>.xml` first, the rest by name).
- `download_financial_statement_xbrl` extracts entry by entry because pre-FY2023 ZIPs name their linkbases with `\`
  (errata); don't replace it with `extractall`.
- `get_multi_company_major_accounts` (`/api/fnlttMultiAcnt.json`, 다중회사 주요계정) takes up to **100 `corp_code`s
  at once** — a 101st makes the whole call fail with `status` `021` (`DartStatusCode.COMPANY_LIMIT_EXCEEDED`), not a
  partial result. Batch callers (e.g. a universe-wide cache load) must chunk corp codes into groups of 100.
- `fnlttMultiAcnt`/`fnlttSinglAcnt` 주요계정·주요지표 응답에는 **지배/비지배 구분이 없다** — 연결재무제표(`fs_div`
  없음, 전체 재무제표만 CFS/OFS 선택 가능)의 당기순이익·자본 합계가 지배주주 몫과 비지배주주 몫을 합친 값으로 온다.
  지주회사처럼 비지배 지분이 큰 종목은 이 값으로 계산한 PBR·ROE 등이 증권사가 쓰는 지배주주 기준 지표보다 낮게(또는
  다르게) 나온다. 지배주주 몫이 필요하면 전체 재무제표(`fnlttSinglAcntAll`)에서 "지배기업 소유주지분"/"비지배지분"
  계정을 직접 찾아 분리해야 한다.

## NH PLUG (nhplug)

- A failing body `rsp_cd` goes through one function, `_exceptions.raise_for_rsp_cd`: known codes
  map to `NHPlugNoDataError` (empty result — **not** a request error), `NHPlugMockUnsupportedError`
  and `NHPlugNotBusinessDayError`, all subclasses of `NHPlugAPIError`. Add a newly observed code to
  the matching `*_RSP_CODES` tuple, and mirror it in TS `nhplug/client.ts`.
- The success codes are a tuple too (`SUCCESS_RSP_CODES`): the docs say `00000` only, the servers add their own.
- WebSocket: the URL needs the path `/websocket`, and the notification channels (`d0`·`d1`·`d2`·`d3`…) are on :7070
  even for gbstock — :7080 is quotes only. US quotes are the free delayed `rc`/`rh`; real-time `RC`/`RH` need a paid
  quote agreement.

## SEC EDGAR (sec)

- No API key: SEC identifies callers by the User-Agent ("Name email"): `SEC_USER_AGENT` in `.env` at runtime
  (`BrokerClientFactory`), in `.env.test` for tests (`tests/sec/_env.py`, like every other integration suite).
  An undeclared agent gets **403** from both www.sec.gov and data.sec.gov (measured 2026-10-11 with
  `python-requests/…`; a browser-like agent still got 403 from www.sec.gov). The 403 page is titled "Request Rate
  Threshold Exceeded" even when the rate is fine — check the agent first. Per SEC's policy a client over 10 req/s
  also gets 403 (not 429) for about 10 minutes (not measured). Hence 403 is never retried and the default is 8 req/s.
- The agent check (`_validate_user_agent`: "@" after stripping) is duplicated in cluefin-xbrl's parser, which
  requires the same value before Arelle fetches SEC taxonomies (xbrl doesn't depend on openapi). Change both together.
- `Client._request` only accepts `https://www.sec.gov` and `https://data.sec.gov` URLs, and every value that goes
  into a URL path passes `_ids.py` (CIK, accession number, single path segment). Keep it that way when adding
  endpoints — EFTS full-text search (`efts.sec.gov`) would need the allow-list widened on purpose.
- `submissions.filings.recent` is column arrays (one list per field), at least 1,000 filings or one year;
  the rest is in `filings.files` pages. `FilingEntry` declares every live column — the integration test fails
  when SEC adds one, so declare it rather than relaxing the test.
- companyfacts/companyconcept repeat the same period's value once per filing that reported it (original,
  next year's comparative, amendments). `fy`/`fp` describe the **filing**, not the value's period; only one row
  per period carries `frame`. Pick rows by `start`/`end`/`accn`, not by `fy`.
- `values_as_of(rows, as_of)` picks, per period, the latest row with `filed < as_of`. Measured 2026-10-11 on ten
  companies' full companyfacts: `frame` sat on the latest-filed row in 54,336 of 54,337 multi-row periods, and its
  value differed from the original filing's in thousands (AAPL 333, GE 3,191), so choosing by `frame` leaks later
  restatements (KHC 2019, SMCI 2019, CELH 2023) and 8-K recasts (GE) into the past. `filed == as_of` is excluded
  because 16:00–17:30 ET acceptances keep that day's date (13 of 29 sampled). Same-day ties go to the higher
  accession sequence of the same filer prefix (SEC's `frame` agreed in 21/21 ties with different values); ties
  across prefixes were never seen and raise `ValueError`, as does one accession with two values for a period.
- `FilingEntry.acceptance_date_time` (`acceptanceDateTime`) ends in `Z` but is not always UTC. Against the filing
  header's `ACCEPTANCE-DATETIME` (Eastern), 20 of 29 10-K/10-Q were real UTC and 9 (every AAPL, KHC and SMCI one
  sampled) were Eastern shifted twice, 4–5 h late — AAPL 0000320193-23-000106: header 2023-11-02 18:08:27 ET,
  JSON `2023-11-03T02:08:27Z` (measured 2026-10-11). Nothing in the JSON tells them apart, so `values_as_of` uses
  `filed` only. `filed` is the header's `FILED AS OF DATE`: acceptance after 17:30 ET counts as the next business day.
- 13F folders hold the cover `primary_doc.xml` and **one** other XML, the information table, whose name is
  arbitrary and may end in upper-case `.XML` (2 of 518 measured 2026-10-12); 13F-NT has the cover only.
  `download_13f_files` picks by elimination and raises if two candidates appear. The submissions'
  `primaryDocument` is the XSL path `xslForm13F_X0n/primary_doc.xml`, not the raw file.
- **An Archives folder opens under any CIK**: another company's CIK with a valid accession number still returns
  200 (measured 2026-10-12), so the CIK in the path proves nothing. `filing_detail()` reads the filing's detail page
  (`<accession>-index.html`), whose `parties` are the real filer/issuer/reporting owner — check `ciks` there.
  It is also the only place with document types (EX-99.1 …; `index.json` has names only, and names are arbitrary).
  `-index-headers.html` (SGML header) would be easier to parse but is **404 before 2015** even though `index.json`
  lists it (AAPL filings, one per year, 2004–2014 404, 2015–2026 200); the detail page has the same layout back to
  2001. Inline XBRL rows link through the viewer (`/ix?doc=…`) and Form 4 lists the XSL rendering path too.
- Fails-to-Deliver is the SEC-side CUSIP → ticker source (13F tables carry no ticker; the 13(f) securities list
  has none either). Zip paths are **not** derivable: four folders by era (`fails-deliver-data`, `other/…`,
  `frequently-requested-foia-document-…`, `node/add/data_distribution`) and `_0` suffixes, so `files()` reads the
  list page's links (413, 2009-07a–2026-09a, no gaps or duplicates, measured 2026-10-12). The zip member sometimes
  lacks `.txt`. Format unchanged since 2009: `|`-separated, `.` for a missing price, two `Trailer …` lines whose
  record count is checked against the rows read (16 files across 2009–2026 matched).

## 한국은행 ECOS (ecos)

- **Errors come as HTTP 200 with `{"RESULT": {"CODE", "MESSAGE"}}`** for the sample key *and* a real key (measured
  2026-10-19: INFO-100/200, ERROR-100/101/200/301). Only an unknown service name gets HTTP 404 (an HTML page titled
  "503"). `INFO-200` (no data, also for an unknown stat code) becomes an empty page, not an exception; every other code
  goes through `_exceptions.raise_for_result` — add a newly seen code to `_RESULT_CODE_ERRORS`.
- The server cuts a query at 60 s with `ERROR-400`, so the default client timeout is 75 s. Below 60 s the client times
  out first and resends the same oversized query `max_retries` times instead of surfacing `EcosQueryTimeoutError`.
  Only `ERROR-600`/`602` are retried (`RETRYABLE_RESULT_CODES`); they come in a 200 body, so the HTTP 429/5xx retry
  never sees them. 400 and 601 fail the same way again.
- **ERROR-301 means three things**: a non-integer row count, start > end, and the `sample` key asking for more than 10
  rows. Only the message tail tells them apart, so `EcosSampleLimitError` is chosen by "sample" in the message and is a
  subclass of `EcosRequestError` (a reworded message just falls back to the parent).
- **The key is a URL path segment.** `request_context["path"]` shows it as `***`, and network/timeout errors are re-raised
  with the key replaced and the cause chain cut (`requests` puts the full URL in its message). Never log the URL.
- Page size is 10 for `sample` (`1/10`, `11/20`, … paging works) and 1000 for a real key. The real key actually has no row
  cap (`1/100000` returned all 5,184 rows) — 1000 follows the docs. `max_pages` stops a runaway loop with an error rather
  than returning a truncated list.
- The portal's spec page is a JS SPA whose data comes from `POST /api/serviceEndpoint/httpService/request.json`
  (`trxCd` `OSUOA03R01` services, `OSUOA04R01` fields with `srchCndYn` Y/N, `OSUOA05R01` messages) and matches the
  downloadable `.xls` specs. The xls `StatisticSearch` example (`200Y001/A/2015/2021`) returns INFO-200; use the web one
  (`200Y101/A/2020/2023/10101`).
- Field types are mixed: `list_total_count`/`DATA_CNT`/`row_count` are numbers, `DATA_VALUE`/`TIME`/`LVL` strings, and
  `WGT` came as `"1000"` — row models use `coerce_numbers_to_str`. `KeyStatisticList` adds an undocumented `row_count`
  and its row order is not stable between calls.

### Finding a series (what the catalog won't tell you up front)

- Start from the table, not a keyword: `table_list()` is 844 rows, 617 of them queryable (`SRCH_YN=Y`), and names
  repeat across tables (e.g. M2 is split by 평잔/말잔 × 원계열/계절조정 into separate tables). For markets, most
  questions land on a handful of tables: `817Y002` (all daily market rates: KTB curve, CD/CP, KOFR, corp bonds),
  `722Y001` (base rate), `121Y006`/`121Y015` (bank lending rates, new vs. outstanding), `802Y001` (daily KOSPI/KOSDAQ,
  foreign net buying, market cap), `901Y014` (monthly PER/dividend yield), `901Y054`–`901Y056` (delinquency, investor
  flows, deposits/margin loans). README has the item codes, measured 2026-10-20.
- `item_list()` returns **one row per item × cycle** (`722Y001`'s base rate appears four times, D/M/Q/A). The cycle you
  pass must be one the item has, or you get INFO-200 (empty), not an error.
- Some tables have **two item groups** (`901Y054`: loan type × bank group, `901Y055`: investor × volume/value). Pass the
  codes in group order; omitting the second returns every group-2 item (`["MO3AB"]` alone gave 3 bank groups per month). The group-2 item carries the unit (`VA` = 백만원),
  the group-1 item shows `unit_name=None`.
- Spreads (term spread, credit spread) are **not** series — fetch both legs and subtract on matched dates.
- Units differ per table and are only in `unit_name` (원, 억원, 십억원, 백만원; 연% vs %). Never assume.
- Monthly/quarterly series lag by 1–3 months (on 2026-10-20: lending rates/M2 ended 2026-08, delinquency 2026-07,
  household credit 2026Q2). A "latest value" query with a tight window returns INFO-200 → empty, which looks like a bug
  but isn't; widen the window.

## Release

- Publishing is `gh workflow run publish-openapi.yml -f bump=micro|minor|major` on `main`. The workflow **bumps the
  version itself** from the value in `pyproject.toml`, runs the unit tests, builds, publishes to PyPI (Trusted
  Publishing, environment `development`), then commits `release(openapi): vX.Y.Z`, tags `cluefin-openapi/vX.Y.Z`,
  pushes `main` and starts CI. It checks `uv lock --check` before bumping, so the lock must already be current.
- So **don't bump the version in a PR** — the workflow bumps on top of it. As of 2026-11-15 `pyproject.toml` says
  1.1.0 (bumped by hand with the KIS endpoint removal) while the last release and tag are `cluefin-openapi/v1.0.0`:
  the next dispatch would publish 1.1.1, 1.2.0 or 2.0.0, and 1.1.0 would never exist on PyPI. To ship that change as
  1.1.0, set `pyproject.toml` and `uv.lock` back to 1.0.0 first and dispatch `minor`.
- PyPI upload comes before the commit and tag push. Don't merge into `main` while the workflow runs: a rejected
  push leaves a published version with no release commit or tag.
- README.md is the PyPI long description: no repo-relative links, and every example must run after
  `pip install cluefin-openapi` alone (`python-dotenv` is a dev dependency, not a runtime one).

## Conventions that are easy to mis-infer

- `_atomic_file` imports `fcntl`, and `import cluefin_openapi` reaches it through the token managers: the package
  imports on macOS and Linux only.
- The response wrappers differ: Kiwoom `KiwoomHttpResponse.headers`, KIS and NH PLUG `.header`, DART `.result`.
- Unit-test styles are per-broker and not interchangeable: Kiwoom uses the table-driven
  `EndpointCase`/`run_post_case` harness (`tests/kiwoom/_helpers.py`), KIS uses JSON
  fixture case files (`tests/kis/*_cases.json`).
- Integration skip helpers encode different meanings: `real_account_only` = permanently
  unsupported on mock; `skip_if_env_blocked` = transient account/market state. Mixing
  them up masks real regressions.
- `.env.test` must be loaded at module import (collection) time, not inside a fixture —
  module-level `skipif`s read `KIWOOM_ENV` during collection.
- The kis, kiwoom and nhplug integration suites each add an autouse `time.sleep(1)` between tests on top of the
  in-client rate limiter; the limiter alone is not enough against live throttling.
