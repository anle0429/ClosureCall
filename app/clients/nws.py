from app.clients.base import fetch_json
from app.services.audit import parse_time, utcnow
import re
from shapely.geometry import Point, shape
from shapely.errors import GEOSException

FIELDS = {'event':'event', 'status':'status', 'message_type':'messageType', 'severity':'severity',
          'certainty':'certainty', 'urgency':'urgency', 'sent':'sent', 'effective':'effective',
          'onset':'onset', 'expires':'expires', 'ends':'ends', 'area_desc':'areaDesc',
          'affected_zones':'affectedZones', 'headline':'headline', 'description':'description',
          'instruction':'instruction', 'references':'references', 'geocode':'geocode'}
SUPPORTED = {'Flash Flood Warning', 'Flood Warning', 'High Wind Warning'}

def location_scope(alert, location):
    if location is None:
        return 'unverified', 'National explorer only; point confirmation required'
    geometry = alert.get('geometry')
    if geometry is not None:
        try:
            polygon = shape(geometry)
            if polygon.geom_type not in ('Polygon', 'MultiPolygon') or polygon.is_empty or not polygon.is_valid:
                raise ValueError('Invalid polygon')
            west, south, east, north = polygon.bounds
            if not (-180 <= west <= east <= 180 and -90 <= south <= north <= 90):
                raise ValueError('Invalid geographic bounds')
            point = Point(location['longitude'], location['latitude'])
            if polygon.covers(point):
                return 'point_confirmed', 'NWS point response and supplied polygon cover the facility point'
            return 'outside_polygon', 'Facility point is outside the supplied alert polygon; point response and polygon disagree for this site'
        except (ValueError, TypeError, KeyError, AttributeError, IndexError, GEOSException):
            return 'unverified', 'Supplied geometry cannot verify facility applicability; manager review required'
    geocode = alert.get('geocode') or {}
    ugcs = geocode.get('UGC', []) if isinstance(geocode, dict) else []
    zones = alert.get('affected_zones') or []
    has_scope = (isinstance(ugcs, list) and any(isinstance(code, str) and re.fullmatch(r'[A-Z]{2}[CZ]\d{3}', code) for code in ugcs))
    has_scope = has_scope or (isinstance(zones, list) and any(isinstance(url, str) and
        re.fullmatch(r'https://api\.weather\.gov/zones/(?:county|forecast|fire|marine)/[A-Z]{2}[CZ]\d{3}', url) for url in zones))
    if has_scope:
        return 'point_confirmed', 'NWS point filter resolved county/zone scope; geometry is null, no independent zone-boundary check'
    return 'unverified', 'No usable polygon or county/zone scope in the point response; manager review required'

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
            alert['applicability_status'], alert['applicability_reason'] = location_scope(alert, location)
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
    if alert.get('status') != 'Actual' or alert.get('message_type') not in ('Alert', 'Update'):
        return False, 'Non-actual, cancelled or unsupported message type'
    try:
        effective = parse_time(alert.get('onset') or alert.get('effective'))
        expires = parse_time(alert.get('ends') or alert.get('expires'))
        if effective is None or expires is None:
            return False, 'Missing validity window; manager review required'
        # The current message cannot supply work-period coverage beyond its expiry.
        message_expires = parse_time(alert.get('expires'))
        if expires <= now or (message_expires and message_expires <= now):
            return False, 'Expired alert; expiration is not proof of safety'
        if message_expires:
            expires = min(expires, message_expires)
        if effective >= expires:
            return False, 'Invalid validity window; manager review required'
        overlap_start, overlap_end = max(effective, start), min(expires, end)
        if overlap_start >= overlap_end:
            return False, 'No work-period overlap'
        if alert.get('applicability_status') == 'outside_polygon':
            return False, alert.get('applicability_reason') or 'Facility point outside alert polygon'
        if alert.get('applicability_status') != 'point_confirmed':
            return False, 'Location not verified; manager review required'
        return True, f'Work-period overlap: {overlap_start.isoformat()} → {overlap_end.isoformat()}; no validity inferred outside this interval'
    except (ValueError, TypeError):
        return False, 'Invalid validity window; manager review required'
