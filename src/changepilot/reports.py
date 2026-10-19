"""Evidence-based report generation; avoids fabricated AI outcomes."""
import csv
import io
from collections import Counter
from .comparison import changed_only
from .models import Change, TraceLink
from .traceability import triage_change


def summary_counts(changes: list[Change]) -> dict[str, int]:
    counts = Counter(x.status for x in changes)
    return {k: counts.get(k, 0) for k in ("Added", "Modified", "Removed", "Unchanged")}


def report_markdown(changes: list[Change], links: list[TraceLink]) -> str:
    counts = summary_counts(changes)
    lines = ["# ChangePilot — Requirements Change Impact Report", "",
             "**Dataset:** Sample fictional retail banking onboarding requirements, unless replaced by the user.",
             "**Method:** Explicit requirement-ID comparison; verified CSV traceability links; rule-based review priority.",
             "**Review status:** Draft, human validation required.", "",
             "## Overview", "",
             " | Status | Count |", " |---|---:|", *[f" | {k} | {v} |" for k, v in counts.items()], "",
             "## Changes and impact questions", ""]
    for change in changed_only(changes):
        item = triage_change(change, links)
        lines.extend([f"### {change.id} — {change.status} — {item['priority']} review priority", "",
                      f"**Prior:** {change.old_text or 'Not present'}", "",
                      f"**Current:** {change.new_text or 'Not present'}", "",
                      f"**Triage rationale:** {item['reason']}", "",
                      "**Verified traceability:** " + ("; ".join(
                          f"{x.system} / {x.user_story} / {x.test_case} / {x.owner}"
                          for x in item["links"]) if item["links"] else "None — assign owner and links."), "",
                      "**Questions for human review:**", *[f"- {q}" for q in item["questions"]], ""])
    lines.extend(["## Limitations", "",
                  "- IDs must remain stable across versions; ID renames are treated as a removal plus addition.",
                  "- CSV links are source-of-truth only for this demonstration and may be outdated.",
                  "- Priority is a transparent rule-based review flag, not an AI risk prediction.",
                  "- No legal or compliance determination is made by this tool.", ""])
    return "\n".join(lines)


def change_csv(changes: list[Change], links: list[TraceLink]) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["requirement_id", "status", "old_text", "new_text", "similarity", "review_priority",
                     "linked_systems", "linked_tests", "traceability_gap"])
    for change in changes:
        t = triage_change(change, links)
        writer.writerow([change.id, change.status, change.old_text, change.new_text, change.similarity,
                         t["priority"] if change.status != "Unchanged" else "Not applicable",
                         "; ".join(x.system for x in t["links"]),
                         "; ".join(x.test_case for x in t["links"]),t["gap"]])
    return output.getvalue()
