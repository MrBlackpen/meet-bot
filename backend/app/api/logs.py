# backend/app/api/logs.py
from fastapi import APIRouter
from app.db.database import SessionLocal
from app.db.models import ExecutionLog

router = APIRouter()

@router.get("/logs")
def get_logs():
    db = SessionLocal()
    logs = db.query(ExecutionLog).order_by(
        ExecutionLog.created_at.desc()
    ).all()
    db.close()

    return logs
