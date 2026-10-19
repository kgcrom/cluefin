"""자주 쓰는 ECOS 통계표·항목코드 (2026-10-17 dartrail 실측 코드에서 옮김).

금리는 연 % 원문("4.182")으로 온다. 비율 변환·반올림은 쓰는 쪽에서 한다.
"""

from typing import NamedTuple


class EcosSeries(NamedTuple):
    """StatisticSearch 한 계열을 가리키는 (통계표, 주기, 항목코드1)."""

    stat_code: str
    cycle: str
    item_code: str
    name: str


# 시장금리(일별) 817Y002
KTB_1Y = EcosSeries("817Y002", "D", "010190000", "국고채(1년)")
KTB_3Y = EcosSeries("817Y002", "D", "010200000", "국고채(3년)")
KTB_5Y = EcosSeries("817Y002", "D", "010200001", "국고채(5년)")
KTB_10Y = EcosSeries("817Y002", "D", "010210000", "국고채(10년)")
KTB_20Y = EcosSeries("817Y002", "D", "010220000", "국고채(20년)")
KTB_30Y = EcosSeries("817Y002", "D", "010230000", "국고채(30년)")
MSB_91D = EcosSeries("817Y002", "D", "010400000", "통안증권(91일)")
CD_91D = EcosSeries("817Y002", "D", "010502000", "CD(91일)")
CORP_BOND_3Y_AA_MINUS = EcosSeries("817Y002", "D", "010300000", "회사채(3년, AA-)")
CORP_BOND_3Y_BBB_MINUS = EcosSeries("817Y002", "D", "010320000", "회사채(3년, BBB-)")

# 주요국 통화의 대원화환율 731Y001
USD_KRW = EcosSeries("731Y001", "D", "0000001", "원/미국달러(매매기준율)")

# 소비자물가지수(2020=100) 901Y009 — 작성: 국가데이터처
CPI_TOTAL = EcosSeries("901Y009", "M", "0", "소비자물가지수 총지수")

MARKET_RATES = (
    KTB_1Y,
    KTB_3Y,
    KTB_5Y,
    KTB_10Y,
    KTB_20Y,
    KTB_30Y,
    MSB_91D,
    CD_91D,
    CORP_BOND_3Y_AA_MINUS,
    CORP_BOND_3Y_BBB_MINUS,
)
