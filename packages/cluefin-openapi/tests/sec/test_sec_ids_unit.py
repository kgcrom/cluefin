import pytest

from cluefin_openapi.sec._ids import accession_dashed, accession_plain, cik10, cik_digits, path_segment


@pytest.mark.parametrize(
    "value, expected",
    [
        (320193, "0000320193"),
        ("320193", "0000320193"),
        ("0000320193", "0000320193"),
        ("CIK0000320193", "0000320193"),
        ("cik320193", "0000320193"),
        (" 320193 ", "0000320193"),
        (9999999999, "9999999999"),
    ],
)
def test_cik10(value, expected):
    assert cik10(value) == expected
    assert cik_digits(value) == expected.lstrip("0")


@pytest.mark.parametrize("value", ["", "0", "0000000000", "abc", "12345678901", "320193/../x", -5])
def test_invalid_cik_is_rejected(value):
    with pytest.raises(ValueError, match="CIK"):
        cik10(value)


@pytest.mark.parametrize("value", ["0000320193-23-000106", "000032019323000106", " 0000320193-23-000106 "])
def test_accession_forms(value):
    assert accession_dashed(value) == "0000320193-23-000106"
    assert accession_plain(value) == "000032019323000106"


@pytest.mark.parametrize("value", ["", "0000320193-23-00010", "0000320193/23/000106", "x" * 18])
def test_invalid_accession_is_rejected(value):
    with pytest.raises(ValueError, match="접수번호"):
        accession_dashed(value)


@pytest.mark.parametrize("value", ["us-gaap", "AccountsPayableCurrent", "USD-per-shares", "aapl-20230930.htm"])
def test_path_segment_accepts_plain_names(value):
    assert path_segment(value, what="x") == value


@pytest.mark.parametrize("value", ["", "..", "a/b", "../etc", ".hidden", "a..b", "a b", "a?b=1", "a#b"])
def test_path_segment_rejects_traversal_and_url_syntax(value):
    with pytest.raises(ValueError):
        path_segment(value, what="x")
