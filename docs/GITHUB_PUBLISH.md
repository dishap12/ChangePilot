# Maintaining the ChangePilot GitHub repository

The project already lives at **[dishap12/ChangePilot](https://github.com/dishap12/ChangePilot)**. You do not need to create a repository or run `git init` again.

## What is already configured

- `app.py`, the source modules, synthetic sample inputs, and unit tests.
- `.gitignore` so local secrets, SQLite files, virtual environments, and caches are not committed accidentally.
- `.env.example` with placeholder settings only.
- `.streamlit/config.toml` for application theming and upload size.
- `.github/workflows/tests.yml` for automated checks on push and pull request.
- `docs/DEPLOYMENT.md` for a safe read-only public demo.

[View GitHub Actions results](https://github.com/dishap12/ChangePilot/actions). A green check verifies tests on the configured synthetic fixtures, **not** production readiness.

## Update your repository from your computer

If you already have a local clone, open its folder and run:

```bash
git pull origin main
# Make your changes, run the tests, and check what's staged:
python -m pytest -q
git status
git add .
git commit -m "Describe your changes"
git push origin main
```

If not, start with:

```bash
git clone https://github.com/dishap12/ChangePilot.git
cd ChangePilot
```

Do not commit `.env`, `.streamlit/secrets.toml`, `.local/`, or confidential source documents. If you ever accidentally commit a credential, revoke and rotate it; merely deleting the file in a later commit will not remove it from history.

## When preparing for recruiters

1. Check that [CI tests](https://github.com/dishap12/ChangePilot/actions) are passing.
2. Read the [deployment guide](DEPLOYMENT.md), set `CHANGEPILOT_PUBLIC_DEMO=true` in the hosting environment, and verify a live read-only sample walkthrough.
3. Inspect the entire repository and its history for sensitive information **before** making it public.
4. Make the repository public through its GitHub settings when ready. The connected GitHub app does not control repository visibility.
5. Add **real** screenshots and a short screen-recorded demonstration. Do not fabricate screenshots or claim the optional AI feature was tested unless it was.
6. Add the verified deployed link to the repository's About section and to the root README.
7. Keep the README's limitations and clear synthetic-data labels. Showcase an engineering choice, its tests, and what you would improve.

## Suggested portfolio description

Requirements change-impact analysis with traceability, evidence retrieval, optional AI-assisted drafting, and human review. Built with Python, Streamlit, scikit-learn, and SQLite.

## Suggested interview description

I built a local-first requirements intelligence application that compares explicit requirement IDs across document versions, traces linked systems and tests from supplied mappings, and produces a human-reviewable change pack. I added automated tests and a reproducible small synthetic benchmark. The application also supports optional cited AI drafts locally; its hosted demo can be restricted to read-only fictional data.

## Not part of this release

Automated requirement extraction from arbitrary freeform documents, independent semantic dependency discovery, authenticated multi-user review, and actual cloud deployment are separate future milestones.
