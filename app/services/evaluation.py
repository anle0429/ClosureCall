import asyncio
import time
from zoneinfo import ZoneInfo
from app.clients import nws, air_quality
from app.policy.engine import assess, load_rules
from app.services.audit import timestamp, utcnow, parse_time
from app.services.recipients import roster
from app.jobs import bounded_worker
from app.settings import settings


async def evaluate(store, run_id):
    started = time.monotonic()
    try:
        run = store.run(run_id)
        body = run["request"]
        facility = store.facility(body["facility_id"])
        weather, aq = await asyncio.gather(
            nws.point(facility["latitude"], facility["longitude"]),
            air_quality.point(facility["latitude"], facility["longitude"]),
        )
        work_period = {k: body[k] for k in ("start", "end", "special_shift")}
        local_start = parse_time(body["start"]).astimezone(
            ZoneInfo(facility["timezone"])
        )
        context = (
            "before_open"
            if utcnow() < parse_time(body["start"])
            else "open" if utcnow() < parse_time(body["end"]) else "after_close"
        )
        snapshot = {
            "mode": "LIVE",
            "snapshot_id": run_id,
            "facility": facility,
            "work_period": {
                **work_period,
                "selected_work_date": local_start.date().isoformat(),
                "timezone": facility["timezone"],
                "operating_context": context,
            },
            "collected_at_utc": timestamp(),
            "nws": weather,
            "air_quality": aq,
            "policy": load_rules(),
            "roster": roster(body["facility_id"], body["start"], body["end"]),
            "roster_version": "synthetic-v1",
        }
        snapshot["assessment"] = assess(snapshot)
        store.save_snapshot(run_id, snapshot)
        store.update_run(run_id, "evaluating")
        if settings.ai_available:
            response = await bounded_worker("app.agent.worker", snapshot)
        else:
            response = {
                "status": "unavailable",
                "safe_error_code": "INFERENCE_NOT_CONFIGURED",
                "narrative": "AI unavailable — deterministic assessment only.",
                "trace": [],
            }
        trace = response.pop("trace", [])
        metrics = {
            "elapsed_ms": round((time.monotonic() - started) * 1000, 2),
            "source_http_attempts": weather.get("http_attempts", 0)
            + aq.get("http_attempts", 0),
            "model_calls": response.get("model_calls", 0),
            "successful_tool_calls": sum(x["status"] == "success" for x in trace),
        }
        store.save_result(
            run_id,
            {"ai": response, "trace": trace, "metrics": metrics},
            (
                "ready"
                if snapshot["assessment"]["review_status"] == "ready_for_manager"
                else "incomplete"
            ),
        )
    except asyncio.CancelledError:
        store.update_run(run_id, "interrupted", "SERVER_SHUTDOWN")
        raise
    except Exception as exc:
        store.update_run(run_id, "failed", type(exc).__name__)
