# cluefin-feeds

브로커·공시 OpenAPI 밖의 공개 데이터 피드와 파일을 받아 읽는 패키지입니다. 공급처마다 하위 모듈이 하나씩 있고(`treasury`,
`bls`, `damodaran`), 키는 필요 없거나(재무부·Damodaran) 선택(BLS)입니다. 받아서 읽기만 하므로 저장은 쓰는 쪽에서 합니다.

uv 워크스페이스 멤버라 저장소 루트에서 `uv sync --all-packages` 로 설치합니다. Damodaran 의 xls 표 두 개는 `damodaran`
extra(`xlrd`)가 더 필요합니다(`--all-extras`).

## 미 재무부 수익률 곡선

```python
from cluefin_feeds.treasury import Client

rows = Client().par_yield_curve("202610")  # 한 달(YYYYMM) 또는 한 해(YYYY)
latest = rows[-1]
print(latest.date, latest.year_10)  # 2026-10-16 5.09 (연 %, Decimal)
```

- 자료가 아직 없는 달(달 초)은 오류가 아니라 빈 목록입니다. 최근 값이 필요하면 지난달을 다시 묻습니다.
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
korea = client.country_risk_premiums().get("Korea")  # HTML, 추가 의존성 없음
print(korea.equity_risk_premium, korea.country_risk_premium)  # 4.87 0.64 (% 단위 Decimal)

# 아래 둘은 xls 라 damodaran extra 가 필요합니다
betas = client.industry_betas("emerging")  # 한국은 Emerging Markets
companies = client.companies("South Korea")  # indname.xls 약 22MB
samsung = next(c for c in companies if c.krx_code == "005930")
beta_u = betas.get(samsung.industry_group).unlevered_beta_corrected_for_cash  # 영업자산 β

debt_to_equity = 0.30  # 대상 기업의 D/E — 비율
tax = float(korea.corporate_tax_rate) / 100  # 26.40(%) → 0.264
beta = beta_u * (1 + (1 - tax) * debt_to_equity)  # 다시 레버한 β
```

- **세율 필드 둘은 단위가 다릅니다.** 국가 표의 `corporate_tax_rate` 는 퍼센트 `Decimal`(26.40), 업종 β 표의
  `marginal_tax_rate` 는 비율 `float`(0.2471)입니다. 위 식의 `tax` 는 비율이라 앞의 것은 100 으로 나누고 뒤의 것은 그대로
  씁니다. 업종 β 표의 `de_ratio` 도 비율입니다.
- **국가 이름이 표마다 다릅니다.** 국가 표는 `"Korea"`(북한은 `"Korea, D.P.R."`), 종목 표는 `"South Korea"` 이고, 이름이
  정확히 같아야 찾습니다.
- **업종 β 표의 마지막 두 행은 업종이 아니라 합계입니다**(`Total Market`, `Total Market (without financials)`).
- `krx_code` 는 `KOSE:A005930` 의 "A" 를 뗀 6자리입니다. `XKON` 은 코넥스이고, 해외 거래소에 상장한 한국 기업은 `None` 입니다.
- 표는 1년에 한두 번 바뀝니다(업종 β 1월, ERP 1월·7월). 매번 받지 말고 저장해 쓰세요.

## 오류

네트워크·응답 오류는 모두 `cluefin_feeds.FeedError` 를 상속합니다. BLS 는 실패도 HTTP 200 에 본문 `status` 로 알리므로
클라이언트가 본문을 보고 `BlsAPIError` 를 올립니다. 잘못된 인자는 `ValueError`, `xlrd` 가 없으면 `ImportError` 입니다.
