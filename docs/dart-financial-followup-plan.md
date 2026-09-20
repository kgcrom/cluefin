# DART 재무제표 명령 후속 과제

작성일: 2026-09-20 · 브랜치: `fix/dart-financial-search`

`dart financial-*` 3종은 실제로 동작한다. 티씨머티리얼즈(corp_code 00381756) 2026 반기를
불러 매출 2,252.7억·영업이익 101.9억·순이익 75.0억을 확인했고, `thstrm_add_amount`가
누적값이라는 `reprt_code` 설명도 실측과 일치한다. 남은 문제는 **에이전트가 이 명령을
찾지 못한다는 것**이다.

## Phase 1 — 검색어로 찾히게 만든다 (가장 급함)

에이전트의 명령 발견 경로는 `search <자연어> --json`이다. 그런데:

| 질의 | 현재 결과 |
| --- | --- |
| `재무제표` | dart 2종이 2·4위로 나온다 (정상) |
| `반기 실적` | KIS 3종만. dart는 없다 |
| `최신 실적 매출 영업이익 반기` | KIS 3종만 |
| `매출액 영업이익` | **0건** |

원인은 `metadata.py`의 한국어 별칭 표다. `("실적", ("earnings", "estimate", "income"))`이
KIS의 추정 실적 쪽으로 보내고, `매출`·`영업이익`·`순이익`·`반기`·`분기`는 별칭 자체가 없다.
명령 등록(`CommandTaxonomy(("statements",), ("financial-statement", ...))`)은 이미 맞게 돼
있으므로 고칠 곳은 별칭뿐이다.

- `실적`의 별칭에 `financial`/`statement` 계열을 더해 DART 쪽도 후보에 들어오게 한다.
- `매출`, `매출액`, `영업이익`, `순이익`, `반기`, `분기`를 별칭에 추가한다.
- `tests/test_search.py`의 `RECALL_CASES`에 위 표의 질의를 넣는다. 이 표가 "0건이던 질의"를
  모아두는 자리이므로 그대로 들어맞는다.

검증: `uv run pytest apps/cluefin-openapi-cli/tests/test_search.py`

## Phase 2 — 두 경로의 경계와 함정을 스키마에 적는다

실측으로 두 가지가 확정됐다. 둘 다 읽는 쪽이 조용히 틀리는 종류라 코드 옆에 적는다.

**① KIS 분기 커버리지는 종목마다 다르다.** `--div-cls-code 1`이 005930·383220에는
분기 30행을 주지만, 125020에는 연간만 주고 그마저 FY2024에서 멈춘다(FY2025 자체가 없다).
대형주로 확인하고 KIS를 기본 경로로 삼으면 소형주 분석이 1년 묵은 수치 위에서 돈다.
→ 최신 실적은 종목 불문 DART, 비율·성장률은 DART에 없으니 KIS.

**② KIS `op_prfi`는 영업이익이 아니라 경상이익(법인세차감전)이다.** 영업이익은
`bsop_prti`다. 125020 FY2024를 DART 원문과 대조해 확정했다 — `bsop_prti` 109억 =
DART 영업이익 109.27억, `op_prfi` 82억 = DART 법인세차감전 82.46억.
파이썬 모델은 이미 "경상 이익"으로 맞게 라벨링돼 있다
(`_domestic_stock_info_types.py`). 틀리는 것은 원시 JSON 필드명만 보는 소비자 쪽이므로,
`kis financial income-statement`의 스키마 설명에 두 필드의 구분을 적는다.

검증: `uv run pytest apps/cluefin-openapi-cli/tests/test_cli_contract.py`

## Phase 3 — 소비자(cluefin-factory) 반영

`.claude/agents/market-review.md`의 재무 레시피가 아직 `kis financial` 6종 번들이다.
최신 실적을 DART에서 읽도록 바꿔야 PER·EPS가 1년 묵은 연간 실적 기준에서 벗어난다.
Phase 2의 `op_prfi` 함정도 레시피에 반영해야 한다 — 이미 이 함정으로 영업이익을
경상이익으로 읽은 리포트가 나왔다.
**별도 저장소의 일이라 이 브랜치 범위 밖이고**, Phase 1이 머지된 뒤 착수한다.

## 확인용 명령

```
uv run cluefin-openapi-cli dart financial-major-accounts \
  --corp-code 00381756 --bsns-year 2026 --reprt-code 11012 --json
```
