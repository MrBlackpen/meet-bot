# backend/app/automation/safety_guard.py
CONFIDENCE_THRESHOLD = 0.85

def missing_fields(intent):
    if intent.intent_type == "SCHEDULE_MEETING":
        if "time" not in intent.details:
            return ["time"]
    return []


def should_execute(intent):
    missing = missing_fields(intent)

    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"

    confidence = intent.confidence or 0.0

    if confidence < CONFIDENCE_THRESHOLD:
        return False, "Low confidence"

    return True, "Approved"
