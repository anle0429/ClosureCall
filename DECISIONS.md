# Technical decisions

## Product boundary

- Preserve Python/FastAPI/static HTML/CSS/JS/SQLite, one process/worker and one Strands agent. Deterministic services own posture/routing; the manager owns approval. No notification transport, map, new agent, SSO or framework added.
- Keep source provenance, applicability, time and uncertainty explicit. Prototype mappings/confidence are not USDA/OPM policy or probability. Replay preserves the original policy/roster/decision/drafts rather than applying current bindings.

## Post-hackathon portfolio pass

- The user's latest instruction authorizes portfolio work after the historical competition cutoff. Preserve competition-era evidence and running source; a new candidate is undeployed until specifically approved. No implied extension, public access, social post or retrospective submission.
- Use one current README/document index and move dated reports to an archive. Preserve original evidence/test exports and exact pre-portfolio checkpoint copies; rebase active Markdown links. Keep GOAL_PROGRESS and RELEASE_MANIFEST as canonical ledgers.
- Standardize source with pinned developer formatters. Compare Python/JS syntax trees and control contracts; preserve runtime dependencies, policies and authority. Do not treat large formatting diffs as logic changes or new capabilities.
- Make memo facility/work-period information precede technical hashes, align its restrained palette with the workbench and version the presentation separately (frozen-memo-v2). Do not change frozen record values, missing-field behavior, source/model calls or draft state.
- The original 0.2s timeout test conflated trace availability with startup scheduling. Observe a real ready worker for the trace assertion, keep the .2s budget, add a no-output termination case and assert real process exit. Preserve all failure logs; original incident timing remains unknown. No production deadline change.
- The GitHub verification workflow is manual-only and has not been dispatched; private progress pushes trigger no hosted runner use or deployment. Public repository/license/team credits/social publication are separate decisions.

Historical decisions: docs/archive/hackathon/DECISIONS_PRE_PORTFOLIO.md.

## Final portfolio gates

- Facility-local work start determines weekend validation. A near-midnight test looked at today's date instead; fix only the test clock and cover both Sunday/Monday outcomes. Equivalent timestamp strings are compared as parsed instants. Keep the original failure logs.
- Keep the final source candidate 3bc1ddd distinct from documentation commits and unchanged runtime a5681bc. Verify actual image content because this Dockerfile has no source label; no registry publication is inferred from a local engine RepoDigest.
- A read-only QA container refused copying verification files; use read-only mounts at startup without weakening protections. Restore only the existing backup into a separate network-disabled volume, then stop QA containers. Original DB/backup/env remain untouched.
- Keep memo printing and human speech explicitly unverified when the browser cannot expose a print destination. Normal loopback preview of a newly generated frozen memo does not retry/bypass the earlier blocked file URL.
