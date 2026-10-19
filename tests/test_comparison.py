from changepilot.comparison import compare_versions, changed_only
from changepilot.parsing import parse_requirements


def test_change_types():
    old = parse_requirements("REQ-001 | Same.\nREQ-002 | Old text.\nREQ-003 | Retired.", "V1")
    new = parse_requirements("REQ-001 | Same.\nREQ-002 | New text.\nREQ-004 | New.", "V2")
    found = {c.id: c.status for c in compare_versions(old, new)}
    assert found == {"REQ-001": "Unchanged", "REQ-002": "Modified", "REQ-003": "Removed", "REQ-004": "Added"}


def test_whitespace_does_not_create_false_modification():
    old = parse_requirements("REQ-001 | Email   is required.", "V1")
    new = parse_requirements("REQ-001 | email is required.", "V2")
    assert compare_versions(old, new)[0].status == "Unchanged"


def test_changed_only():
    old = parse_requirements("REQ-001 | Same.\nREQ-002 | Old.", "V1")
    new = parse_requirements("REQ-001 | Same.\nREQ-002 | New.", "V2")
    assert [x.id for x in changed_only(compare_versions(old, new))] == ["REQ-002"]
