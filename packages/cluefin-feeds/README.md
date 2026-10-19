# cluefin-feeds

브로커·공시 OpenAPI 밖의 공개 데이터 피드와 파일을 받아 읽는 패키지입니다. 공급처마다 하위 모듈이 하나씩 있고,
키가 필요 없거나(재무부) 선택입니다.

| 모듈 | 공급처 | 받는 것 |
|---|---|---|
| `cluefin_feeds.treasury` | 미 재무부 금리 XML 피드 | 명목 국채 수익률 곡선(1개월~30년, 일별) |

## 미 재무부 수익률 곡선

```python
from cluefin_feeds.treasury import Client

rows = Client().par_yield_curve("202610")  # 한 달(YYYYMM) 또는 한 해(YYYY)
latest = rows[-1]
print(latest.date, latest.year_10)  # 2026-10-16 4.05 (연 %, Decimal)
```

- 자료가 아직 없는 달(달 초)은 빈 목록입니다. 최근 값이 필요하면 지난달을 다시 묻습니다.
- 1.5·2·4개월물은 생긴 뒤부터만 값이 있고, 그 전은 `None`입니다.

## 오류

모든 예외는 `cluefin_feeds.FeedError`를 상속합니다. 429·5xx·타임아웃·연결 오류는 재시도한 뒤
`FeedRateLimitError`·`FeedServerError`·`FeedTimeoutError`·`FeedNetworkError`로, 형식이 맞지 않는 응답은
`FeedParseError`로 올라옵니다.
