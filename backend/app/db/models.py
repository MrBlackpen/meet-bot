# backend/app/db/models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from datetime import datetime
from app.db.database import Base

class ExecutionLog(Base):
    __tablename__ = "execution_logs"

    id = Column(Integer, primary_key=True, index=True)
    intent_type = Column(String, index=True)
    speaker = Column(String)
    source_sentence = Column(Text)

    status = Column(String)  # pending / executed / failed / rejected
    approved = Column(Boolean, default=False)

    result = Column(Text, nullable=True)
    error = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)


class TranscriptSession(Base):
    __tablename__ = "transcript_sessions"

    session_id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    finalized_at = Column(DateTime, nullable=True)

    is_finalized = Column(Boolean, default=False)