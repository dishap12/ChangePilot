# Business analyst project brief

## Problem statement
A fictional retail bank updates account onboarding policies across identity checks, consent, risk routing, and audit retention. Analysts need to identify differences, trace linked systems and tests, and document a reviewable implementation impact.

## Stakeholders (fictional)
- Business analyst: reviews the change inventory and writes decisions.
- Product owner: prioritizes requirements for a release.
- QA lead: validates required regression and new test cases.
- Risk and privacy owners: clarify sensitive controls.
- Engineering: estimates implementation work and dependencies.

## MVP functional requirements
| ID | Business need | Acceptance criterion |
|---|---|---|
| CP-01 | Upload baseline and revised requirements | TXT, MD, PDF with text layer, DOCX can be parsed when lines follow `REQ-001 \| ...` |
| CP-02 | Detect added, removed and modified requirements | Deterministic classification by stable requirement ID |
| CP-03 | Show impact evidence | CSV mappings display owner, component, user story and test case |
| CP-04 | Identify traceability gaps | Requirements without mappings are visibly flagged |
| CP-05 | Ask a natural-language question | Local retrieval returns cited requirement IDs and similarity scores |
| CP-06 | Generate optional AI explanation | Explicit key and opt-in; answer labeled draft and evidence shown |
| CP-07 | Record analyst review | Saved reviewer name, decision, note, UTC timestamp in SQLite |
| CP-08 | Export findings | Download Markdown impact report and CSV inventory |
| CP-09 | Prepare handoff | Export a draft change ticket that names verified links and review questions |

## Non-functional requirements (MVP scope)
- Local-first baseline mode works without a paid API.
- Data inputs are fictitious or approved public materials.
- Explicit source IDs and traceability rather than inferred verified dependencies.
- Error messages for invalid or duplicate IDs.
- Automated unit tests with an inspectable evaluation script.

## Out of scope
Automated compliance conclusions; bank production deployment; multi-user secure review; ingestion of scanned PDFs; integration with a real Jira instance; fully autonomous requirement or test-case approval.

## Demo walkthrough (5 minutes)
1. Open the Overview to see 2 added, 5 modified, 1 removed, and 4 unchanged requirements.
2. Open Compare versions; read `REQ-005` risk threshold change from 80 to 65.
3. Open Impact analyzer; select `REQ-005` to see Risk Decision Engine, Risk Operations, `US-005` and `TC-005`.
4. Select `REQ-012`; observe missing owner/system/test mapping rather than a fabricated impact link.
5. Ask about identity verification. Inspect retrieved evidence; optionally run an API-based AI draft.
6. Record a review decision and export the report.
