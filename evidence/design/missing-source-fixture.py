"""Seed one clearly synthetic failure presentation case in the design QA DB only."""
from copy import deepcopy
from datetime import timedelta
import json
from pathlib import Path
import sys
import uuid

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from app.db import Store
from app.services.audit import timestamp,utcnow,digest
from app.services.recipients import roster
from app.policy.engine import load_rules,assess
from app.schemas import DecisionRequest
from app.services.decisions import decide

folder=Path((ROOT/'data/design-preview-location.txt').read_text().strip())
assert folder.resolve().is_relative_to((ROOT/'data').resolve()) and folder.name.startswith('design-preview-')
store=Store(folder/'isolated.sqlite3')
original=json.loads((ROOT/'evidence/release/ui-approved-export.json').read_text(encoding='utf-8'))
s=deepcopy(original['snapshot'])
now=utcnow();start=now+timedelta(minutes=15);end=start+timedelta(hours=2)
body={'facility_id':'kc-demo','start':start.isoformat(),'end':end.isoformat(),'special_shift':True}
run_id,_=store.create_run(body,'synthetic-missing-source-'+uuid.uuid4().hex)
s.update(snapshot_id=run_id,collected_at_utc=timestamp(),
         test_evidence_label='SYNTHETIC DESIGN FAILURE CASE — no provider or model call')
s['work_period'].update(start=body['start'],end=body['end'],special_shift=True)
s['nws'].update(status='unavailable',fetched_at_utc=timestamp(),response_status=None,alerts=[],
                safe_error_code='SYNTHETIC_TIMEOUT',raw_response_sha256=digest('SYNTHETIC MISSING SOURCE'))
s['air_quality'].update(fetched_at_utc=timestamp(),valid_at_utc=timestamp(),us_aqi=44,
                       hourly_forecast=[{'valid_at_utc':(start+timedelta(hours=h)).isoformat(),'us_aqi':44} for h in range(3)])
s['policy']=load_rules();s['roster']=roster('kc-demo',body['start'],body['end'])
s['assessment']=assess(s)
assert s['assessment']['recommended_posture'] is None and s['assessment']['review_status']=='data_incomplete'
store.save_snapshot(run_id,s)
store.save_result(run_id,{'ai':{'status':'degraded','safe_error_code':'SYNTHETIC_MODEL_FAILURE',
                             'narrative':'SYNTHETIC UI CASE: no hosted inference attempted. Deterministic incomplete assessment retained.'},
                         'trace':[],'metrics':{'source_http_attempts':0,'model_calls':0}},'incomplete')
request=DecisionRequest(snapshot_hash=digest(s),action='override',posture='closure',
                        reason='SYNTHETIC UI PRESENTATION CASE ONLY: missing NWS evidence requires explicit review. This seeded override does not verify local conditions or send a notice.')
record=decide(store,run_id,request,'synthetic-design-case','synthetic-case-decision-'+uuid.uuid4().hex)
(ROOT/'evidence/design/missing-source-case.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print('Synthetic missing-source presentation case stored in isolated design DB; no external calls')
