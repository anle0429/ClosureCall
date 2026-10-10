"""Validate model-selected review references; render facts from frozen evidence only."""
import json
from collections import Counter
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field
from app.services.recipients import route

Focus = Literal['LOCAL_ACCESS', 'UNMAPPED_HAZARDS', 'ESSENTIAL_DIRECTIONS', 'MODELED_AQ_LIMITS']
class ReviewSelection(BaseModel):
    model_config = ConfigDict(extra='forbid')
    snapshot_id: str
    policy_version: str
    evidence_ids: list[str] = Field(min_length=1,max_length=100)
    review_focus: list[Focus] = Field(min_length=1,max_length=4)

def allowed_evidence_ids(snapshot):
    allowed={snapshot['snapshot_id'],snapshot['air_quality']['source_url']}
    allowed.update(item['alert_id'] for item in snapshot['nws']['alerts'])
    return allowed

def grounded_brief(text, snapshot):
    selection=ReviewSelection.model_validate(json.loads(text))
    a=snapshot['assessment']
    allowed=allowed_evidence_ids(snapshot)
    if selection.snapshot_id!=snapshot['snapshot_id'] or selection.policy_version!=snapshot['policy']['version']:
        raise ValueError('Brief outside frozen run')
    if not set(selection.evidence_ids)<=allowed:
        raise ValueError('Unknown evidence reference')
    if 'UNMAPPED_HAZARDS' in selection.review_focus and a['review_status']!='unsupported_hazard':
        raise ValueError('Unsupported review claim')
    counts=dict(Counter(person['routing_status'] for person in route(snapshot,a['recommended_posture'])))
    period=snapshot['work_period']
    lines=[f"Strands reviewed the five frozen tools for {snapshot['facility']['display_name']}.",
        f"Affected period: {period['start']} → {period['end']}; facility timezone {snapshot['facility']['timezone']}.",
        f"Prototype candidate: {a['recommended_posture'] or 'incomplete'}; {a['review_status']}. {a['rationale_text']}",
        f"Synthetic routing preview: {len(snapshot['roster'])} employees; "+', '.join(f'{v} {k}' for k,v in sorted(counts.items()))+'.',
        'Model-selected evidence references: '+', '.join(dict.fromkeys(selection.evidence_ids))+'.']
    focus={'LOCAL_ACCESS':'Manager should verify local access, facility conditions and timing.',
        'UNMAPPED_HAZARDS':'Additional alert categories require explicit manager review; no automatic action mapping is supplied.',
        'ESSENTIAL_DIRECTIONS':'Essential personnel reporting requires supervisor direction.',
        'MODELED_AQ_LIMITS':'Air quality is an Open-Meteo/CAMS modeled grid estimate, not an indoor measurement.'}
    lines.extend(focus[item] for item in dict.fromkeys(selection.review_focus))
    lines.append('Facts and routing above are rendered from frozen records. The human manager makes the decision; no notification is sent.')
    return '\n'.join(lines),selection.model_dump()
