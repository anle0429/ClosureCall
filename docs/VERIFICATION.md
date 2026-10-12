# Verification

This page records scope, not a blanket challenge PASS. The release manifest separates the current private runtime from an undeployed portfolio candidate and from documentation checkpoints.

## Current pass

- R0 fresh SSH observation: source a5681bc / image 9ab42b0..., healthy, unchanged 2026-10-11 11:45:50 UTC start, private loopback/non-root/read-only. `evidence/portfolio/runtime-r0.txt`.
- Read-only original data: 2 facilities, 13 runs, 9 decisions/outbox; integrity OK and no active job. `production-r0.json`. No restart, config change or original-data write.
- GitHub metadata freshly confirmed the existing repository is private. `github-metadata.json`. No access/visibility change or hosted workflow dispatch.
- Controlled delayed startup: a 0.2s deadline can correctly kill before any trace, observed at about 0.22s. `deadline-controlled-startup.json`. The exact timing of the old failure remains unknown.
- Timeout tests now separately cover termination without a trace and trace retention after a real worker is ready. The 0.2s budget and original trace assertion remain; actual process termination is also asserted. Targeted final result: 2 passed. The initial Windows CRLF fixture assertion failure is retained, then checked by parsed JSON without altering production logic.
- Six memo boundary tests passed after the presentation update. Frozen record data and no-source/model/recompute traps remain covered.
- Formatting checks: all 47 Python syntax trees exact before/after the formatter; JavaScript syntax tree exact after excluding source-position metadata; all 63 HTML IDs and control contracts preserved. Only memo presentation changes the runtime Python AST from d3ea87e. `python-format-semantics.json`, `js-format-semantics.json`, `protected-contracts.json`.

Final source **3bc1ddd8cbfe14148fa8a1c8c4c2febb9253fa24** is undeployed. Windows: **91 passed in 10.85s** ([log](../evidence/portfolio/windows-source-final.txt)); exact Linux image `sha256:5fdf4901dc2d30bde0558edf5a1520021145bdce7b3a7fcbd8c5ca5c280c76e8`: **91 passed in 7.43s** ([log](../evidence/portfolio/linux-source-final.txt), [identity](../evidence/portfolio/runtime-final.txt)). These are the same 91 cases on two environments. The post-test label lookup failed because the Dockerfile has no labels; independent final inspection and restore pin the image. No test rerun was needed for that metadata failure.

## Browser, memo and integrity gates

- Local 8084 QA: approve and reasoned override, loading/busy/double-click checks, recipient drafts, history refresh/reload, authenticated JSON/HTML downloads. Exactly two new runs/two decisions; original QA nine decisions unchanged. [Approve](../evidence/portfolio/ui-rehearsal-approve.json), [override](../evidence/portfolio/ui-rehearsal-override.json), [download/data proof](../evidence/portfolio/final-data-check.json). These were synthetic with zero provider/model calls, not new live integration evidence. The empty-reason attempt's response text was not captured; regression tests verify API rejection independently.
- **Refresh time (+15 min)** set start to device now +15 minutes in facility timezone, preserved the 120-minute shift and left replay/export/history unchanged. [Observed proof](../evidence/portfolio/work-hours-refresh.json). It updates only the form.
- Selected-tab checks at 1440×900, 1280×800, 768×1024 and 390×844: no horizontal overflow, twelve recipients and 23px draft pills. [Geometry](../evidence/portfolio/responsive-final.json). Before/after screenshots are in evidence/portfolio. Formatting preserved the workbench appearance; a targeted alignment fix stopped long follow-up rows stretching draft pills. Memo-v2 puts facility/work period before technical identity and uses the same restrained palette. [Data preservation](../evidence/portfolio/memo-data-preserved.json), [visual scope](../evidence/portfolio/memo-visual.json).
- A newly generated frozen memo was visually reviewed through normal loopback HTTP, desktop/narrow. Authenticated downloads matched API bytes. Ctrl+P exposed no print destination in this browser: **actual print/pagination NOT VERIFIED** ([attempt](../evidence/portfolio/memo-print-attempt.jpg)). The previously blocked file URL was not retried/bypassed.
- Existing nine-record backup restored into a separate volume with the exact candidate image, network disabled and no inference key/published port. All nine HTTP replay/export/outbox/memo records matched before/after an actual QA restart; in-memory current rules/roster changed and forbidden-source/model/recompute traps stayed at zero. Six restored table fingerprints matched. [Successful drill](../evidence/portfolio/restore-final-verified.txt), [initial read-only-copy refusal](../evidence/portfolio/restore-final.txt). Original data was not restored.
- Fresh final production probe matched all six tables/nine body hashes against R0. Original private runtime remains healthy with the same source/image/start. [Data](../evidence/portfolio/final-data-check.json), [runtime](../evidence/portfolio/runtime-final.txt).

## Retained failures and corrections

An initial full Windows suite passed (90/11.41s), then both Windows and Linux failed near Sunday midnight: an old test checked today's weekday although start +10 minutes was Monday. Production correctly validated the facility-local work start. Tests now fix time and cover Sunday-rejected/Monday-accepted boundaries without changing validation. [Windows failure](../evidence/portfolio/windows-final-after-badge.txt), [Linux failure](../evidence/portfolio/linux-exact-candidate.txt), [targeted pass](../evidence/portfolio/work-day-targeted.txt). The first new assertion compared equivalent Z/+00:00 strings and failed; it now compares parsed instants. Deadline startup/CRLF findings remain separately recorded above. No deadline was extended, assertion skipped or process budget relaxed.

Verdict: **ACCEPTABLE_WITH_LIMITATIONS** for local/private prototype review. This is not government production-readiness, deployment approval or an all-challenge PASS. Fresh live-warning/high-wind/high-AQ, post-event hosted inference, human speech, actual print and external access/submission remain unverified. No hosted CI was dispatched.

## Boundary coverage map

| Boundary | Relevant checks |
| --- | --- |
| Geography, null geometry, time overlap/expiry, cancellation scope | [Feedback scope](../tests/test_feedback_scope.py), [sources](../tests/test_sources.py), [policy](../tests/test_policy.py) |
| Scoped references, tool/model budgets, degraded output and process termination | [Agent](../tests/test_agent.py) |
| Manager auth, stale/superseded decisions, override reason, idempotency | [API](../tests/test_api.py), [approval](../tests/test_approval.py) |
| Synthetic roster, essential/telework/offsite/no-shift/accessibility routes | [Recipients](../tests/test_recipients.py) |
| Frozen replay, changed bindings, escaping, missing memo fields, no recomputation | [Audit](../tests/test_audit.py), [memo](../tests/test_memo.py) |
| Secret handling | [Secret scan](../tests/test_secret_scan.py), [scanner](../scripts/check_secrets.py) |

## Historical evidence

Recorded real NWS/AQ and Strands calls on Linode are in `evidence/release` and `evidence/precision-release`; each retains its source and capture time. The KC empty feed was valid, not a failed request. Saved Flood Watch/warning records are historical; their test override is not a natural closure recommendation or physical safety verification.

Original restore/restart evidence and failed/flaky logs remain under `evidence/`. [Archived acceptance](archive/hackathon/ACCEPTANCE_REPORT.md), [feedback review](archive/hackathon/SPONSOR_FEEDBACK_REVIEW.md) and [restore drill](archive/hackathon/RESTORE_DRILL.md) describe their exact old scope. A previous restore does not prove a new image was restored. Existing human spoken rehearsal and current live-warning/high-wind/high-AQ branches are not inferred from unit tests.
