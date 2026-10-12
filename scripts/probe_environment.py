import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import httpx
from app.settings import settings

if __name__ == "__main__":
    try:
        response = httpx.get(
            "https://ws.akamai-workshops.com/v1/models",
            timeout=15,
            follow_redirects=False,
        )
        print(
            json.dumps(
                {
                    "inference_models_http": response.status_code,
                    "network_reachable": True,
                    "key_present": settings.ai_available,
                    "note": "Unauthenticated connectivity probe only, no model inference.",
                }
            )
        )
    except httpx.HTTPError as exc:
        print(
            json.dumps(
                {
                    "network_reachable": False,
                    "safe_error_code": type(exc).__name__,
                    "key_present": settings.ai_available,
                }
            )
        )
