from pathlib import Path
from changepilot.parsing import parse_requirements
from changepilot.comparison import compare_versions
from changepilot.traceability import load_traceability
from changepilot.reports import summary_counts, report_markdown, change_csv

ROOT = Path(__file__).resolve().parents[1]


def test_sample_report():
    old = parse_requirements((ROOT / "data/onboarding_v1.md").read_text(), "V1")
    new = parse_requirements((ROOT / "data/onboarding_v2.md").read_text(), "V2")
    links = load_traceability((ROOT / "data/traceability.csv").read_text())
    changes = compare_versions(old,new)
    counts = summary_counts(changes)
    assert counts == {"Added": 2, "Modified": 5, "Removed": 1, "Unchanged": 4}
    assert "REQ-011" in report_markdown(changes,links)
    assert "Traceability gaps" not in change_csv(changes,links)  # CSV uses snake_case headers
    assert "traceability_gap" in change_csv(changes,links)
