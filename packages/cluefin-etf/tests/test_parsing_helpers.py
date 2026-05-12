import json
from datetime import date
from decimal import Decimal

import pytest
from bs4 import BeautifulSoup

from cluefin_etf.providers._html import definition_value, json_ld_objects, meta_content
from cluefin_etf.providers._normalization import blank_to_none, parse_display_decimal, return_text
from cluefin_etf.providers._parsing import (
    compact_raw,
    normalize_space,
    parse_compact_date,
    parse_date_text,
    parse_decimal_text,
    parse_int_text,
    parse_korean_eok_amount,
)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("  1,234.50원 상승 ", Decimal("1234.50")),
        ("-12.34 하락", Decimal("-12.34")),
        ("연 0.390% (지정참가회사 0.001%)", Decimal("0.390")),
        ("-", None),
        ("평가 중", None),
    ],
)
def test_parse_decimal_text_extracts_display_numbers(value, expected):
    assert parse_decimal_text(value) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("2026.05.06 기준", date(2026, 5, 6)),
        ("2026-5-6", date(2026, 5, 6)),
        ("2026년 05월 06일", date(2026, 5, 6)),
        ("20260506", date(2026, 5, 6)),
        ("no date", None),
    ],
)
def test_parse_date_helpers_accept_provider_formats(value, expected):
    assert (parse_compact_date(value) if value == "20260506" else parse_date_text(value)) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("1조 2,345억원", Decimal("12345")),
        ("625.66억원", Decimal("625.66")),
        ("-", None),
    ],
)
def test_parse_korean_eok_amount(value, expected):
    assert parse_korean_eok_amount(value) == expected


def test_normalization_helpers_keep_only_meaningful_values():
    assert normalize_space("  KODEX\n 200  ") == "KODEX 200"
    assert blank_to_none(" - ") is None
    assert parse_display_decimal("연 0.022 상승") == Decimal("0.022")
    assert return_text("94.71 하락") == "94.71"
    assert parse_int_text("1,234.56") == 1234
    assert compact_raw({"a": 1, "b": None, "c": 0}, ("a", "b", "c")) == {"a": 1, "c": 0}


def test_json_ld_objects_collects_graph_items_and_skips_malformed_scripts():
    html = """
    <script type="application/ld+json">{bad json</script>
    <script type="application/ld+json">
    {
      "@type": "WebPage",
      "@graph": [
        {"@type": "InvestmentFund", "name": "KODEX 200"},
        "ignored"
      ]
    }
    </script>
    """

    objects = json_ld_objects(html)

    assert objects == [
        {"@type": "WebPage", "@graph": [{"@type": "InvestmentFund", "name": "KODEX 200"}, "ignored"]},
        {"@type": "InvestmentFund", "name": "KODEX 200"},
    ]


def test_definition_and_meta_helpers_extract_normalized_text():
    soup = BeautifulSoup(
        """
        <meta name="description" content="  KODEX 200\nETF  "/>
        <meta property="og:url" content=" https://example.test/detail "/>
        <dl><dt>기준가격(NAV)</dt><dd>  113,589.59 원  </dd></dl>
        <div class="each"><div class="title">벤치마크</div><div class="desc"> 코스피 200 </div></div>
        """,
        "html.parser",
    )

    assert meta_content(soup, name="description") == "KODEX 200 ETF"
    assert meta_content(soup, property_="og:url") == "https://example.test/detail"
    assert definition_value(soup, "기준가격") == "113,589.59 원"
    assert definition_value(soup, "벤치마크") == "코스피 200"


def test_json_ld_objects_ignores_empty_script():
    assert json_ld_objects(json.dumps({})) == []
