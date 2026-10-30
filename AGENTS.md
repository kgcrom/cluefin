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
- Test files are `test_<target>_unit.py` or `test_<target>_integration.py`, flat under each package's
  `tests/` (subfolders only per broker/feed). Shared helpers are `_`-prefixed modules imported
  relatively (`from ._helpers import …`), never via `sys.path` edits.

## Codacy (PR check)

The gate is **zero new issues of minor severity or above**; the complexity/duplication metrics are
shown but don't fail it.

### How a failing check gets resolved (the loop that took 19 findings to 0)

1. `gh pr checks <N>` says `fail` and gives only a link; the web page needs a login. Don't stop there.
2. The Codacy bot's **PR comment** has the counts by category and severity
   (`gh pr view <N> --json comments`), e.g. "8 critical · 11 high" → Security 8 critical / 4 high,
   ErrorProne 7 high. This tells you how bad it is, not where.
3. The check run's **annotations** give every finding as `file:line: message` (command below). Severity
   maps as `failure` = critical, `warning` = high/other — the 8 `failure`s matched the "8 critical".
   Start with those.
4. Group the findings by message, not by file: 19 findings were really four patterns (dynamic RegExp,
   dynamic-key object access, "Unnecessary conditional", hardcoded password). Fix the pattern, not the line.
5. Push, **wait for the new head's check run to get a conclusion**, read the annotations again. A fix can
   expose the next layer (19 → 6: fixing only the dynamic *read* left the dynamic *assignment* flagged).
   Repeat until `Your pull request is up to standards!`.

### Don't bother reproducing it locally

`codacy-cli` (Codacy's own local runner) was tried and removed (2026-10). Even with the project's
real rule set (`config reset --api-token …`), running it on a branch the server had failed with 19
findings reproduced only the 2 dynamic-`RegExp` ones: the CLI's ESLint config has no security /
typescript-eslint plugins, so object-injection, "Unnecessary conditional", hardcoded-password and
generic-call findings exist only on the server. It also pulls ~3 GB of runtimes and writes `.codacy/`
into the repo. Push, read the server result below, and fix with the patterns at the bottom.
`.codacy.yml` excludes `packages/cluefin-openapi-ts/scripts/**`.

### Read what the server found (ground truth)

A failing `gh pr checks` only gives a link and the Codacy web page needs a login. The PR comment has
the summary; the check run's annotations have every finding as `file:line`:

```bash
sha=$(gh pr view <N> --json headRefOid -q .headRefOid)
id=$(gh api repos/kgcrom/cluefin/commits/$sha/check-runs -q '.check_runs[]|select(.name=="Codacy Static Code Analysis")|.id')
gh api "repos/kgcrom/cluefin/check-runs/$id/annotations?per_page=100" \
  -q '.[]|"\(.annotation_level) \(.path):\(.start_line) \(.message)"'
# critical only: add  select(.annotation_level=="failure")|  before the string
```

- Codacy's own API also answers with the same token:
  `GET https://app.codacy.com/api/v3/analysis/organizations/gh/kgcrom/repositories/cluefin/pull-requests/<N>/issues?status=new`
  with header `api-token: $CODACY_API_TOKEN` (returns `{analyzed, data, pagination}`). `.../commits/<sha>/issues`
  is a 404; `.../commits/<sha>/deltaStatistics` works. Item fields of `data` were not checked (empty
  at the time).
- Right after a push the check run for the new head has `conclusion: null` (and `gh pr checks`
  may say "no checks reported"). That is "still analysing", not a pass — poll until the
  conclusion is set before reading annotations.
- Select the check by its exact name, `Codacy Static Code Analysis`. Since #186 a PR also gets `Codacy Diff Coverage`
  and `Codacy Coverage Variation`; matching `test("Codacy")` can pick a coverage check and read its success as the
  analysis result.
- The CI workflow (`ci.yml`: lint, typecheck, tests) runs on pushes to main, not on PRs. To see it before merging, run
  it on the branch: `gh workflow run ci.yml --ref <branch>`.

### Recurring TypeScript findings and what actually fixes them

These came from the `src/dart` client (19 findings, then 6 after a first fix, then 0). The "after"
shapes are in `src/dart/client.ts` and `src/dart/xml.ts`.

- **Dynamic-key object access** (`security/detect-object-injection`, "Generic Object Injection Sink").
  A `// eslint-disable-next-line security/detect-object-injection` comment is **ignored**, so
  restructure. Reads *and* assignments are both flagged, in tests too.
  - Before: building the query string from endpoint metadata with
    `for (const [wireKey, inputKey] of Object.entries(queryMap)) query[wireKey] = String(parsed[inputKey])`.
    Fixing only the read (`parsed[inputKey]`) still left `query[wireKey] = …` flagged.
  - After: invert the map once (`new Map(inputKey → wireKey)`), walk `Object.entries(parsedInput)`,
    push `[wireKey, String(value)]` into an array, then `Object.fromEntries(entries)`. The same applies
    to the XML parser's per-item object (`item[tag] = …` became a `childEntry` helper returning
    `[tag, text]`).
  - Tests that called `service[methodName](input)` (method name from a table) were flagged as
    "non-static data to retrieve and run functions". After: `new Map(Object.entries(service)).get(name)`
    where only the existence/path is checked, and a table of call lambdas
    (`(s) => s.getFoo(input)`) where the typed response is used.
- **`new RegExp(variable)`** (critical; the only class the local CLI also reproduces). The XML helper
  built a regex per call from the tag name, ``new RegExp(`<${tag}>…</${tag}>`)``. After: `indexOf` on the
  opening and closing tag (`findElement`), and a literal regex only for the fixed child pattern.
- **"Unnecessary conditional"** on `match[1] ?? ''`, `child[2] ?? ''`, `x !== undefined`. Codacy analyses
  without `noUncheckedIndexedAccess`, so array/group access looks non-nullable and `??` looks dead
  (while the repo's own tsconfig does flag the missing `?? ''`). After: named regex groups read with
  truthiness (`if (groups.name) …`, `groups.body || ''`) instead of `??` or `!== undefined`; the
  branching lives in a small helper so the loop body stays flat.
- **Hardcoded password** on a test constant like `const AUTH_KEY = 'secret-auth-key-0123…'`
  (a literal assigned to a name containing key/secret/password, even in tests). After: build the dummy
  at runtime, `` `test-${randomUUID()}` `` — which also suits a test whose point is that the value must
  never appear in errors or logs.

### Python: any `import` from the stdlib `xml` package is a critical finding

- Even a type-only import (`from xml.etree.ElementTree import Element` under `TYPE_CHECKING`) or
  `xml.parsers.expat.errors` is flagged as XXE. After: a `Protocol` with the element methods you use
  (`cluefin_dart_notes/_xml.py`), and literal values for expat constants.
- Parse with `defusedxml` and keep it (decided 2026-10). The stdlib parser already refuses external
  entities, but the bundled expat on 3.10–3.14 is 2.6.3, and Python's docs call < 2.7.2 possibly
  vulnerable to entity-expansion and large-token DoS; `defusedxml` forbids entity declarations outright.
  Its stable release is still 0.7.1 (0.8.0 stuck at rc since 2023-09) but it works on 3.10–3.14.

### Python: nested quantifiers in a regex are a critical finding

- "Detected usage of re.compile with an inefficient regular expression" (critical) fires on a
  quantified group inside another quantified group. The case was a combined-label pattern for
  "Items 10, 11 and 12": `{N}(?:\.?(?:\s*(?:,|and|&))+\s*{N})*`.
- After: keep each regex flat (one number, one separator) and loop in code with
  `pattern.match(text, pos)` (`_read_numbers` in `cluefin_sec_notes/_labels.py`). Same results, linear time.
- A mutable default argument (`def f(items=SOME_LIST)`) is a high finding, tests included. Use a tuple.
- `importlib.import_module(<non-literal>)` is a critical "untrusted input loads arbitrary code" finding, tests
  included (#186: a test importing every `*_types.py` by path). Scan the source with `ast` instead of importing,
  as `tests/test_response_models_unit.py` does.
- A stdlib logger call whose message mentions a token/secret/key **and** passes `%s` arguments is a high
  "potential hardcoded secret being logged" finding, even when the argument is a timestamp or path (6 in the
  Kiwoom token manager, #181; loguru calls were never matched). Put the values in an f-string, like the KIS/NH
  token managers, and never log the token itself.

## Environment gotchas

- macOS system dep: `brew install lightgbm` (a runtime dep of `cluefin-desk`). The C
  TA-Lib needs no install: `ta-lib>=0.6` wheels bundle `libta-lib` for every platform in
  the lock (3.11–3.14, macOS/Linux/Windows). It is only `cluefin-ta`'s dev-group test
  oracle; no app imports `talib`.
- Git hooks run via **lefthook** (`uv run lefthook install`) — not the `pre-commit` framework.
- Type checking is `uv run pyright` (basic mode) over the `[tool.pyright] include` list in the root
  `pyproject.toml`; CI's `typecheck` job fails on any error there. Packages are added one at a time once their
  errors are 0 — packages not in the list are unchecked, not clean. pydantic models with `populate_by_name` still
  type-check against the alias only, so construct them by alias.

## Conventions

- Conventional Commits with **Korean** messages: `type(scope): 설명`.
- When discovering broker commands, prefer `cluefin-openapi-cli`'s `--json` output.
- 사용자와 대화하며 하는 기업 분석과 HTML 리포트("리포트 생성")는 메인 대화가 맡는다. 판단 기준은
  `.claude/agents/market-review.md` 의 데이터·분석·판단 절, HTML 은 생성 요청 시에만 `docs/agents/market-review-report-design.md`.
- "Today"/"now" is KST, not the machine's zone (ruff `DTZ`): apps use `clock.today_kst()`/`now_kst()`
  (`cluefin_openapi_cli.clock`, `cluefin_desk.clock`). Token caches stay naive local time — the TS package shares them.
- Internal results and value objects are `@dataclass(frozen=True, slots=True)`; build changed copies with
  `dataclasses.replace`. pydantic is only for external API (wire) models. Any other option set carries a one-line
  `#` reason above the decorator (mutable accumulators/builders, `eq=False` for identity, bases a `BaseModel` also
  inherits).
- Logging is stdlib: `logger = logging.getLogger(__name__)` at module level; f-string messages (loguru's `{}` args
  don't format in stdlib, and `%s` args trip Codacy when the text says token/key — see Codacy above).
  Packages never add handlers or set levels; only app entry points do (`cluefin_openapi_cli.main._configure_logging`,
  `cluefin_desk.app._configure_logging`). Tests read logs with `caplog`.
- Apps import clients, auth, services and exceptions from the broker package (`from cluefin_openapi.kis import
  Auth`), not its `_`-modules. Response models are the exception: only kis realtime and ecos re-export them, so
  `cluefin_openapi.<broker>._*_types` is the path. Patch targets in tests follow the import path the app uses.
- `packages/*/examples/*.ipynb` 노트북은 커밋 전에 output·execution_count 를 지운다
  (출력에 계좌번호가 섞일 수 있다):
  `uv run --with jupyter jupyter nbconvert --clear-output --inplace <노트북>.ipynb`
