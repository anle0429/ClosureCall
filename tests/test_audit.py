import sqlite3
import pytest
from conftest import persist
from app.db import Store
from app.services.decisions import decide
from app.schemas import DecisionRequest
from scripts.backup_db import backup


def test_replay_after_restart_and_current_changes(store, snapshot, monkeypatch):
    run = persist(store, snapshot)
    bundle = decide(
        store,
        run["id"],
        DecisionRequest(snapshot_hash=run["snapshot_hash"], action="approve"),
        "manager",
        "audit-key",
    )
    snapshot["policy"]["version"] = "new-rule"
    snapshot["roster"][0]["name"] = "Changed now"
    import app.policy.engine as engine

    monkeypatch.setattr(
        engine,
        "assess",
        lambda *_: (_ for _ in ()).throw(AssertionError("Replay must not evaluate")),
    )
    restarted = Store(store.path)
    restarted.initialize()
    assert restarted.replay(bundle["decision"]["decision_id"]) == bundle
    destination = store.path + ".backup"
    backup(store.path, destination)
    assert Store(destination).replay(bundle["decision"]["decision_id"]) == bundle


@pytest.mark.parametrize("table", ["snapshots", "results", "decisions", "outbox"])
def test_immutable_tables(store, snapshot, table):
    run = persist(store, snapshot)
    decide(
        store,
        run["id"],
        DecisionRequest(snapshot_hash=run["snapshot_hash"], action="approve"),
        "manager",
        "immutable-key",
    )
    with pytest.raises(sqlite3.IntegrityError):
        with store.connection() as conn:
            conn.execute(f"DELETE FROM {table}")
    with pytest.raises(sqlite3.IntegrityError):
        with store.connection() as conn:
            conn.execute(f"UPDATE {table} SET body='{{}}'")


def test_restart_interrupts_active_run(store):
    id, _ = store.create_run({"facility_id": "kc-demo"}, "restart-key")
    store.initialize()
    assert store.run(id)["status"] == "interrupted"


def test_evaluation_duplicate_and_concurrency(store):
    body = {"facility_id": "kc-demo"}
    id, created = store.create_run(body, "unique-key")
    assert created
    assert store.create_run(body, "unique-key") == (id, False)
    with pytest.raises(sqlite3.IntegrityError):
        store.create_run(body, "other-key")


def test_isolated_api_replay_after_current_rules_roster_change_without_external_calls(
    store, snapshot, tmp_path, monkeypatch
):
    """Copy a test DB; change current providers, never the frozen demo record."""
    from dataclasses import replace
    from fastapi.testclient import TestClient
    import app.main as main
    import app.auth as auth
    import app.services.evaluation as evaluation
    import app.services.recipients as recipients
    import app.policy.engine as engine
    from app.clients import nws, air_quality
    from copy import deepcopy
    from app.services.audit import canonical, digest

    run = persist(store, snapshot)
    original = decide(
        store,
        run["id"],
        DecisionRequest(snapshot_hash=run["snapshot_hash"], action="approve"),
        "synthetic-manager",
        "isolated-replay-key",
    )
    original_bytes = canonical(original)
    isolated = tmp_path / "isolated-acceptance.sqlite3"
    backup(store.path, str(isolated))
    copied = Store(isolated)
    current_rules = deepcopy(snapshot["policy"])
    current_rules["version"] = "CHANGED-CURRENT-SYNTHETIC-v2"
    current_rules["rules"][0]["prototype_mapping_reason"] = "CHANGED CURRENT RULE"
    current_roster = deepcopy(snapshot["roster"])
    current_roster[0].update(
        name="CHANGED CURRENT SYNTHETIC PERSON",
        assignment="no_shift",
        roster_version="synthetic-v2",
    )
    monkeypatch.setattr(engine, "load_rules", lambda: deepcopy(current_rules))
    monkeypatch.setattr(evaluation, "load_rules", engine.load_rules)
    monkeypatch.setattr(recipients, "roster", lambda *_: deepcopy(current_roster))
    monkeypatch.setattr(evaluation, "roster", recipients.roster)
    assert engine.load_rules()["version"] != original["snapshot"]["policy"]["version"]
    assert (
        recipients.roster("kc-demo", "", "")[0]["name"]
        != original["snapshot"]["roster"][0]["name"]
    )
    calls = []

    def forbidden(*args, **kwargs):
        calls.append("external or recompute call")
        raise AssertionError("Historical replay must only read frozen records")

    for module, name in [
        (nws, "point"),
        (nws, "national"),
        (air_quality, "point"),
        (evaluation, "bounded_worker"),
        (evaluation, "assess"),
        (engine, "assess"),
        (recipients, "route"),
    ]:
        monkeypatch.setattr(module, name, forbidden)
    monkeypatch.setattr(main, "store", copied)
    monkeypatch.setattr(
        auth,
        "settings",
        replace(
            auth.settings,
            manager_username="synthetic-manager",
            manager_password="test-only-long-password",
        ),
    )
    path = f"/api/decisions/{original['decision']['decision_id']}/replay"
    for _ in range(2):
        with TestClient(main.app) as client:
            response = client.get(
                path, auth=("synthetic-manager", "test-only-long-password")
            )
            assert response.status_code == 200
            assert canonical(response.json()) == original_bytes
            assert response.json()["bundle_hash"] == original["bundle_hash"]
    assert calls == []
    assert (
        canonical(store.replay(original["decision"]["decision_id"])) == original_bytes
    )
    assert digest(copied.replay(original["decision"]["decision_id"])) == digest(
        original
    )
