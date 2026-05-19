from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel

from cluefin_cli.output import dump_json, error_envelope, success_envelope, to_jsonable


@dataclass(slots=True)
class ExampleData:
    amount: Decimal
    as_of: date


class ExampleModel(BaseModel):
    created_at: datetime


def test_to_jsonable_handles_project_value_types() -> None:
    payload = {
        "data": ExampleData(amount=Decimal("123.45"), as_of=date(2026, 5, 19)),
        "model": ExampleModel(created_at=datetime(2026, 5, 19, 12, 30)),
        "items": {3, 1, 2},
    }

    assert to_jsonable(payload) == {
        "data": {"amount": "123.45", "as_of": "2026-05-19"},
        "model": {"created_at": "2026-05-19T12:30:00"},
        "items": [1, 2, 3],
    }


def test_envelopes_are_json_serializable() -> None:
    success = success_envelope(command="chart", source="kiwoom", params={"stock_code": "005930"}, data={})
    failure = error_envelope(command="chart", error_type="ValidationError", message="invalid stock code")

    assert '"ok": true' in dump_json(success)
    assert '"ok": false' in dump_json(failure)
