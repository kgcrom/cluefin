# AGENTS.md

## Project

Cluefin is a research-oriented toolkit for Korean financial markets. The Python side is a `uv` workspace; the TypeScript OpenAPI client is a separate package under the same repo.

## Repository Layout

- `packages/cluefin-openapi`: Kiwoom, KIS, and DART Python clients
- `packages/cluefin-ta`: technical analysis indicators
- `packages/cluefin-xbrl`: DART XBRL parsing
- `packages/cluefin-openapi-ts`: TypeScript OpenAPI client, Node 20+
- `apps/cluefin-cli`: user-facing CLI
- `apps/cluefin-openapi-cli`: broker command CLI
- `apps/cluefin-ta-cli`: TA command CLI
- `apps/cluefin-desk`: TUI dashboard

Keep reusable libraries under `packages/` and runnable tools under `apps/`. Do not restructure the workspace unless a task explicitly asks for it.

## Working Rules

- Use `uv run` for Python commands.
- Target Python 3.10+.
- Set API keys in `.env`; do not commit local credentials or token caches.
- On macOS, install LightGBM with `brew install lightgbm`.
- Leave unrelated worktree changes alone.

## Verification

Prefer fast local verification before broader checks:

```bash
uv run pytest -m "not integration and not slow"
uv run ruff format . --check
uv run ruff check .
```

For all non-integration tests:

```bash
uv run pytest -m "not integration"
```

For the TypeScript package:

```bash
cd packages/cluefin-openapi-ts
npm run check
npm run typecheck
npm run test:unit
```

## Broker CLI Discovery

For broker command discovery, prefer JSON-friendly commands:

```bash
uv run cluefin-openapi-cli list --json
uv run cluefin-openapi-cli describe <broker> <category> <method> --json
uv run cluefin-openapi-cli describe dart <method> --json
```

## Local Agent Files

- `.entire/` is local Entire state and is ignored by git.
- `.codex/` may be needed for local Codex hooks, but do not commit it unless the task explicitly asks to make Codex/Entire hooks part of the project workflow.
- Do not add repo-local `.pi/` or `SYSTEM.md` files unless a task explicitly asks for Pi package/runtime customization.

## Common Commands

```bash
uv sync --all-packages
uv run lefthook install
uv run ruff format .
uv run ruff check . --fix
```

## Quick Usage

```bash
uv run cluefin-cli ta 005930
uv run cluefin-cli ta 005930 --chart --ml-predict --shap-analysis
```
