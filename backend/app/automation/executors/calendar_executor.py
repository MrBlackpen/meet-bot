# backend/app/automation/executors/calendar_executor.py
from app.services.google_auth_service import get_google_service
from app.automation.normalizers.datetime_normalizer import normalize_datetime
from app.automation.normalizers.attendee_normalizer import normalize_attendees
from datetime import datetime, timedelta

def create_calendar_event(details: dict):
    service = get_google_service("calendar", "v3")
    title = details.get("topic", "Meeting")
    raw_date = details.get("date", "today")  # Default to today if no date
    raw_time = details.get("time")
    raw_attendees = details.get("attendees")
    
    if not raw_time:
        raise ValueError("Time information missing")
    
    # Combine into full phrase for normalizer
    natural_text = f"{raw_date} at {raw_time}"
    
    date, time = normalize_datetime(natural_text)
    attendees = normalize_attendees(raw_attendees)
    
    start_dt = f"{date}T{time}:00"
    end_dt = (
        datetime.fromisoformat(start_dt) + timedelta(hours=1)
    ).isoformat()
    
    event = {
        "summary": title,
        "start": {
            "dateTime": start_dt,
            "timeZone": "Asia/Kolkata",
        },
        "end": {
            "dateTime": end_dt,
            "timeZone": "Asia/Kolkata",
        },
        "attendees": [{"email": a} for a in attendees],
    }
    created = service.events().insert(
        calendarId="primary",
        body=event
    ).execute()
    return {
        "action": "calendar_event_created",
        "event_id": created["id"],
        "link": created["htmlLink"]
    }