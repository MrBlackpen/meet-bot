# backend/app/api/clarify.py
from fastapi import APIRouter
from app.db.database import SessionLocal
from app.db.models import ExecutionLog

router = APIRouter()

@router.get("/clarify/{log_id}")
def get_clarification(log_id: int):
    db = SessionLocal()
    log = db.query(ExecutionLog).filter(
        ExecutionLog.id == log_id,
        ExecutionLog.status == "pending"
    ).first()
    db.close()

    if not log:
        return {"message": "No clarification needed"}

    return {
        "message": "Additional information required",
        "missing": log.error
    }
