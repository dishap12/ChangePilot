# ChangePilot v0.2 — Architecture and engineering tradeoffs

## Purpose

ChangePilot is a local-first Business Analyst portfolio tool. It compares requirement IDs across versions and builds a source-auditable handoff. The hosted demo is **read-only, synthetic-data-only**, not an enterprise application.

## Processing flow

~~~mermaid
flowchart TB
  OLD[Baseline DOCX/PDF/MD/TXT] --> PARSER[Parse stable REQ IDs]
  NEW[Revised DOCX/PDF/MD/TXT] --> PARSER
  PARSER --> DIFF[Deterministic version comparison]
  DIFF --> LIST[Change inventory]
  LIST --> REN[Proposed ID rename similarity]
  MAP[Supplied traceability CSV] --> LINKS[Verified-link lookup]
  LIST --> LINKS
  LINKS --> SANKEY[Plotly dependency visualization]
  LINKS --> TRIAGE[Transparent priority heuristic]
  TRIAGE --> REPORTS[Impact pack and acceptance drafts]
  NEW --> SEARCH[Local TF-IDF]
  SEARCH --> EVIDENCE[Requirement evidence and scores]
  SEARCH --> OPT{Local opt-in and API key?}
  OPT -->|Yes| SEM[Optional OpenAI embeddings and LLM drafts]
  BRIEF[Freeform text brief] --> EXTRACT[Modal-language extraction]
  EXTRACT --> WORKSHEET[Editable unverified worksheet]
  LIST --> SQLITE[(Local-only SQLite reviewer decisions)]
~~~

## Provenance rules

1. **Identity matching:** Exact stable REQ ID matching is the only confirmed method across documents. A renamed ID is counted as Removed and Added, never silently resolved.
2. **Unverified rename suggestions:** Character-level TF-IDF and SequenceMatcher propose possible pairs among added/removed IDs. Similarity is not semantic proof or an approved relationship.
3. **Traceability:** Plotly Sankey edges connect requirements, systems, owners and test IDs only when explicitly supplied in the verified-links CSV. A missing link is an investigation gap, not evidence of no effect.
4. **Triage:** Review priority is determined by documented keyword / gap heuristic, not a risk model or compliance judgement. High-priority values describe a review queue.
5. **Local search:** Lexical TF-IDF on requirement-sized chunks. Scores are ranking signals only.
6. **Optional API:** When manually selected in unrestricted *local* mode, semantic embeddings send the question and current requirement text to an external API. Optional cited generation sends only retrieved snippets. Both may incur charges. Citation membership checks do not validate factual accuracy.
7. **Extraction:** A conservative modal-verb regex proposes line-based draft statements from a freeform brief, preserving line references. Analyst must correct text and manually assign stable IDs before integration.
8. **Acceptance drafts:** Templated user story, happy/negative path and numeric-change discussion prompts cite the originating requirement. They do not assert unprovided expected outcomes.
9. **Audit:** Local SQLite stores reviewer actions per input-set hash without authentication or tenant isolation. The hosted public demo does not read or write this database.
10. **HTML safety:** Word-level highlighting HTML-escapes user-uploaded requirement text before rendering.

## Public-demo safety

Host using the **public_demo.py** entrypoint. It overrides CHANGEPILOT_PUBLIC_DEMO=true before the application runs, irrespective of conflicting hosting environment values. Public mode disables all uploads, API calls, secret entry and reviewer writes, while demonstrating impact and exports on synthetic data.

The public mode is not a multi-user security certification. Do not host the unrestricted app.py for external visitors or process unapproved sensitive documents.

## Dependencies

- Streamlit: UI, data tables, interactive local widgets
- Plotly: change donut and known-link Sankey visualization
- pandas: table and worksheet CSVs
- scikit-learn: lexical source retrieval and character-level rename proposals
- python-docx and pypdf: text extraction only, not OCR
- SQLite (stdlib): local demo reviewer trail
- OpenAI (optional): opt-in embedding ranking or cited answer drafting
- pytest + GitHub Actions: offline tests and UI startup checks

## Known limitations and future iterations

- Requirement statements must use stable IDs in the main comparison, and formatted TXT/MD/PDF/DOCX text; irregular layouts and OCR are not handled.
- No robust ontology / transitive dependency inference; Sankey visualizes direct source-provided links.
- No confirmed reviewer workflow, role-based access or secure retention for enterprise use.
- No independently collected large benchmark; current small hand-labeled scenario demonstrates functionality only.
- No screenshots or video have been fabricated. Add a real visual walkthrough from the deployed build when reviewed.
- Future: analyst-confirmed freeform extraction → stable-ID reconciliation → versioned graph and authenticated review.
