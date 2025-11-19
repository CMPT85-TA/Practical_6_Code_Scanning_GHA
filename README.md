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
- `.github/workflows/coverity.yml` — example workflow to run Coverity analysis on C samples
- `c_examples/demo.c` — intentionally unsafe C code for static-analysis demos
- `c_examples/Makefile` — minimal build instructions for the C demo

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

## SonarQube Cloud integration

Connecting SonarQube Cloud (SonarCloud) to GitHub mirrors the flow shown in the screenshots above and only takes a few clicks.

### Integration steps

1. Sign up at [sonarcloud.io](https://sonarcloud.io) using your GitHub account for a one-click registration.
2. When prompted, import an organization from GitHub or create one manually to match your GitHub workspace. The first image shows the GitHub App consent screen you will confirm here.
3. Install the SonarQube Cloud GitHub App for either **All repositories** or the specific repositories you want to scan.
4. Pick the plan that fits (free tier works for public projects); private repositories require the paid plan after the trial, as noted in the second image.

### Analysis steps

1. Select the repository you want to analyze and click **Set Up**. With automatic analysis enabled, there is no need to commit workflow files before you see results.
2. Define the New Code Definition (NCD) so Sonar focuses on recent changes—this fuels the “Clean as You Code” dashboard and keeps developers looking at the latest deltas.
3. Automatic analysis triggers immediately. SonarQube Cloud ingests the default branch, evaluates reliability, security, maintainability, and other quality measures, and updates the dashboard like the third screenshot.
4. Review findings under **Issues**, **Security Hotspots**, and **Measures**. Pull request decoration happens automatically once the GitHub App is installed, so future PRs show quality gates without extra configuration.

If you later want to run custom rules or on-premise scans, you can still add a `sonar-project.properties` file and use the `sonar-scanner` CLI or the `sonarsource/sonarcloud-github-action`. For the default classroom scenario, the GitHub App-driven automatic analysis is enough to start reviewing code quality within minutes.

## Coverity demo

Static analyzers such as Coverity can consume C and C++ examples in addition to Python. The repository now includes a vulnerable C sample under `c_examples/demo.c` and a Makefile that builds it with `make -C c_examples demo`.

- The code intentionally concatenates user-controlled input into a fixed buffer, triggering buffer overflow findings in Coverity, SonarQube, and other analyzers.
- The workflow `.github/workflows/coverity.yml` captures the build with `cov-build`, analyzes the intermediate directory, and submits results to a Coverity Connect server.
- Required GitHub secrets: `COVERITY_DOWNLOAD_URL` (pre-authenticated URL for the Coverity Analysis CLI), `COVERITY_URL`, `COVERITY_STREAM`, `COVERITY_USER`, and `COVERITY_PASSPHRASE`.
- Provide `cov-analysis` via the download URL once per cache key; subsequent runs reuse the cached installation to stay within runner time limits.
- If you add more compiled targets, update the Makefile and adjust the `cov-build` command.

Run `make -C c_examples clean` to remove the compiled binary after local experiments.