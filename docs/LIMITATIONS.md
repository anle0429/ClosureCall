# Limitations

ClosureCall is an independent prototype for synthetic offices and staff. It is not an official USDA product, a federal closure policy implementation or a government compliance certification.

- NWS point filtering supplies coverage for alerts without usable geometry; there is no independent zone-boundary database. Source metadata that is internally consistent but wrong can evade checks. A point/period match does not physically verify local conditions.
- Empty available alerts differ from failed/unverified inputs. Neither proves power, water, security, travel or building safety. Unsupported hazards require human review.
- Open-Meteo/CAMS air quality is a modeled grid estimate, not an indoor sensor. Model valid time and retrieval time have different meanings.
- Operating mappings, freshness budgets and confidence are prototype assumptions. Confidence is an evidence-completeness/applicability rubric, not a probability or guarantee. Delay/dismissal need human timing/basis.
- All messages remain drafts. Channel labels do not prove delivery. Essential staff require supervisor direction; deferred review is manual. OnSolve integration, transport, delivery receipts and enterprise rosters are not implemented.
- The hosted model can degrade, and the workshop endpoint's post-event availability has not been newly checked. The underlying model vendor/version behind its alias is not verified. Historical successful calls are a small dated sample.
- Authentication is manager Basic auth within the private local/tunnel arrangement. No enterprise SSO or public service is provided. Record hashes detect ordinary changes, not privileged-host tampering.
- The original 0.2s test failure's precise scheduling cause cannot be recovered from its log. Controlled startup reproduced the missing-trace condition; new tests separate startup/trace concerns and assert termination without extending the budget. Initial/final logs are retained.
- Responsive/browser observations are scoped tests, not accessibility certification. Memo print/pagination and human spoken rehearsal require their explicit verification; a successful HTML download is not print-perfect proof.
- License/team publication rights, public code/demo access, social publication and any new deployment are separate user decisions. No portal write, submission receipt or approval is claimed.

Current and historical evidence is distinguished in [verification](VERIFICATION.md) and [the release manifest](../RELEASE_MANIFEST.json). All old source snapshots remain historical after capture.
