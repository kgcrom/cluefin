# KIS API 커버리지 갭 분석

Python(`cluefin-openapi`)과 TypeScript(`cluefin-openapi-ts`) 간 KIS REST API 엔드포인트 커버리지 비교.

## 요약

| 모듈 | Python 엔드포인트 | TypeScript 엔드포인트 | 상태 |
| --- | ---: | ---: | --- |
| 국내주식 REST (6개 도메인) | 135 | 135 | 100% 일치 |
| Kiwoom 전체 (10개 도메인) | 134 | 134 | 100% 일치 |
| `OverseasBasicQuote` - 해외주식 시세 | 13 | 13 | 100% 일치 (신규 추가) |
| `OnmarketBondBasicQuote` - 장내채권 시세 | 8 | 8 | 100% 일치 (신규 추가) |
| `DomesticRealtimeQuote` - 국내 실시간 | 6 | - | 미구현 (WebSocket) |
| `OverseasRealtimeQuote` - 해외 실시간 | - | - | 미구현 (WebSocket) |
| `OnmarketBondRealtimeQuote` - 채권 실시간 | - | - | 미구현 (WebSocket) |
| **REST 합계** | **290** | **290** | **100%** |

> REST 엔드포인트 기준 Python과 TypeScript는 완전히 동일한 커버리지를 달성.

---

## OverseasBasicQuote - 해외주식 시세 (13 endpoints)

| # | 메서드명 | TR ID | HTTP | API 경로 | 상태 |
| ---: | --- | --- | --- | --- | --- |
| 1 | `getStockCurrentPriceDetail` | HHDFS76200200 | GET | `/uapi/overseas-price/v1/quotations/price-detail` | 완료 |
| 2 | `getCurrentPriceFirstQuote` | HHDFS76200100 | GET | `/uapi/overseas-price/v1/quotations/inquire-asking-price` | 완료 |
| 3 | `getStockCurrentPriceConclusion` | HHDFS00000300 | GET | `/uapi/overseas-price/v1/quotations/price` | 완료 |
| 4 | `getConclusionTrend` | HHDFS76200300 | GET | `/uapi/overseas-price/v1/quotations/inquire-ccnl` | 완료 |
| 5 | `getStockMinuteChart` | HHDFS76950200 | GET | `/uapi/overseas-price/v1/quotations/inquire-time-itemchartprice` | 완료 |
| 6 | `getIndexMinuteChart` | FHKST03030200 | GET | `/uapi/overseas-price/v1/quotations/inquire-time-indexchartprice` | 완료 |
| 7 | `getStockPeriodQuote` | HHDFS76240000 | GET | `/uapi/overseas-price/v1/quotations/dailyprice` | 완료 |
| 8 | `getItemIndexExchangePeriodPrice` | FHKST03030100 | GET | `/uapi/overseas-price/v1/quotations/inquire-daily-chartprice` | 완료 |
| 9 | `searchByCondition` | HHDFS76410000 | GET | `/uapi/overseas-price/v1/quotations/inquire-search` | 완료 |
| 10 | `getSettlementDate` | CTOS5011R | GET | `/uapi/overseas-stock/v1/quotations/countries-holiday` | 완료 |
| 11 | `getProductBaseInfo` | CTPF1702R | GET | `/uapi/overseas-price/v1/quotations/search-info` | 완료 |
| 12 | `getSectorPrice` | HHDFS76370000 | GET | `/uapi/overseas-price/v1/quotations/industry-theme` | 완료 |
| 13 | `getSectorCodes` | HHDFS76370100 | GET | `/uapi/overseas-price/v1/quotations/industry-price` | 완료 |

---

## OnmarketBondBasicQuote - 장내채권 시세 (8 endpoints)

| # | 메서드명 | TR ID | HTTP | API 경로 | 상태 |
| ---: | --- | --- | --- | --- | --- |
| 1 | `getBondAskingPrice` | FHKBJ773401C0 | GET | `/uapi/domestic-bond/v1/quotations/inquire-asking-price` | 완료 |
| 2 | `getBondPrice` | FHKBJ773400C0 | GET | `/uapi/domestic-bond/v1/quotations/inquire-price` | 완료 |
| 3 | `getBondExecution` | FHKBJ773403C0 | GET | `/uapi/domestic-bond/v1/quotations/inquire-ccnl` | 완료 |
| 4 | `getBondDailyPrice` | FHKBJ773404C0 | GET | `/uapi/domestic-bond/v1/quotations/inquire-daily-price` | 완료 |
| 5 | `getBondDailyChartPrice` | FHKBJ773701C0 | GET | `/uapi/domestic-bond/v1/quotations/inquire-daily-itemchartprice` | 완료 |
| 6 | `getBondAvgUnitPrice` | CTPF2005R | GET | `/uapi/domestic-bond/v1/quotations/avg-unit` | 완료 (*) |
| 7 | `getBondInfo` | CTPF1114R | GET | `/uapi/domestic-bond/v1/quotations/search-bond-info` | 완료 |
| 8 | `getBondIssueInfo` | CTPF1101R | GET | `/uapi/domestic-bond/v1/quotations/issue-info` | 완료 |

> (*) `getBondAvgUnitPrice` 제한 사항: KIS API는 `custtype` 헤더로 개인(`P`)/법인(`B`)을 구분하나, 현재 TypeScript 구현에서는 `http-client.ts`에서 `custtype: 'P'`로 하드코딩되어 있어 법인 계정 호출이 불가. `custtype` 파라미터가 metadata에 정의되어 있지만 query parameter로 전달될 뿐 헤더에 반영되지 않음. 향후 헤더 오버라이드 메커니즘 추가 시 해결 가능.

---

## 미구현 모듈 (이번 PR 범위 외)

### DomesticRealtimeQuote - 국내 실시간 시세 (WebSocket)

Python에서 `_domestic_realtime_quote.py`로 구현된 WebSocket 기반 실시간 스트리밍 모듈. REST API가 아닌 WebSocket 프로토콜을 사용하므로 metadata 기반 자동 생성 구조와 호환되지 않아 이번 PR에서 제외.

Python 구현 기능 (6개):
- `subscribe_execution` / `unsubscribe_execution` - 체결 실시간
- `subscribe_orderbook` / `unsubscribe_orderbook` - 호가 실시간
- `subscribe_execution_notification` / `unsubscribe_execution_notification` - 체결 통보

해외 실시간(`OverseasRealtimeQuote`), 채권 실시간(`OnmarketBondRealtimeQuote`)도 동일하게 WebSocket 기반이며 미구현.
