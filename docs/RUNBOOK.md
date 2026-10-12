# Runbook

## Local configuration

Use a virtual environment and the pinned Python requirements. Deployment uses Python 3.12 and `requirements-linux.lock`; local Windows verification uses the existing 3.13 environment. The runtime dependency versions are unchanged in the portfolio pass.

Create `.env` from `.env.example` only for a fresh checkout. Set `MANAGER_USERNAME`, `MANAGER_PASSWORD` and an identifying NWS user agent privately. `DATABASE_PATH` points to local SQLite. Hosted inference uses the configured approved Chat Completions endpoint/model/key; availability after the event is not assumed. Missing/placeholder keys produce an explicit unavailable/degraded state.

```sh
python scripts/seed_demo.py
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 1
```

Seed is for a synthetic local office/roster. Preserve existing data. Choose a future-ending period in the displayed facility timezone, not the alert's validity window. Use the special-shift checkbox for a weekend demonstration. Refresh changes only form time; evaluate is separate.

## Checks

```sh
python -m pytest -q
npm ci --ignore-scripts
npm run format:check
python -m black --check --target-version py312 app tests scripts
python scripts/check_secrets.py
```

Tests use explicitly synthetic fixtures and do not require a hosted model. Live smoke scripts are separate opt-in network/provider operations; running a suite is not live integration proof. Keep credentials and raw provider diagnostics out of screenshots and logs.

The app image copies Python/app/static source and production scripts. Node/formatters are development tools. Linux candidate verification runs the complete tests in the exact built image with historical fixtures mounted read-only. Do not substitute a different rebuild for the tested image.

## Private operator deployment

The current private source is a5681bc; this portfolio candidate is not deployed. Existing operator access/recovery is in [DEMO_RECOVERY.md](DEMO_RECOVERY.md). Production deployment/restart remains separately approved, with no active jobs, a fresh consistent current backup, exact-image checks and original-body comparisons required.

Keep one worker, non-root/read-only container, loopback binding, existing env and persistent volume. No public HTTP Basic authentication, firewall/DNS change or new resource is part of local preparation. Never use `down -v`, prune volumes, reset/reseed production or restore an old backup merely to roll code back.

## Data and history

Replay reads frozen records and verifies bundle hashes. Roster/rules changes create later assessments; they do not rewrite an earlier decision. A memo is a separately versioned presentation of that record. Backups use SQLite's consistent backup API, not a blind copy of a live WAL database. Restore drills use a separate database/container.

A restart interrupts pending work rather than inventing success; re-evaluate explicitly. Idempotency protects repeated manager actions. Before recovery, check actual current activity and preserve all later decisions.
