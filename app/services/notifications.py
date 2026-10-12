from app.services.recipients import route


def package(snapshot, decision):
    recipients = route(snapshot, decision["posture"])
    if decision["status"] == "rejected":
        for person in recipients:
            person.update(
                routing_status="excluded",
                channel=None,
                reason="Assessment rejected; no notification queued",
                instruction="No notification package for a rejected assessment.",
                follow_up=None,
            )
    for person in recipients:
        person["notification_status"] = (
            "queued_demo" if person["routing_status"] == "included" else "draft"
        )
        person["subject"] = (
            f"ClosureCall prototype: {decision['posture'] or 'rejected'} — {snapshot['facility']['display_name']}"
        )
        follow_up = f"Follow-up: {person['follow_up']}\n" if person["follow_up"] else ""
        person["message"] = (
            f"{person['name']},\n{person['instruction']}\n{follow_up}"
            f"Work period: {decision['effective_window']['start']} to {decision['effective_window']['end']}\n"
            f"Confirmed timing: {decision.get('timing_at') or 'Not applicable'}\n"
            f"Manager reason: {decision['reason']}\n"
            f"{snapshot['assessment']['protective_action_notice']}\n\n"
            "SYNTHETIC RECIPIENT / PROTOTYPE DEMO OUTBOX — no email, SMS or voice call sent. Not an official USDA notice."
        )
    return {
        "mode": "outbox_only",
        "batch_id": decision["decision_id"],
        "recipients": recipients,
        "counts": {
            s: sum(x["routing_status"] == s for x in recipients)
            for s in ("included", "excluded", "deferred")
        },
    }
