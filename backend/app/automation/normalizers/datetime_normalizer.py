# backend/app/automation/normalizers/datetime_normalizer.py
from datetime import datetime, timedelta
import re

def normalize_datetime(natural_text: str):
    """
    Normalize natural language or ISO date + time strings into (YYYY-MM-DD, HH:MM)
    """
    text = natural_text.lower().strip()
    print(f"Input to normalizer: '{text}'")

    now = datetime.now()

    # ────────────────────────────────────────────────
    # 1. Try to extract full ISO date (YYYY-MM-DD)
    # ────────────────────────────────────────────────
    iso_date_match = re.search(r'\b(\d{4}-\d{2}-\d{2})\b', text)
    if iso_date_match:
        date_str = iso_date_match.group(1)
        # Try to parse it to validate
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            date_str = None
    else:
        date_str = None

    # ────────────────────────────────────────────────
    # 2. Extract time (12h or 24h formats)
    # ────────────────────────────────────────────────
    time_match_12h = re.search(
        r'\b(\d{1,2})(?::(\d{2}))?\s*(am|pm)\b',
        text, re.IGNORECASE
    )
    time_match_24h = re.search(
        r'\b(\d{1,2}):(\d{2})\b',
        text
    )

    time_match = time_match_12h or time_match_24h

    if time_match:
        if time_match_12h:
            hour = int(time_match.group(1))
            minute = int(time_match.group(2) or 0)
            meridian = time_match.group(3).lower() if time_match.group(3) else None
            if meridian == "pm" and hour != 12:
                hour += 12
            if meridian == "am" and hour == 12:
                hour = 0
        else:  # 24h
            hour = int(time_match.group(1))
            minute = int(time_match.group(2))
        time_str = f"{hour:02d}:{minute:02d}"
    else:
        raise ValueError("Time not found in input")

    # ────────────────────────────────────────────────
    # 3. Determine date
    # ────────────────────────────────────────────────
    if date_str:
        # We already have valid ISO date
        return date_str, time_str

    # Natural relative dates
    if "tomorrow" in text:
        date = now + timedelta(days=1)
    elif "today" in text:
        date = now
    elif "day after tomorrow" in text:
        date = now + timedelta(days=2)
    elif "next monday" in text:  # basic weekday support
        days_ahead = (0 - now.weekday() + 7) % 7 + 1  # next Monday
        if days_ahead == 0: days_ahead = 7
        date = now + timedelta(days=days_ahead)
    else:
        raise ValueError("Unsupported date format — no ISO date or known relative term found")

    return date.strftime("%Y-%m-%d"), time_str