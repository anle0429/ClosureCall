import json
import uuid
from app.services.audit import canonical, digest, parse_time, utcnow, timestamp
from app.services.notifications import package
from app.settings import settings


class DecisionConflict(ValueError):
    pass


def decide(store, run_id, request, actor, key):
    request_body = request.model_dump(mode="json")
    fingerprint = digest({"run_id": run_id, "actor": actor, "request": request_body})
    # Hold transaction from stale/supersession checks through decision+outbox insert.
    with store.connection() as conn:
        conn.execute("BEGIN IMMEDIATE")
        existing = conn.execute(
            "SELECT id,request_hash FROM decisions WHERE idempotency_key=?", (key,)
        ).fetchone()
        if existing:
            if existing["request_hash"] != fingerprint:
                raise DecisionConflict("Idempotency key reused with different content")
            return store.replay(existing["id"])
        if conn.execute(
            "SELECT id FROM decisions WHERE run_id=?", (run_id,)
        ).fetchone():
            raise DecisionConflict("This assessment already has a manager decision")
        run = store.run(run_id)
        if run["status"] not in ("ready", "incomplete"):
            raise DecisionConflict("Assessment is not ready for review")
        snapshot = run["snapshot"]
        if snapshot["mode"] != "LIVE":
            raise DecisionConflict(
                "Simulation/replay cannot create manager decisions or outbox"
            )
        if request.snapshot_hash != run["snapshot_hash"]:
            raise DecisionConflict("Snapshot hash changed; refresh review")
        newer = conn.execute(
            "SELECT 1 FROM runs WHERE facility_id=? AND created_at>? LIMIT 1",
            (run["facility_id"], run["created_at"]),
        ).fetchone()
        now = utcnow()
        age = (now - parse_time(snapshot["collected_at_utc"])).total_seconds()
        stale = (
            bool(newer)
            or age > settings.nws_freshness
            or parse_time(snapshot["work_period"]["end"]) <= now
        )
        source_age = (
            now - parse_time(snapshot["nws"]["fetched_at_utc"])
        ).total_seconds()
        aq_valid = parse_time(snapshot["air_quality"].get("valid_at_utc"))
        if source_age > settings.nws_freshness or (
            aq_valid and abs((now - aq_valid).total_seconds()) > settings.aq_max_age
        ):
            stale = True
        matched_ids = set(snapshot["assessment"]["evidence_ids"])
        for alert in snapshot["nws"]["alerts"]:
            if (
                alert["alert_id"] in matched_ids
                and parse_time(alert.get("expires")) is not None
                and parse_time(alert["expires"]) <= now
            ):
                stale = True
        if request.action == "approve":
            if stale or snapshot["assessment"]["review_status"] != "ready_for_manager":
                raise DecisionConflict(
                    "Re-evaluate, or explicitly override with a reason for stale/incomplete evidence"
                )
            posture = snapshot["assessment"]["recommended_posture"]
            if request.posture is not None and request.posture != posture:
                raise DecisionConflict("Changed posture requires override")
        elif request.action == "override":
            if not request.reason.strip() or request.posture is None:
                raise DecisionConflict(
                    "Override requires an explicit posture and reason"
                )
            posture = request.posture
        else:
            if not request.reason.strip():
                raise DecisionConflict("Reject requires a reason")
            posture = None
        if posture in ("delayed_arrival", "early_dismissal"):
            timing = request.timing_at
            if (
                timing is None
                or timing.tzinfo is None
                or not request.timing_basis.strip()
            ):
                raise DecisionConflict(
                    "Timing posture requires timezone-aware confirmed timing and evidence/assumption"
                )
            if (
                not parse_time(snapshot["work_period"]["start"])
                < timing
                < parse_time(snapshot["work_period"]["end"])
            ):
                raise DecisionConflict(
                    "Confirmed timing must be inside the affected work period"
                )
        decision = {
            "decision_id": str(uuid.uuid4()),
            "evaluation_id": run_id,
            "snapshot_hash": run["snapshot_hash"],
            "posture": posture,
            "actor": actor,
            "status": {
                "approve": "approved",
                "override": "overridden",
                "reject": "rejected",
            }[request.action],
            "reason": request.reason.strip()
            or "Approved deterministic prototype recommendation",
            "approved_at": timestamp(),
            "effective_window": snapshot["work_period"],
            "timing_at": request_body["timing_at"],
            "timing_basis": request.timing_basis,
            "stale_or_superseded_override": stale and request.action == "override",
        }
        notifications = package(snapshot, decision)
        bundle = {
            "snapshot": snapshot,
            "snapshot_hash": run["snapshot_hash"],
            "ai": run["ai"],
            "trace": run["trace"],
            "metrics": run.get("metrics", {}),
            "decision": decision,
            "notifications": notifications,
        }
        conn.execute(
            "INSERT INTO decisions VALUES (?,?,?,?,?,?)",
            (
                decision["decision_id"],
                run_id,
                key,
                fingerprint,
                canonical(bundle),
                digest(bundle),
            ),
        )
        conn.execute(
            "INSERT INTO outbox VALUES (?,?)",
            (decision["decision_id"], canonical(notifications)),
        )
    return store.replay(decision["decision_id"])
