import asyncio
from datetime import timedelta
import httpx
from app.clients.base import fetch_json
from app.clients.nws import normalize
from app.clients.air_quality import normalize as normalize_aq
from app.services.audit import timestamp


def test_http_failure_bounded_not_empty(monkeypatch):
    calls = []

    async def send(self, request):
        calls.append(request.url)
        return httpx.Response(503, request=request, json={"error": "synthetic"})

    monkeypatch.setattr(httpx.AsyncClient, "send", send)
    body, meta = asyncio.run(
        fetch_json("https://api.weather.gov/alerts/active", nws=True)
    )
    assert len(calls) == 2 and body is None and meta["status"] == "unavailable"
    assert (
        normalize(body, meta, {"latitude": 0, "longitude": 0})["status"]
        == "unavailable"
    )


def test_401_not_retried(monkeypatch):
    calls = []

    async def send(self, request):
        calls.append(request.url)
        return httpx.Response(401, request=request)

    monkeypatch.setattr(httpx.AsyncClient, "send", send)
    body, meta = asyncio.run(
        fetch_json("https://api.weather.gov/alerts/active", nws=True)
    )
    assert len(calls) == 1 and meta["response_status"] == 401


def test_null_and_malformed_aq_are_missing():
    meta = {"status": "available", "fetched_at_utc": timestamp()}
    body = {
        "latitude": 0,
        "longitude": 0,
        "current": {"time": "2026-10-10T20:00", "us_aqi": None, "pm2_5": None},
    }
    assert normalize_aq(body, meta, {})["status"] == "missing"
    body["current"]["us_aqi"] = float("nan")
    assert normalize_aq(body, meta, {})["status"] == "unavailable"


def test_invalid_nws_shape_unavailable():
    assert (
        normalize({"features": []}, {"status": "available"})["status"] == "unavailable"
    )
