# cluefin-feeds

브로커·공시 OpenAPI 밖의 공개 데이터 피드와 파일을 받아 읽는 패키지입니다. 공급처마다 하위 모듈이 하나씩 있고,
키가 필요 없거나(재무부) 선택입니다.

| 모듈 | 공급처 | 받는 것 |
|---|---|---|
| `cluefin_feeds.treasury` | 미 재무부 금리 XML 피드 | 명목 국채 수익률 곡선(1개월~30년, 일별) |
| `cluefin_feeds.bls` | 미 노동통계국 Public Data API | 시계열 ID로 CPI·고용 등 (월별·연평균) |
| `cluefin_feeds.damodaran` | Damodaran Online (NYU, 공개 파일) | 국가 위험 프리미엄·ERP, 지역별 업종 β, 종목 → 업종 분류 |

## 미 재무부 수익률 곡선

```python
from cluefin_feeds.treasury import Client

rows = Client().par_yield_curve("202610")  # 한 달(YYYYMM) 또는 한 해(YYYY)
latest = rows[-1]
print(latest.date, latest.year_10)  # 2026-10-16 4.05 (연 %, Decimal)
```

- 자료가 아직 없는 달(달 초)은 빈 목록입니다. 최근 값이 필요하면 지난달을 다시 묻습니다.
- 1.5·2·4개월물은 생긴 뒤부터만 값이 있고, 그 전은 `None`입니다.

## BLS 시계열

```python
import os
from cluefin_feeds.bls import CPI_U_ALL_ITEMS, Client

client = Client(registration_key=os.getenv("BLS_REGISTRATION_KEY"))  # 없으면 v1
cpi = client.timeseries([CPI_U_ALL_ITEMS], 2015, 2026, annual_average=True).get(CPI_U_ALL_ITEMS)
annual_2015 = next(r for r in cpi.data if r.year == 2015 and r.period == "M13").value  # Decimal("237.017")
```

- 키 없이 v1(한 번에 25시리즈·10년, 하루 25회), [등록 키](https://data.bls.gov/registrationEngine/)가 있으면
  v2(50시리즈·20년, 하루 500회, 1년마다 갱신). 한도를 넘는 시리즈·연도는 나눠 보내고 결과를 합칩니다.
  서버는 넘치는 연도를 **앞쪽 10년만** 남기므로 직접 부를 때도 나눠야 최근 값이 빠지지 않습니다.
- 결측은 `raw_value == "-"`, `value is None`(예: 2025-10 셧다운, 각주 코드 X). 없는 시리즈도 성공으로 오고
  `messages`에 "Invalid Series for Series …"가 실립니다.

## Damodaran

```python
from cluefin_feeds.damodaran import Client

client = Client()
korea = client.country_risk_premiums().get("Korea")  # HTML, 의존성 없음
print(korea.equity_risk_premium, korea.country_risk_premium)  # 4.87 0.64 (% 단위 Decimal)

# 아래 둘은 xls — pip install 'cluefin-feeds[damodaran]'
betas = client.industry_betas("emerging")  # 한국은 Emerging Markets
companies = client.companies("South Korea")  # indname.xls 약 22MB
samsung = next(c for c in companies if c.krx_code == "005930")
beta_u = betas.get(samsung.industry_group).unlevered_beta_corrected_for_cash  # 영업자산 β
```

- 표는 1년에 한두 번 바뀝니다(업종 β 1월, ERP 1월·7월). 매번 받지 말고 저장해 쓰세요.
- 다시 레버할 때는 β = β_U × (1 + (1 − t) × D/E), t 는 한계세율(`corporate_tax_rate` 또는 표의 `marginal_tax_rate`).

## 오류

모든 예외는 `cluefin_feeds.FeedError`를 상속합니다. 429·5xx·타임아웃·연결 오류는 재시도한 뒤
`FeedRateLimitError`·`FeedServerError`·`FeedTimeoutError`·`FeedNetworkError`로, 형식이 맞지 않는 응답은
`FeedParseError`로 올라옵니다.
