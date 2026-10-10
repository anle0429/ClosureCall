import math
from app.clients.base import fetch_json
from app.services.audit import parse_time

def normalize(body, meta, location):
    evidence = {**meta, 'source_id': 'aq', 'requested_location': location, 'modeled': True,
                'attribution': 'Open-Meteo / Copernicus Atmosphere Monitoring Service (CAMS)',
                'us_aqi': None, 'pm2_5': None, 'valid_at_utc': None, 'hourly_forecast': []}
    if body is None:
        return evidence
    try:
        current = body['current']
        valid = parse_time(current['time'])
        evidence.update(returned_grid_location={'latitude': body['latitude'], 'longitude': body['longitude']},
                        valid_at_utc=valid.isoformat(), units=body.get('current_units', {}))
        for field in ('us_aqi', 'pm2_5'):
            value = current.get(field)
            if value is not None and (not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0):
                raise ValueError('Invalid AQ value')
            evidence[field] = value
        hourly = body.get('hourly', {})
        times, values = hourly.get('time', []), hourly.get('us_aqi', [])
        if len(times) != len(values):
            raise ValueError('Mismatched hourly data')
        for t, value in zip(times, values):
            if value is not None and (not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0):
                raise ValueError('Invalid AQ forecast')
            evidence['hourly_forecast'].append({'valid_at_utc': parse_time(t).isoformat(), 'us_aqi': value})
        if evidence['us_aqi'] is None:
            evidence['status'] = 'missing'
    except (KeyError, TypeError, ValueError, AttributeError):
        evidence.update(status='unavailable', safe_error_code='InvalidAirQuality')
    return evidence

async def point(latitude, longitude):
    body, meta = await fetch_json('https://air-quality-api.open-meteo.com/v1/air-quality',
        {'latitude': latitude, 'longitude': longitude, 'current': 'us_aqi,pm2_5',
         'hourly': 'us_aqi', 'forecast_days': 2, 'timezone': 'UTC'})
    return normalize(body, meta, {'latitude': latitude, 'longitude': longitude})
