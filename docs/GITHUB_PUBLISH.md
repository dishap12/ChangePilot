# Publish ChangePilot to a new GitHub account

You do not need a GitHub account to develop or run ChangePilot. Create it only when ready to publish your own tested work.

## Preparation
1. Run the project locally using the root `README.md`.
2. Personalize the documentation: what you built, what you measured, what worked and what did not.
3. Never upload an `.env` with your API key. `.gitignore` excludes it by default.
4. Add original screenshots, a short demo video, and a candid limitations section.

## GitHub account and repository
1. Create an account at https://github.com/signup and verify your email.
2. Create a **new public repository** named `changepilot-requirements-intelligence`.
3. Leave 'Add a README', `.gitignore`, and License **unchecked** when creating the empty repository, because these files already exist locally.
4. Make sure Git is installed on your computer.
5. In the unzipped `ChangePilot` folder, open Terminal / PowerShell:

```bash
git init
git add .
git commit -m "Build ChangePilot requirements intelligence MVP"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/changepilot-requirements-intelligence.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username. Sign in to GitHub when prompted using GitHub's recommended authentication method; a normal password may not work for pushing over HTTPS.

## Portfolio polish after the first push
- Record a 90-second screen capture showcasing REQ-005, REQ-012, retrieval evidence, and exports.
- Update the README with your verified evaluation results and a screenshot.
- Add a section on choices (why deterministic IDs and verified traceability instead of speculative AI links).
- Add CI to run `python -m pytest -q` for every push.
- Optionally deploy a **read-only** demo on Streamlit Community Cloud, with sensitive data and review logs removed/disabled first.

## Suggested repository description
> Requirements change-impact analysis with traceability, source-grounded retrieval, optional LLM assistance, and human review — Python, Streamlit, SQL-style SQLite audit, scikit-learn.

## Suggested profile project pitch
> Built ChangePilot, a local-first requirements intelligence tool to compare document versions, trace affected system components and tests, surface source-backed evidence, and generate draft analyst change tickets. Designed for human validation with transparent rules and a reproducible synthetic benchmark.
