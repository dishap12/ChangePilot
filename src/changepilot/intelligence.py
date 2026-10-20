"""Transparent analyst suggestions, never silently approved or inferred facts."""
from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .models import Change


@dataclass(frozen=True)
class RenameCandidate:
    removed_id: str
    added_id: str
    score: float
    old_text: str
    new_text: str


def propose_renamed_links(changes: list[Change], min_score: float = 0.24) -> list[RenameCandidate]:
    """Find *possible* ID renames among removed and added requirements.

    Uses character TF-IDF and edit similarity; never changes the source inventory
    or calls a suggestion a verified relation.
    """
    removed = [x for x in changes if x.status == "Removed" and x.old_text.strip()]
    added = [x for x in changes if x.status == "Added" and x.new_text.strip()]
    if not removed or not added:
        return []
    texts = [x.old_text for x in removed] + [x.new_text for x in added]
    try:
        matrix = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5),
                                 lowercase=True, sublinear_tf=True).fit_transform(texts)
        cosine = cosine_similarity(matrix[:len(removed)], matrix[len(removed):])
    except ValueError:
        return []
    ranked = []
    for i, before in enumerate(removed):
        for j, after in enumerate(added):
            fuzzy = SequenceMatcher(None, before.old_text.lower(), after.new_text.lower()).ratio()
            score = round(0.7 * float(cosine[i, j]) + 0.3 * fuzzy, 3)
            if score >= min_score:
                ranked.append(RenameCandidate(before.id, after.id, score, before.old_text, after.new_text))
    ranked.sort(key=lambda x: (-x.score, x.removed_id, x.added_id))
    selected, used_old, used_new = [], set(), set()
    for item in ranked:
        if item.removed_id not in used_old and item.added_id not in used_new:
            selected.append(item)
            used_old.add(item.removed_id)
            used_new.add(item.added_id)
    return selected


RULE_WORDS = re.compile(r"\b(shall|must|should|needs? to|required to|will)\b", re.I)
BULLET = re.compile(r"^\s*(?:[-*•]\s+|\d{1,3}[.)]\s+)")
EXPLICIT_ID = re.compile(r"^\s*REQ-\d{3,5}\s*\|\s*", re.I)


def extract_draft_requirements(text: str, limit: int = 40) -> list[dict]:
    """Suggest candidate statements from a freeform brief, with line provenance.

    This intentionally conservative line-based heuristic cannot replace BA review.
    Draft IDs MUST be manually reconciled with real requirements before use.
    """
    results = []
    for lineno, raw in enumerate(text.splitlines(), 1):
        clean = BULLET.sub("", raw).strip()
        clean = EXPLICIT_ID.sub("", clean)
        if not 20 <= len(clean) <= 500 or not RULE_WORDS.search(clean):
            continue
        if clean.startswith(("#", ">")):
            clean = clean.lstrip("#> ").strip()
        if not clean:
            continue
        results.append({"Draft ID": f"DRAFT-{len(results)+1:03d}",
                        "Candidate requirement": clean,
                        "Source line": lineno,
                        "Review status": "Unverified — edit and assign stable ID"})
        if len(results) >= limit:
            break
    return results


def draft_story_and_criteria(change: Change) -> str:
    """Source-grounded *draft* handoff, not approved acceptance criteria."""
    current = change.new_text if change.new_text else change.old_text
    if not current:
        return "No requirement text available for a draft."
    status_note = "retirement / replacement review" if change.status == "Removed" else "updated behaviour"
    lines = [
        f"## DRAFT — {change.id}: {status_note}",
        "",
        "**Proposed user story (requires stakeholder confirmation)**",
        "",
        f"As a business process owner, I want the product team to implement and validate the documented {change.id} behaviour so that onboarding follows the approved requirement.",
        "",
        f"**Source [{change.id}]**: {current}",
        "",
        "**Proposed acceptance-test discussion (NOT validated assertions)**",
        "",
        f"1. **Happy path:** Given the required inputs and permissions, when {change.id} is exercised, then confirm the result meets the exact current wording above.",
        "2. **Negative case:** Given invalid or missing inputs, verify the team's agreed rejection/handling behaviour; do not assume a result not stated in the source.",
        "3. **Audit / integration:** Check relevant linked systems and logging only where the approved specification requires them.",
    ]
    old_numbers = re.findall(r"\b\d+(?:\.\d+)?\b", change.old_text)
    new_numbers = re.findall(r"\b\d+(?:\.\d+)?\b", change.new_text)
    if old_numbers and new_numbers and old_numbers != new_numbers:
        lines.append(
            f"4. **Changed values:** Previous text includes {', '.join(old_numbers)}; "
            f"current text includes {', '.join(new_numbers)}. Request specific below/at/above boundary "
            "expected outcomes before writing executable tests."
        )
    lines.extend(["", "**Approval gates:** Business owner clarifies ambiguous wording; QA defines expected outcomes; Engineering confirms impact.", "",
                  "*Draft is derived from source text only and has not been approved.*"])
    return "\n".join(lines)
