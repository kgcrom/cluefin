# cluefin-openapi-cli

`cluefin-openapi-cli`는 `cluefin-openapi`의 broker API를 **AI agent가 직접 호출하는 용도**로 노출하는 명령줄 인터페이스입니다. 사람이 읽는 화면이 아니라, agent가 JSON을 읽고 다음 명령을 조립하는 것을 전제로 설계했습니다.

- 모든 출력은 JSON입니다. `--json`을 주거나 stdout이 TTY가 아니면 자동으로 JSON입니다.
- 어떤 API를 호출할 수 있는지(`search`, `brokers`, `list`), 어떤 parameter를 받는지(`schema`)를 CLI 자체가 JSON으로 알려줍니다. 외부 문서를 미리 읽을 필요가 없습니다.
- 실행 전 `--dry-run`으로 parameter를 로컬 검증하고, 실패는 exit code와 구조화된 `error` JSON으로 돌려줍니다.

그래서 이 문서에는 명령·옵션 목록이 없습니다. 처음 돌릴 때 걸리는 곳, 명령을 쓰는 순서, `trend-setup` 규칙의 근거만 적습니다. agent 가 따르는 규칙과 broker 별 실측 함정은 [AGENTS.md](AGENTS.md) 에 있습니다.

## Broker 역할

| broker | role | 언제 쓰나 |
|---|---|---|
| `kis` | **primary** | 모든 작업의 시작점. 시세·차트·순위·수급·업종·ETF·일정 |
| `kiwoom` | **auxiliary** | KIS 에 없는 것만 — 테마, 업종 구성종목, 틱 차트, 프로그램매매 상세, 거래원 수급 |
| `dart` | reference | 한국 공시와 재무제표. 실적 숫자는 여기서만 받는다(KIS 재무제표·재무비율 API 는 2026-11-11 서비스 종료로 없앴다) |
| `sec` | reference | 미국 고객사·경쟁사의 10-K/10-Q/8-K. 20-F/6-K(한국 ADR 대부분)는 읽지 못한다 |
| `ecos` | reference | 한국은행 금리·환율·물가·경기 통계. `ECOS_AUTH_KEY` 가 없으면 공개 `sample` 키(한 번에 10행)로 돈다 |

Kiwoom command에는 `kis_alternatives` 필드가 있습니다. 비어 있지 않으면 같은 질문을 KIS로 먼저 풀어야 하고, 비어 있으면 그것이 Kiwoom을 쓰는 이유입니다. `brokers --json`의 `kiwoom_only_commands`가 그 목록입니다.

## 빠른 시작

워크스페이스 루트에서 실행합니다.

```bash
uv sync --all-packages
uv run cluefin-openapi-cli --json
```

실제 API 호출 전에는 루트 `.env` 또는 환경변수가 필요합니다. CLI는 현재 작업 디렉터리의 `.env`를 읽고, 같은 키가 환경변수에도 있으면 환경변수가 우선합니다.

```env
KIS_APP_KEY=...
KIS_SECRET_KEY=...
KIWOOM_APP_KEY=...
KIWOOM_SECRET_KEY=...
DART_AUTH_KEY=...
SEC_USER_AGENT="Your Name your.email@example.com"   # SEC는 키 대신 User-Agent에 이름·이메일을 요구한다
ECOS_AUTH_KEY=...   # 선택. 없으면 공개 sample 키(한 번에 10행, 쪽 넘김으로 이어 받음)
```

어느 broker가 설정돼 있는지는 값을 노출하지 않고 `brokers --json`의 `credentials.configured`로 확인합니다.

- **저장소 루트에서 부릅니다.** `.env` 는 현재 디렉터리에서만 찾으므로 `apps/cluefin-openapi-cli` 안에서 부르면 exit 3 `CredentialsMissing` 입니다.
- **루트 `.env` 는 실계좌 자격증명입니다.** 주문 명령은 없지만(모든 command 가 `side_effect: "read"`) 조회만 해도 실제 토큰이 발급됩니다. `--dry-run` 만 토큰을 발급하지 않습니다.

## Agent 워크플로

```bash
uv run cluefin-openapi-cli search 외국인 순매수 --json                    # 0. 자연어 → 순위가 매겨진 후보 (권장 시작점)
uv run cluefin-openapi-cli brokers --json                              # 1. 역할·설정 상태·Kiwoom 전용 목록
uv run cluefin-openapi-cli list --broker kis --domain chart --json     # 2. 후보 command (brief)
uv run cluefin-openapi-cli schema kis stock current-price --json       # 3. parameter JSON Schema + 호출 예시
uv run cluefin-openapi-cli kis stock current-price --stock-code 005930 --dry-run --json   # 4. 로컬 검증
uv run cluefin-openapi-cli kis stock current-price --stock-code 005930 --fields current_price,per --json  # 5. 실행
```

- `search` 는 순위를 매긴 후보를 주고, 맞는 것이 없으면 빈 배열 대신 `fallback`(가까운 domain·tag·recipe)을 줍니다. `list --query` 는 이름·설명의 **리터럴 부분 문자열 필터**라 한국어·자연어 질의에는 맞지 않습니다.
- `list --json` 을 필터 없이 부르면 약 130KB(`--compact` 약 90KB, 2026-11-15)입니다. agent 맥락에 넣기엔 크므로 `--broker`·`--domain`·`--tag` 로 좁힙니다.
- 여러 command 를 엮는 일은 `recipes --json` → `recipe <name> --json` 에 순서와 주의사항(`agent_notes`)이 있습니다. recipe 는 실행기가 아니라 안내입니다.
- `cache`·`review`·`audit` 은 broker command 가 아니라서 `search`·`list`·`schema` 에 나오지 않습니다. `cache --help --json` 처럼 `--help` 로 봅니다.

### 입력과 출력에서 걸리는 곳

- `--fields a,b.c` 는 없는 키를 조용히 생략합니다. 응답이 비어 보이면 mask 없이 한 번 불러 반환 키를 확인합니다.
- `--limit N` 은 결과 배열을 N행으로 자르고 `--fields` 다음에 적용됩니다. 실제로 잘린 경우에만 `_truncated` 에 `limit`·`path`·`returned`·`total` 이 붙고, 최상위가 리스트면 `{"items": [...], "_truncated": {...}}` 로 감쌉니다 — 잘렸을 때만 shape 이 바뀝니다. broker command 에는 암묵 기본값이 없습니다(20행짜리 일봉은 유효한 20일 차트처럼 보이므로 조용히 자르지 않습니다).
- broker command 의 boolean parameter 는 값 없이 주면 true 입니다(`--listed-only`). `cache`·`review`·`audit` 의 옵션은 값을 받아야 합니다(`--history true`, 값이 없으면 exit 2).
- 배열·객체 parameter 는 `--params-json` 으로 넘기고, 같은 필드를 flag 로도 주면 flag 가 이깁니다.
- 문자열 값에 제어문자, `..`, `%`, `?`, `#` 가 있으면 broker 를 부르기 전에 exit 2 로 거부합니다(중첩 JSON 안쪽도 검사).

## 오류와 exit code

실패하면 stdout 에 `error` 객체 하나(`type`·`message`·`exit_code`·`retryable`·`hint`·`data`)만 나옵니다. agent 는 `exit_code` 와 `retryable` 로 분기합니다.

| exit | 의미 | agent 행동 |
|---|---|---|
| 0 | 성공 | |
| 1 | CLI/client 내부의 예상치 못한 실패 | 그대로 재시도하지 말 것 |
| 2 | usage·검증 오류 | `error.data.issues[]` 를 읽고 인자를 고친다. `schema`를 다시 본다 |
| 3 | 자격증명 누락·거부 (SEC는 `SEC_USER_AGENT` 누락·403) | `.env`/환경변수 확인. 재시도 무의미. SEC 403은 과속 차단(약 10분)일 수도 있다 |
| 4 | broker API·네트워크·타임아웃·응답 파싱 실패 | `retryable`이 true일 때만 한 번 재시도 |
| 5 | broker rate limit | `data.retry_after`초(없으면 1초 이상) 대기 후 재시도. 단 DART `data.status == "020"` 은 일일 한도라 반복 재시도 금지 |

`error.type` 예: `ValidationError`, `CredentialsMissing`, `AuthenticationError`, `RateLimitError`, `BrokerUnavailable`, `BrokerApiError`, `BrokerRejectedRequest`, `ResponseParseError`(존재하지 않는 종목코드처럼 broker가 빈 응답을 준 경우, 다른 회사의 공시), `NotFound`(SEC 404: CIK·접수번호 확인), `ExecutionError`.

## 로컬 일봉 캐시 (`cache`)

KIS 는 일봉을 한 번에 100행까지만 주므로 전 종목 횡단면 질의나 백테스트를 실시간 호출로는 할 수 없습니다. 그래서 상장 주식 전 종목(2016년 이후 폐지 종목 포함)과 지수의 일봉, 시장금리·환율, 키움 테마 스냅샷, DART 주요계정 5개년을 DuckDB 파일 하나(`~/.cache/cluefin/market.duckdb`, `CLUEFIN_CACHE_DIR` 로 변경)에 쌓습니다. `cache load` 만 broker 를 부르고(KIS·키움·DART·ECOS, 한 번에 하나씩) 나머지 하위 명령은 파일만 읽습니다.

```bash
uv run cluefin-openapi-cli cache load --json               # 장 마감 뒤(16시 이후)에
uv run cluefin-openapi-cli cache status --json
uv run cluefin-openapi-cli cache ohlcv --code 005930 --since 20260901 --adjusted true --json
uv run cluefin-openapi-cli cache base-rate-build --json    # `cache base-rate` 를 쓰기 전에 한 번
```

- **소요 시간.** `cache load` 첫 실행 ~2시간 20분, 이후 하루 ~7분(2026-10-18 실측 — 테마·재무 적재가 `all` 에 들어가기 전 값이고 그 뒤로 다시 재지 않았습니다). `cache base-rate-build` 첫 구축은 9분 45초(2026-11-03, 표본일 530개·486,382행)이고 이후는 증분입니다.
- **금리·환율(`rates`)은 `ECOS_AUTH_KEY` 가 있어야 받습니다.** sample 키면 오류 한 줄을 남기고 건너뜁니다.
- **일봉은 원주가입니다.** 수정주가는 `가격 × adj_factor` 입니다. 신호를 계산할 때는 `--adjusted true`, 백테스트 체결가는 원주가를 씁니다. `cache perf`·`rs`·`breadth`·`trend-setup` 은 스스로 수정주가로 계산합니다.
- **지수 코드는 `U0001` KOSPI · `U1001` 코스닥 · `U2001` KOSPI200 입니다.** 캐시에 지수 이름이 없어 `U1001` 을 KOSPI200 으로 읽기 쉽습니다. `kis chart trend-setup` 이 쓰는 KIS 업종코드 `0001`·`1001` 과 같은 지수입니다.
- **`company` 의 이름·업종·시장·상장주식수는 현재 값입니다**(과거 시점 값이 아님). 그래서 과거 날짜의 시총은 그날 종가 × 현재 주식수 근사입니다.
- **`cache financials` 는 `dart financial-summary` 와 단위·범위가 다릅니다.** 금액이 **원**이고(`financial-summary` 는 억원), 연간 표준 12개 계정뿐이며 지배/비지배 구분과 현금흐름표가 없습니다. `cache screen` 의 per·pbr·roe 가 `kis stock valuation` 의 지배주주 기준 값과 다른 이유입니다. 우선주 코드로 물으면 보통주의 행을 주고 `financials_code` 에 적습니다.
- **분기·TTM 은 `cache load --only financials_quarterly` 로 받고 `cache financials --period quarter|ttm` 으로 봅니다.** 1분기·반기·3분기 보고서를 최근 5년(상장폐지 포함) 받아 `financials_quarterly` 에 두고, 분기 3개월·TTM 은 `financials_ttm` 에 다시 계산합니다. 4분기 3개월은 연간 − 3분기 누적입니다. `cache screen` 의 `*_ttm`·`pbr_mrq`·`*_yoy_q` 가 이 표를 씁니다.
- `cache screen --preset <이름>` 은 `research/screens.toml` 의 `[이름]` 절(`where`·`sort`·`order`·`top`)을 읽습니다. `research/` 는 gitignore 된 내 폴더라 직접 만듭니다.

DuckDB 는 쓰는 동안 다른 프로세스가 파일을 열 수 없습니다. `cache load` 중의 읽기는 exit 1 `CacheLocked`, 첫 적재 전은 exit 2 `CacheMissing` 입니다.

DuckDB CLI(`brew install duckdb`, 캐시와 같은 1.5 계열)로 직접 SQL 을 쓸 수 있습니다. 켜 둔 동안은 `cache load` 가 못 쓰니 적재 전에 닫습니다.

```bash
duckdb -readonly ~/.cache/cluefin/market.duckdb          # SQL 셸, .quit 로 종료
# 브라우저 UI(http://localhost:4213): 메모리 DB 로 띄우고 캐시만 읽기 전용으로 붙인다
duckdb -cmd "ATTACH '$HOME/.cache/cluefin/market.duckdb' AS market (READ_ONLY); USE market; CALL start_ui();"
```

`duckdb -readonly -ui <파일>` 은 UI 가 자기 상태 카탈로그(`_duckdb_ui`)를 만들지 못해 `Catalog "_duckdb_ui" does not exist` 로 실패합니다.

## 종목 검토 기록과 감사 (`review`, `audit`)

종목 하나를 검토하려면 명령 열댓 개(비교 기업마다 아홉 개 더)를 불러야 했고, 그 응답 JSON 이 전부 agent 맥락에 쌓였습니다. 수집은 같은 날 같은 종목이면 같은 명령이라, CLI 가 대신 펼쳐 폴더 하나에 받고 agent 는 파일만 읽게 했습니다.

```bash
uv run cluefin-openapi-cli review collect --stock-code 214320 --peers 030000 --json   # /private/tmp/cluefin-review/214320-<날짜>/
uv run cluefin-openapi-cli review checklist --from /private/tmp/cluefin-review/214320-20261108 --json
uv run cluefin-openapi-cli review record --from /private/tmp/cluefin-review/214320-20261108 --source company-review --json
uv run cluefin-openapi-cli review due --days 14 --events true --json
uv run cluefin-openapi-cli audit check --run <agent id> --json
```

1. **`review collect`** 가 명령마다 stdout 을 `raw/<node>.json` 에, argv·exit code 를 `manifest.jsonl` 에 남깁니다. 화면에는 폴더 경로와 실패·건너뜀 요약만 나옵니다(2026-11-08 실측: 본 종목 + 비교 1곳 34호출 17.6초). 비교 기업을 원문을 읽은 뒤 정했으면 `--into <폴더> --peers` 로 그 호출만 더합니다.
2. agent(`.claude/agents/company-review.md`)가 폴더를 읽고 그 안에 `report.md` 와 `verdict.json` 을 씁니다.
3. **`review checklist`** 는 내가 정한 기준(`research/principles.toml`, 없으면 `--init` 으로 예시 생성)을 폴더의 raw 파일과 대조합니다. 점수나 매수 신호가 아니라 규칙마다 `pass`/`fail`/`unknown` 입니다.
4. **`review record`** 는 판단(`verdict.json`)을 저장소 루트 `research/verdicts.jsonl` 에 한 줄씩 쌓습니다. 수집 폴더는 `/tmp` 라 사라지므로 나중에 가격과 대조할 판단만 여기 남깁니다. `research/` 는 worktree 에서 돌려도 메인 체크아웃의 것이고(`$CLUEFIN_RESEARCH_DIR` 로 바꿈) git 에 올리지 않습니다. watch·hold 는 `trigger.entry_above`·`exit_below` 중 하나, buy·sell 은 `target`·`stop` 이 필요하고, 빠진 필드는 한 번에 모두 알려 줍니다(exit 2). 앞 줄은 고치지 않습니다 — 생각이 바뀌면 새 줄입니다.
5. **`review track`·`review due`** 는 그 판단을 로컬 캐시 일봉과 대조합니다(가격 도달은 일봉 종가 기준, 기록한 가격은 기준일 `adj_factor` 로 맞춤). `due` 는 다시 볼 판단만 고르고, `--events true` 일 때만 KIS 일정과 DART 공시를 부릅니다.
6. **`audit`** 은 agent 실행을 Claude Code 트랜스크립트에서 읽어 그 agent 파일의 감사 기준과 대조합니다(빠진 명령·같은 인자 반복·exit 3 뒤 계속·재시도 없는 실패). 판단이 맞았는지는 보지 않습니다 — 그건 `review track` 의 몫입니다.

## 재무 품질·가치 지표가 `null` 일 때

`dart financial-summary` 의 `quality` 블록(ROIC·DuPont·발생액 비율·F-Score·Altman Z'')과 `kis stock investor-metrics`(FCF 수익률·오너 어닝스·EV/EBIT·PEG·주주수익률·Altman Z)는 라벨·판정 없이 값과 구성요소만 냅니다. 공식과 출처 문헌은 `quality.py`·`investor_metrics.py` 의 모듈 docstring 과 응답의 `notes` 에 있습니다. 입력이 없으면 0 으로 메우지 않고 `null` 과 이유를 내는데, 자주 만나는 경우는 다음과 같습니다.

- **금융업(은행·보험·증권)은 일부 항목이 구조적으로 `null` 입니다.** K-IFRS 는 금융업에 유동/비유동 구분 재무상태표를 요구하지 않으므로 `current_assets`/`current_liabilities`(그리고 흔히 `revenue`)가 애초에 없습니다. 그래서 Altman X1, F-Score 의 유동비율·매출총이익률·자산회전율 항목이 `null` 이고 `altman_z_double_prime.missing` 에 이유가 적힙니다.
- **오너 어닝스는 대형주에서 자주 `null` 입니다.** 감가상각비·무형자산상각비를 현금흐름표 "조정" 한 줄에 묶어 내는 회사가 많습니다(표본 62개사 중 감가상각비를 따로 낸 곳은 8곳, 2026-11-10). 주석의 값은 `dart financial-as-filed` 의 `note_figures` 에 있습니다.
- **F-Score 는 두 해가 있어야** 계산되므로 3개년 중 가장 오래된 해는 `incomplete: true` 입니다.
- **주주수익률만 예외로 0 을 씁니다.** 현금흐름표가 읽혔으면 없는 항목(자사주 취득·처분, 주식 발행)은 그 활동이 없었던 것으로 보고 0 으로 계산하며 `assumed_zero` 에 이름을 남깁니다.
- **차입금을 못 읽으면 EV 를 내지 않습니다**(`ev_reason`). 차입 0 으로 계산하던 때는 "차입금 및 사채" 계정을 놓친 회사의 EV/EBIT 가 1.6배로 나왔고 실제는 6.6배였습니다(2026-11-08 수정). 유형자산 취득을 음수로 공시하는 회사가 있어 FCF 계산에는 절댓값을 씁니다.
- **기준 기간이 섞여 있습니다.** FCF 수익률·오너 어닝스·주주수익률은 최신 사업보고서 1개년, EV/EBIT·PER 은 직전 4개 분기 합(TTM)입니다. 분기 현금흐름은 누적뿐이라 연환산하지 않습니다.

## trend-setup 규칙과 근거

`kis chart trend-setup`(종목 하나, KIS 실시간)과 `cache trend-setup`(전 종목, 로컬 캐시)이 쓰는 관심종목 1·2·3그룹 규칙의 출처다.
채택한 값은 `trend_setup.py` 의 `RULES` 에만 있고, 여기는 그 값이 어디서 왔는지를 적는다. 정의는 cluefin-factory(아카이브)
`scripts/watchlist/*.mjs` 를 그대로 옮긴 것이고, 골든 테스트가 백테스트 값과 소수 6자리까지 같은지 확인한다. **공식을 바꾸면 근거가
사라진다** — 값을 바꾸려면 백테스트부터 다시 돌린다.

**`kis chart technical` 과 숫자가 다르다.** 이 명령의 `atr14_pct` 는 14일 true range 의 **단순 평균**이고 technical 의 ATR14 는
ta-lib(Wilder) 평활이다. 52주 고가·저가는 당일을 빼고 직전 250거래일의 장중 고가·저가다. 지수는 코스피 종목 `0001`, 코스닥 종목
`1001` 이다(KOSPI200 이 아니다).

### §1 데이터와 방법

- 원 백테스트(factory): 코스피·코스닥 보통주 2,487개, KIS 수정주가 2024-01~2026-10, 피봇 돌파 2025-02~2026-10 약 1.2만 건.
  t일 종가까지의 정보로 셋업을 정하고(피봇은 t−3일까지 확정된 프랙탈 고점), t+1일 고가가 피봇 이상이면 max(시가, 피봇)에 산다.
  시가가 피봇 +5% 를 넘으면 사지 않는다. 손절 −8%, 익절 +24%(3R), 왕복 비용 0.3%. 결과는 평균 R(손절폭 대비 손익)로 본다.
- 기준선(20일 평균 거래대금 ≥ 10억인 모든 피봇 돌파): 7,860건, 승률 30.6%, +0.14R — 기간이 강세장이라 기준선도 플러스다.
- 5년 재검증(2026-10, 2021-10~2026-10, **상장폐지 포함**, 같은 시뮬레이터): 3그룹 1,512건 평균 +0.13R, 4슬롯·25% 포트폴리오
  CAGR +7.5%·MDD 34%. 1·2그룹 매수는 모든 규칙에서 마이너스였다.

### §2 그룹

그룹은 겹칠 수 있고, action 은 한 번만 정한다: 비유동 → 제외, 1그룹 → 제외, 3그룹 → 피봇 거리로 알림/관찰, 2그룹 → 관찰, 나머지 → 제외.

| 그룹 | 그 자리 돌파의 성과(원 백테스트) |
|---|---|
| 1 강세선두(과열) | 1,269건, 승률 28.1%, +0.06R — 우위 없음, 사지 않는다 |
| 2 추세시작 | 1,243건, 승률 30.5%, +0.14R — 기준선과 같음 |
| 3 돌파대기 | 143건, 승률 49.7%, +0.79R(§3) |

- 공통: 20일 평균 거래대금 10억 미만은 대상 밖(손절이 계획대로 체결되지 않는다).
- 1그룹: 지수 대비 강도 상위(백분위 RS ≥ 90 ≈ 지수 대비 ≥ 1.32)이면서 52주 고점 −20% 이내, 10일 고저폭이나 50일선 이격으로 과열.
- 2그룹: 트렌드 템플릿(현재가 > 50일 > 150일 > 200일선, 200일선 상승, 52주 저점 +25% 이상, 고점 −25% 이내) + 52주 저점 대비
  +30~150%(Stage 2 초입) + 지수보다 강함.

### §3 3그룹(돌파대기)

수축 3회 이상, 마지막 수축 10% 이하, 10일 고저폭 12% 이하, 52주 고점 −20% 이내, 지수 대비 1 초과 1.32 미만, 거래대금 10억 이상.
알림은 종가가 피봇 아래 8% 안일 때만이다(백테스트 셋업 조건). 임계값을 바꿔도 결과가 평평했다(마지막 수축 8~15%·수축 2~4회
조합 +0.29~+0.70R, 10일 고저폭 8%~제한 없음 +0.53~+0.62R). 피봇은 좌우 3봉보다 높은(왼쪽은 엄격히, 오른쪽은 같아도 됨) 고가 중
가장 최근 것이고, 마지막 수축은 피봇 **다음 봉부터** 최저가까지의 하락률이다.

### §4 지수 대비 강도(RS 대신)

전 종목 백분위 대신 **종목 가중수익률 ÷ 자기 시장 지수 가중수익률**(가중수익률 = 2×63일 + 126일 + 189일 + 250일 수익 배수)을 쓴다.
백분위는 이 값의 순위일 뿐이라 `> 1` 은 "종목 RS > 지수 RS" 와 같은 비교다. 같은 3그룹 조건에서 백분위 RS 60~90 은 +0.60R,
지수 대비 1~1.32 는 +0.79R 이었다. 상한 1.32 는 백분위 RS 90 에 해당하는 지수 대비 값의 기간 중앙값이고, 백분위 RS ≥ 90 은 모든
조합에서 성과가 무너졌다. 지수가 강한 시기에는 통과 종목이 급감해 장세 필터처럼 작동한다. 지수 대비 21일 초과수익 ≤ 5.5%p 는
백분위 RS(1M) ≤ 80 과 91% 일치한다(§5).

### §5 2그룹 점수 — 3그룹 후보

2그룹 종목을 20거래일마다 관측해 90일 안에 3그룹 돌파를 수익으로 끝냈는지 봤다(평균 5.9%). 7개 조건(10일 고저폭 ≤ 12%,
ATR14 ≤ 4.5%, 60일 깊이 ≤ 30%, 50일선 이격 ≤ 10%, 지수 대비 21일 초과수익 ≤ 5.5%p, 52주 저점 대비 ≤ 100%, 52주 고점 −15% 이내)의
충족 개수별 성공률은 0점 0% → 6점 16.6% → 7점 20.1% 로 두 해 모두 단조였다. 6점 이상을 3그룹 후보(`g3_candidate`)로 낸다.
최근 한 달 덜 오른 2그룹이 더 잘 됐다.

### §6 주문 가격(`levels`)

알림 = 피봇 −3%(**매수가가 아니다** — 피봇 −3% 선매수의 27% 는 피봇에 닿지 못하고 −1R 로 끝났다), 매수 스톱 = 피봇, 추격 한도 =
피봇 +5%, 손절 = 피봇 −8%, 익절 = 피봇 +24%(3R). 모두 한국거래소 호가 단위로 내림하되 매수 스톱(체결된 고가)은 그대로다. 수량·금액
(포지션 사이징)은 내지 않는다. 매수 당일 확인할 것 — 같은 업종 +3% 이상 종목 비율, 돌파일 거래량 50일 평균의 1.5배 — 은 장중에만
알 수 있어 판정에 없다.

### §7 하지 않는 것과 한계

- 장세 필터(지수 60일선 등)는 3그룹 성과를 개선하지 못했다. 하락 방어는 −8% 손절이 맡는다.
- 원 규칙은 2025-02~2026-10 강세장 위주이고, 2026Q3 폭락기에는 3그룹도 전패했다. 5년 재검증의 +0.13R 이 더 보수적인 기대치다.
- **폭락 뒤 V자 반등장의 짧은 베이스 돌파는 3그룹으로 잡지 않는다** — 10일 고저폭 ≤ 12% 를 못 채우고 대부분 1그룹(과열)이 된다.
- 시가총액은 쓰지 않는다. 캐시의 `company.market` 은 현재 값이라 시장을 옮긴 종목은 과거 날짜에서 비교 지수가 틀릴 수 있다.

### §8 테마(`cache trend-setup` 의 `theme`)

키움 테마 스냅샷으로 관심 테마와 그 테마의 주도주를 **표시만** 한다(action 은 바꾸지 않는다 — 백테스트가 없다). 관심 테마는
구성종목 5개 이상 테마 중 캐시 수정주가 20일 수익률 **중앙값** 상위 20%, 주도주는 그 테마에서 20일 거래대금 상위 3 또는 키움
주요종목이면서 지수 대비 강도가 테마 중앙값 이상인 종목(크기만 크고 약한 종목은 뺀다). 키움 기간수익률은 원주가 기준이라
감자·병합 종목이 +905% 로 잡혀(2026-10 실측) 테마 평균을 망치므로 쓰지 않는다. `--theme-filter true` 는 관심 테마의 주도주만 남긴다.

### §9 상태 이력(`history`)

판정은 날마다 새로 매겨 상태를 저장하지 않는다. `history` 는 지난 봉으로 다시 계산한 사실이다: 현재 상태(`illiquid`·`g1`·`g3`·
`g2`·`none`, 이 우선순위)의 지속 일수(최대 20), 2일 이하 깜빡임을 건너뛴 이전 상태, 직전 60거래일 안의 1그룹 여부, 3그룹을 벗어난
날의 종류(전날 피봇 이상 `breakout`, 손절선 아래 `breakdown`, 그 사이 `faded`). 성과와의 관계는 아래 표본 외 검증 결과만 말한다.

**표본 외 검증(2026-10, 2017-01~2021-10, 상장폐지 포함, §1 과 같은 시뮬레이터, 3그룹 2,185건).** 가설·지표·문턱은 결과를 보기
전에 정했다(구간 탐색 2021-10~2026-10 에서 본 것을 처음 보는 구간에서 확인). 통과 = 방향 같음, 종목 단위 부트스트랩 95% 구간이 0 초과,
연도 과반 방향 같음, 두 칸 각 100건 이상, 포트폴리오(4슬롯·25%)에서 CAGR 이 낮아지지 않거나 MDD 가 5%p 이상 줄어든다.

| 가설 | 결과 | 숫자 |
|---|---|---|
| 3그룹 연속 2~3일 > 11일 이상 | **통과** | +0.26R(659건) vs −0.10R(128건), 95% 구간 [+0.01, +0.68], 5년 중 5년, MDD 45→31%(CAGR 5.2→2.4%) |
| 직전 60거래일 안에 1그룹 이력 있음 > 없음 | 실패 | +0.21R(647) vs +0.13R(1,538), 구간 [−0.09, +0.25], 5년 중 2년 |
| `exit` 라벨 점검: breakout 뒤 20일 > breakdown 뒤 | 통과 | 중앙값 −0.79% vs −1.10% |

통과한 것만 필터로 낸다: `cache trend-setup --history-filter fresh_g3` 는 3그룹이 된 지 2~3일인 종목만 남긴다. 거래 기회가 줄어
포트폴리오 CAGR 은 낮아졌으니 손실 폭을 줄이는 쪽의 필터다. 1그룹 이력(`g1_within_60d`)은 사실로만 표시하고 성과와 엮지 않는다.
판정(`action`)은 어느 경우에도 바꾸지 않았다.

## 고칠 때

command 는 `cluefin-openapi` 를 들여다보고 자동 생성하지 않고 handler 에 손으로 씁니다. 추가·변경 절차, broker 별 실측 함정, 무관해 보이는 변경에 깨지는 테스트는 [AGENTS.md](AGENTS.md) 에 있습니다.

이 README 와 AGENTS.md 의 코드 블록에 있는 `uv run cluefin-openapi-cli …` 줄은 단위 테스트(`tests/test_cli_contract_unit.py`)가 실행합니다 — 네트워크가 필요 없는 줄은 그대로, broker command 는 `--dry-run` 을 붙여서, `cache`·`review`·`audit` 줄은 하위 명령 이름만. 예시는 실제로 유효한 명령이어야 합니다.
