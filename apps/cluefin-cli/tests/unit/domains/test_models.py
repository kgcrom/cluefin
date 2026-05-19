import json

from cluefin_cli.domains.models import (
    FinancialMetric,
    OhlcvPoint,
    OhlcvSeries,
    StatementSnapshot,
)
from cluefin_cli.output import dump_json


def test_domain_dtos_are_json_serializable() -> None:
    snapshot = StatementSnapshot(
        stock_code="005930",
        source="dart",
        corp_code="00126380",
        accounts=[FinancialMetric(name="Revenue", label="매출액", value="1000", unit="KRW")],
    )
    series = OhlcvSeries(
        stock_code="005930",
        source="kiwoom",
        interval="daily",
        points=[OhlcvPoint(timestamp="20260519", open=70000, high=71000, low=69000, close=70500, volume=12345)],
    )

    payload = json.loads(dump_json({"statement": snapshot, "series": series}))

    assert payload["statement"]["accounts"][0]["name"] == "Revenue"
    assert payload["series"]["points"][0]["close"] == 70500
