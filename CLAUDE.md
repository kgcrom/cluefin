# CLAUDE.md

## Project

Cluefin is a Korean market analysis monorepo.

- `packages/cluefin-openapi`: Kiwoom, KIS, DART clients
- `packages/cluefin-ta`: technical indicators
- `packages/cluefin-xbrl`: XBRL / DART statement parsing
- `apps/cluefin-cli`: analysis CLI
- `apps/cluefin-openapi-cli`: broker command CLI
- `apps/cluefin-desk`: TUI app

## Rules

- Use `uv run` for Python commands
- Keep secrets in `.env`
- Use mocks for unit tests
- Use real API keys only for `integration` tests

## Common Commands

```bash
uv sync --all-packages
uv run pytest -m "not integration"
uv run pytest -m integration
uv run ruff format .
uv run ruff check . --fix
```

## TypeScript

```bash
cd packages/cluefin-openapi-ts
npm install
npm run test:unit
npm run lint
npm run build
```
