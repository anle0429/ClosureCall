# Verification evidence — local, 2026-10-10

This records executed tests, not a claim that all starter-kit acceptance items or the remote MVP passed.

- `python -m pytest -q`: 58 passed in 7.35s using .venv Python 3.13.9. Synthetic evidence appears only in tests with explicit labels.
- Import smoke: real Strands SDK 1.59.0, OpenAIModel and FastAPI imports passed; `pip check` passed.
- `scripts/smoke_sources.py`: NWS 200 / valid zero-alert Kansas City feed; Open-Meteo 200, modeled current AQI 44, valid 2026-10-10 20:00 UTC. Evidence `data/source-smoke.json`, ignored.
- Browser live warning explorer: NWS national feed 200 / 513 alerts at 20:48 UTC; supported warnings limited to 50 display rows. A synthetic site at 33.3400, -82.08478125 was independently confirmed by the NWS point endpoint. NWS metadata verified America/New_York.
- Real warning workflow: evaluation `bfe6fc0f-d562-453d-9996-65efdfe46f8a`, snapshot collected 20:53:42 UTC; three alerts including a Severe Flash Flood Warning. Current modeled AQI 47. Candidate closure preserved despite good AQ; additional Advisory/Watch had no automatic action mapping, so manager review/override was required.
- Authenticated prototype manager override at 20:54:37 UTC: decision `4d9ecd40-d611-46e4-99c6-09a23fe9ec1c`; 9 included, 2 excluded, 1 deferred. Essential staff keep supervisor reporting requirements, one accessible voice draft. No notification sent.
- Warning snapshot latency 2,092.04 ms, 2 source HTTP attempts, 0 model calls and 0 successful tools (AI unavailable). No inferred remote performance.
- Historical warning bundle hash `3ee9906908139c3fdc37cc0c813a3478252dcbf3899e875555f29768cfe4161e`. Kansas City normal decision `f0776147-bfed-4f7b-9ab3-2b4b692ab2b3` persisted unchanged across actual local server restarts, hash `f555dbd75cf75d6ca7712d303cb4ddb1cf61d674c9a3c2adeb27326794482af3`.
- Browser reload/sign-in restores the exact historical site, work period, timezone and stored decision; JSON package download to user Downloads succeeded. UI uses textContent and CSP; no model/source HTML execution.
- `scripts/check_secrets.py --decision-id ...`: 68 staged/tracked source files and 7 authenticated API responses passed configured secret/private-key scan (count before adding this document). `.env`, .venv, data, logs, backups and screenshots are ignored; no remote Git publish.
- `docker compose config --quiet` passed. Docker daemon unavailable locally, so image/Linux behavior is not yet proven.
- Tests cover cutoff boundaries 150/150.99/151/172; API timeout/503/401; null/stale/gapped AQ; point/time applicability; expired/test/cancelled/superseded alerts; unsupported alert; routing; auth/actor spoof/CSRF; missing override reason (422); stale and superseded approval; duplicate requests and transaction/outbox; immutable records, replay/backup/restart; actual SDK tool dispatch with a synthetic Model; model/tool budgets; subprocess kill and preservation of pre-timeout trace.

## Pending gates

- `scripts/smoke_inference.py`: exit 2 BLOCKED, INFERENCE_API_KEY missing/placeholder. Unauthenticated `/v1/models` probe returned 401, confirming network reachability only. Synthetic model tests do not satisfy live Strands/provider proof.
- SSH server at 172.234.201.174 accepts the supplied public key but signing requires the private-key passphrase. Windows ssh-agent is stopped/disabled. Remote OS/security/Docker/service state not inspected because authentication did not complete.
- Linux/image tests, remote workflow/restart persistence, firewall/listener proof, actual AI brief and final submission remain pending. No public app endpoint exposed.
- Organizer deadline/timezone and judging-access requirements not independently confirmed from the original challenge.

## Integration checkpoint 21:07 UTC
- 59 tests passed in 7.99s after grounded output validation change.
- Real workshop smoke passed with 2 model calls / 1 verified tool; full grounded brief passed with 2 model calls / all 5 verified tools. No raw generated time/count claims are exposed.
- Local warning decision replay bundle/drafts exactly unchanged after actual server restart.
- Browser reloaded during evaluating, re-login resumed the same run; facility/work-period/timezone restored correctly after small UI fix.
- SSH verified Ubuntu 24.04.4; Docker 29.9.0 / Compose 5.6.0 installed, hello-world passed; second closurecall session/Docker access passed. SSH passwords disabled, root key-only recovery, UFW SSH-only active. Linux app/image and remote workflow remain pending.
