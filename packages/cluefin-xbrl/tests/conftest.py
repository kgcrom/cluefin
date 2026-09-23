"""Shared test fixtures for cluefin-xbrl tests."""

from decimal import Decimal, InvalidOperation
from pathlib import Path

import pytest

from cluefin_xbrl._types import PeriodType, XbrlFact, XbrlPeriod

FIXTURES_DIR = Path(__file__).parent / "fixtures"

# DART instance documents qualify facts with this axis to distinguish consolidated (연결)
# from separate (별도) figures; see statements.py / notes.py for the matching logic.
CONSOLIDATED_AXIS = "ifrs-full:ConsolidatedAndSeparateFinancialStatementsAxis"

# Observed DART role-code convention: a linkrole containing role-D210000 is the
# consolidated statement of financial position, role-D210005 its separate counterpart.
DART_ROLE_BS_CONSOLIDATED = "http://dart.fss.or.kr/role/ifrs/dart_2024-06-30_role-D210000"
DART_ROLE_BS_SEPARATE = "http://dart.fss.or.kr/role/ifrs/dart_2024-06-30_role-D210005"


@pytest.fixture
def fixtures_dir():
    return FIXTURES_DIR


@pytest.fixture
def sample_xbrl_path():
    return FIXTURES_DIR / "sample.xbrl"


@pytest.fixture
def sample_xbrl_dir():
    return FIXTURES_DIR


@pytest.fixture
def consolidated_axis():
    return CONSOLIDATED_AXIS


@pytest.fixture
def dart_role_bs_consolidated():
    return DART_ROLE_BS_CONSOLIDATED


@pytest.fixture
def dart_role_bs_separate():
    return DART_ROLE_BS_SEPARATE


def _make_xbrl_fact(
    concept_local_name: str = "Assets",
    concept_qname: str = "ifrs-full:Assets",
    value: str = "1000",
    dimensions: dict[str, str] | None = None,
    **overrides,
) -> XbrlFact:
    """Build a minimal numeric XbrlFact for statement/note extraction tests.

    Covers the boilerplate shared by ``_make_assets_fact`` (test_statements.py) and
    ``_make_obligation_fact`` (test_notes.py): a numeric fact with an instant period,
    on the standard IFRS namespace, that callers can override via ``**overrides``.
    """
    if "numeric_value" not in overrides:
        try:
            overrides["numeric_value"] = Decimal(value) if value is not None else None
        except InvalidOperation:
            overrides["numeric_value"] = None

    fields = {
        "concept_local_name": concept_local_name,
        "concept_qname": concept_qname,
        "namespace": "http://xbrl.ifrs.org/taxonomy/2021-03-24/ifrs-full",
        "value": value,
        "period": XbrlPeriod(period_type=PeriodType.INSTANT),
        "dimensions": dimensions or {},
    }
    fields.update(overrides)
    return XbrlFact(**fields)


@pytest.fixture
def make_xbrl_fact():
    return _make_xbrl_fact
