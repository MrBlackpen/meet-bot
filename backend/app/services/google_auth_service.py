# backend/app/services/google_auth_service.py
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/gmail.send"
]

def get_google_service(service_name, version):
    creds = None

    if os.path.exists("app/config/token.json"):
        creds = Credentials.from_authorized_user_file(
            "app/config/token.json", SCOPES
        )

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "app/config/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("app/config/token.json", "w") as token:
            token.write(creds.to_json())

    return build(service_name, version, credentials=creds)
