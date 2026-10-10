# ClosureCall — Project State
Updated: 2026-10-10T22:03:59.649072+00:00 (UTC; America/Chicago UTC-05)
Repo: C:\Projects\ClosureCall; branch master; existing checkout preserved; one writer.
Deployed application commit: 75300d4ef4b86f8175be9f17f1fa291b00f9d7b9
Documentation/evidence checkpoint: subsequent local Git HEAD; see git log. No Git remote/publication.

## Current outcome
Private MVP and acceptance audit complete within the starter-kit scope. Fresh remote business/browser workflows were checked separately from synthetic tests. ACCEPTANCE_REPORT.md assigns VERIFIED / FAILED / NOT VERIFIED per deliverable. No blanket challenge-compliance claim. One unresolved observed AI validation failure remains in zero-alert KC runs; deterministic recommendation, manager approval and drafts worked.

## Runtime and access
- Existing authorized Akamai Linode 172.234.201.174, Ubuntu 24.04.4; deploy user closurecall, root key-only recovery. Region/resource label/Cloud Manager screenshot NOT VERIFIED.
- Docker 29.9.0 / Compose 5.6.0 / Python 3.12.15. Release /opt/closurecall/releases/75300d4ef4b86f8175be9f17f1fa291b00f9d7b9.
- Exact tested image sha256:6d89b1918e312c8b4f9dbd427dc0be0718016bf01cdecdfd461e6cc72dc9fc81. Container healthy after actual final restart; started 2026-10-10T21:59:17Z, rechecked 22:03 UTC.
- Appuser, read-only root, capabilities dropped, no-new-privileges; database in persistent named volume closurecall_closurecall-data. Backend binds VM loopback 127.0.0.1:8000. UFW active, SSH only.
- Remote operator UI http://127.0.0.1:8081 through existing pinned SSH tunnel. Use scripts/open_tunnel.ps1; passphrase entered directly in terminal. Existing unrelated port 8080 preserved. No public endpoint or judging URL.
- Local app http://127.0.0.1:8000 restarted with the same verified source/build; prior two local historical records exactly unchanged. Local .venv Python 3.13.9.
- Secrets remain ignored local .env / private remote /opt/closurecall/config/.env (600; parent 700). No credentials printed in acceptance logs or committed. Manager credentials in tab memory only; reload requires sign-in.

## Fresh acceptance workflows
- Fixed synthetic warning site 33.3400/-82.08478125, America/New_York, unchanged from baseline. Actual NWS Flash Flood Warning ID urn:oid:2.49.0.1.840.0.9e5ffc208914d848114373f0eabd11c9fbd68cfe.002.1; expires 2026-10-10T22:30Z. Captured records become historical; site name does not imply a current warning.
- Final warning run 8fac2108-0e09-492b-be31-8e41ad97b50a, NWS fetched 21:56:15 UTC/200/2 alerts. Selected synthetic shift 22:11–00:11 UTC intersects warning until 22:30; modeled AQI 48, valid 21:00 UTC. Natural closure candidate, unsupported Flood Watch review, low confidence rubric, prototype-v1 / FLOOD_WARNING version 1.
- Final warning AI active: real Strands 1.59.0 / hackathon-chat, 2 model calls / 5 successful scoped tools. Elapsed 57607.79 ms for this one run only.
- Manager test override 2efe6988-a638-4887-a15a-abc3319e5879 explicitly acknowledges missing local checks; drafts only. Bundle hash 4b5b9b42c30069005c51bdc0c2cc963f21c61c9fefcd46bc03ea84edc56039a0.
- Final KC run 9f0eeb64-a9f3-4660-881e-e9ffd36e2192: real empty NWS feed + fresh modeled AQ, natural normal/ready_for_manager. AI degraded ValueError after 5 successful tools / 2 model calls; no substituted historical AI success. Manager approval fc569eb8-54bd-4989-b9b7-fedcc46b3896; hash a5ff2acb07cc6f8e22cf038ca0a5301995af7c2f16b7ab6ff30695907ff8bb41.
- Actual packages explain all 12 synthetic people: 9 included / 2 excluded / 1 deferred for the saved roster. Included means queued_demo drafts, not delivery. Variant synthetic assignments produce 10/2/0; counts are not hardcoded. Deferred has explicit manual supervisor review/reassignment follow-up; essential and accessible voice instructions inspected.
- Before earlier run 47ba5569 finished, browser reload/re-login restored the same run and period; it completed with active five-tool AI and test override. Direct read-only SQLite counters show one decision/outbox batch per each of the five acceptance runs, despite browser double-clicks.

## Persistence, isolated changes and UI
- Original 8316a0c demo cf6d7432-7246-49d0-96ce-cb3da56d7f89 hash ec8f0456b3a4ff15be12a815e0526ad1892d7e7f6267d49903cf3e483ccb3705 remains exact across all acceptance deployments/restart. Original backups preserved.
- Isolated real historical export imported into separate ignored DB. Persisted current roster/rules changed; two API replay reads across lifespan restart remain identical, with zero NWS/AQ/model/assessment/routing calls. No demo DB or original backup edited.
- Final remote backup /app/data/backups/closurecall-20261010T215916Z.sqlite3. Actual container restart: all six remote historical bundles and drafts exactly equal baselines. Browser Refresh/replay/JSON export exact match; decoded accessible .eml body matches the frozen draft/no-send notice.
- Minimal acceptance fixes: deferred manual follow-up; matched rule version; concise validation errors; long-text wrapping; clear prior manager inputs for a new run; clear previous evidence/brief/timeline during current source collection. No architecture expansion.
- UI widths verified: 1280 ->1265, 720 ->705/single column, default 920 ->905; viewport reset. Empty override reason rejected, retry worked. Loading/active reload/double-click/history refresh/replay/export exercised.

## Tests and review artifacts
- Windows Python 3.13.9: 62 tests in 7.67s, named results evidence/acceptance/windows-tests-final.txt; pip check passed.
- Exact frozen Linux image Python 3.12.15: 62 tests in 4.96s before service change, evidence/acceptance/linux-deploy-tests-frozen.txt.
- Live source/model observations are separate JSON traces, not inferred from totals. Evidence under evidence/acceptance includes runtime/security/counters/restart/isolation/browser records, native screenshots, secret scan and hash manifest.
- Root documents: ACCEPTANCE_REPORT.md, DEMO_SCRIPT.md (180 seconds), SUBMISSION.md (unsubmitted draft), KNOWN_LIMITATIONS.md, DEMO_RECOVERY.md. Older docs now point to current handoff; docs/VERIFICATION.md retains dated baseline evidence.

## Remaining limits and information
- FAILED: observed KC AI validation degradation; exact rejected model selection/cause not logged, so cause NOT VERIFIED. Validation was not weakened to produce an active label.
- NOT VERIFIED: original USDA/Strands/Akamai organizer rubric, deadline/event timezone, eligibility, public judge access, Cloud Manager VM screenshot/region/resource label; live high-wind/high-AQ trigger; real local conditions/USDA authority; full accessibility certification; timed human rehearsal; full backup restoration into a separate live container.
- No current SSH/inference credential blocker. NWS contact email not supplied; unique honest product User-Agent works.
- Publication/HTTPS/domain/public repo/submission need explicit authorization and organizer requirements. No paid resources, external messages or notifications were sent.
- Synthetic staff/facilities/shifts; prototype mappings/confidence, modeled AQ, manual follow-up, drafts only. No compliance certification or statistical latency/impact claim.
