# Attribution inventory

Prepared for the offline submission handoff. This is an inventory of observed data/SDK/distribution metadata, not a complete licensing review or selection of a license for ClosureCall. Portal-specific requirements and team attestations remain unknown/user-owned.

| Component | Observed use / source |
|---|---|
| National Weather Service / NOAA | Actual public NWS point alert responses. Source URL, fetch time, alert ID, validity and applicable work window are frozen in each record; old alerts are historical after capture. |
| Open-Meteo / CAMS | Same-point modeled AQ. The application displays Open-Meteo / Copernicus Atmosphere Monitoring Service attribution, valid time and returned grid coordinates; no indoor sensor claim. |
| Strands Agents SDK | One strands-agents 1.59.0 agent; five scoped read-only tools. Model reference/focus selection is validated; factual text is rendered from frozen records. |
| Akamai | Existing Linode application hosting and approved workshop inference endpoint using hackathon-chat alias. Alias does not establish the underlying model vendor/version. |
| ClosureCall | Existing project code continued in place. Synthetic facilities/people/shifts; prototype policy mappings. No organization endorsement or contribution attribution inferred from account names. |

Direct distribution metadata inspected in the existing Windows environment (`importlib.metadata`), matching direct pinned versions; captured in `evidence/release-followup/distribution-metadata.json`. These labels describe the installed distributions; transitive dependencies and all notices have not been audited here.

| Distribution | Version | Metadata license field |
|---|---|---|
| fastapi | 0.143.0 | MIT |
| uvicorn | 0.54.0 | BSD-3-Clause |
| httpx | 0.28.1 | BSD-3-Clause |
| pydantic | 2.14.0 | MIT |
| python-dotenv | 1.2.4 | BSD-3-Clause |
| strands-agents | 1.59.0 | Apache-2.0 |
| tzdata | 2026.5 | Apache-2.0 |
| shapely | 2.2.0 | BSD-3-Clause |

No ClosureCall LICENSE/NOTICE file was found in the tracked project at this audit. No new project license was assigned. Team/member contributions and any required licensing/terms confirmation must be entered by the user using the actual organizer form. Existing package license/notice files remain in their distributions; they were not removed or modified.
