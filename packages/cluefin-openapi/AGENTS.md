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
  (e.g. ka10009). On integration failures, check the docs list before debugging code.
- The gitignored `CLAUDE.local.md` records the working procedure for scraping the
  official KIS/Kiwoom doc portals (Kiwoom's POST doc endpoints are blocked by AhnLab
  Eversafe; only GET works). Read it before re-deriving that.

## NH PLUG (nhplug)

- Token issuance (`/oauth2/token`) is **live-domain only** (no mock endpoint), rate-limited
  to 1/sec server-side, and every unnecessary re-issue triggers a security alert on the
  account — always go through `Auth.generate()` (TokenManager cache), never call the raw
  endpoint in loops or retries. On 429, retry with the SAME token.
- One token serves both live (`api.nhplug.com`) and mock (`moapi.nhplug.com`) calls, which
  is why the nhplug token cache is scoped by app_key only (no env) — don't "fix" it to
  match kis/kiwoom.
- `TokenManager` is now a **third** copy (kis/kiwoom/nhplug) — mirror cache-behavior
  changes by hand in all three. nhplug deliberately has no `MAX_CACHE_AGE` (no early
  server-side invalidation) and computes expiry from `cached_at + expires_in`.
- All four gbstock 시세 APIs (`/gbstock/quote/v1/*`) are **live-domain only**. moapi rejects
  `current` with `IGW40019 "종목코드(iem_cd)를 확인해주세요"` for every ticker format —
  a misleading message that means "not provided on mock", not a bad code (2026-08-22 실측).
- gbstock quote responses return the stock name as `iem_nm`, while the spec declares
  `kor_name` (`current`, `period`) / `hts_kor_isnm` (`symbolIndexFxPeriod`). Both are
  modelled; read `iem_nm`.
- The portal spec backend is KIS-portal-style JSON: `/api/apis/public/api-list/{groupId}`
  → `/api/apis/guide/tr/{apiId}` → `/api/apis/guide/tr/property/{trId}` (no auth needed).
  Asset-class specs are also public at `https://www.nhplug.com/openapi-docs/<slug>/openapi.json`
  (the declared source of truth; slugs: common·krstock·gbstock·krfuture·gbfuture·krbond·krgold).

## Kiwoom scope

- Kiwoom US-stock (overseas) support is **Python-only**; the sibling `cluefin-openapi-ts`
  package's `overseas-*` files are KIS, not Kiwoom.

## Conventions that are easy to mis-infer

- The two `TokenManager` classes (kis/kiwoom) are copy-pasted, not shared — mirror
  cache-behavior changes by hand in both.
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
