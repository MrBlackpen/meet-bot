# backend/app/api/confirm.py
from fastapi import APIRouter, HTTPException
from app.db.database import SessionLocal
from app.db.models import ExecutionLog
from app.automation.router import route_intent
import json

router = APIRouter()

@router.post("/confirm/{log_id}")
def confirm_action(log_id: int):
    db = SessionLocal()
    log = db.query(ExecutionLog).filter(
        ExecutionLog.id == log_id,
        ExecutionLog.status == "pending"
    ).first()

    if not log:
        db.close()
        raise HTTPException(status_code=404, detail="Pending action not found")

    # Rebuild minimal intent object
    intent = type("Intent", (), {
        "intent_type": log.intent_type,
        "details": {},
        "speaker": log.speaker,
        "source_sentence": log.source_sentence
    })

    try:
        result = route_intent(intent)
        log.status = "executed"
        log.approved = True
        log.result = json.dumps(result)

    except Exception as e:
        log.status = "failed"
        log.error = str(e)

    db.commit()
    db.close()

    return {"status": "approved", "log_id": log_id}

@router.post("/reject/{log_id}")
def reject_action(log_id: int):
    db = SessionLocal()
    log = db.query(ExecutionLog).filter(
        ExecutionLog.id == log_id,
        ExecutionLog.status == "pending"
    ).first()

    if not log:
        db.close()
        raise HTTPException(status_code=404, detail="Pending action not found")

    log.status = "rejected"
    db.commit()
    db.close()

    return {"status": "rejected", "log_id": log_id}
