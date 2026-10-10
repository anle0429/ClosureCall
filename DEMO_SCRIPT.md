# ClosureCall — 180-second prototype demo

Use the already signed-in private browser at http://127.0.0.1:8081/. No slides. This is an English speaking script; the presenter still needs to rehearse it. Agent UI runs took 86.005 and 123.789 seconds, excluding a human spoken pitch.

Before presenting: confirm healthy e5f7801 runtime/tunnel, keep secrets off screen, choose the actual facility/date/timezone and a future-ending work period. Weekends require the explicitly synthetic special shift checkbox. Never reuse an old work period for a new LIVE decision. Test connectivity early; check current NWS warning validity if choosing the fixed synthetic site. Its old name “Flash Flood Warning” is historical context, not current weather.

| Time | Actual UI action | Say |
|---|---|---|
| 0–20s | Show facility and synthetic/prototype notice; select valid period. | “ClosureCall turns evidence into a human operating decision, tailored employee drafts and an exact historical record. These offices and people are synthetic; our action mappings are prototype assumptions.” |
| 20–75s | Click **Collect live evidence & evaluate** once. Show fetched UTC, point URL, validity/alert count and modeled AQ. While Strands runs, explain source/rule facts already displayed. Open **What would change this** and **Assumptions & confidence basis** after the final render. | “This request fetches NWS and modeled CAMS air quality for this point and period. An empty available feed differs from a failed feed. The policy proposes a candidate; confidence is a rubric, not probability. The model is bounded and does not decide.” |
| 75–110s | If ready, **Approve recommendation**, enter short truthful review reason, then **Record decision & prepare demo outbox**. If unsupported/incomplete, explain that state; only use **Override with reason** for a clearly labeled synthetic test, with explicit posture/reason. | “The manager owns approval. A Watch has no automatic mapping here. Local access is not physically verified. Closure is not evacuation and does not decide essential reporting.” |
| 110–140s | Open **Review recipient draft** for Harper Quinn and Jordan Lake; optionally Casey Brook. Point to offsite/no-shift reasons. | “Essential staff require supervisor direction. Telework gets an informational draft with manual follow-up. Offsite and no-shift staff are excluded from urgent site instructions. These channel labels are drafts; no email, SMS or call is sent.” |
| 140–165s | **Refresh**, choose a historical **Replay**, show collection/decision timestamps and **Export frozen decision package**. | “This is REPLAY of the decision at its recorded time. Evidence, rules, roster, AI selection and drafts are frozen; sources and model are not called again. Separate-container restore preserved six bundles after changing current roster/rules.” |
| 165–180s | Show tool timeline and identify private Linode runtime. End. | “One Strands agent reads five scoped tools and selects validated references. The app and persistent data run on Akamai Linode. We have tested the workflow; official policy approval, real delivery and judge access remain outside this prototype.” |

If inference is still pending at 75 seconds, say so. Switch to a stored record using Historical replay and explicitly announce its timestamp; do not pretend it is the current request. Clicking Replay stops UI polling, though the background evaluation continues. To resume that same live request afterward, reload/sign in; session storage retains the run ID. Do not click Evaluate repeatedly or fabricate progress.

If AI degrades, show its actual label and deterministic evidence. If sources are incomplete, do not call the result normal/safe. Use the existing historical degraded record for explanation, without claiming a new live failure.

Prepared records (all historical after capture):

- Natural normal/active AI: approval **2026-10-10T22:55:50.009363Z**, decision `a9cfe7dc-2336-4cde-8f55-694defe160ad`, KC source collection 22:54:46 UTC.
- Current-at-capture Flood Watch: test override **22:58:10.440131Z**, decision `16a170c1-af9b-4950-86b2-a3eecf1ad26b`, collection 22:56:36 UTC. No natural posture, unsupported_hazard/low confidence; the closure is explicitly a controlled test.
- Historical Flash Flood Warning closure candidate: decision `2efe6988-a638-4887-a15a-abc3319e5879`, collection 21:56 UTC. Warning expired **22:30 UTC October 10**. Use only as REPLAY.
- Historical degraded AI/normal: approval **21:58:29.736476Z**, decision `fc569eb8-54bd-4989-b9b7-fedcc46b3896`. This old ValueError remains stored truthfully.

Do not claim ongoing monitoring, automated follow-up, real delivery, official USDA thresholds, universal AI success, latency percentiles, safety impact or a public judging URL. Portal/team/access/Submit are handled by the user after technical handoff.
