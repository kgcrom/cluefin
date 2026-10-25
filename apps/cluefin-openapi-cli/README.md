# cluefin-openapi-cli

`cluefin-openapi-cli`는 `cluefin-openapi`의 broker API를 **AI agent가 직접 호출하는 용도**로 노출하는 명령줄 인터페이스입니다. 사람이 읽는 화면이 아니라, agent가 JSON을 읽고 다음 명령을 조립하는 것을 전제로 설계했습니다.

- 모든 출력은 JSON입니다. `--json`을 주거나 stdout이 TTY가 아니면 자동으로 JSON입니다.
- 어떤 API를 호출할 수 있는지(`brokers`, `list`), 어떤 parameter를 받는지(`schema`)를 CLI 자체가 JSON으로 알려줍니다. 외부 문서를 미리 읽을 필요가 없습니다.
- 실행 전 `--dry-run`으로 parameter를 로컬 검증하고, 실패는 exit code와 구조화된 `error` JSON으로 돌려줍니다.

## Broker 역할

| broker | role | 용도 |
|---|---|---|
| `kis` | **primary** | 기본 소스. 시세·차트·순위·재무·업종·ETF·일정·휴장일. 모든 작업은 여기서 시작한다. 계산 명령: `chart technical`(지표·신호), `chart trend-setup`(추세 셋업 1·2·3그룹 판정), `stock opinion-summary`(증권사별 목표가 집계), `stock valuation`(종가 × DART 주식수 × DART 재무로 시총·TTM PER·PBR). |
| `kiwoom` | **auxiliary** | KIS가 못 보는 빈칸만 채운다. 테마, 업종 구성종목, 틱 차트, 프로그램매매 상세, 거래원(회원사) 수급. |
| `dart` | reference | 공시 원문·기업 고유번호·최대주주·발행주식수·정기보고서 재무제표(반기·분기 포함, `financial-as-filed` 는 접수 당시 값, `financial-summary` 는 분기 역산·3개년·비율·TTM 계산)·원문 서술(사업의 내용 `document-outline`/`document-section`, 재무제표 주석 `financial-notes`)·주요사항보고서 본문(`major-event`: CB·BW·EB·유무상증자·감자·자사주·합병·분할 등 36종)·정기보고서 주요정보(`report-item`: 배당·자기주식·임원·보수·사채 잔액·감사의견 등 26종). 시세 소스가 아니다. |
| `sec` | reference | 미국 SEC EDGAR. 미국 상장 고객사·경쟁사의 10-K/10-Q/8-K Item 본문(`filing-items`)과 8-K 실적 보도자료 EX-99.1(`filing-exhibit`). 20-F/6-K(한국 ADR 대부분)는 읽지 않는다. 한국 기업 공시는 `dart`. |

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
```

어느 broker가 설정돼 있는지는 값을 노출하지 않고 `brokers --json`의 `credentials.configured`로 확인합니다.

## Agent 워크플로

```bash
uv run cluefin-openapi-cli search 외국인 순매수 --json                    # 0. 자연어 → 순위가 매겨진 후보 (권장 시작점)
uv run cluefin-openapi-cli brokers --json                              # 1. 역할·설정 상태·Kiwoom 전용 목록
uv run cluefin-openapi-cli list --broker kis --domain chart --json     # 2. 후보 command (brief)
uv run cluefin-openapi-cli schema kis stock current-price --json       # 3. parameter JSON Schema + 호출 예시
uv run cluefin-openapi-cli kis stock current-price --stock-code 005930 --dry-run --json   # 4. 로컬 검증
uv run cluefin-openapi-cli kis stock current-price --stock-code 005930 --fields current_price,per --json  # 5. 실행
```

### 1. Discovery

```bash
uv run cluefin-openapi-cli search 외국인 순매수 상위 종목 --json
uv run cluefin-openapi-cli search dividend schedule --limit 5 --compact
uv run cluefin-openapi-cli search 재무제표 --broker kis --json
uv run cluefin-openapi-cli brokers --json
uv run cluefin-openapi-cli list --broker kis --category stock --json
uv run cluefin-openapi-cli list --domain chart --json
uv run cluefin-openapi-cli list --tag ohlcv --json
uv run cluefin-openapi-cli list --tag screening --json
uv run cluefin-openapi-cli list --query theme --json
uv run cluefin-openapi-cli list --full --domain chart --json
uv run cluefin-openapi-cli domains --json
uv run cluefin-openapi-cli tags --json
uv run cluefin-openapi-cli kis --help --json
uv run cluefin-openapi-cli kis chart --help --json
```

`search`는 자연어 작업 설명을 받아 BM25F로 **순위를 매긴 후보 command**를 돌려줍니다. 기본 8건, 약 3KB로 항상 첫 호출로 쓸 만큼 쌉니다. 한국어 질의는 `metadata.QUERY_ALIASES`가 영어 색인 용어로 확장합니다(코퍼스는 전부 영어입니다). 각 row에는 그대로 실행 가능한 `next`(해당 command의 `schema` 호출)가 붙습니다. 결과가 없거나 `confidence`가 `low`면 빈 배열 대신 `fallback`(`did_you_mean`, `nearest_domains`, `nearest_tags`, `recipes`, `next`)이 들어옵니다 — `search`는 막다른 빈 결과를 주지 않습니다.

`list --query`는 `qualified_name`·`description`에 대한 **리터럴 부분 문자열 필터**입니다. 자연어·한국어 질의에는 `search`를, 정확한 문자열 필터링에는 `list --query`를 씁니다.

`list`는 기본이 **brief**입니다. 한 row에 `qualified_name`, `broker_role`, `description`, `domains`, `tags`, `required`(필수 parameter 이름), `kis_alternatives`만 담아 command 목록 전체가 100KB 이하로 떨어집니다. parameter 전체가 필요하면 `--full`을 주거나, 특정 command만 `schema`로 봅니다. 정렬은 항상 kis → kiwoom → dart → sec 입니다.

`--full`을 필터 없이 부르면 상위 25개만 반환하고 `count`(전체)·`returned`·`truncated: true`·`hint`를 함께 냅니다. 전체가 필요하면 `--limit 0`을 명시합니다.

`domains`·`tags`는 category에서 자동 파생되지 않고 **command마다 직접 부여**됩니다(`metadata.COMMAND_TAXONOMY`). 따라서 `--tag`·`--domain` 필터는 실제로 좁혀지며, 잘 알려진 개념은 `--query`보다 이쪽이 정확합니다.

`<broker> --help`는 category마다 `description`·`when_to_use`·실제 command에서 계산한 `domains`/`tags`·바로 실행 가능한 `list_command`를 냅니다. `<broker> <category> --help`는 그 category의 command를 설명과 함께 냅니다. 모든 meta command도 `--help`를 받습니다.

`category`는 provider SDK 구조이고, `domain`은 Agent 업무 의도입니다. 예를 들어 `kis chart period`는 category가 `chart`이고 domain도 `chart`지만, 투자자 수급성 API는 provider별 category가 달라도 `trading-flow` domain으로 함께 찾을 수 있습니다.

Agent용 분류 기준:

- `domains`: 업무 영역입니다. 예: `chart`, `statements`, `trading-flow`.
- `tags`: 세부 기능 또는 데이터 특성입니다. 예: `ohlcv`, `dividend`, `program-trading`.
- `recipes`: 여러 command를 조합하는 workflow guide입니다. Recipe는 command 실행기가 아니라 탐색 순서와 조합 의도를 설명합니다.

`domains --json`, `tags --json`는 `name`, `command_count`뿐 아니라 `description`, `when_to_use`, `avoid_when`, `related_domains`, `related_tags`, `example_filter`를 포함합니다. Agent는 `example_filter`를 그대로 다음 탐색 명령으로 사용할 수 있습니다.

예시 taxonomy 응답:

```json
{
  "name": "chart",
  "description": "Price, volume, and OHLCV time-series lookup commands.",
  "when_to_use": "Use before technical analysis, price trend review, or volume analysis.",
  "avoid_when": "Skip when the question is what the indicators say rather than what the prices were — `kis chart technical` computes them and returns readings instead of rows.",
  "related_tags": ["ohlcv", "daily", "minute", "tick"],
  "example_filter": "uv run cluefin-openapi-cli list --domain chart --json",
  "command_count": 17
}
```

### 2. Schema

`schema`는 한 command의 **호출 계약 전체**를 JSON으로 냅니다. `describe`는 같은 정보를 discovery metadata 중심으로, `schema`는 실행 중심으로 정리한 것입니다.

```bash
uv run cluefin-openapi-cli schema kis stock current-price --json
uv run cluefin-openapi-cli describe kis stock current-price --json
uv run cluefin-openapi-cli kis stock current-price --help --json
```

`schema` 응답 필드:

- `parameters`: JSON Schema (`additionalProperties: false`). `enum`, `pattern`, `required`가 실행 시 그대로 검증됩니다.
- `options`: parameter마다 `--flag` 이름, 타입, 필수 여부, enum/pattern. 배열·객체 타입은 `pass_via: "--params-json"`.
- `invoke`: 바로 실행 가능한 세 가지 문자열 `flags`, `params_json`, `dry_run`.
- `kis_alternatives`, `broker_role`, `required_credentials`, `agent_notes`.

Agent는 `describe --json`의 `examples[0].command` 또는 `schema --json`의 `invoke.dry_run`을 실행 skeleton으로 사용하고, `agent_notes`를 provider별 주의사항으로 참고할 수 있습니다.

### 3. Workflow Recipes

```bash
uv run cluefin-openapi-cli recipes --json
uv run cluefin-openapi-cli recipe stock-research --json
uv run cluefin-openapi-cli recipe technical-analysis --json
uv run cluefin-openapi-cli recipe market-scan --json
uv run cluefin-openapi-cli recipe corporate-actions --json
uv run cluefin-openapi-cli recipe disclosure-monitoring --json
uv run cluefin-openapi-cli recipe us-peer-filings --json
```

### 4. Command Path

- `kis <category> <name>`
- `kiwoom <category> <name>`
- `dart <name>`, `sec <name>` (category 단계 없음)
- `search`, `brokers`, `list`, `describe`, `schema`, `domains`, `tags`, `recipes`, `recipe`는 meta command

```bash
uv run cluefin-openapi-cli kis stock current-price --stock-code 005930 --json
uv run cluefin-openapi-cli kiwoom chart tick --stock-code KRX:005930 --tic-scope 1 --json
uv run cluefin-openapi-cli dart company-overview --corp-code 00126380 --json
uv run cluefin-openapi-cli dart major-event --corp-code 00126380 --event convertible-bond --bgn-de 20230101 --end-de 20261016 --json
uv run cluefin-openapi-cli dart report-item --corp-code 00126380 --item dividend --bsns-year 2025 --reprt-code 11011 --json
uv run cluefin-openapi-cli sec filing-items --cik 320193 --accession-number 0000320193-23-000106 --items 1A --json
uv run cluefin-openapi-cli kis chart trend-setup --stock-code 005930 --json
```

### 5. 로컬 일봉 캐시 (`cache`)

전종목 횡단면 질의·백테스트용으로 상장 주식 전종목(2016년 이후 폐지 종목 포함)과 KOSPI·KOSDAQ·KOSPI200 일봉, 국고채·CD
일별 금리를 DuckDB 파일 하나(`~/.cache/cluefin/market.duckdb`, `CLUEFIN_CACHE_DIR` 로 변경)에 쌓습니다. `cache load` 만 broker 를
부르고(KIS·키움·DART·ECOS, 한 번에 하나씩), 나머지는 파일만 읽습니다. 금리(`rates`)는 `.env` 의 `ECOS_AUTH_KEY` 가 있어야 받습니다.

```bash
uv run cluefin-openapi-cli cache load --json                     # 장 마감 후. 첫 실행 ~2시간 20분, 이후 ~7분
uv run cluefin-openapi-cli cache status --json
uv run cluefin-openapi-cli cache ohlcv --code 005930 --since 20260901 --adjusted true --json
uv run cluefin-openapi-cli cache company --as-of 20180102 --limit 5 --json
uv run cluefin-openapi-cli cache perf --code 005930 --bench U0001 --since 20210101 --risk-free ktb3y --json
uv run cluefin-openapi-cli cache trend-setup --status alert,watch --json            # 마지막 거래일 전 종목 1·2·3그룹
uv run cluefin-openapi-cli cache trend-setup --as-of 20261016 --theme-filter true --history true --json
```

`cache trend-setup` 은 `kis chart trend-setup` 과 같은 판정을 그날 상장한 보통주 전부(우선주·스팩 제외, 나중에 폐지된 종목 포함)에
돌립니다(약 1초). 기본은 alert·watch 행만 내고 전체는 `summary` 건수로 셉니다. 행의 `failed` 는 2·3그룹에서 통과 못 한 check id 라
"왜 3그룹이 아닌가"를 행만 보고 알 수 있고, 규칙별 값 전체는 `kis chart trend-setup --end-date` 로 봅니다. 테마(`theme`)는
`cache load --only theme` 스냅샷이 있는 날만 붙고, `--history true` 는 보이는 행마다 상태 이력을 계산합니다(행이 많으면 느립니다).
`--history-filter fresh_g3` 은 3그룹이 된 지 2~3일인 종목만 남깁니다(표본 외 검증을 통과한 유일한 이력 필터, 아래 §9).

`cache perf` 는 종목을 수정주가로 사서 들고 있었을 때의 성과(`cluefin-ta` `PERFORMANCE`: CAGR·MDD·변동성·샤프·소르티노·칼마·
베타·알파)와 같은 기간 벤치마크(기본 `U0001`) 자체의 성과를 함께 줍니다. 두 코드 모두 일봉이 있는 날만 쓰고, CAGR 은 달력 연수로
셉니다. `--risk-free` 는 연율 소수(3.5% 는 `0.035`)나 `rates` 계열 이름(`ktb3y` 등)입니다. 계열이면 각 기간 첫날의 금리(그날 발표가
없으면 직전 발표값)를 쓰고, 캐시에 없으면 exit 2 `RatesMissing` 입니다.

| 테이블 | 내용 |
|---|---|
| `company` | 종목 하나에 한 행: 이름·시장·업종·표준산업분류·DART 고유번호·결산월·상장일·폐지일·관리/정지 |
| `ohlcv` | 종목·지수(`U0001`·`U1001`·`U2001`) 일봉. 원주가 + `adj_factor`(수정주가 = 가격 × 계수), 락구분·분할비율·재평가사유 |
| `theme`·`theme_member` | 키움 테마 스냅샷(날마다, `as_of` 별): 테마 이름·구성종목 수·주요종목, 구성종목. 키움 기간수익률은 원주가라 참고로만 |
| `rates` | ECOS 일별 시장금리 `ktb1y`·`ktb3y`·`ktb10y`·`cd91d`. 값은 발표 원문 그대로 연 %(3.5 = 3.5%) |
| `load_log`·`adj_log`·`bar_log`·`probe_log` | 적재 기록, 수정계수 확인 시점, 일봉 시작일, 폐지 후보 확인 기록 |

DuckDB 는 쓰는 동안 다른 프로세스가 파일을 열 수 없습니다. `cache load` 중의 읽기는 exit 1 `CacheLocked`, 첫 적재 전은
exit 2 `CacheMissing` 입니다.

DuckDB CLI(`brew install duckdb`, 캐시와 같은 1.5 계열)로 직접 SQL 을 쓸 수 있습니다. 켜 둔 동안은 `cache load` 가 못 쓰니
적재 전에 닫습니다.

```bash
duckdb -readonly ~/.cache/cluefin/market.duckdb          # SQL 셸, .quit 로 종료
# 브라우저 UI(http://localhost:4213): 메모리 DB 로 띄우고 캐시만 읽기 전용으로 붙인다
duckdb -cmd "ATTACH '$HOME/.cache/cluefin/market.duckdb' AS market (READ_ONLY); USE market; CALL start_ui();"
```

`duckdb -readonly -ui <파일>` 은 UI 가 자기 상태 카탈로그(`_duckdb_ui`)를 만들지 못해 `Catalog "_duckdb_ui" does not exist`
로 실패합니다. 수정주가는 `close * adj_factor` 입니다.

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

## 입력 방식

scalar 필드는 `--flag value` 또는 `--flag=value`로 줍니다. 배열·객체는 `--params-json`에 전체 객체를 넣거나, 해당 flag에 JSON 문자열을 넣습니다.

```bash
uv run cluefin-openapi-cli kis stock current-price --stock-code 005930 --json
uv run cluefin-openapi-cli kis analysis watchlist-multi-quote \
  --params-json '{"stocks":[{"market":"J","stock_code":"005930"},{"market":"J","stock_code":"000660"}]}' \
  --json
```

입력 규칙:

- 같은 필드를 둘 다 주면 개별 flag가 `--params-json`보다 우선
- 모든 parameter는 네트워크 호출 전에 로컬 검증: `required`, 알려지지 않은 필드, 타입, `enum`, `pattern`, 숫자·길이 범위
- 문자열에 제어문자, `..` 경로 이동, `%`(사전 URL 인코딩), `?`, `#`가 들어 있으면 거부. 중첩 JSON 내부도 검사
- 검증 실패는 exit 2, `error.data.issues[]`에 필드별 `problem`, `value`, `allowed`, `hint`

### `--dry-run`

parameter 병합·검증만 수행하고 broker를 호출하지 않습니다. 토큰 발급도 일어나지 않습니다.

```bash
uv run cluefin-openapi-cli kis stock current-price --stock-code 005930 --dry-run --json
```

응답에는 최종 `params`, `credentials.configured`(값 노출 없이 설정 여부), `kis_alternatives`, 그대로 실행할 `execute` 문자열이 들어 있습니다.

## 출력 방식

- `--json`: 항상 JSON. stdout이 TTY가 아니면 기본값
- `--compact`: 한 줄 JSON. agent 컨텍스트에 가장 저렴
- `--fields a,b.c`: 결과 field mask. 최상위 키 또는 점 경로. 리스트 값이면 각 요소에 적용. 없는 키는 조용히 생략되므로 반환 키를 확인할 것
- `--limit N`: 결과 배열을 N행으로 자름. `--fields`(열 마스킹) 다음에 적용됩니다. 실제로 잘린 경우에만 `_truncated`에 `limit`과 `path`·`returned`·`total`이 붙습니다. 최상위가 리스트면 `{"items": [...], "_truncated": {...}}`로 감쌉니다 — 잘렸을 때만 shape이 바뀝니다. `0`이면 제한 없음. broker command에는 암묵 기본값이 없습니다(20행짜리 일봉은 유효한 20일 차트처럼 보이므로 조용히 자르지 않습니다)
- client 라이브러리의 DEBUG/INFO 로그는 stderr에서 숨김. `CLUEFIN_OPENAPI_DEBUG=1`이면 표시

```bash
uv run cluefin-openapi-cli kis stock current-price --stock-code 005930 --fields stock_code,current_price,per --compact
uv run cluefin-openapi-cli kis chart daily --stock-code 005930 --fields output.stck_bsop_date,output.stck_clpr --limit 20 --compact
uv run cluefin-openapi-cli kiwoom theme group --query-type 0 --date-type 10 --theme-name "" \
  --fluctuation-type 1 --exchange-type 1 --fields thema_grp.thema_grp_cd,thema_grp.thema_nm --json
```

## 오류와 exit code

실패하면 stdout에 아래 envelope 하나만 나옵니다(JSON 모드). agent는 `exit_code`와 `retryable`로 분기합니다.

```json
{
  "error": {
    "type": "ValidationError",
    "message": "Parameter validation failed.",
    "exit_code": 2,
    "retryable": false,
    "hint": "Run `schema kis stock current-price --json` and fix the listed fields.",
    "data": {"command": "kis.stock.current-price", "missing": [], "issues": [{"field": "market", "problem": "not one of the allowed values", "value": "X", "allowed": ["J", "NX", "UN"]}]}
  }
}
```

| exit | 의미 | agent 행동 |
|---|---|---|
| 0 | 성공 | |
| 1 | CLI/client 내부의 예상치 못한 실패 | 그대로 재시도하지 말 것 |
| 2 | usage·검증 오류 | 인자를 고친다. `schema`를 다시 본다 |
| 3 | 자격증명 누락·거부 (SEC는 `SEC_USER_AGENT` 누락·403) | `.env`/환경변수 확인. 재시도 무의미. SEC 403은 과속 차단(약 10분)일 수도 있다 |
| 4 | broker API·네트워크·타임아웃·응답 파싱 실패 | `retryable`이 true일 때만 한 번 재시도 |
| 5 | broker rate limit | `data.retry_after`초(없으면 1초 이상) 대기 후 재시도. 단 DART `data.status == "020"` 은 일일 한도라 반복 재시도 금지 |

`error.type` 예: `ValidationError`, `CredentialsMissing`, `AuthenticationError`, `RateLimitError`, `BrokerUnavailable`, `BrokerApiError`, `BrokerRejectedRequest`, `ResponseParseError`(존재하지 않는 종목코드처럼 broker가 빈 응답을 준 경우, 다른 회사의 공시), `NotFound`(SEC 404: CIK·접수번호 확인), `ExecutionError`.

## 뼈대: 모듈과 요청 흐름

```
src/cluefin_openapi_cli/
├── main.py         진입점. argv 파싱 → meta command 또는 broker command 분기, 출력·오류 envelope
├── registry.py     CommandSpec(경로·schema·role·kis_alternatives·executor) 조립과 조회
├── metadata.py     BROKER_ROLES, KIWOOM_KIS_ALTERNATIVES, domain/tag taxonomy, 예시·agent_notes 생성
├── validation.py   네트워크 호출 전 로컬 검증(required/enum/pattern/범위)과 문자열 하드닝
├── errors.py       exit code 계약(EXIT_CODES)과 broker 예외 → CliError 분류(classify_exception)
├── output.py       JSON 직렬화, --compact, --fields 마스킹
├── search.py       자연어 query → BM25F 순위 command 후보. 한국어 alias 확장·fallback
├── recipes.py      여러 command를 엮는 workflow guide
├── indicators.py   `kis chart technical` 의 지표·신호 조립(cluefin-ta)
├── trend_setup.py  `trend-setup` 두 명령의 판정(백테스트 정의 이식, cluefin-ta 를 쓰지 않음)
├── cache/          로컬 DuckDB 캐시: store(스키마·잠금) · company · bars · adjust · rates · theme · read · perf · trend · cli(`cache <sub>`)
└── handlers/
    ├── _base.py    @rpc_method 데코레이터, KIS/Kiwoom 응답 추출 헬퍼
    ├── kis/        category별 handler 모듈 (stock, chart, ranking, financial, …)
    ├── kiwoom/     category별 handler 모듈 (theme, sector, etf, program, …)
    ├── dart.py
    └── sec.py
```

한 번의 broker command 실행은 다음 순서로 흐릅니다.

```
argv ─▶ _parse_named_options ─▶ registry.resolve_command(path)
     ─▶ _merge_params (--params-json ⊕ flags → 타입 변환)
     ─▶ validation.validate_params (실패: exit 2, issues[])
     ─▶ --dry-run 이면 여기서 종료 (토큰 발급 없음)
     ─▶ registry.invoke_command → BrokerClientFactory → handler(params, session)
     ─▶ 예외: errors.classify_exception → exit 3/4/5 + error envelope
     ─▶ output.select_fields(--fields) → render_output(--compact)
```

command 하나는 handler 함수에 붙은 `@rpc_method(name="stock.current_price", parameters={JSON Schema}, broker="kis")` 하나로 정의됩니다. `name`의 점이 CLI 경로(`kis stock current-price`)가 되고, `parameters`가 그대로 `schema` 출력과 flag 목록과 로컬 검증 규칙이 됩니다. 새 command를 추가하려면 handler 모듈에 함수를 쓰고 그 모듈의 `_ALL_HANDLERS`에 넣으면 끝입니다. Kiwoom command가 KIS와 겹치면 `metadata.KIWOOM_KIS_ALTERNATIVES`에 한 줄을 추가합니다.

검증 테스트(`tests/`):

- `test_agent_surface_unit.py`: role·alternatives·schema·dry-run·검증·field mask·exit code 분류
- `test_cli_contract_unit.py`: 모든 command가 `schema`가 유효하고 `invoke.dry_run` 예시가 실제로 exit 0으로 통과하는지, README 코드 블록의 명령이 실행되는지
- `test_handler_client_contract_unit.py`: handler가 호출하는 client 메서드·응답 필드가 실제 `cluefin-openapi`에 존재하는지
- `test_rpc_registry_unit.py`: command 수·metadata 완결성·taxonomy 커버리지·`COMMAND_TAXONOMY` 전수 대응·필터 선택도
- `test_search_unit.py`: 한국어/영어 질의 recall, 순위, fallback, alias 동기화, 인덱스 캐싱

## 동작 원칙

- CLI 내부 registry가 command metadata와 executor set을 직접 관리
- 실제 broker client 생성은 `cluefin_openapi.client_factory`를 사용
- KIS, Kiwoom은 토큰 캐시를 사용하고, DART·SEC는 stateless client로 동작
- 모든 command는 `side_effect: "read"`. 주문·계좌 변경 command는 없다
- Agent integration은 이 CLI의 JSON discovery를 직접 사용합니다. agent용 사용 규칙은 `AGENTS.md` 첫 절에 있습니다

## 주의사항

- 실 API 호출에는 broker credential이 필요합니다. `brokers --json`으로 먼저 확인합니다
- `.env`가 없거나 값이 비어 있으면 해당 broker command는 exit 3으로 실패합니다
- 일부 command는 복합 입력 때문에 사실상 `--params-json`이 필요합니다. `schema`의 `options[].pass_via`를 봅니다
