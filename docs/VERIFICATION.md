# Executed verification — 2026-10-10T21:20:18+00:00

These are executed results. Synthetic unit fixtures and prototype manager tests remain explicitly labeled.

## Tests and image
- Windows private Python 3.13.9: 59 passed in 7.99s; pip check/import smoke passed.
- Linux first image: 59 passed in 5.77s. Final locked production image: 59 passed in 6.16s before docker compose up --no-build.
- Deployment commit 8316a0ca896362f0dbe11b5b6c61ff6371a62902; Python 3.12.15; Strands 1.59.0. Production pip check passed.
- Image identity sha256:64386106d97f124f0d30645cb9b920ff1ee4a195edcda0c553536bee87ac19c7. Base digest pinned and transitive Linux dependencies captured from actual tested image.
- Tests cover exact AQ boundaries, missing/stale/invalid/gapped feeds, point/work-period applicability, expired/test/cancelled/superseded alerts, unsupported categories, essential/accessibility/telework/offsite routes, auth/spoof/CSRF, reason validation, stale/superseded/idempotent decisions, atomic outbox, immutable records/replay/backup, actual SDK dispatch with a synthetic model, budget/deadline/process termination, and rejection of invented model references/facts.

## Live integrations and remote operation
- Local and remote real workshop smoke: 2 model calls / 1 verified tool; random server token used exactly once. No synthetic model is counted as hosted inference proof.
- Remote national NWS explorer: HTTP 200, 521 actual alerts at 21:14:41 UTC. Polygon point independently confirmed; timezone America/New_York verified by NWS metadata.
- Remote evaluation 49395bae-6b9f-4ec8-b267-7d0902f72212, collected 2026-10-10T21:15:19.606431+00:00. NWS 200 / 3 actual alerts, including Severe Flash Flood Warning. Open-Meteo 200 / modeled AQI 46 valid 21:00 UTC.
- Real Strands full brief active, 2 model calls and all five tools successful. Model-selected references and review focus validate against the frozen snapshot; server renders counts/timestamps/posture. Prior free-form model time/count mistakes prompted this validated contract.
- Single measured latency 29763.77 ms; 2 source HTTP attempts. No general performance/impact claim.
- Browser manager test override cf6d7432-7246-49d0-96ce-cb3da56d7f89 at 21:16:06 UTC: explicit synthetic office/shift reason, closure candidate plus review of unmapped Advisory/Watch. 9 included / 2 excluded / 1 deferred; all 12 have reasons/drafts. No notification sent.
- Reload while evaluating: re-login resumed the same run with correct site/work period/timezone. API verified one run and one decision.
- Baseline replay hash ec8f0456b3a4ff15be12a815e0526ad1892d7e7f6267d49903cf3e483ccb3705; SQLite backup then actual docker compose restart app; post-restart entire replay JSON/drafts exactly matched baseline.
- Browser re-login, explicit Replay and authenticated JSON download passed after restart. Export saved to user Downloads. Screenshots and safe Docker proof in ignored artifacts/.
- Local prior normal/warning decisions also retained exact replay after local restarts; their original AI-unavailable status is preserved honestly.

## Server and security
- SSH verified supplied existing host 172.234.201.174 / Ubuntu 24.04.4. Second non-root closurecall session passed before restrictions.
- Docker 29.9.0 / Compose 5.6.0 official apt install and hello-world passed. Ubuntu updates applied, reboot completed, kernel 6.8.0-134-generic; fresh strict SSH verifies SSH/Docker/UFW active.
- SSH passwords/keyboard-interactive/X11 disabled; root key-only recovery retained, config backed up. Initial host-key trust was TOFU; later SSH strictly pinned.
- Private env mode 600 with parent 700. Secrets excluded from Git/image build; 73 source files and 7 remote business API responses scanned with configured secrets, passed before final documentation additions.
- Running app uid 10001, read-only root, capdrop ALL, no-new-privileges; persistent writable data volume. Docker port explicitly 127.0.0.1:8000; UFW only rate-limited SSH. Public 8000 unreachable from this client; private tunnel health passes.
- Windows 8080 occupied by existing AgentService.exe preserved; tunnel uses 127.0.0.1:8081.
- Remote backup /app/data/backups/closurecall-20261010T211630Z.sqlite3 (159744 bytes) persists in named volume. No volume pruning/reset or existing history overwrite.

## External verification pending
Organizer deadline/timezone, eligibility and judging access; public repository/domain/HTTPS and actual submission. Region/resource console label not inspected. Private MVP operation is verified; localhost tunnel is not a public judging URL.
