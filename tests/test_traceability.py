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


def test_triage_distinguishes_routine_mapped_changes_from_control_flags():
    from changepilot.models import Change, TraceLink

    link = TraceLink("REQ-002", "Notification Service", "Communications", "US-002", "TC-002")
    routine = Change("REQ-002", "Modified",
                     "A verification email shall arrive within 24 hours.",
                     "A verification email shall arrive within 10 minutes.", 0.7)
    assert triage_change(routine, [link])["priority"] == "Medium"

    risk_link = TraceLink("REQ-005", "Risk Decision Engine", "Risk Ops", "US-005", "TC-005")
    risk = Change("REQ-005", "Modified",
                  "Manual review when risk score reaches 80.",
                  "Manual review when risk score reaches 65.", 0.7)
    assert triage_change(risk, [risk_link])["priority"] == "High"

    unmapped = Change("REQ-012", "Added", "", "New optional customer onboarding step", 0)
    result = triage_change(unmapped, [])
    assert result["priority"] == "High"
    assert result["gap"] is True


def test_demo_review_flag_count_is_useful():
    old = parse_requirements((ROOT / "data" / "onboarding_v1.md").read_text(), "V1")
    new = parse_requirements((ROOT / "data" / "onboarding_v2.md").read_text(), "V2")
    links = load_traceability((ROOT / "data" / "traceability.csv").read_text())
    changed = changed_only(compare_versions(old, new))
    high = sum(triage_change(change, links)["priority"] == "High" for change in changed)
    assert high == 5
