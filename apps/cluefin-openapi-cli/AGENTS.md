# AGENTS.md — cluefin-openapi-cli

Non-obvious constraints only; see the root AGENTS.md for repo-wide rules.

## Env & safety

- Credential loading is hardcoded to `Path.cwd() / ".env"` (via
  `cluefin_openapi.client_factory`) — there is no `.env.test` or `--env-file` support,
  so running from the repo root always uses production credentials.
- Every registered command is `side_effect="read"` (asserted by a test): the CLI cannot
  place orders today. Running any kis/kiwoom command still generates and caches a real
  auth token, though.

## Commands are hand-written, not generated

- Nothing introspects `cluefin-openapi`. A new client method needs: an `@rpc_method`
  handler, an entry in that module's `_ALL_HANDLERS`, and wiring in the broker
  aggregator (`get_kis_handlers()` / `get_kiwoom_handlers()` / `DART_HANDLERS`).
- The `name=` passed to `@rpc_method` controls the CLI path via dot-splitting
  (`category.leaf` for kis/kiwoom; dart has no category segment) — wrong dot placement
  lands the command in the wrong path.
- A `category` missing from `_CATEGORY_DEFAULTS` in `metadata.py` silently falls back to
  domain `market` / tag `ranking` instead of erroring — add an entry for new categories.

## Tests that break on unrelated-looking changes

- `test_rpc_registry.py` hardcodes the total command count — bump it when adding or
  removing any handler.
- New auto-derived domains/tags must also be added to `_DOMAIN_TAXONOMY`/`_TAG_TAXONOMY`
  or the taxonomy-coverage test fails.
- Recipe → command references are validated only by a test, not at runtime; renaming a
  command path silently breaks recipes until tests run.
- `test_readme_smoke.py` does literal substring assertions against `README.md` — keep
  the README's example/taxonomy strings in sync with `metadata.py` text.
