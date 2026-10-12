"""Offline synthetic geography/time/snapshot cases; never live incident evidence."""

import asyncio
from copy import deepcopy
from datetime import timedelta
import json
import httpx
import pytest
from app.clients.base import fetch_json
from app.clients.nws import FIELDS, normalize, applicability
from app.policy.engine import assess
from app.services.audit import parse_time
from app.agent.brief import grounded_brief

KC_POLYGON = {
    "type": "Polygon",
    "coordinates": [[[-95, 38], [-94, 38], [-94, 40], [-95, 40], [-95, 38]]],
}
WISCONSIN_POLYGON = {
    "type": "Polygon",
    "coordinates": [[[-90, 43], [-89, 43], [-89, 44], [-90, 44], [-90, 43]]],
}


def response(snapshot, alert, geometry, *, scope=False):
    props = {source: alert.get(key) for key, source in FIELDS.items()}
    props["id"] = alert["alert_id"]
    if scope:
        props["geocode"] = {"UGC": ["MOZ037"], "SAME": ["029095"]}
        props["affectedZones"] = ["https://api.weather.gov/zones/forecast/MOZ037"]
    body = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "id": alert["alert_id"],
                "geometry": geometry,
                "properties": props,
            }
        ],
    }
    return normalize(body, snapshot["nws"], snapshot["nws"]["request_location"])


def test_wisconsin_polygon_cannot_supply_kc_closure(snapshot, alert):
    snapshot["nws"] = response(snapshot, alert, WISCONSIN_POLYGON)
    stored = snapshot["nws"]["alerts"][0]
    assert stored["applicability_status"] == "outside_polygon"
    assert "outside" in stored["applicability_reason"].lower()
    result = assess(snapshot)
    assert result["recommended_posture"] != "closure"
    assert alert["alert_id"] not in result["evidence_ids"]


def test_polygon_hole_is_not_positive_bbox_proof(snapshot, alert):
    geometry = deepcopy(KC_POLYGON)
    geometry["coordinates"].append(
        [[-94.8, 39], [-94.4, 39], [-94.4, 39.3], [-94.8, 39.3], [-94.8, 39]]
    )
    assert (
        response(snapshot, alert, geometry)["alerts"][0]["applicability_status"]
        == "outside_polygon"
    )


@pytest.mark.parametrize(
    "geometry",
    [
        None,
        "SYNTHETIC MALFORMED GEOMETRY",
        {"type": "Point", "coordinates": [-94.5786, 39.0997]},
        {"type": "Polygon", "coordinates": []},
        {
            "type": "Polygon",
            "coordinates": [[[-95, 38], [-94, 40], [-95, 40], [-94, 38], [-95, 38]]],
        },
    ],
)
def test_unknown_scope_is_incomplete_not_normal_or_closure(snapshot, alert, geometry):
    snapshot["nws"] = response(snapshot, alert, geometry)
    assert snapshot["nws"]["alerts"][0]["applicability_status"] == "unverified"
    result = assess(snapshot)
    assert result["review_status"] == "data_incomplete"
    assert result["recommended_posture"] is None


@pytest.mark.parametrize(
    "scope,event",
    [("MOZ037", "High Wind Warning"), ("MOC095", "Severe Thunderstorm Watch")],
)
def test_null_geometry_retains_point_filtered_county_zone_scope(
    snapshot, alert, scope, event
):
    alert["event"] = event
    alert["geocode"] = {"UGC": [scope]}
    alert["affected_zones"] = [
        f'https://api.weather.gov/zones/{"county" if "C" in scope else "forecast"}/{scope}'
    ]
    snapshot["nws"] = response(snapshot, alert, None)
    item = snapshot["nws"]["alerts"][0]
    assert item["applicability_status"] == "point_confirmed"
    assert item["geocode"]["UGC"] == [scope]
    assert "point" in item["applicability_reason"].lower()
    assert assess(snapshot)["review_status"] != "data_incomplete"


@pytest.mark.parametrize("bad_geometry", [WISCONSIN_POLYGON, None])
def test_wrong_or_unknown_alert_does_not_erase_valid_warning(
    snapshot, alert, bad_geometry
):
    bad = response(snapshot, {**alert, "alert_id": "SYNTHETIC-BAD"}, bad_geometry)[
        "alerts"
    ][0]
    good = response(snapshot, alert, KC_POLYGON)["alerts"][0]
    snapshot["nws"]["alerts"] = [bad, good]
    result = assess(snapshot)
    assert result["recommended_posture"] == "closure"
    assert result["matched_rules"][0]["evidence_id"] == alert["alert_id"]
    assert "SYNTHETIC-BAD" not in result["evidence_ids"]
    assert result["review_status"] == (
        "data_incomplete" if bad_geometry is None else "ready_for_manager"
    )


def test_partial_overlap_is_bounded_by_message_expiry(snapshot, alert):
    start, end = map(
        parse_time, [snapshot["work_period"]["start"], snapshot["work_period"]["end"]]
    )
    stop = start + timedelta(minutes=30)
    alert.update(
        onset=(start - timedelta(minutes=30)).isoformat(),
        expires=stop.isoformat(),
        ends=end.isoformat(),
    )
    applies, reason = applicability(
        alert, start, end, parse_time(snapshot["collected_at_utc"])
    )
    assert applies
    assert start.isoformat() in reason and stop.isoformat() in reason
    assert end.isoformat() not in reason
    snapshot["nws"]["alerts"] = [alert]
    match = assess(snapshot)["matched_rules"][0]
    assert stop.isoformat() in match["categorical_match_reason"]


def test_future_work_period_after_message_expiry_has_no_match(snapshot, alert):
    start, end = map(
        parse_time, [snapshot["work_period"]["start"], snapshot["work_period"]["end"]]
    )
    alert.update(
        onset=snapshot["collected_at_utc"],
        expires=(start - timedelta(minutes=1)).isoformat(),
        ends=end.isoformat(),
    )
    assert (
        applicability(alert, start, end, parse_time(snapshot["collected_at_utc"]))[0]
        is False
    )


def selection(snapshot, ids):
    return json.dumps(
        {
            "snapshot_id": snapshot["snapshot_id"],
            "policy_version": snapshot["policy"]["version"],
            "evidence_ids": ids,
            "review_focus": ["LOCAL_ACCESS"],
        }
    )


def test_reference_present_only_in_historical_run_rejected(snapshot, alert):
    old = deepcopy(snapshot)
    old["snapshot_id"] = "SYNTHETIC-OLD-RUN"
    old["nws"]["alerts"] = [alert]
    assert (
        alert["alert_id"]
        in grounded_brief(selection(old, [alert["alert_id"]]), old)[1]["evidence_ids"]
    )
    with pytest.raises(ValueError, match="Unknown evidence reference"):
        grounded_brief(selection(snapshot, [alert["alert_id"]]), snapshot)


@pytest.mark.parametrize(
    "current_scope,expected",
    [("point_confirmed", "closure"), ("outside_polygon", "normal")],
)
def test_same_id_in_two_snapshots_uses_current_membership_and_assessment(
    snapshot, alert, current_scope, expected
):
    old = deepcopy(snapshot)
    old["snapshot_id"] = "SYNTHETIC-OLD-RUN"
    old["nws"]["alerts"] = [deepcopy(alert)]
    old["assessment"] = assess(old)
    snapshot["nws"]["alerts"] = [{**alert, "applicability_status": current_scope}]
    snapshot["assessment"] = assess(snapshot)
    assert old["assessment"]["recommended_posture"] == "closure"
    text, chosen = grounded_brief(selection(snapshot, [alert["alert_id"]]), snapshot)
    assert chosen["snapshot_id"] == snapshot["snapshot_id"]
    assert f"Prototype candidate: {expected};" in text
    assert snapshot["assessment"]["recommended_posture"] == expected


def test_wrong_location_cancel_cannot_suppress_valid_warning(snapshot, alert):
    wrong = response(
        snapshot,
        {
            **alert,
            "alert_id": "SYNTHETIC-OUTSIDE-CANCEL",
            "message_type": "Cancel",
            "references": [{"identifier": alert["alert_id"]}],
        },
        WISCONSIN_POLYGON,
    )["alerts"][0]
    good = response(snapshot, alert, KC_POLYGON)["alerts"][0]
    snapshot["nws"]["alerts"] = [good, wrong]
    assert assess(snapshot)["recommended_posture"] == "closure"


def test_empty_200_and_timeout_have_distinct_assessments(snapshot, monkeypatch):
    async def timeout(self, request):
        raise httpx.ReadTimeout("SYNTHETIC OFFLINE TIMEOUT", request=request)

    monkeypatch.setattr(httpx.AsyncClient, "send", timeout)
    body, meta = asyncio.run(
        fetch_json("https://api.weather.gov/alerts/active", nws=True)
    )
    assert body is None and meta["status"] == "unavailable"
    empty = deepcopy(snapshot)
    empty["nws"] = normalize(
        {"type": "FeatureCollection", "features": []},
        snapshot["nws"],
        snapshot["nws"]["request_location"],
    )
    assert empty["nws"]["response_status"] == 200
    assert assess(empty)["recommended_posture"] == "normal"
    assert "not a safety guarantee" in assess(empty)["rationale_text"]
    snapshot["nws"] = normalize(body, meta, snapshot["nws"]["request_location"])
    assert assess(snapshot)["review_status"] == "data_incomplete"
    assert assess(snapshot)["recommended_posture"] is None
