"""Offline acceptance probe of a copied real historical bundle. Never contacts providers.

Run from the repo: .venv/Scripts/python.exe evidence/acceptance/replay_isolation.py
The separate SQLite DB and changed rules/roster files stay under ignored data/acceptance.
"""
import json
from pathlib import Path
import sys
import tempfile
from copy import deepcopy
from dataclasses import replace
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from fastapi.testclient import TestClient
from app.db import Store
from app.services.audit import canonical,digest,utcnow
import app.main as main
import app.auth as auth
import app.services.evaluation as evaluation
import app.policy.engine as engine
import app.services.recipients as recipients
import app.clients.nws as nws
import app.clients.air_quality as aq

source=ROOT/'evidence/acceptance/old-demo-baseline.json'
before=source.read_bytes()
original=json.loads(before)
bundle={k:v for k,v in original.items() if k not in ('mode','bundle_hash')}
assert digest(bundle)==original['bundle_hash']
parent=ROOT/'data/acceptance'
parent.mkdir(parents=True,exist_ok=True)
directory=Path(tempfile.mkdtemp(prefix='replay-',dir=parent)).resolve()
assert directory.is_relative_to(parent.resolve())
db=Store(directory/'isolated.sqlite3')
db.initialize()
run_id=bundle['decision']['evaluation_id']
decision_id=bundle['decision']['decision_id']
snapshot=bundle['snapshot']
with db.connection() as conn:
    conn.execute('INSERT INTO runs(id,facility_id,status,created_at,request,request_key) VALUES (?,?,?,?,?,?)',
        (run_id,snapshot['facility']['facility_id'],'incomplete',snapshot['collected_at_utc'],canonical({}),'isolated-import'))
    conn.execute('INSERT INTO snapshots VALUES (?,?,?)',(run_id,canonical(snapshot),bundle['snapshot_hash']))
    conn.execute('INSERT INTO results VALUES (?,?)',(run_id,canonical({k:bundle[k] for k in ('ai','trace','metrics')})))
    conn.execute('INSERT INTO decisions VALUES (?,?,?,?,?,?)',
        (decision_id,run_id,'isolated-import-decision','offline-import',canonical(bundle),original['bundle_hash']))
    conn.execute('INSERT INTO outbox VALUES (?,?)',(decision_id,canonical(bundle['notifications'])))
assert db.replay(decision_id)==original
rules=deepcopy(snapshot['policy'])
rules['version']='CHANGED-CURRENT-SYNTHETIC-v2'
rules['rules'][0]['version']='2'
rules['rules'][0]['proposed_posture']='telework'
roster=deepcopy(snapshot['roster'])
roster[0].update(name='CHANGED CURRENT SYNTHETIC PERSON',assignment='no_shift')
rules_path=directory/'current-rules.json'
roster_path=directory/'current-roster.json'
rules_path.write_text(canonical(rules),encoding='utf-8')
roster_path.write_text(canonical(roster),encoding='utf-8')
def current_rules():return json.loads(rules_path.read_text(encoding='utf-8'))
def current_roster(*_):return json.loads(roster_path.read_text(encoding='utf-8'))
calls=[]
def forbidden(*args,**kwargs):
    calls.append('source/model/recompute')
    raise AssertionError('Replay attempted external call or recomputation')
settings=replace(auth.settings,manager_username='isolated-manager',manager_password='isolated-test-only-password')
with patch.object(main,'store',db),patch.object(auth,'settings',settings), \
     patch.object(engine,'load_rules',current_rules),patch.object(evaluation,'load_rules',current_rules), \
     patch.object(recipients,'roster',current_roster),patch.object(evaluation,'roster',current_roster), \
     patch.object(nws,'point',forbidden),patch.object(nws,'national',forbidden),patch.object(aq,'point',forbidden), \
     patch.object(evaluation,'bounded_worker',forbidden),patch.object(engine,'assess',forbidden), \
     patch.object(evaluation,'assess',forbidden),patch.object(recipients,'route',forbidden):
    assert evaluation.load_rules()['version']!=snapshot['policy']['version']
    assert evaluation.roster('','','')[0]['name']!=snapshot['roster'][0]['name']
    for _ in range(2):
        with TestClient(main.app) as client:
            response=client.get(f'/api/decisions/{decision_id}/replay',auth=('isolated-manager','isolated-test-only-password'))
            assert response.status_code==200 and response.json()==original
assert calls==[] and source.read_bytes()==before
print(json.dumps({'status':'VERIFIED','checked_at_utc':utcnow().isoformat(),
    'scope':'isolated copy of real historical export; no demo DB/backup modified',
    'decision_id':decision_id,'bundle_hash':original['bundle_hash'],
    'current_policy_version':rules['version'],'historical_policy_version':snapshot['policy']['version'],
    'changed_current_roster':True,'replay_reads_after_restart':2,'source_model_recompute_calls':0,
    'historical_exact_equal':True,'input_export_unchanged':True},indent=2))
