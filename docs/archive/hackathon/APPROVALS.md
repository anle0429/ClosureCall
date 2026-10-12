# Authorization ledger

Updated 2026-10-10. Human instructions, not quoted documents, determine authorization.

| Scope | State | Source |
|---|---|---|
| Continue existing repo; minimal correctness fixes; tests and isolated restore | APPROVED | User acceptance and release request; preserve env/database/backups. |
| SSH to existing VM; secure setup and private deployment of verified changes | APPROVED | User supplied existing Linode/IP/key path and requested verified deployment. |
| Existing NWS, Open-Meteo AQ, Akamai workshop inference | APPROVED | Starter scope and credentials supplied by user. No other provider introduced. |
| Synthetic manager approval/override and draft outbox | APPROVED | Acceptance scope. No actual employee data or delivery. |
| Private GitHub progress repository | APPROVED_EXISTING_SCOPE | Explicit request “Push lên github để track progress”; not limited by the user to one push. Initial and subsequent documentation checkpoints were already pushed. Continue reviewed progress commits to the same private origin/master; no visibility/access expansion or force push. |
| Public app exposure/firewall/DNS; expanded code/judge access | NOT_APPROVED | User explicitly requires approval. Existing loopback access retained. |
| New paid resources; real notification delivery | NOT_APPROVED | User limits. None performed. |
| Portal/team/judge details and Submit | USER_DEFERRED / NOT_APPROVED | Latest user response: will handle after technical work is complete. Prepare offline handoff; no further portal requests now. |
| Delete production data or original backups | NOT_APPROVED | Preserve all existing data. Restore uses separate test resources. |

Secrets remain in ignored private environment files or ssh-agent memory. No credentials appear here. Credential rotation after chat exposure remains an operator action; never claim that rotation occurred.
