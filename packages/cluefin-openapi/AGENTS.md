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
