# AGENTS.md — cluefin-openapi-cli

Non-obvious constraints only; see the root AGENTS.md for repo-wide rules.

## Env & safety

- Credential loading is hardcoded to `Path.cwd() / ".env"` (via
  `cluefin_openapi.client_factory`) — there is no `.env.test` or `--env-file` support,
  so running from the repo root always uses production credentials.
- Every registered command is `side_effect="read"` (asserted by a test): the CLI cannot
  place orders today. Running any kis/kiwoom command still generates and caches a real
  auth token, though. `--dry-run` is the only execution path that never touches auth.
- `brokers --json` and `--dry-run` report `credentials.configured` as a boolean derived
  from `BrokerClientConfig.from_env()`; never add the values themselves to any payload.
- Client `loguru` output is cut to WARNING in `main()` so agents get clean stderr. Set
  `CLUEFIN_OPENAPI_DEBUG=1` to see client DEBUG/INFO again.

## Broker roles are data, not code paths

- KIS = primary, Kiwoom = auxiliary, DART = reference — defined once in
  `metadata.BROKER_ROLES`. Ordering everywhere (`list`, `brokers`, `iter_brokers`) comes
  from `broker_rank`, not from alphabetical sorting.
- `metadata.KIWOOM_KIS_ALTERNATIVES` is a hand-maintained map; a Kiwoom command missing
  from it is *declared* Kiwoom-only and shows up in `brokers --json` →
  `kiwoom_only_commands`. When adding a Kiwoom handler that overlaps KIS, add the entry
  or agents will treat it as the intended Kiwoom use. `test_agent_surface.py` fails if
  any key or target is not a real command path.

## Exit codes and error envelope

- Exit codes are a contract with agents (`errors.EXIT_CODES`; mirrored in README and
  SKILL.md): 2 usage/validation, 3 credentials/auth, 4 broker/network/response-parse,
  5 rate limit, 1 everything else. Do not raise `CliError` with a bare exit 1 for a
  classifiable failure — route it through `classify_exception`.
- Broker exceptions are classified by **class-name suffix** (`*RateLimitError`,
  `*AuthenticationError`, …) because kis/kiwoom/dart exception hierarchies are parallel
  copies. A pydantic `ValidationError` from response parsing is deliberately separated
  from broker `*ValidationError` (request rejected) — the former is `ResponseParseError`.
- Validation (`validation.py`) runs *before* any client is created: enum, pattern,
  bounds, unknown fields, and string hardening (control chars, `..`, `%`, `?`, `#`) on
  every nested string. If a broker ever needs a literal `%`/`?`/`#` in a parameter, the
  hardening list must be made per-field, not removed.

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
- `test_readme_smoke.py` does literal substring assertions against `README.md` and
  `SKILL.md` — keep the example/taxonomy strings in sync with `metadata.py` text.
- `list` is **brief** by default (`_command_brief`); `--full` restores the old
  per-command `parameters`. Tests and agents that need parameters must use `--full` or
  `schema`.
