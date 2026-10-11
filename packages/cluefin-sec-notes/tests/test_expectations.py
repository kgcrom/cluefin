from cluefin_sec_notes import extract_items, parse_filing
from cluefin_sec_notes._expectations import (
    FAILED,
    FIXED,
    KNOWN_BAD,
    OK,
    accept_items,
    check_expectations,
    expectation_key,
    invariant_violations,
    sec_item_violations,
)


def test_statuses(synthetic):
    extraction = extract_items(parse_filing(synthetic.filing()))
    length = len(extraction.item("1A").text)
    entry = {
        "items": {
            "1A": {"starts_with": "Item 1A. Risk Factors", "chars": length},
            "7": {"starts_with": "Item 8."},
            "8": {"min_chars": 10_000},
        },
        "present": ["2", "99"],
        "known_bad": {"8": "too short", "3": "should be wrong but is fine"},
    }
    statuses = {check.key: check.status for check in check_expectations(extraction, entry)}
    assert statuses == {"1A": OK, "7": FAILED, "8": KNOWN_BAD, "2": OK, "99": FAILED, "3": FIXED}


def test_known_bad_records_whether_the_item_is_warned(synthetic):
    content = (
        synthetic.body()
        .replace(f'<div id="{synthetic.anchor_id("7A")}"></div>', "")
        .replace(
            '<div style="font-weight:700">Item 7A. Quantitative and Qualitative Disclosures About Market Risk</div>', ""
        )
    )
    extraction = extract_items(parse_filing(synthetic.filing(content=content)))
    entry = {"items": {"8": {"min_chars": 10_000}}, "known_bad": {"7A": "missing", "8": "too short"}}
    warned = {check.key: check.warned for check in check_expectations(extraction, entry)}
    assert warned == {"7A": True, "8": False}


def test_char_tolerance(synthetic):
    extraction = extract_items(parse_filing(synthetic.filing()))
    length = len(extraction.item("1A").text)
    near = {"items": {"1A": {"chars": int(length * 1.05)}}}
    far = {"items": {"1A": {"chars": length * 2}}}
    assert check_expectations(extraction, near)[0].status == OK
    assert check_expectations(extraction, far)[0].detail == f"길이 {length} (기대 {length * 2})"


def test_accept_items_turns_fixed_known_bad_into_expectations(synthetic):
    extraction = extract_items(parse_filing(synthetic.filing()))
    entry = {
        "items": {"1A": {"min_chars": 10_000, "excludes": "Item 2."}},
        "present": ["2", "3"],
        "known_bad": {"1A": "was too short", "2": "was missing"},
    }
    assert accept_items(extraction, entry, ["1A", "2", "99"]) == ["99"]
    risk = extraction.item("1A")
    assert entry["items"]["1A"] == {"starts_with": risk.heading[:60], "chars": len(risk.text), "excludes": "Item 2."}
    assert entry["items"]["2"]["chars"] == len(extraction.item("2").text)
    assert entry["present"] == ["3"]
    assert "known_bad" not in entry
    assert {check.status for check in check_expectations(extraction, entry)} == {OK}


def test_sec_item_violations_compare_with_the_filing_index():
    assert sec_item_violations(["2.02", "9.01"], ["2.02", "9.01"]) == []
    assert sec_item_violations(["2.02", "7.01"], ["2.02", " 9.01"]) == ["extra:7.01", "missing:9.01"]


def test_expectation_key_and_ten_k_invariants(synthetic):
    extraction = extract_items(parse_filing(synthetic.filing()))
    risk = extraction.item("1A")
    assert expectation_key(risk, part_scoped=False) == "1A"
    assert expectation_key(risk, part_scoped=True) == "I:1A"
    # 합성 공시의 1A는 짧다. sec_items는 8-K에서만 본다.
    assert invariant_violations(extraction, sec_items=["1.01"]) == ["short:1A"]


def test_table_row_expectation(synthetic):
    table = (
        "<table><tr><td></td><td colspan='2'>2025</td></tr>"
        "<tr><td>Revenue</td><td>$</td><td>1,234</td></tr><tr><td>Costs</td><td></td><td>(56</td><td>)</td></tr></table>"
    )
    content = synthetic.body().replace("<div>Body of item 8.</div>", "<div>Body of item 8.</div>" + table)
    extraction = extract_items(parse_filing(synthetic.filing(content=content)))
    good = {"tables": [{"item": "8", "row": ["Revenue", "$1,234"]}]}
    bad = {"tables": [{"item": "8", "row": ["Revenue", "$9"]}]}
    assert [check.status for check in check_expectations(extraction, good)] == [OK]
    assert (
        check_expectations(extraction, bad)[0].detail
        == "행이 없다: ('Revenue', '$9') (같은 라벨 행: ('Revenue', '$1,234'))"
    )
