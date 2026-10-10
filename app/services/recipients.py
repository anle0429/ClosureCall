from app.services.audit import parse_time

def roster(facility_id, start, end):
    names = ['Avery Hart', 'Blair Reed', 'Casey Brook', 'Drew Vale', 'Ellis Lane', 'Finley Stone',
             'Gray Morgan', 'Harper Quinn', 'Indigo Ray', 'Jordan Lake', 'Kai Rowan', 'Logan Fern']
    result = []
    for i, name in enumerate(names):
        result.append({'employee_id': f'demo-{i+1:02}', 'name': name,
            'email': f'employee{i+1}@example.com', 'synthetic': True, 'roster_version': 'synthetic-v1',
            'essential': i in (7, 8), 'telework_eligible': i < 5 or i == 9,
            'assignment': 'telework' if i == 9 else 'offsite' if i == 10 else 'no_shift' if i == 11 else 'onsite',
            'assigned_facility_id': 'other-demo-site' if i == 10 else facility_id,
            'assignment_start': start, 'assignment_end': end,
            'preferred_channel': 'voice_accessible' if i == 2 else 'app_inbox'})
    return result

def route(snapshot, posture):
    result = []
    start, end = parse_time(snapshot['work_period']['start']), parse_time(snapshot['work_period']['end'])
    for person in snapshot['roster']:
        status, channel, reason = 'included', person['preferred_channel'], 'Assigned onsite in affected work period'
        if person['assignment'] == 'no_shift':
            status, channel, reason = 'excluded', None, 'No assigned shift during affected work period'
        elif person['assigned_facility_id'] != snapshot['facility']['facility_id'] or person['assignment'] == 'offsite':
            status, channel, reason = 'excluded', None, 'Current detail/assignment is at another site'
        elif parse_time(person['assignment_start']) >= end or parse_time(person['assignment_end']) <= start:
            status, channel, reason = 'excluded', None, 'Assignment does not overlap affected work period'
        elif person['assignment'] == 'telework':
            status, channel, reason = 'deferred', 'app_inbox', 'Already scheduled for telework; informational inbox only'
        if person['essential']:
            instruction = 'Essential personnel: reporting requirements remain subject to supervisor direction. Contact the designated supervisor; follow local emergency procedures.'
        elif posture == 'telework' and person['telework_eligible']:
            instruction = 'Use approved telework arrangements for the affected work period; contact your supervisor for task coordination.'
        elif posture in ('closure', 'telework'):
            instruction = 'Routine onsite reporting is affected. Contact your supervisor for approved work or leave arrangements; this prototype does not grant paid leave.'
        elif posture == 'delayed_arrival':
            instruction = 'Report only at the manager-confirmed opening time shown in this decision; contact your supervisor if travel conditions prevent reporting.'
        elif posture == 'early_dismissal':
            instruction = 'Use the manager-confirmed timing and established local procedures. Do not depart into an imminent hazard automatically.'
        else:
            instruction = 'No supported prototype trigger found. Continue assigned duties and monitor official updates and supervisor instructions.'
        if status == 'excluded':
            instruction = 'No urgent instruction for this site assignment.'
        if status == 'deferred':
            instruction = 'Informational update only; continue scheduled telework unless your supervisor directs otherwise.'
        follow_up = None
        if status == 'deferred':
            follow_up = ('Supervisor reviews the informational draft before the assigned shift starts, '
                'or immediately if the shift is already underway. If the employee is reassigned onsite, '
                're-evaluate the updated assignment and record a new manager decision; otherwise continue scheduled telework. '
                'This is a manual follow-up step, not an automatic send or scheduled job.')
        result.append({**person, 'routing_status': status, 'channel': channel, 'reason': reason,
                       'instruction': instruction, 'follow_up': follow_up})
    return result
