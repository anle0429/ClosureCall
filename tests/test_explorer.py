from copy import deepcopy
from fastapi.testclient import TestClient
from dataclasses import replace
import app.main as main
import app.auth as auth
from app.clients import nws


def test_synthetic_demo_site_requires_point_confirmation_and_timezone(
    store, snapshot, alert, monkeypatch
):
    alert["geometry"] = {
        "type": "Polygon",
        "coordinates": [[[-95, 39], [-94, 39], [-94, 40], [-95, 40], [-95, 39]]],
    }

    async def national():
        return {**snapshot["nws"], "alerts": [alert]}

    async def point(lat, lon):
        assert 39 <= lat <= 40 and -95 <= lon <= -94
        return {**snapshot["nws"], "alerts": [alert]}

    async def timezone(*args, **kwargs):
        return {"properties": {"timeZone": "America/Chicago"}}, {"status": "available"}

    import app.clients.base as base

    monkeypatch.setattr(nws, "national", national)
    monkeypatch.setattr(nws, "point", point)
    monkeypatch.setattr(base, "fetch_json", timezone)
    monkeypatch.setattr(main, "store", store)
    monkeypatch.setattr(main, "explorer_cache", None)
    monkeypatch.setattr(
        auth,
        "settings",
        replace(
            auth.settings,
            manager_username="test",
            manager_password="synthetic-test-password",
        ),
    )
    with TestClient(main.app) as client:
        response = client.post(
            "/api/facilities/demo-site",
            json={"alert_id": alert["alert_id"]},
            auth=("test", "synthetic-test-password"),
        )
        assert response.status_code == 201, response.text
        body = response.json()
        assert body["synthetic"] and body["timezone"] == "America/Chicago"
        assert body["source_alert_id"] == alert["alert_id"]
        assert store.facility(body["facility_id"]) == body

        async def missing(*args):
            return {**snapshot["nws"], "alerts": []}

        monkeypatch.setattr(nws, "point", missing)
        response = client.post(
            "/api/facilities/demo-site",
            json={"alert_id": alert["alert_id"]},
            auth=("test", "synthetic-test-password"),
        )
        assert response.status_code == 409
