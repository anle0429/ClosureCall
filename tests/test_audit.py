import sqlite3
import pytest
from conftest import persist
from app.db import Store
from app.services.decisions import decide
from app.schemas import DecisionRequest
from scripts.backup_db import backup

def test_replay_after_restart_and_current_changes(store,snapshot,monkeypatch):
    run=persist(store,snapshot)
    bundle=decide(store,run['id'],DecisionRequest(snapshot_hash=run['snapshot_hash'],action='approve'),'manager','audit-key')
    snapshot['policy']['version']='new-rule'
    snapshot['roster'][0]['name']='Changed now'
    import app.policy.engine as engine
    monkeypatch.setattr(engine,'assess',lambda *_: (_ for _ in ()).throw(AssertionError('Replay must not evaluate')))
    restarted=Store(store.path)
    restarted.initialize()
    assert restarted.replay(bundle['decision']['decision_id'])==bundle
    destination=store.path+'.backup'
    backup(store.path,destination)
    assert Store(destination).replay(bundle['decision']['decision_id'])==bundle

@pytest.mark.parametrize('table',['snapshots','results','decisions','outbox'])
def test_immutable_tables(store,snapshot,table):
    run=persist(store,snapshot)
    decide(store,run['id'],DecisionRequest(snapshot_hash=run['snapshot_hash'],action='approve'),'manager','immutable-key')
    with pytest.raises(sqlite3.IntegrityError):
        with store.connection() as conn:conn.execute(f'DELETE FROM {table}')
    with pytest.raises(sqlite3.IntegrityError):
        with store.connection() as conn:conn.execute(f"UPDATE {table} SET body='{{}}'")

def test_restart_interrupts_active_run(store):
    id,_=store.create_run({'facility_id':'kc-demo'},'restart-key')
    store.initialize()
    assert store.run(id)['status']=='interrupted'

def test_evaluation_duplicate_and_concurrency(store):
    body={'facility_id':'kc-demo'}
    id,created=store.create_run(body,'unique-key')
    assert created
    assert store.create_run(body,'unique-key')==(id,False)
    with pytest.raises(sqlite3.IntegrityError):store.create_run(body,'other-key')
