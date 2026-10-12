from app.services.recipients import route
from app.services.notifications import package


def test_all_12_routes_explained(snapshot):
    people = route(snapshot, "telework")
    assert len(people) == 12
    assert all(p["reason"] and p["instruction"] for p in people)
    assert sum(p["routing_status"] == "included" for p in people) == 9
    assert sum(p["routing_status"] == "excluded" for p in people) == 2
    assert sum(p["routing_status"] == "deferred" for p in people) == 1


def test_essential_accessibility_nontelework(snapshot):
    people = route(snapshot, "closure")
    assert all(
        "reporting requirements" in p["instruction"] for p in people if p["essential"]
    )
    assert people[2]["channel"] == "voice_accessible"
    assert "paid leave" in people[5]["instruction"]


def test_no_urgent_broadcast_offsite_or_telework(snapshot):
    people = route(snapshot, "closure")
    assert (
        people[9]["routing_status"] == "deferred"
        and people[9]["channel"] == "app_inbox"
    )
    assert people[10]["routing_status"] == "excluded" and people[10]["channel"] is None
    assert people[11]["routing_status"] == "excluded"


def test_assignment_window_not_home_facility(snapshot):
    snapshot["roster"][0]["assignment_start"] = snapshot["work_period"]["end"]
    assert route(snapshot, "closure")[0]["routing_status"] == "excluded"


def test_deferred_has_manual_follow_up_in_draft(snapshot):
    decision = {
        "decision_id": "synthetic-deferred",
        "status": "approved",
        "posture": "closure",
        "effective_window": snapshot["work_period"],
        "reason": "Synthetic acceptance test",
    }
    pack = package(snapshot, decision)
    deferred = pack["recipients"][9]
    assert (
        deferred["channel"] == "app_inbox"
        and deferred["notification_status"] == "draft"
    )
    assert "before the assigned shift starts" in deferred["follow_up"]
    assert (
        "immediately" in deferred["follow_up"]
        and "reassigned onsite" in deferred["follow_up"]
    )
    assert deferred["follow_up"] in deferred["message"]
    assert all(
        p["follow_up"] is None
        for p in pack["recipients"]
        if p["routing_status"] != "deferred"
    )
    decision["status"] = "rejected"
    rejected = package(snapshot, decision)
    assert all(
        p["channel"] is None and p["follow_up"] is None for p in rejected["recipients"]
    )


def test_counts_and_instructions_change_with_roster_and_posture(snapshot):
    decision = {
        "decision_id": "synthetic-routing",
        "status": "approved",
        "posture": "telework",
        "effective_window": snapshot["work_period"],
        "reason": "Synthetic acceptance test",
    }
    baseline = package(snapshot, decision)
    assert "approved telework" in baseline["recipients"][0]["instruction"]
    assert "paid leave" in baseline["recipients"][5]["instruction"]
    snapshot["roster"][0]["assignment"] = "no_shift"
    snapshot["roster"][9]["assignment"] = "onsite"
    snapshot["roster"][10]["assignment"] = "onsite"
    snapshot["roster"][10]["assigned_facility_id"] = snapshot["facility"]["facility_id"]
    changed = package(snapshot, decision)
    assert changed["counts"] == {"included": 10, "excluded": 2, "deferred": 0}
    decision["posture"] = "closure"
    assert (
        "Routine onsite reporting"
        in package(snapshot, decision)["recipients"][9]["instruction"]
    )
