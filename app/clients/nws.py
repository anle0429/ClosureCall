from app.clients.base import fetch_json
from app.services.audit import parse_time, utcnow

FIELDS = {'event':'event', 'status':'status', 'message_type':'messageType', 'severity':'severity',
          'certainty':'certainty', 'urgency':'urgency', 'sent':'sent', 'effective':'effective',
          'onset':'onset', 'expires':'expires', 'ends':'ends', 'area_desc':'areaDesc',
          'affected_zones':'affectedZones', 'headline':'headline', 'description':'description',
          'instruction':'instruction', 'references':'references'}
SUPPORTED = {'Flash Flood Warning', 'Flood Warning', 'High Wind Warning'}

def normalize(body, meta, location=None):
    evidence = {**meta, 'source_id': 'nws', 'request_location': location, 'alerts': [],
                'location_verified': location is not None}
    if body is None:
        return evidence
    if body.get('type') != 'FeatureCollection' or not isinstance(body.get('features'), list):
        return {**evidence, 'status': 'unavailable', 'safe_error_code': 'InvalidFeatureCollection'}
    try:
        for feature in body['features']:
            props = feature['properties']
            alert = {key: props.get(source) for key, source in FIELDS.items()}
            alert.update(alert_id=props.get('id') or feature['id'], geometry=feature.get('geometry'))
            alert['applicability_status'] = 'point_confirmed' if location else 'unverified'
            alert['applicability_reason'] = 'Returned by NWS point endpoint' if location else 'National explorer only; point confirmation required'
            evidence['alerts'].append(alert)
    except (KeyError, TypeError):
        return {**evidence, 'alerts': [], 'status': 'unavailable', 'safe_error_code': 'InvalidAlert'}
    return evidence

async def point(latitude, longitude):
    body, meta = await fetch_json('https://api.weather.gov/alerts/active',
                                  {'point': f'{latitude},{longitude}'}, nws=True)
    return normalize(body, meta, {'latitude': latitude, 'longitude': longitude})

async def national():
    body, meta = await fetch_json('https://api.weather.gov/alerts/active', nws=True)
    return normalize(body, meta)

def applicability(alert, start, end, now=None):
    now = now or utcnow()
    if alert.get('applicability_status') != 'point_confirmed':
        return False, 'Location not verified'
    if alert.get('status') != 'Actual' or alert.get('message_type') not in ('Alert', 'Update'):
        return False, 'Non-actual, cancelled or unsupported message type'
    try:
        effective = parse_time(alert.get('onset') or alert.get('effective'))
        expires = parse_time(alert.get('ends') or alert.get('expires'))
        if effective is None or expires is None:
            return False, 'Missing validity window; manager review required'
        # ends can exceed expires; expiration of the current message must also be respected.
        message_expires = parse_time(alert.get('expires'))
        if expires <= now or (message_expires and message_expires <= now):
            return False, 'Expired alert; expiration is not proof of safety'
        return effective < end and expires > start, 'Work-period overlap checked'
    except (ValueError, TypeError):
        return False, 'Invalid validity window; manager review required'
