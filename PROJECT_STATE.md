# ClosureCall — Project State
Updated: 2026-10-10 16:07 America/Chicago (21:07 UTC)
Repo: C:\Projects\ClosureCall; branch master; initial verified commit being prepared.
Current writer: Codex local, single writer.

## Working and verified
- Preserved original starter; continued existing implementation and SQLite data.
- LIVE NWS + Open-Meteo/CAMS -> deterministic prototype policy -> real Strands tools -> authenticated manager decision -> targeted demo outbox -> frozen REPLAY.
- Local normal and warning workflows verified; warning decision 4d9ecd40-d611-46e4-99c6-09a23fe9ec1c retains exact bundle/drafts after actual restart, hash 3ee9906908139c3fdc37cc0c813a3478252dcbf3899e875555f29768cfe4161e.
- Real workshop smoke passed: Strands 1.59.0, hackathon-chat, 2 model calls / 1 smoke tool. Full grounded brief probe passed: 2 model calls / 5 scoped tools; references and review focus validated, counts/time rendered from frozen data.
- Browser reload during evaluating restored the same run; corrected facility/timezone controls. No duplicate evaluation/notification.
- SSH verified existing Akamai Linode 172.234.201.174, Ubuntu 24.04.4, 44 GB free. Docker 29.9.0 and Compose 5.6.0 installed from official apt repo; hello-world passed.
- Second non-root closurecall SSH session and Docker access verified. SSH passwords/keyboard-interactive/X11 disabled; root key-only recovery retained. UFW active, deny incoming, SSH rate-limited; no app port opened. Configuration backed up before change.
- Credentials configured only in ignored .env; unlocked SSH identity has two-hour agent lifetime. Host key pinned in ignored data/deployment_known_hosts (initial TOFU).

## Environment and tests
- Local Python 3.13.9 private .venv; target Linux Python 3.12 not yet verified.
- Local http://127.0.0.1:8000; current hidden launcher PID in data/server.pid. Remote app/tunnel pending.
- Latest pytest: 59 passed in 7.99s. Meaningful grounding validation test added after actual model misread timezone/routing counts; raw generated factual prose is no longer published.
- Secret scan with actual key: 69 source files + 7 authenticated API responses passed before latest grounding/hardening additions; repeat before commit.
- Compose quiet config validates; Linux build/tests and remote full workflow not yet run.
- Runtime evidence and backups ignored. No Git remote publish or public app endpoint.

## In progress
- Ubuntu package upgrades running; no automatic reboot requested.
- Export verified commit, configure private remote env, test Linux image before loopback-only deployment.
- Then SSH tunnel full remote workflow, backup/restart/replay, resource and browser proof.

## Blockers / unresolved
- No current credential blocker. Real NWS contact email not supplied; honest product User-Agent works, contact recommended.
- Organizer deadline/event timezone and judging-access requirements not independently confirmed.
- Publication/domain/public judging URL remains outside current authorization.

## Next three actions
1. Secret-scan and commit tested source locally; transfer source archive and private env over pinned SSH.
2. Run exact-image Linux tests; pin tested Linux dependencies/image, deploy only passing image.
3. Verify real remote AI/source/manager/outbox/replay and exact hash after restart; finalize runbook and state.

## Limits and data honesty
- Synthetic facility, 12-person roster and weekend special shift; manager actions are explicit prototype test-account decisions, not real USDA facility actions.
- Rules/confidence are prototype assumptions, not USDA/OPM policy or probability. Unsupported categories remain for manager review; modeled AQ is not indoor sensing.
- Notification outbox drafts only; no email/SMS sent. No enterprise auth, public endpoint, simulation UI or absolute tamper resistance.
