"""Verified CSV links; never imply unknown links are confirmed dependencies."""
import csv
import io
import re
from .models import Change, TraceLink

FIELDS = {"requirement_id", "system", "owner", "user_story", "test_case"}
SENSITIVE_TERMS = {"identity", "risk", "consent", "audit", "retention", "fraud", "security", "verification", "accessibility"}


def load_traceability(csv_text: str) -> list[TraceLink]:
    reader = csv.DictReader(io.StringIO(csv_text))
    if not reader.fieldnames or not FIELDS.issubset(reader.fieldnames):
        raise ValueError(f"Traceability CSV needs columns: {', '.join(sorted(FIELDS))}")
    items = []
    for i, row in enumerate(reader, start=2):
        req_id = (row.get("requirement_id") or "").strip().upper()
        if not re.fullmatch(r"REQ-\d{3,5}", req_id):
            raise ValueError(f"Invalid requirement ID at CSV line {i}: {req_id!r}")
        items.append(TraceLink(req_id, (row.get("system") or "").strip(),
                               (row.get("owner") or "").strip(),
                               (row.get("user_story") or "").strip(),
                               (row.get("test_case") or "").strip(),
                               (row.get("link_type") or "verified").strip()))
    return items


def linked_items(requirement_id: str, links: list[TraceLink]) -> list[TraceLink]:
    return [x for x in links if x.requirement_id == requirement_id]


def triage_change(change: Change, links: list[TraceLink]) -> dict:
    """Rule-based review priority, NOT a predictive risk model."""
    linked = linked_items(change.id, links)
    words = set(re.findall(r"[a-z]+", f"{change.old_text} {change.new_text}".lower()))
    sensitive = sorted(SENSITIVE_TERMS & words)
    missing = not linked
    priority = "High" if (sensitive or missing) else "Medium"
    if change.status == "Removed":
        questions = ["Does the retired requirement have a replacement?", "Which tests and controls should be retired or rewritten?"]
    elif change.status == "Added":
        questions = ["Which system and owner should implement this?", "Which acceptance criteria and tests must be created?"]
    else:
        questions = ["What behaviour changes for the end user?", "Which existing acceptance criteria and tests should be updated?"]
    if missing:
        questions.append("Traceability gap: assign a system, owner, user story, and test case.")
    return {
        "priority": priority,
        "reason": ("Sensitive domain terms: " + ", ".join(sensitive) + ". " if sensitive else "") +
                  ("No verified traceability links." if missing else f"{len(linked)} verified link(s) to review."),
        "links": linked,
        "questions": questions,
        "gap": missing,
    }
