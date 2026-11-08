# AGENTS.md

Cluefin is a research toolkit for Korean financial markets. Each AGENTS.md records only what exploring the repo
won't tell you. `apps/AGENTS.md` and `packages/AGENTS.md` cover their side; each app/package has its own on top.

## Secrets & real accounts

- `.env` and `.env.test` at the repo root hold real credentials — **never echo, print, or commit their values**.
- `.env` is the **production** pair (real brokerage account). `.env.test` is mock/dev for Kiwoom only — its KIS side
  is still `KIS_ENV=prod`. Anything that loads `.env`, local CLI runs included, talks to a real account.

## Testing policy

- Real API keys are used **only** by tests marked `integration`; everything else is mocked and hits no network.
- `realtime`-marked tests require market hours (09:00–15:30 KST).
- Test files are `test_<target>_unit.py` / `test_<target>_integration.py`, flat under `tests/` (subfolders only per
  broker/feed). Shared helpers are `_`-prefixed modules imported relatively, never via `sys.path` edits.
- The CI workflow (lint, typecheck, tests) runs on pushes to main, not on PRs: `gh workflow run ci.yml --ref <branch>`.

## Codacy (PR check)

The gate is **zero new issues of minor severity or above**; complexity/duplication are shown but don't fail it.
`gh pr checks` gives only a login-walled link — read the findings from GitHub instead, one call at a time:

```bash
gh pr view <N> --json comments          # bot comment: counts by category and severity
gh pr view <N> --json headRefOid -q .headRefOid
gh api repos/kgcrom/cluefin/commits/<sha>/check-runs -q '.check_runs[]|select(.name=="Codacy Static Code Analysis")|.id'
gh api "repos/kgcrom/cluefin/check-runs/<id>/annotations?per_page=100" -q '.[]|"\(.annotation_level) \(.path):\(.start_line) \(.message)"'
```

- `failure` = critical, `warning` = high/other. Group findings by message, not file — 19 findings were four patterns.
- Select the check by its exact name: `Codacy Diff Coverage`/`Coverage Variation` also match "Codacy" and pass.
- Right after a push the new head's run has `conclusion: null` — still analysing, not a pass. Poll until it is set;
  a fix can expose the next layer (19 → 6 → 0).
- Don't reproduce locally: `codacy-cli` was tried and removed (2026-10). Its ESLint lacks the security /
  typescript-eslint plugins, so it reproduced 2 of 19 server findings, and it pulls ~3 GB of runtimes.
- Fix patterns: Python in `packages/AGENTS.md`, TypeScript in `packages/cluefin-openapi-ts/AGENTS.md`.

## Shell commands in a worktree session

A worktree-isolated session refuses commands it can't prove don't run git outside the worktree (measured 2026-11-03):

- Refused, **not only git**: a `$(...)` value passed to a command that could run git (`sha=$(gh …); gh api …/$sha`,
  `x=$(…); uv run cluefin-openapi-cli $x`), and a loop with `gh` inside `$(...)`.
- Refused, git only: git with `$?`, in a `for` loop, or `git -C <another dir>`.
- Runs: plain commands joined by `|` `;` `&&`, a plain variable, a non-git loop with literal arguments, `bash -c '…'`.
- So: **one command per Bash call**, paste literal values (sha, check-run id) into the next call, and send
  independent calls in parallel. Poll with a pipe in a background call:
  `until gh pr checks <N> | grep -E 'Codacy Static Code Analysis[[:space:]]+(pass|fail)'; do sleep 20; done`.
- The main checkout's absolute path is outside the repository for git, and its untracked files aren't in the worktree.

## Conventions

- Conventional Commits with **Korean** messages: `type(scope): 설명`.
- Git hooks are lefthook (`uv run lefthook install`), not the `pre-commit` framework.
- Internal results and value objects are `@dataclass(frozen=True, slots=True)`, changed with `dataclasses.replace`;
  pydantic only for external API (wire) models. Any other option set carries a one-line `#` reason above it.
- Logging is stdlib `logging.getLogger(__name__)` with f-string messages (loguru `{}` args don't format; `%s` args
  trip Codacy when the text mentions token/key). Only app entry points add handlers or set levels; tests use `caplog`.
- 사용자와 대화하며 하는 기업 분석과 HTML 리포트("리포트 생성")는 메인 대화가 맡는다. 판단 기준은
  `.claude/agents/company-review.md` 의 수집·데이터·분석·판단 절(데이터는 `review collect` 로 폴더에 받는다), HTML 은 생성
  요청 시에만 `docs/agents/company-review-report-design.md`.
- agent 는 `.claude/agents/` 의 넷이다: company-review(종목 하나), market-scan(장세·후보, 판단 없음), disclosure-watch
  (관심 종목 공시), agent-audit(실행 감사). 감사는 사람이 원할 때만 수동으로 한다 — `cluefin-openapi-cli audit check` 로
  결정적 검사, agent-audit 로 놓침 판독. 감사는 판단 적중(수익률)을 평가하지 않는다 — 적중은 `review track` 이 따로 본다. agent 데이터 절을 고치면 그 파일 끝
  `audit` 블록도 같이 고친다.
