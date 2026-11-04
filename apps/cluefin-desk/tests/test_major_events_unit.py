"""`data/major_events.py` 의 순수 수집 로직 — 가짜 DART 클라이언트로 정규화·정렬·
실패 격리를 본다. 실제 네트워크·화면 조립은 test_financial_analysis_screen_unit.py 가 본다.
"""

from datetime import date
from types import SimpleNamespace

from cluefin_desk.data.major_events import MAJOR_EVENT_TYPES, collect_major_events


def _response(items, status="000"):
    return SimpleNamespace(result=SimpleNamespace(status=status, list=items))


class FakeMajorMattersReport:
    """`major_matters_report` 자리에 끼워 넣는다 — 메서드마다 호출 기록·응답을 쥔다."""

    def __init__(self, responses=None, raising=None):
        self._responses = responses or {}
        self._raising = raising or {}
        self.calls: list[tuple[str, dict]] = []

    def __getattr__(self, name):
        def _method(**kwargs):
            self.calls.append((name, kwargs))
            if name in self._raising:
                raise self._raising[name]
            return self._responses.get(name, _response(None, status="013"))

        return _method


class FakeDartClient:
    def __init__(self, responses=None, raising=None):
        self.major_matters_report = FakeMajorMattersReport(responses, raising)


def _item(**kwargs):
    return SimpleNamespace(**kwargs)


class TestCollectMajorEvents:
    def test_every_event_type_is_called_with_a_365_day_window(self):
        client = FakeDartClient()
        collect_major_events(client, "00126380", end=date(2026, 11, 4))

        assert len(client.major_matters_report.calls) == len(MAJOR_EVENT_TYPES)
        for _, kwargs in client.major_matters_report.calls:
            assert kwargs["corp_code"] == "00126380"
            assert kwargs["bgn_de"] == "20251104"
            assert kwargs["end_de"] == "20261104"

    def test_window_floors_at_dart_2015_start(self):
        client = FakeDartClient()
        collect_major_events(client, "00126380", end=date(2015, 3, 1))

        _, kwargs = client.major_matters_report.calls[0]
        assert kwargs["bgn_de"] == "20150101"

    def test_status_013_is_skipped_silently(self):
        client = FakeDartClient(responses={"convertible_bond_issuance_decision": _response(None, status="013")})
        rows, errors = collect_major_events(client, "00126380", end=date(2026, 11, 4))

        assert rows == []
        assert errors == {}

    def test_rows_are_normalized_and_sorted_newest_first(self):
        client = FakeDartClient(
            responses={
                "convertible_bond_issuance_decision": _response(
                    [_item(rcept_no="20260101000111", bd_fta="10,000,000,000")]
                ),
                "default_occurrence": _response(
                    [_item(rcept_no="20260615000222", df_amt="5,000,000,000", df_bnk="국민은행")]
                ),
            }
        )
        rows, errors = collect_major_events(client, "00126380", end=date(2026, 11, 4))

        assert errors == {}
        assert [row.rcept_dt for row in rows] == ["20260615", "20260101"]

        default_row, bond_row = rows
        assert default_row.kind == "부도발생"
        assert default_row.summary == "부도금액 5,000,000,000원 (국민은행)"
        assert default_row.link == "https://dart.fss.or.kr/dsaf001/main.do?rcpNo=20260615000222"

        assert bond_row.kind == "전환사채권 발행결정"
        assert bond_row.summary == "권면(전자등록)총액 10,000,000,000원"
        assert bond_row.rcept_no == "20260101000111"

    def test_one_failing_event_type_does_not_block_the_others(self):
        client = FakeDartClient(
            responses={"default_occurrence": _response([_item(rcept_no="20260615000222", df_amt="1", df_bnk="-")])},
            raising={"business_suspension": RuntimeError("요청 제한을 초과하였습니다")},
        )
        rows, errors = collect_major_events(client, "00126380", end=date(2026, 11, 4))

        assert len(rows) == 1
        assert rows[0].kind == "부도발생"
        assert errors == {"business-suspension": "요청 제한을 초과하였습니다"}

    def test_every_slug_calls_a_distinct_client_method(self):
        """slug 가 어긋나면 잘못된 종류를 부른다 — 15개 슬롯이 서로 다른 메서드명을
        부르는지로 그 어긋남을 잡는다(CLI `_MAJOR_EVENTS` 표와의 대조는 수동 점검)."""
        client = FakeDartClient()
        collect_major_events(client, "00126380", end=date(2026, 11, 4))

        called_methods = [name for name, _ in client.major_matters_report.calls]
        assert len(called_methods) == len(set(called_methods)) == len(MAJOR_EVENT_TYPES)
