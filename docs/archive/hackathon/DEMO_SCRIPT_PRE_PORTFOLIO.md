# ClosureCall — 180-second prototype demo

Use the already signed-in private browser at http://127.0.0.1:8081/. No slides. This is an English speaking script; the presenter still needs to rehearse it. Agent UI runs took 86.005 and 123.789 seconds, excluding a human spoken pitch.

Latest verified application **a5681bc** adds **Refresh time (+15 min)** below Work starts/Work ends. Use it before a fresh evaluation: start becomes device now +15 minutes in the facility timezone and end keeps a valid shift length (2h fallback). It only updates the form; click Check conditions separately. Refresh does not update a saved record or make its weather LIVE. [Current release](WORK_HOURS_REFRESH.md); the earlier precision checkpoint below retains its date and scope.

Vietnamese presenter annotations and exact branch-transition lines: [DEMO_PRESENTER_NOTES.md](DEMO_PRESENTER_NOTES.md). This is preparation, not a completed human rehearsal.

Current private release, verified 2026-10-11: production source **4dffaac**, precision design applied, authenticated main tab open at **8081**. See [release evidence](PRIVATE_DESIGN_RELEASE.md). The current UI labels below match this release. The memo download button is deployed, but downloaded-file visual/print QA is still unverified; use the verified Replay/JSON demonstration. Latest separate remote QA retrieved real NWS/AQ and all five Strands tools with zero KC alerts; do not promise an active warning.

Before presenting: confirm healthy 4dffaac runtime/tunnel, keep secrets off screen, choose the actual facility/date/timezone and a future-ending work period. Weekends require the explicitly synthetic special shift checkbox. Never reuse an old work period for a new LIVE decision. Test connectivity early; check current NWS warning validity if choosing the fixed synthetic site. Its old name “Flash Flood Warning” is historical context, not current weather. The already open saved record is REPLAY; select current work hours before clicking Check conditions.

| Time | Actual UI action | Say |
|---|---|---|
| 0–20s | Show facility and synthetic/prototype notice; select valid period. | “ClosureCall supports the duty officer and manager in reviewing evidence, documenting a decision and preparing employee drafts. These offices, people and action mappings are synthetic prototype assumptions.” |
| 20–75s | Click **Check conditions & recommendation** once. Show facility coordinates/timezone, fetched UTC, point URL, validity/alert count and modeled AQ. While Strands runs, explain source/rule facts already displayed. Open **What could change the recommendation?** and **Why this confidence level?** after the final render. | “This request fetches NWS and modeled CAMS air quality for this point and period. Empty data differs from a failed request; neither verifies power, water or security. Rules propose a candidate. Confidence is a rubric, not probability, and the model does not decide.” |
| 75–110s | If ready, **Approve recommendation**, enter short truthful review reason, then **Save decision & prepare drafts**. If unsupported/incomplete, explain that state; only use **Override recommendation** for a clearly labeled synthetic test, with explicit posture/reason. | “The manager owns approval. A Watch has no automatic mapping here. Local access is not physically verified. Closure is not evacuation and does not decide essential reporting.” |
| 110–140s | **4 Check employee drafts**, then **Read draft message** for Harper Quinn and Jordan Lake; optionally Casey Brook. Point to offsite/no-shift reasons. | “Essential staff require supervisor direction. Telework has manual follow-up; offsite and no-shift staff are excluded from urgent site instructions. These drafts can support an operator's existing notification process. No message is sent, and OnSolve integration is not implemented.” |
| 140–165s | **Open saved decisions**, **Refresh**, then **Open saved decision**; show REPLAY, collection/decision timestamps, original recommendation versus final decision/reason and **Export frozen decision package**. | “This is historical replay. The original recommendation, manager decision and reason remain separate. Evidence, rules, roster and drafts are frozen; replay calls no sources or model. This record supports explanation, not a compliance certification.” |
| 165–180s | Show tool timeline and identify private Linode runtime. End. | “One Strands agent reads five scoped tools. The app and persistent records run on Akamai Linode. ClosureCall supports the existing emergency team; local safety and real delivery remain unverified.” |

If inference is still pending at 75 seconds, say so. Switch to a stored record using Historical replay and explicitly announce its timestamp; do not pretend it is the current request. Clicking Replay stops UI polling, though the background evaluation continues. To resume that same live request afterward, reload/sign in; session storage retains the run ID. Do not click Evaluate repeatedly or fabricate progress.

If AI degrades, show its actual label and deterministic evidence. If sources are incomplete, do not call the result normal/safe. Use the existing historical degraded record for explanation, without claiming a new live failure.

Prepared records (all historical after capture):

- Natural normal/active AI: approval **2026-10-10T22:55:50.009363Z**, decision `a9cfe7dc-2336-4cde-8f55-694defe160ad`, KC source collection 22:54:46 UTC.
- Current-at-capture Flood Watch: test override **22:58:10.440131Z**, decision `16a170c1-af9b-4950-86b2-a3eecf1ad26b`, collection 22:56:36 UTC. No natural posture, unsupported_hazard/low confidence; the closure is explicitly a controlled test.
- Historical Flash Flood Warning closure candidate: decision `2efe6988-a638-4887-a15a-abc3319e5879`, collection 21:56 UTC. Warning expired **22:30 UTC October 10**. Use only as REPLAY.
- Historical degraded AI/normal: approval **21:58:29.736476Z**, decision `fc569eb8-54bd-4989-b9b7-fedcc46b3896`. This old ValueError remains stored truthfully.

Do not claim ongoing monitoring, automated follow-up, real delivery, official USDA thresholds, universal AI success, latency percentiles, safety impact or a public judging URL. Portal/team/access/Submit are handled by the user after technical handoff.

The reported USDA conversation informs positioning, not policy or endorsement. Retain Normal, Telework, Closure, Delayed arrival and Early dismissal. If asked about Wisconsin/Kansas City, say the current release includes offline synthetic regression tests for contradictory polygons and snapshot references; do not describe a live incident or universal bad-data detection. Null-geometry county/zone coverage still relies on NWS point-filter resolution. A source can be wrong while its metadata remains internally consistent.
