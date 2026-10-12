# LinkedIn draft — not posted

This copy is prepared locally for the user's review. Confirm team contributions, publication rights and the chosen code-access link before posting. No award, government endorsement or measurable impact is claimed.

---

I've been working on ClosureCall, a decision-support prototype for facility managers reviewing disruptive weather and operating conditions.

The workflow starts with a specific site and work period: NWS alerts and modeled air-quality evidence, an explicit rules assessment, a manager approval or reasoned override, recipient-specific notification drafts, and a frozen decision record that can be reopened later.

The engineering question I found most useful was where to put authority. ClosureCall uses one AWS Strands Agents SDK agent with five read-only tools to review frozen evidence. Deterministic services control the candidate posture and recipient routing; the manager makes the decision. The model has no approval or sending tool.

The app runs on Akamai Linode with persistent SQLite records. Historical replay keeps the evidence, policy, roster, recommendation, human reason and draft messages from the original decision. Reopening a record does not call current weather APIs or regenerate the past with a model.

This project grew from the USDA Closure Call challenge. It is an independent prototype: synthetic offices and staff, prototype policy mappings, modeled air quality and unsent drafts. It does not verify local building safety or replace an emergency team.

The part I'm continuing to refine is explainability in the workbench: making source applicability, missing information and the human decision easy to inspect.

[Add the approved repository/demo link and team credits here.]

#DecisionSupport #StrandsAgents #Akamai
