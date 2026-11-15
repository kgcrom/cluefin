# AGENTS.md — cluefin-openapi-ts

Non-obvious constraints only; see the root AGENTS.md for repo-wide rules. Measured vendor behaviour shared with the
Python sibling lives in `packages/cluefin-openapi/AGENTS.md` and `VENDOR_DOC_ERRATA.md` — this file keeps what is
TypeScript-only and what must be mirrored by hand.

## Scope boundary (easy to get wrong)

- "해외/overseas" means three different things here, and only one of them is out of scope:
  - `src/kis/overseas-*` — **KIS** overseas stock. In scope.
  - `src/nhplug/overseas-stock-*` — **NH PLUG gbstock** (`/gbstock/...`). In scope, REST + WebSocket. The class/file
    names say "overseas", the paths and the vendor docs say "gbstock" — same thing.
  - **Kiwoom** US stock. Out of scope: the Kiwoom side implements domestic REST only; Kiwoom US-stock REST and all
    Kiwoom WebSocket support are Python-only.
- NH PLUG's other asset classes (krfuture·gbfuture·krbond·krgold) have public specs but are not ported — only
  common·krstock·gbstock are.
- The seven KIS 국내주식 종목분석 endpoints (balance sheet, income statement, financial/profit/other/stability/growth
  ratios) were removed in 1.1.0: KIS blocked them for every app on 2026-11-11 16:00 (data licence). Don't port them back.

## Mirror the Python sibling by hand

Nothing enforces any of this automatically.

- `npm run generate:metadata` regex-parses `packages/cluefin-openapi`'s Python source into the KIS/Kiwoom/nhplug
  metadata and the DART metadata **and Zod schemas**. Re-run it when Python endpoints change, or the TS side silently
  goes stale. **Check it by regenerating on a clean tree: `git diff` must be empty** (#225 — after Python switched to `X | None`
  annotations the generator crashed on DART and nobody saw, because nothing runs it).
  - It chains `npm run format`: raw `JSON.stringify` output doesn't match Biome's quoting, so without it every
    metadata file shows up in the diff.
  - A Python param is required when it has no default, even if typed `X | None`.
  - Never hand-edit `src/dart/metadata|schemas`. Per-method additions that must survive regeneration go in the
    generator's own tables.
- **ECOS is hand-written, outside the generator** (Python `ecos/` builds URL path segments, not path + query metadata).
  When Python `ecos/_*.py` or `_*_types.py` change, update `src/ecos/*` yourself: schemas, result-code table, constants.
- **Token cache files are shared with Python** (`<tmpdir>/cluefin-openapi/`). Each broker's `token-cache.ts` mirrors that
  broker's Python `TokenManager._cache_file_name` byte for byte — `kisTokenCacheFileName` / `kiwoomTokenCacheFileName`
  (`env` + `sha256(app_key)[:8]`) and `nhplugTokenCacheFileName` (app key only: one NH token serves live and mock). Don't
  unify the schemes; change a Python name or cache JSON shape and you change the TS file too. Why each rule exists
  (6h max age, env scoping, NH re-issue alerts) is in the Python AGENTS.md.
  - `cached_at` is naive local time with no `Z`/offset (`localIsoNow` in `src/core/token-file.ts`, never
    `toISOString()`): Python parses it with `fromisoformat` and compares against a naive `datetime.now()`.
  - KIS and Kiwoom drop a cached token after 6h (`MAX_CACHE_AGE_MS`); nhplug has no max age, only
    `cachedAt + expiresIn`.
  - A revoke in either language kills the token the other is reusing. Kiwoom returns the *same* token on re-issue while
    one is valid, so a revoke test that never reads the cache file still broke every later run with `8005`
    (2026-09-23). Hence `KIS_TEST_REVOKE=1` / `KIWOOM_TEST_REVOKE=1` gate the TS revoke tests (nhplug has no TS auth
    integration test; `NHPLUG_TEST_REVOKE` is Python's). Neither side re-issues on `8005`.
  - `KiwoomAuth.revokeToken()` does not clear the cache store, unlike `KisAuth.revoke()` and `NhplugAuth.revoke()`.
- nhplug body codes: keep `SUCCESS_RSP_CODES` and the `NO_DATA` / `MOCK_UNSUPPORTED` / `NOT_BUSINESS_DAY` lists in
  `src/nhplug/client.ts` identical to Python's `_model.SUCCESS_RSP_CODES` and `_exceptions.*_RSP_CODES`. A 00000-only
  check reports false failures (mock answers `XA102`, live account inquiries `00166`, `buyableQuantity` `00221`).

## Client behaviour that surprises

- **Default `env` is not uniform**: `KisHttpClient` defaults to `'prod'`, everything else (`KisAuth`, `KisSocketClient`,
  Kiwoom, nhplug) to `'dev'`. Pass it explicitly in code and tests.
- Kiwoom's auth API is `generateToken()`/`revokeToken()`, KIS and NH PLUG use `generate()`/`revoke()` — real, not a typo.
- **`KisApiError` is not the parent of `KisAuthenticationError`** (same for every broker): the typed errors extend
  the shared `Api*Error` classes, the `<Broker>ApiError` extends `ApiError` directly. Catch `ApiError` for "anything".
- KIS `custtype` is a per-call input on HTTP (header, default `'P'`); only the socket client hardcodes `'P'`.
- **One KIS WebSocket session per app key, and each `approve()` voids earlier approval keys.** The server answers
  `OPSP8996 ALREADY IN USE appkey` or `OPSP0011 invalid approval` and drops the connection (2026-10-12);
  `KisSocketClient` emits it as an `error` event and repeats it in the next "not connected" error. A realtime test
  fails this way when desk, a Python run or another TS run uses the same key.
- Wire format is snake_case (Zod schemas match the wire); the public API camelCases responses. `CamelizeKeys` in
  `src/core/types.ts` wraps its mapping in `Uncapitalize` because the runtime `toCamelCase` lowercases the first
  character — it only shows on NH PLUG's capitalized envelope keys (`Output_0` → `output0`). Dropping it desyncs the
  declared types from the returned values.
- nhplug sends body values **as given** — unlike KIS/Kiwoom it must not stringify them: the server rejects a string
  where the spec says integer/number with `IGW40011` (2026-09-27). `reqCnt: 10`, not `'10'`.
- An nhplug HTTP 200 can carry a failing `rsp_cd`. The check is in `NhplugClient.invokeEndpoint`, after the HTTP layer,
  so HTTP-level retry and rate-limit logic never see those errors.
- `common.closeWebsocketSession` throws when no session is open: the server answers HTTP 200 + `rsp_cd 10000`
  (2026-09-23; HTTP 500 `IGW50025` a month earlier). It has no integration test — it tears down the account's sessions.

## OpenDART (`src/dart`)

- **Fix Python, not the generator, when a response is wrong.** Python's tests built fake responses from its own models
  and its integration tests accepted `013`, so wrong models and paths went unseen (2026-10: wrong model for
  trust-contract, duplicated path for tangible-asset transfer, a `recpt_no` typo, a required field the server never
  sends). TS integration tests attach `responseSchema` to the call so a mismatch with live data throws — a failure
  there usually means a Python bug.
- Python method names were renamed to match their endpoints on 2026-11-04 (`profit_revocation` → `lawsuit_filing` for
  소송등의제기, and the class to `MajorMattersReport`). The old names survive only as deprecated aliases — don't use them
  in new code. **The files are still named `major-shareholder-disclosure.ts`** (source, metadata, schemas, tests); the
  symbol and the client getter are `MajorMattersReport` / `majorMattersReport`.
- A non-`000` body `status` is **returned, not thrown** — including a bad key (`010`), which Python raises as
  `DartAuthenticationError`. Only binary endpoints throw `DartApiError`, because their errors arrive as a small XML
  body. Don't add `NoData`-style errors like nhplug.
- Auth is the `crtfc_key` query param (no token, no cache). The key is masked in errors/logs — keep it out of
  `requestContext`.
- Zod `int`/`float` fields are `number | string` on purpose: pydantic coerces numeric strings, so the wire type is
  unknown. Don't tighten them without live proof.
- ZIP/XML parsing is hand-rolled (`src/core/zip.ts`, `src/dart/xml.ts`) to avoid dependencies: no ZIP64, no encryption,
  flat `<list>` XML only. Binary endpoints return bytes / `Map`, never write files.
- 주요사항보고서 are event-driven, so a fixed company returns only `013`. The integration test uses dated real filings
  in `tests/dart/fixtures/`; `013` must not count as a pass there.
- `PublicDisclosure` and `PeriodicReportFinancialStatement` are class + interface merges (custom methods plus generated
  ones) — Biome's `noUnsafeDeclarationMerging` is off for this.

## Bank of Korea ECOS (`src/ecos`)

- Wire keys are UPPER_SNAKE (`STAT_CODE`). The shared `toCamelCase` would turn them into `sTATCode`, so rows go through
  `camelizeEcosKeys` (lowercase first). Field names follow the wire (`pStatCode`, `srchYn`, `wgt`), not Python's renamed
  fields (`parent_stat_code`, `searchable`, `weight`).
- Errors arrive as HTTP 200 + `RESULT.CODE`; `INFO-200` is an empty page, not an error. The code → class table and the
  retryable set (600·602) mirror Python `_exceptions.py`. ERROR-301 becomes `EcosSampleLimitError` only when the
  message contains "sample".
- The auth key sits in the URL path: `requestContext.path` is masked (`/***/`) and messages are redacted. `sample` is
  not redacted — it is public and the server's own messages contain the word.
- Row schemas are `z.looseObject` (unknown fields pass), so the integration test compares row keys with each schema's
  shape to catch spec drift. It runs on `sample` with no key; `ECOS_AUTH_KEY` adds one real-key paging test.

## Declaration output (`dist/types`)

- **Relative specifiers in `src` must carry an explicit `.js` extension** (`./core/errors.js`, and `./kis/index.js` for
  a directory barrel — never `./kis.js`). `tsc` copies specifiers into the emitted declarations verbatim, and
  extensionless ones are illegal under `moduleResolution: node16`/`nodenext`: the consumer gets TS2834 on the `.d.ts`
  and then TS2305 for *every* imported name. `tests/` may stay extensionless.
- `tests/core/dts-consumer.test.ts` compiles a consumer fixture twice, under Bundler and NodeNext — a Bundler-only
  check cannot see the failure above. The NodeNext project's `skipLibCheck: false` + `types: ["node"]` are what surface
  TS2834 in every emitted file; don't "simplify" them.
- `tsconfig.build.json` turns off `declarationMap`/`sourceMap` — turning them back on doubles the shipped file count
  with maps pointing at absent `src`.
- **`npm run typecheck` checks `src` only.** The base `tsconfig.json` also includes `tests`, which carries pre-existing
  type errors, so no gate type-checks tests; run `npx tsc -p tsconfig.json --noEmit` and grep for your file.
- `npx @arethetypeswrong/cli --pack` reports **`node16 (from CJS)`: Masquerading as ESM**. Known and accepted: the
  package is `"type": "module"` with a dual build but one `types` field. Fixing it means a `.d.cts` plus
  `exports.require.types` — a distribution-shape change.
- **KIS `schemas/*` are emitted but unreachable**: `src/kis/index.ts` re-exports no schema module, while the Kiwoom,
  nhplug and DART barrels do. Consumers can't `import type { GetStockCurrentPriceResponse }`. That is a barrel change,
  not a build change.

## Codacy findings in TypeScript

These came from `src/dart` (19 findings, then 6, then 0); the fixed shapes are in `src/dart/client.ts` and
`src/dart/xml.ts`.

- **Dynamic-key object access** (`security/detect-object-injection`): reads *and* assignments are flagged, tests too.
  In that PR an `eslint-disable` comment did not clear the finding. `src/` still has such comments (KIS, Kiwoom and
  nhplug clients, the DART alias loop) — don't take them as proof it works; restructure instead.
  `query[wireKey] = String(parsed[inputKey])` became: invert the map once (`new Map(inputKey → wireKey)`), walk
  `Object.entries(parsedInput)`, push `[wireKey, value]`, then `Object.fromEntries`. Tests calling
  `service[methodName](input)` became `new Map(Object.entries(service)).get(name)` or a table of lambdas.
- **`new RegExp(variable)`** is critical. A per-tag ``new RegExp(`<${tag}>…</${tag}>`)`` became `indexOf` on the opening
  and closing tag (`findElement`) plus one literal regex.
- **"Unnecessary conditional"** on `match[1] ?? ''` or `x !== undefined`: Codacy analyses without
  `noUncheckedIndexedAccess`, so `??` looks dead while this tsconfig requires it. Use named regex groups read by
  truthiness (`groups.body || ''`), branching in a small helper.
- **Hardcoded password** on a literal assigned to a name containing key/secret/password, tests included. Build the
  dummy at runtime: `` `test-${randomUUID()}` ``.

## Tests

- **Run `npm run test:unit` as it is.** Under Claude Code (`AI_AGENT` set) vitest picks its agent reporter: summary and
  failures only. Add `--reporter=verbose` only when you need the console output of *passing* tests — the empty-block
  warnings below — because the agent reporter hides it and `silent: false` does not bring it back.
- Unit tests must not load the root `.env`: `vitest.config.ts` has no setup file on purpose (#138 — the old setup
  file put real-account keys into `process.env`, one env dump away from the test output). Only the integration config
  loads `.env.test` then `.env`, first-wins — an exported shell variable silently shadows `.env.test`.
- CI (`ci-openapi-ts.yml`) runs `npm run publish:check` on **Node 24 only**; `engines` says `>=20` but nothing tests
  20 or 22.
- `tests/nhplug/readme-samples.test.ts` executes the README's NH PLUG examples against a fake `fetch` and pins which
  host each call reaches. Change the README example and that test together.
- Integration tests are gated by `CLUEFIN_OPENAPI_TS_RUN_INTEGRATION=1` and run serialized; keep them out of the
  parallel unit config. KIS account tests skip silently without `KIS_CANO`.
- **Kiwoom mock (dev) app keys expire.** Token issuance then returns HTTP 200 without a token, and every Kiwoom
  integration test fails in `getKiwoomClient()` with `KiwoomAuthenticationError: … missing token or expires_dt`.
  Re-issue the mock key before debugging code.
- Realtime tests assert on **received data**, never on the subscribe reply (reasons and measurements: Python
  AGENTS.md, "Dangerous integration tests"); use `tests/_helpers/kis-realtime.ts` / `nhplug-realtime.ts`. The gate in
  `tests/_helpers/market-hours.ts` knows weekdays and hours (KRX stocks 09:00–15:20 KST) but **not holidays** — on a
  market holiday the tests would run and fail on the 30s wait. NH PLUG and KIS 통합 체결(`H0UNCNT0`) realtime tests are
  prod-only: the mocks don't serve those channels.
- Response-shape helpers, one per broker — don't loosen them, record a measured divergence in the call's ignore list
  (policy: Python AGENTS.md): `assertKisResponseShapeDeep` (not the older `assertResponseShape`, which misses item
  fields), `assertKiwoomSpecConformance`, `assertNhplugMatchesSpec`. An empty array passes vacuously —
  `KIS_SHAPE_REPORT_EMPTY=1` warns about empty KIS blocks, the Kiwoom helper always warns
  (`[kiwoom-spec] … empty blocks`).

## Releasing (npm)

The npm name is `cluefin-openapi` (same as the PyPI package); no workflow publishes it.

1. Bump `package.json` and `package-lock.json` together: `npm version X.Y.Z --no-git-tag-version`. v0.6.0–v1.0.0 did
   it as a separate `release(openapi-ts): vX.Y.Z` commit on `main`; 1.1.0 was bumped inside its feature PR (#228).
   Either way, **publish only from merged `main`**: an npm version can never be republished, so a number spent on code
   that then changes in review is gone. `package.json` can be ahead of the registry — compare with
   `npm view cluefin-openapi version` before choosing the next number.
2. `npm run publish:preview` — the CI gate (`publish:check`: build, biome, typecheck, unit tests) plus
   `npm pack --dry-run` to read the file list.
3. `npm run publish:manual` (`publish:check` + `npm publish --access public`). It needs the maintainer's npm login with
   2FA, so an agent can't run it — ask the user to run `! npm login` and
   `! cd packages/cluefin-openapi-ts && npm run publish:manual`.
4. The registry lags: `npm view` can answer 404 or the old `latest` for several minutes after a successful publish.

- **No git tags for the TS package.** The `cluefin-openapi/v*` tags belong to the Python package and are created by
  its publish workflow; a TS tag would need a distinct prefix (e.g. `cluefin-openapi-ts/v…`).
