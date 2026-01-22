# backend/app/schemas/transcript_schema.py
from pydantic import BaseModel
from datetime import datetime


class TranscriptAppendRequest(BaseModel):
    session_id: str
    speaker: str
    text: str
    timestamp: datetime


class TranscriptFinalizeRequest(BaseModel):
    session_id: str
    ended_at: datetime
