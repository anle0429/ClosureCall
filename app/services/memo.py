"""A presentation of a frozen replay bundle, with no evidence or policy recomputation."""

from datetime import datetime
from html import escape
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

RENDERER_VERSION = "frozen-memo-v2"


def text(value):
    return escape(
        "Not recorded" if value is None or value == "" else str(value), quote=True
    )


def recorded_time(value, zone):
    if not value:
        return "Not recorded"
    try:
        date = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if date.tzinfo is None:
            return f"{value} (offset not recorded; no conversion)"
        local = date.astimezone(ZoneInfo(zone))
        return f"{value} | {local.isoformat()} [{zone}]"
    except (ValueError, TypeError, ZoneInfoNotFoundError):
        return f"{value} (facility timezone conversion unavailable)"


def fields(items):
    return (
        "<dl>"
        + "".join(
            f"<dt><strong>{escape(label)}</strong></dt><dd>{text(value)}</dd>"
            for label, value in items
        )
        + "</dl>"
    )


def saved_list(title, items):
    values = ["Not recorded"] if items is None else items or ["No entries recorded"]
    return (
        f"<h3>{escape(title)}</h3><ul>"
        + "".join(f"<li>{text(item)}</li>" for item in values)
        + "</ul>"
    )


def render_memo(record):
    if record.get("mode") != "REPLAY":
        raise ValueError("Memo requires a frozen replay record")
    s, d, pack = record["snapshot"], record["decision"], record["notifications"]
    facility, period, a = s["facility"], s["work_period"], s["assessment"]
    zone = facility.get("timezone")
    time = lambda value: recorded_time(value, zone)
    identity = fields(
        [
            ("Memo renderer (presentation only)", RENDERER_VERSION),
            ("Decision ID", d.get("decision_id")),
            ("Evaluation ID", d.get("evaluation_id")),
            ("Historical bundle hash", record.get("bundle_hash")),
            ("Snapshot hash", record.get("snapshot_hash")),
            ("Original snapshot mode", s.get("mode")),
            (
                "Stored test label",
                s.get("test_evidence_label") or "No additional test label recorded",
            ),
        ]
    )
    parts = [
        '<!doctype html><html lang="en"><head><meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width,initial-scale=1">',
        '<meta http-equiv="Content-Security-Policy" content="default-src &#39;none&#39;; style-src &#39;unsafe-inline&#39;; base-uri &#39;none&#39;; form-action &#39;none&#39;">',
        "<title>ClosureCall decision memo — REPLAY</title>",
        "<style>body{font:15px/1.6 Segoe UI,Arial,sans-serif;color:#1F2933;background:#F5F6F7;margin:24px}"
        "main{max-width:1000px;margin:auto;padding:28px;background:white;border:1px solid #D4D9DE;border-top:3px solid #234866}"
        "h1{font-size:26px;line-height:1.25;color:#234866}h2{color:#234866;border-top:1px solid #D4D9DE;padding-top:16px;margin-top:28px}"
        "h3{font-size:17px}dl{display:grid;grid-template-columns:240px minmax(0,1fr);gap:8px 16px;font-size:13px}"
        "dd{margin:0}dt,dd,p,li,pre{overflow-wrap:anywhere}pre{white-space:pre-wrap;font:13px/1.6 Segoe UI,Arial,sans-serif}"
        "details{padding:12px;background:#F5F6F7}summary{cursor:pointer}"
        "@media(max-width:640px){body{margin:8px}main{padding:16px}dl{display:block}dd{margin-bottom:12px}}"
        "@media print{body{background:white;margin:0}main{border:0;padding:0}h2,h3{break-after:avoid}}"
        "</style></head><body><main>",
        "<h1>ClosureCall decision memo — REPLAY</h1>",
        "<p><strong>PROTOTYPE · synthetic office and roster · notification drafts only.</strong></p>",
        "<p>This is a new presentation of stored records, not current weather or a new operational decision. "
        "No sources, model, policy assessment or recipient routing are called again. "
        "Prototype action thresholds are not verified USDA/OPM policy; this memo is not a compliance certification.</p>",
        "<h2>Facility and affected work period</h2>",
        fields(
            [
                ("Facility", facility.get("display_name")),
                ("Facility ID", facility.get("facility_id")),
                (
                    "Latitude / longitude",
                    f"{facility.get('latitude')} / {facility.get('longitude')}",
                ),
                ("Facility timezone", zone),
                ("Work period start", time(period.get("start"))),
                ("Work period end", time(period.get("end"))),
                ("Special shift (stored)", period.get("special_shift")),
                ("Evidence collected", time(s.get("collected_at_utc"))),
            ]
        ),
        "<h2>Original recommendation — before manager decision</h2>",
        fields(
            [
                (
                    "Original posture",
                    a.get("recommended_posture") or "No candidate recorded",
                ),
                ("Review status", a.get("review_status")),
                ("Policy version", a.get("policy_version")),
                ("Confidence rubric (not probability)", a.get("confidence_label")),
                ("Saved rationale", a.get("rationale_text")),
            ]
        ),
        "<h3>Matched prototype rules</h3>",
    ]
    for rule in a.get("matched_rules", []):
        parts.append(
            fields(
                [
                    ("Rule ID / version", f"{rule.get('id')} / {rule.get('version')}"),
                    ("Observed value", rule.get("observed_value")),
                    ("Numeric threshold", rule.get("threshold")),
                    ("Numeric exceedance", rule.get("exceedance")),
                    ("Evidence ID", rule.get("evidence_id")),
                    (
                        "Saved applicability / category basis",
                        rule.get("categorical_match_reason"),
                    ),
                    ("Prototype action basis", rule.get("prototype_mapping_reason")),
                    ("Reference", rule.get("reference_source_url")),
                ]
            )
        )
    if not a.get("matched_rules"):
        parts.append("<p>No matched rules stored.</p>")
    for title, key in [
        ("Missing inputs", "missing_inputs"),
        ("Confidence basis", "confidence_basis"),
        ("Assumptions", "assumptions"),
        ("What would change the recommendation", "what_would_change"),
    ]:
        parts.append(saved_list(title, a.get(key)))
    parts.extend(
        [
            "<h2>Final manager decision — separate from recommendation</h2>",
            fields(
                [
                    ("Decision status", d.get("status")),
                    ("Final posture", d.get("posture")),
                    ("Recorded actor", d.get("actor")),
                    ("Decision time", time(d.get("approved_at"))),
                    ("Recorded manager reason", d.get("reason")),
                    ("Confirmed timing", time(d.get("timing_at"))),
                    ("Timing evidence / assumption", d.get("timing_basis")),
                    (
                        "Stale / superseded override (stored)",
                        d.get("stale_or_superseded_override"),
                    ),
                ]
            ),
            "<h2>Frozen evidence and saved applicability</h2>",
        ]
    )
    nws, aq = s["nws"], s["air_quality"]
    parts.append(
        fields(
            [
                ("NWS source request", nws.get("source_url")),
                (
                    "NWS status / HTTP",
                    f"{nws.get('status')} / {nws.get('response_status')}",
                ),
                ("NWS fetched", time(nws.get("fetched_at_utc"))),
                ("Requested location", nws.get("request_location")),
            ]
        )
    )
    if not nws.get("alerts"):
        parts.append(
            "<p>No alert entries stored. Read the saved source status: empty available data and unavailable data differ. Neither establishes all local hazards are absent.</p>"
        )
    for alert in nws.get("alerts", []):
        parts.append(
            "<h3>"
            + text(alert.get("event"))
            + "</h3>"
            + fields(
                [
                    ("Alert ID", alert.get("alert_id")),
                    (
                        "Message status / type",
                        f"{alert.get('status')} / {alert.get('message_type')}",
                    ),
                    ("Issued", time(alert.get("sent"))),
                    ("Effective", time(alert.get("effective"))),
                    ("Onset", time(alert.get("onset"))),
                    ("Expires", time(alert.get("expires"))),
                    ("Ends", time(alert.get("ends"))),
                    ("Saved applicability status", alert.get("applicability_status")),
                    ("Saved applicability reason", alert.get("applicability_reason")),
                    ("County / zone metadata (stored)", alert.get("geocode")),
                    ("Affected zone references (stored)", alert.get("affected_zones")),
                    ("Saved instruction", alert.get("instruction")),
                ]
            )
        )
    parts.extend(
        [
            fields(
                [
                    ("AQ source request", aq.get("source_url")),
                    ("AQ status", aq.get("status")),
                    ("AQ fetched", time(aq.get("fetched_at_utc"))),
                    ("AQ valid", time(aq.get("valid_at_utc"))),
                    ("US AQI (stored)", aq.get("us_aqi")),
                    ("PM2.5 (stored)", aq.get("pm2_5")),
                    ("AQ attribution", aq.get("attribution")),
                ]
            ),
            "<p>AQ is a modeled grid estimate, not an indoor measurement. Weather/AQ do not verify power, water, security or physical access. "
            "Source assertions are shown as stored; old records are not revalidated with a newer connector.</p>",
            fields(
                [("Saved protective-action notice", a.get("protective_action_notice"))]
            ),
            "<h2>Stored AI brief</h2>",
            fields(
                [
                    ("AI status", record["ai"].get("status")),
                    ("Saved brief", record["ai"].get("narrative")),
                ]
            ),
            "<h2>Notification package — DRAFTS, NOT SENT</h2>",
            fields(
                [
                    ("Stored notification mode", pack.get("mode")),
                    ("Stored counts", pack.get("counts")),
                ]
            ),
            "<p>Included/queued_demo means a draft. Channel labels do not prove email, SMS or voice delivery. Deferred follow-up is manual. "
            "This package may support an operator's existing process; OnSolve integration/import compatibility is not implemented or tested.</p>",
        ]
    )
    for person in pack["recipients"]:
        parts.extend(
            [
                "<h3>" + text(person.get("name")) + "</h3>",
                fields(
                    [
                        ("Employee ID", person.get("employee_id")),
                        ("Essential (stored)", person.get("essential")),
                        ("Route", person.get("routing_status")),
                        ("Reason", person.get("reason")),
                        ("Planned channel", person.get("channel")),
                        ("Draft status", person.get("notification_status")),
                        ("Manual follow-up", person.get("follow_up")),
                    ]
                ),
                "<details><summary>Stored recipient draft</summary><p>"
                + text(person.get("subject"))
                + "</p><pre>"
                + text(person.get("message"))
                + "</pre></details>",
            ]
        )
    parts.append("<h2>Record identity and presentation</h2>" + identity)
    parts.append(
        "<hr><p>Keep the frozen JSON export with this memo for the full stored geometry, policy, roster, tool trace and hashes. "
        "Missing historical fields are not inferred by this renderer.</p></main></body></html>"
    )
    return "".join(parts)
