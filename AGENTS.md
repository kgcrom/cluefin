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

The gate is **zero new issues of minor severity or above**; the complexity/duplication metrics are
shown but don't fail it. `.codacy.yml` excludes `packages/cluefin-openapi-ts/scripts/**`.

### Run it locally before pushing (partial coverage)

`CODACY_API_TOKEN`, `CODACY_ORGANIZATION_PROVIDER`, `CODACY_USERNAME`, `CODACY_PROJECT_NAME` are
already exported in the maintainer's shell (CI uses the same names as secrets).

```bash
brew install codacy/codacy-cli-v2/codacy-cli-v2
# The project's real rule set. Bare `codacy-cli init` uses defaults and finds almost nothing.
# The rule download is large and often times out ("context deadline exceeded") — just rerun it.
codacy-cli config reset --api-token "$CODACY_API_TOKEN" --provider "$CODACY_ORGANIZATION_PROVIDER" \
  --organization "$CODACY_USERNAME" --repository "$CODACY_PROJECT_NAME"
codacy-cli install                       # first run downloads runtimes/tools, ~2 min
codacy-cli analyze --tool opengrep --format sarif -o /tmp/opengrep.sarif packages/cluefin-openapi-ts
codacy-cli analyze --tool eslint   --format sarif -o /tmp/eslint.sarif   packages/cluefin-openapi-ts
```

- It writes `.codacy/` into the repo — put it in `.git/info/exclude`, or run it in a throwaway
  worktree. `analyze` takes **one** path (Trivy fails on several); without `--tool` it runs every
  tool. Read the SARIF's `results[].locations[0].physicalLocation` for `file:line`.
- **Coverage is partial — don't treat a clean local run as a pass.** Replaying PR #132's failing
  commit, the local run caught only the 2 dynamic-`RegExp` findings (opengrep
  `non-literal-regexp`) out of 19, plus an unrelated ESLint `no-undef` the server never reported.
  The local ESLint config has no security / typescript-eslint plugins, so object-injection,
  "Unnecessary conditional", hardcoded-password and generic-call findings only show up on the server.

### Read what the server found (ground truth)

A failing `gh pr checks` only gives a link and the Codacy web page needs a login. The PR comment has
the summary; the check run's annotations have every finding as `file:line`:

```bash
sha=$(gh pr view <N> --json headRefOid -q .headRefOid)
id=$(gh api repos/kgcrom/cluefin/commits/$sha/check-runs -q '.check_runs[]|select(.name|test("Codacy"))|.id')
gh api "repos/kgcrom/cluefin/check-runs/$id/annotations?per_page=100" \
  -q '.[]|"\(.annotation_level) \(.path):\(.start_line) \(.message)"'
```

- Codacy's own API also answers with the same token:
  `GET https://app.codacy.com/api/v3/analysis/organizations/gh/kgcrom/repositories/cluefin/pull-requests/<N>/issues?status=new`
  with header `api-token: $CODACY_API_TOKEN` (returns `{analyzed, data, pagination}`). `.../commits/<sha>/issues`
  is a 404; `.../commits/<sha>/deltaStatistics` works. Item fields of `data` were not checked (empty
  at the time).
- Right after a push the check run for the new head has `conclusion: null` (and `gh pr checks`
  may say "no checks reported"). That is "still analysing", not a pass — poll until the
  conclusion is set before reading annotations.

### Recurring TypeScript findings and what actually fixes them

- `// eslint-disable-next-line security/detect-object-injection` is **ignored** — restructure
  instead: `Map.get`, iterate `Object.entries`, collect `[key, value]` pairs and
  `Object.fromEntries` them. Both reads *and* assignments with a dynamic key are flagged, in tests too.
- `new RegExp(variable)` is flagged critical (also reproduces locally) — scan with `indexOf`, or
  use a literal regex.
- "Unnecessary conditional" on `match[1] ?? ''` or `x !== undefined`: Codacy analyses without
  `noUncheckedIndexedAccess`, so index access and destructured groups look non-nullable. Use
  named groups with truthiness checks (`groups.name ? … : …`) rather than `??` on an index.
- A string literal assigned to a name containing key/secret/password is reported as a hardcoded
  password, even in tests — generate the dummy at runtime (`randomUUID()`).

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
