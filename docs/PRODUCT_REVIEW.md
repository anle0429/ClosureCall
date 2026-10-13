# Product and engineering review

Reviewed October 13, 2026. Scope: existing application source `3bc1ddd`, repository checkpoint `7767b0a`, one test-only correction and documentation improvements. No application behavior, provider, policy, framework, deployment or production data changed.

## Verdict

ClosureCall is a usable, testable prototype with a complete evidence → recommendation → manager decision → recipient draft → historical record workflow. It is suitable for a technical portfolio review and a supervised synthetic demo. It is **not ready for unsupervised operations with real employees**.

There is no meaningful completion percentage for these different boundaries. A working prototype, a maintainable repository and an operational government service require different evidence. Test totals do not establish live availability, policy acceptance, accessibility certification or delivery.

## What is supported

| Area | Assessment and evidence | Remaining boundary |
| --- | --- | --- |
| Decision workflow | Deterministic assessment, explicit approval/override, idempotency and atomic decision/outbox transaction; API/approval/recipient tests | Offices and roster are synthetic; supervisor procedures and action thresholds are prototype assumptions |
| Agent authority | One Strands agent, five scoped read-only tools, strict reference/output validation and bounded subprocess; SDK loop tested with a synthetic model | Workshop inference availability after the event is not newly verified; no approval/sending tool |
| History | Immutable snapshot/result/decision/outbox tables and frozen-body hash checks; replay/memo tests; October 12 exact-image nine-record restore/restart evidence | A privileged host operator is outside the integrity guarantee; no retention/compliance certification |
| Evidence quality | Location, supplied polygons, time overlap, cancellation/reference boundaries and missing-source distinctions have regression coverage | Null geometry relies on NWS point filtering; internally consistent incorrect metadata can evade checks; local safety is not physically verified |
| Repository quality | Pinned runtime/development requirements, modular Python services, readable static source, architecture/contributor/security docs and dated evidence | Cross-layer payloads use dictionaries; global store/job state and the 988-line frontend need care as scope grows; browser coverage is largely recorded manual QA |
| Reproducibility | October 13: 93 Windows tests from an isolated tracked-source export without local env/DB/keys; 93 against the existing exact Linux image | Uses the existing dependency environment, not a fresh package install. GitHub Actions is manual-only and has not been run |
| Private hosting | Fresh read-only SSH observation: a5681bc/image9ab42b0 healthy, non-root/read-only/loopback, same container start | Candidate is not deployed; manager Basic auth/shared operator identity is not enterprise identity or public-service access control |

Relevant source: [API/auth](../app/main.py), [manager gate](../app/auth.py), [decisions](../app/services/decisions.py), [store](../app/db.py), [worker budget](../app/jobs.py), [agent factory](../app/agent/factory.py), [tool scope](../app/agent/tools.py), [strict requests](../app/schemas.py). [Boundary test map and dated browser/restore evidence](VERIFICATION.md).

## Changes made in this review

- Removed a conditional provider test that could execute no assertion when an operator's real inference key was configured. It now always checks empty key, placeholder key and an unapproved endpoint with synthetic configuration. No endpoint was contacted and production allowlisting is unchanged.
- Added a product-status assessment to the README, made environment invocation explicit and kept engineering controls separate from readiness claims.
- Replaced stale GitHub handoff instructions with one current workflow; preserved the October 10 account of the original push in the historical archive.
- Kept old evidence, failures and source/image identities intact. New review evidence is separate under `evidence/product-review-20261013`.

## Priorities after this review

| Priority | Work before the next stage | Acceptance |
| --- | --- | --- |
| 1 — Sustained demo use | Confirm an authorized post-event inference configuration; keep degraded behavior explicit | An actual, labeled integration smoke with recorded source/model timestamps and no secret exposure; no silent provider switch |
| 2 — Publication | Confirm team credit, ownership/license and the exact code-access scope | Owner-approved license/credits and repository visibility; no invented authorship or government endorsement |
| 3 — Maintenance | Add repeatable browser checks when changing the UI; use module extraction only when a concrete feature needs it | Evaluate/review/approve/override/download/replay, refresh, busy/errors and narrow layout covered without provider calls or production data |
| 4 — Real-user pilot | Define policy owners, per-user authority, audit/retention/access requirements and expected load | Requirements and authorized threat/operational review, not just a larger test total; one shared manager and one worker remain current limits |
| 5 — Delivery | Specify a separate draft-to-send adapter and supervisor/deferred handling if requested | Approved transport, consent/channel semantics, idempotency, delivery failure/receipt testing; current app still sends nothing |

These are proposed next-stage work, not features added or implied approvals. No broad refactor, framework migration, automatic CI/deployment, real notification or public access was introduced. Reviewed checkpoint 2ba6096 was pushed to private master and the review branch by fast-forward; [push proof](../evidence/product-review-20261013/push-checkpoint.json).

## Fresh checks and disclosures

- [Windows source-export suite](../evidence/product-review-20261013/clean-checkout-windows.txt): **93 passed in 11.26s**.
- [Linux candidate-image suite](../evidence/product-review-20261013/linux-existing-candidate.txt): **93 passed in 9.24s**, against image `sha256:5fdf4901dc2d30bde0558edf5a1520021145bdce7b3a7fcbd8c5ca5c280c76e8`, with current tests mounted read-only.
- [Checkout scope](../evidence/product-review-20261013/checkout-scope.json): original local environment/data/keys not copied; source application unchanged, test overlay recorded.
- [Fresh private runtime observation](../evidence/product-review-20261013/runtime-read.txt) and [GitHub visibility](../evidence/product-review-20261013/github.json). Health is not a new end-to-end weather/model evaluation.
- Python formatting, frontend formatting and dependency consistency passed; no fresh browser, live provider, print or human pitch rehearsal is claimed in this review.

Each change should identify the problem, explain how the implementation preserves the existing boundaries, and include reproducible verification. The existing application can be built and tested independently of a coding-assistant session.
