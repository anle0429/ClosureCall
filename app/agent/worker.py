import json
import logging
import sys
from pydantic import BaseModel, Field
from app.agent.factory import make_agent
from app.settings import settings
from app.agent.brief import grounded_brief, allowed_evidence_ids

class BriefResult(BaseModel):
    status: str
    narrative: str = Field(max_length=12000)
    safe_error_code: str | None = None
    trace: list[dict]
    model_calls: int = 0
    tool_calls: int = 0
    model_alias: str = settings.inference_model
    review_selection: dict | None = None

def run(snapshot, on_trace=None):
    agent,budget=make_agent(snapshot)
    budget.on_trace=on_trace
    try:
        result=str(agent(f"Read all five tools and summarize this run. facility_id={snapshot['facility']['facility_id']}; "
            f"snapshot_id={snapshot['snapshot_id']}; policy_version={snapshot['policy']['version']}; "
            f"posture={snapshot['assessment']['recommended_posture'] or 'incomplete'}\n"
            f"Allowed evidence_ids: {json.dumps(sorted(allowed_evidence_ids(snapshot)))}\n"
            "Choose evidence_ids only from that exact list. Cite this snapshot_id for the NWS collection, "
            "including a valid empty alert feed; the NWS request URL is provenance, not an allowed reference ID."))
        successful={x['tool_name'] for x in budget.trace if x['status']=='success'}
        complete=len(successful)==5 and not budget.exhausted
        narrative,selection=grounded_brief(result,snapshot) if complete else ('',None)
        return BriefResult(status='active' if complete else 'degraded',narrative=narrative,
            safe_error_code=None if complete else 'AGENT_BUDGET_OR_REQUIRED_TOOLS_MISSING',
            trace=budget.trace,model_calls=budget.model_calls,tool_calls=budget.tool_calls,
            review_selection=selection).model_dump()
    except Exception as exc:
        return BriefResult(status='degraded',narrative='',safe_error_code=type(exc).__name__,
            trace=budget.trace,model_calls=budget.model_calls,tool_calls=budget.tool_calls).model_dump()

if __name__=='__main__':
    logging.disable(logging.CRITICAL)
    try:
        body=run(json.load(sys.stdin),lambda event:print(json.dumps({'event':'tool_trace','trace':event}),flush=True))
    except Exception as exc:
        body={'status':'degraded','narrative':'','safe_error_code':type(exc).__name__,'trace':[]}
    sys.stdout.write(json.dumps(body))
