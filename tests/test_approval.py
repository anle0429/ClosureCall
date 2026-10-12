from datetime import timedelta
import pytest
from pydantic import ValidationError
from conftest import persist
from app.services.decisions import decide, DecisionConflict
from app.schemas import DecisionRequest
from app.services.audit import utcnow


def request(run, **kwargs):
    return DecisionRequest(
        snapshot_hash=run["snapshot_hash"], action="approve", **kwargs
    )


def test_idempotent_decision_and_outbox(store, snapshot):
    run = persist(store, snapshot)
    first = decide(store, run["id"], request(run), "manager", "decision-key")
    second = decide(store, run["id"], request(run), "manager", "decision-key")
    assert first == second
    assert first["decision"]["actor"] == "manager"
    with store.connection() as conn:
        assert conn.execute("SELECT COUNT(*) FROM decisions").fetchone()[0] == 1
        assert conn.execute("SELECT COUNT(*) FROM outbox").fetchone()[0] == 1


def test_idempotency_mismatch_and_duplicate_rejected(store, snapshot):
    run = persist(store, snapshot)
    decide(store, run["id"], request(run), "manager", "decision-key")
    with pytest.raises(DecisionConflict):
        decide(
            store, run["id"], request(run, reason="changed"), "manager", "decision-key"
        )
    with pytest.raises(DecisionConflict):
        decide(store, run["id"], request(run), "manager", "different-key")


def test_override_requires_reason(store, snapshot):
    run = persist(store, snapshot)
    with pytest.raises(ValidationError):
        decide(
            store,
            run["id"],
            DecisionRequest(
                snapshot_hash=run["snapshot_hash"], action="override", posture="closure"
            ),
            "manager",
            "override-key",
        )


@pytest.mark.parametrize("change", ["stale", "superseded", "simulation", "hash"])
def test_approval_guards(store, snapshot, change):
    if change == "stale":
        snapshot["collected_at_utc"] = (utcnow() - timedelta(hours=1)).isoformat()
    if change == "simulation":
        snapshot["mode"] = "SIMULATION"
    run = persist(store, snapshot)
    if change == "superseded":
        persist(store, snapshot, "newer-run-key")
    req = request(run)
    if change == "hash":
        req.snapshot_hash = "0" * 64
    with pytest.raises(DecisionConflict):
        decide(store, run["id"], req, "manager", "guard-key")


def test_stale_explicit_override(store, snapshot):
    snapshot["collected_at_utc"] = (utcnow() - timedelta(hours=1)).isoformat()
    run = persist(store, snapshot)
    result = decide(
        store,
        run["id"],
        DecisionRequest(
            snapshot_hash=run["snapshot_hash"],
            action="override",
            posture="telework",
            reason="Local supervisor verification; stale source acknowledged",
        ),
        "manager",
        "override-key",
    )
    assert result["decision"]["stale_or_superseded_override"] is True


def test_timing_requires_confirmation(store, snapshot):
    run = persist(store, snapshot)
    req = DecisionRequest(
        snapshot_hash=run["snapshot_hash"],
        action="override",
        posture="early_dismissal",
        reason="local verification",
    )
    with pytest.raises(DecisionConflict):
        decide(store, run["id"], req, "manager", "timing-key")
    req.timing_at = utcnow() + timedelta(days=5)
    req.timing_basis = "Manager assumption"
    with pytest.raises(DecisionConflict):
        decide(store, run["id"], req, "manager", "timing-key")


def test_reject_never_queues_notification(store, snapshot):
    run = persist(store, snapshot)
    result = decide(
        store,
        run["id"],
        DecisionRequest(
            snapshot_hash=run["snapshot_hash"],
            action="reject",
            reason="Insufficient local evidence",
        ),
        "manager",
        "reject-key",
    )
    assert result["notifications"]["counts"]["included"] == 0
    assert all(
        p["notification_status"] == "draft"
        for p in result["notifications"]["recipients"]
    )
