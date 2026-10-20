# 🧭 ChangePilot
### Requirements intelligence • change-impact analysis • evidence-driven handoff

[**Launch the interactive demo ↗**](https://changepilot-app.streamlit.app/) · [Case study](docs/CASE_STUDY.md) · [Architecture](docs/ARCHITECTURE.md) · [Project brief](docs/PROJECT_BRIEF.md) · [Deployment](docs/DEPLOYMENT.md)

[![GitHub Actions](https://github.com/dishap12/ChangePilot/actions/workflows/tests.yml/badge.svg)](https://github.com/dishap12/ChangePilot/actions/workflows/tests.yml)

**A Business Analysis portfolio application** built with Python, Streamlit, Plotly, scikit-learn, SQLite, and optional OpenAI APIs. Compare revisions, visualize verified impacts, research requirements, and draft human-reviewable change artifacts.

> This is a **synthetic retail-banking portfolio demonstration**, not a banking product. The hosted build is restricted to fictional inputs and disables uploads, AI calls and review writes.

## Features

| Feature | Value | Important limitation |
|---|---|---|
| **Command center** | KPI tiles, interactive change mix, triage queue, gap coverage | Priority is a transparent keyword/link heuristic |
| **Version comparison** | Word-highlighted before/after view with filters | Stable REQ identifiers are the comparison basis |
| **Potential ID-renames** | Character TF-IDF + edit similarity flags candidate removed/added pairs | Proposals are unverified and never automatically reconciled |
| **Dependency explorer** | Interactive Sankey connecting requirements to mapped systems, owners and tests | Only explicitly provided CSV links appear |
| **Evidence search** | Source-cited offline TF-IDF retrieval | Lexical retrieval is not a neural semantic model |
| **Optional semantic retrieval** | OpenAI embedding ranking in local mode only | Requires explicit API opt-in, data transfer and possible charges |
| **Optional AI explanations** | Source-constrained, cited draft answers in local mode | Must be verified by a human |
| **Extraction studio** | Modal-language candidates from a freeform brief, with line provenance | Manual ID assignment and human review required |
| **Story & acceptance drafts** | Proposed user stories, boundary discussion prompts, change tickets | Not approved or executable acceptance tests |
| **Export and review** | Markdown/CSV review pack; local-only SQLite signoff log | Public mode has no shared review writes |

## A five-minute demo

The [live hosted version](https://changepilot-app.streamlit.app/) uses fictional retail banking onboarding requirements.

1. **Command center** — inspect 2 added, 5 modified, and 1 removed requirement; locate the 2 traceability gaps.
2. **Compare versions** — open REQ-005 to see risk-rule wording changes highlighted.
3. **Impact map** — select REQ-005 to visualize the Risk Decision Engine, mapped owner and tests. Then select unmapped REQ-012.
4. **Intelligence lab** — ask about identity verification, explore the source evidence, generate a freeform extraction worksheet, and review a source-backed acceptance-criteria draft.
5. **Review & handoff** — export the impact assessment and change inventory. Review logging is **disabled** in the hosted public demo.

There are no fabricated screenshots or claimed production metrics. Real screenshots and a video walkthrough can be added after visual verification.

## Run it locally

**Use Python 3.11 or 3.12.**

~~~bash
git clone https://github.com/dishap12/ChangePilot.git
cd ChangePilot
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
~~~

On Windows PowerShell, create your environment with py -m venv .venv and activate with .venv\Scripts\Activate.ps1.

Local comparison, impact maps, evidence search, extraction and exports work without an API key. For *optional* LLM answers and embeddings, copy .env.example to an untracked local .env and provide your own OPENAI_API_KEY. Do not upload private work documents or credentials.

### Input format

Supported local documents: TXT, Markdown, text-based PDF and DOCX. The deterministic parser requires one stable-ID requirement per line:

~~~text
REQ-001 | The system shall log the customer's consent version.
REQ-002 | The system must apply the risk team's approved review threshold.
~~~

Traceability links can be supplied in a CSV with columns:

~~~text
requirement_id,system,owner,user_story,test_case,link_type
~~~

Freeform extraction is an **unverified worksheet**, not an automatic replacement for an approved baseline.

## High-level architecture

~~~mermaid
flowchart LR
  A[Baseline and revised requirements] --> B[Deterministic ID diff]
  B --> C[Change queue]
  C --> D[Suggested rename review]
  T[Verified traceability CSV] --> E[System and test impact map]
  C --> E
  C --> F[Change ticket and acceptance drafts]
  A --> G[Local evidence retrieval]
  G --> H[Optional embeddings and LLM locally]
  X[Freeform brief] --> Y[Unverified candidate extraction]
  E --> Z[Export and analyst signoff]
~~~

Read [architecture and safety decisions](docs/ARCHITECTURE.md) for a full technical description.

## Testing

GitHub Actions runs on Python **3.11 and 3.12**, exercising module tests, Streamlit start-up (including forced safe public mode), the curated synthetic benchmark, and syntax checks.

~~~bash
python -m pytest -q
python scripts/evaluate.py
~~~

The small benchmark checks 12 hand-labeled change outcomes and Recall@3 on 7 deliberately selected synthetic questions. Those figures demonstrate reproducible functionality, **not** independent real-world precision or LLM accuracy.

## Safety, tradeoffs and roadmap

- Use **public_demo.py** as the Streamlit Community Cloud entry point. It forces read-only fictional-data mode. Do not deploy unrestricted app.py publicly.
- No real authentication, tenant isolation, or secure review data storage; SQLite is local-only. No claim of production or compliance readiness.
- Stable requirement IDs are the only verified version links. Candidate renames, extraction results and acceptance scenarios remain drafts.
- Supplied CSV links can be incomplete or outdated; unmapped does not mean unaffected.
- Neural semantic retrieval and AI answers are optional *local* API workflows, disabled in the public demo.
- Future priorities: editable versioned traceability, broader independent benchmarks, reviewer-confirmed complex-document extraction, authenticated workspaces, and a real screen-recorded walkthrough.

[MIT license](LICENSE) · [Deployment guide](docs/DEPLOYMENT.md) · [Business analyst project brief](docs/PROJECT_BRIEF.md)
