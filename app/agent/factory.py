from importlib.metadata import version
from app.settings import settings
from strands import Agent
from strands.models.openai import OpenAIModel
from strands.hooks import HookProvider
from strands.hooks.events import (
    BeforeModelCallEvent,
    BeforeToolCallEvent,
    AfterToolCallEvent,
)
from strands.tools.executors import SequentialToolExecutor
from app.services.audit import timestamp
from app.agent.prompts import SYSTEM_PROMPT
from app.agent.tools import build_tools


class BudgetHooks(HookProvider):
    def __init__(self, run_id, allowed, tool_limit=None, model_limit=None):
        self.run_id = run_id
        self.allowed = set(allowed)
        self.tool_limit = tool_limit or settings.agent_tool_limit
        self.model_limit = model_limit or settings.agent_model_limit
        self.tool_calls = 0
        self.model_calls = 0
        self.exhausted = False
        self.pending = {}
        self.trace = []
        self.on_trace = None

    def register_hooks(self, registry, **kwargs):
        registry.add_callback(BeforeModelCallEvent, self.before_model)
        registry.add_callback(BeforeToolCallEvent, self.before_tool)
        registry.add_callback(AfterToolCallEvent, self.after_tool)

    def before_model(self, event):
        if self.model_calls >= self.model_limit or self.exhausted:
            self.exhausted = True
            event.cancel = "MODEL_OR_TOOL_BUDGET_EXCEEDED"
            return
        self.model_calls += 1

    def before_tool(self, event):
        self.tool_calls += 1
        name = event.tool_use.get("name", "unknown")
        if self.tool_calls > self.tool_limit:
            self.exhausted = True
            event.cancel_tool = "TOOL_BUDGET_EXCEEDED"
        elif name not in self.allowed:
            event.cancel_tool = "TOOL_NOT_ALLOWED"
        # Only contract arguments; do not record arbitrary injected payloads.
        args = {
            k: str(v)[:150]
            for k, v in event.tool_use.get("input", {}).items()
            if k in ("snapshot_id", "facility_id", "policy_version", "posture")
        }
        self.pending[event.tool_use["toolUseId"]] = {
            "run_id": self.run_id,
            "step_number": self.tool_calls,
            "tool_name": name if name in self.allowed else "unapproved_tool",
            "validated_arguments": args,
            "started_at": timestamp(),
            "provider_label": "Akamai workshop Chat Completions",
            "configured_model_alias": settings.inference_model,
            "sdk_version": version("strands-agents"),
        }

    def after_tool(self, event):
        row = self.pending.pop(event.tool_use["toolUseId"])
        success = (
            event.result.get("status") == "success" and event.cancel_message is None
        )
        if not success:
            row["validated_arguments"] = {}
        row.update(
            ended_at=timestamp(),
            duration_ms=round((event.duration or 0) * 1000, 2),
            status="success" if success else "error",
            evidence_ids=[self.run_id] if success else [],
            output_summary=(
                "Frozen current-run evidence returned"
                if success
                else "Read-only tool rejected or failed"
            ),
            safe_error_code=(
                None
                if success
                else (
                    "TOOL_CANCELLED"
                    if event.cancel_message
                    else "TOOL_VALIDATION_OR_EXECUTION"
                )
            ),
        )
        self.trace.append(row)
        if self.on_trace:
            self.on_trace(row)


def model():
    if not settings.ai_available:
        raise ValueError("INFERENCE_NOT_CONFIGURED_OR_UNAPPROVED")
    return OpenAIModel(
        client_args={
            "base_url": settings.inference_base_url,
            "api_key": settings.inference_key,
            "timeout": 25.0,
            "max_retries": 0,
        },
        model_id=settings.inference_model,
        params={"max_tokens": 1000, "temperature": 0},
    )


def make_agent(snapshot):
    names = [
        "read_facility_context",
        "read_nws_evidence",
        "read_air_quality_evidence",
        "run_policy_assessment",
        "preview_employee_impact",
    ]
    budget = BudgetHooks(snapshot["snapshot_id"], names)
    agent = Agent(
        model=model(),
        tools=build_tools(snapshot),
        system_prompt=SYSTEM_PROMPT,
        callback_handler=None,
        hooks=[budget],
        tool_executor=SequentialToolExecutor(),
        retry_strategy=None,
        load_tools_from_directory=False,
    )
    return agent, budget
