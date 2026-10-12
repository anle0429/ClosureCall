# ClosureCall — 180-second walkthrough

This English speaking script is preparation, not a completed human rehearsal. Candidate **3bc1ddd** runs locally at `http://127.0.0.1:8084/` as isolated QA: new evaluations are explicitly synthetic, providers are blocked and AI is unavailable. Private Linode remains **a5681bc**. [Verification](VERIFICATION.md), [access/recovery](DEMO_RECOVERY.md).

Sign in before sharing the screen; keep credentials off screen. Use the workbench without slides. The saved Watch record has a manager test override, not a natural closure recommendation. The synthetic site's old name is not current weather.

| Time | Action | Say |
| --- | --- | --- |
| 0–20s | Show facility, coordinates, timezone and prototype notice. Choose work hours; click **Refresh time (+15 min)** if needed. | “ClosureCall helps a manager review evidence, document a decision and prepare employee drafts. These offices, staff and action mappings are synthetic prototype assumptions.” |
| 20–65s | Click **Check conditions & recommendation** once. Read source timing, applicability and missing inputs; open **Why this confidence level?** | On 8084: “This isolated walkthrough calls no weather provider or model.” For a separately authorized actual run: “NWS alerts and modeled CAMS air quality are checked for this site and period. Empty alerts differ from failed data. Neither verifies local building safety.” |
| 65–105s | Read the original posture. Choose **Approve recommendation**, enter a truthful reason, click **Approve recommendation & prepare drafts**. Alternatively select **Override recommendation**, a posture and explicit test reason, then click **Save override & prepare drafts**. | “Rules propose a candidate. Confidence describes evidence completeness/applicability, not safety probability. The manager owns approval. This override is a synthetic test, not an operating determination.” |
| 105–140s | **4 Check employee drafts**; **Read draft message** for essential staff and the teleworker. Point to offsite/no-shift exclusions and Casey's accessible voice draft. | “Each person has a route and a reason. Essential reporting follows supervisor direction; telework follow-up is manual. Channels describe drafts. Nothing is sent.” |
| 140–170s | **Saved decisions**, **Refresh**, **Open saved decision**. Show REPLAY, original recommendation versus final decision, timestamp/reason, **Export frozen decision package**, **Download decision memo (HTML)**. | “This reopens the original evidence, policy, roster and drafts. It does not fetch weather or regenerate history. The memo presents this saved record.” |
| 170–180s | **Evidence & tool details**; distinguish local QA from private deployment. | “The deployed app uses one Strands agent with five scoped read-only tools on Akamai Linode. This local QA run did not invoke Strands. The prototype supports the emergency team.” |

The table is a speaking budget, not a measured human run. Agent UI observations: approve 153.088s and override 59.332s, including automation/observation waits; neither is inference latency or spoken-pitch performance. [Approve evidence](../evidence/portfolio/ui-rehearsal-approve.json), [override](../evidence/portfolio/ui-rehearsal-override.json). Human speech and actual printing remain unverified.

## Fallback

- Zero alerts: show the available empty feed; never call it “all clear.”
- Unsupported hazard: explain no automatic posture, low confidence and manager judgment. Test overrides must be labeled.
- Slow/unavailable AI or sources: read the actual state. At 65s, open a saved decision and announce its capture time. Replay stops UI polling while an existing background job may continue; avoid duplicate evaluations. Reload/sign in to resume that run when appropriate.
- Network unavailable: use labeled local QA/historical evidence. It is not a new LIVE result or proof of current conditions.

Prepared historical records: natural normal/active-AI approval `a9cfe7dc-2336-4cde-8f55-694defe160ad` (collection 2026-10-10T22:54:46Z); unsupported Flood Watch/test closure override `16a170c1-af9b-4950-86b2-a3eecf1ad26b` (collection 22:56:36Z). Earlier warning records expired on October 10. All are REPLAY now.

Do not promise official policy/endorsement, OnSolve integration, monitoring, delivery, measured impact, public access or a submission receipt. [Vietnamese notes](DEMO_PRESENTER_NOTES.md), [Q&A](PITCH_QA.md).
