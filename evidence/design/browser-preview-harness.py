"""Isolated design QA: real frozen replay, explicitly synthetic new evaluations.

Uses existing authenticated business endpoints and decision service. Never opens
the original database, uses inference credentials, or contacts providers.
"""
import asyncio
from copy import deepcopy
from datetime import timedelta
import json
import os
from pathlib import Path
import sys
import uuid

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
FOLDER = ROOT / 'data' / ('design-preview-' + uuid.uuid4().hex[:8])
FOLDER.mkdir()
os.environ.update(DATABASE_PATH=str(FOLDER / 'isolated.sqlite3'),
                  INFERENCE_API_KEY='', MANAGER_USERNAME='design-review',
                  MANAGER_PASSWORD='synthetic-design-preview-only', APP_ENV='design-test',
                  DEPLOYMENT_LABEL='ISOLATED DESIGN QA — synthetic evaluations / historical replay',
                  BUILD_COMMIT='design-working-candidate')
from app.db import Store
from app.services.audit import canonical, digest, timestamp, parse_time, utcnow
from app.services.recipients import roster
from app.policy.engine import assess, load_rules
import app.main as main
from fastapi.responses import JSONResponse
import uvicorn

store = Store(FOLDER / 'isolated.sqlite3')
store.initialize()
records = []
for name in ['ui-approved-export.json', 'ui-override-export.json']:
    record = json.loads((ROOT / 'evidence' / 'release' / name).read_text(encoding='utf-8'))
    s, d = record['snapshot'], record['decision']
    run_id = d['evaluation_id']
    request = {'facility_id': s['facility']['facility_id'], **{k:s['work_period'][k] for k in ('start','end','special_shift')}}
    bundle = {k:v for k,v in record.items() if k not in ('mode','bundle_hash')}
    assert digest(bundle) == record['bundle_hash'] and digest(s) == record['snapshot_hash']
    with store.connection() as conn:
        conn.execute('INSERT OR IGNORE INTO facilities VALUES (?,?)', (s['facility']['facility_id'], canonical(s['facility'])))
        conn.execute('INSERT INTO runs VALUES (?,?,?,?,?,?,?)', (run_id,s['facility']['facility_id'],'ready',s['collected_at_utc'],canonical(request),None,'preview-'+run_id))
        conn.execute('INSERT INTO snapshots VALUES (?,?,?)', (run_id,canonical(s),record['snapshot_hash']))
        conn.execute('INSERT INTO results VALUES (?,?)', (run_id,canonical({k:record[k] for k in ('ai','trace','metrics')})))
        conn.execute('INSERT INTO decisions VALUES (?,?,?,?,?,?)', (d['decision_id'],run_id,'preview-'+d['decision_id'],digest(d),canonical(bundle),record['bundle_hash']))
        conn.execute('INSERT INTO outbox VALUES (?,?)', (d['decision_id'],canonical(record['notifications'])))
    assert store.replay(d['decision_id']) == record
    records.append(record)
main.store = store

async def synthetic_evaluate(store, run_id):
    await asyncio.sleep(3)
    body = store.run(run_id)['request']
    s = deepcopy(records[0]['snapshot'])
    s.update(snapshot_id=run_id, collected_at_utc=timestamp(),
             test_evidence_label='SYNTHETIC DESIGN TEST — no weather or model call',
             facility=store.facility(body['facility_id']))
    s['work_period'] = {**s['work_period'], **{k:body[k] for k in ('start','end','special_shift')}}
    s['work_period']['timezone'] = s['facility']['timezone']
    loc = {k:s['facility'][k] for k in ('latitude','longitude')}
    s['nws'].update(alerts=[], fetched_at_utc=timestamp(), request_location=loc,
                    raw_response_sha256=digest('SYNTHETIC DESIGN TEST'))
    s['air_quality'].update(fetched_at_utc=timestamp(), valid_at_utc=timestamp(),
                           requested_location=loc, returned_grid_location=loc, us_aqi=44,
                           hourly_forecast=[{'valid_at_utc':(parse_time(body['start'])+timedelta(hours=h)).isoformat(),'us_aqi':44}
                                            for h in range(25)])
    s['policy'] = load_rules()
    s['roster'] = roster(body['facility_id'],body['start'],body['end'])
    s['assessment'] = assess(s)
    store.save_snapshot(run_id,s)
    store.update_run(run_id,'evaluating')
    await asyncio.sleep(3)
    store.save_result(run_id, {'ai':{'status':'unavailable','narrative':'SYNTHETIC DESIGN TEST: no hosted inference invocation.',
                                    'safe_error_code':'DESIGN_PREVIEW_NO_INFERENCE'},'trace':[],
                               'metrics':{'model_calls':0,'source_http_attempts':0}},
                      'ready' if s['assessment']['review_status']=='ready_for_manager' else 'incomplete')
main.evaluate = synthetic_evaluate

@main.app.middleware('http')
async def block_sources(request, call_next):
    if request.url.path in ('/api/live-alerts','/api/facilities/demo-site'):
        return JSONResponse({'detail':'Isolated design QA: live provider calls are disabled'},status_code=403)
    return await call_next(request)

def forbidden(*args, **kwargs):
    raise AssertionError('External provider call forbidden in isolated design QA')
from app.clients import nws, air_quality, base
for module,name in [(base,'fetch_json'),(nws,'point'),(nws,'national'),(air_quality,'point')]:
    setattr(module,name,forbidden)
(ROOT/'data'/'design-preview-location.txt').write_text(str(FOLDER),encoding='utf-8')
print('Isolated design QA ready: original records exact; provider/model calls disabled',flush=True)
uvicorn.run(main.app,host='127.0.0.1',port=8084)
