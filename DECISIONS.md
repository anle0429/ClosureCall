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

## GitHub progress decision (2026-10-10)
- User explicitly requested pushing to GitHub to track progress. Use a private repository in the already signed-in personal account, anle0429/ClosureCall. Preserve the existing master branch and all commits; no history rewrite, force push, generated starter files or application deployment.
- Scan complete reachable history as well as current tracked files before the first push. Keep environment files, runtime data, backups and SSH keys outside Git; HTTPS remote contains no credentials, and Git Credential Manager handles authentication.
- Verified first remote checkpoint daebe1a by git ls-remote. Documentation records the private remote; public visibility, collaborator access and actual challenge submission remain separate authorization steps.

## V2 verified release decisions — 2026-10-10
- Runtime 75300d4 versus docs daebe1a/6076307 differed only in docs/evidence; no blind redeploy for SHA matching. Deploy e5f7801 only after a necessary prompt fix and exact-image tests.
- New frozen-input model diagnostic selected NWS request URL as evidence ID; reject remained correct. Share existing ID set with prompt, enumerate it, cite empty NWS by snapshot ID. No schema relaxation, retry, provider/SDK change or new agent. Original historical exact error remains unknowable from safe log.
- Three consecutive new KC active samples suffice for bounded verification, not reliability statistics. Four total V2 live evaluations used; avoid repeated weather/model calls just for prettier evidence.
- Keep fixed site/thresholds unchanged. New Watch stays incomplete/low/unsupported; test override explicitly synthetic. Historical expired warning never reused as current LIVE.
- Restore with distinct volume/container/internal network/random test auth and no inference key. Read-only Docker cp failure fixed by stdin/tmpfs verification, without weakened isolation. Actual Uvicorn HTTP ran inside container; host port 8002 was unreachable. Stop drill container; retain original backups/data/resources.
- Code/policy/dependencies frozen at e5f7801; docs commit tracked separately. Existing explicit private progress-push authorization covers reviewed checkpoints on same origin/master, no force/public/access grants. User package files preserved and not auto-staged.
- User handles portal/team/judge access/Submit after technical readiness. No fabricated receipt or completed-goal status; finish independent technical work and handoff.

## Documentation follow-up — 2026-10-10 23:18 UTC
- Correct top-level entry points to e5f7801 / 65 actual tests, with dates and separate evidence/runtime identities. Keep older evidence intact; do not rerun tests or rebuild the frozen image for Markdown changes.
- Add Vietnamese presenter guidance required by the release goal alongside the English pitch, without inventing a human rehearsal. Attribution inventory reports local distribution metadata only; license selection, member attestations and portal terms remain user-owned.
- Actual read-only SSH health check at 23:16:01 UTC confirmed the same source/image/start/loopback. External access/Submit still deferred, with no new credential blocker; no further permission prompts or autonomous publishing.

## External gate audit
- Previous continuation made concrete documentation progress (78c0ddd and a5b433e). The same user-owned access/portal/Submit condition nevertheless remains unresolved through three goal turns; independent technical work is exhausted within approved scope. Mark the full goal blocked, preserve READY_WITH_DISCLOSED_LIMITATIONS / NOT_SUBMITTED, and stop autonomous continuation.
- User explicitly deferred portal/team/judge/Submit. Do not replace that decision with public exposure, collaborator grants, a guessed portal, accepted attestations, repeated weather/model runs or a manufactured receipt. Resume external release work only when the user supplies the needed information/authorization or asks to proceed.
