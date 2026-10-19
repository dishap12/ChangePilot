"""Deterministic, auditable draft change ticket for analyst review."""
from .models import Change, TraceLink
from .traceability import triage_change


def draft_change_ticket(change: Change, links: list[TraceLink]) -> str:
    impact = triage_change(change, links)
    owners = sorted({x.owner for x in impact["links"] if x.owner})
    systems = sorted({x.system for x in impact["links"] if x.system})
    tests = sorted({x.test_case for x in impact["links"] if x.test_case})
    stories = sorted({x.user_story for x in impact["links"] if x.user_story})
    lines = [
        f"# [DRAFT] {change.id}: {change.status} onboarding requirement",
        "", "**Status:** Proposed / not approved", f"**Review priority (heuristic):** {impact['priority']}",
        f"**Mapped owner(s):** {', '.join(owners) if owners else 'Unassigned — investigate'}",
        f"**Mapped system(s):** {', '.join(systems) if systems else 'Unmapped — investigate'}",
        f"**Existing user story reference(s):** {', '.join(stories) if stories else 'None mapped'}",
        "", "## Change description", "",
        f"- Previous: {change.old_text or 'Not present in baseline'}",
        f"- Current: {change.new_text or 'Not present in revised version'}",
        "", "## Suggested acceptance-review checklist (draft, not executable tests)", "",
        "- [ ] Confirm business owner accepts the wording and scope of the revised requirement.",
        "- [ ] Define positive, negative, and boundary-case tests appropriate to the change.",
        "- [ ] Validate system integration and downstream reporting impact.",
        "- [ ] Confirm updated behaviour with stakeholders before sign-off.",
        "", "## Existing test references requiring review", "",
    ]
    lines.extend([f"- {test}" for test in tests] if tests else ["- None mapped — create appropriate test case IDs."])
    lines.extend(["", "## Analyst questions", ""])
    lines.extend(f"- {q}" for q in impact["questions"])
    lines.extend(["", "## Evidence and cautions", "",
                  f"- Source requirement: `{change.id}`, compared across the baseline and revised input.",
                  "- System, owner, story and test references are only from the uploaded traceability CSV.",
                  "- This template is not an approved user story, functional specification, or compliance assessment.", ""])
    return "\n".join(lines)
