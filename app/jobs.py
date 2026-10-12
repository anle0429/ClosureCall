import asyncio
import json
import sys
from app.settings import settings


async def bounded_worker(module, payload, deadline=None):
    process = await asyncio.create_subprocess_exec(
        sys.executable,
        "-m",
        module,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.DEVNULL,
    )
    trace = []

    async def exchange():
        process.stdin.write(json.dumps(payload).encode())
        await process.stdin.drain()
        process.stdin.close()
        result = None
        async for line in process.stdout:
            event = json.loads(line)
            if not isinstance(event, dict):
                raise ValueError("Invalid worker event")
            if event.get("event") == "tool_trace":
                trace.append(event["trace"])
            else:
                result = event
        await process.wait()
        if process.returncode != 0 or not isinstance(result, dict):
            raise ValueError("Worker failed without final result")
        return result

    try:
        body = await asyncio.wait_for(
            exchange(), timeout=deadline or settings.agent_deadline
        )
        return body
    except asyncio.TimeoutError:
        if process.returncode is None:
            process.kill()
        await process.wait()
        return {
            "status": "degraded",
            "safe_error_code": "AGENT_DEADLINE",
            "narrative": "",
            "trace": trace,
        }
    except asyncio.CancelledError:
        if process.returncode is None:
            process.kill()
        await process.wait()
        raise
    except (ValueError, TypeError, KeyError, BrokenPipeError, ConnectionResetError):
        if process.returncode is None:
            process.kill()
        await process.wait()
        return {
            "status": "degraded",
            "safe_error_code": "AGENT_INVALID_OUTPUT",
            "narrative": "",
            "trace": trace,
        }
