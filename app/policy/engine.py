import json
from pathlib import Path
from app.clients.nws import applicability, SUPPORTED
from app.services.audit import parse_time, utcnow
from app.schemas import Assessment
from app.settings import settings

def load_rules():
    return json.loads(Path(__file__).with_name('rules.json').read_text(encoding='utf-8'))

def assess(snapshot, now=None):
    now = now or utcnow()
    start, end = parse_time(snapshot['work_period']['start']), parse_time(snapshot['work_period']['end'])
    nws, aq = snapshot['nws'], snapshot['air_quality']
    policy = snapshot['policy']
    missing, matches, ids, unsupported = [], [], [], []
    posture = None
    if nws['status'] != 'available' or not nws.get('location_verified'):
        missing.append('NWS feed unavailable or location unverified')
    else:
        age = (now - parse_time(nws['fetched_at_utc'])).total_seconds()
        if age > settings.nws_freshness or age < -60:
            missing.append('NWS feed retrieval stale or invalid')
        location = nws.get('request_location', {})
        if (location.get('latitude'), location.get('longitude')) != (snapshot['facility']['latitude'], snapshot['facility']['longitude']):
            missing.append('NWS request location differs from facility')
    rules = {r['id']: r for r in policy['rules']}
    referenced = set()
    for alert in nws['alerts']:
        if (alert.get('status') == 'Actual' and alert.get('message_type') in ('Update', 'Cancel')
                and alert.get('applicability_status') == 'point_confirmed'):
            for ref in alert.get('references') or []:
                if isinstance(ref, dict):
                    referenced.add(ref.get('identifier'))
    for alert in nws['alerts']:
        applies, reason = applicability(alert, start, end, now)
        if alert['alert_id'] in referenced:
            continue
        if not applies:
            if 'Missing validity' in reason or 'Invalid validity' in reason or 'Location not verified' in reason:
                missing.append(f"Alert {alert['alert_id']}: {reason}")
            continue
        ids.append(alert['alert_id'])
        if alert['event'] not in SUPPORTED:
            unsupported.append(alert['event'])
            continue
        rule_id = None
        if alert['event'] in ('Flood Warning', 'Flash Flood Warning') and alert['severity'] in ('Severe', 'Extreme'):
            rule_id = 'FLOOD_WARNING'
        elif alert['event'] == 'High Wind Warning':
            rule_id = 'WIND_WARNING'
        if rule_id:
            rule = rules[rule_id]
            proposed = rule['proposed_posture']
            if proposed == 'telework' and not snapshot['facility']['telework_supported']:
                missing.append('Telework unsupported; manager must select an operating posture')
                continue
            matches.append({**rule, 'observed_value': alert['event'], 'exceedance': None,
                            'categorical_match_reason': f"{alert['severity']} / {alert['certainty']} / {alert['urgency']}; {reason}",
                            'evidence_id': alert['alert_id']})
            if proposed == 'closure' or posture != 'closure':
                posture = proposed
    aq_location = aq.get('requested_location', {})
    samples = []
    if aq['status'] != 'available' or aq.get('us_aqi') is None:
        missing.append('Modeled AQ unavailable or null')
    else:
        fetched = parse_time(aq['fetched_at_utc'])
        valid = parse_time(aq['valid_at_utc'])
        if (now - fetched).total_seconds() > settings.nws_freshness or abs((now - valid).total_seconds()) > settings.aq_max_age:
            missing.append('Modeled AQ valid time or retrieval stale')
        elif (aq_location.get('latitude'), aq_location.get('longitude')) != (snapshot['facility']['latitude'], snapshot['facility']['longitude']):
            missing.append('AQ request location differs from facility')
        else:
            # Each hourly value represents [valid time, valid time + 1 hour).
            from datetime import timedelta
            samples = [(parse_time(x['valid_at_utc']), x['us_aqi']) for x in aq['hourly_forecast']
                       if start <= parse_time(x['valid_at_utc']) < end or
                       parse_time(x['valid_at_utc']) < start < parse_time(x['valid_at_utc']) + timedelta(hours=1)]
            if not samples or any(value is None for _, value in samples):
                missing.append('AQ forecast missing for selected work period')
            elif (samples[0][0] > start or samples[-1][0] + timedelta(hours=1) < end
                  or any(b[0]-a[0] != timedelta(hours=1) for a,b in zip(samples,samples[1:]))):
                missing.append('AQ forecast does not cover entire selected work period')
            else:
                value = max(value for _, value in samples)
                ids.append('aq')
                if value >= rules['AQ_151']['threshold']:
                    if snapshot['facility']['telework_supported']:
                        matches.append({**rules['AQ_151'], 'observed_value': value,
                            'exceedance': value - rules['AQ_151']['threshold'],
                            'categorical_match_reason': None, 'evidence_id': 'aq'})
                        if posture != 'closure':
                            posture = 'telework'
                    else:
                        missing.append('AQ trigger but facility does not support telework')
    if missing:
        review = 'data_incomplete'
        if any('NWS' in text for text in missing):
            posture = None
        # Keep supported protective trigger as candidate; never infer normal on missing data.
        rationale = 'Assessment incomplete. ' + '; '.join(missing)
    elif unsupported:
        review = 'unsupported_hazard'
        rationale = 'Unsupported hazard — manager review: ' + ', '.join(unsupported)
    else:
        review = 'ready_for_manager'
        posture = posture or 'normal'
        rationale = 'Supported prototype triggers: ' + ', '.join(m['id'] for m in matches) if matches else 'No supported trigger found in fetched evidence; this is not a safety guarantee.'
    notice = 'Closure does not mean evacuation. Follow official NWS instructions and established local emergency procedures; essential reporting requirements require supervisor direction.'
    if posture == 'closure' and start <= now < end:
        notice = 'Hazard overlaps an ongoing shift. Do not direct employees outdoors automatically. ' + notice
    return Assessment(recommended_posture=posture, review_status=review, rationale_text=rationale,
        matched_rules=matches, evidence_ids=ids, confidence_label='low' if missing or unsupported else 'moderate',
        confidence_basis=['Completeness/applicability rubric, not probability of correctness',
                          'Modeled AQ does not establish indoor conditions'], missing_inputs=missing,
        what_would_change=['New NWS warning/update or point applicability', 'AQ valid time / forecast changes',
                          'Manager verifies local access, timing or facility conditions'],
        protective_action_notice=notice, assumptions=[policy['disclaimer'],
        'Fetch freshness and AQ age budgets are engineering assumptions.',
        'Delay and early dismissal are manager-selectable with verified timing; not automatic recommendations.'],
        policy_version=policy['version']).model_dump()
