# AGENTS.md — apps

`cluefin-openapi-cli` (agent-facing JSON CLI) and `cluefin-desk` (TUI). Both are read-only — no order code — but
both issue real tokens. Each has its own AGENTS.md; Python Codacy patterns are in `packages/AGENTS.md`.

- Both read only `<cwd>/.env`: run from the repo root. From `apps/cluefin-openapi-cli` the CLI finds no `.env` and
  fails with exit 3 `CredentialsMissing` (`cache load` stopped on Kiwoom, 2026-11-04); `brokers --json` shows which
  keys the current directory sees.
- To discover broker commands, use `cluefin-openapi-cli`'s `--json` output rather than reading the handlers.
- "Today"/"now" is KST, not the machine's zone (ruff `DTZ`): use `clock.today_kst()`/`now_kst()`
  (`cluefin_openapi_cli.clock`, `cluefin_desk.clock`). Token caches stay naive local time — the TS package shares them.
- Import clients, auth, services and exceptions from the broker package (`from cluefin_openapi.kis import Auth`),
  not its `_`-modules. Response models are the exception: only kis realtime and ecos re-export them, so
  `cluefin_openapi.<broker>._*_types` is the path. Patch targets in tests follow the import path the app uses.
