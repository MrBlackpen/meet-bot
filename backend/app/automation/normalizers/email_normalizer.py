# backend/app/automation/normalizers/email_normalizer.py
def normalize_email_details(intent):
    """
    Converts semantic intent details into
    executable email fields
    """

    details = intent.details
    intent_type = intent.intent_type

    # Recipient
    to = (
        details.get("to")
        or details.get("recipient")
        or details.get("email")
    )

    if not to:
        raise ValueError("Recipient email missing")

    # Subject
    if intent_type == "SHARE_DOCUMENT":
        subject = f"Sharing: {details.get('document_name', 'Document')}"
        body = (
            f"Hi,\n\n"
            f"I am sharing the {details.get('document_name')} as discussed.\n\n"
            f"I’ll follow up with the document shortly.\n\n"
            f"Regards"
        )

    elif intent_type == "FOLLOW_UP":
        subject = "Follow-up"
        body = "Following up on our previous discussion."

    else:
        subject = details.get("subject", "Message")
        body = details.get("body", "")

    return {
        "to": to,
        "subject": subject,
        "body": body
    }
