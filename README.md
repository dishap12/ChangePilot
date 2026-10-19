# 🧭 ChangePilot — Requirements Intelligence & Change Impact Analysis

**A working, local-first business analysis portfolio application** for comparing requirements across versions, showing traceability to systems and tests, retrieving source evidence, and documenting human review decisions.

> **Portfolio demo, not a bank product.** All included onboarding rules, teams, user stories and test cases are synthetic. Do not upload confidential employer materials.

## The business problem
Changes in onboarding requirements frequently affect systems, acceptance criteria, tests and business owners. Analysts need a reproducible way to discover changes and identify known dependencies without pretending unverified links are facts.

## Key features

| Feature | Implementation | Evidence |
|---|---|---|
| Version comparison | Stable `REQ-###` ID matching + text comparison | Added / modified / removed / unchanged |
| Traceability | Verified CSV lookups | System, owner, user story, test case |
| Change triage | Explicit rules for sensitive terms and unmapped requirements | Review priority + explanation |
| Requirements Q&A | Local TF-IDF retrieval with numbered sources | No AI account required |
| Optional RAG generation | OpenAI Responses API over retrieved excerpts | Cited draft; analyst validates |
| Draft change tickets | Deterministic template from source requirements and CSV links | Downloadable Markdown checklist |
| Human review | SQLite decision log | Reviewer, UTC timestamp, action, note |
| Exports | Markdown and CSV | Shareable draft change pack |
| Evaluation | Unit tests + curated benchmark | Reproducible, limited metrics |

## Quick start (Mac / Windows / Linux)

You **do not need GitHub, a paid API, or a database server** to run the baseline app.

1. Install Python 3.10+ from https://www.python.org/downloads/ and open Terminal (Mac) or PowerShell (Windows).
2. Unzip `ChangePilot.zip`. In the terminal, change into the `ChangePilot` folder.
3. Create and activate a virtual environment:

**Mac / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

4. Install dependencies and start the app:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local URL shown in the terminal (typically `http://localhost:8501`). The **fictional sample data** loads automatically.

## Five-minute recruiter demo

1. **Overview:** See 2 new, 5 modified, 1 removed and 4 unchanged onboarding requirements.
2. **Compare versions:** Inspect REQ-005, which changes the hypothetical review threshold from 80 to 65.
3. **Impact analyzer:** See Risk Decision Engine, its mapped owner and test case. Download a draft change ticket. Review REQ-012 to see a new requirement with *missing links*, not invented impact.
4. **Ask requirements:** Search `Which requirements mention identity verification and selfie checks?` and inspect retrieved IDs. Works fully offline.
5. **Review log:** Record a decision, then export Markdown and CSV summaries.

## Optional AI generation

The search/retrieval and other workflows run for free locally, **without a language model**. To add AI-generated explanations grounded in retrieved requirements:

```bash
cp .env.example .env
```

On Windows, copy the file manually if needed. Open `.env` and set `OPENAI_API_KEY=...`. Do not commit `.env`, and do not paste the key into your README. Set `OPENAI_MODEL` to a model supported by your API account (default in example: `gpt-4.1-mini`). In the app's **Ask requirements** tab, check the optional AI box and click **Search requirements**.

AI calls are metered by the provider and can be wrong even with citations. The app checks that cited IDs were retrieved, but it does **not** guarantee the wording is accurate. Do not treat its response as an approved business requirement.

## File format for your own documents

Upload `.md`, `.txt`, text-based `.pdf`, or `.docx` files using one requirement per line:

```text
REQ-001 | The system shall notify the applicant of a final decision.
REQ-002 | Audit events shall be retained for 90 days.
```

Stable IDs are important. This MVP does not automatically identify freeform requirements in unstructured documents, convert scanned PDFs, or match renamed IDs.

For your own links, upload a CSV with the same columns as `data/traceability.csv`:

```text
requirement_id,system,owner,user_story,test_case,link_type
REQ-001,Notifications,Customer Ops,US-001,TC-001,verified
```

## Run tests and evaluate

```bash
python -m pytest -q
python scripts/evaluate.py
```

The benchmark uses curated questions on a tiny **synthetic** dataset; it is a functionality check, not evidence of production accuracy.

## Repo layout

```text
ChangePilot/
├── app.py                       # Streamlit interface
├── requirements.txt
├── data/                        # Synthetic sample requirements & verified links
│   ├── onboarding_v1.md
│   ├── onboarding_v2.md
│   └── traceability.csv
├── src/changepilot/             # Parsing, comparison, traceability, retrieval, AI, audit, reports
├── tests/                       # Unit tests
├── scripts/evaluate.py          # Transparent demo benchmark
├── docs/ARCHITECTURE.md         # Data flow, design decisions, production gaps
└── docs/PROJECT_BRIEF.md        # Stakeholders, acceptance criteria, demo walkthrough
```

## Engineering tradeoffs and limitations

- **No secret AI dependency:** All non-LLM functionality works offline using scikit-learn.
- **No pretend semantic engine:** TF-IDF is lexical retrieval, not embeddings or a neural search index.
- **No invented links:** Traceability is verified only relative to the supplied demo mapping; new requirements create review gaps.
- **No enterprise compliance assertion:** The tool does not determine regulatory adequacy or operational risk.
- **Not secure for public multi-user use:** Local SQLite reviews are unauthenticated. Do not host it with real user or organizational data.
- **Not all Word/PDF layouts parse:** Requirement lines must retain `REQ-### | ...` structure.

## Next roadmap milestones

- [ ] Semantic retrieval and retrieval quality evaluation against a separate benchmark
- [ ] Human-reviewed extraction of requirements from freeform docs
- [ ] Versioned requirements-to-test graph with transitive impact
- [ ] AI-assisted user stories and *specific*, testable acceptance criteria with source citations (current ticket template is a human-review checklist)
- [ ] Integration with a fictional issue tracker API
- [ ] Authenticated review workflows, access control, data retention settings
- [ ] UI screenshots and a 90-second public demo video

## Interview framing

**Problem:** Coordinating onboarding requirement changes across business and engineering teams is time-consuming and error-prone.

**Approach:** Built a Python + Streamlit application that compares stable requirement IDs, traces verified linked systems and test cases, and retrieves cited supporting evidence. Added optional LLM explanations and a human-review audit trail.

**Result:** Demonstrated reproducible change identification and an auditable draft report on fictional test cases. The synthetic benchmark measures functional correctness; real-world validation and production safeguards are future work.

## License
MIT — see `LICENSE`.
