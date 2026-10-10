# Technical decisions

## 2026-10-10
- Start kit found in project and read in full; no existing code to overwrite. Initialize local Git only, no remote publishing.
- Use existing Python 3.13.9 in an isolated .venv, validate imports/tests; deployment remains Python 3.12 Linux and requires separate verification.
- Single process/worker, static frontend, SQLite WAL; one writer and no delegation.
- Missing inference key produces explicit AI unavailable, never simulated tool-call proof.
- Generate a local random manager password in ignored .env without printing it. User can replace locally. Credentials rejected if placeholders.
- G1 remote blocked on Linode access/approval; continue G2–G4 independently as starter kit requires.
- Use subprocess isolation for inference deadline and read-only snapshot tools; no approval or notification tools.
- Add shapely for verified representative points in NWS polygons; no blind centroid or state-wide applicability.
- Fetch two days of hourly AQ to cover the selected work period across midnight. Validate complete hourly coverage, exact numeric cutoff and source/grid provenance.
- Empty LIVE NWS feed is valid; unavailable/stale/unverified NWS never becomes normal. Preserve strong warning candidates when supplemental evidence is incomplete, but require human override.
- Direct dependency versions pinned only after local import/test verification. Linux transitive lock and image digest remain pending successful Linux tests.
- User authorized setup/deployment of existing Ubuntu 24.04 Linode at 172.234.201.174, root SSH, supplied key path. No new paid provisioning/public exposure authorized.
- SSH trust on first use recorded in ignored per-project known_hosts; subsequent attempts strict. Server accepts the key; its passphrase and stopped/disabled ssh-agent are a real access blocker. Never remove the passphrase or request it in chat.
- Canonical NWS /points metadata coordinates use four decimal places; observed full-precision request returned 301, canonical request 200. Keep redirects disabled. Alert applicability is independently confirmed at the exact saved facility point.
- Bootstrap/deployment scripts prepared for review. Linux tests must pass inside the exact commit-tagged image; deploy that image with --no-build and preserve the named database volume.
- Local manager actions are explicitly prototype smoke-test decisions for synthetic offices; no real facility/employee direction or outbound messages.
- Live warning smoke measured 2,092.04 ms, 2 source HTTP attempts, 0 model/tool calls. This is one local observation, not a claimed impact metric or remote latency.

- 2026-10-10: Use the user-created Linode, no paid provisioning. Verified closurecall key-only second session before SSH/UFW changes; retain root key-only recovery and keep application loopback-only.
- Actual hosted model called all tools but misread UTC versus EDT and routing count in free prose. Replace unvalidated model facts with strict JSON evidence-reference/review-focus selection; validate against frozen run and render all facts from authoritative data. Invalid model selections degrade safely. Real grounded five-tool smoke passed.

- Linux Python 3.12 image passed 59 tests; capture that actual dependency resolution in requirements-linux.lock and pin the pulled base digest. Final Compose drops all capabilities, read-only root, no-new-privileges; SQLite and backups remain in writable persistent /app/data. Bound processes/memory/logs on the observed 1 CPU / 2 GB VM.
- Ubuntu packages were upgraded; controlled reboot before first app deployment applies security updates without interrupting any application data (no app was running).

- Private MVP verified on Linode, commit 8316a0ca896362f0dbe11b5b6c61ff6371a62902; retain source release and named SQLite data volume. Documentation checkpoints can advance local Git HEAD separately from deployed application commit. No application code change follows the verified freeze. Public exposure and submission stay external authorization steps.
- Existing local 8080 service preserved; use 8081 for the private SSH tunnel and constrained verification scripts.

## Acceptance decisions (2026-10-10)
- User authorized acceptance/demo checks and fixes that block correctness or presentation, without architecture expansion. Reopened the earlier code freeze only for observed gaps; final application freeze is 75300d4. Existing code, databases, old images/releases and backups are preserved; documentation HEAD can advance separately.
- Keep both saved sites fixed. Natural warning candidate is closure, with unsupported Flood Watch requiring review; explicit synthetic manager override acknowledges unverified access. KC approves natural normal with honest empty live feed. Do not engineer a nicer hazard result.
- Deferred is informational app inbox with explicit manual supervisor review before shift/immediately if ongoing; onsite reassignment requires new evaluation/decision. Do not add a scheduler/send integration. New fields do not rewrite historical bundles.
- Fix actual browser horizontal overflow, validation JSON readability, prior reason/timing retention and old evidence remaining during new LIVE collection. Clear only when run ID changes; preserve input during polling of that same run. No refactor/framework/agent expansion.
- Real zero-alert KC runs degraded after successful tools due to rejected model output (safe ValueError). Exact selection/cause is not logged; do not guess a root cause, relax validation, add unproven retries or claim all AI responses succeed. Retain as FAILED in acceptance.
- Use isolated SQLite/imported historical copy and changed current provider files for replay mutation test; external/recompute traps enforce zero calls. Never mutate production roster/rules or original backups for proof.
- Fresh exact-image Linux tests precede every private source release. Final backup/restart compares every stored bundle/draft and independently reads Docker identity, loopback ports and database counters. Evidence totals are not blanket proof of challenge requirements.
- Public/organizer-dependent items remain NOT VERIFIED. Official Akamai guide's Cloud Manager VM view is not replaced with an application footer label; SSH/runtime evidence is kept separately. Submission remains a draft.
