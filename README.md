# ClosureCall

ClosureCall helps a facility manager turn live weather and modeled air-quality evidence into a reviewed operating decision, targeted employee drafts, and a reconstructable decision record.

Hackathon targets: USDA Closure Call, AWS Strands Agents SDK, Akamai Cloud. This is a prototype for synthetic administrative offices, not an official USDA system. Action mappings are team assumptions, not federal closure policy. No real employee data or notification sending.

Progress is tracked in the [private GitHub repository](https://github.com/anle0429/ClosureCall), on branch `master`. See [GitHub progress instructions](docs/GITHUB_PROGRESS.md). A Git push stores code and review evidence; the application is deployed separately and remains accessible through its private SSH tunnel.

## Local setup

Use Python 3.12 (deployment) or the verified local 3.13 environment:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

Copy `.env.example` to `.env` only if `.env` does not exist. Set `MANAGER_PASSWORD` to a long random password, and configure `INFERENCE_API_KEY` privately. Do not paste keys into chat or Git. The initial local setup generated a password in ignored `.env`; view or change it locally. `MANAGER_USERNAME` defaults to `manager`. Set a contact email in `NWS_USER_AGENT`. If that field is still a placeholder, API requests use a unique product identification string without fake contact details.

```powershell
.\.venv\Scripts\python.exe scripts\seed_demo.py
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 1
```

Open http://127.0.0.1:8000. Sign in, select a work period in the displayed facility timezone, explicitly check the synthetic special-shift box on weekends, and collect live evidence. Review sources and policy, approve or explicitly override, then inspect routes and replay. Essential staff retain supervisor reporting instructions. Outbox `.eml` exports are drafts, never sent messages.

## Verification

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe scripts\smoke_sources.py
.\.venv\Scripts\python.exe scripts\smoke_inference.py
.\.venv\Scripts\python.exe scripts\backup_db.py
docker compose config --quiet
```

Unit test evidence is explicitly synthetic. `smoke_sources.py` makes real NWS and Open-Meteo calls and stores timestamps/hashes in ignored data. Inference smoke verifies that a real Strands tool returns a random server-side token and the model uses it. Missing inference key is a blocker, never a passing result.

Business routes all require server-side Basic authentication. Do not expose Basic Auth over public HTTP. The server runs one worker, one active evaluation, bounded API retries, and inference in a subprocess with a hard deadline, model-call and tool-call budgets. Provider errors are reduced to safe codes. No shell/cloud/send tools are given to the agent. The deterministic backend remains authoritative over posture and routing.

SQLite WAL stores immutable snapshots, results, decisions and outbox. Decisions and outbox are transactional and idempotent. Replay reads frozen records and checks hashes without calling sources, policy or model. This detects accidental changes; it is not a claim of government compliance or absolute tamper resistance. Restart interrupts active jobs rather than inventing success.

See [runbook](docs/RUNBOOK.md), [limitations](docs/LIMITATIONS.md), [demo](docs/DEMO_SCRIPT.md), and [project state](PROJECT_STATE.md) for actual verification/deployment status.

## Verified private deployment

Latest source **a5681bcd98400fd75d02670f378a04365459dd7e**, verified healthy/open at 8081 on 2026-10-11, adds **Refresh time (+15 min)** in Facility & work hours. Refresh updates only the form in the facility timezone and keeps shift length; it never starts an evaluation automatically. Final Windows **89/14.18s**, exact Linux **89/6.38s**; all nine original historical packages unchanged after deployment. [Current refresh release](WORK_HOURS_REFRESH.md). The precision release paragraph below records its earlier source/evidence.

Current application commit `4dffaac63f06b57bd97e2af17140ff850be147e5` was verified healthy and opened on 2026-10-11 through the private SSH tunnel **http://127.0.0.1:8081/**. The precision design is applied to the main release; 8084 remains separate QA. Use `scripts/open_tunnel.ps1` to reopen the tunnel; credentials stay in ignored `.env`. Exact deployed Linux image passed 89 tests / 6.53s; the earlier final Windows run passed 89 / 10.68s with unchanged app source. Separate remote QA used real NWS/AQ/Strands, natural recommendation, test approval, unsent drafts and replay. KC returned zero alerts. All nine original historical packages and six table fingerprints remained exact after the actual deployment/restart. See [current private release](PRIVATE_DESIGN_RELEASE.md) and [design comparison](PRECISION_DESIGN_REVIEW.md). The older [release manifest](RELEASE_MANIFEST.json) remains dated V2 evidence, not the current deployment identity.

Read [acceptance report](ACCEPTANCE_REPORT.md), [180-second English demo](DEMO_SCRIPT.md), [Vietnamese presenter notes](DEMO_PRESENTER_NOTES.md), [submission draft](SUBMISSION.md), [limits](KNOWN_LIMITATIONS.md), [attribution inventory](ATTRIBUTIONS.md) and [private recovery](DEMO_RECOVERY.md). Historical AI degradation remains preserved; new smoke success does not guarantee every future call. Saved Flood Watch/warning records are REPLAY only. Public exposure was cancelled in favor of laptop-only presentation; no domain or public app endpoint was opened. Judge access, team eligibility and actual submission remain user-owned and unverified. No real notification was sent.
