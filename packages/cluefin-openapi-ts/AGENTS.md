# AGENTS.md — cluefin-openapi-ts

Non-obvious constraints only; see the root AGENTS.md for repo-wide rules.

## Scope boundary (easy to get wrong)

- "해외/overseas" means three different things here, and only one of them is out of scope:
  - `src/kis/overseas-*` — **KIS** overseas stock. In scope.
  - `src/nhplug/overseas-stock-*` — **NH PLUG gbstock** (`/gbstock/...`). In scope, REST +
    WebSocket. The class/file names say "overseas", the paths and the vendor docs say
    "gbstock" — same thing.
  - **Kiwoom** US stock. Out of scope: the Kiwoom side implements domestic endpoints only,
    and Kiwoom US-stock REST plus all Kiwoom WebSocket support are Python-only (sibling
    `cluefin-openapi`).
- NH PLUG's other asset classes (krfuture·gbfuture·krbond·krgold) have public specs but are
  not ported here — only common·krstock·gbstock are.

## Coupling to the Python sibling

- `generate:metadata` regex-parses `packages/cluefin-openapi`'s Python source to produce
  the TS metadata files. Nothing re-runs it automatically: when the Python package's
  endpoints change, re-run it or the TS side silently goes stale.
- The KIS token cache JSON (`<repo>/data/.kis_token_cache.json`) is **shared with the
  Python package** — same file, same snake_case format — because KIS allows only 1
  token generation per minute. Don't change the format on one side only.
- The nhplug token cache file is **also shared with Python**, but is scoped by **app_key
  only** (`nhplugTokenCacheFileName`), not by env — one NH token is issued on the live
  domain and used for both live and mock calls. The KIS store is env-scoped. Don't
  "unify" the two schemes; changing either breaks cache sharing with Python.
- Endpoint-count tests hardcode totals (`tests/core/endpoint-count.test.ts`, KIS
  contract tests); bump them whenever metadata changes.

## Declaration output (`dist/types`)

- `build:types` is `tsc -p tsconfig.build.json` — a real `--emitDeclarationOnly` pass over
  `src` only. It emits a tree mirroring `src`; `dist/types/index.d.ts` is the entry and
  re-exports the rest. Declarations come from `tsc`, not from a template — the only
  generator script is `scripts/generate-metadata.mjs`.
- `tsconfig.build.json` turns off `declarationMap`/`sourceMap` that the base config sets —
  turning them back on doubles the shipped file count with maps pointing at absent `src`.
- The base `tsconfig.json` includes `tests`, which has ~61 pre-existing type errors. They
  don't block the build because `tsconfig.build.json` includes `src` only. `npm run
  typecheck` therefore runs `tsc -p tsconfig.build.json --noEmit` (src) **and** tsdown.
- **Relative specifiers in `src` must carry an explicit `.js` extension** (`./core/errors.js`,
  and `./kis/index.js` for a directory barrel — never `./kis.js`). `tsc` copies specifiers
  into the emitted declarations verbatim, and extensionless ones are illegal under
  `moduleResolution: node16`/`nodenext`: the consumer gets TS2834 on the `.d.ts` and then
  TS2305 for *every* imported name. vitest and tsdown both resolve `./foo.js` → `foo.ts`,
  so this costs nothing at build/test time. `tests/` may stay extensionless.
- `tests/core/dts-consumer.test.ts` compiles `tests/fixtures/dts-consumer/consumer.ts`,
  which imports by package name (`cluefin-openapi`) so it goes through `package.json`'s
  `exports["."].types`. That fixture is excluded from the root `tsconfig.json` — it only
  resolves after a build. The test builds `dist/types` itself if it's missing.
  It compiles the fixture **twice**, under `tsconfig.json` (Bundler) and
  `tsconfig.nodenext.json` (NodeNext) — a Bundler-only check cannot see the
  extensionless-specifier failure described above. The NodeNext project
  deliberately sets `skipLibCheck: false` (that is what surfaces TS2834 across all 112
  declaration files rather than only on names the fixture happens to import), which in
  turn needs `types: ["node"]`. Don't "simplify" either setting.
- `npx @arethetypeswrong/cli --pack` reports **`node16 (from CJS)`: Masquerading as ESM**.
  Known and accepted: the package is `"type": "module"` with a dual ESM/CJS build but a
  single `types` field, so `require` gets an ESM-flavoured `.d.ts`. Fixing it means
  emitting a `.d.cts` and adding `exports.require.types` — a distribution-shape change.
- **KIS `schemas/*` (166 names) are emitted but unreachable**: `src/kis/index.ts` re-exports
  zero schema modules, while `src/kiwoom/index.ts` re-exports 9 and `src/nhplug/index.ts` 7.
  Consumers can't `import type { GetStockCurrentPriceResponse }`. Fixing that is a barrel
  change, not a build change (measured: no name collisions with the current surface).

## Tooling surprises

- `npm run typecheck` runs `tsc -p tsconfig.build.json --noEmit` and then the tsdown
  bundler; `publish:check` gates on it.
- Wire format is snake_case (Zod schemas match the wire); the public API auto-camelCases
  responses. A new field must be handled with this asymmetry in mind.
- KIS `custtype` is hardcoded to `'P'` (personal) in the HTTP and socket clients —
  corporate-account calls aren't possible without changing that.
- Kiwoom's auth API is `generateToken()`/`revokeToken()`, while KIS and NH PLUG use
  `generate()`/`revoke()` — the asymmetry is real, not a typo.
- `CamelizeKeys` in `src/core/types.ts` deliberately wraps its key mapping in
  `Uncapitalize` because the runtime `toCamelCase` lowercases the first character. This is
  invisible for KIS/Kiwoom (lowercase snake_case wire keys) and only shows up on NH PLUG's
  capitalized envelope keys (`Output_0` → `output0`). Dropping it silently desyncs the
  declared response types from the values actually returned.
- nhplug treats **both** `00000` and `XA102` as success (`SUCCESS_RSP_CODES`) — the mock
  server answers some successful inquiries with `XA102`, so a 00000-only check reports
  false failures. Keep the list identical to Python's `_model.SUCCESS_RSP_CODES`.
- An nhplug HTTP 200 can still carry a failing `rsp_cd`; the failure check lives in
  `NhplugClient.invokeEndpoint` after the HTTP layer, so HTTP-level retry/rate-limit logic
  never sees those errors.

## Integration tests

- Gated by `CLUEFIN_OPENAPI_TS_RUN_INTEGRATION=1`; env loads root `.env.test` then
  `.env`, first-wins — an exported shell var silently shadows `.env.test`.
- They run serialized (separate vitest config, single fork, 180s timeout) to respect
  live rate limits; don't fold them into the parallel unit config.
- KIS account tests need `KIS_CANO`; without it they skip silently rather than fail.

## Stale docs

- `docs/api-coverage-gap.md` is a snapshot: its "미구현" rows for KIS realtime quotes
  are outdated (those files exist now), and it predates NH PLUG entirely.
