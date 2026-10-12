# ClosureCall — review packet draft

Status: **PREP_COMPLETE_PENDING_EXTERNAL / ON_HOLD / NOT_SUBMITTED**. Purpose: post-hackathon portfolio preparation under the user's latest instruction. No organizer extension, retrospective submission, portal write, public code access or social publication is claimed.

## Project copy

**Title:** ClosureCall

**Tagline:** Evidence, a manager decision, and a record you can explain.

**Short description:** ClosureCall helps facility managers review weather and modeled air-quality evidence for a specific site and work period, record a human operating decision, prepare recipient-specific drafts, and reopen the original decision record.

**Long description:** One FastAPI service collects NWS point alerts and Open-Meteo/CAMS modeled air quality. Deterministic prototype rules determine supported candidate postures and disclose missing inputs, applicability, threshold matches and confidence basis. One Strands agent reads five tools scoped to the frozen evaluation; it cannot approve, change policy or send notifications. The manager approves or records an explicit reasoned override. A twelve-person synthetic roster produces explained included/excluded/deferred routes and unsent drafts. SQLite preserves the evidence, policy, roster, AI trace, manager decision and drafts for historical replay without fresh source/model calls. A standalone decision memo is a presentation of this frozen record, not a new decision.

## Verified source and private access

- Running private application: `a5681bcd98400fd75d02670f378a04365459dd7e`.
- Image: `sha256:9ab42b0dcdfaee241b3d9156ac5433ecd0da772f29707ec6cb397664f0256b90`, observed through authorized SSH; no registry publication.
- Repository base: `d3ea87e`; current portfolio work is a **separate undeployed candidate**, not that runtime.
- Original data: 13 runs / 9 decisions, verified read-only at R0. No current-data write or restore.
- Undeployed portfolio candidate: `3bc1ddd8cbfe14148fa8a1c8c4c2febb9253fa24`, exact image `sha256:5fdf4901dc2d30bde0558edf5a1520021145bdce7b3a7fcbd8c5ca5c280c76e8`. New full results: 91 Windows/10.85s and 91 exact Linux/7.43s; same suite in two environments.

## Sponsor mapping

| Context | Implemented evidence | Limits |
| --- | --- | --- |
| USDA Closure Call challenge | Real recorded NWS point retrieval, modeled AQ, disclosed rules, manager authority, per-person drafts and frozen replay | Synthetic offices/people; prototype assumptions, no endorsement or verified local building safety |
| AWS Strands Agents SDK | One actual Strands 1.59.0 agent, five scoped read-only tools; dated real tool traces | No Bedrock claim; model alias does not identify its undisclosed backing model; AI may degrade |
| Akamai Cloud | Existing Ubuntu Linode runs containerized app and persistent records; current SSH identity/health observed | Private SSH access only, not a public product or judge URL |

## Access and remaining publication fields

The existing repository is private (`https://github.com/anle0429/ClosureCall`). Same-private-remote progress is authorized. Localhost/SSH addresses are operator access, not shareable remote demo URLs. Candidate deployment, public visibility/access, social publication, license and team publication rights require the user's separate decision. Registered team/members/tracks, organizer form limits, eligibility, accepted terms and receipt remain **NOT VERIFIED / USER-OWNED**; do not fill them automatically.

All notifications are drafts; deferred follow-up is manual. No OnSolve integration, power/water/security feed, real delivery, federal policy certification, measured impact or guaranteed AI reliability. All old warning/Watch examples are historical after capture. Fresh KC zero-alert proof is dated evidence, not current LIVE weather.

## Local review assets

- [Current verification and retained failures](docs/VERIFICATION.md), [limitations](docs/LIMITATIONS.md), [release identity](RELEASE_MANIFEST.json).
- [Desktop](evidence/portfolio/after-desktop.jpg), [narrow](evidence/portfolio/after-mobile.jpg), [before desktop](evidence/portfolio/before-desktop.jpg), [before narrow](evidence/portfolio/before-mobile.jpg). Historical replay; no LIVE label.
- [Frozen memo-v2 example](evidence/portfolio/memo-after.html), [before](evidence/portfolio/memo-before.html), [memo visual](evidence/portfolio/memo-after-desktop.jpg). Generated from dated public/synthetic frozen evidence, not new source data. Actual print remains unverified.
- [180-second demo/fallback](docs/DEMO_SCRIPT.md), [Vietnamese presenter notes](docs/DEMO_PRESENTER_NOTES.md), [recovery](docs/DEMO_RECOVERY.md), [Q&A](docs/PITCH_QA.md).
- [LinkedIn draft](docs/LINKEDIN_DRAFT.md), [architecture](docs/ARCHITECTURE.md), [sources](docs/SOURCES.md), [attributions](docs/ATTRIBUTIONS.md).

The packet is this local index plus referenced source/evidence/assets; nothing has been uploaded or posted. Test downloads are explicitly synthetic. Historical live integration remains dated. Do not distribute env, databases/backups, keys, manager credentials or raw provider errors. Repository/private packet history scan scope and checksums are in evidence/portfolio; a scan is not a guarantee of every possible secret. Read before approving public access.

Private progress: documentation/evidence checkpoint `e8bb341` pushed to `maintenance/portfolio-readiness`; master preserved. [Private branch](https://github.com/anle0429/ClosureCall/tree/maintenance/portfolio-readiness). This is not public judge access, an external publication or a deployment.
