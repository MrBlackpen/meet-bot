# backend/app/api/transcript.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.transcript_schema import (
    TranscriptAppendRequest,
    TranscriptFinalizeRequest
)
from app.services.transcript_service import (
    append_line,
    read_full_transcript
)
from app.services.transcript_session_service import finalize_session
from app.agents.intent_agent import detect_intents
from app.db.database import get_db
from app.automation.action_dispatcher import execute_intents

router = APIRouter(prefix="/api/transcript", tags=["Transcript"])

@router.post("/append")
def append_transcript_line(
    req: TranscriptAppendRequest,
    db: Session = Depends(get_db)
):
    # Ensure session exists
    from app.services.transcript_session_service import get_or_create_session
    get_or_create_session(db, req.session_id)

    line = f"{req.timestamp.isoformat()} | {req.speaker}: {req.text}"

    try:
        append_line(req.session_id, line)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"status": "ok"}


@router.post("/finalize")
def finalize_transcript(
    req: TranscriptFinalizeRequest,
    db: Session = Depends(get_db)
):
    # 🔐 Idempotency guard
    first_time = finalize_session(db, req.session_id)
    if not first_time:
        return {
            "status": "already_finalized",
            "session_id": req.session_id
        }

    try:
        transcript_text = read_full_transcript(req.session_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Transcript not found")

    if not transcript_text.strip():
        return {
            "status": "finalized",
            "session_id": req.session_id,
            "ended_at": req.ended_at,
            "intents": [],
            "note": "No transcript data captured"
        }


    # 🧠 SINGLE LLM CALL
    intents = detect_intents(transcript_text)
    execution_results = execute_intents(intents)

    return {
        "status": "finalized",
        "session_id": req.session_id,
        "ended_at": req.ended_at,
        "intents": intents.model_dump(),
        "automation": execution_results
    }

@router.get("/replay/{session_id}")
def replay_transcript(session_id: str):
    """
    Allows replaying transcript for debugging or reprocessing.
    """
    try:
        transcript = read_full_transcript(session_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Transcript not found")

    return {
        "session_id": session_id,
        "transcript": transcript
    }
