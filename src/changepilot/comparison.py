"""Explicit ID-based version comparison. No unsupported AI matching claims."""
from difflib import SequenceMatcher
from .models import Requirement, Change


def normalize(text: str) -> str:
    return " ".join(text.lower().split())


def compare_versions(old: list[Requirement], new: list[Requirement]) -> list[Change]:
    old_by_id = {x.id: x for x in old}
    new_by_id = {x.id: x for x in new}
    changes: list[Change] = []
    for req_id in sorted(set(old_by_id) | set(new_by_id)):
        before = old_by_id.get(req_id)
        after = new_by_id.get(req_id)
        if before is None:
            status, score = "Added", 0.0
        elif after is None:
            status, score = "Removed", 0.0
        else:
            score = SequenceMatcher(None, normalize(before.text), normalize(after.text)).ratio()
            status = "Unchanged" if normalize(before.text) == normalize(after.text) else "Modified"
        changes.append(Change(req_id, status, before.text if before else "", after.text if after else "", round(score, 3)))
    return changes


def changed_only(changes: list[Change]) -> list[Change]:
    return [x for x in changes if x.status != "Unchanged"]
