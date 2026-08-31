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
  the TS metadata files, and `build:types` string-templates `index.d.ts` from that
  metadata. Nothing re-runs these automatically: when the Python package's endpoints
  change, re-run both or the TS side silently goes stale. New domain classes must also
  be added to the arrays inside `scripts/generate-types.mjs` or they won't appear in
  the published `.d.ts`.
- The KIS token cache JSON (`<repo>/data/.kis_token_cache.json`) is **shared with the
  Python package** — same file, same snake_case format — because KIS allows only 1
  token generation per minute. Don't change the format on one side only.
- The nhplug token cache file is **also shared with Python**, but is scoped by **app_key
  only** (`nhplugTokenCacheFileName`), not by env — one NH token is issued on the live
  domain and used for both live and mock calls. The KIS store is env-scoped. Don't
  "unify" the two schemes; changing either breaks cache sharing with Python.
- Endpoint-count tests hardcode totals (`tests/core/endpoint-count.test.ts`, KIS
  contract tests); bump them whenever metadata changes.
- `dist/types/index.d.ts` is **string-templated by hand**, not emitted by `tsc`. Domain
  classes come from metadata, but everything else (auth, token cache, socket client,
  standalone consts) has to be typed out literally in `scripts/generate-types.mjs` — it
  silently under-declares otherwise. `tests/core/dts-drift.test.ts` guards all three
  vendors by diffing the generator output against the runtime exports of
  `src/kis/index.ts`, `src/kiwoom/index.ts` and `src/nhplug/index.ts` — add a barrel
  export without a declaration and it fails, naming the missing symbols.
- The KIS realtime declarations (`*_FIELD_NAMES` literal tuples, `*RealtimeQuote` item
  interfaces, and the `RealtimeSchema<T>` handles for the Zod schemas) are **parsed out of
  `src/kis/metadata/*-realtime-quote.ts`** by the generator, which assumes every schema
  field is a bare `z.string()` and throws if that stops being true. The schemas are
  declared as `RealtimeSchema<Item>` (parse/safeParse only), not as `z.ZodObject<...>`.
- Kiwoom's `schemas/*` response types (~200 `export type` names in `src/kiwoom/index.ts`)
  are still undeclared — the drift test only enforces an explicit allowlist of type-only
  exports per vendor.

## Tooling surprises

- `npm run typecheck` runs the tsdown bundler, not `tsc --noEmit` — type errors surface
  as bundler errors, and this is what `publish:check` gates on.
- Wire format is snake_case (Zod schemas match the wire); the public API auto-camelCases
  responses. A new field must be handled with this asymmetry in mind.
- KIS `custtype` is hardcoded to `'P'` (personal) in the HTTP and socket clients —
  corporate-account calls aren't possible without changing that.
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
- (The README's KIS quick-start used to call a non-existent `auth.generateToken()`; it now
  correctly says `generate()`. Note that Kiwoom really does use `generateToken()`/
  `revokeToken()` while KIS and NH PLUG use `generate()`/`revoke()` — the asymmetry is
  real, not a typo.)
