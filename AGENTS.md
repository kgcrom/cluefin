# AGENTS.md

Cluefin is a research toolkit for Korean financial markets. This file records only what
can't be learned by exploring the repo — layout, tooling, and command lists are
discoverable, so they're not repeated here. Each package/app has its own AGENTS.md for
its non-obvious constraints.

## Secrets & real accounts

- Real credentials live in `.env` and `.env.test` at the repo root — **never echo, print,
  or commit their values**.
- `.env` is the **production** pair (real brokerage account). `.env.test` is mock/dev for
  Kiwoom only — its KIS side is still `KIS_ENV=prod`. Anything that loads `.env` —
  including local CLI runs — talks to a real account.

## Testing policy

- Real API keys are used **only** by tests marked `integration`; everything else is mocked
  and hits no network.
- `realtime`-marked tests require market hours (09:00–15:30 KST).

## Environment gotchas

- macOS system deps: `brew install lightgbm ta-lib`.
- Git hooks run via **lefthook** (`uv run lefthook install`) — not the `pre-commit` framework.

## Conventions

- Conventional Commits with **Korean** messages: `type(scope): 설명`.
- When discovering broker commands, prefer `cluefin-openapi-cli`'s `--json` output.

## Local agent files

- `.entire/` is local Entire state and is git-ignored.
- Don't commit `.codex/`, or add repo-local `.pi/` / `SYSTEM.md`, unless a task explicitly
  asks to make those part of the project workflow.
