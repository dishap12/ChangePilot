"""ChangePilot Streamlit MVP. Synthetic demo; no authentication or production claims."""
from __future__ import annotations
import os
import sys
import hashlib
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from changepilot.parsing import extract_document, parse_requirements, RequirementsFormatError
from changepilot.comparison import compare_versions, changed_only
from changepilot.traceability import load_traceability, triage_change
from changepilot.retrieval import search_requirements, offline_response
from changepilot.ai import grounded_answer
from changepilot.audit import add_decision, list_decisions, ACTIONS
from changepilot.reports import report_markdown, change_csv, summary_counts
from changepilot.tickets import draft_change_ticket

load_dotenv(ROOT / ".env")
st.set_page_config(page_title="ChangePilot | Requirements Intelligence", page_icon="🧭", layout="wide")
st.markdown("""<style>
.block-container {padding-top: 1.5rem; max-width: 1250px}
[data-testid='stMetricValue'] {font-weight: 650}
div[data-testid='stTabs'] button {font-weight: 600}
</style>""", unsafe_allow_html=True)


def data_file(relative: str) -> bytes:
    return (ROOT / "data" / relative).read_bytes()


def decode_input(upload, demo_filename: str) -> str:
    if upload is None:
        return data_file(demo_filename).decode("utf-8")
    return extract_document(upload.name, upload.getvalue())


with st.sidebar:
    st.markdown("## 🧭 ChangePilot")
    st.caption("Requirements Intelligence · Portfolio MVP v0.1")
    st.markdown("### Workspace inputs")
    st.caption("Upload both document versions, or use the fictional banking demo.")
    upload_old = st.file_uploader("Baseline requirements", type=["md", "txt", "pdf", "docx"], key="old")
    upload_new = st.file_uploader("Revised requirements", type=["md", "txt", "pdf", "docx"], key="new")
    upload_csv = st.file_uploader("Traceability links (optional CSV)", type=["csv"])
    st.markdown("### AI mode (optional)")
    api_key = st.text_input("API key (session only)", type="password", value=os.getenv("OPENAI_API_KEY", ""),
                            help="Never commit your key. Only retrieved snippets are sent when AI generation is requested.")
    model = st.text_input("Model name", value=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"))
    st.info("Local retrieval works without an API key. AI answers require an OpenAI API key and may incur charges.")
    st.warning("Use fictional or approved public materials only. This demo has no authentication or tenant isolation.")

st.title("ChangePilot")
st.markdown("**From changing requirements to reviewable system impact.** Compare versions, inspect verified dependencies, and explore source-grounded answers.")

try:
    old_text = decode_input(upload_old, "onboarding_v1.md")
    new_text = decode_input(upload_new, "onboarding_v2.md")
    old_requirements = parse_requirements(old_text, "V1")
    new_requirements = parse_requirements(new_text, "V2")
    link_text = upload_csv.getvalue().decode("utf-8-sig") if upload_csv else data_file("traceability.csv").decode("utf-8")
    links = load_traceability(link_text)
    changes = compare_versions(old_requirements, new_requirements)
    workspace_id = hashlib.sha256((old_text + "\0" + new_text + "\0" + link_text).encode()).hexdigest()[:16]
except (RequirementsFormatError, ValueError, UnicodeDecodeError) as exc:
    st.error(str(exc))
    st.stop()

if upload_old or upload_new or upload_csv:
    st.info("You are using at least one custom input. Ensure your documents use IDs in the `REQ-001 | description` format and review whether the traceability CSV applies.")
else:
    st.caption("Demo scenario: a fictional retail bank updates onboarding identity checks, risk thresholds, consent, and audit rules.")

counts = summary_counts(changes)
changed = changed_only(changes)
a, b, c, d = st.columns(4)
a.metric("Added", counts["Added"])
b.metric("Modified", counts["Modified"])
c.metric("Removed", counts["Removed"])
d.metric("Traceability gaps", sum(triage_change(x, links)["gap"] for x in changed))

overview_tab, compare_tab, impact_tab, explore_tab, review_tab = st.tabs([
    "Overview & export", "Compare versions", "Impact analyzer", "Ask requirements", "Review log"
])

with overview_tab:
    st.subheader("What changed?")
    st.markdown("**Step 1:** Compare the two versions by requirement ID. **Step 2:** Review linked systems and tests. **Step 3:** Record a human decision or export a draft report.")
    summary = [
        {"Requirement": x.id, "Change": x.status, "Review priority": triage_change(x, links)["priority"],
         "Verified systems": ", ".join(sorted({p.system for p in triage_change(x, links)["links"]})) or "Unmapped"}
        for x in changed
    ]
    st.dataframe(pd.DataFrame(summary), use_container_width=True, hide_index=True)
    st.markdown("#### Export a review pack")
    e1, e2 = st.columns(2)
    e1.download_button("Download impact report (.md)", report_markdown(changes, links),
                       file_name="changepilot-impact-report.md", mime="text/markdown", use_container_width=True)
    e2.download_button("Download change inventory (.csv)", change_csv(changes, links),
                       file_name="changepilot-change-inventory.csv", mime="text/csv", use_container_width=True)
    with st.expander("How this analysis works"):
        st.markdown("Requirement IDs are compared exactly. Traceability comes only from the supplied CSV. Review priority is rule-based, not an AI risk prediction. ID renaming, implied dependencies, and ambiguous document wording require human review.")

with compare_tab:
    st.subheader("Version comparison")
    show_status = st.multiselect("Filter by status", ["Added", "Modified", "Removed", "Unchanged"],
                                 default=["Added", "Modified", "Removed"])
    options = [x for x in changes if x.status in show_status]
    st.caption(f"Showing {len(options)} of {len(changes)} requirements")
    if not options:
        st.info("No requirements match the selected statuses.")
    for item in options:
        with st.expander(f"{item.id}  ·  {item.status}" + (f"  ·  text similarity {item.similarity:.0%}" if item.status == "Modified" else "")):
            lcol, rcol = st.columns(2)
            lcol.markdown("**Baseline**")
            lcol.write(item.old_text or "— Not present —")
            rcol.markdown("**Revised**")
            rcol.write(item.new_text or "— Not present —")

with impact_tab:
    st.subheader("Impact analysis and traceability")
    if not changed:
        st.success("No changes detected using explicit requirement IDs.")
    else:
        choice = st.selectbox("Choose a changed requirement", [f"{x.id} — {x.status}" for x in changed])
        item = next(x for x in changed if x.id == choice.split(" — ")[0])
        triage = triage_change(item, links)
        st.markdown(f"**{item.id} · {item.status} · {triage['priority']} review priority**")
        st.write(item.new_text or "This requirement is absent from the revised document.")
        st.caption(triage["reason"])
        st.markdown("#### Verified traceability (from CSV)")
        if triage["links"]:
            st.dataframe(pd.DataFrame([{"System": x.system, "Owner": x.owner, "User story": x.user_story,
                                       "Test case": x.test_case, "Link type": x.link_type}
                                      for x in triage["links"]]), use_container_width=True, hide_index=True)
        else:
            st.warning("No verified links. This is a traceability gap, not evidence of zero impact.")
        st.markdown("#### Analyst's review questions")
        for q in triage["questions"]:
            st.markdown(f"- {q}")
        st.markdown("#### Export an analyst-ready change ticket")
        with st.expander("Preview a draft change ticket"):
            st.markdown(draft_change_ticket(item, links))
        st.download_button("Download draft change ticket (.md)", draft_change_ticket(item, links),
                           file_name=f"{item.id.lower()}-draft-ticket.md", mime="text/markdown")
        st.markdown("#### Draft review decision (local-only audit log)")
        with st.form("review_form"):
            reviewer = st.text_input("Reviewer name", placeholder="e.g. Demo Analyst")
            decision = st.selectbox("Action", sorted(ACTIONS))
            note = st.text_area("Reason / follow-up", placeholder="What evidence or clarification is required?")
            submitted = st.form_submit_button("Record review decision")
        if submitted:
            try:
                add_decision(ROOT / ".local" / "reviews.db", item.id, decision, reviewer, note, workspace_id)
                st.success(f"Saved a local review action for {item.id}. See the Review log tab.")
            except (ValueError, OSError) as exc:
                st.error(str(exc))

with explore_tab:
    st.subheader("Ask the requirements")
    st.markdown("Retrieve the most relevant **current-version** requirements. Optionally use an LLM to draft a cited explanation.")
    q = st.text_input("Question", value="What changed in enhanced identity verification and what needs review?")
    k = st.slider("Maximum retrieved requirements", 1, 7, 4)
    use_ai = st.checkbox("Generate AI-assisted answer (requires API key)", value=False)
    if st.button("Search requirements", type="primary"):
        hits = search_requirements(q, new_requirements, top_k=k)
        if not hits:
            st.warning("No sufficiently relevant excerpts found. Try a more specific question.")
        else:
            if use_ai:
                try:
                    answer, warnings = grounded_answer(q, hits, api_key, model)
                    st.markdown("#### AI-assisted draft — human review required")
                    st.markdown(answer)
                    for warning in warnings:
                        st.warning(warning)
                except Exception as exc:
                    st.error(f"AI generation did not complete: {exc}")
                    st.markdown("#### Local retrieval fallback")
                    st.markdown(offline_response(hits))
            else:
                st.markdown("#### Local evidence (no LLM call)")
                st.markdown(offline_response(hits))
            st.markdown("#### Retrieved sources")
            for h in hits:
                with st.expander(f"{h.requirement.id}  ·  retrieval score {h.score:.3f}"):
                    st.write(h.requirement.text)
        st.caption("Evidence is retrieved using TF-IDF, not semantic embeddings. LLM reasoning is optional and may contain errors.")

with review_tab:
    st.subheader("Human approval trail")
    st.caption("For local demonstration only. SQLite storage is not multi-user secure; do not deploy with real identities or private requirements.")
    log = list_decisions(ROOT / ".local" / "reviews.db", workspace_id)
    if log:
        st.dataframe(pd.DataFrame(log), use_container_width=True, hide_index=True)
    else:
        st.info("No reviews logged yet. Go to Impact analyzer to record a decision.")
    st.markdown("**Future production requirements:** user authentication, access controls, versioned decisions, encryption, and review workflow isolation.")

st.divider()
st.caption("ChangePilot v0.1 · Synthetic demonstration · Source-grounded retrieval · Analyst approval required")
