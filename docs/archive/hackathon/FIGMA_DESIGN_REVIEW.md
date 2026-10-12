# ClosureCall Figma proposal

Created and verified through the connected Figma MCP on 2026-10-11 UTC. This is an editable design proposal based on the existing application source `e820f0f` on `design/operations-dashboard`. It is not an application release.

- [Desktop — 1440 px](https://www.figma.com/design/3UWLj8CU622rsZJ374ZzLQ?node-id=7-257)
- [Mobile — 390 px](https://www.figma.com/design/3UWLj8CU622rsZJ374ZzLQ?node-id=7-480)
- [Reusable components](https://www.figma.com/design/3UWLj8CU622rsZJ374ZzLQ?node-id=5-28)

The original frontend screenshots, browser checks and dated tests remain in [DESIGN_REVIEW.md](DESIGN_REVIEW.md). The new proposal has screenshots and an actual Plugin API readback in [evidence/figma](../../../evidence/figma).

## Content and provenance

Source: the isolated loopback preview at port 8084, displaying the actual frozen decision `16a170c1-af9b-4950-86b2-a3eecf1ad26b`. Its facility name is preserved even though the saved alert is a **Flood Watch**, not a Flash Flood Warning. Facility and roster are synthetic. The evidence was collected October 10 at 6:56 PM EDT; it is historical, not LIVE.

Both layouts show facility identity, timezone and affected work hours separately from alert validity and source retrieval. The original unsupported-hazard / low-confidence recommendation remains separate from the recorded manager test override. The saved override reason, prototype-v1 boundary and manual deferred follow-up are visible. All twelve recipients retain their route, draft channel and relevant essential/telework/offsite/no-shift explanation. The 9/2/1 counts describe this example only.

Copy is a presentation summary of the visible historical record. No database, audit record, provider response or historical hash was edited. Figma controls are static design elements, not working API controls. The hidden manager review form, approval/override interaction states, loading/error states and keyboard behavior are not reproduced or tested in this Figma artifact; their existing frontend checks remain separate.

## Verified design checks

| Check | Actual result |
|---|---|
| Editable desktop and mobile compositions | 139 text nodes and 31 instances in each; zero image fills |
| Reusable local components | Nine: six statuses, context tile, workflow step, recipient route; editable text properties |
| Foundations | 37 local variables with explicit scopes / WEB syntax; primitive-to-semantic color aliases; six shared text styles |
| Layout readback | No empty or unstyled text; no measured horizontal overflow in either screen or component board |
| Visual review | Desktop, full mobile and component screenshots inspected; mobile evaluation-button overflow fixed; overridden decision uses amber |
| Font fidelity to existing app | **NOT MATCHED**: proposed Inter; source Segoe UI / Arial unavailable to MCP |
| Application / deployment verification in this task | No code changes; no new suite run, LIVE evaluation or remote health/deployment check |

Simple Design System buttons and fields are instantiated, not flattened. Its text/spacing values were copied into local styles and variables because imported style/variable handles did not persist across MCP calls. The additional `--cc-*` WEB syntax names describe proposal tokens; they are not claimed to exist in current CSS.

## Remaining limits

The Starter plan rejected the final MCP call that would rename the page and remove temporary capture frame `3:2`. That reference remains in the file; it is not one of the final linked screens. Captured native form selection state did not serialize faithfully, so that reference must not be used as a record or final UI proposal. The final semantic layouts show the correct saved facility and special shift. No upgrade was purchased. Further MCP edits require restored quota or user-owned plan changes.

The direct desktop link was opened in the in-app browser and the actual canvas was visibly verified at 50% zoom; screenshot `browser-file.jpg`. That browser surface is an anonymous view and cannot edit without signing in. MCP account authentication and canvas writes were separately verified. Default Figma link-sharing/access settings were not verified; no sharing settings were changed. The file contains only synthetic roster/site and public historical weather content, no credentials.

The long mobile canvas reflects the existing single-page workflow and full roster; it is not an interactive or paginated prototype. Native field values may truncate within the field; the full facility name remains visible in the context tile. Contrast certification, interactive Figma prototype behavior and exact Segoe UI fidelity are not verified.

Review this proposal before implementation. The existing backend, contracts, authorization, deterministic rules, one Strands agent and frozen audit data remain the implementation constraints. Deployment of any frontend candidate still requires explicit approval, exact Linux verification and a current production backup.
