"""Unit tests for interpretable intelligence additions and graph provenance."""
from changepilot.comparison import compare_versions
from changepilot.intelligence import (
    draft_story_and_criteria, extract_draft_requirements, propose_renamed_links,
)
from changepilot.models import Change, Requirement, TraceLink
from changepilot.visuals import change_donut, dependency_sankey


def test_extraction_has_source_lines_and_unverified_ids():
    text = ("Executive context\n"
            "The platform must record new consent agreements.\n"
            "This is a generic comment.\n"
            "- Customers should receive an acknowledgment message.\n")
    result = extract_draft_requirements(text)
    assert len(result) == 2
    assert [r["Source line"] for r in result] == [2, 4]
    assert result[0]["Draft ID"] == "DRAFT-001"
    assert all("Unverified" in r["Review status"] for r in result)


def test_no_extraction_from_generic_prose():
    assert extract_draft_requirements("We discussed some ideas yesterday.") == []


def test_rename_candidates_do_not_change_inventory():
    changes = compare_versions(
        [Requirement("REQ-002", "The system must verify applicant identity.", "V1")],
        [Requirement("REQ-099", "The system must verify the applicant identity.", "V2")],
    )
    proposed = propose_renamed_links(changes)
    assert len(proposed) == 1
    assert (proposed[0].removed_id, proposed[0].added_id) == ("REQ-002", "REQ-099")
    assert [x.status for x in changes] == ["Removed", "Added"]


def test_no_rename_suggestion_for_unrelated_requirements():
    changes = [
        Change("REQ-001", "Removed", "Validate user postal address", "", 0),
        Change("REQ-002", "Added", "", "Operate a banking branch kiosk", 0),
    ]
    assert propose_renamed_links(changes, min_score=0.99) == []


def test_story_draft_contains_source_and_flags_changed_numbers():
    change = Change("REQ-005", "Modified", "Manual review above 80.", "Manual review above 65.", .8)
    draft = draft_story_and_criteria(change)
    assert "REQ-005" in draft and "80" in draft and "65" in draft
    assert "NOT validated assertions" in draft
    assert "stakeholder confirmation" in draft


def test_sankey_displays_only_verified_input_links():
    change = Change("REQ-004", "Modified", "", "New consent version must be stored", 0)
    link = TraceLink("REQ-004", "Consent Service", "Privacy Ops", "US-004", "TC-004")
    figure = dependency_sankey(change, [link])
    assert figure is not None
    labels = set(figure.data[0]["node"]["label"])
    assert "REQ-004" in labels
    assert "Consent Service" in labels
    assert "Owner: Privacy Ops" in labels
    assert "Test: TC-004" in labels
    assert dependency_sankey(change, []) is None


def test_chart_handles_no_changes():
    fig = change_donut([])
    assert fig is not None
