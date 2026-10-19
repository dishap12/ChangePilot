from changepilot.parsing import parse_requirements
from changepilot.retrieval import search_requirements, offline_response


def test_query_finds_right_requirement():
    requirements = parse_requirements("REQ-001 | Audit event retention is 365 days.\nREQ-002 | Email notifications are sent to applicants.", "V2")
    result = search_requirements("How long are audit events retained?", requirements)
    assert result
    assert result[0].requirement.id == "REQ-001"


def test_unrelated_returns_no_answer():
    requirements = parse_requirements("REQ-001 | Audit logs are stored.", "V2")
    hits = search_requirements("spacecraft propulsion", requirements)
    assert hits == []
    assert "No sufficiently similar" in offline_response(hits)
