from cluefin_sec_notes import extract_items, parse_filing
from cluefin_sec_notes._expectations import FAILED, FIXED, KNOWN_BAD, OK, check_expectations


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


def test_char_tolerance(synthetic):
    extraction = extract_items(parse_filing(synthetic.filing()))
    length = len(extraction.item("1A").text)
    near = {"items": {"1A": {"chars": int(length * 1.05)}}}
    far = {"items": {"1A": {"chars": length * 2}}}
    assert check_expectations(extraction, near)[0].status == OK
    assert check_expectations(extraction, far)[0].detail == f"길이 {length} (기대 {length * 2})"
