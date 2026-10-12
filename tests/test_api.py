from dataclasses import replace
from datetime import timedelta
import json
import pytest
from fastapi.testclient import TestClient
from app.services.audit import utcnow
from app.services import evaluation
from app.clients import nws, air_quality


@pytest.fixture
def client(store, snapshot, monkeypatch):
    import app.main as main
    import app.auth as auth

    monkeypatch.setattr(main, "store", store)
    monkeypatch.setattr(
        auth,
        "settings",
        replace(
            auth.settings,
            manager_username="synthetic-manager",
            manager_password="test-only-long-password",
        ),
    )

    async def weather(*args):
        return snapshot["nws"]

    async def aq(*args):
        return snapshot["air_quality"]

    monkeypatch.setattr(nws, "point", weather)
    monkeypatch.setattr(air_quality, "point", aq)
    monkeypatch.setattr(
        evaluation, "settings", replace(evaluation.settings, inference_key="")
    )
    with TestClient(main.app) as test:
        yield test


AUTH = ("synthetic-manager", "test-only-long-password")


def test_health_and_every_business_route_auth(client):
    assert client.get("/health").status_code == 200
    for path in [
        "/api/config",
        "/api/facilities",
        "/api/evaluations",
        "/api/decisions",
        "/api/live-alerts",
        "/api/evaluations/fake",
        "/api/evaluations/fake/trace",
        "/api/decisions/fake/replay",
        "/api/decisions/fake/notifications",
        "/api/decisions/fake/export",
    ]:
        assert client.get(path).status_code == 401
    assert client.post("/api/evaluations/fake/decision", json={}).status_code == 401
    assert (
        client.get("/api/facilities", auth=("synthetic-manager", "wrong")).status_code
        == 401
    )


def test_full_api_synthetic_flow(client, snapshot):
    payload = {
        "facility_id": "kc-demo",
        **{k: snapshot["work_period"][k] for k in ("start", "end", "special_shift")},
    }
    headers = {"Idempotency-Key": "synthetic-api-run"}
    response = client.post("/api/evaluations", json=payload, auth=AUTH, headers=headers)
    assert response.status_code == 202
    id = response.json()["run_id"]
    assert (
        client.post(
            "/api/evaluations", json=payload, auth=AUTH, headers=headers
        ).json()["run_id"]
        == id
    )
    import time

    for _ in range(100):
        run = client.get("/api/evaluations/" + id, auth=AUTH).json()
        if run["status"] not in ("collecting", "evaluating"):
            break
        time.sleep(0.01)
    assert run["status"] == "ready"
    assert run["ai"]["status"] == "unavailable"
    decision = {"action": "approve", "snapshot_hash": run["snapshot_hash"]}
    path = "/api/evaluations/" + id + "/decision"
    response = client.post(
        path,
        json=decision,
        auth=AUTH,
        headers={"Idempotency-Key": "synthetic-api-decision"},
    )
    assert response.status_code == 200, response.text
    bundle = response.json()
    decision_id = bundle["decision"]["decision_id"]
    assert bundle["decision"]["actor"] == "synthetic-manager"
    assert (
        client.post(
            path,
            json=decision,
            auth=AUTH,
            headers={"Idempotency-Key": "synthetic-api-decision"},
        ).json()
        == bundle
    )
    assert (
        client.get(f"/api/decisions/{decision_id}/replay", auth=AUTH).json() == bundle
    )
    assert client.get(f"/api/decisions/{decision_id}/notifications", auth=AUTH).json()[
        "counts"
    ] == {"included": 9, "excluded": 2, "deferred": 1}
    export = client.get(
        f"/api/decisions/{decision_id}/notifications/demo-03/export", auth=AUTH
    )
    assert export.status_code == 200 and "PROTOTYPE DEMO OUTBOX" in export.text
    assert "test-only-long-password" not in json.dumps(bundle)


def test_auth_actor_spoof_unknown_fields_and_cross_origin(client, snapshot):
    assert (
        client.post(
            "/api/evaluations/fake/decision",
            json={"approved_by": "attacker"},
            auth=AUTH,
            headers={"Idempotency-Key": "spoof-actor-key"},
        ).status_code
        == 422
    )
    assert (
        client.post(
            "/api/evaluations",
            json={},
            auth=AUTH,
            headers={
                "Origin": "https://evil.example",
                "Idempotency-Key": "cross-origin",
            },
        ).status_code
        == 403
    )
    assert (
        client.post(
            "/api/evaluations/fake/decision",
            json={
                "action": "override",
                "posture": "closure",
                "snapshot_hash": "a" * 64,
            },
            auth=AUTH,
            headers={"Idempotency-Key": "missing-reason"},
        ).status_code
        == 422
    )


def test_work_period_validation(client, snapshot):
    payload = {
        "facility_id": "kc-demo",
        **{k: snapshot["work_period"][k] for k in ("start", "end", "special_shift")},
    }
    payload["start"] = "2026-10-11T08:00:00"
    assert (
        client.post(
            "/api/evaluations",
            json=payload,
            auth=AUTH,
            headers={"Idempotency-Key": "timezone-key"},
        ).status_code
        == 422
    )
    # A weekend work period needs special-shift acknowledgement.
    now = utcnow()
    if (
        now.astimezone(__import__("zoneinfo").ZoneInfo("America/Chicago")).weekday()
        >= 5
    ):
        payload["start"] = (now + timedelta(minutes=10)).isoformat()
        payload["end"] = (now + timedelta(hours=2)).isoformat()
        payload["special_shift"] = False
        assert (
            client.post(
                "/api/evaluations",
                json=payload,
                auth=AUTH,
                headers={"Idempotency-Key": "weekend-key"},
            ).status_code
            == 422
        )


def test_ui_security_headers_and_no_inner_html(client):
    page = client.get("/")
    assert page.status_code == 200
    assert "script-src 'self'" in page.headers["content-security-policy"]
    js = client.get("/static/app.js").text
    assert "innerHTML" not in js and "textContent" in js
