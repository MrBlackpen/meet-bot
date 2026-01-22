# backend/app/automation/router.py
from app.automation.executors.calendar_executor import create_calendar_event
from app.automation.executors.email_executor import send_email
from app.automation.normalizers.email_normalizer import normalize_email_details

def route_intent(intent):
    intent_type = intent.intent_type
    details = intent.details

    if intent_type in ["SCHEDULE_MEETING", "ADD_REMINDER"]:
        return create_calendar_event(details)

    if intent_type in ["SEND_EMAIL", "FOLLOW_UP", "SHARE_DOCUMENT", "SEND_REMINDER"]:
        email_payload = normalize_email_details(intent)
        return send_email(email_payload)

    # Safe fallback
    return {"info": "No automation mapped for this intent"}
