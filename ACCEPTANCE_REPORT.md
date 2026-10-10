# ClosureCall acceptance report

Audit date: 2026-10-10, America/Chicago (UTC-05). This report distinguishes live observations, synthetic tests and historical replay. VERIFIED means the specified check was performed; it does not certify official USDA operating policy or prize eligibility. Prior totals of 59 tests were not reused as proof for all requirements.

## Scope and baseline

Read PROJECT_STATE.md, TASKS.md, DECISIONS.md, AGENTS.md and the complete starter kit. Git was clean at 5fb8110; SSH and Docker confirmed the running application was 8316a0c. Existing code, database and backups were preserved. No new framework, agent or public endpoint was introduced.

Requirements below follow starter-kit section 2.1. Its referenced original organizer file `Pasted text(20261010-192748).txt` is not available in this checkout. The different Downloads file does not contain the named challenge. Exact original USDA/AWS rubric, eligibility, deadline/timezone and submission access requirements are NOT VERIFIED. The [official Akamai build guide](https://github.com/akamai-developers/akamai-workshop-hackmidwest/blob/main/docs/build.md) was inspected; it asks for a real application operation and a VM shown in Cloud Manager.

Application acceptance release: 75300d4ef4b86f8175be9f17f1fa291b00f9d7b9. Exact-image Linux tests, final workflows, actual restart and browser checks completed; evidence is recorded below. Documentation is a later Git checkpoint; use `git log -1` for that checkpoint, not as the deployed application identity.

## Deliverables

| Deliverable | Status | Concrete evidence and bounds |
|---|---|---|
| USDA: live NWS with real alert ID, URL, timestamp | VERIFIED | `evidence/acceptance/baseline-natural.json`, run b24192b3-49bc-4a9d-9cec-110488d674da, fetched 21:44:26 UTC, HTTP 200. Browser source panel and pre-override brief inspected. Saved site was not moved. |
| USDA: correct point and work period | VERIFIED | Point endpoint at 33.34/-82.08478125 returned Actual Severe Flash Flood Warning, ID `urn:oid:2.49.0.1.840.0.9e5ffc208914d848114373f0eabd11c9fbd68cfe.002.1`. Issued 21:33 UTC, expires 22:30 UTC; chosen synthetic shift 22:00–00:00 UTC overlaps the warning for 30 minutes, not the whole shift. NWS-verified site timezone America/New_York. |
| USDA: synthetic facility and additional signal | VERIFIED | Frozen facility includes coordinates, timezone, hours, working days, notice field and telework flag. All 12 people are synthetic. Same-point Open-Meteo/CAMS US AQI 46, PM2.5 3.7, returned grid 33.300003/-82.1, valid 21:00 UTC; source/forecast/attribution frozen. Modeled grid, not indoor sensing. |
| USDA: natural recommendation before override | VERIFIED | Pre-decision run has decision_id null, closure, unsupported_hazard, low confidence, FLOOD_WARNING match. Flood Watch requires human review; expired/nonoverlapping Advisory is retained as source context without creating the match. Screenshot 01 and JSON are pre-override evidence. |
| USDA: graduated posture, sources, versions, confidence/change basis | VERIFIED | Frozen policy prototype-v1, matched rule FLOOD_WARNING version 1, category match, numeric exceedance null. Browser inspected confidence/change disclosures; rule version now visible. Synthetic `test_aq_exact_cutoff` covers 150, 150.99, 151, 172. No fabricated live AQ exceedance. |
| USDA: reasoned human override | VERIFIED | Browser manager test override 8cfdc9a8-6daa-4576-b901-a93c8a7a1a25, `remote-override.json`. Reason acknowledges unsupported Watch and unverified access. Retains closure candidate; it does not claim local physical conditions were verified. Empty reason was rejected before any record. |
| USDA: approve natural recommendation | VERIFIED | Browser approval 9c022ef8-90ac-4f06-848f-24b232c35180, run c09838c5-b14f-4cc0-84ef-5f11d128ffef. Unchanged KC preset, current NWS HTTP 200/zero alerts, AQI 48, normal/ready_for_manager. `remote-approved.json`. AI was degraded and was explicitly acknowledged. |
| USDA: notification package for entire roster | VERIFIED | Both stored packages contain 12 distinct IDs, reason/channel/instruction/draft body. All rows checked against source roster; browser expanded accessibility, essential, telework, offsite and no-shift drafts. See roster table below. No real delivery. |
| USDA: deferred action is explicit | VERIFIED | Baseline FAILED: no follow-up step. Fixed recipients/notifications/UI; new package has manual supervisor review before shift or immediately if ongoing; onsite reassignment requires re-evaluation/new human decision. `test_deferred_has_manual_follow_up_in_draft`, screenshot 03. Original historical drafts were not rewritten. |
| USDA: dynamic counts, not fixed 9/2/1 | VERIFIED | `test_counts_and_instructions_change_with_roster_and_posture` changes assignments and obtains 10/2/0; reject test yields zero included. Counts are calculated from routes. Actual saved roster currently happens to produce 9/2/1. |
| USDA: reconstructable historical decision record | VERIFIED | Exact snapshot, policy, roster, assessment, validated AI selection, SDK trace, metrics, actor/time/reason and drafts are frozen. Original bundle hash ec8f0456b3a4ff15be12a815e0526ad1892d7e7f6267d49903cf3e483ccb3705 unchanged across acceptance deployment. |
| USDA: replay after current roster/rules change without sources/model | VERIFIED | `replay_isolation.py` copies the real historical export into a separate ignored SQLite DB. Changed current rules/roster are persisted in separate files and bound to current providers. Two API reads across app lifespan restart remain exactly equal; NWS/AQ/model/assessment/routing call traps count zero. `replay-isolation-results.json`; separate pytest integration also passes. No demo DB or original backup changed. |
| USDA: threshold defensibility | VERIFIED | `app/policy/rules.json` separates reference_claim, prototype_mapping_reason, required_context and limitations. [AirNow](https://www.airnow.gov/aqi/aqi-basics/) confirms 151–200 is unhealthy; [NWS API](https://www.weather.gov/documentation/services-web-api) describes alert data. Office posture mappings are explicitly our prototype assumptions. Official USDA/OPM approval of thresholds is NOT VERIFIED. |
| Strands: actual SDK and hosted tool calls | VERIFIED | Real run b24192b3 shows SDK 1.59.0, hackathon-chat, 2 model calls, 5 successful scoped hooks. `baseline-natural.json` trace and `remote-override.json`, plus SDK synthetic loop tests. Model alias does not identify a verified underlying model vendor/version. |
| Strands: bounded, read-only agent authority | VERIFIED | `app/agent/factory.py`, tools, prompts, grounded_brief; model/tool/deadline/scope/injection tests in Windows log. Agent has no approve/send/shell tool. Factual prose is rendered from frozen data after model reference/focus validation. |
| Strands: successful AI brief on every normal live run | FAILED | KC live runs c09838c5 and final 9f0eeb64 degraded with safe code ValueError after 5 successful tools/2 model calls. Deterministic recommendation and approval remain usable. Exact rejected model output was not logged, so its precise cause is NOT VERIFIED; validation was not weakened. |
| Akamai: actual remote application workflow | VERIFIED | Strict SSH to authorized VM, commit-tagged tested image, loopback tunnel, real evaluate/review/manager decision/drafts/replay. `remote-runtime.txt`, Linux deploy log and frozen remote records; health alone was not used as proof. |
| Akamai: Cloud Manager resource screenshot/region/label | NOT VERIFIED | SSH/runtime proof exists, but no authenticated Cloud Manager view was supplied/inspected. Obtain a secret-free VM resource screenshot before submission. |
| Akamai: shared inference integration | VERIFIED | Successful remote Strands feature uses approved workshop endpoint and alias with key backend-only; current [inference reference](https://github.com/akamai-developers/akamai-workshop-hackmidwest/blob/main/docs/inference.md) inspected. Eligibility of shared inference alone is NOT VERIFIED; this app also runs on Linode. |
| Public judging URL, public repository access and actual submission | NOT VERIFIED | App remains private; no public repository/HTTPS/domain or submission was created. Subsequent user-authorized progress push created private anle0429/ClosureCall; git ls-remote matched daebe1a. This does not establish judge access or submission. Public access requires organizer requirements and explicit authorization. |

## Notification review of the actual closure package

`queued_demo` means an included draft placed in the demo outbox. It does not mean email/SMS/voice delivery. All included channels are planning labels; no transport exists. Excluded draft exports exist for audit inspection but have channel none.

| ID / synthetic person | Route / channel | Reason and content checked |
|---|---|---|
| demo-01 Avery Hart | included / app_inbox | Onsite overlap; supervisor approves work/leave; no paid-leave entitlement. |
| demo-02 Blair Reed | included / app_inbox | Same onsite conditions and bounded closure instruction. |
| demo-03 Casey Brook | included / voice_accessible | Accessibility preference preserved; same factual work period/reason; voice is a draft, no call. |
| demo-04 Drew Vale | included / app_inbox | Onsite overlap; supervisor work/leave guidance. |
| demo-05 Ellis Lane | included / app_inbox | Onsite overlap; supervisor work/leave guidance. |
| demo-06 Finley Stone | included / app_inbox | Not telework eligible; no automatic telework or paid leave granted. |
| demo-07 Gray Morgan | included / app_inbox | Not telework eligible; supervisor-approved arrangements. |
| demo-08 Harper Quinn | included / app_inbox | Essential: reporting remains subject to designated supervisor and local procedures. |
| demo-09 Indigo Ray | included / app_inbox | Essential: same explicit reporting safeguards. |
| demo-10 Jordan Lake | deferred / app_inbox | Already telework; informational only. Manual follow-up before shift/immediately if ongoing; re-evaluate after onsite reassignment. |
| demo-11 Kai Rowan | excluded / none | Offsite/current assignment at another facility; no urgent site instruction. |
| demo-12 Logan Fern | excluded / none | No assigned shift; no urgent site instruction. |

The approved-normal package instead says continue assigned duties/monitor updates for routine onsite staff. Essential and telework safeguards remain. Synthetic telework-posture tests verify eligible versus ineligible instructions. No live wind/high-AQ trigger was available at these fixed sites; those live branches are NOT VERIFIED.

## UI findings and test evidence

- Baseline long URLs/IDs caused document width 1274 at viewport 920. Minimal wrapping fix verified document width 905 after deployment. Source IDs, grounded text and footer remain readable. No layout redesign.
- Baseline missing-reason error exposed a large validation JSON; now a concise validation message. Empty-reason record rejected, button returns enabled, manager can correct and retry.
- Baseline reason/timing remained in form across evaluations. Inputs now clear only on a new run ID, not during polling of the same run. Final browser recheck: previous manager reason cleared, all reason/timing/basis inputs empty; screenshot 11 and browser-verification.json.
- Real browser double-clicks on evaluate and decision were exercised. Database read-only counters and immutable/idempotency tests establish one record/batch per run; total counts are not inferred from the number of visible buttons.
- Reload/re-login restores the saved work period, timezone and current run; history Refresh/replay and frozen export are exercised. Active-job reload retained run 47ba5569-4800-4161-b7fb-dd2899dc6c25; no duplicate run/batch. Screen checks at 1280/720/default 920 are in browser-verification.json.
- Windows: `windows-tests-final.txt`, Python 3.13.9, 62 passed in 7.67s. Frozen image Linux checks: `linux-deploy-tests-frozen.txt`, Python 3.12.15, 62 passed in 4.96s; test totals do not establish live integrations. Pip check passed locally.
- Synthetic T01–T19/T23 assertions are covered by explicitly named tests in those logs: source failures/nulls, applicability/test/cancel/expiry, exact cutoffs, human auth/override/idempotency/staleness/simulation/timing, agent scope/budgets, injection and DOM escaping. Simulation UI is not implemented; only rejection at the decision boundary is verified.

## Remaining acceptance boundaries

FAILED live behavior: AI validation degradation in the observed KC normal run. No silent replacement of it with a successful historical AI response. Local building access, real USDA staff/authority, transport delivery, official threshold approval, full accessibility certification, high-wind/high-AQ live trigger and Cloud Manager resource view are NOT VERIFIED. Follow-up is manual, not a scheduler. An end-to-end restored backup in a separate live container remains NOT VERIFIED; isolated SQLite copy/replay is verified. No statistical latency or impact claims are made.

## Final frozen-release verification

- Deployed application: 75300d4ef4b86f8175be9f17f1fa291b00f9d7b9, image sha256:6d89b1918e312c8b4f9dbd427dc0be0718016bf01cdecdfd461e6cc72dc9fc81. `remote-runtime-frozen.txt` shows healthy exact tag, appuser, read-only root, dropped capabilities, no-new-privileges and 127.0.0.1:8000 binding. `remote-security.txt` shows UFW SSH-only and env directory/file modes 700/600.
- Fresh final warning workflow: run 8fac2108-0e09-492b-be31-8e41ad97b50a; NWS fetched 21:56:15 UTC at unchanged saved point, 2 actual alerts. Natural closure + unsupported Flood Watch review, policy prototype-v1/rule 1/confidence low, AQI 48 valid 21:00 UTC. Selected shift 22:11–00:11 UTC intersects warning through 22:30 (19 minutes). Active Strands: 2 models/5 successful tools, elapsed 57607.79 ms for this observation only. Manager test override 2efe6988-a638-4887-a15a-abc3319e5879; bundle hash 4b5b9b42c30069005c51bdc0c2cc963f21c61c9fefcd46bc03ea84edc56039a0. `remote-frozen-warning.json`, screenshot 09 (before decision), screenshot 10 (drafts).
- Fresh final normal workflow: run 9f0eeb64-a9f3-4660-881e-e9ffd36e2192 at unchanged KC preset; NWS empty/200, modeled AQ fetched anew. Natural normal/ready_for_manager; degraded AI ValueError with 5 tools/2 model calls. Manager approval fc569eb8-54bd-4989-b9b7-fedcc46b3896; hash a5ff2acb07cc6f8e22cf038ca0a5301995af7c2f16b7ab6ff30695907ff8bb41. `remote-frozen-approved.json`. The current failure is not described as an active AI success.
- Collecting UI previously retained the last snapshot while displaying LIVE: baseline FAILED. Fixed by clearing evidence/brief/timeline until the new snapshot exists. Verified at a real collecting state; screenshot 08. This is a correctness fix, not a data substitution.
- `remote-db-counters.json`: five acceptance evaluations, each with exactly one decision and one outbox batch despite real double-clicks; original prior decision remains. Counts are read directly from SQLite in read-only mode.
- Actual final container restart after backup `/app/data/backups/closurecall-20261010T215916Z.sqlite3`. `restart-verification.json`: all six remote historical bundles exactly equal their pre-restart baselines, including the original demo record and drafts. Browser Refresh -> Replay -> JSON export after restart matches the frozen warning record exactly. Accessible draft .eml decoded with email.parser equals the stored message and includes the no-send notice. Raw MIME line wrapping is not mistaken for missing content. `browser-verification.json`, screenshot 13.
- Layout widths: 1265 at viewport 1280, 705 at 720 (single column), 905 at default 920. No horizontal document overflow at those tested sizes; override reset to default. Full accessibility certification and a stopwatch rehearsal are still NOT VERIFIED.
- Local server was idle, backed up and restarted with the same verified source/build; `local-runtime-check.json` confirms all prior local records unchanged. Local source/model LIVE workflow was not rerun just to duplicate remote integration evidence.
- Sanitized files and configured-secret/API scans are recorded in `secret-scan-results.txt`; evidence integrity manifest in `manifest.json`. Screenshot frames are manager-desk views without credentials. No public exposure, paid provisioning, real messages or submission occurred.
