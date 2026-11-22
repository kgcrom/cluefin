# AGENTS.md

Cluefin is a research toolkit for Korean financial markets. Each AGENTS.md records only what exploring the repo
won't tell you. `apps/AGENTS.md` and `packages/AGENTS.md` cover their side; each app/package has its own on top.

## Secrets & real accounts

- `.env` and `.env.test` at the repo root hold real credentials — **never echo, print, or commit their values**.
- `.env` is the **production** pair (real brokerage account). `.env.test` is mock/dev for Kiwoom and NH PLUG only —
  its KIS side is still `KIS_ENV=prod`. Anything that loads `.env`, local CLI runs included, talks to a real account,
  and a KIS integration test does too: check that the call is read-only before running it.
- A lookup still issues a real token (KIS: one issue per minute, `EGW00133` if sooner — wait a minute, retry once).
- Company names and receipt/accession numbers from the local filing corpora (`docs/plans/*-corpus/`) never go into
  code, fixtures, docs, commits or PRs. Write "checked against large-cap and unlisted filings" instead.

## Testing policy

- Real API keys are used **only** by tests marked `integration`; everything else is mocked and hits no network.
- `realtime`-marked tests run only when `-m` names both `integration` and `realtime`, inside market hours (KRX stocks
  09:00–15:20 KST — after 15:20 is the closing auction and no trades arrive; bonds until 15:30; US 09:30–16:00 ET).
  The gate does not know holidays, so they fail on one. `mutation` places real orders; its opt-in rules are in
  `packages/cluefin-openapi/AGENTS.md`.
- Integration tests read `.env.test` from the repo root whatever the cwd. A broker whose mock keys or mock account
  expired fails at authentication for every test — suspect the account before the code (symptoms in
  `packages/cluefin-openapi/AGENTS.md`).
- Test files are `test_<target>_unit.py` / `test_<target>_integration.py`, flat under `tests/` (subfolders only per
  broker/feed). Shared helpers are `_`-prefixed modules imported relatively, never via `sys.path` edits.
- The CI workflow (lint, typecheck, tests) runs on pushes to main, not on PRs: `gh workflow run ci.yml --ref <branch>`.
  Commits touching only `*.md`/`docs/` skip it — except `apps/cluefin-openapi-cli/README.md` and `AGENTS.md`, which
  unit tests read and execute (every fenced `uv run cluefin-openapi-cli …` line). Editing those two is a code change.

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
- Treat the server annotations as the source of truth. `codacy-cli` was tried and removed (2026-10): its ESLint
  lacks the security / typescript-eslint plugins, so it reproduced 2 of 19 server findings, and it pulls ~3 GB.
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
- The main checkout's absolute path is outside the repository for git, and its untracked files aren't in the worktree
  (`docs/plans/` included — read a plan by its absolute path).
- The first push from a fresh worktree fails in the pre-push `node-test` right after `npm ci`; pushing again passes
  (seen twice, 2026-11-04). Run `npm ci` in `packages/cluefin-openapi-ts` first if `node_modules` is missing.

## Conventions

- Conventional Commits with **Korean** messages: `type(scope): 설명`.
- Git hooks are lefthook (`uv run lefthook install`), not the `pre-commit` framework. pre-commit only checks (ruff
  `--check`, no auto-fix); pre-push runs pyright over the whole include list because a changed helper can break a
  caller nobody touched (#196).
- `docs/plans/` is deliberately **not** in `.gitignore` (ignored files can't be `@`-mentioned) and is never committed:
  stage by path, never `git add .`/`-A`. Only its corpus subfolders are ignored. Finished plans are deleted, not
  marked done; what is left to do lives in `docs/plans/TODO.md`, and a constraint worth keeping moves to an AGENTS.md.
- Internal results and value objects are `@dataclass(frozen=True, slots=True)`, changed with `dataclasses.replace`;
  pydantic only for external API (wire) models. Any other option set carries a one-line `#` reason above it.
- Logging is stdlib `logging.getLogger(__name__)` with f-string messages (loguru `{}` args don't format; `%s` args
  trip Codacy when the text mentions token/key). Only app entry points add handlers or set levels; tests use `caplog`.

## Analysis agents

기업 분석(대화형 분석·HTML 리포트·지난 판단 재검토)은 메인 대화가 `.claude/agents/company-review.md` 를 따른다.
판단(`research/verdicts.jsonl`)과 HTML 리포트(`research/reports/`)는 gitignore 된 로컬 기록이다. worktree 에서도
`review record` 는 메인 체크아웃의 `research/` 에 쓰므로, 리포트 파일도 그 경로에 둔다.

스크린에서 검토로 이어 갈 때(결정 2026-11-22): 메인 대화가 `cache screen --preset <이름> --compare-as-of <지난달> --json` 을
돌리고, `compare.in` 종목과 상위 10개(겹치면 한 번)를 company-review 서브에이전트로 병렬 검토한다. 리포트는 종목별
company-review 리포트뿐이다 — 스크린 결과를 따로 요약 문서로 만들지 않는다.
