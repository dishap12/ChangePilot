"""Small transparent demo benchmark; not an enterprise validation claim."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from changepilot.parsing import parse_requirements
from changepilot.comparison import compare_versions
from changepilot.retrieval import search_requirements

ROOT = Path(__file__).resolve().parents[1]
old = parse_requirements((ROOT / "data/onboarding_v1.md").read_text(), "V1")
new = parse_requirements((ROOT / "data/onboarding_v2.md").read_text(), "V2")
changes = compare_versions(old,new)
# Hand-labeled expected change categories for the synthetic sample.
GOLD = {
    "REQ-001": "Unchanged", "REQ-002": "Modified", "REQ-003": "Modified",
    "REQ-004": "Modified", "REQ-005": "Modified", "REQ-006": "Unchanged",
    "REQ-007": "Modified", "REQ-008": "Unchanged", "REQ-009": "Removed",
    "REQ-010": "Unchanged", "REQ-011": "Added", "REQ-012": "Added",
}
correct = sum(GOLD[item.id] == item.status for item in changes)
print(f"Change-type agreement: {correct}/{len(GOLD)} ({correct/len(GOLD):.0%}) on the hand-built synthetic sample")

# Query-to-requirement cases that assess ranking, not model factual correctness.
QUERIES = [
    ("verification email sending time", "REQ-002"),
    ("enhanced identity selfie", "REQ-003"),
    ("versioned privacy consent", "REQ-004"),
    ("manual risk review threshold", "REQ-005"),
    ("audit retention period", "REQ-007"),
    ("address mismatch verification", "REQ-011"),
    ("alternate accessible verification", "REQ-012"),
]
matched = sum(bool(search_requirements(query,new,top_k=3)) and
              any(h.requirement.id == expected for h in search_requirements(query,new,top_k=3))
              for query,expected in QUERIES)
print(f"Retrieval Recall@3: {matched}/{len(QUERIES)} ({matched/len(QUERIES):.0%}) on {len(QUERIES)} curated synthetic questions")
print("Limitations: Small illustrative set; does not establish production performance or evaluate LLM correctness.")
