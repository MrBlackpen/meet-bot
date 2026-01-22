# backend/app/automation/executors/email_executor.py
import base64
from email.mime.text import MIMEText
from app.services.google_auth_service import get_google_service

def send_email(details: dict):
    """
    Sends a real email using Gmail API
    """

    to = details.get("to")
    subject = details.get("subject", "Follow-up")
    body = details.get("body", "")

    if not to:
        raise ValueError("Recipient email missing")

    gmail = get_google_service("gmail", "v1")

    message = MIMEText(body)
    message["to"] = to
    message["subject"] = subject

    raw_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    sent = gmail.users().messages().send(
        userId="me",
        body={"raw": raw_message}
    ).execute()

    return {
        "action": "email_sent",
        "to": to,
        "message_id": sent["id"]
    }
