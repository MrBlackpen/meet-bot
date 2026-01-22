# backend/app/automation/logger.py
from app.db.database import SessionLocal
from app.db.models import ExecutionLog

def log_execution(intent, status, result=None, error=None, approved=False):
    db = SessionLocal()

    log = ExecutionLog(
        intent_type=intent.intent_type,
        speaker=intent.speaker,
        source_sentence=intent.source_sentence,
        status=status,
        approved=approved,
        result=str(result) if result else None,
        error=error
    )

    db.add(log)
    db.commit()
    db.refresh(log)
    db.close()

    return log.id
