import json
import logging
import secrets
import sys
from strands import Agent, tool
from strands.tools.executors import SequentialToolExecutor
from app.agent.factory import BudgetHooks, model


def run():
    token = secrets.token_hex(10)
    calls = []

    @tool
    def retrieve_test_value() -> dict[str, str]:
        """Read the exact server-side test value; obtain it by calling this tool."""
        calls.append("retrieve_test_value")
        return {"value": token}

    budget = BudgetHooks("smoke", ["retrieve_test_value"], tool_limit=1, model_limit=3)
    budget.on_trace = lambda event: print(
        json.dumps({"event": "tool_trace", "trace": event}), flush=True
    )
    agent = Agent(
        model=model(),
        tools=[retrieve_test_value],
        callback_handler=None,
        hooks=[budget],
        retry_strategy=None,
        tool_executor=SequentialToolExecutor(),
        system_prompt="Use the supplied tool exactly once and return its exact value. No internal reasoning.",
    )
    try:
        response = str(
            agent("Call retrieve_test_value once and return its exact value.")
        )
        passed = len(calls) == 1 and token in response and not budget.exhausted
        return {
            "status": "pass" if passed else "fail",
            "tool_calls": len(calls),
            "model_calls": budget.model_calls,
            "trace": budget.trace,
        }
    except Exception as exc:
        return {
            "status": "fail",
            "safe_error_code": type(exc).__name__,
            "trace": budget.trace,
        }


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    try:
        result = run()
    except Exception as exc:
        result = {"status": "fail", "safe_error_code": type(exc).__name__}
    print(json.dumps(result))
