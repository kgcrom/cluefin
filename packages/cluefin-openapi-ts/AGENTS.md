# AGENTS.md — cluefin-openapi-ts

Non-obvious constraints only; see the root AGENTS.md for repo-wide rules.

## Scope boundary (easy to get wrong)

- The Kiwoom side implements **domestic endpoints only**. Kiwoom US-stock REST and all
  Kiwoom WebSocket support are Python-only (sibling `cluefin-openapi`) and out of scope
  here. The `src/kis/overseas-*` files are **KIS** overseas-stock APIs and *are* in
  scope — don't confuse the two.

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
- Endpoint-count tests hardcode totals (`tests/core/endpoint-count.test.ts`, KIS
  contract tests); bump them whenever metadata changes.

## Tooling surprises

- `npm run typecheck` runs the tsdown bundler, not `tsc --noEmit` — type errors surface
  as bundler errors, and this is what `publish:check` gates on.
- Wire format is snake_case (Zod schemas match the wire); the public API auto-camelCases
  responses. A new field must be handled with this asymmetry in mind.
- KIS `custtype` is hardcoded to `'P'` (personal) in the HTTP and socket clients —
  corporate-account calls aren't possible without changing that.

## Integration tests

- Gated by `CLUEFIN_OPENAPI_TS_RUN_INTEGRATION=1`; env loads root `.env.test` then
  `.env`, first-wins — an exported shell var silently shadows `.env.test`.
- They run serialized (separate vitest config, single fork, 180s timeout) to respect
  live rate limits; don't fold them into the parallel unit config.
- KIS account tests need `KIS_CANO`; without it they skip silently rather than fail.

## Stale docs

- `docs/api-coverage-gap.md` is a snapshot: its "미구현" rows for KIS realtime quotes
  are outdated (those files exist now). The README's KIS quick-start calls
  `auth.generateToken()`, but the real method is `generate()` — don't copy it verbatim.
