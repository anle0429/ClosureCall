"""Frozen memo view; no live inputs, sends, history changes or inferred actors."""

from copy import deepcopy
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from conftest import persist
from app.schemas import DecisionRequest
from app.services.decisions import decide
from app.services.audit import canonical
from app.services.memo import render_memo, RENDERER_VERSION


@pytest.fixture
def frozen(store, snapshot):
    run = persist(store, snapshot)
    return decide(
        store,
        run["id"],
        DecisionRequest(
            snapshot_hash=run["snapshot_hash"],
            action="override",
            posture="closure",
            reason="SYNTHETIC MEMO TEST ONLY",
        ),
        "synthetic-manager",
        "memo-test-decision",
    )


def test_memo_api_authenticated_frozen_no_sources_model_rules_or_routing(
    store, frozen, monkeypatch
):
    import app.main as main
    import app.auth as auth
    import app.clients.base as base
    from app.clients import nws, air_quality
    import app.services.evaluation as evaluation
    import app.policy.engine as engine
    import app.services.recipients as recipients
    import app.services.notifications as notifications
    import app.agent.brief as brief
    import app.services.decisions as decisions

    calls = []

    def forbidden(*args, **kwargs):
        calls.append("forbidden")
        raise AssertionError("Memo cannot call current inputs or recompute")

    for module, name in [
        (base, "fetch_json"),
        (nws, "point"),
        (nws, "national"),
        (air_quality, "point"),
        (evaluation, "bounded_worker"),
        (evaluation, "assess"),
        (evaluation, "load_rules"),
        (evaluation, "roster"),
        (engine, "assess"),
        (engine, "load_rules"),
        (recipients, "roster"),
        (recipients, "route"),
        (notifications, "package"),
        (decisions, "package"),
        (brief, "grounded_brief"),
    ]:
        monkeypatch.setattr(module, name, forbidden)
    monkeypatch.setattr(main, "store", store)
    monkeypatch.setattr(
        auth,
        "settings",
        replace(
            auth.settings,
            manager_username="synthetic-manager",
            manager_password="memo-test-only-password",
        ),
    )
    original = canonical(frozen)
    path = "/api/decisions/" + frozen["decision"]["decision_id"]
    with TestClient(main.app) as client:
        assert client.get(path + "/memo").status_code == 401
        response = client.get(
            path + "/memo", auth=("synthetic-manager", "memo-test-only-password")
        )
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert ".html" in response.headers["content-disposition"]
        assert "script-src 'self'" in response.headers["content-security-policy"]
        assert RENDERER_VERSION in response.text
        assert "Original posture</strong></dt><dd>normal" in response.text
        assert "Final posture</strong></dt><dd>closure" in response.text
        assert frozen["bundle_hash"] in response.text
        assert (
            canonical(
                client.get(
                    path + "/export",
                    auth=("synthetic-manager", "memo-test-only-password"),
                ).json()
            )
            == original
        )
        assert "Download decision memo (HTML)" in client.get("/static/app.js").text
        assert "closurecall-decision-memo.html" in client.get("/static/app.js").text
    assert canonical(store.replay(frozen["decision"]["decision_id"])) == original
    assert calls == []


def test_memo_timezone_escaping_and_no_inferred_actor_reason(frozen):
    record = deepcopy(frozen)
    record["snapshot"]["work_period"].update(
        start="2026-10-10T14:00:00Z", end="2026-10-10T22:00:00Z"
    )
    record["snapshot"]["facility"]["display_name"] = "<script>unsafe()</script>"
    record["decision"].update(actor=None, reason="")
    record["notifications"]["recipients"][0]["message"] = "<img src=x onerror=unsafe()>"
    output = render_memo(record)
    assert "2026-10-10T09:00:00-05:00 [America/Chicago]" in output
    assert "<script>" not in output and "<img" not in output
    assert "&lt;script&gt;unsafe()&lt;/script&gt;" in output
    assert "&lt;img src=x onerror=unsafe()&gt;" in output
    assert "Recorded actor</strong></dt><dd>Not recorded" in output
    assert "Recorded manager reason</strong></dt><dd>Not recorded" in output
    assert "Approved deterministic prototype recommendation" not in output
    assert "<h3>Missing inputs</h3><ul><li>No entries recorded</li></ul>" in output


def test_memo_missing_timezone_or_offset_is_not_inferred(frozen):
    record = deepcopy(frozen)
    record["snapshot"]["facility"]["timezone"] = "Not/A/Timezone"
    record["snapshot"]["work_period"]["start"] = "2026-10-10T09:00:00"
    output = render_memo(record)
    assert "offset not recorded; no conversion" in output
    assert "facility timezone conversion unavailable" in output


@pytest.mark.parametrize("name", ["ui-approved-export.json", "ui-override-export.json"])
def test_actual_historical_exports_unchanged_by_new_memo(name, monkeypatch):
    import app.policy.engine as engine
    import app.clients.base as base

    def forbidden(*args, **kwargs):
        raise AssertionError("Historical rendering must not fetch or assess")

    monkeypatch.setattr(engine, "assess", forbidden)
    monkeypatch.setattr(base, "fetch_json", forbidden)
    path = Path(__file__).resolve().parents[1] / "evidence" / "release" / name
    before = path.read_bytes()
    record = json.loads(before)
    original = canonical(record)
    drafts = deepcopy(record["notifications"])
    output = render_memo(record)
    assert (
        record["decision"]["decision_id"] in output and record["bundle_hash"] in output
    )
    assert "REPLAY" in output and "DRAFTS, NOT SENT" in output
    assert "Original recommendation — before manager decision" in output
    assert "Final manager decision — separate from recommendation" in output
    if name == "ui-override-export.json":
        assert "Original posture</strong></dt><dd>No candidate recorded" in output
        assert "Final posture</strong></dt><dd>closure" in output
        assert "CONTROLLED SYNTHETIC REHEARSAL ONLY" in output
    assert canonical(record) == original and record["notifications"] == drafts
    assert hashlib.sha256(path.read_bytes()).digest() == hashlib.sha256(before).digest()


def test_memo_requires_replay(frozen):
    with pytest.raises(ValueError, match="frozen replay"):
        render_memo({**frozen, "mode": "LIVE"})
