from copy import deepcopy
from datetime import timedelta
import pytest
from app.db import Store
from app.policy.engine import load_rules, assess
from app.services.audit import utcnow, digest
from app.services.recipients import roster

@pytest.fixture
def store(tmp_path):
    result=Store(tmp_path/'synthetic.sqlite3')
    result.initialize()
    return result

@pytest.fixture
def snapshot(store):
    now=utcnow()
    start=now.replace(minute=0,second=0,microsecond=0)+timedelta(hours=1)
    end=start+timedelta(hours=2)
    location={'latitude':39.0997,'longitude':-94.5786}
    body={'mode':'LIVE','test_evidence_label':'SYNTHETIC TEST ONLY — never live fallback',
        'snapshot_id':'synthetic-run', 'collected_at_utc':now.isoformat(), 'facility':store.facility('kc-demo'),
        'work_period':{'start':start.isoformat(),'end':end.isoformat(),'special_shift':True,
                       'selected_work_date':start.date().isoformat(),'timezone':'America/Chicago','operating_context':'before_open'},
        'nws':{'source_id':'nws','status':'available','fetched_at_utc':now.isoformat(),
               'response_status':200,'location_verified':True,'request_location':location,
               'raw_response_sha256':digest('SYNTHETIC'),'source_url':'https://api.weather.gov/alerts/active?point=39.0997,-94.5786','alerts':[]},
        'air_quality':{'source_id':'aq','status':'available','us_aqi':44,'pm2_5':6,
            'modeled':True,'requested_location':location,'returned_grid_location':location,
            'fetched_at_utc':now.isoformat(),'valid_at_utc':now.isoformat(),'response_status':200,
            'source_url':'https://air-quality-api.open-meteo.com/v1/air-quality','attribution':'Open-Meteo / CAMS',
            'hourly_forecast':[{'valid_at_utc':(start+timedelta(hours=h)).isoformat(),'us_aqi':44} for h in range(2)]},
        'policy':load_rules(),'roster':roster('kc-demo',start.isoformat(),end.isoformat()),'roster_version':'synthetic-v1'}
    body['assessment']=assess(body,now)
    return body

@pytest.fixture
def alert(snapshot):
    return {'alert_id':'SYNTHETIC-ALERT-01','event':'Flash Flood Warning','status':'Actual','message_type':'Alert',
            'severity':'Severe','certainty':'Observed','urgency':'Immediate',
            'effective':snapshot['work_period']['start'],'onset':snapshot['work_period']['start'],
            'sent':snapshot['collected_at_utc'],'expires':snapshot['work_period']['end'],'ends':snapshot['work_period']['end'],
            'area_desc':'SYNTHETIC TEST AREA','headline':'SYNTHETIC WARNING','description':'Synthetic test only',
            'instruction':'Follow official instructions','applicability_status':'point_confirmed',
            'applicability_reason':'Synthetic point fixture','references':[]}

def persist(store,snapshot,key='synthetic-evaluation-key'):
    body={'facility_id':snapshot['facility']['facility_id'],**{k:snapshot['work_period'][k] for k in ('start','end','special_shift')}}
    id,_=store.create_run(body,key)
    snap=deepcopy(snapshot)
    snap['snapshot_id']=id
    snap['assessment']=assess(snap)
    store.save_snapshot(id,snap)
    store.save_result(id,{'ai':{'status':'unavailable','narrative':'Synthetic test — no inference call'},'trace':[]},
                      'ready' if snap['assessment']['review_status']=='ready_for_manager' else 'incomplete')
    return store.run(id)
