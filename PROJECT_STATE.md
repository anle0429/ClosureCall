# ClosureCall — Project State
Updated: 2026-10-10T21:20:18+00:00 (UTC; America/Chicago UTC-05)
Repo: C:\Projects\ClosureCall; branch master; single writer Codex local.
Deployed application commit: 8316a0ca896362f0dbe11b5b6c61ff6371a62902
Documentation checkpoint: subsequent local Git commit; see git log. No remote Git publish.

## Outcome
MVP private deployment complete: real NWS + modeled Open-Meteo/CAMS -> explicit prototype policy -> real Strands read-only tools -> authenticated manager test override -> targeted notification outbox -> immutable historical replay after restart.

## Deployment and access
- Existing authorized Akamai Linode: 172.234.201.174; Ubuntu 24.04.4; 1 CPU / about 2 GB RAM; region/Cloud Manager label not independently inspected.
- Docker 29.9.0; Compose 5.6.0; Python 3.12.15. Active release /opt/closurecall/releases/8316a0ca896362f0dbe11b5b6c61ff6371a62902.
- Container closurecall-app-1 healthy; appuser uid 10001, read-only root, all capabilities dropped, no-new-privileges; /app/data named persistent volume.
- Backend only 127.0.0.1:8000 on VM. Public port 8000 connection test failed as intended; verified listener and UFW SSH-only rules.
- Windows remote UI: http://127.0.0.1:8081 through active SSH tunnel; PID in ignored data/tunnel.pid. Port 8080 belongs to existing AgentService.exe and was preserved. Use scripts/open_tunnel.ps1 to reopen.
- Local UI: http://127.0.0.1:8000; separate hidden process PID in data/server.pid.
- Manager username manager; password in local .env and remote private /opt/closurecall/config/.env. Do not print or commit credentials. Remote env mode 600, parent 700. Key passphrase stays out of files/arguments; Git agent identity lifetime two hours, established tunnel continues while connected.
- Ubuntu packages upgraded and reboot completed. Kernel 6.8.0-134-generic; Docker/SSH/UFW active after fresh strict SSH. Password/keyboard-interactive/X11 disabled; root key-only recovery retained. Config backups /root/closurecall-config-backups.

## Remote workflow proof
- Synthetic point-confirmed office: site-b1a88d67-83cb-4c8c-a4b2-220f29254ed6, 33.3400/-82.08478125, NWS-verified America/New_York.
- Evaluation 49395bae-6b9f-4ec8-b267-7d0902f72212, collected 2026-10-10T21:15:19.606431+00:00; NWS HTTP 200, 3 actual alerts (Severe Flash Flood Warning, Flood Advisory, Flood Watch); modeled AQ HTTP 200, US AQI 46 valid 21:00 UTC.
- Work period 21:30–23:30 UTC, explicit synthetic weekend shift. Prototype closure candidate; additional Advisory/Watch categories require manager review.
- AI active: Strands 1.59.0, hackathon-chat, 2 model calls / 5 successful scoped tools. Strict model reference/focus selection validated; factual prose rendered from frozen data.
- Measured single evaluation: 29763.77 ms; 2 source HTTP attempts. No extrapolated impact/performance claim.
- Authenticated prototype manager test override: cf6d7432-7246-49d0-96ce-cb3da56d7f89, 21:16:06 UTC, explicit test reason. 9 included / 2 excluded / 1 deferred, all 12 explained; accessible voice draft and essential supervisor instructions retained. No real employee action or message sent.
- Historical bundle hash ec8f0456b3a4ff15be12a815e0526ad1892d7e7f6267d49903cf3e483ccb3705. Baseline exactly equals post-container-restart replay, including evidence, rules, brief, decision and drafts. Browser replay/re-login/export verified after restart.
- Reload during active job resumed same run and work period; API verified exactly one run/decision at this checkpoint.
- Remote SQLite backup /app/data/backups/closurecall-20261010T211630Z.sqlite3 is in persistent data volume. Local checkpoints/backups preserved separately.

## Tests and evidence
- Windows Python 3.13.9: 59 tests passed in 7.99s; private .venv; pip check passed.
- First Linux Python 3.12 image: 59 tests in 5.77s; captured actual dependency lock. Final locked image: 59 tests in 6.16s before deployment; pip check passed.
- Image identity sha256:64386106d97f124f0d30645cb9b920ff1ee4a195edcda0c553536bee87ac19c7; tested Docker base digest pinned in Dockerfile.
- Real workshop smoke passed locally and inside remote container: 2 model calls / 1 verified smoke tool using random returned token.
- Secret scan: 73 tracked source files + 7 remote authenticated API responses passed with configured secrets; final documentation scan next.
- Evidence: docs/VERIFICATION.md; ignored data/remote-*.json; artifacts/linode-verification.txt; artifacts/closurecall-linode-replay.png and closurecall-linode-outbox.png.

## Remaining external steps
- No current deployment/credential blocker. Public repository, HTTPS/domain/judging URL and actual submission need explicit publication authorization and organizer requirements.
- NWS contact email was not provided; honest product User-Agent works, contact recommended.
- Deadline/event timezone/eligibility not independently confirmed. G6 optional simulation UI intentionally omitted.

## Data honesty and limits
Synthetic offices/roster/shift and prototype manager tests; not official USDA operations. Rules/confidence are engineering assumptions, not USDA/OPM policy or probabilities. Unsupported categories stay visible for human review. Modeled AQ is not indoor sensing. Outbox drafts only, no send integration. HTTP Basic via private SSH; no enterprise login or public app endpoint. Hashes/immutable tables detect changes but are not compliance certification or absolute tamper resistance.

## Next actions if authorized
1. Confirm organizer deadline, access and submission requirements.
2. If public demo requested, obtain controlled domain/HTTPS/publication authorization; keep backend loopback and manager auth.
3. Rehearse using LIVE evidence when fresh and labeled historical replay when warnings have expired; preserve database/backups.
