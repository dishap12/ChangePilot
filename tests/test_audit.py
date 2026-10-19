import pytest
from changepilot.audit import add_decision, list_decisions


def test_audit_round_trip(tmp_path):
    path = tmp_path / "audit.db"
    add_decision(path, "REQ-007", "Request clarification", "Demo Analyst", "Retention owner to confirm.")
    decisions = list_decisions(path)
    assert len(decisions) == 1
    assert decisions[0]["requirement_id"] == "REQ-007"
    assert decisions[0]["note"] == "Retention owner to confirm."


def test_blank_reviewer_rejected(tmp_path):
    with pytest.raises(ValueError, match="Reviewer name"):
        add_decision(tmp_path / "x.db", "REQ-001", "Request clarification", "", "test")


def test_review_is_scoped_to_document_workspace(tmp_path):
    path = tmp_path / "audit.db"
    add_decision(path, "REQ-005", "Approve for implementation", "Reviewer", "Approved for test", "project-A")
    assert len(list_decisions(path, "project-A")) == 1
    assert list_decisions(path, "project-B") == []
