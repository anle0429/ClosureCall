from app.services.recipients import route

def test_all_12_routes_explained(snapshot):
    people=route(snapshot,'telework')
    assert len(people)==12
    assert all(p['reason'] and p['instruction'] for p in people)
    assert sum(p['routing_status']=='included' for p in people)==9
    assert sum(p['routing_status']=='excluded' for p in people)==2
    assert sum(p['routing_status']=='deferred' for p in people)==1

def test_essential_accessibility_nontelework(snapshot):
    people=route(snapshot,'closure')
    assert all('reporting requirements' in p['instruction'] for p in people if p['essential'])
    assert people[2]['channel']=='voice_accessible'
    assert 'paid leave' in people[5]['instruction']

def test_no_urgent_broadcast_offsite_or_telework(snapshot):
    people=route(snapshot,'closure')
    assert people[9]['routing_status']=='deferred' and people[9]['channel']=='app_inbox'
    assert people[10]['routing_status']=='excluded' and people[10]['channel'] is None
    assert people[11]['routing_status']=='excluded'

def test_assignment_window_not_home_facility(snapshot):
    snapshot['roster'][0]['assignment_start']=snapshot['work_period']['end']
    assert route(snapshot,'closure')[0]['routing_status']=='excluded'
