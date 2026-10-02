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

## Codacy (PR check)

- The gate is **zero new issues of minor severity or above**; complexity/duplication metrics
  are shown but don't fail it. It runs on Codacy's servers, so it can't be reproduced locally
  — read the findings, fix, push.
- A failing `gh pr checks` only gives a link, and the Codacy web page needs a login. Read the
  findings from GitHub instead — the PR comment has the summary, and the check run's
  annotations have every finding as `file:line`:
  ```bash
  sha=$(gh pr view <N> --json headRefOid -q .headRefOid)
  id=$(gh api repos/kgcrom/cluefin/commits/$sha/check-runs -q '.check_runs[]|select(.name|test("Codacy"))|.id')
  gh api "repos/kgcrom/cluefin/check-runs/$id/annotations?per_page=100" \
    -q '.[]|"\(.annotation_level) \(.path):\(.start_line) \(.message)"'
  ```
- Right after a push the check run for the new head has `conclusion: null` (and `gh pr checks`
  may say "no checks reported"). That is "still analysing", not a pass — poll until the
  conclusion is set before reading annotations.
- TypeScript findings that recur and what actually fixes them:
  - `// eslint-disable-next-line security/detect-object-injection` is **ignored** — restructure
    instead (`Map.get`, iterate `Object.entries`, no `obj[dynamicKey]`, also in tests).
  - `new RegExp(variable)` is flagged critical — scan with `indexOf`, or use a literal regex.
  - "Unnecessary conditional" on `match[1] ?? ''`: Codacy analyses without
    `noUncheckedIndexedAccess`, so index access looks non-nullable. Use named groups or
    destructuring defaults rather than `??` on an index.
  - A string literal assigned to a name containing key/secret/password is reported as a
    hardcoded password, even in tests — generate the dummy at runtime.

## Environment gotchas

- macOS system deps: `brew install lightgbm ta-lib`. `lightgbm` is a runtime dep of
  `cluefin-desk`; the C `ta-lib` is **only** needed to run `cluefin-ta`'s parity tests
  (they `import talib` at module level with no skip guard). No app imports `talib`, and
  `cluefin-ta` itself is pure Python — skip the `ta-lib` install if you are not running
  those tests.
- Git hooks run via **lefthook** (`uv run lefthook install`) — not the `pre-commit` framework.

## Conventions

- Conventional Commits with **Korean** messages: `type(scope): 설명`.
- When discovering broker commands, prefer `cluefin-openapi-cli`'s `--json` output.
- `packages/*/examples/*.ipynb` 노트북은 커밋 전에 output·execution_count 를 지운다
  (출력에 계좌번호가 섞일 수 있다):
  `uv run --with jupyter jupyter nbconvert --clear-output --inplace <노트북>.ipynb`
