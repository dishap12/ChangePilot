from pathlib import Path
import pytest
from changepilot.comparison import compare_versions, changed_only
from changepilot.parsing import parse_requirements
from changepilot.traceability import load_traceability, triage_change

ROOT = Path(__file__).resolve().parents[1]


def test_trace_links_load():
    links = load_traceability((ROOT / "data" / "traceability.csv").read_text())
    assert len(links) >= 10
    assert len([l for l in links if l.requirement_id == "REQ-003"]) == 2


def test_missing_columns_error():
    with pytest.raises(ValueError, match="needs columns"):
        load_traceability("requirement_id,name\nREQ-001,hi")


def test_new_requirement_has_traceability_gap():
    old = parse_requirements((ROOT / "data" / "onboarding_v1.md").read_text(), "V1")
    new = parse_requirements((ROOT / "data" / "onboarding_v2.md").read_text(), "V2")
    links = load_traceability((ROOT / "data" / "traceability.csv").read_text())
    added = next(x for x in changed_only(compare_versions(old,new)) if x.id == "REQ-012")
    triage = triage_change(added, links)
    assert triage["gap"] is True
    assert triage["priority"] == "High"
