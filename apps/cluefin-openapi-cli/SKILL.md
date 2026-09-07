---
name: cluefin-openapi-cli
description: Query Korean market data (quotes, charts, rankings, financials, sector/theme, ETF, corporate actions, DART filings) through the cluefin-openapi-cli. KIS is the primary broker; Kiwoom fills gaps; DART is reference. Use for any task that needs Korean stock market or disclosure data.
---

# cluefin-openapi-cli

Run every command from the workspace root with `uv run cluefin-openapi-cli ...`. Output is JSON; parse it, never scrape text.

## Invariants

- **Start with KIS.** KIS is the primary broker, Kiwoom is auxiliary, DART is reference. Call `list --broker kis --json` first. Use a `kiwoom` command only when its `kis_alternatives` is `[]`, or the KIS call returned no usable data. Never call Kiwoom for something KIS covers.
- **Read the schema before the first call.** `schema <broker> <category> <name> --json` gives the JSON Schema, one `--flag` per parameter, and ready-to-run `invoke.*` strings. Do not guess parameter names or code values; `enum` and `pattern` are enforced locally.
- **Dry-run before a new command shape.** Add `--dry-run` the first time you build a call. It validates and echoes the resolved `params` without touching the network or issuing a token.
- **Keep responses small.** Always pass `--fields` with the keys you actually need, and `--compact`. `list` is brief by default; only use `--full` when you need every parameter for many commands at once.
- **Branch on exit code, then `error.retryable`.** 0 ok · 1 internal · 2 fix your arguments · 3 credentials · 4 broker/network (retry once only if `retryable` is true) · 5 rate limited (wait `data.retry_after`, default 1s). Never retry a 2 or 3 as-is.
- **Every command is read-only.** There is no order or account-mutating command. Running any kis/kiwoom command still uses the real account credentials from `.env` in the current directory.
- **Never print credentials.** `brokers --json` tells you `credentials.configured` per broker without exposing values; that is the only credential check you need.

## Workflow

```bash
uv run cluefin-openapi-cli brokers --json                                # roles, configured?, kiwoom-only list
uv run cluefin-openapi-cli list --broker kis --domain quote --json       # or --tag, --category, --query
uv run cluefin-openapi-cli schema kis stock current-price --json
uv run cluefin-openapi-cli kis stock current-price --stock-code 005930 --dry-run --json
uv run cluefin-openapi-cli kis stock current-price --stock-code 005930 --fields current_price,per,pbr --compact
```

Workflow guides for multi-step tasks: `recipes --json`, then `recipe <name> --json`. Domain and tag catalogs: `domains --json`, `tags --json`; each entry includes `when_to_use`, `avoid_when`, and an `example_filter` you can run verbatim.

## Input rules

- Scalars: `--stock-code 005930` or `--stock-code=005930`. Arrays/objects: `--params-json '{...}'` (flags override its keys) or inline JSON on the flag.
- Strings containing control characters, `..`, `%`, `?`, or `#` are rejected before any network call. Pass raw values; the CLI encodes them.
- Stock codes are 6 digits for KIS (`005930`); Kiwoom chart/quote commands take `KRX:005930` style where the schema says so.

## When a call fails

- `ValidationError` (exit 2): read `error.data.issues[]`; each has `field`, `problem`, `allowed` or `hint`.
- `ResponseParseError` (exit 4): the broker answered with an empty or sparse body. Usually a nonexistent code or closed market. Verify the code with `kis stock basic-info` before retrying.
- `CredentialsMissing` / `AuthenticationError` (exit 3): stop and report; do not retry.
