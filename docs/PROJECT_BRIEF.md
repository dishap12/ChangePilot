# ChangePilot — Business analyst project brief (v0.2)

## Business problem

A fictional retail bank updates account onboarding requirements across identity verification, risk routing, consent, notifications and audit retention. Analysts must quickly identify changes, check *known* system/test relationships, and create reviewable requirements artifacts while avoiding unsubstantiated impact claims.

## Fictional stakeholders

- Business analyst — maintains requirements, assesses gaps and authors signoff artifacts
- Product owner — prioritizes requested changes and resolves scope questions
- Engineering lead — reviews system interfaces and implementation constraints
- QA lead — validates test impacts and defines executable expected results
- Privacy / risk subject experts — review compliance-sensitive areas; no automatic legal determinations

## Scope and acceptance criteria

| ID | Outcome | Acceptance check |
|---|---|---|
| CP-01 | Reliable comparison | Added/Modified/Removed/Unchanged classified by explicit source ID |
| CP-02 | Visual understanding | Command center shows counts and mapped-gap coverage |
| CP-03 | Understand wording | Selected requirements show HTML-escaped word-level before/after diff |
| CP-04 | Renamed ID investigation | Unverified similarity candidates shown without changing source classification |
| CP-05 | Documented links | Interactive map shows only CSV-supplied system, owner and test IDs |
| CP-06 | Evidence retrieval | Offline query returns sourced requirement excerpts and retrieval scores |
| CP-07 | Optional local AI | Semantic embedding or answer-generation features require manual key and opt-in |
| CP-08 | Unstructured candidate extraction | Freeform modal statements proposed with source line and unverified status |
| CP-09 | Handoff | Change ticket, draft user story, proposed criteria and impact report exported |
| CP-10 | Local review | SQLite decision records are tied to the selected input set |
| CP-11 | Safe hosted demo | Forced public_demo.py disables uploads, API calls and review writes |
| CP-12 | Regression coverage | GitHub Actions runs pytest, demonstration benchmark and syntax checks |

## Non-functional boundaries

- No claims of regulatory approval, production security, statistical model accuracy or autonomous BA signoff.
- Data comes from a synthetic sample unless explicit local input is provided.
- Stable requirement IDs and CSV links are the source of truth for comparison and dependency visualization.
- Optional API modes may incur charges; hosted public demo requires none.
- Human review is required for possible renamed IDs, extracted candidates, acceptance drafts and impacts.

## Demo story

1. Open the Command center: 2 additions, 5 modifications, 1 removal and 2 unmapped changes.
2. Inspect REQ-005 in Compare versions: the fictional numeric threshold changes from 80 to 65.
3. Select REQ-005 in Impact map: see Risk Decision Engine, Risk Operations and TC-005, based only on fixture CSV.
4. Select REQ-012: highlight unresolved traceability instead of inventing a system relationship.
5. Use Intelligence lab: search identity-verification requirements; suggest draft statements from a fictional freeform brief; review REQ-005 user-story / test-discussion prompts.
6. Export Markdown and CSV reports in Review & handoff. Public reviewer writes are intentionally disabled.

## Measurable but limited validation

The included benchmark evaluates a small deterministic fixture with 12 hand-labeled change classes and 7 curated retrieval cases; it does not establish generalization. Automated tests also exercise public-mode safety and new analysis modules. Do not report simulation outcomes as organizational improvements.
