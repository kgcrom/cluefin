# AGENTS.md — cluefin-openapi

Non-obvious constraints only; see the root AGENTS.md for repo-wide rules.

## Dangerous integration tests

- Running the full `integration` suite with `KIWOOM_ENV=prod` **submits live market
  orders** (the domestic order tests use market-order type `trde_tp="3"`) and `ust31302`
  executes a **real currency exchange**. Run only read-only tests against prod.
- KIS debug artifacts (`/tmp/cluefin-kis-debug/*.json`) are written with unredacted raw
  response bodies on every integration response — `KIS_DEBUG_ON_FAILURE` only gates
  *printing*, not the file write.
- `_sanitize_request_context` (`_http_base.py`) is the only redaction layer for request
  context in exceptions/logs: it strips headers but keeps `params`/`body` as-is, so
  never put secrets in params/body context.

## Response models

- **Never put `max_length` (or any length constraint) on a response model.** The portal
  docs state field lengths, but the live servers exceed them (2026-09-02: a Kiwoom ka90001
  theme name over 20 chars made pydantic reject the *whole* response with
  `string_too_long`, blanking the desk theme screen). A constraint on a response can only
  reject good data; `tests/test_response_models_unit.py` fails if one comes back.
  `json_schema_extra` metadata is fine — it doesn't validate.
- **DART 응답 본문은 `DartHttpBody.parse()` 가 채우는 `result` 안에만 있다.** 모델
  최상위에 `list` 같은 필드를 선언해도 parse() 는 건드리지 않아 항상 기본값(빈 리스트)이
  남고, 읽는 쪽은 예외 없이 0건을 받는다. `UniqueNumber` 가 실제로 그랬다 — 실서버는
  119,313행을 돌려주는데 CLI 는 빈 목록을 내보내고 있었다. 행은 `result.list` 로 읽는다.

- **`validate_kis_response` 는 로그를 남기지 않고 `KISValidationError` 만 던진다.** 원문은
  예외의 `response_data` 에 실려 있다. 같은 내용을 `logger.error` 로도 찍으면 호출부가 예외를
  잡아 처리해도 에러 로그가 남고, 계좌 모듈로 넓히면 원문 속 계좌번호가 로그에 남는다
  (2026-09-20 결정). 다른 KIS 모듈로 넓힐 때도 로그를 다시 넣지 말 것.

## Broker server behavior the code can't show

- KIS may invalidate tokens before their stated 24h expiry — `MAX_CACHE_AGE=6h` in the
  token manager is deliberate. KIS also rate-limits token generation to 1/min server-side.
- Kiwoom can return HTTP 200 with a failing body `return_code`; the `_post` wrapper
  resolves body codes before HTTP status. Never assume 200 == success.
- WebSocket auth differs per broker: KIS needs a separate `approval_key` from
  `Auth.approve()`, while Kiwoom reuses the plain access token. Don't assume symmetry.
- Kiwoom's mock (`dev`) domestic WebSocket supports KRX only.
- Mixed dev/prod tokens are rejected server-side (Kiwoom `8031`, KIS `EGW00123`) — this
  is why token caches are scoped by env/app_key.
- Kiwoom occasionally removes TRs from its official docs while the API keeps working
  (e.g. ka10009), but a `1504:해당 URI에서는 지원하는 API ID가 아닙니다` means the TR is gone
  from the server too (ka10087·ka10098, 2026-09-23). Check the docs list before debugging code.
- **Broker doc ≠ live server cases live in `VENDOR_DOC_ERRATA.md`** (KIS and Kiwoom: misnamed blocks and
  fields, fields the server omits or adds, wrong lengths, and server behavior the docs don't mention).
  Code follows the live server; check that file before "fixing" a model back to the docs, and add a row
  when you measure a new divergence.
- Integration tests compare the raw response with the model exactly — KIS `tests/kis/_response_shape.py`
  (TS `assertKisResponseShapeDeep`), Kiwoom `tests/kiwoom/_spec_conformance.py` (TS
  `assertKiwoomSpecConformance`), which also checks request/response lengths against
  `tests/kiwoom/spec_lengths.json` (a dump of the portal's Length column, shared by both languages).
  A divergence already measured goes in the call's `ignore`/`ignore_length` with a comment pointing
  at the errata — don't loosen the helpers. An empty block passes vacuously and only warns
  (`EmptyBlockWarning`); run with `-W always::UserWarning` to see which ones.
- **Kiwoom returns an empty result instead of an error for most bad inputs**, so a wrong request
  passes a shape-only test. Found in the 2026-09-27 audit: `KRX:069500` (the `KRX:` in the stock-code
  description is a format example, not a prefix), a date sent to a period field (`dt`: `5:5일…`),
  positional args in the wrong order, non-doc codes like `'0'`. Use the portal's request example values.
- The gitignored `CLAUDE.local.md` records the working procedure for scraping the
  official KIS/Kiwoom doc portals (Kiwoom's POST doc endpoints are blocked by AhnLab
  Eversafe; only GET works). Read it before re-deriving that. Kiwoom's contents URL is now
  path-style `/guide/apiGuideContents/{jobTpCode}/{apiId}` (the query-string form returns a page with no TR list).
  Save dumps with case-distinct filenames — realtime TRs `0g`/`0G`, `0u`/`0U` collide on macOS APFS.

## NH PLUG (nhplug)

- Token issuance (`/oauth2/token`) is **live-domain only** (no mock endpoint), rate-limited
  to 1/sec server-side, and every unnecessary re-issue triggers a security alert on the
  account — always go through `Auth.generate()` (TokenManager cache), never call the raw
  endpoint in loops or retries. On 429, retry with the SAME token.
- One token serves both live (`api.nhplug.com`) and mock (`moapi.nhplug.com`) calls, which
  is why the nhplug token cache is scoped by app_key only (no env) — don't "fix" it to
  match kis/kiwoom.
- nhplug's `TokenManager` deliberately has no `MAX_CACHE_AGE` (no early server-side
  invalidation) and computes expiry from `cached_at + expires_in`.
- All 시세 APIs (`/krstock/quote/*`, `/gbstock/quote/*`) are **live-domain only**. moapi rejects
  them with `IGW40023`, or for gbstock `IGW40019 "종목코드(iem_cd)를 확인해주세요"` — a misleading
  message that means "not provided on mock", not a bad code. Their integration tests only run
  with `NHPLUG_ENV=prod`; run **only the quote files** that way — the order tests would place
  real orders.
- A failing body `rsp_cd` goes through one function, `_exceptions.raise_for_rsp_cd`: known codes
  map to `NHPlugNoDataError` (empty result — **not** a request error), `NHPlugMockUnsupportedError`
  and `NHPlugNotBusinessDayError`, all subclasses of `NHPlugAPIError`. Add a newly observed code to
  the matching `*_RSP_CODES` tuple, and mirror it in TS `nhplug/client.ts`.
- NH PLUG doc ≠ live server cases (spec field names off by one, fields the server omits, `"1E"`
  sign codes, `iem_nm` instead of `kor_name`, strict request types) are in `VENDOR_DOC_ERRATA.md`.
- NH PLUG integration tests check raw keys and spec lengths with `assert_matches_spec`
  (`tests/nhplug/_response_shape.py`, TS `assertNhplugMatchesSpec`). Every model is
  `extra="allow"`, so without it undeclared fields vanish into `model_extra` silently. Lengths
  come from the spec snapshot `tests/nhplug/spec_lengths.json`; a confirmed over-length goes in
  its `known_exceed` (shared with TS), a key the server omits in the call's `ignore` —
  `mock_omits(...)` when only moapi omits it, so a prod run still checks it.
- The WebSocket needs the path `/websocket` (`host:port` alone never upgrades), and the
  notification channels (`d0`·`d1`·`d2`·`d3`…) are on :7070 even for gbstock — :7080 is quotes only.
- The portal spec backend is KIS-portal-style JSON: `/api/apis/public/api-list/{groupId}`
  → `/api/apis/guide/tr/{apiId}` → `/api/apis/guide/tr/property/{trId}` (no auth needed).
  Asset-class specs are also public at `https://www.nhplug.com/openapi-docs/<slug>/openapi.json`
  (the declared source of truth; slugs: common·krstock·gbstock·krfuture·gbfuture·krbond·krgold).

## SEC EDGAR (sec)

- No API key: SEC identifies callers by the User-Agent ("Name email"), from `SEC_USER_AGENT` in `.env`.
  Per SEC's access policy, an undeclared agent **and** a client over 10 req/s both get **403**, not 429, and the
  over-rate block lasts about 10 minutes. That is why 403 is never retried and the default is 8 req/s.
- `Client._request` only accepts `https://www.sec.gov` and `https://data.sec.gov` URLs, and every value that goes
  into a URL path passes `_ids.py` (CIK, accession number, single path segment). Keep it that way when adding
  endpoints — EFTS full-text search (`efts.sec.gov`) would need the allow-list widened on purpose.
- SEC integration tests read `SEC_USER_AGENT` with `dotenv_values` (`tests/sec/_env.py`), never `load_dotenv`:
  `.env` is the broker **prod** pair, and loading it would leak `KIS_ENV=prod` etc. into every later test.
- `submissions.filings.recent` is column arrays (one list per field), at least 1,000 filings or one year;
  the rest is in `filings.files` pages. `FilingEntry` declares every live column — the integration test fails
  when SEC adds one, so declare it rather than relaxing the test.
- companyfacts/companyconcept repeat the same period's value once per filing that reported it (original,
  next year's comparative, amendments). `fy`/`fp` describe the **filing**, not the value's period; only one row
  per period carries `frame`. Pick rows by `start`/`end`/`accn`, not by `fy`.

## Kiwoom scope

- Kiwoom US-stock (overseas) support is **Python-only**; the sibling `cluefin-openapi-ts`
  package's `overseas-*` files are KIS, not Kiwoom.

## Conventions that are easy to mis-infer

- The three `TokenManager` classes (kis/kiwoom/nhplug) are copy-pasted, not shared —
  mirror cache-behavior changes by hand in all three. The sibling `cluefin-openapi-ts`
  package's `token-cache.ts` per broker also mirrors each `_cache_file_name`/cache JSON
  shape to share the same cache files — mirror changes there too, by hand.
- Unit-test styles are per-broker and not interchangeable: Kiwoom uses the table-driven
  `EndpointCase`/`run_post_case` harness (`tests/kiwoom/_helpers.py`), KIS uses JSON
  fixture case files (`tests/kis/*_cases.json`).
- Integration skip helpers encode different meanings: `real_account_only` = permanently
  unsupported on mock; `skip_if_env_blocked` = transient account/market state. Mixing
  them up masks real regressions.
- `.env.test` must be loaded at module import (collection) time, not inside a fixture —
  module-level `skipif`s read `KIWOOM_ENV` during collection.
- Both integration suites add an autouse `time.sleep(1)` between tests on top of the
  in-client rate limiter; the limiter alone is not enough against live throttling.
- `examples/*.ipynb` 노트북은 커밋 전에 output·execution_count 를 지운다 (출력에 계좌번호가
  섞인다). 워크스페이스 루트에서:
  `uv run --with jupyter jupyter nbconvert --clear-output --inplace packages/cluefin-openapi/examples/<노트북>.ipynb`
