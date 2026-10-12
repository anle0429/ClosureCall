import asyncio
import json
from types import SimpleNamespace
import pytest
from app.agent.factory import BudgetHooks, make_agent
from app.agent.tools import build_tools
from app.jobs import bounded_worker


def test_model_and_tool_budgets_enforced_without_model():
    budget = BudgetHooks(
        "synthetic-run", ["read_facility_context"], tool_limit=1, model_limit=1
    )
    first = SimpleNamespace(cancel=False)
    budget.before_model(first)
    assert not first.cancel
    second = SimpleNamespace(cancel=False)
    budget.before_model(second)
    assert second.cancel and budget.model_calls == 1
    one = SimpleNamespace(
        tool_use={"name": "read_facility_context", "input": {}, "toolUseId": "1"},
        cancel_tool=False,
    )
    budget.before_tool(one)
    two = SimpleNamespace(
        tool_use={"name": "read_facility_context", "input": {}, "toolUseId": "2"},
        cancel_tool=False,
    )
    budget.before_tool(two)
    assert two.cancel_tool == "TOOL_BUDGET_EXCEEDED"


def test_tools_scoped_to_run_and_no_mutations(snapshot):
    tools = build_tools(snapshot)
    names = [x.tool_name for x in tools]
    assert names == [
        "read_facility_context",
        "read_nws_evidence",
        "read_air_quality_evidence",
        "run_policy_assessment",
        "preview_employee_impact",
    ]
    for name in names:
        assert all(
            unsafe not in name for unsafe in ("approve", "send", "shell", "delete")
        )
    # Decorated tools retain direct callable behavior; argument checks reject injection IDs.
    with pytest.raises(ValueError):
        tools[1](snapshot_id="another-run")
    with pytest.raises(ValueError):
        tools[3](snapshot_id=snapshot["snapshot_id"], policy_version="invented-policy")
    with pytest.raises(ValueError):
        tools[4](snapshot_id=snapshot["snapshot_id"], posture="closure")


def test_subprocess_deadline_is_enforced(tmp_path, monkeypatch):
    # Trace retention needs a started worker; startup scheduling is a separate case.
    (tmp_path / "synthetic_slow_worker.py").write_text(
        'import time\nprint(\'{"event":"tool_trace","trace":{"synthetic":true}}\',flush=True)\ntime.sleep(20)\n',
        encoding="utf-8",
    )
    monkeypatch.setenv("PYTHONPATH", str(tmp_path))
    create = asyncio.create_subprocess_exec
    spawned = []

    class StartedOutput:
        def __init__(self, first_line, stream):
            self.first_line, self.stream = first_line, stream

        async def __aiter__(self):
            yield self.first_line
            async for line in self.stream:
                yield line

    async def start_and_observe(*args, **kwargs):
        process = await create(*args, **kwargs)
        spawned.append(process)
        try:
            # This is bounded fixture setup, not an extension of the .2s deadline.
            first_line = await asyncio.wait_for(process.stdout.readline(), timeout=5)
            assert json.loads(first_line) == {
                "event": "tool_trace",
                "trace": {"synthetic": True},
            }
            process.stdout = StartedOutput(first_line, process.stdout)
            return process
        except BaseException:
            if process.returncode is None:
                process.kill()
            await process.wait()
            raise

    monkeypatch.setattr(asyncio, "create_subprocess_exec", start_and_observe)
    result = asyncio.run(bounded_worker("synthetic_slow_worker", {}, deadline=0.2))
    assert result["safe_error_code"] == "AGENT_DEADLINE"
    assert result["trace"] == [{"synthetic": True}]
    assert len(spawned) == 1 and spawned[0].returncode is not None


def test_deadline_terminates_worker_before_any_trace(tmp_path, monkeypatch):
    # A worker that has not produced output must also be killed, not left running.
    (tmp_path / "synthetic_startup_worker.py").write_text(
        "import time\ntime.sleep(20)\n", encoding="utf-8"
    )
    monkeypatch.setenv("PYTHONPATH", str(tmp_path))
    create = asyncio.create_subprocess_exec
    spawned = []

    async def observe(*args, **kwargs):
        process = await create(*args, **kwargs)
        spawned.append(process)
        return process

    monkeypatch.setattr(asyncio, "create_subprocess_exec", observe)
    result = asyncio.run(bounded_worker("synthetic_startup_worker", {}, deadline=0.2))
    assert result["safe_error_code"] == "AGENT_DEADLINE"
    assert result["trace"] == []
    assert len(spawned) == 1 and spawned[0].returncode is not None


def test_provider_placeholder_never_creates_agent(snapshot):
    from app.settings import settings

    if not settings.ai_available:
        with pytest.raises(ValueError):
            make_agent(snapshot)


def test_real_sdk_tool_loop_and_hooks_with_synthetic_model(snapshot, monkeypatch):
    import json
    from strands.models.model import Model
    import app.agent.factory as factory
    from app.agent.worker import run

    class SyntheticModel(Model):
        def update_config(self, **kwargs):
            pass

        def get_config(self):
            return {"model_id": "SYNTHETIC-UNIT-TEST"}

        async def structured_output(self, *args, **kwargs):
            raise NotImplementedError
            yield

        async def stream(self, messages, *args, **kwargs):
            yield {"messageStart": {"role": "assistant"}}
            if not any("toolResult" in block for block in messages[-1]["content"]):
                params = [
                    (
                        "read_facility_context",
                        {"facility_id": snapshot["facility"]["facility_id"]},
                    ),
                    ("read_nws_evidence", {"snapshot_id": snapshot["snapshot_id"]}),
                    (
                        "read_air_quality_evidence",
                        {"snapshot_id": snapshot["snapshot_id"]},
                    ),
                    (
                        "run_policy_assessment",
                        {
                            "snapshot_id": snapshot["snapshot_id"],
                            "policy_version": snapshot["policy"]["version"],
                        },
                    ),
                    (
                        "preview_employee_impact",
                        {"snapshot_id": snapshot["snapshot_id"], "posture": "normal"},
                    ),
                ]
                for i, (name, args) in enumerate(params):
                    yield {
                        "contentBlockStart": {
                            "contentBlockIndex": i,
                            "start": {"toolUse": {"toolUseId": str(i), "name": name}},
                        }
                    }
                    yield {
                        "contentBlockDelta": {
                            "contentBlockIndex": i,
                            "delta": {"toolUse": {"input": json.dumps(args)}},
                        }
                    }
                    yield {"contentBlockStop": {"contentBlockIndex": i}}
                yield {"messageStop": {"stopReason": "tool_use"}}
            else:
                yield {"contentBlockStart": {"start": {}}}
                selected = {
                    "snapshot_id": snapshot["snapshot_id"],
                    "policy_version": snapshot["policy"]["version"],
                    "evidence_ids": [snapshot["snapshot_id"]],
                    "review_focus": ["LOCAL_ACCESS", "ESSENTIAL_DIRECTIONS"],
                }
                yield {"contentBlockDelta": {"delta": {"text": json.dumps(selected)}}}
                yield {"contentBlockStop": {}}
                yield {"messageStop": {"stopReason": "end_turn"}}

    monkeypatch.setattr(factory, "model", lambda: SyntheticModel())
    result = run(snapshot)
    assert result["status"] == "active", result
    assert len(result["trace"]) == 5
    assert all(t["status"] == "success" and t["sdk_version"] for t in result["trace"])
    assert result["model_calls"] == 2


def test_brief_rejects_invented_facts_and_ids(snapshot):
    import json
    from app.agent.brief import grounded_brief

    valid = {
        "snapshot_id": snapshot["snapshot_id"],
        "policy_version": snapshot["policy"]["version"],
        "evidence_ids": [snapshot["snapshot_id"]],
        "review_focus": ["LOCAL_ACCESS"],
    }
    narrative, _ = grounded_brief(json.dumps(valid), snapshot)
    assert "12 employees" in narrative and snapshot["work_period"]["start"] in narrative
    for change in (
        {"evidence_ids": ["invented"]},
        {"routing_count": 8},
        {"review_focus": ["UNMAPPED_HAZARDS"]},
        {"snapshot_id": "other"},
        {"review_focus": ["EVACUATE"]},
    ):
        with pytest.raises(ValueError):
            grounded_brief(json.dumps({**valid, **change}), snapshot)


def test_sdk_stops_repeated_model_calls(snapshot, monkeypatch):
    import json
    from strands.models.model import Model
    from dataclasses import replace
    import app.agent.factory as factory
    from app.agent.worker import run

    class LoopModel(Model):
        def update_config(self, **kwargs):
            pass

        def get_config(self):
            return {"model_id": "SYNTHETIC-LOOP"}

        async def structured_output(self, *args, **kwargs):
            raise NotImplementedError
            yield

        async def stream(self, messages, *args, **kwargs):
            yield {"messageStart": {"role": "assistant"}}
            yield {
                "contentBlockStart": {
                    "start": {
                        "toolUse": {
                            "toolUseId": str(len(messages)),
                            "name": "read_facility_context",
                        }
                    }
                }
            }
            yield {
                "contentBlockDelta": {
                    "delta": {
                        "toolUse": {
                            "input": json.dumps(
                                {"facility_id": snapshot["facility"]["facility_id"]}
                            )
                        }
                    }
                }
            }
            yield {"contentBlockStop": {}}
            yield {"messageStop": {"stopReason": "tool_use"}}

    monkeypatch.setattr(factory, "model", lambda: LoopModel())
    monkeypatch.setattr(
        factory, "settings", replace(factory.settings, agent_model_limit=2)
    )
    result = run(snapshot)
    assert result["status"] == "degraded"
    assert result["model_calls"] == 2


@pytest.mark.parametrize("alert_ids", [[], ["urn:synthetic-warning"]])
def test_prompt_scopes_model_references_to_frozen_contract(
    snapshot, monkeypatch, alert_ids
):
    import json
    import app.agent.worker as worker

    snapshot["nws"]["alerts"] = [{"alert_id": value} for value in alert_ids]
    captured = []

    def agent(prompt):
        captured.append(prompt)
        return json.dumps(
            {
                "snapshot_id": snapshot["snapshot_id"],
                "policy_version": snapshot["policy"]["version"],
                "evidence_ids": [snapshot["snapshot_id"]],
                "review_focus": ["LOCAL_ACCESS"],
            }
        )

    budget = SimpleNamespace(
        trace=[
            {"tool_name": name, "status": "success"}
            for name in (
                "read_facility_context",
                "read_nws_evidence",
                "read_air_quality_evidence",
                "run_policy_assessment",
                "preview_employee_impact",
            )
        ],
        exhausted=False,
        model_calls=2,
        tool_calls=5,
    )
    monkeypatch.setattr(worker, "make_agent", lambda frozen: (agent, budget))
    result = worker.run(snapshot)
    assert result["status"] == "active"
    marker = "Allowed evidence_ids: "
    assert (
        marker in captured[0]
    ), "The model needs an explicit list when a valid NWS feed has no alert IDs."
    allowed = json.loads(captured[0].split(marker, 1)[1].split("\n", 1)[0])
    assert set(allowed) == {
        snapshot["snapshot_id"],
        snapshot["air_quality"]["source_url"],
        *alert_ids,
    }
    assert snapshot["nws"]["source_url"] not in allowed


def test_zero_alert_nws_url_still_rejected_and_snapshot_reference_accepted(snapshot):
    import json
    from app.agent.brief import grounded_brief

    snapshot["nws"]["alerts"] = []
    selected = {
        "snapshot_id": snapshot["snapshot_id"],
        "policy_version": snapshot["policy"]["version"],
        "evidence_ids": [snapshot["nws"]["source_url"]],
        "review_focus": ["LOCAL_ACCESS"],
    }
    with pytest.raises(ValueError, match="Unknown evidence reference"):
        grounded_brief(json.dumps(selected), snapshot)
    selected["evidence_ids"] = [snapshot["snapshot_id"]]
    narrative, _ = grounded_brief(json.dumps(selected), snapshot)
    assert "12 employees" in narrative
