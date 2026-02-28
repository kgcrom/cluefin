# RPC 핸들러 확장: KIS/Kiwoom API 전면 노출

## 1. 개요

### 목적
cluefin-openapi에 이미 구현된 KIS ~190개, Kiwoom ~105개 API 메서드를 cluefin-rpc JSON-RPC 서버를 통해 체계적으로 노출하여, LLM이 `rpc.list_methods`로 카테고리별 탐색 → 필요한 메서드 호출하는 workflow를 구현한다.

### 현황
- 현재 RPC 노출: KIS 6개, Kiwoom 4개, KRX 2개, TA 11개, DART 4개, session 3개 = **총 30개**
- 이번 작업 후: KIS 113개, Kiwoom ~100개 추가 = **총 ~240개**

### 대상 카테고리

**KIS (한국투자증권):**
| 카테고리 | 서비스 클래스 | 메서드 수 |
|----------|-------------|-----------|
| 국내주식 기본시세 | `DomesticBasicQuote` | 21개 |
| 국내주식 업종/기타 | `DomesticIssueOther` | 14개 |
| 국내주식 종목정보 | `DomesticStockInfo` | 26개 |
| 국내주식 시세분석 | `DomesticMarketAnalysis` | 29개 |
| 국내주식 순위분석 | `DomesticRankingAnalysis` | 23개 |

**Kiwoom (키움증권):**
| 카테고리 | 서비스 클래스 | 메서드 수 |
|----------|-------------|-----------|
| 기관/외국인 | `DomesticForeign` | 3개 |
| 순위정보 | `DomesticRankInfo` | 22개 |
| 시세 | `DomesticMarketCondition` | 16개 |
| 업종 | `DomesticSector` | 6개 |
| 종목정보 | `DomesticStockInfo` | 28개 |
| 차트 | `DomesticChart` | 14개 |
| 테마 | `DomesticTheme` | 2개 |
| ETF | `DomesticETF` | 9개 |

---

## 2. 디렉토리 구조

### 변경 전
```
apps/cluefin-rpc/src/cluefin_rpc/handlers/
    __init__.py
    _base.py
    session.py
    ta.py
    dart.py
    quote.py        ← KIS(6) + Kiwoom(4) + KRX(2) 혼합
```

### 변경 후
```
apps/cluefin-rpc/src/cluefin_rpc/handlers/
    __init__.py
    _base.py                         # extract_output(), extract_body() 헬퍼 추가
    session.py                       # 유지
    ta.py                            # 유지
    dart.py                          # 유지
    quote.py                         # KRX 핸들러(2개)만 남김
    kis/                             # NEW
        __init__.py                  # register_kis_handlers() 집약
        domestic_basic_quote.py      # 21개 핸들러
        domestic_issue_other.py      # 14개 핸들러
        domestic_stock_info.py       # 26개 핸들러
        domestic_market_analysis.py  # 29개 핸들러
        domestic_ranking_analysis.py # 23개 핸들러
    kiwoom/                          # NEW
        __init__.py                  # register_kiwoom_handlers() 집약
        domestic_chart.py            # 14개 핸들러
        domestic_etf.py              # 9개 핸들러
        domestic_foreign.py          # 3개 핸들러
        domestic_market_condition.py # 16개 핸들러
        domestic_rank_info.py        # 22개 핸들러
        domestic_sector.py           # 6개 핸들러
        domestic_stock_info.py       # 28개 핸들러
        domestic_theme.py            # 2개 핸들러
```

---

## 3. RPC 메서드 네이밍 컨벤션

### 패턴: `{broker}.{category}.{method_name}`

기존 `quote.kis.stock_current` → `kis.basic_quote.stock_current_price`
기존 `quote.kiwoom.stock_daily` → `kiwoom.chart.stock_daily`

---

## 4. `_base.py` 헬퍼 함수

### 추가할 함수

```python
def extract_output(response, field: str = "output"):
    """KIS/Kiwoom 응답 body에서 특정 output 필드 추출 후 model_dump().

    KIS 응답은 output, output1, output2 필드 패턴을 사용.
    - output: Optional[Item] → 단일 객체 dict
    - output: Sequence[Item] → 리스트 of dict
    - output1 + output2: 요약 + 상세 리스트
    """
    body = response.body
    data = getattr(body, field, None)
    if data is None:
        return None
    if isinstance(data, (list, tuple)):
        return [item.model_dump() if hasattr(item, "model_dump") else item for item in data]
    return data.model_dump() if hasattr(data, "model_dump") else data


def extract_body(response):
    """응답 body 전체를 model_dump(). Kiwoom 응답에 적합.

    Kiwoom 응답은 output 대신 커스텀 필드명 사용 (etfprft_rt_lst 등).
    body 전체를 dump하면 return_code, return_msg + 데이터 필드 모두 포함.
    """
    return response.body.model_dump() if hasattr(response.body, "model_dump") else {}
```

---

## 5. KIS 핸들러 상세

### 5-1. `kis/domestic_basic_quote.py` (21개)

**소스 참조:** `packages/cluefin-openapi/src/cluefin_openapi/kis/_domestic_basic_quote.py`
**타입 참조:** `packages/cluefin-openapi/src/cluefin_openapi/kis/_domestic_basic_quote_types.py`

| RPC 메서드명 | API 메서드 | 파라미터 | output 패턴 |
|-------------|-----------|----------|-------------|
| `kis.basic_quote.stock_current_price` | `get_stock_current_price(fid_cond_mrkt_div_code, fid_input_iscd)` | `stock_code` (required), `market` (J/NX/UN, default J) | `output: Optional[Item]` |
| `kis.basic_quote.stock_current_price_2` | `get_stock_current_price_2(fid_cond_mrkt_div_code, fid_input_iscd)` | `stock_code`, `market` | `output: Optional[Item]` |
| `kis.basic_quote.stock_conclusion` | `get_stock_current_price_conclusion(fid_cond_mrkt_div_code, fid_input_iscd)` | `stock_code`, `market` | `output: Sequence[Item]` |
| `kis.basic_quote.stock_daily` | `get_stock_current_price_daily(fid_cond_mrkt_div_code, fid_input_iscd, fid_period_div_code, fid_org_adj_prc)` | `stock_code`, `market`, `period` (D/W/M), `adj_price` (0/1) | `output: Sequence[Item]` |
| `kis.basic_quote.stock_asking_expected` | `get_stock_current_price_asking_expected_conclusion(fid_cond_mrkt_div_code, fid_input_iscd)` | `stock_code`, `market` | `output1 + output2` |
| `kis.basic_quote.stock_investor` | `get_stock_current_price_investor(fid_cond_mrkt_div_code, fid_input_iscd)` | `stock_code`, `market` | `output: Sequence[Item]` |
| `kis.basic_quote.stock_member` | `get_stock_current_price_member(fid_cond_mrkt_div_code, fid_input_iscd)` | `stock_code`, `market` | `output: Sequence[Item]` |
| `kis.basic_quote.stock_period_quote` | `get_stock_period_quote(fid_cond_mrkt_div_code, fid_input_iscd, fid_input_date_1, fid_input_date_2, fid_period_div_code, fid_org_adj_prc)` | `stock_code`, `market`, `start_date`, `end_date`, `period` (D/W/M/Y), `adj_price` | `output1 + output2` |
| `kis.basic_quote.stock_today_minute` | `get_stock_today_minute_chart(fid_cond_mrkt_div_code, fid_input_iscd, fid_input_hour_1)` | `stock_code`, `market`, `hour` (HHMMSS) | `output1 + output2` |
| `kis.basic_quote.stock_daily_minute` | `get_stock_daily_minute_chart(...)` | 시그니처 참조 | `output1 + output2` |
| `kis.basic_quote.stock_time_conclusion` | `get_stock_current_price_time_item_conclusion(fid_cond_mrkt_div_code, fid_input_iscd, fid_input_hour_1)` | `stock_code`, `market`, `hour` | `output1 + output2` |
| `kis.basic_quote.stock_overtime_daily_price` | `get_stock_current_price_daily_overtime_price(fid_cond_mrkt_div_code, fid_input_iscd)` | `stock_code`, `market` | `output1 + output2` |
| `kis.basic_quote.stock_overtime_conclusion` | `get_stock_current_price_overtime_conclusion(fid_cond_mrkt_div_code, fid_input_iscd)` | `stock_code`, `market` | `output1 + output2` |
| `kis.basic_quote.stock_overtime_current_price` | `get_stock_overtime_current_price(fid_cond_mrkt_div_code, fid_input_iscd)` | `stock_code`, `market` | `output: Optional[Item]` |
| `kis.basic_quote.stock_overtime_asking_price` | `get_stock_overtime_asking_price(fid_cond_mrkt_div_code, fid_input_iscd)` | `stock_code`, `market` | `output: Optional[Item]` |
| `kis.basic_quote.stock_closing_expected_price` | `get_stock_closing_expected_price(fid_cond_mrkt_div_code, fid_input_iscd)` | `stock_code`, `market` | `output1: Sequence` |
| `kis.basic_quote.etf_etn_current_price` | `get_etfetn_current_price(fid_input_iscd)` | `stock_code` | `output: Optional[Item]` |
| `kis.basic_quote.etf_component_stock_price` | `get_etf_component_stock_price(...)` | 시그니처 참조 | `output1 + output2` |
| `kis.basic_quote.etf_nav_comparison_trend` | `get_etf_nav_comparison_trend(...)` | 시그니처 참조 | `output1 + output2` |
| `kis.basic_quote.etf_nav_comparison_daily` | `get_etf_nav_comparison_daily_trend(...)` | 시그니처 참조 | `output: Sequence` |
| `kis.basic_quote.etf_nav_comparison_time` | `get_etf_nav_comparison_time_trend(...)` | 시그니처 참조 | `output: Sequence` |

**기존 핸들러 마이그레이션:**
- `handle_kis_stock_current` → `kis.basic_quote.stock_current_price` (수동 필드 매핑 유지)
- `handle_kis_stock_daily` → `kis.basic_quote.stock_daily` (수동 필드 매핑 유지)
- `handle_kis_stock_period` → `kis.basic_quote.stock_period_quote`
- `handle_kis_stock_investor` → `kis.basic_quote.stock_investor`
- `handle_kis_etf_current` → `kis.basic_quote.etf_etn_current_price`

### 5-2. `kis/domestic_issue_other.py` (14개)

**소스 참조:** `packages/cluefin-openapi/src/cluefin_openapi/kis/_domestic_issue_other.py`
**타입 참조:** `packages/cluefin-openapi/src/cluefin_openapi/kis/_domestic_issue_other_types.py`

| RPC 메서드명 | API 메서드 | 주요 파라미터 |
|-------------|-----------|-------------|
| `kis.issue_other.sector_current_index` | `get_sector_current_index(fid_cond_mrkt_div_code, fid_input_iscd)` | `market`, `sector_code` |
| `kis.issue_other.sector_daily_index` | `get_sector_daily_index(fid_cond_mrkt_div_code, fid_input_iscd, fid_input_date_1, fid_input_date_2, fid_period_div_code)` | `market`, `sector_code`, `start_date`, `end_date`, `period` |
| `kis.issue_other.sector_time_index_second` | `get_sector_time_index_second(...)` | 시그니처 참조 |
| `kis.issue_other.sector_time_index_minute` | `get_sector_time_index_minute(...)` | 시그니처 참조 |
| `kis.issue_other.sector_minute_inquiry` | `get_sector_minute_inquiry(...)` | 시그니처 참조 |
| `kis.issue_other.sector_period_quote` | `get_sector_period_quote(...)` | 시그니처 참조 |
| `kis.issue_other.sector_all_quote_by_category` | `get_sector_all_quote_by_category(...)` | 시그니처 참조 |
| `kis.issue_other.expected_index_trend` | `get_expected_index_trend(...)` | 시그니처 참조 |
| `kis.issue_other.expected_index_all` | `get_expected_index_all(...)` | 시그니처 참조 |
| `kis.issue_other.volatility_interruption_status` | `get_volatility_interruption_status(...)` | 시그니처 참조 |
| `kis.issue_other.interest_rate_summary` | `get_interest_rate_summary(...)` | 시그니처 참조 |
| `kis.issue_other.market_announcement_schedule` | `get_market_announcement_schedule(...)` | 시그니처 참조 |
| `kis.issue_other.holiday_inquiry` | `get_holiday_inquiry(...)` | 시그니처 참조 |
| `kis.issue_other.futures_business_day_inquiry` | `get_futures_business_day_inquiry(...)` | 시그니처 참조 |

**기존 핸들러 마이그레이션:**
- `handle_kis_sector_index` → `kis.issue_other.sector_current_index`

### 5-3. `kis/domestic_stock_info.py` (26개)

**소스 참조:** `packages/cluefin-openapi/src/cluefin_openapi/kis/_domestic_stock_info.py`
**타입 참조:** `packages/cluefin-openapi/src/cluefin_openapi/kis/_domestic_stock_info_types.py`

| RPC 메서드명 | API 메서드 |
|-------------|-----------|
| `kis.stock_info.product_basic_info` | `get_product_basic_info(...)` |
| `kis.stock_info.stock_basic_info` | `get_stock_basic_info(...)` |
| `kis.stock_info.balance_sheet` | `get_balance_sheet(...)` |
| `kis.stock_info.income_statement` | `get_income_statement(...)` |
| `kis.stock_info.financial_ratio` | `get_financial_ratio(...)` |
| `kis.stock_info.profitability_ratio` | `get_profitability_ratio(...)` |
| `kis.stock_info.other_key_ratio` | `get_other_key_ratio(...)` |
| `kis.stock_info.stability_ratio` | `get_stability_ratio(...)` |
| `kis.stock_info.growth_ratio` | `get_growth_ratio(...)` |
| `kis.stock_info.margin_tradable_stocks` | `get_margin_tradable_stocks(...)` |
| `kis.stock_info.ksd_dividend_decision` | `get_ksd_dividend_decision(...)` |
| `kis.stock_info.ksd_stock_dividend_decision` | `get_ksd_stock_dividend_decision(...)` |
| `kis.stock_info.ksd_merger_split_decision` | `get_ksd_merger_split_decision(...)` |
| `kis.stock_info.ksd_par_value_change_decision` | `get_ksd_par_value_change_decision(...)` |
| `kis.stock_info.ksd_capital_reduction_schedule` | `get_ksd_capital_reduction_schedule(...)` |
| `kis.stock_info.ksd_listing_info_schedule` | `get_ksd_listing_info_schedule(...)` |
| `kis.stock_info.ksd_ipo_subscription_schedule` | `get_ksd_ipo_subscription_schedule(...)` |
| `kis.stock_info.ksd_forfeited_share_schedule` | `get_ksd_forfeited_share_schedule(...)` |
| `kis.stock_info.ksd_deposit_schedule` | `get_ksd_deposit_schedule(...)` |
| `kis.stock_info.ksd_paid_in_capital_increase_schedule` | `get_ksd_paid_in_capital_increase_schedule(...)` |
| `kis.stock_info.ksd_stock_dividend_schedule` | `get_ksd_stock_dividend_schedule(...)` |
| `kis.stock_info.ksd_shareholder_meeting_schedule` | `get_ksd_shareholder_meeting_schedule(...)` |
| `kis.stock_info.estimated_earnings` | `get_estimated_earnings(...)` |
| `kis.stock_info.stock_loanable_list` | `get_stock_loanable_list(...)` |
| `kis.stock_info.investment_opinion` | `get_investment_opinion(...)` |
| `kis.stock_info.investment_opinion_by_brokerage` | `get_investment_opinion_by_brokerage(...)` |

### 5-4. `kis/domestic_market_analysis.py` (29개)

**소스 참조:** `packages/cluefin-openapi/src/cluefin_openapi/kis/_domestic_market_analysis.py`
**타입 참조:** `packages/cluefin-openapi/src/cluefin_openapi/kis/_domestic_market_analysis_types.py`

| RPC 메서드명 | API 메서드 |
|-------------|-----------|
| `kis.market_analysis.trading_weight_by_amount` | `get_trading_weight_by_amount(...)` |
| `kis.market_analysis.buy_sell_volume_by_stock_daily` | `get_buy_sell_volume_by_stock_daily(...)` |
| `kis.market_analysis.investor_trend_by_stock_daily` | `get_investor_trading_trend_by_stock_daily(...)` |
| `kis.market_analysis.investor_trend_by_market_daily` | `get_investor_trading_trend_by_market_daily(...)` |
| `kis.market_analysis.investor_trend_by_market_intraday` | `get_investor_trading_trend_by_market_intraday(...)` |
| `kis.market_analysis.foreign_brokerage_aggregate` | `get_foreign_brokerage_trading_aggregate(...)` |
| `kis.market_analysis.institutional_foreign_aggregate` | `get_institutional_foreign_trading_aggregate(...)` |
| `kis.market_analysis.foreign_net_buy_trend` | `get_foreign_net_buy_trend_by_stock(...)` |
| `kis.market_analysis.foreign_institutional_estimate` | `get_foreign_institutional_estimate_by_stock(...)` |
| `kis.market_analysis.member_trend_by_stock` | `get_member_trading_trend_by_stock(...)` |
| `kis.market_analysis.member_trend_tick` | `get_member_trading_trend_tick(...)` |
| `kis.market_analysis.program_summary_daily` | `get_program_trading_summary_daily(...)` |
| `kis.market_analysis.program_summary_intraday` | `get_program_trading_summary_intraday(...)` |
| `kis.market_analysis.program_trend_by_stock_daily` | `get_program_trading_trend_by_stock_daily(...)` |
| `kis.market_analysis.program_trend_by_stock_intraday` | `get_program_trading_trend_by_stock_intraday(...)` |
| `kis.market_analysis.program_investor_trend_today` | `get_program_trading_investor_trend_today(...)` |
| `kis.market_analysis.short_selling_trend_daily` | `get_short_selling_trend_daily(...)` |
| `kis.market_analysis.stock_loan_trend_daily` | `get_stock_loan_trend_daily(...)` |
| `kis.market_analysis.credit_balance_trend_daily` | `get_credit_balance_trend_daily(...)` |
| `kis.market_analysis.resistance_level_trading_weight` | `get_resistance_level_trading_weight(...)` |
| `kis.market_analysis.limit_price_stocks` | `get_limit_price_stocks(...)` |
| `kis.market_analysis.market_fund_summary` | `get_market_fund_summary(...)` |
| `kis.market_analysis.expected_price_trend` | `get_expected_price_trend(...)` |
| `kis.market_analysis.after_hours_expected_fluctuation` | `get_after_hours_expected_fluctuation(...)` |
| `kis.market_analysis.watchlist_groups` | `get_watchlist_groups(...)` |
| `kis.market_analysis.watchlist_stocks_by_group` | `get_watchlist_stocks_by_group(...)` |
| `kis.market_analysis.watchlist_multi_quote` | `get_watchlist_multi_quote(...)` |
| `kis.market_analysis.condition_search_list` | `get_condition_search_list(...)` |
| `kis.market_analysis.condition_search_result` | `get_condition_search_result(...)` |

### 5-5. `kis/domestic_ranking_analysis.py` (23개)

**소스 참조:** `packages/cluefin-openapi/src/cluefin_openapi/kis/_domestic_ranking_analysis.py`
**타입 참조:** `packages/cluefin-openapi/src/cluefin_openapi/kis/_domestic_ranking_analysis_types.py`

| RPC 메서드명 | API 메서드 |
|-------------|-----------|
| `kis.ranking.trading_volume` | `get_trading_volume_rank(...)` |
| `kis.ranking.stock_fluctuation` | `get_stock_fluctuation_rank(...)` |
| `kis.ranking.large_execution_count` | `get_stock_large_execution_count_top(...)` |
| `kis.ranking.execution_strength` | `get_stock_execution_strength_top(...)` |
| `kis.ranking.after_hours_fluctuation` | `get_stock_after_hours_fluctuation_rank(...)` |
| `kis.ranking.after_hours_volume` | `get_stock_after_hours_volume_rank(...)` |
| `kis.ranking.market_cap` | `get_stock_market_cap_top(...)` |
| `kis.ranking.profit` | `get_stock_profit_top(...)` |
| `kis.ranking.expected_execution_rise_decline` | `get_stock_expected_execution_rise_decline_top(...)` |
| `kis.ranking.hoga_quantity` | `get_stock_hoga_quantity_rank(...)` |
| `kis.ranking.preferred_stock_ratio` | `get_stock_preferred_stock_ratio_top(...)` |
| `kis.ranking.market_price` | `get_stock_market_price_rank(...)` |
| `kis.ranking.credit_balance` | `get_stock_credit_balance_top(...)` |
| `kis.ranking.short_selling` | `get_stock_short_selling_top(...)` |
| `kis.ranking.disparity_index` | `get_stock_disparity_index_rank(...)` |
| `kis.ranking.proprietary_trading` | `get_stock_proprietary_trading_top(...)` |
| `kis.ranking.dividend_yield` | `get_stock_dividend_yield_top(...)` |
| `kis.ranking.finance_ratio` | `get_stock_finance_ratio_rank(...)` |
| `kis.ranking.profitability_indicator` | `get_stock_profitability_indicator_rank(...)` |
| `kis.ranking.new_high_low_approaching` | `get_stock_new_high_low_approaching_top(...)` |
| `kis.ranking.watchlist_registration` | `get_stock_watchlist_registration_top(...)` |
| `kis.ranking.hts_inquiry_top_20` | `get_hts_inquiry_top_20(...)` |
| `kis.ranking.time_hoga` | `get_stock_time_hoga_rank(...)` |

---

## 6. Kiwoom 핸들러 상세

### 6-1. `kiwoom/domestic_chart.py` (14개)

**소스 참조:** `packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_chart.py`
**타입 참조:** `packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_chart_types.py`

| RPC 메서드명 | API 메서드 | 주요 파라미터 |
|-------------|-----------|-------------|
| `kiwoom.chart.stock_tick` | `get_stock_tick(stk_cd, tic_scope, upd_stkpc_tp)` | `stock_code`, `tic_scope`, `adj_price` (0/1) |
| `kiwoom.chart.stock_minute` | `get_stock_minute(stk_cd, tic_scope, upd_stkpc_tp)` | `stock_code`, `tic_scope`, `adj_price` |
| `kiwoom.chart.stock_daily` | `get_stock_daily(stk_cd, base_dt, upd_stkpc_tp)` | `stock_code`, `base_date`, `adj_price` |
| `kiwoom.chart.stock_weekly` | `get_stock_weekly(stk_cd, base_dt, upd_stkpc_tp)` | `stock_code`, `base_date`, `adj_price` |
| `kiwoom.chart.stock_monthly` | `get_stock_monthly(stk_cd, base_dt, upd_stkpc_tp)` | `stock_code`, `base_date`, `adj_price` |
| `kiwoom.chart.stock_yearly` | `get_stock_yearly(stk_cd, base_dt, upd_stkpc_tp)` | `stock_code`, `base_date`, `adj_price` |
| `kiwoom.chart.industry_tick` | `get_industry_tick(inds_cd, tic_scope)` | `industry_code`, `tic_scope` |
| `kiwoom.chart.industry_minute` | `get_industry_minute(inds_cd, tic_scope)` | `industry_code`, `tic_scope` |
| `kiwoom.chart.industry_daily` | `get_industry_daily(inds_cd, base_dt)` | `industry_code`, `base_date` |
| `kiwoom.chart.industry_weekly` | `get_industry_weekly(inds_cd, base_dt)` | `industry_code`, `base_date` |
| `kiwoom.chart.industry_monthly` | `get_industry_monthly(inds_cd, base_dt)` | `industry_code`, `base_date` |
| `kiwoom.chart.industry_yearly` | `get_industry_yearly(inds_cd, base_dt)` | `industry_code`, `base_date` |
| `kiwoom.chart.institutional_by_stock` | `get_individual_stock_institutional_chart(dt, stk_cd, amt_qty_tp, trde_tp, unit_tp)` | `date`, `stock_code`, `amount_qty_type`, `trade_type`, `unit_type` |
| `kiwoom.chart.intraday_investor_trading` | `get_intraday_investor_trading(mrkt_tp, amt_qty_tp, trde_tp, stk_cd)` | `market_type`, `amount_qty_type`, `trade_type`, `stock_code` |

**기존 핸들러 마이그레이션:**
- `handle_kiwoom_stock_daily` → `kiwoom.chart.stock_daily`
- `handle_kiwoom_stock_minute` → `kiwoom.chart.stock_minute`
- `handle_kiwoom_stock_weekly` → `kiwoom.chart.stock_weekly`
- `handle_kiwoom_stock_monthly` → `kiwoom.chart.stock_monthly`

### 6-2. `kiwoom/domestic_etf.py` (9개)

**소스 참조:** `packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_etf.py`
**타입 참조:** `packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_etf_types.py`

| RPC 메서드명 | API 메서드 | 주요 파라미터 |
|-------------|-----------|-------------|
| `kiwoom.etf.return_rate` | `get_etf_return_rate(stk_cd, etfobjt_idex_cd, dt)` | `stock_code`, `index_code`, `period` (0~3) |
| `kiwoom.etf.item_info` | `get_etf_item_info(stk_cd)` | `stock_code` |
| `kiwoom.etf.daily_trend` | `get_etf_daily_trend(stk_cd)` | `stock_code` |
| `kiwoom.etf.full_price` | `get_etf_full_price(txon_type, navpre, mngmcomp, txon_yn, trace_idex, stex_tp)` | `tax_type`, `nav_premium`, `management_company`, `tax_yn`, `trace_index`, `exchange_type` |
| `kiwoom.etf.hourly_trend` | `get_etf_hourly_trend(stk_cd)` | `stock_code` |
| `kiwoom.etf.hourly_execution` | `get_etf_hourly_execution(stk_cd)` | `stock_code` |
| `kiwoom.etf.daily_execution` | `get_etf_daily_execution(stk_cd)` | `stock_code` |
| `kiwoom.etf.hourly_execution_v2` | `get_etf_hourly_execution_v2(stk_cd)` | `stock_code` |
| `kiwoom.etf.hourly_trend_v2` | `get_etf_hourly_trend_v2(stk_cd)` | `stock_code` |

### 6-3. `kiwoom/domestic_foreign.py` (3개)

**소스 참조:** `packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_foreign.py`
**타입 참조:** `packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_foreign_types.py`

| RPC 메서드명 | API 메서드 | 주요 파라미터 |
|-------------|-----------|-------------|
| `kiwoom.foreign.investor_trading_trend` | `get_foreign_investor_trading_trend_by_stock(stk_cd)` | `stock_code` |
| `kiwoom.foreign.stock_institution` | `get_stock_institution(stk_cd)` | `stock_code` |
| `kiwoom.foreign.consecutive_net_buy_sell` | `get_consecutive_net_buy_sell_status_by_institution_foreigner(dt, mrkt_tp, stk_inds_tp, amt_qty_tp, stex_tp, ...)` | `period`, `market_type`, `stock_industry_type`, `amount_qty_type`, `exchange_type` |

### 6-4. `kiwoom/domestic_market_condition.py` (16개)

**소스 참조:** `packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_market_condition.py`
**타입 참조:** `packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_market_condition_types.py`

| RPC 메서드명 | API 메서드 |
|-------------|-----------|
| `kiwoom.market_condition.stock_quote` | `get_stock_quote(stk_cd)` |
| `kiwoom.market_condition.stock_quote_by_date` | `get_stock_quote_by_date(stk_cd)` |
| `kiwoom.market_condition.stock_price` | `get_stock_price(stk_cd)` |
| `kiwoom.market_condition.market_sentiment` | `get_market_sentiment_info(stk_cd)` |
| `kiwoom.market_condition.new_stock_warrant_price` | `get_new_stock_warrant_price(newstk_recvrht_tp)` |
| `kiwoom.market_condition.daily_institutional_trading` | `get_daily_institutional_trading_items(...)` |
| `kiwoom.market_condition.institutional_trend_by_stock` | `get_institutional_trading_trend_by_stock(...)` |
| `kiwoom.market_condition.execution_intensity_by_time` | `get_execution_intensity_trend_by_time(stk_cd)` |
| `kiwoom.market_condition.execution_intensity_by_date` | `get_execution_intensity_trend_by_date(stk_cd)` |
| `kiwoom.market_condition.intraday_trading_by_investor` | `get_intraday_trading_by_investor(...)` |
| `kiwoom.market_condition.after_market_trading_by_investor` | `get_after_market_trading_by_investor(...)` |
| `kiwoom.market_condition.securities_firm_trend` | `get_securities_firm_trading_trend_by_stock(...)` |
| `kiwoom.market_condition.daily_stock_price` | `get_daily_stock_price(stk_cd, qry_dt, indc_tp)` |
| `kiwoom.market_condition.after_hours_single_price` | `get_after_hours_single_price(stk_cd)` |
| `kiwoom.market_condition.program_trading_trend_by_time` | `get_program_trading_trend_by_time(...)` |
| `kiwoom.market_condition.program_trading_cumulative` | `get_program_trading_cumulative_trend(...)` |

**참고:** 프로그램매매 관련 6개 메서드 중 대표적인 것만 포함. 나머지도 구현 시 추가.

### 6-5. `kiwoom/domestic_rank_info.py` (22개)

**소스 참조:** `packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_rank_info.py`
**타입 참조:** `packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_rank_info_types.py`

| RPC 메서드명 | API 메서드 |
|-------------|-----------|
| `kiwoom.rank_info.remaining_order_qty` | `get_top_remaining_order_quantity(mrkt_tp, sort_tp)` |
| `kiwoom.rank_info.increasing_remaining_order` | `get_rapidly_increasing_remaining_order_quantity(mrkt_tp)` |
| `kiwoom.rank_info.increasing_total_sell` | `get_rapidly_increasing_total_sell_orders(mrkt_tp)` |
| `kiwoom.rank_info.increasing_volume` | `get_rapidly_increasing_trading_volume(mrkt_tp)` |
| `kiwoom.rank_info.pct_change_from_prev` | `get_top_percentage_change_from_previous_day(mrkt_tp, sort_tp)` |
| `kiwoom.rank_info.expected_conclusion_pct_change` | `get_top_expected_conclusion_percentage_change(mrkt_tp)` |
| `kiwoom.rank_info.current_day_volume` | `get_top_current_day_trading_volume(mrkt_tp)` |
| `kiwoom.rank_info.prev_day_volume` | `get_top_previous_day_trading_volume(mrkt_tp)` |
| `kiwoom.rank_info.transaction_value` | `get_top_transaction_value(mrkt_tp)` |
| `kiwoom.rank_info.margin_ratio` | `get_top_margin_ratio(mrkt_tp)` |
| `kiwoom.rank_info.foreigner_period_trading` | `get_top_foreigner_period_trading(mrkt_tp)` |
| `kiwoom.rank_info.consecutive_net_buy_sell_foreigners` | `get_top_consecutive_net_buy_sell_by_foreigners(mrkt_tp)` |
| `kiwoom.rank_info.limit_exhaustion_rate_foreigner` | `get_top_limit_exhaustion_rate_foreigner(mrkt_tp)` |
| `kiwoom.rank_info.foreign_account_group_trading` | `get_top_foreign_account_group_trading(mrkt_tp)` |
| `kiwoom.rank_info.securities_firm_by_stock` | `get_stock_specific_securities_firm_ranking(mmcm_cd)` |
| `kiwoom.rank_info.securities_firm_trading` | `get_top_securities_firm_trading(mrkt_tp)` |
| `kiwoom.rank_info.current_day_major_traders` | `get_top_current_day_major_traders(mrkt_tp)` |
| `kiwoom.rank_info.net_buy_trader` | `get_top_net_buy_trader_ranking(mrkt_tp)` |
| `kiwoom.rank_info.current_day_deviation_sources` | `get_top_current_day_deviation_sources(mrkt_tp)` |
| `kiwoom.rank_info.same_net_buy_sell` | `get_same_net_buy_sell_ranking(mrkt_tp)` |
| `kiwoom.rank_info.intraday_trading_by_investor` | `get_top_intraday_trading_by_investor(mrkt_tp, amt_qty_tp, invsr)` |
| `kiwoom.rank_info.after_hours_single_price_change` | `get_after_hours_single_price_change_rate_ranking(mrkt_tp)` |

### 6-6. `kiwoom/domestic_sector.py` (6개)

**소스 참조:** `packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_sector.py`
**타입 참조:** `packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_sector_types.py`

| RPC 메서드명 | API 메서드 | 주요 파라미터 |
|-------------|-----------|-------------|
| `kiwoom.sector.program` | `get_industry_program(stk_code)` | `stock_code` |
| `kiwoom.sector.investor_net_buy` | `get_industry_investor_net_buy(mrkt_tp, amt_qty_tp, base_dt, stex_tp)` | `market_type`, `amount_qty_type`, `base_date`, `exchange_type` |
| `kiwoom.sector.current_price` | `get_industry_current_price(mrkt_tp, inds_cd)` | `market_type`, `industry_code` |
| `kiwoom.sector.price_by_sector` | `get_industry_price_by_sector(mrkt_tp, inds_cd, stex_tp)` | `market_type`, `industry_code`, `exchange_type` |
| `kiwoom.sector.all_index` | `get_all_industry_index(inds_cd)` | `industry_code` |
| `kiwoom.sector.daily_current_price` | `get_daily_industry_current_price(mrkt_tp, inds_cd)` | `market_type`, `industry_code` |

### 6-7. `kiwoom/domestic_stock_info.py` (28개)

**소스 참조:** `packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_stock_info.py`
**타입 참조:** `packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_stock_info_types.py`

| RPC 메서드명 | API 메서드 |
|-------------|-----------|
| `kiwoom.stock_info.basic` | `get_stock_info(stk_cd)` |
| `kiwoom.stock_info.trading_member` | `get_stock_trading_member(stk_cd)` |
| `kiwoom.stock_info.execution` | `get_execution(stk_cd)` |
| `kiwoom.stock_info.margin_trading_trend` | `get_margin_trading_trend(stk_cd, dt, qry_tp)` |
| `kiwoom.stock_info.daily_trading_details` | `get_daily_trading_details(stk_cd, strt_dt)` |
| `kiwoom.stock_info.new_high_low_price` | `get_new_high_low_price(mrkt_tp, ntl_tp, high_low_close_tp, stk_cnd, trde_qty_tp, crd_cnd, updown_incls, dt, stex_tp)` |
| `kiwoom.stock_info.upper_lower_limit` | `get_upper_lower_limit_price(mrkt_tp, updown_tp, sort_tp, stk_cnd, trde_qty_tp, crd_cnd, trde_gold_tp, stex_tp)` |
| `kiwoom.stock_info.high_low_approach` | `get_high_low_price_approach(stk_cd, qry_tp)` |
| `kiwoom.stock_info.price_volatility` | `get_price_volatility(stk_cd)` |
| `kiwoom.stock_info.volume_renewal` | `get_trading_volume_renewal()` |
| `kiwoom.stock_info.supply_demand_concentration` | `get_supply_demand_concentration()` |
| `kiwoom.stock_info.high_per` | `get_high_per(mrkt_tp)` |
| `kiwoom.stock_info.change_rate_from_open` | `get_change_rate_from_open(mrkt_tp)` |
| `kiwoom.stock_info.trading_member_supply_demand` | `get_trading_member_supply_demand_analysis(mmcm_cd)` |
| `kiwoom.stock_info.trading_member_instant_volume` | `get_trading_member_instant_volume(mmcm_cd)` |
| `kiwoom.stock_info.volatility_control_event` | `get_volatility_control_event()` |
| `kiwoom.stock_info.prev_day_execution_volume` | `get_daily_previous_day_execution_volume()` |
| `kiwoom.stock_info.daily_trading_by_investor` | `get_daily_trading_items_by_investor(strt_dt, end_dt, mrkt_tp, stex_tp)` |
| `kiwoom.stock_info.institutional_by_stock` | `get_institutional_investor_by_stock(stk_cd)` |
| `kiwoom.stock_info.total_institutional_by_stock` | `get_total_institutional_investor_by_stock(stk_cd)` |
| `kiwoom.stock_info.prev_day_conclusion` | `get_daily_previous_day_conclusion()` |
| `kiwoom.stock_info.interest_stock` | `get_interest_stock_info()` |
| `kiwoom.stock_info.summary` | `get_stock_info_summary()` |
| `kiwoom.stock_info.basic_v1` | `get_stock_info_v1(stk_cd)` |
| `kiwoom.stock_info.industry_code` | `get_industry_code(stk_cd)` |
| `kiwoom.stock_info.member_company` | `get_member_company()` |
| `kiwoom.stock_info.program_net_buy_top50` | `get_top_50_program_net_buy()` |
| `kiwoom.stock_info.program_trading_by_stock` | `get_program_trading_status_by_stock(stk_cd)` |

### 6-8. `kiwoom/domestic_theme.py` (2개)

**소스 참조:** `packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_theme.py`
**타입 참조:** `packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_theme_types.py`

| RPC 메서드명 | API 메서드 | 주요 파라미터 |
|-------------|-----------|-------------|
| `kiwoom.theme.group` | `get_theme_group(qry_tp, date_tp, thema_nm, flu_pl_amt_tp, stex_tp, stk_cd)` | `query_type`, `date_type`, `theme_name`, `fluctuation_type`, `exchange_type`, `stock_code` |
| `kiwoom.theme.group_stocks` | `get_theme_group_stocks(thema_grp_cd, stex_tp, date_tp)` | `theme_group_code`, `exchange_type`, `date_type` |

---

## 7. 응답 구조 참고

### KIS 응답 body output 패턴

| 패턴 | 예시 | 설명 |
|------|------|------|
| `output: Optional[Item]` | stock_current_price | 단일 객체 |
| `output: Sequence[Item]` | ranking 전체, investor, member | 리스트 |
| `output1 + output2` | period_quote, minute_chart | 요약 + 상세 리스트 |
| `output1: Sequence[Item]` | closing_expected_price, dividend_yield_top | 리스트 (output1) |

### Kiwoom 응답 body 패턴

| 타입 | 필드명 예시 |
|------|-----------|
| `DomesticEtfReturnRate` | `etfprft_rt_lst: list[Item]` |
| `DomesticEtfDailyTrend` | `etfdaly_trnsn: list[Item]` |
| 차트 응답 | `output: list[Item]` (일부는 output 사용) |

→ Kiwoom은 `extract_body(response)` 로 전체 body dump하는 것이 가장 일관적.

---

## 8. `quote.py` 마이그레이션 상세

### 제거할 핸들러 (새 파일로 이전)
- `handle_kis_stock_current` → `kis/domestic_basic_quote.py`
- `handle_kis_stock_daily` → `kis/domestic_basic_quote.py`
- `handle_kis_stock_period` → `kis/domestic_basic_quote.py`
- `handle_kis_stock_investor` → `kis/domestic_basic_quote.py`
- `handle_kis_etf_current` → `kis/domestic_basic_quote.py`
- `handle_kis_sector_index` → `kis/domestic_issue_other.py`
- `handle_kiwoom_stock_daily` → `kiwoom/domestic_chart.py`
- `handle_kiwoom_stock_minute` → `kiwoom/domestic_chart.py`
- `handle_kiwoom_stock_weekly` → `kiwoom/domestic_chart.py`
- `handle_kiwoom_stock_monthly` → `kiwoom/domestic_chart.py`

### `quote.py`에 남길 핸들러
- `handle_krx_kospi`
- `handle_krx_kosdaq`

---

## 9. `server.py` 변경사항

### 변경 전
```python
from cluefin_rpc.handlers.quote import register_quote_handlers
# ...
register_quote_handlers(dispatcher)
```

### 변경 후
```python
from cluefin_rpc.handlers.kis import register_kis_handlers
from cluefin_rpc.handlers.kiwoom import register_kiwoom_handlers
from cluefin_rpc.handlers.quote import register_quote_handlers  # KRX만

# _build_dispatcher():
register_kis_handlers(dispatcher)
register_kiwoom_handlers(dispatcher)
register_quote_handlers(dispatcher)

# main():
register_kis_handlers(dispatcher)
register_kiwoom_handlers(dispatcher)
register_quote_handlers(dispatcher)
```

---

## 10. `kis/__init__.py` / `kiwoom/__init__.py`

### `handlers/kis/__init__.py`
```python
from cluefin_rpc.handlers.kis.domestic_basic_quote import register_kis_basic_quote_handlers
from cluefin_rpc.handlers.kis.domestic_issue_other import register_kis_issue_other_handlers
from cluefin_rpc.handlers.kis.domestic_stock_info import register_kis_stock_info_handlers
from cluefin_rpc.handlers.kis.domestic_market_analysis import register_kis_market_analysis_handlers
from cluefin_rpc.handlers.kis.domestic_ranking_analysis import register_kis_ranking_handlers

def register_kis_handlers(dispatcher):
    register_kis_basic_quote_handlers(dispatcher)
    register_kis_issue_other_handlers(dispatcher)
    register_kis_stock_info_handlers(dispatcher)
    register_kis_market_analysis_handlers(dispatcher)
    register_kis_ranking_handlers(dispatcher)
```

### `handlers/kiwoom/__init__.py`
```python
from cluefin_rpc.handlers.kiwoom.domestic_chart import register_kiwoom_chart_handlers
from cluefin_rpc.handlers.kiwoom.domestic_etf import register_kiwoom_etf_handlers
from cluefin_rpc.handlers.kiwoom.domestic_foreign import register_kiwoom_foreign_handlers
from cluefin_rpc.handlers.kiwoom.domestic_market_condition import register_kiwoom_market_condition_handlers
from cluefin_rpc.handlers.kiwoom.domestic_rank_info import register_kiwoom_rank_info_handlers
from cluefin_rpc.handlers.kiwoom.domestic_sector import register_kiwoom_sector_handlers
from cluefin_rpc.handlers.kiwoom.domestic_stock_info import register_kiwoom_stock_info_handlers
from cluefin_rpc.handlers.kiwoom.domestic_theme import register_kiwoom_theme_handlers

def register_kiwoom_handlers(dispatcher):
    register_kiwoom_chart_handlers(dispatcher)
    register_kiwoom_etf_handlers(dispatcher)
    register_kiwoom_foreign_handlers(dispatcher)
    register_kiwoom_market_condition_handlers(dispatcher)
    register_kiwoom_rank_info_handlers(dispatcher)
    register_kiwoom_sector_handlers(dispatcher)
    register_kiwoom_stock_info_handlers(dispatcher)
    register_kiwoom_theme_handlers(dispatcher)
```

---

## 11. 핸들러 구현 템플릿

### KIS 핸들러 (단일 output)
```python
@rpc_method(
    name="kis.basic_quote.stock_overtime_current_price",
    description="Get overtime current price for a stock from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "6-digit stock code"},
            "market": {"type": "string", "enum": ["J", "NX", "UN"], "description": "Market code. Default J."},
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="kis.basic_quote",
    broker="kis",
)
def handle_kis_stock_overtime_current_price(params: dict, session) -> dict:
    kis = session.get_kis()
    market = params.get("market", "J")
    response = kis.domestic_basic_quote.get_stock_overtime_current_price(market, params["stock_code"])
    result = extract_output(response, "output")
    if result is None:
        return {"stock_code": params["stock_code"], "error": "No data returned"}
    return {"stock_code": params["stock_code"], **result}
```

### KIS 핸들러 (output1 + output2 리스트)
```python
@rpc_method(
    name="kis.basic_quote.stock_period_quote",
    description="Get stock price for a specific date range from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "6-digit stock code"},
            "start_date": {"type": "string", "description": "Start date (YYYYMMDD)"},
            "end_date": {"type": "string", "description": "End date (YYYYMMDD)"},
            "market": {"type": "string", "enum": ["J", "NX", "UN"], "description": "Market code. Default J."},
            "period": {"type": "string", "enum": ["D", "W", "M", "Y"], "description": "Period. Default D."},
            "adj_price": {"type": "string", "enum": ["0", "1"], "description": "0:adjusted, 1:original. Default 0."},
        },
        "required": ["stock_code", "start_date", "end_date"],
    },
    returns={"type": "object"},
    category="kis.basic_quote",
    broker="kis",
)
def handle_kis_stock_period_quote(params: dict, session) -> dict:
    kis = session.get_kis()
    market = params.get("market", "J")
    period = params.get("period", "D")
    adj = params.get("adj_price", "0")
    response = kis.domestic_basic_quote.get_stock_period_quote(
        market, params["stock_code"], params["start_date"], params["end_date"], period, adj
    )
    return {
        "stock_code": params["stock_code"],
        "summary": extract_output(response, "output1"),
        "data": extract_output(response, "output2"),
    }
```

### KIS 순위 핸들러 (다수 파라미터)
```python
@rpc_method(
    name="kis.ranking.trading_volume",
    description="Get trading volume ranking from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "market": {"type": "string", "enum": ["J", "NX"], "description": "Market code"},
            "sector_code": {"type": "string", "description": "Sector code. 0000 for all."},
            "classification": {"type": "string", "enum": ["0", "1", "2"], "description": "0:all, 1:common, 2:preferred"},
            "sort_by": {"type": "string", "enum": ["0", "1", "2", "3", "4"], "description": "0:avg vol, 1:increase rate, 2:avg turnover, 3:amount, 4:avg amount turnover"},
        },
        "required": ["market"],
    },
    returns={"type": "object"},
    category="kis.ranking",
    broker="kis",
)
def handle_kis_trading_volume_rank(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_ranking_analysis.get_trading_volume_rank(
        fid_cond_mrkt_div_code=params["market"],
        fid_cond_scr_div_code="20171",
        fid_input_iscd=params.get("sector_code", "0000"),
        fid_div_cls_code=params.get("classification", "0"),
        fid_blng_cls_code=params.get("sort_by", "0"),
        fid_trgt_cls_code=params.get("target_cls", "111111111"),
        fid_trgt_exls_cls_code=params.get("target_exclude_cls", "0000000000"),
        fid_input_price_1=params.get("price_min", ""),
        fid_input_price_2=params.get("price_max", ""),
        fid_vol_cnt=params.get("volume_min", ""),
        fid_input_date_1=params.get("date", ""),
    )
    return {"data": extract_output(response, "output")}
```

### Kiwoom 핸들러 (body dump)
```python
@rpc_method(
    name="kiwoom.etf.return_rate",
    description="Get ETF return rate from Kiwoom.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "ETF stock code (e.g. 069500)"},
            "index_code": {"type": "string", "description": "ETF target index code (e.g. 001)"},
            "period": {"type": "integer", "enum": [0, 1, 2, 3], "description": "0:1week, 1:1month, 2:6months, 3:1year"},
        },
        "required": ["stock_code", "index_code", "period"],
    },
    returns={"type": "object"},
    category="kiwoom.etf",
    broker="kiwoom",
)
def handle_kiwoom_etf_return_rate(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.etf.get_etf_return_rate(
        params["stock_code"], params["index_code"], params["period"]
    )
    return extract_body(response)
```

---

## 12. 구현 순서

| 단계 | 작업 | 파일 |
|------|------|------|
| 1 | `_base.py`에 `extract_output()`, `extract_body()` 헬퍼 추가 | `handlers/_base.py` |
| 2 | `handlers/kis/__init__.py` 생성 | |
| 3 | `handlers/kis/domestic_basic_quote.py` 생성 (21개, 기존 6개 마이그레이션 포함) | |
| 4 | `handlers/kis/domestic_issue_other.py` 생성 (14개, 기존 1개 마이그레이션 포함) | |
| 5 | `handlers/kis/domestic_stock_info.py` 생성 (26개) | |
| 6 | `handlers/kis/domestic_market_analysis.py` 생성 (29개) | |
| 7 | `handlers/kis/domestic_ranking_analysis.py` 생성 (23개) | |
| 8 | `handlers/kiwoom/__init__.py` 생성 | |
| 9 | `handlers/kiwoom/domestic_chart.py` 생성 (14개, 기존 4개 마이그레이션 포함) | |
| 10 | `handlers/kiwoom/domestic_etf.py` 생성 (9개) | |
| 11 | `handlers/kiwoom/domestic_foreign.py` 생성 (3개) | |
| 12 | `handlers/kiwoom/domestic_market_condition.py` 생성 (16개) | |
| 13 | `handlers/kiwoom/domestic_rank_info.py` 생성 (22개) | |
| 14 | `handlers/kiwoom/domestic_sector.py` 생성 (6개) | |
| 15 | `handlers/kiwoom/domestic_stock_info.py` 생성 (28개) | |
| 16 | `handlers/kiwoom/domestic_theme.py` 생성 (2개) | |
| 17 | `quote.py`에서 KIS/Kiwoom 핸들러 제거, KRX만 남김 | `handlers/quote.py` |
| 18 | `server.py` 등록 코드 업데이트 | `server.py` |
| 19 | 테스트 작성 및 검증 | `tests/` |

---

## 13. 테스트 전략

### 단위 테스트
- 각 핸들러 파일별: `_ALL_HANDLERS`의 `_rpc_schema` 존재 검증, category/broker 일치 검증
- 대표 핸들러 2-3개에 대해 mock 기반 호출 테스트

### 통합 검증
```bash
# 전체 메서드 목록 출력 검증
uv run python -m cluefin_rpc.server --list-methods

# 린트
uv run ruff format apps/cluefin-rpc && uv run ruff check apps/cluefin-rpc --fix

# 테스트
uv run pytest apps/cluefin-rpc/tests -m "not integration"
```

---

## 14. 파라미터 매핑 규칙

### KIS API 파라미터 → RPC 파라미터
| KIS 원본 | RPC 파라미터 | 설명 |
|----------|-------------|------|
| `fid_cond_mrkt_div_code` | `market` | 시장 코드 (J/NX/UN) |
| `fid_input_iscd` | `stock_code` | 종목코드 (6자리) |
| `fid_period_div_code` | `period` | 기간 구분 (D/W/M/Y) |
| `fid_org_adj_prc` | `adj_price` | 수정주가 여부 (0/1) |
| `fid_input_date_1` | `start_date` | 시작일 (YYYYMMDD) |
| `fid_input_date_2` | `end_date` | 종료일 (YYYYMMDD) |
| `fid_input_hour_1` | `hour` | 시간 (HHMMSS) |

### Kiwoom API 파라미터 → RPC 파라미터
| Kiwoom 원본 | RPC 파라미터 | 설명 |
|-------------|-------------|------|
| `stk_cd` | `stock_code` | 종목코드 |
| `inds_cd` | `industry_code` | 업종코드 |
| `base_dt` | `base_date` | 기준일 (YYYYMMDD) |
| `mrkt_tp` | `market_type` | 시장구분 (001:KOSPI, 101:KOSDAQ) |
| `stex_tp` | `exchange_type` | 거래소구분 (1:KRX, 2:NXT, 3:SOR) |
| `upd_stkpc_tp` | `adj_price` | 수정주가 (0/1) |
| `tic_scope` | `tic_scope` | 틱범위 |
| `cont_yn` | `cont_yn` | 연속조회 (Y/N) |
| `next_key` | `next_key` | 연속조회 키 |
| `amt_qty_tp` | `amount_qty_type` | 금액/수량 구분 |
| `strt_dt` | `start_date` | 시작일 |
| `end_dt` | `end_date` | 종료일 |

---

## 15. 주요 참조 파일 경로

### cluefin-rpc (수정 대상)
- `apps/cluefin-rpc/src/cluefin_rpc/handlers/_base.py`
- `apps/cluefin-rpc/src/cluefin_rpc/handlers/quote.py`
- `apps/cluefin-rpc/src/cluefin_rpc/server.py`
- `apps/cluefin-rpc/src/cluefin_rpc/dispatcher.py` (읽기 전용 참조)
- `apps/cluefin-rpc/src/cluefin_rpc/middleware/auth.py` (읽기 전용 참조)

### cluefin-openapi (읽기 전용 참조 — API 시그니처 확인용)
- `packages/cluefin-openapi/src/cluefin_openapi/kis/_domestic_basic_quote.py`
- `packages/cluefin-openapi/src/cluefin_openapi/kis/_domestic_basic_quote_types.py`
- `packages/cluefin-openapi/src/cluefin_openapi/kis/_domestic_issue_other.py`
- `packages/cluefin-openapi/src/cluefin_openapi/kis/_domestic_issue_other_types.py`
- `packages/cluefin-openapi/src/cluefin_openapi/kis/_domestic_stock_info.py`
- `packages/cluefin-openapi/src/cluefin_openapi/kis/_domestic_stock_info_types.py`
- `packages/cluefin-openapi/src/cluefin_openapi/kis/_domestic_market_analysis.py`
- `packages/cluefin-openapi/src/cluefin_openapi/kis/_domestic_market_analysis_types.py`
- `packages/cluefin-openapi/src/cluefin_openapi/kis/_domestic_ranking_analysis.py`
- `packages/cluefin-openapi/src/cluefin_openapi/kis/_domestic_ranking_analysis_types.py`
- `packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_chart.py`
- `packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_chart_types.py`
- `packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_etf.py`
- `packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_etf_types.py`
- `packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_foreign.py`
- `packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_foreign_types.py`
- `packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_market_condition.py`
- `packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_market_condition_types.py`
- `packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_rank_info.py`
- `packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_rank_info_types.py`
- `packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_sector.py`
- `packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_sector_types.py`
- `packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_stock_info.py`
- `packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_stock_info_types.py`
- `packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_theme.py`
- `packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_theme_types.py`
