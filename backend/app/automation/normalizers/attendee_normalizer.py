# backend/app/automation/normalizers/attendee_normalizer.py
def normalize_attendees(raw):
    """
    For MVP:
    - Team names → empty list
    - Emails → list
    """

    if isinstance(raw, list):
        return raw

    if isinstance(raw, str):
        if "@" in raw:
            return [raw]

    return []   # teams like "backend team"
