"""Rebuild static recruiter-friendly sample artifacts without opening the GUI."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from changepilot.parsing import parse_requirements
from changepilot.comparison import compare_versions
from changepilot.traceability import load_traceability
from changepilot.reports import report_markdown, change_csv
from changepilot.tickets import draft_change_ticket

ROOT = Path(__file__).resolve().parents[1]
old = parse_requirements((ROOT / "data/onboarding_v1.md").read_text(), "V1")
new = parse_requirements((ROOT / "data/onboarding_v2.md").read_text(), "V2")
links = load_traceability((ROOT / "data/traceability.csv").read_text())
changes = compare_versions(old, new)
out = ROOT / "demo_output"
out.mkdir(exist_ok=True)
(out / "impact_report.md").write_text(report_markdown(changes, links), encoding="utf-8")
(out / "change_inventory.csv").write_text(change_csv(changes, links), encoding="utf-8")
selected = next(x for x in changes if x.id == "REQ-005")
(out / "req-005-draft-ticket.md").write_text(draft_change_ticket(selected, links), encoding="utf-8")
print(f"Wrote three examples to {out}")
