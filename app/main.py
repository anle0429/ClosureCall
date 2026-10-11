import asyncio
from contextlib import asynccontextmanager
from datetime import timedelta
import json
from pathlib import Path
import sqlite3
import time
import uuid
from zoneinfo import ZoneInfo
from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from shapely.geometry import shape
from app.auth import manager
from app.db import Store
from app.schemas import EvaluationRequest, DecisionRequest, DemoSiteRequest
from app.services.audit import utcnow, parse_time
from app.services.decisions import decide, DecisionConflict
from app.services.evaluation import evaluate
from app.clients import nws
from app.settings import settings

store = Store(settings.database)
tasks = set()
explorer_cache = None
explorer_time = 0
explorer_lock = asyncio.Lock()

@asynccontextmanager
async def lifespan(app):
    store.initialize()
    yield
    for task in tasks:
        task.cancel()
    if tasks:
        await asyncio.gather(*tasks,return_exceptions=True)

app = FastAPI(title='ClosureCall prototype', lifespan=lifespan)
api = APIRouter(prefix='/api', dependencies=[Depends(manager)])
static = Path(__file__).parent/'static'

@app.middleware('http')
async def headers(request, call_next):
    response = await call_next(request)
    response.headers['Cache-Control'] = 'no-store'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Referrer-Policy'] = 'no-referrer'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self' data:; frame-ancestors 'none'; base-uri 'none'; form-action 'self'"
    return response

@app.get('/health')
def health():
    return {'status':'ok','product':'ClosureCall','prototype':True}

@app.get('/')
def index():
    return FileResponse(static/'index.html')

@api.get('/config')
def config():
    return {'environment':settings.environment,'deployment':settings.deployment,'build':settings.build,
            'ai_mode':'configured' if settings.ai_available else 'unavailable',
            'notification_mode':'outbox_only', 'prototype':True}

@api.get('/facilities')
def facilities():
    return store.facilities()

async def national_cached():
    global explorer_cache, explorer_time
    async with explorer_lock:
        if explorer_cache is None or time.monotonic()-explorer_time >= 300:
            explorer_cache = await nws.national()
            explorer_time = time.monotonic()
        return explorer_cache

@api.get('/live-alerts')
async def live_alerts():
    data = await national_cached()
    return {**data,'mode':'LIVE','alerts': [x for x in data['alerts'] if x['event'] in nws.SUPPORTED][:50],
            'national_total':len(data['alerts']), 'display_limit':50}

@api.post('/facilities/demo-site', status_code=201)
async def demo_site(body: DemoSiteRequest):
    data = await national_cached()
    alert = next((x for x in data['alerts'] if x['alert_id']==body.alert_id and x['event'] in nws.SUPPORTED),None)
    if alert is None or not alert.get('geometry'):
        raise HTTPException(422,'No supported alert polygon; manual verified zone location needed')
    try:
        polygon = shape(alert['geometry'])
        if not polygon.is_valid or polygon.is_empty or polygon.geom_type not in ('Polygon','MultiPolygon'):
            raise ValueError('Invalid polygon')
        point = polygon.representative_point()
    except (ValueError,TypeError,KeyError):
        raise HTTPException(422,'Invalid NWS polygon')
    confirmed = await nws.point(point.y,point.x)
    if confirmed['status']!='available' or not any(x['alert_id']==body.alert_id and x.get('applicability_status')=='point_confirmed' for x in confirmed['alerts']):
        raise HTTPException(409,'Point endpoint did not confirm this alert')
    from app.clients.base import fetch_json
    # NWS normalizes point metadata to four decimal places with a redirect.
    # Use its canonical coordinate precision without enabling arbitrary redirects.
    point_info, _ = await fetch_json(f'https://api.weather.gov/points/{point.y:.4f},{point.x:.4f}',nws=True)
    try:
        zone = point_info['properties']['timeZone']
        ZoneInfo(zone)
    except (TypeError,KeyError,ValueError):
        raise HTTPException(409,'Facility timezone could not be verified')
    facility = {**store.facility('kc-demo'), 'facility_id':'site-'+str(uuid.uuid4()),
        'display_name':f"Synthetic site — {alert['event']}", 'latitude':point.y, 'longitude':point.x,
        'timezone':zone,'source_alert_id':body.alert_id,'location_verification':'NWS point endpoint confirmed'}
    store.add_facility(facility)
    return facility

def get_run(id):
    try:
        return store.run(id)
    except KeyError:
        raise HTTPException(404,'Unknown evaluation')
    except ValueError:
        raise HTTPException(409,'Snapshot integrity failure')

@api.post('/evaluations',status_code=202)
async def evaluations(body: EvaluationRequest, idempotency_key: str = Header(min_length=8,max_length=150)):
    try:
        facility = store.facility(body.facility_id)
    except KeyError:
        raise HTTPException(404,'Unknown facility')
    local = body.start.astimezone(ZoneInfo(facility['timezone']))
    if local.weekday() not in facility['working_days'] and not body.special_shift:
        raise HTTPException(422,'Weekend work requires explicitly labeled synthetic special shift')
    if body.end <= utcnow() or body.start > utcnow()+timedelta(days=1):
        raise HTTPException(422,'Live work period must end in the future and begin within 24 hours')
    try:
        id, created = store.create_run(body.model_dump(mode='json'),idempotency_key)
    except sqlite3.IntegrityError:
        raise HTTPException(409,'Evaluation busy — wait for the active run')
    except ValueError as exc:
        raise HTTPException(409,str(exc))
    if created:
        task = asyncio.create_task(evaluate(store,id))
        tasks.add(task)
        task.add_done_callback(tasks.discard)
    return {'run_id':id, 'mode':'LIVE', 'created':created}

@api.get('/evaluations')
def recent():
    return store.recent()

@api.get('/evaluations/{id}')
def evaluation(id: str):
    return get_run(id)

@api.get('/evaluations/{id}/trace')
def trace(id: str):
    return get_run(id).get('trace',[])

@api.post('/evaluations/{id}/decision')
def decision(id: str, body: DecisionRequest, actor: str=Depends(manager),
             idempotency_key: str=Header(min_length=8,max_length=150)):
    get_run(id)
    try:
        return decide(store,id,body,actor,idempotency_key)
    except DecisionConflict as exc:
        raise HTTPException(409,str(exc))

@api.get('/decisions')
def decisions():
    return store.decisions()

def replay_record(id):
    try:
        return store.replay(id)
    except KeyError:
        raise HTTPException(404,'Unknown decision')
    except ValueError:
        raise HTTPException(409,'Historical integrity check failed')

@api.get('/decisions/{id}')
def decision_record(id: str):
    return replay_record(id)['decision']

@api.get('/decisions/{id}/replay')
def replay(id: str):
    return replay_record(id)

@api.get('/decisions/{id}/notifications')
def notifications(id: str):
    return replay_record(id)['notifications']

@api.get('/decisions/{id}/export')
def export(id: str):
    return Response(json.dumps(replay_record(id),indent=2),media_type='application/json',
                    headers={'Content-Disposition':f'attachment; filename="closurecall-{uuid.UUID(id)}.json"'})

@api.get('/decisions/{id}/memo')
def memo(id: str):
    from app.services.memo import render_memo
    return Response(render_memo(replay_record(id)), media_type='text/html',
                    headers={'Content-Disposition':f'attachment; filename="closurecall-memo-{uuid.UUID(id)}.html"'})

@api.get('/decisions/{id}/notifications/{employee_id}/export')
def message_export(id: str, employee_id: str):
    from email.message import EmailMessage
    people = replay_record(id)['notifications']['recipients']
    person = next((x for x in people if x['employee_id']==employee_id),None)
    if not person:
        raise HTTPException(404,'Unknown synthetic recipient')
    message = EmailMessage()
    message['To'] = person['email']
    message['From'] = 'closurecall-demo@example.com'
    message['Subject'] = person['subject']
    message.set_content(person['message'])
    return Response(message.as_bytes(),media_type='message/rfc822',headers={'Content-Disposition':'attachment; filename="prototype-draft.eml"'})

app.include_router(api)
app.mount('/static',StaticFiles(directory=static),name='static')
