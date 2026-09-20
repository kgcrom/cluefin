---
name: cluefin-openapi-cli
description: Query Korean market data (quotes, charts, rankings, financials, sector/theme, ETF, corporate actions, DART filings) through the cluefin-openapi-cli. KIS is the primary broker; Kiwoom fills gaps; DART is reference. Use for any task that needs Korean stock market or disclosure data.
---

# cluefin-openapi-cli

Run every command from the workspace root with `uv run cluefin-openapi-cli ...`. Output is JSON; parse it, never scrape text.

## Invariants

- **Start from `search`.** `search <자연어 설명> --json` returns a ranked shortlist (default 8, ~3KB) and never returns an empty result — a miss carries `fallback` with runnable next steps. Use it before `list`. A bare `list --json` is a 61KB catalog dump; never call one.
- **Tags are authored, not inferred.** `domains`/`tags` are set per command, so `--tag`/`--domain` narrow precisely. Prefer them over `--query` for well-known concepts.
- **Start with KIS.** KIS is the primary broker, Kiwoom is auxiliary, DART is reference. Call `list --broker kis --json` first. Use a `kiwoom` command only when its `kis_alternatives` is `[]`, or the KIS call returned no usable data. Never call Kiwoom for something KIS covers.
- **Latest results come from DART, ratios from KIS.** `kis financial *` returns annual rows for most stocks and lags the newest filing on small caps. For the most recent half-year or quarter, or to verify a reported number against the filing, resolve `corp_code` with `dart corp-code-lookup` and call `dart financial-major-accounts` with `--reprt-code` (11013 Q1 · 11012 H1 · 11014 Q3 · 11011 annual). In quarterly reports `thstrm_amount` is that quarter alone and `thstrm_add_amount` is year-to-date.
- **Read the schema before the first call.** `schema <broker> <category> <name> --json` gives the JSON Schema, one `--flag` per parameter, and ready-to-run `invoke.*` strings. Do not guess parameter names or code values; `enum` and `pattern` are enforced locally.
- **Dry-run before a new command shape.** Add `--dry-run` the first time you build a call. It validates and echoes the resolved `params` without touching the network or issuing a token.
- **Keep responses small.** Always pass `--fields` with the keys you actually need, plus `--limit N` for any command that returns rows, plus `--compact`. When data was cut you get `_truncated` with the real `total` — check it before concluding anything. `list` is brief by default; filter it. Unfiltered `list --full` returns only the first 25 rows (`--limit 0` for all).
- **Branch on exit code, then `error.retryable`.** 0 ok · 1 internal · 2 fix your arguments · 3 credentials · 4 broker/network (retry once only if `retryable` is true) · 5 rate limited (wait `data.retry_after`, default 1s). Never retry a 2 or 3 as-is.
- **Every command is read-only.** There is no order or account-mutating command. Running any kis/kiwoom command still uses the real account credentials from `.env` in the current directory.
- **Never print credentials.** `brokers --json` tells you `credentials.configured` per broker without exposing values; that is the only credential check you need.

## Workflow

```bash
uv run cluefin-openapi-cli search 외국인 순매수 상위 종목 --json        # ranked candidates, ~3KB
uv run cluefin-openapi-cli brokers --json                                # roles, configured?, kiwoom-only list
uv run cluefin-openapi-cli list --broker kis --domain quote --json       # or --tag, --category, --query
uv run cluefin-openapi-cli kis chart --help --json                      # category description + its commands
uv run cluefin-openapi-cli schema kis stock current-price --json
uv run cluefin-openapi-cli kis stock current-price --stock-code 005930 --dry-run --json
uv run cluefin-openapi-cli kis stock current-price --stock-code 005930 --fields current_price,per,pbr --compact
uv run cluefin-openapi-cli kis chart daily --stock-code 005930 --fields output.stck_clpr --limit 20 --compact
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
- Nothing found: `search` never returns an empty result. Read `fallback.did_you_mean`, `fallback.nearest_domains[].example_filter`, and `fallback.recipes[].next` — each is runnable verbatim. Do not fall back to dumping `list --json`.
