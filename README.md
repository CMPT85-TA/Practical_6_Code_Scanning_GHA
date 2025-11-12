# Code scanning demo

This repository demonstrates a few insecure Python patterns and safe alternatives. It also includes example GitHub Actions workflows to run automated scans with Bandit, Gitleaks, and CodeQL.

Files added:

- `vuln_app.py` — intentionally vulnerable patterns (eval, shell=True, MD5)
- `secure_app.py` — safer alternatives (ast.literal_eval, subprocess without shell, SHA-256)
- `tests/test_apps.py` — pytest tests for the secure functions
- `requirements.txt` — dependencies for local testing and Bandit
- `.github/workflows/bandit.yml` — example workflow to run Bandit
- `.github/workflows/gitleaks.yml` — example workflow to run Gitleaks
- `.github/workflows/codeql.yml` — example workflow to run CodeQL

## Enable GitHub Secret Scanning and Push Protection

GitHub has built-in secret scanning that does not require a workflow. You enable it in repository settings so GitHub scans your codebase and history for known secret formats, and optionally blocks pushes that contain secrets.

Steps (repository-level):

1) Go to your repository on GitHub > Settings > Code security and analysis.
2) Under “Secret scanning”, click “Enable” (or “Enable all” if presented).
3) Under “Secret scanning” > “Push protection”, click “Enable” to block pushes that include detected secrets.
4) Optional (org-level): In your organization’s Settings > Code security and analysis, turn on defaults so all repos inherit Secret scanning and Push protection. You can also add Custom patterns there.

Where results appear:

- Security tab > Secret scanning alerts (separate from Code scanning alerts).
- Some providers are notified by GitHub so they can help protect or revoke exposed tokens.

Demo in this repo:

- `vuln_app.py` includes clearly fake, hard-coded “DEMO_” credential strings meant only to trigger scanners. They are not real secrets.
- To avoid creating noise in a production repository, consider using a teaching branch and removing these demo strings after the exercise.

How to run locally (Windows PowerShell):

```powershell
python -m pip install -r requirements.txt
# Run tests
python -m pytest -q
# Run bandit scan
python -m pip install bandit
bandit -r .
```

Notes:

- The vulnerable examples are intentionally dangerous. Do not run `run_untrusted_code` on untrusted input.
- The CI workflows are example templates — you should review and adapt them for your repository and policies.