# AGENTS.md

Cluefin is a research toolkit for Korean financial markets. The Python side is a `uv`
workspace; `packages/cluefin-openapi-ts` is a separate TypeScript client in the same repo.
This file records only things that aren't obvious from reading the code — layout, tooling,
and command lists are discoverable, so they're not repeated here.

## Secrets

- Real credentials live in `.env` (and `.env.test`) at the repo root — **never echo, print,
  or commit their values**.
- For setup, copy a `*.env.sample` (e.g. `packages/cluefin-openapi/.env.sample`,
  `apps/cluefin-cli/.env.sample`) to `.env`.

## Testing policy

- Unit tests use mocks and hit no network. Real API keys are used **only** for tests marked
  `integration`.
- Markers: `integration`, `realtime` (requires market hours, 09:00–15:30 KST), `slow`.
- Fast local check: `uv run pytest -m "not integration and not slow"`.

## Environment gotchas

- macOS needs `brew install lightgbm`; TA-Lib requires its C library as a system dep.
- Git hooks run via **lefthook** (`uv run lefthook install`) — not the `pre-commit` framework.

## Broker CLI discovery

Prefer the JSON output when discovering broker commands:

```bash
uv run cluefin-openapi-cli list --json
uv run cluefin-openapi-cli describe <broker> <category> <method> --json
```

## Commits & PRs

- Conventional Commits with **Korean** messages: `type(scope): 설명`.
- Fill out `.github/PULL_REQUEST_TEMPLATE.md` when opening a PR.

## Local agent files

- `.entire/` is local Entire state and is git-ignored.
- Don't commit `.codex/`, or add repo-local `.pi/` / `SYSTEM.md`, unless a task explicitly
  asks to make those part of the project workflow.

## Kiwoom 미국주식 (overseas)

The active US-stock work (branch `feat/kiwoom-overseas`) is **Python-only** — the
`cluefin-openapi-ts` package is out of scope (its `overseas-*` files are KIS, not Kiwoom).

- **Modules** (under `packages/cluefin-openapi/src/cluefin_openapi/kiwoom/`): each category is
  a pair — `_overseas_<category>.py` (impl class `Overseas<Category>`) and
  `_overseas_<category>_types.py` (Pydantic v2 models `Overseas<Category><Thing>` that inherit
  `(BaseModel, KiwoomHttpBody)`, set `ConfigDict(title="미국주식 …")`, and name fields by the
  raw Kiwoom field codes). Mirrors the existing `_domestic_*` set.
- **Client wiring** (`_client.py`): no separate client — lazy `@property` accessors on the
  single `Client`, with `overseas_`-prefixed names (`overseas_account`, `overseas_order`, …).
- **WebSocket** (`_overseas_condition_search`, `_overseas_realtime`): async, not on the HTTP
  `Client`. `_socket_client.py`'s `KiwoomWebSocketClient` is a shared raw-asyncio (no extra
  dep) client for `wss://…:10000/api/us/websocket` that handles LOGIN/PING; the two domain
  classes take it in their ctor and send JSON frames (REG/REMOVE, GCNSRLST/GCNSRREQ/GCNSRCLR)
  + parse responses. Mirrors the `kis/_socket_client.py` pattern.
- **Tests** (`packages/cluefin-openapi/tests/kiwoom/`): `test_overseas_<category>_unit.py`
  (table-driven via `_helpers.py` `EndpointCase` / `run_post_case`, no marker) plus
  `test_overseas_<category>_integration.py` (`@pytest.mark.integration`, using the `client`
  fixture in `conftest.py` that skips when `KIWOOM_*` env is absent).
