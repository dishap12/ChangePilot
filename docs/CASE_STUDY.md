# Case study — ChangePilot Requirements Intelligence

**Project type:** Self-directed, portfolio demonstration (fictional retail banking)
**Role simulated:** Business Analyst / Technology Consultant
**Application:** https://changepilot-app.streamlit.app/

## 1. The problem

A digital onboarding team receives a revised requirements baseline. A change to identity verification, risk threshold, consent or audit retention can affect multiple systems and test cases, but teams often have to manually compare documents and search for ownership and dependency references.

This demonstration asks: **How can an analyst create a traceable, review-ready impact assessment quickly, without presenting speculative AI output as confirmed system impact?**

The problem is intentionally scoped to a fictional scenario. No organizational customer data, actual banking policies or business impact measurements were used.

## 2. Requirements and success criteria

- Detect which stable-ID requirements were added, modified, removed or unchanged.
- Show literal before/after text differences and source IDs.
- Present *only* CSV-supplied system/owner/test links as verified traceability.
- Distinguish mapping gaps from low-risk results.
- Supply a fast evidence-search experience and human-reviewable change artifacts.
- Provide a safe public demonstration without user uploads, API calls or shared reviewer writes.

## 3. Design decisions

**Deterministic before speculative:** The version diff is anchored on requirement IDs. An ID rename is not silently guessed; it appears as removal + addition plus an optional, explicitly unverified similarity suggestion.

**Provenance-aware impact map:** Plotly Sankey shows connections only from the traceability fixture. The user can inspect the system and test records backing a graphic.

**Human-in-the-loop draft generation:** Proposed acceptance criteria contain a cited source requirement and boundary discussion questions. The tool does not fabricate expected results or claim that a generated sentence is an approved user story.

**Local-first retrieval:** TF-IDF needs no paid account for the hosted demo. Separate, explicit local-only opt-in modes can call hosted embeddings or an LLM for more advanced work, without disguising this as a completely free or offline neural model.

**Safe public deployment:** Streamlit's main hosting entrypoint is public_demo.py. It forces read-only fictional-data mode, while full local app.py retains upload and SQLite demo capabilities.

## 4. What the demo shows

| Business scenario | Observable result |
|---|---|
| Risk review rule changes from 80 to 65 (REQ-005) | Modified status, before/after diff, verified Risk Decision Engine link, draft test-discussion prompts |
| An accessible verification alternative is introduced (REQ-012) | Added status, traceability gap flag, explicit owner/test assignment question |
| Old address-verification rule is removed (REQ-009) | Removed status; possible rename relationships are kept unverified |
| Freeform fictional business brief | Candidate requirement statements with original line references; editable worksheet, no automatic approval |
| Analyst asks about identity verification | Source-ranked requirement evidence; public mode uses offline lexical matching |

The sample includes **2 added, 5 modified, 1 removed, and 4 unchanged** requirement IDs, with **2 unmapped changes**. These numbers describe the synthetic test fixture and are *not* time savings or measured organizational outcomes.

## 5. How I validated it

- Unit tests cover parsing, change classification, mapping gaps, reporting, local reviewer actions, rename suggestions, modal extraction, story drafts and graph provenance.
- Streamlit AppTest checks local and public startup, including that public_demo.py blocks uploads even when an environment variable attempts to disable safety mode.
- GitHub Actions tests Python 3.11 and 3.12, runs a small hand-labeled change benchmark (12 requirement outcomes), and checks Recall@3 on seven curated retrieval questions.
- These tests do not demonstrate real-world accuracy; a more diverse corpus, independent evaluation, and stakeholder validation are needed.

## 6. Current limitations

No OCR, robust freeform document extraction across complex layouts, automatic transitive graph inference, production authentication, enterprise access controls, or compliant retention scheme. Hosted mode intentionally disables review storage and AI APIs.

## 7. Portfolio / interview explanation

> I designed ChangePilot to reduce the manual work involved in understanding changes to business requirements. It compares document versions using stable requirement identifiers, traces the affected systems and test cases using explicit mappings, and provides an interactive impact view with evidence-backed draft review artifacts. I prioritized traceability and human validation over AI-generated claims, added a safe public demonstration, and tested the solution across two Python versions through automated CI.

**Skills demonstrated:** Business requirements analysis, change-impact assessment, source traceability, data modeling, Python application development, Streamlit/Plotly visualization, software testing, responsible applied AI integration, technical communication.

**Next iteration:** Analyst-confirmed traceability updates, independent retrieval evaluation, complex-document extraction, and an original screen-recorded walkthrough.
