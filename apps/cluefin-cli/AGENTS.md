# AGENTS.md — cluefin-cli

Non-obvious constraints only; see the root AGENTS.md for repo-wide rules.

## Real-account behavior

- `Settings` loads `.env` **cwd-relative** (pydantic-settings) with no env-switching flag,
  so running from the repo root silently picks up the production credentials, and
  `DomesticDataFetcher.__init__` generates a real Kiwoom token immediately (not lazily).
  The app is strictly read-only — no order-placement code exists — so the exposure is
  auth/API usage, not trades.
- The `kis_*` fields on `Settings` are dead: nothing in this app reads them and
  `.env.sample` omits them. Don't assume KIS is wired up here.

## Conventions

- This app deliberately does **not** use `cluefin_openapi.client_factory`. New commands
  follow the local pattern: a fetcher class that imports the `settings` singleton,
  validates its own required keys, and constructs Auth/Client in `__init__` (see
  `data/fetcher.py`, `data/fundamentals.py`, `data/xbrl.py`).

## Stale docs / dead code

- README's `ML_MODEL_PATH` / `ML_CACHE_DIR` settings are aspirational — no code reads
  them; every `--ml-predict` run retrains in memory from scratch.
- `_generate_mock_data` in `data/fetcher.py` is dead code, not a real fallback path.

## Testing

- All unit tests patch the fetcher classes at the call site; there are no integration
  tests in this app, so `pytest` here never reads `.env` or touches the network.
