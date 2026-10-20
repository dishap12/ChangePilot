"""ChangePilot v0.2 — requirements intelligence portfolio experience.

Read-only public demo accepts ONLY the checked-in synthetic example.
Local mode may load user-approved files; not production-ready or multi-tenant.
"""
from __future__ import annotations

from collections import Counter
from difflib import SequenceMatcher
from html import escape
import hashlib
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from changepilot.ai import grounded_answer
from changepilot.audit import ACTIONS, add_decision, list_decisions
from changepilot.comparison import compare_versions, changed_only
from changepilot.intelligence import (
    draft_story_and_criteria, extract_draft_requirements, propose_renamed_links,
)
from changepilot.parsing import RequirementsFormatError, extract_document, parse_requirements
from changepilot.reports import change_csv, report_markdown, summary_counts
from changepilot.retrieval import (
    offline_response, search_requirements, semantic_search_requirements,
)
from changepilot.tickets import draft_change_ticket
from changepilot.traceability import load_traceability, triage_change
from changepilot.visuals import change_donut, dependency_sankey

load_dotenv(ROOT / ".env")
PUBLIC_DEMO = os.getenv("CHANGEPILOT_PUBLIC_DEMO", "false").strip().lower() in {"1", "true", "yes"}
st.set_page_config(
    page_title="ChangePilot | Requirements intelligence",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Manrope:wght@400;500;600;700;800&display=swap');
:root { --ink: #18243d; --muted: #62718c; --blue: #5563d9; --border: #e2e8f3; }
html, body, [class*="css"], .stApp { font-family: 'DM Sans', sans-serif; }
.stApp { background: #f7f9fd; color: var(--ink); }
.block-container { max-width: 1450px; padding-top: 1.1rem; padding-bottom: 3rem; }
[data-testid="stSidebar"] { background: #eff3fb; border-right: 1px solid #e1e6f2; }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { line-height: 1.55; }
h1, h2, h3 { font-family: 'Manrope', sans-serif; letter-spacing: -.025em; color: #1c2945; }
h2 { font-size: 1.45rem; } h3 { font-size: 1.1rem; }
p, li { line-height: 1.58; }
.cp-brand { font: 800 1.38rem 'Manrope',sans-serif; letter-spacing: -.045em; color: #182648; margin: 0 0 .12rem; }
.cp-brand-mark { background: linear-gradient(135deg,#5c62e8,#2589b0); padding: .25rem .5rem; border-radius: 12px; color: white; margin-right: .35rem; }
.cp-subtitle { color: #61728f; font-size: .78rem; margin-bottom: 1.1rem; }
.cp-hero { background: linear-gradient(115deg,#182c59 0%,#2b3675 55%,#4054a2 100%);
           color: white; border-radius: 22px; padding: 1.45rem 2rem; margin-bottom: .9rem;
           box-shadow: 0 12px 34px rgba(31,55,109,.13); position: relative; overflow: hidden; }
.cp-hero:after { content: ''; position: absolute; right: -60px; top: -110px;
                 width: 420px; height: 350px; border: 1px solid rgba(255,255,255,.15);
                 transform: rotate(-22deg); border-radius: 50%; pointer-events: none; }
.cp-eyebrow { font-size: .69rem; font-weight: 800; letter-spacing: .16em; color: #bcd7ff;
              text-transform: uppercase; margin-bottom: .5rem; }
.cp-hero h1 { color: #fff; margin: 0 0 .45rem; font-size: clamp(1.9rem,3vw,2.65rem);
              font-weight: 800; line-height: 1.2; letter-spacing: -.045em; }
.cp-hero p { color: #dce7ff; font-size: .99rem; max-width: 760px; margin: 0; }
.cp-hero-pills { margin-top: .8rem; display: flex; flex-wrap: wrap; gap: .5rem; }
.cp-pill { display: inline-block; font-size: .74rem; color: #e8f2ff; border-radius: 30px;
           border: 1px solid rgba(255,255,255,.26); background: rgba(255,255,255,.09);
           padding: .3rem .7rem; }
.cp-sectionlabel { text-transform: uppercase; color: #71819d; font-weight: 800;
                   letter-spacing: .1em; font-size: .7rem; margin-bottom: .3rem; }
.cp-lead { color: #6d7992; font-size: .89rem; margin-top: -.5rem; margin-bottom: .9rem; }
.cp-glass { padding: 1rem 1.2rem; border: 1px solid #e1e7f2; border-radius: 16px;
            background: #fff; margin-bottom: 1rem; box-shadow: 0 4px 18px rgba(30,60,110,.04); }
.cp-flow { display: flex; gap: .65rem; flex-wrap: wrap; margin: .85rem 0; }
.cp-step { background: #eff3fc; border: 1px solid #e2e9f6; color: #334a7d;
           border-radius: 12px; padding: .6rem .9rem; font-size: .79rem; font-weight: 700; }
.cp-small { font-size: .79rem; color: #64758f; }
.cp-diff { padding: .85rem 1rem; line-height: 1.9; min-height: 90px; border-radius: 13px;
           background: #f2f5fb; font-size: .91rem; overflow-wrap: anywhere; }
.cp-add { background: #d9f3ea; color: #186c52; border-radius: 4px; padding: .1rem .2rem; }
.cp-del { background: #ffe7df; color: #a14d31; border-radius: 4px; padding: .1rem .2rem; text-decoration: line-through; }
.cp-banner { border: 1px solid #d9e2f5; background: #edf3fe; padding: .8rem 1rem;
             border-radius: 12px; color: #354b75; font-size: .85rem; margin-bottom: 1rem; }
[data-testid="stMetric"] { padding: 1.1rem 1.2rem; border: 1px solid #e0e7f1;
                             background: white; border-radius: 18px;
                             box-shadow: 0 4px 20px rgba(20,45,100,.045); }
[data-testid="stMetricLabel"] p { color: #667691; font-size: .81rem; font-weight: 650; }
[data-testid="stMetricValue"] { color: #273a69; font-family: 'Manrope',sans-serif; font-weight: 800; }
.stTabs [data-baseweb="tab-list"] { gap: .55rem; border-bottom: 1px solid #e0e6f0; }
.stTabs [data-baseweb="tab"] { border-radius: 10px 10px 0 0; padding: .75rem 1rem; font-weight: 700; font-size: .87rem; white-space: nowrap; }
.stTabs [aria-selected="true"] { background: #e9edff; color: #424fbb; }
div[data-testid="stVerticalBlockBorderWrapper"] > div { border-radius: 17px; }
div[data-testid="stDataFrame"] { border: 1px solid #e1e7f2; border-radius: 12px; overflow: hidden; }
.stButton button[kind="primary"] { background: #5864d6; border: 0; border-radius: 11px; }
.stButton button, .stDownloadButton button { border-radius: 11px; font-weight: 650; }
footer { visibility: hidden; }
</style>
""",
    unsafe_allow_html=True,
)


def data_file(relative: str) -> bytes:
    return (ROOT / "data" / relative).read_bytes()


def decode_input(upload, demo_filename: str) -> str:
    if upload is None:
        return data_file(demo_filename).decode("utf-8")
    return extract_document(upload.name, upload.getvalue())


def diff_html(before: str, after: str) -> tuple[str, str]:
    """Word-level diff; escape all uploaded text before HTML formatting."""
    a, b = before.split(), after.split()
    left, right = [], []
    for kind, i, j, k, l in SequenceMatcher(None, a, b).get_opcodes():
        a_text = escape(" ".join(a[i:j]))
        b_text = escape(" ".join(b[k:l]))
        left.append(f"<span class='cp-del'>{a_text}</span>" if kind in ("delete", "replace") and a_text else a_text)
        right.append(f"<span class='cp-add'>{b_text}</span>" if kind in ("insert", "replace") and b_text else b_text)
    return " ".join(left) or "<em>Not present</em>", " ".join(right) or "<em>Not present</em>"


with st.sidebar:
    st.markdown("<div class='cp-brand'><span class='cp-brand-mark'>◈</span> ChangePilot</div>", unsafe_allow_html=True)
    st.markdown("<div class='cp-subtitle'>REQUIREMENTS INTELLIGENCE · VERSION 0.2</div>", unsafe_allow_html=True)
    st.markdown("**Workspace**")
    if PUBLIC_DEMO:
        # Hosting is restricted to checked-in fictional inputs.
        upload_old = upload_new = upload_csv = None
        api_key, model = "", ""
        st.success("Public demo · fictional sample data only. Uploads, AI calls, and review writes are disabled.")
        st.caption("Explore the workflow safely without connecting any services or providing personal data.")
    else:
        st.caption("Use synthetic or approved public documents only.")
        upload_old = st.file_uploader("Baseline document", type=["md", "txt", "pdf", "docx"], key="old")
        upload_new = st.file_uploader("Revised document", type=["md", "txt", "pdf", "docx"], key="new")
        upload_csv = st.file_uploader("Verified links (CSV)", type=["csv"], key="trace")
        with st.expander("Optional AI configuration", expanded=False):
            api_key = st.text_input("API key — local session", type="password",
                                    value=os.getenv("OPENAI_API_KEY", ""))
            model = st.text_input("Generation model", value=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"))
            st.caption("Explicit requests may send retrieved source excerpts to OpenAI and incur API charges.")
    st.divider()
    with st.expander("How to explore the demo", expanded=False):
        st.caption("01 · Review change inventory")
        st.caption("02 · Compare language")
        st.caption("03 · Trace system & test impact")
        st.caption("04 · Explore evidence and drafts")
        st.caption("05 · Export an analyst review pack")
    st.divider()
    st.caption("Synthetic retail banking scenario · Not a banking product · Human approval required.")


try:
    old_text = decode_input(upload_old, "onboarding_v1.md")
    new_text = decode_input(upload_new, "onboarding_v2.md")
    old_requirements = parse_requirements(old_text, "V1")
    new_requirements = parse_requirements(new_text, "V2")
    link_text = (upload_csv.getvalue().decode("utf-8-sig")
                 if upload_csv else data_file("traceability.csv").decode("utf-8"))
    links = load_traceability(link_text)
    changes = compare_versions(old_requirements, new_requirements)
    workspace_id = hashlib.sha256((old_text + "\0" + new_text + "\0" + link_text).encode()).hexdigest()[:16]
except (RequirementsFormatError, ValueError, UnicodeDecodeError) as exc:
    st.error(f"Input could not be processed: {exc}")
    st.stop()

counts = summary_counts(changes)
changed = changed_only(changes)
triage = {item.id: triage_change(item, links) for item in changed}
gaps = sum(t["gap"] for t in triage.values())
mapped_systems = len({link.system for ch in changed for link in triage[ch.id]["links"] if link.system})
high_priority = sum(t["priority"] == "High" for t in triage.values())
is_custom = bool(upload_old or upload_new or upload_csv)

st.markdown(
    """<section class="cp-hero">
<div class="cp-eyebrow">Business analysis · Change intelligence · Evidence first</div>
<h1>Understand change.<br>Know what it touches.</h1>
<p>Turn evolving requirements into a traceable change inventory, a visual map of known
dependencies, and review-ready decisions — without inventing system impact.</p>
<div class="cp-hero-pills"><span class="cp-pill">◉ Change detection</span>
<span class="cp-pill">↗ Traceability mapping</span><span class="cp-pill">✳ Evidence retrieval</span>
<span class="cp-pill">✓ Human in the loop</span></div></section>""",
    unsafe_allow_html=True,
)
if is_custom:
    st.info("Custom input mode. Verify that supplied requirement IDs and the traceability CSV refer to the same workspace.")
else:
    st.markdown("<div class='cp-banner'><b>Live scenario:</b> a fictional retail bank revises customer identity checks, risk routing, consent, and audit standards. All results are illustrative.</div>",
                unsafe_allow_html=True)

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Added", counts["Added"])
m2.metric("Modified", counts["Modified"])
m3.metric("Removed", counts["Removed"])
m4.metric("Elevated review flags", high_priority, help="Heuristic only: selected control terms or missing traceability. Not a validated risk or compliance score.")
m5.metric("Unmapped changes", gaps)

overview_tab, comparison_tab, map_tab, intelligence_tab, handoff_tab = st.tabs([
    "Command center", "Compare versions", "Impact map", "Intelligence lab", "Review & handoff"
])

with overview_tab:
    st.markdown("### Change intelligence at a glance")
    st.markdown("<div class='cp-lead'>Review the change mix, locate traceability gaps, and prioritize follow-up work.</div>",
                unsafe_allow_html=True)
    left, right = st.columns([1, 1.65], gap="large")
    with left:
        with st.container(border=True):
            st.markdown("**Requirements mix**")
            st.plotly_chart(change_donut(changes), width="stretch", config={"displayModeBar": False})
    with right:
        with st.container(border=True):
            st.markdown("**Suggested analyst sequence**")
            st.markdown("""<div class='cp-flow'><span class='cp-step'>01 · Detect changes</span>
            <span class='cp-step'>02 · Review risk flags</span>
            <span class='cp-step'>03 · Follow known links</span>
            <span class='cp-step'>04 · Approve / export</span></div>""", unsafe_allow_html=True)
            st.markdown(f"**{len(changed)} changed requirements** across **{mapped_systems} mapped systems**.")
            st.caption(f"{gaps} changed requirements have no mapped dependencies. The application flags these as gaps, not as evidence of no impact.")
            st.progress((len(changed)-gaps)/len(changed) if changed else 1.0,
                        text="Change-level traceability coverage (demonstration only)")
            st.info("Elevated flags prioritize changes with missing links or selected control-domain terms. These are review cues, not validated risk scores.")
    st.markdown("#### Priority review queue")
    if changed:
        rows = []
        for item in changed:
            t = triage[item.id]
            rows.append({"Requirement": item.id, "Change": item.status,
                         "Priority": t["priority"], "Traceability": "Gap — review" if t["gap"] else "Mapped",
                         "Known systems": ", ".join(sorted({x.system for x in t["links"] if x.system})) or "—"})
        rows.sort(key=lambda row: (row["Traceability"] != "Gap — review",
                                   row["Priority"] != "High", row["Requirement"]))
        st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True,
                     column_config={"Requirement": st.column_config.TextColumn(width="small"),
                                    "Known systems": st.column_config.TextColumn(width="large")})
    else:
        st.success("No explicit-ID changes detected between these versions.")
    st.caption("Click **Impact map** to investigate a requirement and explore the verified system-to-test connections.")

with comparison_tab:
    st.markdown("### Compare requirement versions")
    st.markdown("<div class='cp-lead'>See what was added, rewritten, or retired. Highlighted words are compared literally, not semantically.</div>",
                unsafe_allow_html=True)
    filter_a, filter_b = st.columns([1.3, 1])
    with filter_a:
        statuses = st.multiselect("Change status", ["Added", "Modified", "Removed", "Unchanged"],
                                  default=["Added", "Modified", "Removed"])
    with filter_b:
        search_id = st.text_input("Filter requirement text or ID", placeholder="e.g. REQ-005, identity, audit")
    filtered = [ch for ch in changes if ch.status in statuses and
                (not search_id or search_id.casefold() in (ch.id + " " + ch.old_text + " " + ch.new_text).casefold())]
    st.caption(f"{len(filtered)} matching requirements · click a row to view a word-level diff")
    for ch in filtered:
        with st.expander(f"{ch.id}   ·   {ch.status}" +
                         (f"   ·   {ch.similarity:.0%} text similarity" if ch.status == "Modified" else "")):
            left, right = st.columns(2, gap="medium")
            old_html, new_html = diff_html(ch.old_text, ch.new_text)
            with left:
                st.caption("BEFORE · BASELINE")
                st.markdown(f"<div class='cp-diff'>{old_html}</div>", unsafe_allow_html=True)
            with right:
                st.caption("AFTER · REVISED")
                st.markdown(f"<div class='cp-diff'>{new_html}</div>", unsafe_allow_html=True)
            st.caption("Similarity is a string comparison only. A small edit can still have major business impact.")
    if not filtered:
        st.info("No requirements match those filters.")
    st.divider()
    st.markdown("#### Possible renamed requirements")
    st.caption("Character-level matching finds candidate links between *removed* and *added* IDs. Suggestions do not alter the comparison inventory.")
    suggestions = propose_renamed_links(changes)
    if suggestions:
        st.dataframe(pd.DataFrame([{"Removed ID": x.removed_id, "Added ID": x.added_id,
                                    "Text similarity": x.score, "Status": "Unverified — human review"}
                                   for x in suggestions]), width="stretch", hide_index=True)
    else:
        st.info("No credible rename candidates identified among the additions and removals.")

with map_tab:
    st.markdown("### Impact & dependency explorer")
    st.markdown("<div class='cp-lead'>Follow only documented CSV traceability. A missing edge means unknown impact, not confirmed independence.</div>",
                unsafe_allow_html=True)
    if not changed:
        st.success("There are no changed requirement IDs to investigate.")
    else:
        item_choice = st.selectbox("Investigate requirement", [f"{x.id}  ·  {x.status}" for x in changed])
        selected_id = item_choice.split()[0]
        item = next(x for x in changed if x.id == selected_id)
        impact = triage[item.id]
        a, b, c = st.columns(3)
        a.metric("Review priority", impact["priority"])
        b.metric("Verified links", len(impact["links"]))
        c.metric("Mapping gap", "Yes" if impact["gap"] else "No")
        st.markdown(f"**Current source — [{item.id}]**")
        st.write(item.new_text or "Requirement removed from revised version.")
        st.caption(impact["reason"])
        graph = dependency_sankey(item, links)
        if graph:
            with st.container(border=True):
                st.markdown("**Documented dependency map**")
                st.plotly_chart(graph, width="stretch", config={"displayModeBar": False})
                st.caption("Interactive visualization: requirement → system → owner / test case. All edges come from the supplied CSV.")
        else:
            st.warning("No verified dependency links for this requirement. Assign an owner and check downstream tests before approval.")
        if impact["links"]:
            st.markdown("#### Linked business artifacts")
            st.dataframe(pd.DataFrame([
                {"System": t.system, "Owner": t.owner, "User story": t.user_story,
                 "Test case": t.test_case, "Mapping": t.link_type}
                for t in impact["links"]]), width="stretch", hide_index=True)
        with st.expander("Analyst questions to resolve", expanded=True):
            for question in impact["questions"]:
                st.markdown(f"- {question}")
        st.download_button("Download this change ticket", draft_change_ticket(item, links),
                           file_name=f"{item.id.lower()}-ticket.md", mime="text/markdown")

with intelligence_tab:
    st.markdown("### Intelligence lab")
    st.markdown("<div class='cp-lead'>Find cited requirements, preview human-review extraction, and draft handoff language.</div>",
                unsafe_allow_html=True)
    qtab, xtab, stab = st.tabs(["Evidence search", "Extraction studio", "Story & criteria drafts"])
    with qtab:
        st.markdown("**Ask a question about the revised requirements**")
        question = st.text_input("Question", value="Which requirements relate to identity verification?",
                                 key="question")
        col_k, col_mode = st.columns([1, 2])
        with col_k:
            top_k = st.slider("Maximum evidence items", 1, 7, 4)
        with col_mode:
            if PUBLIC_DEMO:
                retrieval_mode = "Offline hybrid lexical (free)"
                st.caption("Public demo uses local lexical retrieval only. No document content is sent to an API.")
            else:
                retrieval_mode = st.selectbox("Retrieval method", [
                    "Offline hybrid lexical (free)", "Semantic embeddings (API, opt-in)"
                ])
        generate = st.checkbox("Draft an AI explanation (API, opt-in)", value=False,
                               disabled=PUBLIC_DEMO)
        if st.button("Explore evidence", key="search", type="primary"):
            if not question.strip():
                st.warning("Enter a question before searching.")
            else:
                try:
                    if retrieval_mode.startswith("Semantic"):
                        hits = semantic_search_requirements(question, new_requirements, api_key, top_k)
                    else:
                        hits = search_requirements(question, new_requirements, top_k=top_k)
                    if not hits:
                        st.warning("No sufficiently relevant evidence. Try more specific wording.")
                    else:
                        if generate and not PUBLIC_DEMO:
                            try:
                                answer, warnings = grounded_answer(question, hits, api_key, model)
                                st.markdown("#### AI-assisted draft — human approval required")
                                st.markdown(answer)
                                for warning in warnings:
                                    st.warning(warning)
                            except Exception as exc:
                                st.warning(f"AI generation could not complete: {exc}")
                                st.markdown(offline_response(hits))
                        else:
                            st.markdown("#### Evidence from source requirements")
                            st.markdown(offline_response(hits))
                        st.markdown("**Sources and retrieval scores**")
                        for hit in hits:
                            with st.expander(f"[{hit.requirement.id}]  ·  relevance {hit.score:.3f}"):
                                st.write(hit.requirement.text)
                        st.caption("Scores represent algorithmic retrieval ranking, not evidence reliability or requirement correctness.")
                except Exception as exc:
                    st.error(f"Retrieval could not complete: {exc}")
        st.info("Offline matching uses TF-IDF word features. Optional semantic embedding search and AI drafting make API calls only on explicit local opt-in.")
    with xtab:
        st.markdown("**Convert a freeform brief into a draft extraction worksheet**")
        st.caption("Suggestions are generated by conservative modal-language rules. They are not automatically assigned production requirement IDs.")
        brief = st.text_area(
            "Fictional business brief (editable for local analysis)",
            value=data_file("freeform_brief.md").decode("utf-8"),
            height=195, disabled=PUBLIC_DEMO,
        )
        if st.button("Propose requirement statements", key="extract"):
            candidates = extract_draft_requirements(brief)
            if candidates:
                st.session_state["extraction_drafts"] = candidates
            else:
                st.session_state["extraction_drafts"] = []
        if "extraction_drafts" in st.session_state:
            candidates = st.session_state["extraction_drafts"]
            if candidates:
                st.caption(f"{len(candidates)} candidate statements · review and edit before assigning stable requirement IDs")
                edited = st.data_editor(pd.DataFrame(candidates), key="draft_editor",
                                        width="stretch", hide_index=True, num_rows="fixed",
                                        disabled=["Draft ID", "Source line"])
                output = edited.to_csv(index=False)
                st.download_button("Export draft extraction worksheet", output,
                                   file_name="changepilot-extraction-draft.csv", mime="text/csv")
                st.info("Candidates are NOT applied automatically to the comparison. An analyst must review, assign stable REQ IDs, and import approved documents locally.")
            else:
                st.warning("No modal-language statements were found. Try lines with 'must', 'shall', or 'should'.")
        else:
            st.caption("Select **Propose requirement statements** to preview candidates from the fictional example.")
    with stab:
        if changed:
            story_id = st.selectbox("Source requirement", [c.id for c in changed], key="storyid")
            story_change = next(c for c in changed if c.id == story_id)
            proposal = draft_story_and_criteria(story_change)
            st.markdown(proposal)
            st.download_button("Export draft user story and criteria", proposal,
                               file_name=f"{story_id.lower()}-acceptance-draft.md",
                               mime="text/markdown")
            st.caption("These are review prompts, not approved or executable acceptance tests.")

with handoff_tab:
    st.markdown("### Review & handoff")
    st.markdown("<div class='cp-lead'>Export a change pack for BA, product, risk and QA review. No auto-approval.</div>",
                unsafe_allow_html=True)
    r1, r2 = st.columns(2)
    with r1:
        with st.container(border=True):
            st.markdown("**Impact assessment**")
            st.caption("Markdown report with source text, mapped systems, risks and analyst questions.")
            st.download_button("Download impact assessment", report_markdown(changes, links),
                               file_name="changepilot-impact-assessment.md",
                               mime="text/markdown", width="stretch")
    with r2:
        with st.container(border=True):
            st.markdown("**Change inventory**")
            st.caption("Machine-readable CSV including added/modified/removed status and traceability gaps.")
            st.download_button("Download change inventory", change_csv(changes, links),
                               file_name="changepilot-change-inventory.csv", mime="text/csv",
                               width="stretch")
    st.divider()
    st.markdown("#### Review decision ledger")
    if PUBLIC_DEMO:
        st.info("Read-only public demo. Human-review writes and the SQLite ledger are disabled. Use the local app to demonstrate reviewer sign-off.")
    else:
        if changed:
            with st.form("review_form"):
                selected_req = st.selectbox("Requirement to review", [c.id for c in changed])
                reviewer = st.text_input("Reviewer", placeholder="Demo analyst")
                decision = st.selectbox("Decision", sorted(ACTIONS))
                rationale = st.text_area("Evidence / next step", placeholder="Document why the decision was taken")
                submitted = st.form_submit_button("Record review decision")
            if submitted:
                try:
                    add_decision(ROOT / ".local" / "reviews.db", selected_req, decision,
                                 reviewer, rationale, workspace_id)
                    st.success(f"Recorded review action for {selected_req}.")
                except (ValueError, OSError) as exc:
                    st.error(str(exc))
        log = list_decisions(ROOT / ".local" / "reviews.db", workspace_id)
        if log:
            st.dataframe(pd.DataFrame(log), width="stretch", hide_index=True)
        else:
            st.caption("No decisions saved yet for this local document set.")
    st.markdown("#### Analysis boundaries")
    st.caption("Stable requirement IDs are the only verified identity links across versions. Suggested renames, draft extractions, and proposed criteria require BA review. CSV links can be outdated. This is not an enterprise compliance assessment.")

st.divider()
st.caption("ChangePilot v0.2 · Fictional banking data · Evidence-backed analysis · Human validation required")
