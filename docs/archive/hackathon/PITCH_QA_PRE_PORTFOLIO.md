# Pitch questions

- **Does this replace OnSolve or the emergency team?** No integration or import compatibility has been implemented/tested. ClosureCall supports a duty officer/manager's evidence review, decision documentation and draft preparation within an existing process; it does not provide a staffed 24/7 service.
- **Could Wisconsin data be treated as Kansas City evidence?** Current snapshot references and request-location checks already exist. Undeployed candidate 656e8a0 adds offline-tested supplied-polygon checks and conservative unknown-scope handling. Those fixtures are not a live incident; point-filtered null-geometry county/zone data and internally consistent upstream errors retain disclosed limits.
- **What does the memo show?** Original recommendation separately from final decision, facility/work period/timezone, recorded actor/time/reason, saved evidence/basis/limits, decision ID/hash and unsent drafts. Candidate renderer frozen-memo-v1 presents stored records without source/model/recompute calls. Production still uses Replay/JSON export; the candidate is not deployed and downloaded-file visual inspection is unverified.

- **What does the agent do?** One Strands agent reads five frozen tools and selects scoped evidence references/review focus. Validated facts are rendered from stored data. Deterministic rules propose a candidate; the human manager decides. The agent cannot approve or send.
- **What if AI fails?** Keep available deterministic evidence and show AI degraded/unavailable. Never substitute a historical successful AI response into a new run. Missing source evidence requires human review, not an inferred safe normal result.
- **Zero alerts versus missing data?** HTTP 200 with an empty NWS feed is a valid observed empty feed. Failed/malformed retrieval is unavailable. Neither proves local safety.
- **Why no automatic closure for Flood Watch?** It is outside the prototype action mappings; current run has no candidate and low confidence. A manager test override is labeled as a synthetic rehearsal, not a validated operating decision.
- **Why separate essential staff?** Closure does not establish essential reporting or evacuation instructions. Designated supervisor/local procedures control those instructions.
- **What does deferred mean?** Telework staff get an informational draft and an explicit manual supervisor review before shift/immediately if ongoing. Reassignment onsite needs re-evaluation and a new human decision. No scheduled follow-up runs automatically.
- **Are messages delivered?** No. queued_demo and channel labels describe drafts only. Accessible voice is a preference label, not a call.
- **Is AQ measured indoors?** No. Open-Meteo/CAMS is a modeled grid estimate with source, valid time and returned grid coordinates.
- **Are thresholds USDA policy?** No. Category references and prototype action mappings are separately disclosed; no USDA/OPM endorsement or operational approval.
- **Is history tamper-proof?** No. Frozen bundles, hashes and immutable SQLite tables detect ordinary changes and reconstruct records. A privileged host administrator remains outside that guarantee.
- **What runs on Akamai?** The actual FastAPI app and persistent SQLite volume run in Docker on the existing Chicago Linode. Hosted inference uses workshop alias hackathon-chat; underlying model vendor/version is not verified by the alias.
- **Is it public/submitted?** No. Operator access is a private SSH tunnel and GitHub is private. User will arrange permitted judge access and Submit. No receipt exists.
