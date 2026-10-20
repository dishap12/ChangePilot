# Running and deploying ChangePilot

ChangePilot is a portfolio prototype. Its included requirements and traceability links are **fictional**. There is no authentication or tenant isolation.

## Run locally with the complete feature set

1. Install Python 3.11 or 3.12.
2. Clone and enter the repository:

```bash
git clone https://github.com/dishap12/ChangePilot.git
cd ChangePilot
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Windows PowerShell: create the environment with `py -m venv .venv`, activate with `.venv\Scripts\Activate.ps1`, and run the final two commands using `python`.

Without configuration, the app runs locally with example banking requirements, deterministic comparisons, TF-IDF search, exports, and a local SQLite review log. It does not need an OpenAI API key.

Optional, local-only LLM explanation: copy `.env.example` to `.env`, add your own `OPENAI_API_KEY`, and leave `CHANGEPILOT_PUBLIC_DEMO=false`. Never commit your `.env`, paste credentials into chat or screenshots, or upload confidential work materials.

## Before hosting a public demo

**Use `public_demo.py` as the deployed app's entrypoint.** It forces `CHANGEPILOT_PUBLIC_DEMO=true` before running the application, without needing an API key or a hosting secret. This switches the UI into a **read-only fictional-data demo**:

- Only the checked-in sample documents and traceability CSV can be used.
- File uploads are not offered.
- API-key entry and AI generation are disabled.
- Reviewer names and decisions are neither collected nor written to SQLite.
- The comparison, impact analysis, requirement retrieval, and downloadable draft reports still work with fictional content.

The local `app.py` defaults to full local mode; **do not deploy `app.py` publicly**. Deploy only `public_demo.py` to enable the safe subset by default. This is a safety precaution, **not** a claim of production-grade security. Review the app yourself after deploying.

## Deploy using Streamlit Community Cloud

1. Check that GitHub Actions is passing on `main`. Check for secrets in the repository's commit history before changing its visibility. A `.gitignore` does **not** remove secrets already committed.
2. Make `dishap12/ChangePilot` **public** when you want recruiters to see its source (GitHub repository **Settings → General → Danger Zone → Change repository visibility**). This is a user-only administrative action.
3. Open [Streamlit Community Cloud](https://share.streamlit.io/) and sign in with the GitHub account authorized for this repository.
4. Choose **Create app** / **Deploy an app** from GitHub and specify:
   - Repository: `dishap12/ChangePilot`
   - Branch: `main`
   - Main file path: `public_demo.py`
   - Python version: `3.11` or `3.12`
5. No secrets or API keys are needed for `public_demo.py`. Keep the hosting Secrets field empty, and do not configure OpenAI API credentials on a public demo.

6. Deploy, open the generated app URL, and verify that the sidebar says **Public demo**. If uploads or review forms are visible, unpublish the app and check the secret setting before sharing.
7. Smoke-test these tabs: Overview (sample KPIs), Compare (REQ-005), Impact analyzer (REQ-005 mapped, REQ-012 missing links), Ask requirements (local retrieval), Review log (disabled), and report downloads.
8. Only after verifying the app, add its real URL to the README and GitHub repository About section.

Reference: [Streamlit documentation: deploy](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app) · [Streamlit secrets](https://docs.streamlit.io/develop/concepts/connections/secrets-management).

## Continuous integration (GitHub Actions)

The file `.github/workflows/tests.yml` runs on each push to `main`, on pull requests, and manually. It checks Python 3.11 and 3.12, installs dependencies, runs the tests, evaluates the fictional benchmark, and compiles Python syntax. No credentials are needed.

View results at [ChangePilot Actions](https://github.com/dishap12/ChangePilot/actions).

## Troubleshooting

- **App fails to start:** Verify you're in the repository root and installed `requirements.txt` in an activated virtual environment.
- **No document requirements recognized:** This MVP needs lines formatted as `REQ-001 | The system shall ...`; scanned PDFs and arbitrary business documents are not automatically converted.
- **No AI answer:** Offline retrieval still works. AI generation requires an API key locally and explicit opt-in.
- **A public demo still allows uploads:** Verify the deployed main file path is `public_demo.py` (not `app.py`) and redeploy. Never publish the unrestricted local entrypoint.
- **SQLite audit log missing:** Public demo deliberately disables it; local mode creates `.local/reviews.db` when needed.

## What this demo does not prove

No real enterprise documents were validated. Requirement identity relies on explicit IDs, dependency links are supplied in a CSV, retrieval is lexical, and the AI output is not independently fact-checked. Enterprise deployment would require authentication, isolated and persistent storage, privacy review, and extensive testing.
