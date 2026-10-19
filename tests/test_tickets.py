from changepilot.comparison import compare_versions
from changepilot.parsing import parse_requirements
from changepilot.tickets import draft_change_ticket
from changepilot.traceability import load_traceability


def test_ticket_cites_verified_links_only():
    old = parse_requirements("REQ-001 | Require two days for reporting.", "V1")
    new = parse_requirements("REQ-001 | Require one day for reporting.", "V2")
    links = load_traceability("requirement_id,system,owner,user_story,test_case\nREQ-001,Reporting,Data Ops,US-1,TC-1")
    ticket = draft_change_ticket(compare_versions(old,new)[0], links)
    assert "Reporting" in ticket and "TC-1" in ticket and "[DRAFT]" in ticket


def test_ticket_missing_links_explicit():
    new = parse_requirements("REQ-002 | Users must verify their identity.", "V2")
    ticket = draft_change_ticket(compare_versions([],new)[0], [])
    assert "Unmapped" in ticket
    assert "None mapped" in ticket
