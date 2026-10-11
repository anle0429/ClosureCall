"""Ignored, isolated read-only browser harness; never production data or live calls."""
import json
import os
from pathlib import Path
import sys
root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root))
from datetime import datetime, timezone
folder = root / 'data' / ('feedback-preview-reproduce-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
folder.mkdir(exist_ok=True)
db = folder / 'isolated.sqlite3'
if db.exists():
    raise SystemExit('Preview DB exists; refusing overwrite')
os.environ.update(DATABASE_PATH=str(db), INFERENCE_API_KEY='', MANAGER_USERNAME='feedback-preview',
                  MANAGER_PASSWORD='synthetic-preview-only-password', APP_ENV='feedback-preview',
                  DEPLOYMENT_LABEL='Offline read-only feedback candidate preview', BUILD_COMMIT='656e8a0a5ee78d89064ddb47318bd2ec75e0b899')
from app.db import Store
from app.services.audit import canonical, digest
from app.services.memo import render_memo
import app.main as main
from fastapi.responses import JSONResponse
import uvicorn
store = Store(db)
store.initialize()
records = []
for name in ['ui-approved-export.json', 'ui-override-export.json']:
    record = json.loads((root / 'evidence' / 'release' / name).read_text(encoding='utf-8'))
    s, d = record['snapshot'], record['decision']
    run_id = d['evaluation_id']
    request = {'facility_id': s['facility']['facility_id'], **{key:s['work_period'][key] for key in ('start', 'end', 'special_shift')}}
    bundle = {key:value for key,value in record.items() if key not in ('mode', 'bundle_hash')}
    assert digest(bundle) == record['bundle_hash'] and digest(s) == record['snapshot_hash']
    with store.connection() as conn:
        conn.execute('INSERT OR IGNORE INTO facilities VALUES (?,?)', (s['facility']['facility_id'], canonical(s['facility'])))
        conn.execute('INSERT INTO runs VALUES (?,?,?,?,?,?,?)', (run_id, s['facility']['facility_id'], 'ready', s['collected_at_utc'], canonical(request), None, 'preview-'+run_id))
        conn.execute('INSERT INTO snapshots VALUES (?,?,?)', (run_id, canonical(s), record['snapshot_hash']))
        conn.execute('INSERT INTO results VALUES (?,?)', (run_id, canonical({key:record[key] for key in ('ai', 'trace', 'metrics')})))
        conn.execute('INSERT INTO decisions VALUES (?,?,?,?,?,?)', (d['decision_id'], run_id, 'preview-'+d['decision_id'], digest(d), canonical(bundle), record['bundle_hash']))
        conn.execute('INSERT INTO outbox VALUES (?,?)', (d['decision_id'], canonical(record['notifications'])))
    assert store.replay(d['decision_id']) == record
    (folder / (name.replace('.json', '.html'))).write_text(render_memo(record), encoding='utf-8')
    records.append(record)
main.store = store
@main.app.middleware('http')
async def read_only(request, call_next):
    if request.method not in ('GET', 'HEAD') or request.url.path == '/api/live-alerts':
        return JSONResponse({'detail': 'Offline read-only feedback preview: no live calls or manager writes'}, status_code=403)
    return await call_next(request)
from app.clients import nws, air_quality
import app.clients.base as base
import app.services.evaluation as evaluation
def forbidden(*args, **kwargs):
    raise AssertionError('Preview must not call providers or recompute')
for module, name in [(base,'fetch_json'),(nws,'point'),(nws,'national'),(air_quality,'point'),
                     (evaluation,'bounded_worker'),(evaluation,'assess'),(evaluation,'load_rules'),(evaluation,'roster')]:
    setattr(module,name,forbidden)
print('Offline read-only preview initialized; two historical exports exact; providers blocked', flush=True)
uvicorn.run(main.app, host='127.0.0.1', port=8083)
